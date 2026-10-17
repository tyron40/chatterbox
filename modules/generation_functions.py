"""
Speech generation, conversion, and utility functions for Chatterbox TTS Enhanced
"""
import random
import numpy as np
import torch
import time
import re
import base64
import json
import os
import tempfile
import urllib.error
import urllib.request
from .config import DEVICE, LANGUAGE_CONFIG, SUPPORTED_LANGUAGES
from .model_manager import model_manager
from .voice_manager import resolve_voice_path


def set_seed(seed: int):
    """Set random seed for reproducibility."""
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)


def estimate_generation_time(text_length):
    """Estimate generation time based on text length."""
    return (text_length / 50) * 2 + 1


def format_time(seconds):
    """Format seconds into readable time string."""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes} minute{'s' if minutes != 1 else ''} {seconds:.1f} seconds"


def smart_chunk_text(text, max_words=40):
    """
    Intelligently chunk text based on sentence boundaries and word count.
    Accumulates sentences to maximize chunk size up to max_words.
    Supports all languages including CJK (Chinese, Japanese, Korean).
    """
    # Detect if text contains CJK characters (Chinese, Japanese, Korean)
    def has_cjk(text):
        return bool(re.search(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]', text))
    
    is_cjk = has_cjk(text)
    
    # Enhanced sentence pattern supporting multiple languages
    # Includes: . ! ? (Western), 。！？ (CJK), । (Hindi), ؟ (Arabic)
    sentence_pattern = r'(?<=[.!?。！？।؟])\s*|\n+'
    sentences = re.split(sentence_pattern, text)
    
    chunks = []
    current_chunk = []
    current_count = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Count words (space-separated) or characters (CJK)
        if is_cjk:
            sentence_count = len(re.sub(r'\s+', '', sentence))
        else:
            sentence_count = len(sentence.split())
        
        # Check if adding this sentence exceeds the limit
        if current_count + sentence_count > max_words:
            # If current chunk is not empty, save it
            if current_chunk:
                chunks.append(' '.join(current_chunk) if not is_cjk else ''.join(current_chunk))
                current_chunk = []
                current_count = 0
            
            # If the single sentence itself is longer than max_words, we must split it
            if sentence_count > max_words:
                # Split at commas/semicolons: , ; (Western), ，、； (CJK), ، (Arabic)
                sub_parts = re.split(r'[,;،、；،]\s*', sentence)
                for part in sub_parts:
                    part = part.strip()
                    if not part:
                        continue
                    
                    if is_cjk:
                        part_count = len(re.sub(r'\s+', '', part))
                    else:
                        part_count = len(part.split())
                    
                    if current_count + part_count > max_words and current_chunk:
                        chunks.append(' '.join(current_chunk) if not is_cjk else ''.join(current_chunk))
                        current_chunk = [part]
                        current_count = part_count
                    else:
                        current_chunk.append(part)
                        current_count += part_count
            else:
                # Sentence fits in a new chunk
                current_chunk.append(sentence)
                current_count += sentence_count
        else:
            # Sentence fits in current chunk
            current_chunk.append(sentence)
            current_count += sentence_count
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk) if not is_cjk else ''.join(current_chunk))
    
    return chunks if chunks else [text]


