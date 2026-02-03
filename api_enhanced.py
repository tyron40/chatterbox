"""
Chatterbox TTS Enhanced API - Complete Feature Set
Includes: Default Voices, Voice Conversion, Multilingual TTS, Turbo TTS
"""
import os
import uuid
import io
import tempfile
import shutil
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from supabase import create_client

# Add project root to path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Lazy imports for heavy dependencies
_torch = None
_np = None
_model_manager = None
_generation_functions = None
_voice_manager = None
_scipy_wavfile = None

def get_torch():
    """Lazy import torch"""
    global _torch
    if _torch is None:
        try:
            import torch
            _torch = torch
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to import torch: {str(e)}")
    return _torch

def get_numpy():
    """Lazy import numpy"""
    global _np
    if _np is None:
        try:
            import numpy as np
            _np = np
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to import numpy: {str(e)}")
    return _np

def get_model_manager():
    """Lazy import model_manager"""
    global _model_manager
    if _model_manager is None:
        try:
            from modules.model_manager import model_manager
            _model_manager = model_manager
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to import model_manager: {str(e)}")
    return _model_manager

def get_generation_functions():
    """Lazy import generation functions"""
    global _generation_functions
    if _generation_functions is None:
        try:
            from modules import generation_functions
            _generation_functions = generation_functions
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to import generation_functions: {str(e)}")
    return _generation_functions

def get_voice_manager():
    """Lazy import voice_manager"""
    global _voice_manager
    if _voice_manager is None:
        try:
            from modules import voice_manager
            _voice_manager = voice_manager
            # Load voices on first import
            _voice_manager.load_voices()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to import voice_manager: {str(e)}")
    return _voice_manager

def get_scipy_wavfile():
    """Lazy import scipy.io.wavfile"""
    global _scipy_wavfile
    if _scipy_wavfile is None:
        try:
            import scipy.io.wavfile as wavfile
            _scipy_wavfile = wavfile
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to import scipy.io.wavfile: {str(e)}")
    return _scipy_wavfile

app = FastAPI(
    title="Chatterbox TTS Enhanced API",
    description="Complete voice cloning, text-to-speech, voice conversion & multilingual TTS API",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase configuration - lazy initialization
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "voices")

def get_supabase():
    """Lazy Supabase client initialization"""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Supabase not configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables."
        )
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# ============================================================================
# ROOT & HEALTH ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """API root endpoint with all available endpoints"""
    return {
        "name": "Chatterbox TTS Enhanced API",
        "version": "2.0.0",
        "description": "Complete TTS solution with voice cloning, conversion & multilingual support",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "default_voices": "/default-voices",
            "list_voices": "/voices",
            "upload_voice": "/upload-voice",
            "delete_voice": "/voices/{voice_id}",
            "generate_tts": "/generate/tts",
            "generate_multilingual": "/generate/multilingual",
            "generate_turbo": "/generate/turbo",
            "convert_voice": "/convert-voice",
            "supported_languages": "/languages"
        },
        "features": [
            "30+ Default Celebrity & Character Voices",
            "Voice Cloning & Upload",
            "23 Language Support",
            "Voice Conversion (Voice-to-Voice)",
            "Turbo TTS (3x faster)",
            "Paralinguistic Tags Support"
        ]
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    supabase_connected = bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)
    
    device = "unknown"
    try:
        torch = get_torch()
        device = "cuda" if torch.cuda.is_available() else "cpu"
    except:
        device = "not_loaded"
    
    return {
        "ok": True,
        "supabase_connected": supabase_connected,
        "device": device,
        "version": "2.0.0"
    }


