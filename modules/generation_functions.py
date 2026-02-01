"""
Speech generation, conversion, and utility functions for Chatterbox TTS Enhanced
"""
import random
import numpy as np
import torch
import time
import re
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


def generate_batch_speech(texts, voices, model_type, language_code=None):
    """
    Generate multiple audio files from batch text input.
    
    Args:
        texts: List of text strings to generate audio for
        voices: List of voice names to use for each text
        model_type: "tts" (English), "multilingual", or "turbo"
        language_code: Language code (required for multilingual)
    
    Yields:
        progress: Progress percentage (0-100)
        audio_data: Audio data for the current text (sample_rate, audio_array)
        status_update: Status message
        audio_index: Index of the audio in the texts list
    """
    import os
    import scipy.io.wavfile as wavfile
    from datetime import datetime
    
    try:
        start_time = time.time()
        
        # Input validations
        if not texts:
            yield 0, None, "❌ Error: No valid texts provided.", None
            return
        
        total_texts = len(texts)
        
        if total_texts > 1000:
            yield 0, None, f"❌ Error: Maximum 1000 texts allowed. You provided {total_texts}.", None
            return
        
        yield 5, None, f"📝 Found {total_texts} text{'s' if total_texts != 1 else ''} to generate...", None
        
        # Validate voices
        if len(voices) != len(texts):
            yield 0, None, f"❌ Error: Number of voices ({len(voices)}) does not match number of texts ({len(texts)}).", None
            return
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join("batch_output", f"batch_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        yield 10, None, f"📁 Output directory: {output_dir}", None
        
        # Load appropriate model
        yield 15, None, f"Loading {model_type.upper()} model...", None
        
        if model_type == "tts":
            model = model_manager.get_tts_model()
        elif model_type == "multilingual":
            if not language_code:
                yield 0, None, "❌ Error: Language code required for multilingual generation.", None
                return
            model = model_manager.get_mtl_model()
        elif model_type == "turbo":
            model = model_manager.get_turbo_model()
        else:
            yield 0, None, f"❌ Error: Invalid model type '{model_type}'.", None
            return
        
        if model is None:
            yield 0, None, f"❌ Error: Failed to load {model_type} model.", None
            return
        
        # Generate audio for each text
        generated_files = []
        failed_count = 0
        
        for i, (text, voice_name) in enumerate(zip(texts, voices)):
            progress = 20 + int((i / total_texts) * 75)
            yield progress, None, f"Generating {i+1}/{total_texts}: {text[:50]}{'...' if len(text) > 50 else ''}", None
            
            # Skip if text is empty
            if not text or not text.strip():
                yield progress, None, f"⏭️ Skipping text {i+1} (empty)", i
                continue
            
            # Resolve voice path for this text
            if voice_name and voice_name != "None":
                # Debug: Print voice name being processed
                print(f"DEBUG: Processing voice '{voice_name}' for text {i+1}")
                
                if model_type == "multilingual":
                    audio_prompt_path = resolve_voice_path(voice_name, language_code or "en")
                else:
                    audio_prompt_path = resolve_voice_path(voice_name, "en")
                
                # Debug: Print resolved path
                print(f"DEBUG: Resolved path for '{voice_name}': {audio_prompt_path}")
                
                if not audio_prompt_path:
                    # For turbo model, voice is required
                    if model_type == "turbo":
                        error_msg = f"❌ Error: Voice '{voice_name}' not found for text {i+1}. Turbo requires a valid voice."
                        print(f"DEBUG: {error_msg}")
                        yield progress, None, error_msg, i
                        failed_count += 1
                        continue
                    
                    yield progress, None, f"⚠️ Warning: Voice '{voice_name}' not found for text {i+1}. Using default.", None
                    if model_type == "multilingual" and language_code:
                        audio_prompt_path = LANGUAGE_CONFIG.get(language_code, {}).get("audio")
                    else:
                        audio_prompt_path = None
            else:
                # For turbo model, voice is required
                if model_type == "turbo":
                    error_msg = f"❌ Error: No voice selected for text {i+1}. Turbo requires a voice."
                    print(f"DEBUG: {error_msg}")
                    yield progress, None, error_msg, i
                    failed_count += 1
                    continue
                
                if model_type == "multilingual" and language_code:
                    audio_prompt_path = LANGUAGE_CONFIG.get(language_code, {}).get("audio")
                else:
                    audio_prompt_path = None
                        
            # Generate audio based on model type
            try:
                if model_type == "tts":
                    wav = model.generate(
                        text,
                        audio_prompt_path=audio_prompt_path,
                        exaggeration=0.5,
                        temperature=0.8,
                        cfg_weight=0.5,
                        min_p=0.05,
                        top_p=1.0,
                        repetition_penalty=1.2
                    )
                elif model_type == "multilingual":
                    wav = model.generate(
                        text,
                        language_id=language_code,
                        audio_prompt_path=audio_prompt_path,
                        exaggeration=0.5,
                        temperature=0.8,
                        cfg_weight=0.5
                    )
                elif model_type == "turbo":
                    # CRITICAL: Turbo model needs chunking just like single TTS!
                    # Generate with chunking to match the working single Turbo TTS behavior
                    text_chunks = smart_chunk_text(text)
                    chunk_wavs = []
                    
                    for chunk in text_chunks:
                        chunk_wav = model.generate(
                            chunk,
                            audio_prompt_path=audio_prompt_path
                        )
                        chunk_wavs.append(chunk_wav)
                    
                    # Concatenate chunks if multiple
                    if len(chunk_wavs) > 1:
                        wav = torch.cat(chunk_wavs, dim=-1)
                    else:
                        wav = chunk_wavs[0]
                    
                # Save audio file
                filename = f"audio_{i+1:04d}.wav"
                filepath = os.path.join(output_dir, filename)
                
                # CRITICAL: Match the exact conversion process used in single Turbo TTS
                # The working single TTS does: full_wav.squeeze(0).numpy()
                # We must do the same to preserve audio quality
                if hasattr(wav, 'is_cuda') and wav.is_cuda:
                    wav_numpy = wav.squeeze(0).cpu().numpy()
                else:
                    # This is the key: call .numpy() directly without intermediate conversions
                    wav_numpy = wav.squeeze(0).numpy() if hasattr(wav, 'squeeze') else wav.numpy()
                
                # Convert to int16 for wav file (scipy expects int16)
                # wav_numpy is already in the correct float format from the model
                wav_int16 = (wav_numpy * 32767).astype(np.int16)
                wavfile.write(filepath, model.sr, wav_int16)
                generated_files.append(filepath)
                
                # Return the audio data for display in the UI
                # Use the original wav_numpy without any additional conversions
                audio_data = (model.sr, wav_numpy)
                yield progress, audio_data, f"Generated audio {i+1}/{total_texts}", i
                        
            except Exception as e:
                error_msg = f"Failed to generate audio {i+1}: {str(e)}"
                print(error_msg)
                yield progress, None, error_msg, i
                failed_count += 1
                continue
                        
        yield 95, None, "Finalizing batch generation...", None
        
        # Create summary file
        summary_path = os.path.join(output_dir, "summary.txt")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"Batch Generation Summary\n")
            f.write(f"========================\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {model_type.upper()}\n")
            f.write(f"\nTotal texts: {total_texts}\n")
            f.write(f"Successfully generated: {len(generated_files)}\n")
            f.write(f"Failed: {failed_count}\n\n")
            f.write(f"Generated Files:\n")
            f.write(f"================\n")
            for i, text in enumerate(texts):
                status = "✓" if i < len(generated_files) else "✗"
                voice_info = f" (Voice: {voices[i]})" if voices[i] else ""
                f.write(f"{status} {i+1:04d}. {text}{voice_info}\n")
        
        # Calculate total time
        total_time = time.time() - start_time
        
        final_status = f"""✅ Batch generation complete!
        
📊 Summary:
- Total texts: {total_texts}
- Successfully generated: {len(generated_files)}
- Failed: {failed_count}
- Time taken: {format_time(total_time)}
- Output directory: {output_dir}

📁 Files saved:
- {len(generated_files)} audio files (.wav)
- 1 summary file (summary.txt)

You can download individual files or use the "Download All" button to get a zip file.
"""
        
        yield 100, None, final_status, None
        
    except Exception as e:
        error_status = f"❌ Error in batch generation: {str(e)}"
        yield 0, None, error_status, None