def generate_speech(text, voice_name, exaggeration, temperature, seed_num, cfgw, min_p, top_p, repetition_penalty):
    """Generate speech with progress tracking and validation."""
    try:
        start_time = time.time()
        
        # Input validations
        if not text or not text.strip():
            yield 0, None, "❌ Error: Input text cannot be empty."
            return
        
        if len(text) > 250:
            print(f"ℹ️ Text length: {len(text)} chars - Using smart chunking")
        
        if not voice_name or voice_name == "None":
            audio_prompt_path = None
            yield 10, None, "⚠️ No voice selected - using default voice..."
        else:
            audio_prompt_path = resolve_voice_path(voice_name, "en")
            if not audio_prompt_path:
                yield 0, None, f"❌ Error: Voice '{voice_name}' not found."
                return
            yield 10, None, f"Loading voice: {voice_name}..."
        
        # Load model via manager (handles unloading others)
        yield 20, None, "Loading TTS model..."
        model = model_manager.get_tts_model()
        if model is None:
             yield 0, None, "❌ Error: Failed to load TTS model."
             return
        
        # Set seed if specified
        if seed_num != 0:
            set_seed(int(seed_num))
            yield 30, None, f"Seed set to {seed_num}"
        
        # Chunk text
        text_chunks = smart_chunk_text(text)
        total_chunks = len(text_chunks)
        generated_wavs = []
        
        # Estimate time
        estimated_time = estimate_generation_time(len(text))
        yield 40, None, f"Generating speech (English)...\nChunks: {total_chunks}\nEstimated time: {format_time(estimated_time)}"
        
        # Generate audio for each chunk
        for i, chunk in enumerate(text_chunks):
            progress = 40 + int((i / total_chunks) * 50)
            yield progress, None, f"Generating chunk {i+1}/{total_chunks}..."
            
            chunk_wav = model.generate(
                chunk,
                audio_prompt_path=audio_prompt_path,
                exaggeration=exaggeration,
                temperature=temperature,
                cfg_weight=cfgw,
                min_p=min_p,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
            )
            generated_wavs.append(chunk_wav)
        
        if not generated_wavs:
             yield 0, None, "❌ Error: No audio generated."
             return

        yield 90, None, "Finalizing audio..."
        
        # Concatenate audio chunks
        if len(generated_wavs) > 1:
            full_wav = torch.cat(generated_wavs, dim=-1)
        else:
            full_wav = generated_wavs[0]
        
        # Calculate actual time taken
        total_time = time.time() - start_time
        final_status = f"✅ Generation complete!\nTime taken: {format_time(total_time)}\nText length: {len(text)} chars\nChunks: {total_chunks}"
        
        yield 100, (model.sr, full_wav.squeeze(0).numpy()), final_status
        
    except Exception as e:
        error_status = f"❌ Error generating speech: {str(e)}"
        yield 0, None, error_status


def generate_multilingual_speech(text, voice_name, language_code, exaggeration, temperature, seed_num, cfgw):
    """Generate multilingual speech with progress tracking."""
    try:
        start_time = time.time()
        
        # Input validations
        if not text or not text.strip():
            yield 0, None, "❌ Error: Input text cannot be empty."
            return
        
        if len(text) > 250:
            print(f"ℹ️ Text length: {len(text)} chars - Using smart chunking")
        
        if not language_code:
            yield 0, None, "❌ Error: Please select a language for multilingual TTS."
            return
        
        # Resolve voice path based on language
        if not voice_name or voice_name == "None":
            audio_prompt_path = LANGUAGE_CONFIG.get(language_code, {}).get("audio")
            yield 10, None, f"⚠️ Using default voice for {SUPPORTED_LANGUAGES.get(language_code, language_code)}..."
        else:
            audio_prompt_path = resolve_voice_path(voice_name, language_code)
            if not audio_prompt_path:
                yield 0, None, f"❌ Error: Voice '{voice_name}' not found for {SUPPORTED_LANGUAGES.get(language_code)}."
                return
            yield 10, None, f"Loading voice: {voice_name}..."
        
        # Load model via manager (handles unloading others)
        yield 20, None, "Loading Multilingual TTS model..."
        model = model_manager.get_mtl_model()
        if model is None:
             yield 0, None, "❌ Error: Failed to load Multilingual model."
             return
        
        # Set seed if specified
        if seed_num != 0:
            set_seed(int(seed_num))
            yield 30, None, f"Seed set to {seed_num}"
        
        # Chunk text
        text_chunks = smart_chunk_text(text)
        total_chunks = len(text_chunks)
        generated_wavs = []
        
        # Estimate time
        estimated_time = estimate_generation_time(len(text))
        lang_name = SUPPORTED_LANGUAGES.get(language_code, language_code)
        yield 40, None, f"Generating speech in {lang_name}...\nChunks: {total_chunks}\nEstimated time: {format_time(estimated_time)}"
        
        # Generate audio for each chunk
        for i, chunk in enumerate(text_chunks):
            progress = 40 + int((i / total_chunks) * 50)
            yield progress, None, f"Generating chunk {i+1}/{total_chunks}..."
            
            chunk_wav = model.generate(
                chunk,
                language_id=language_code,
                audio_prompt_path=audio_prompt_path,
                exaggeration=exaggeration,
                temperature=temperature,
                cfg_weight=cfgw,
            )
            generated_wavs.append(chunk_wav)
            
        if not generated_wavs:
             yield 0, None, "❌ Error: No audio generated."
             return
        
        yield 90, None, "Finalizing audio..."
        
        # Concatenate audio chunks
        if len(generated_wavs) > 1:
            full_wav = torch.cat(generated_wavs, dim=-1)
        else:
            full_wav = generated_wavs[0]
        
        # Calculate actual time taken
        total_time = time.time() - start_time
        final_status = f"✅ Generation complete!\nLanguage: {lang_name}\nTime taken: {format_time(total_time)}\nText length: {len(text)} chars\nChunks: {total_chunks}"
        
        yield 100, (model.sr, full_wav.squeeze(0).numpy()), final_status
        
    except Exception as e:
        error_status = f"❌ Error generating speech: {str(e)}"
        yield 0, None, error_status


