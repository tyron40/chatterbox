"""
Chatterbox TTS API - FastAPI Voice Upload & Generation Service
Deployed on Render with Supabase Storage
"""
import os
import uuid
import io
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from supabase import create_client
import torch
import numpy as np

# Import your TTS modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.model_manager import model_manager
from modules.generation_functions import generate_turbo_speech, generate_speech

app = FastAPI(
    title="Chatterbox TTS API",
    description="Voice cloning and text-to-speech API with Supabase storage",
    version="1.0.0"
)

# ✅ Allow apps + websites to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can lock this down
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase configuration - lazy initialization to prevent boot crashes
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "voices")

def get_supabase():
    """
    Lazy Supabase client initialization
    Only creates client when actually needed, preventing boot crashes
    """
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Supabase not configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables."
        )
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        

@app.get("/")
def root():
    """API root endpoint"""
    return {
        "name": "Chatterbox TTS API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "upload_voice": "/upload-voice",
            "list_voices": "/voices",
            "generate_audio": "/generate"
        }
    }


@app.get("/health")
def health():
    """Health check endpoint - works even without Supabase"""
    supabase_connected = bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)
    return {
        "ok": True,
        "supabase_connected": supabase_connected,
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }
    

@app.post("/upload-voice")
async def upload_voice(
    file: UploadFile = File(...),
    name: str = Form(""),
    gender: str = Form("male"),
    language: str = Form("en")
):
    """
    Upload a voice file to Supabase storage
    
    Parameters:
    - file: Audio file (WAV, MP3, FLAC, M4A)
    - name: Voice name (optional)
    - gender: male or female (default: male)
    - language: Language code (default: en)
    
    Returns:
    - id: Unique voice ID
    - name: Voice name
    - url: Public URL to the voice file
    - gender: Voice gender
    - language: Voice language
    """
    supabase = get_supabase()  # Lazy init
    
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Only audio files allowed")

    voice_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1] if "." in file.filename else "wav"
    
    # Create filename with metadata
    filename = f"{voice_id}_{gender}_{language}.{ext}"

    file_bytes = await file.read()

    try:
        supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=filename,
            file=file_bytes,
            file_options={"content-type": file.content_type},
        )

        url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)

        return {
            "id": voice_id,
            "name": name or file.filename,
            "url": url,
            "gender": gender,
            "language": language,
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/voices")
def list_voices():
    """
    List all uploaded voices from Supabase storage
    
    Returns:
    - List of voice objects with name, url, gender, language
    """
    supabase = get_supabase()  # Lazy init
    
    try:
        res = supabase.storage.from_(SUPABASE_BUCKET).list()

        output = []
        for item in res:
            fname = item.get("name")
            if fname:
                # Parse metadata from filename
                parts = fname.replace(".wav", "").replace(".mp3", "").replace(".flac", "").split("_")
                voice_id = parts[0] if len(parts) > 0 else "unknown"
                gender = parts[1] if len(parts) > 1 else "unknown"
                language = parts[2] if len(parts) > 2 else "en"
                
                output.append({
                    "id": voice_id,
                    "name": fname,
                    "url": supabase.storage.from_(SUPABASE_BUCKET).get_public_url(fname),
                    "gender": gender,
                    "language": language
                })

        return {"voices": output, "count": len(output)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list voices: {str(e)}")


@app.post("/generate")
async def generate_audio(
    text: str = Form(...),
    voice_url: str = Form(None),
    model_type: str = Form("turbo")
):
    """
    Generate speech from text using a voice
    
    Parameters:
    - text: Text to convert to speech
    - voice_url: URL of the voice file (from /upload-voice or /voices)
    - model_type: "turbo" or "standard" (default: turbo)
    
    Returns:
    - Audio file (WAV format)
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Download voice file if URL provided
        voice_path = None
        if voice_url:
            import requests
            response = requests.get(voice_url)
            if response.status_code == 200:
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(response.content)
                    voice_path = tmp.name
        
        # Generate audio using your TTS model
        if model_type == "turbo":
            # Use turbo model
            model = model_manager.get_turbo_model()
            if model is None:
                raise HTTPException(status_code=500, detail="Failed to load Turbo model")
            
            # Generate audio
            wav = model.generate(text, audio_prompt_path=voice_path)
        else:
            # Use standard model
            model = model_manager.get_tts_model()
            if model is None:
                raise HTTPException(status_code=500, detail="Failed to load TTS model")
            
            wav = model.generate(
                text,
                audio_prompt_path=voice_path,
                exaggeration=0.5,
                temperature=0.8,
                cfg_weight=0.5
            )
        
        # Convert to WAV bytes
        import scipy.io.wavfile as wavfile
        wav_io = io.BytesIO()
        
        # Convert tensor to numpy
        if hasattr(wav, 'cpu'):
            wav_numpy = wav.squeeze(0).cpu().numpy()
        else:
            wav_numpy = wav.squeeze(0).numpy()
        
        # Convert to int16
        wav_int16 = (wav_numpy * 32767).astype(np.int16)
        
        # Write to BytesIO
        wavfile.write(wav_io, model.sr, wav_int16)
        wav_io.seek(0)
        
        # Clean up temp file
        if voice_path and os.path.exists(voice_path):
            os.unlink(voice_path)
        
        return StreamingResponse(
            wav_io,
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; filename=generated_{uuid.uuid4()}.wav"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.delete("/voices/{voice_id}")
def delete_voice(voice_id: str):
    """
    Delete a voice from Supabase storage
    
    Parameters:
    - voice_id: The voice ID to delete
    
    Returns:
    - Success message
    """
    supabase = get_supabase()  # Lazy init
    
    try:
        # List all files and find matching voice_id
        res = supabase.storage.from_(SUPABASE_BUCKET).list()
        
        files_to_delete = []
        for item in res:
            fname = item.get("name")
            if fname and fname.startswith(voice_id):
                files_to_delete.append(fname)
        
        if not files_to_delete:
            raise HTTPException(status_code=404, detail="Voice not found")
        
        # Delete files
        for fname in files_to_delete:
            supabase.storage.from_(SUPABASE_BUCKET).remove([fname])
        
        return {
            "success": True,
            "message": f"Deleted {len(files_to_delete)} file(s)",
            "deleted_files": files_to_delete
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
