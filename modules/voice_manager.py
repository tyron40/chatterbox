"""
Voice management functions for Chatterbox TTS Enhanced
"""
import os
import shutil
import tempfile
import urllib.request
import gradio as gr
from .config import VOICE_DIR, LANGUAGE_CONFIG, SUPPORTED_LANGUAGES
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("⚠️ Warning: pydub not available. Audio format conversion will be limited.")

# Voice storage
VOICES = {"samples": {}}


def extract_gender_from_name(voice_name):
    """Extract gender from voice name if present."""
    if voice_name.endswith("_male"):
        return "male", voice_name[:-5]  # Remove _male suffix
    elif voice_name.endswith("_female"):
        return "female", voice_name[:-7]  # Remove _female suffix
    return None, voice_name


def format_voice_display_name(voice_name):
    """Format voice name with gender symbol for display."""
    gender, base_name = extract_gender_from_name(voice_name)
    if gender == "male":
        return f"{base_name} ♂️"
    elif gender == "female":
        return f"{base_name} ♀️"
    return base_name


def load_voices():
    """Load all available voice samples from the voice_samples directory."""
    VOICES["samples"].clear()
    for name in os.listdir(VOICE_DIR):
        if name.endswith(".wav"):
            base = os.path.splitext(name)[0]
            wav_path = os.path.join(VOICE_DIR, name)
            VOICES["samples"][base] = wav_path
    return list(VOICES["samples"].keys())


def get_voices_for_language(language_code):
    """Get voices available for a specific language (cloned + default sample)."""
    voices = []
    
    # Add default sample for this language if available
    if language_code in LANGUAGE_CONFIG and language_code != "en":
        voices.append(f"Default ({SUPPORTED_LANGUAGES[language_code]})")
    
    # Add cloned voices for this language
    for voice_name in VOICES["samples"].keys():
        # Check if voice has language suffix
        if voice_name.endswith(f"_{language_code}"):
            # Remove language suffix for display
            base_name = voice_name.replace(f"_{language_code}", "")
            display_name = format_voice_display_name(base_name)
            voices.append(display_name)
        elif language_code == "en":
            # For English, check if it's a voice without language suffix
            # but might have gender suffix
            # Skip if it has another language code
            has_other_lang = any(voice_name.endswith(f"_{code}") for code in SUPPORTED_LANGUAGES.keys() if code != "en")
            if not has_other_lang:
                display_name = format_voice_display_name(voice_name)
                voices.append(display_name)
    
    return voices


def resolve_voice_path(voice_name, language_code):
    """Resolve the actual voice path from display name and language."""
    if voice_name.startswith("Default ("):
        # Use default sample audio for this language
        audio_url = LANGUAGE_CONFIG.get(language_code, {}).get("audio")
        if audio_url and audio_url.startswith("http"):
            # Download the file to temp directory
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f"chatterbox_sample_{language_code}.flac")
            
            # Download if not already cached
            if not os.path.exists(temp_file):
                try:
                    print(f"Downloading sample audio for {language_code}...")
                    urllib.request.urlretrieve(audio_url, temp_file)
                    print(f"Downloaded to {temp_file}")
                except Exception as e:
                    print(f"Error downloading audio: {e}")
                    return None
            
            return temp_file
        return audio_url
    
    # Remove gender symbols and other special characters from display name
    clean_name = voice_name.replace(" ♂️", "").replace(" ♀️", "").replace(" ☑️", "").replace("☑️", "").strip()
    
    print(f"🔍 Resolving voice: '{voice_name}' -> clean: '{clean_name}' for language: {language_code}")
    print(f"📁 Available voices: {list(VOICES['samples'].keys())}")
    
    # Try to find the voice with different gender suffix combinations
    possible_names = [
        clean_name,
        f"{clean_name}_male",
        f"{clean_name}_female"
    ]
    
    if language_code == "en":
        # English voices don't have language suffix
        for name in possible_names:
            if name in VOICES["samples"]:
                resolved_path = VOICES["samples"][name]
                print(f"✅ Found voice: {name} -> {resolved_path}")
                return resolved_path
    else:
        # Other languages have language suffix
        for name in possible_names:
            full_name = f"{name}_{language_code}"
            if full_name in VOICES["samples"]:
                resolved_path = VOICES["samples"][full_name]
                print(f"✅ Found voice: {full_name} -> {resolved_path}")
                return resolved_path
    
    print(f"❌ Voice not found! Tried: {possible_names}")
    return None
                

