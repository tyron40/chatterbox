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
        import traceback
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
        import traceback
        error_traceback = traceback.format_exc()
        error_status = f"❌ Error generating speech: {str(e)}\n\nFull traceback:\n{error_traceback}"
        print(f"\n{'='*50}\nERROR IN generate_speech:\n{error_traceback}\n{'='*50}\n")
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
        import traceback
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
        import traceback
        error_traceback = traceback.format_exc()
        error_status = f"❌ Error generating speech: {str(e)}\n\nFull traceback:\n{error_traceback}"
        print(f"\n{'='*50}\nERROR IN generate_turbo_speech:\n{error_traceback}\n{'='*50}\n")
        yield 0, None, error_status


def generate_batch_turbo_speech(text_list, voice_list, use_same_voice, bgmusic_list=None):
    """
    Generate multiple speech outputs in batch using Turbo model with optional background music.
    
    Args:
        text_list: List of text strings to synthesize (50 items)
        voice_list: List of voice names (or single voice if use_same_voice is True)
        use_same_voice: Boolean indicating if same voice should be used for all
        bgmusic_list: Optional list of background music file paths (50 items)
    
    Yields:
        Tuple of (overall_progress, audio_outputs_list, status_message)
        audio_outputs_list is always 50 items (None for empty/failed)
    """
    try:
        import os
        import tempfile
        import soundfile as sf
        from .audio_mixer import mix_audio_with_music
        
        start_time = time.time()
        
        # Initialize output list with 50 None values
        audio_outputs = [None] * 50
        
        # Filter out empty texts but keep track of original indices
        valid_items = [(i, text, voice_list[0] if use_same_voice else voice_list[i]) 
                       for i, text in enumerate(text_list) 
                       if text and text.strip()]
        
        if not valid_items:
            yield 0, audio_outputs, "❌ Error: No valid text inputs provided."
            return
        
        total_items = len(valid_items)
        yield 5, audio_outputs, f"📦 Starting batch generation for {total_items} items..."
        
        # Load model once for all generations
        yield 10, audio_outputs, "Loading Turbo TTS model..."
        model = model_manager.get_turbo_model()
        if model is None:
            yield 0, audio_outputs, "❌ Error: Failed to load Turbo model."
            return
        
        successful_count = 0
        failed_count = 0
        
        # Generate each item
        for idx, (original_idx, text, voice_name) in enumerate(valid_items):
            item_num = idx + 1
            
            # Resolve voice path
            if not voice_name or voice_name == "None":
                yield int(10 + (idx / total_items) * 85), audio_outputs, f"❌ Item {item_num}/{total_items}: No voice selected"
                failed_count += 1
                continue
            
            audio_prompt_path = resolve_voice_path(voice_name, "en")
            if not audio_prompt_path:
                yield int(10 + (idx / total_items) * 85), audio_outputs, f"❌ Item {item_num}/{total_items}: Voice not found"
                failed_count += 1
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
                
                # Check if background music should be added
                if bgmusic_list and bgmusic_list[original_idx]:
                    bgmusic_path = bgmusic_list[original_idx]
                    if bgmusic_path and os.path.exists(bgmusic_path):
                        yield int(10 + (idx / total_items) * 85), audio_outputs, f"🎵 Adding background music to item {item_num}/{total_items}..."
                        
                        # Save voice audio to temp file
                        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_voice:
                            temp_voice_path = temp_voice.name
                            sf.write(temp_voice_path, full_wav.squeeze(0).numpy(), model.sr)
                        
                        try:
                            # Mix with background music
                            mixed_path = mix_audio_with_music(
                                voice_path=temp_voice_path,
                                music_path=bgmusic_path,
                                output_path=None,
                                music_volume=0.15,
                                enable_ducking=True
                            )
                            
                            if mixed_path and os.path.exists(mixed_path):
                                # Load mixed audio
                                mixed_audio, mixed_sr = sf.read(mixed_path)
                                audio_outputs[original_idx] = (mixed_sr, mixed_audio)
                                # Clean up temp files
                                os.remove(mixed_path)
                            else:
                                # If mixing failed, use original voice
                                audio_outputs[original_idx] = (model.sr, full_wav.squeeze(0).numpy())
                        finally:
                            # Clean up temp voice file
                            if os.path.exists(temp_voice_path):
                                os.remove(temp_voice_path)
                    else:
                        # No valid background music, use voice only
                        audio_outputs[original_idx] = (model.sr, full_wav.squeeze(0).numpy())
                else:
                    # No background music, use voice only
                    audio_outputs[original_idx] = (model.sr, full_wav.squeeze(0).numpy())
                
                successful_count += 1
                
            except Exception as e:
                yield int(10 + (idx / total_items) * 85), audio_outputs, f"❌ Item {item_num}/{total_items}: Error - {str(e)}"
                failed_count += 1
                continue
        
        # Calculate total time
        total_time = time.time() - start_time
        
        final_status = f"✅ Batch generation complete!\n"
        final_status += f"Total items: {total_items}\n"
        final_status += f"Successful: {successful_count}\n"
        final_status += f"Failed: {failed_count}\n"
        final_status += f"Total time: {format_time(total_time)}\n"
        final_status += f"Average time per item: {format_time(total_time / total_items)}"
        
        yield 100, audio_outputs, final_status
        
    except Exception as e:
        error_status = f"❌ Error in batch generation: {str(e)}"
        yield 0, [None] * 50, error_status


def create_batch_zip(audio_outputs):
    """
    Create a ZIP file containing all generated audio files.
    
    Args:
        audio_outputs: List of audio tuples (sample_rate, audio_data) or None
    
    Returns:
        Path to the created ZIP file or None if failed
    """
    try:
        import os
        import tempfile
        import zipfile
        import soundfile as sf
        from datetime import datetime
        
        # Filter out None values
        valid_audios = [(i, audio) for i, audio in enumerate(audio_outputs) if audio is not None]
        
        if not valid_audios:
            return None
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create ZIP file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"batch_tts_{timestamp}.zip"
        zip_path = os.path.join(output_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for idx, (sr, audio_data) in valid_audios:
                # Create temp WAV file
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                    temp_path = temp_file.name
                    sf.write(temp_path, audio_data, sr)
                
                # Add to ZIP with proper name
                audio_filename = f"audio_{idx+1:02d}.wav"
                zipf.write(temp_path, audio_filename)
                
                # Clean up temp file
                os.remove(temp_path)
        
        return zip_path
        
    except Exception as e:
        print(f"Error creating ZIP file: {e}")
        return None
                                