# ============================================================================
# VOICE MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/default-voices")
def get_default_voices():
    """
    Get all default voices available in the system
    
    Returns:
    - List of default voice objects with name, gender, language, and file path
    """
    try:
        voice_manager = get_voice_manager()
        
        voices = []
        for voice_name, voice_path in voice_manager.VOICES["samples"].items():
            # Parse voice metadata from filename
            gender, language = None, "en"
            
            # Extract gender
            if voice_name.endswith("_male"):
                gender = "male"
                base_name = voice_name[:-5]
            elif voice_name.endswith("_female"):
                gender = "female"
                base_name = voice_name[:-7]
            else:
                base_name = voice_name
                gender = "unknown"
            
            # Extract language (if present)
            lang_codes = ["ar", "da", "de", "el", "es", "fi", "fr", "he", "hi", "it", "ja", "ko", "ms", "nl", "no", "pl", "pt", "ru", "sv", "sw", "tr", "zh"]
            for lang in lang_codes:
                if base_name.endswith(f"_{lang}"):
                    language = lang
                    base_name = base_name[:-3]  # Remove language suffix
                    break
            
            voices.append({
                "id": voice_name,
                "name": base_name,
                "display_name": voice_manager.format_voice_display_name(voice_name),
                "gender": gender,
                "language": language,
                "is_default": True
            })
        
        return {
            "voices": voices,
            "count": len(voices),
            "message": f"Found {len(voices)} default voices"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load default voices: {str(e)}")


@app.get("/voices")
def list_voices(include_defaults: bool = True):
    """
    List all voices (uploaded + default)
    
    Parameters:
    - include_defaults: Include default system voices (default: True)
    
    Returns:
    - List of voice objects
    """
    all_voices = []
    
    # Get default voices if requested
    if include_defaults:
        try:
            default_response = get_default_voices()
            all_voices.extend(default_response["voices"])
        except:
            pass
    
    # Get uploaded voices from Supabase
    try:
        supabase = get_supabase()
        res = supabase.storage.from_(SUPABASE_BUCKET).list()
        
        for item in res:
            fname = item.get("name")
            if fname:
                parts = fname.replace(".wav", "").replace(".mp3", "").replace(".flac", "").split("_")
                voice_id = parts[0] if len(parts) > 0 else "unknown"
                gender = parts[1] if len(parts) > 1 else "unknown"
                language = parts[2] if len(parts) > 2 else "en"
                
                all_voices.append({
                    "id": voice_id,
                    "name": fname,
                    "display_name": fname,
                    "url": supabase.storage.from_(SUPABASE_BUCKET).get_public_url(fname),
                    "gender": gender,
                    "language": language,
                    "is_default": False
                })
    except:
        # Supabase not configured, only return defaults
        pass
    
    return {
        "voices": all_voices,
        "count": len(all_voices),
        "default_count": sum(1 for v in all_voices if v.get("is_default")),
        "uploaded_count": sum(1 for v in all_voices if not v.get("is_default"))
    }


@app.post("/upload-voice")
async def upload_voice(
    file: UploadFile = File(...),
    name: str = Form(""),
    gender: str = Form("male"),
    language: str = Form("en")
):
    """Upload a custom voice file to Supabase storage"""
    supabase = get_supabase()
    
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Only audio files allowed")

    voice_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1] if "." in file.filename else "wav"
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
            "filename": filename,
            "is_default": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.delete("/voices/{voice_id}")
def delete_voice(voice_id: str):
    """Delete an uploaded voice from Supabase storage"""
    supabase = get_supabase()
    
    try:
        res = supabase.storage.from_(SUPABASE_BUCKET).list()
        
        files_to_delete = []
        for item in res:
            fname = item.get("name")
            if fname and fname.startswith(voice_id):
                files_to_delete.append(fname)
        
        if not files_to_delete:
            raise HTTPException(status_code=404, detail="Voice not found")
        
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


# ============================================================================
# LANGUAGE SUPPORT ENDPOINT
# ============================================================================

@app.get("/languages")
def get_supported_languages():
    """Get list of all supported languages for multilingual TTS"""
    from modules.config import SUPPORTED_LANGUAGES, LANGUAGE_CONFIG
    
    languages = []
    for code, name in SUPPORTED_LANGUAGES.items():
        languages.append({
            "code": code,
            "name": name,
            "has_default_voice": code in LANGUAGE_CONFIG and "audio" in LANGUAGE_CONFIG[code]
        })
    
    return {
        "languages": languages,
        "count": len(languages),
        "message": f"Supports {len(languages)} languages"
    }


# ============================================================================
# TEXT-TO-SPEECH GENERATION ENDPOINTS
# ============================================================================