def get_all_voices_with_gender():
    """Get all voices formatted with gender symbols for display."""
    formatted_voices = []
    for voice_name in VOICES["samples"].keys():
        formatted_voices.append(format_voice_display_name(voice_name))
    return formatted_voices


def clone_voice(audio_file, new_voice_name, voice_language, voice_gender):
    """Clone a voice by saving the reference audio with automatic format conversion."""
    try:
        # Input validations
        if not new_voice_name or not new_voice_name.strip():
            return "❌ Error: Voice name cannot be empty.", gr.update()
        
        if not audio_file:
            return "❌ Error: No audio file provided.", gr.update()
        
        # Sanitize voice name
        new_voice_name = new_voice_name.strip()
        
        # Add gender suffix (always required now)
        new_voice_name = f"{new_voice_name}_{voice_gender}"
        
        # Add language tag for non-English voices
        if voice_language and voice_language != "en":
            new_voice_name = f"{new_voice_name}_{voice_language}"
        
        if new_voice_name in VOICES["samples"]:
            return f"❌ Error: Voice '{new_voice_name}' already exists. Please choose a different name.", gr.update()
        
        # Determine output path
        wav_path = os.path.join(VOICE_DIR, f"{new_voice_name}.wav")
        
        # Check if input file is already WAV
        file_ext = os.path.splitext(audio_file)[1].lower()
        
        # Always convert/re-encode audio to ensure proper format
        if PYDUB_AVAILABLE:
            try:
                print(f"Processing audio file ({file_ext})...")
                audio = AudioSegment.from_file(audio_file)
                
                # Convert to mono if stereo
                if audio.channels > 1:
                    print(f"Converting from {audio.channels} channels to mono...")
                    audio = audio.set_channels(1)
                
                # Resample to 24kHz if needed
                if audio.frame_rate != 24000:
                    print(f"Resampling from {audio.frame_rate}Hz to 24000Hz...")
                    audio = audio.set_frame_rate(24000)
                
                # Export as WAV with proper settings
                audio.export(
                    wav_path,
                    format='wav',
                    parameters=["-acodec", "pcm_s16le"]  # 16-bit PCM WAV
                )
                print(f"✅ Audio processed and saved successfully")
            except Exception as conv_error:
                print(f"⚠️ pydub conversion failed: {conv_error}")
                print(f"⚠️ Attempting direct copy as fallback...")
                shutil.copy(audio_file, wav_path)
        else:
            # If pydub not available, try direct copy
            print(f"⚠️ pydub not available, attempting direct copy...")
            shutil.copy(audio_file, wav_path)
        
        # Update voices dictionary
        VOICES["samples"][new_voice_name] = wav_path
        updated_voices = list(VOICES["samples"].keys())
        
        # Format display name with gender symbol
        display_name = format_voice_display_name(new_voice_name)
        
        return f"✅ Voice '{display_name}' cloned successfully!", gr.update(choices=["None"] + updated_voices, value=new_voice_name)
        
    except Exception as e:
        return f"❌ Error cloning voice: {str(e)}", gr.update()
                

def check_voice_format(voice_name):
    """Check if a voice file needs format conversion."""
    try:
        if not voice_name or voice_name == "None":
            return "❌ Error: No voice selected."
        
        # Remove gender symbols if present
        clean_name = voice_name.replace(" ♂️", "").replace(" ♀️", "")
        
        # Try to find the actual voice name in VOICES
        actual_name = None
        possible_names = [
            clean_name,
            f"{clean_name}_male",
            f"{clean_name}_female"
        ]
        
        for name in possible_names:
            if name in VOICES["samples"]:
                actual_name = name
                break
        
        if not actual_name:
            return f"❌ Error: Voice '{voice_name}' not found."
        
        wav_path = VOICES["samples"][actual_name]
        
        if not os.path.exists(wav_path):
            return f"❌ Error: Voice file not found at {wav_path}"
        
        # Try to load with pydub to check format
        if PYDUB_AVAILABLE:
            try:
                audio = AudioSegment.from_file(wav_path)
                
                issues = []
                if audio.channels > 1:
                    issues.append(f"Stereo ({audio.channels} channels)")
                if audio.frame_rate != 24000:
                    issues.append(f"Sample rate: {audio.frame_rate}Hz")
                
                if issues:
                    return f"⚠️ Voice '{voice_name}' needs conversion:\n- " + "\n- ".join(issues) + "\n\nClick 'Convert Voice' to fix."
                else:
                    return f"✅ Voice '{voice_name}' is in correct format:\n- Mono (1 channel)\n- 24000Hz sample rate"
            except Exception as e:
                return f"⚠️ Voice '{voice_name}' may have format issues:\n{str(e)}\n\nClick 'Convert Voice' to fix."
        else:
            return "⚠️ pydub not available. Cannot check voice format."
            
    except Exception as e:
        return f"❌ Error checking voice: {str(e)}"


