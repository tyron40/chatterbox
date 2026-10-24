"""Authenticated, reusable voice API. Run on a Python host with model compute."""
import os
import secrets
import tempfile
import threading
from pathlib import Path

from fastapi import FastAPI, Depends, Header, HTTPException, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel, Field

app = FastAPI(title="Chatterbox Voice API", version="0.1.0", docs_url=None, redoc_url=None)
inference_lock = threading.Lock()
stt_model = None

def authorize(authorization: str | None = Header(default=None)):
    key = os.environ.get("VOICE_API_KEY")
    if not key:
        raise HTTPException(status_code=503, detail="VOICE_API_KEY is not configured")
    if not authorization or not secrets.compare_digest(authorization, "Bearer " + key):
        raise HTTPException(status_code=401, detail="Unauthorized")

class SpeakRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    voice: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "chatterbox-voice", "stt_engine": "faster-whisper (optional)", "tts_engine": "chatterbox"}

@app.post("/v1/speech", dependencies=[Depends(authorize)])
def speech(payload: SpeakRequest):
    """Returns WAV; loads model lazily. One inference at a time to bound GPU use."""
    if not inference_lock.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="Voice engine busy; retry later")
    try:
        import io
        import soundfile as sf
        import torch
        from modules.model_manager import model_manager
        from modules.voice_manager import resolve_voice_path
        model = model_manager.get_tts_model()
        if model is None:
            raise HTTPException(status_code=503, detail="Speech model unavailable")
        voice_path = resolve_voice_path(payload.voice, "en") if payload.voice else None
        if payload.voice and not voice_path:
            raise HTTPException(status_code=404, detail="Requested voice unavailable")
        if not voice_path and model.conds is None:
            raise HTTPException(status_code=422, detail="A configured voice sample is required")
        with torch.inference_mode():
            wav = model.generate(payload.text, audio_prompt_path=voice_path)
        audio = io.BytesIO()
        sf.write(audio, wav.squeeze().detach().cpu().numpy(), model.sr, format="WAV")
        return Response(audio.getvalue(), media_type="audio/wav", headers={"Cache-Control": "no-store"})
    finally:
        inference_lock.release()

@app.post("/v1/transcriptions", dependencies=[Depends(authorize)])
async def transcribe(file: UploadFile = File(...)):
    """Optional local faster-whisper engine. No uploads are persisted."""
    global stt_model
    max_bytes = 12 * 1024 * 1024
    if not inference_lock.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="Voice engine busy; retry later")
    path = None
    try:
        data = await file.read(max_bytes + 1)
        if not data or len(data) > max_bytes:
            raise HTTPException(status_code=413, detail="Audio must be 1 byte to 12 MB")
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in {".wav", ".mp3", ".m4a", ".ogg", ".flac", ".webm"}:
            raise HTTPException(status_code=415, detail="Unsupported audio format")
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            raise HTTPException(status_code=503, detail="Install optional faster-whisper dependency")
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(data)
            path = tmp.name
        if stt_model is None:
            stt_model = WhisperModel(os.getenv("STT_MODEL_SIZE", "base"), device="cpu", compute_type="int8")
        segments, info = stt_model.transcribe(path, vad_filter=True)
        return {"text": " ".join(s.text.strip() for s in segments).strip(), "language": info.language}
    finally:
        if path:
            Path(path).unlink(missing_ok=True)
        inference_lock.release()