@app.post("/generate/tts")
async def generate_tts(
    text: str = Form(...),
    voice_id: str = Form(None),
    voice_url: str = Form(None),
    exaggeration: float = Form(0.5),
    temperature: float = Form(0.8),
    cfg_weight: float = Form(0.5),
    min_p: float = Form(0.05),
    top_p: float = Form(1.0),
    repetition_penalty: float = Form(1.2),
    seed: int = Form(0)
):
    """
    Generate English speech using standard TTS model
    
    Parameters:
    - text: Text to convert to speech
    - voice_id: ID of default voice or uploaded voice
    - voice_url: URL of voice file (alternative to voice_id)
    - exaggeration: Voice exaggeration (0.0-1.0, default: 0.5)
    - temperature: Sampling temperature (0.0-2.0, default: 0.8)
    - cfg_weight: Classifier-free guidance weight (0.0-1.0, default: 0.5)
    - min_p: Minimum probability threshold (0.0-1.0, default: 0.05)
    - top_p: Top-p sampling (0.0-1.0, default: 1.0)
    - repetition_penalty: Repetition penalty (1.0-2.0, default: 1.2)
    - seed: Random seed (0 for random, default: 0)
    
    Returns:
    - Audio file (WAV format)
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        np = get_numpy()
        model_manager = get_model_manager()
        voice_manager = get_voice_manager()
        wavfile = get_scipy_wavfile()
        
        # Resolve voice path
        voice_path = None
        if voice_id:
            # Check if it's a default voice
            if voice_id in voice_manager.VOICES["samples"]:
                voice_path = voice_manager.VOICES["samples"][voice_id]
            else:
                # Try to resolve using voice_manager
                voice_path = voice_manager.resolve_voice_path(voice_id, "en")
        elif voice_url:
            # Download voice from URL
            import requests
            response = requests.get(voice_url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(response.content)
                    voice_path = tmp.name
        
        # Load model
        model = model_manager.get_tts_model()
        if model is None:
            raise HTTPException(status_code=500, detail="Failed to load TTS model")
        
        # Set seed if specified
        if seed != 0:
            from modules.generation_functions import set_seed
            set_seed(seed)
        
        # Generate audio
        from modules.generation_functions import smart_chunk_text
        text_chunks = smart_chunk_text(text)
        generated_wavs = []
        
        for chunk in text_chunks:
            chunk_wav = model.generate(
                chunk,
                audio_prompt_path=voice_path,
                exaggeration=exaggeration,
                temperature=temperature,
                cfg_weight=cfg_weight,
                min_p=min_p,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
            )
            generated_wavs.append(chunk_wav)
        
        # Concatenate chunks
        torch = get_torch()
        if len(generated_wavs) > 1:
            full_wav = torch.cat(generated_wavs, dim=-1)
        else:
            full_wav = generated_wavs[0]
        
        # Convert to WAV bytes
        wav_io = io.BytesIO()
        wav_numpy = full_wav.squeeze(0).cpu().numpy() if hasattr(full_wav, 'cpu') else full_wav.squeeze(0).numpy()
        wav_int16 = (wav_numpy * 32767).astype(np.int16)
        wavfile.write(wav_io, model.sr, wav_int16)
        wav_io.seek(0)
        
        # Clean up temp file
        if voice_path and voice_url and os.path.exists(voice_path):
            os.unlink(voice_path)
        
        return StreamingResponse(
            wav_io,
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename=tts_{uuid.uuid4()}.wav"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/generate/multilingual")
async def generate_multilingual(
    text: str = Form(...),
    language: str = Form(...),
    voice_id: str = Form(None),
    voice_url: str = Form(None),
    exaggeration: float = Form(0.5),
    temperature: float = Form(0.8),
    cfg_weight: float = Form(0.5),
    seed: int = Form(0)
):
    """
    Generate speech in any of 23 supported languages
    
    Parameters:
    - text: Text to convert to speech
    - language: Language code (ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh)
    - voice_id: ID of default voice or uploaded voice
    - voice_url: URL of voice file (alternative to voice_id)
    - exaggeration: Voice exaggeration (0.0-1.0, default: 0.5)
    - temperature: Sampling temperature (0.0-2.0, default: 0.8)
    - cfg_weight: Classifier-free guidance weight (0.0-1.0, default: 0.5)
    - seed: Random seed (0 for random, default: 0)
    
    Returns:
    - Audio file (WAV format)
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if not language:
        raise HTTPException(status_code=400, detail="Language code is required")
    
    from modules.config import SUPPORTED_LANGUAGES, LANGUAGE_CONFIG
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    
    try:
        np = get_numpy()
        model_manager = get_model_manager()
        voice_manager = get_voice_manager()
        wavfile = get_scipy_wavfile()
        
        # Resolve voice path
        voice_path = None
        if voice_id:
            if voice_id in voice_manager.VOICES["samples"]:
                voice_path = voice_manager.VOICES["samples"][voice_id]
            else:
                voice_path = voice_manager.resolve_voice_path(voice_id, language)
        elif voice_url:
            import requests
            response = requests.get(voice_url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(response.content)
                    voice_path = tmp.name
        else:
            # Use default voice for language
            audio_url = LANGUAGE_CONFIG.get(language, {}).get("audio")
            if audio_url:
                voice_path = voice_manager.resolve_voice_path(f"Default ({SUPPORTED_LANGUAGES[language]})", language)
        
        # Load model
        model = model_manager.get_mtl_model()
        if model is None:
            raise HTTPException(status_code=500, detail="Failed to load Multilingual model")
        
        # Set seed if specified
        if seed != 0:
            from modules.generation_functions import set_seed
            set_seed(seed)
        
        # Generate audio
        from modules.generation_functions import smart_chunk_text
        text_chunks = smart_chunk_text(text)
        generated_wavs = []
        
        for chunk in text_chunks:
            chunk_wav = model.generate(
                chunk,
                language_id=language,
                audio_prompt_path=voice_path,
                exaggeration=exaggeration,
                temperature=temperature,
                cfg_weight=cfg_weight,
            )
            generated_wavs.append(chunk_wav)
        
        # Concatenate chunks
        torch = get_torch()
        if len(generated_wavs) > 1:
            full_wav = torch.cat(generated_wavs, dim=-1)
        else:
            full_wav = generated_wavs[0]
        
        # Convert to WAV bytes
        wav_io = io.BytesIO()
        wav_numpy = full_wav.squeeze(0).cpu().numpy() if hasattr(full_wav, 'cpu') else full_wav.squeeze(0).numpy()
        wav_int16 = (wav_numpy * 32767).astype(np.int16)
        wavfile.write(wav_io, model.sr, wav_int16)
        wav_io.seek(0)
        
        # Clean up temp file
        if voice_path and voice_url and os.path.exists(voice_path):
            os.unlink(voice_path)
        
        return StreamingResponse(
            wav_io,
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename=multilingual_{language}_{uuid.uuid4()}.wav"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/generate/turbo")
async def generate_turbo(
    text: str = Form(...),
    voice_id: str = Form(...),
    voice_url: str = Form(None)
):
    """
    Generate speech using Turbo model (3x faster, supports paralinguistic tags)
    
    Parameters:
    - text: Text to convert to speech (supports tags: [laugh], [chuckle], [sigh], [gasp], etc.)
    - voice_id: ID of default voice or uploaded voice (REQUIRED for Turbo)
    - voice_url: URL of voice file (alternative to voice_id)
    
    Returns:
    - Audio file (WAV format)
    
    Note: Turbo model requires a reference voice and supports paralinguistic tags
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if not voice_id and not voice_url:
        raise HTTPException(status_code=400, detail="Turbo model requires a voice reference (voice_id or voice_url)")
    
    try:
        np = get_numpy()
        model_manager = get_model_manager()
        voice_manager = get_voice_manager()
        wavfile = get_scipy_wavfile()
        
        # Resolve voice path
        voice_path = None
        if voice_id:
            if voice_id in voice_manager.VOICES["samples"]:
                voice_path = voice_manager.VOICES["samples"][voice_id]
            else:
                voice_path = voice_manager.resolve_voice_path(voice_id, "en")
        elif voice_url:
            import requests
            response = requests.get(voice_url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(response.content)
                    voice_path = tmp.name
        
        if not voice_path:
            raise HTTPException(status_code=400, detail="Voice not found")
        
        # Load model
        model = model_manager.get_turbo_model()
        if model is None:
            raise HTTPException(status_code=500, detail="Failed to load Turbo model")
        
        # Generate audio
        from modules.generation_functions import smart_chunk_text
        text_chunks = smart_chunk_text(text)
        generated_wavs = []
        
        for chunk in text_chunks:
            chunk_wav = model.generate(
                chunk,
                audio_prompt_path=voice_path
            )
            generated_wavs.append(chunk_wav)
        
        # Concatenate chunks
        torch = get_torch()
        if len(generated_wavs) > 1:
            full_wav = torch.cat(generated_wavs, dim=-1)
        else:
            full_wav = generated_wavs[0]
        
        # Convert to WAV bytes
        wav_io = io.BytesIO()
        wav_numpy = full_wav.squeeze(0).cpu().numpy() if hasattr(full_wav, 'cpu') else full_wav.squeeze(0).numpy()
        wav_int16 = (wav_numpy * 32767).astype(np.int16)
        wavfile.write(wav_io, model.sr, wav_int16)
        wav_io.seek(0)
        
        # Clean up temp file
        if voice_path and voice_url and os.path.exists(voice_path):
            os.unlink(voice_path)
        
        return StreamingResponse(
            wav_io,
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename=turbo_{uuid.uuid4()}.wav"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ============================================================================
# VOICE CONVERSION ENDPOINT
# ============================================================================

@app.post("/convert-voice")
async def convert_voice(
    input_audio: UploadFile = File(...),
    target_voice_id: str = Form(None),
    target_voice_url: str = Form(None)
):
    """
    Convert voice from input audio to target voice (Voice Translator)
    
    Parameters:
    - input_audio: Source audio file to convert
    - target_voice_id: ID of target voice (default or uploaded)
    - target_voice_url: URL of target voice file (alternative to target_voice_id)
    
    Returns:
    - Converted audio file (WAV format)
    
    Note: This is the "Voice Translator" feature - converts any voice to sound like the target voice
    """
    if not input_audio:
        raise HTTPException(status_code=400, detail="Input audio file is required")
    
    try:
        np = get_numpy()
        model_manager = get_model_manager()
        voice_manager = get_voice_manager()
        wavfile = get_scipy_wavfile()
        
        # Save input audio to temp file
        input_path = None
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await input_audio.read()
            tmp.write(content)
            input_path = tmp.name
        
        # Resolve target voice path
        target_path = None
        if target_voice_id and target_voice_id != "None":
            # Remove gender symbols if present
            clean_name = target_voice_id.replace(" ♂️", "").replace(" ♀️", "")
            
            # Try to find the voice
            possible_names = [clean_name, f"{clean_name}_male", f"{clean_name}_female"]
            for name in possible_names:
                if name in voice_manager.VOICES["samples"]:
                    target_path = voice_manager.VOICES["samples"][name]
                    break
        elif target_voice_url:
            import requests
            response = requests.get(target_voice_url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(response.content)
                    target_path = tmp.name
        
        # Load model
        model = model_manager.get_vc_model()
        if model is None:
            raise HTTPException(status_code=500, detail="Failed to load Voice Conversion model")
        
        # Convert voice
        wav = model.generate(input_path, target_voice_path=target_path)
        
        # Convert to WAV bytes
        wav_io = io.BytesIO()
        wav_numpy = wav.squeeze(0).cpu().numpy() if hasattr(wav, 'cpu') else wav.squeeze(0).numpy()
        wav_int16 = (wav_numpy * 32767).astype(np.int16)
        wavfile.write(wav_io, model.sr, wav_int16)
        wav_io.seek(0)
        
        # Clean up temp files
        if input_path and os.path.exists(input_path):
            os.unlink(input_path)
        if target_path and target_voice_url and os.path.exists(target_path):
            os.unlink(target_path)
        
        return StreamingResponse(
            wav_io,
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename=converted_{uuid.uuid4()}.wav"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice conversion failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