def convert_voice(input_audio, target_voice_name):
    """Convert voice with progress tracking."""
    try:
        start_time = time.time()
        
        # Input validations
        if not input_audio:
            yield 0, None, "❌ Error: No input audio provided."
            return
        
        yield 20, None, "Loading input audio..."
        
        # Remove gender symbols if present
        clean_name = target_voice_name.replace(" ♂️", "").replace(" ♀️", "")
        
        if not clean_name or clean_name == "None":
            target_voice_path = None
            yield 40, None, "⚠️ No target voice selected - using default..."
        else:
            # Try to find the voice with different gender suffix combinations
            from .voice_manager import VOICES
            possible_names = [
                clean_name,
                f"{clean_name}_male",
                f"{clean_name}_female"
            ]
            
            target_voice_path = None
            for name in possible_names:
                if name in VOICES["samples"]:
                    target_voice_path = VOICES["samples"][name]
                    break
            
            if not target_voice_path:
                yield 0, None, f"❌ Error: Target voice '{target_voice_name}' not found."
                return
            yield 40, None, f"Using target voice: {target_voice_name}..."
        
        # Load model via manager (handles unloading others)
        yield 60, None, "Loading Voice Conversion model..."
        model = model_manager.get_vc_model()
        if model is None:
             yield 0, None, "❌ Error: Failed to load VC model."
             return
        
        yield 70, None, "Converting voice..."
        
        # Convert voice
        wav = model.generate(input_audio, target_voice_path=target_voice_path)
        
        yield 95, None, "Finalizing audio..."
        
        # Calculate actual time taken
        total_time = time.time() - start_time
        final_status = f"✅ Conversion complete!\nTime taken: {format_time(total_time)}"
        
        yield 100, (model.sr, wav.squeeze(0).numpy()), final_status
        
    except Exception as e:
        error_status = f"❌ Error converting voice: {str(e)}"
        yield 0, None, error_status