def convert_existing_voice(voice_name):
    """Convert an existing voice to proper format."""
    try:
        if not voice_name or voice_name == "None":
            return "❌ Error: No voice selected.", gr.update()
        
        # Remove gender symbols if present
        clean_name = voice_name.replace(" ♂️", "").replace(" ♀️", "")
        
        # Try to find the actual voice name in VOICES
        actual_name = None
        possible_names = [
            clean_name,
            f"{clean_name}_male",
            f"{clean_name}_female"
        ]
        
        for name in possible_names:
            if name in VOICES["samples"]:
                actual_name = name
                break
        
        if not actual_name:
            return f"❌ Error: Voice '{voice_name}' not found.", gr.update()
        
        wav_path = VOICES["samples"][actual_name]
        
        if not os.path.exists(wav_path):
            return f"❌ Error: Voice file not found at {wav_path}", gr.update()
        
        if not PYDUB_AVAILABLE:
            return "❌ Error: pydub not available. Cannot convert voice.", gr.update()
        
        # Create backup
        backup_path = wav_path + ".backup"
        shutil.copy(wav_path, backup_path)
        print(f"📦 Created backup: {backup_path}")
        
        try:
            print(f"🔄 Converting voice: {voice_name}")
            audio = AudioSegment.from_file(wav_path)
            
            # Convert to mono if stereo
            if audio.channels > 1:
                print(f"Converting from {audio.channels} channels to mono...")
                audio = audio.set_channels(1)
            
            # Resample to 24kHz if needed
            if audio.frame_rate != 24000:
                print(f"Resampling from {audio.frame_rate}Hz to 24000Hz...")
                audio = audio.set_frame_rate(24000)
            
            # Export as WAV with proper settings
            audio.export(
                wav_path,
                format='wav',
                parameters=["-acodec", "pcm_s16le"]  # 16-bit PCM WAV
            )
            
            print(f"✅ Voice converted successfully")
            
            # Remove backup if successful
            if os.path.exists(backup_path):
                os.remove(backup_path)
                print(f"🗑️ Removed backup")
            
            return f"✅ Voice '{voice_name}' converted successfully!\n- Format: 16-bit PCM WAV\n- Channels: Mono\n- Sample rate: 24000Hz", gr.update()
            
        except Exception as conv_error:
            # Restore from backup if conversion failed
            if os.path.exists(backup_path):
                shutil.copy(backup_path, wav_path)
                os.remove(backup_path)
                print(f"⚠️ Conversion failed, restored from backup")
            
            return f"❌ Error converting voice: {str(conv_error)}", gr.update()
            
    except Exception as e:
        return f"❌ Error: {str(e)}", gr.update()


def delete_voice(voice_name):
    """Delete a voice and its associated file."""
    try:
        if not voice_name or voice_name == "None":
            return "❌ Error: No voice selected.", gr.update()
        
        # Remove gender symbols if present
        clean_name = voice_name.replace(" ♂️", "").replace(" ♀️", "")
        
        # Try to find the actual voice name in VOICES
        actual_name = None
        possible_names = [
            clean_name,
            f"{clean_name}_male",
            f"{clean_name}_female"
        ]
        
        for name in possible_names:
            if name in VOICES["samples"]:
                actual_name = name
                break
        
        if not actual_name:
            return f"❌ Error: Voice '{voice_name}' not found.", gr.update()
        
        # Delete the file
        wav_path = VOICES["samples"][actual_name]
        if os.path.exists(wav_path):
            os.remove(wav_path)
        
        # Remove from dictionary
        del VOICES["samples"][actual_name]
        
        remaining_voices = get_all_voices_with_gender()
        new_selected = remaining_voices[0] if remaining_voices else "None"
        
        return f"✅ Voice '{voice_name}' deleted successfully!", gr.update(choices=["None"] + remaining_voices, value=new_selected)
        
    except Exception as e:
        return f"❌ Error deleting voice: {str(e)}", gr.update()