def generate_turbo_speech(text, voice_name):
    """Generate speech using Turbo model with progress tracking and paralinguistic tag support."""
    try:
        start_time = time.time()
        
        # Input validations
        if not text or not text.strip():
            yield 0, None, "❌ Error: Input text cannot be empty."
            return
        
        if len(text) > 250:
            print(f"ℹ️ Text length: {len(text)} chars - Using smart chunking")
        
        if not voice_name or voice_name == "None":
            yield 0, None, "❌ Error: Please select a voice for Turbo TTS. A reference clip is required."
            return
        else:
            audio_prompt_path = resolve_voice_path(voice_name, "en")
            if not audio_prompt_path:
                yield 0, None, f"❌ Error: Voice '{voice_name}' not found."
                return
            yield 10, None, f"Loading voice: {voice_name}..."
        
        # Load model via manager (handles unloading others)
        yield 20, None, "Loading Turbo TTS model..."
        model = model_manager.get_turbo_model()
        if model is None:
             yield 0, None, "❌ Error: Failed to load Turbo model."
             return
        
        # Chunk text
        text_chunks = smart_chunk_text(text)
        total_chunks = len(text_chunks)
        generated_wavs = []
        
        # Estimate time (Turbo is faster, so reduce estimate)
        estimated_time = estimate_generation_time(len(text)) * 0.3  # Turbo is ~3x faster
        yield 40, None, f"Generating speech with Turbo (English)...\nChunks: {total_chunks}\nEstimated time: {format_time(estimated_time)}\n💡 Tip: Use tags like [chuckle], [laugh], [sigh] for realism!"
        
        # Generate audio for each chunk
        for i, chunk in enumerate(text_chunks):
            progress = 40 + int((i / total_chunks) * 50)
            yield progress, None, f"Generating chunk {i+1}/{total_chunks}..."
            
            chunk_wav = model.generate(
                chunk,
                audio_prompt_path=audio_prompt_path
            )
            generated_wavs.append(chunk_wav)
        
        if not generated_wavs:
             yield 0, None, "❌ Error: No audio generated."
             return

        yield 90, None, "Finalizing audio..."
        
        # Concatenate audio chunks
        if len(generated_wavs) > 1:
            full_wav = torch.cat(generated_wavs, dim=-1)
        else:
            full_wav = generated_wavs[0]
        
        # Calculate actual time taken
        total_time = time.time() - start_time
        final_status = f"✅ Generation complete!\nTime taken: {format_time(total_time)}\nText length: {len(text)} chars\nChunks: {total_chunks}\n⚡ Generated with Turbo (350M params)"
        
        yield 100, (model.sr, full_wav.squeeze(0).numpy()), final_status
        
    except Exception as e:
        error_status = f"❌ Error generating speech: {str(e)}"
        yield 0, None, error_status


def generate_batch_turbo_speech(text_list, voice_list, use_same_voice):
    """
    Generate multiple speech outputs in batch using Turbo model.
    
    Args:
        text_list: List of text strings to synthesize
        voice_list: List of voice names (or single voice if use_same_voice is True)
        use_same_voice: Boolean indicating if same voice should be used for all
    
    Yields:
        Tuple of (overall_progress, audio_outputs_list, status_message)
    """
    try:
        start_time = time.time()
        
        # Filter out empty texts
        valid_items = [(i, text, voice_list[0] if use_same_voice else voice_list[i]) 
                       for i, text in enumerate(text_list) 
                       if text and text.strip()]
        
        if not valid_items:
            yield 0, [], "❌ Error: No valid text inputs provided."
            return
        
        total_items = len(valid_items)
        yield 5, [], f"📦 Starting batch generation for {total_items} items..."
        
        # Load model once for all generations
        yield 10, [], "Loading Turbo TTS model..."
        model = model_manager.get_turbo_model()
        if model is None:
            yield 0, [], "❌ Error: Failed to load Turbo model."
            return
        
        audio_outputs = []
        
        # Generate each item
        for idx, (original_idx, text, voice_name) in enumerate(valid_items):
            item_num = idx + 1
            
            # Resolve voice path
            if not voice_name or voice_name == "None":
                yield int(10 + (idx / total_items) * 85), audio_outputs, f"❌ Item {item_num}/{total_items}: No voice selected"
                audio_outputs.append(None)
                continue
            
            audio_prompt_path = resolve_voice_path(voice_name, "en")
            if not audio_prompt_path:
                yield int(10 + (idx / total_items) * 85), audio_outputs, f"❌ Item {item_num}/{total_items}: Voice not found"
                audio_outputs.append(None)
                continue
            
            yield int(10 + (idx / total_items) * 85), audio_outputs, f"🎙️ Generating item {item_num}/{total_items}: {text[:50]}..."
            
            try:
                # Chunk text
                text_chunks = smart_chunk_text(text)
                generated_wavs = []
                
                # Generate audio for each chunk
                for chunk in text_chunks:
                    chunk_wav = model.generate(
                        chunk,
                        audio_prompt_path=audio_prompt_path
                    )
                    generated_wavs.append(chunk_wav)
                
                # Concatenate chunks
                if len(generated_wavs) > 1:
                    full_wav = torch.cat(generated_wavs, dim=-1)
                else:
                    full_wav = generated_wavs[0]
                
                audio_outputs.append((model.sr, full_wav.squeeze(0).numpy()))
                
            except Exception as e:
                yield int(10 + (idx / total_items) * 85), audio_outputs, f"❌ Item {item_num}/{total_items}: Error - {str(e)}"
                audio_outputs.append(None)
                continue
        
        # Calculate total time
        total_time = time.time() - start_time
        successful = sum(1 for audio in audio_outputs if audio is not None)
        
        final_status = f"✅ Batch generation complete!\n"
        final_status += f"Total items: {total_items}\n"
        final_status += f"Successful: {successful}\n"
        final_status += f"Failed: {total_items - successful}\n"
        final_status += f"Total time: {format_time(total_time)}\n"
        final_status += f"Average time per item: {format_time(total_time / total_items)}"
        
        yield 100, audio_outputs, final_status
        
    except Exception as e:
        error_status = f"❌ Error in batch generation: {str(e)}"
        yield 0, [], error_status
                    


# Motivation Hub's production TTS endpoint accepts the same six voice IDs used in its app.
MOTIVATION_HUB_VOICES = ("alloy", "echo", "fable", "onyx", "nova", "shimmer")
MOTIVATION_HUB_TTS_URL = "https://motivation-hub-iota.vercel.app/api/tts"
MAX_REMOTE_TTS_RESPONSE_BYTES = 25 * 1024 * 1024


def generate_motivation_hub_speech(text, voice_name):
    """Generate audio through Motivation Hub's production TTS API."""
    if not text or not text.strip():
        yield 0, None, "❌ Enter text before generating audio."
        return

    text = text.strip()
    if len(text) > 4000:
        yield 0, None, "❌ Text must be 4,000 characters or fewer."
        return

    if voice_name not in MOTIVATION_HUB_VOICES:
        yield 0, None, "❌ Select one of the available Motivation Hub voices."
        return

    endpoint = os.environ.get("MOTIVATION_HUB_TTS_URL", MOTIVATION_HUB_TTS_URL).strip()
    if not endpoint.startswith("https://"):
        yield 0, None, "❌ The production TTS endpoint must use HTTPS."
        return

    yield 10, None, f"Sending text to Motivation Hub production TTS ({voice_name})..."
    request = urllib.request.Request(
        endpoint,
        data=json.dumps({"text": text, "voice": voice_name}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw_response = response.read(MAX_REMOTE_TTS_RESPONSE_BYTES + 1)
        if len(raw_response) > MAX_REMOTE_TTS_RESPONSE_BYTES:
            yield 0, None, "❌ The TTS response exceeded the 25 MB limit."
            return

        payload = json.loads(raw_response.decode("utf-8"))
        audio_data = payload.get("audio", {}).get("base64Data")
        if not audio_data:
            detail = payload.get("error") or payload.get("details") or "The API did not return audio."
            yield 0, None, f"❌ Motivation Hub TTS error: {detail}"
            return

        audio_bytes = base64.b64decode(audio_data, validate=True)
        mime_type = payload.get("audio", {}).get("mimeType", "audio/mpeg").lower()
        extension = ".wav" if "wav" in mime_type else ".mp3"
        with tempfile.NamedTemporaryFile(prefix="motivation_hub_tts_", suffix=extension, delete=False) as audio_file:
            audio_file.write(audio_bytes)
            audio_path = audio_file.name

        yield 100, audio_path, f"✅ Generated with Motivation Hub's {voice_name} voice."
    except urllib.error.HTTPError as exc:
        detail = exc.read(1000).decode("utf-8", errors="replace")
        yield 0, None, f"❌ Production TTS returned HTTP {exc.code}: {detail or exc.reason}"
    except urllib.error.URLError as exc:
        yield 0, None, f"❌ Could not reach the production TTS endpoint: {exc.reason}"
    except (ValueError, KeyError, TypeError) as exc:
        yield 0, None, f"❌ Invalid TTS response: {exc}"
    except Exception as exc:
        yield 0, None, f"❌ TTS request failed: {exc}"
