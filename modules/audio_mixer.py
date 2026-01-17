"""
Cinematic Audio Mixer for Chatterbox TTS
Automatically adds background music with ducking to voice files
"""
import os
import subprocess
import random
import json
from pathlib import Path

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_DIR = os.path.join(PROJECT_ROOT, "music")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Ensure directories exist
os.makedirs(MUSIC_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
for mood in ["epic", "emotional", "uplifting"]:
    os.makedirs(os.path.join(MUSIC_DIR, mood), exist_ok=True)

# Audio mixing settings
MUSIC_VOLUME = 0.15  # Background music volume (15% of original)
DUCKING_THRESHOLD = -30  # dB threshold for ducking
DUCKING_RATIO = 4  # Compression ratio for ducking
ATTACK_TIME = 0.1  # seconds
RELEASE_TIME = 0.5  # seconds


def check_ffmpeg():
    """Check if FFmpeg is installed and accessible."""
    # First try system PATH
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Try common installation paths (WinGet, manual install, etc.)
    common_paths = [
        r"C:\Program Files\FFmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe"),
    ]
    
    for ffmpeg_path in common_paths:
        if os.path.exists(ffmpeg_path):
            try:
                result = subprocess.run(
                    [ffmpeg_path, "-version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    # Store the working path for later use
                    globals()['FFMPEG_PATH'] = ffmpeg_path
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
    
    return False


def get_ffmpeg_command():
    """Get the FFmpeg command (either 'ffmpeg' or full path)."""
    if 'FFMPEG_PATH' in globals():
        return globals()['FFMPEG_PATH']
    return "ffmpeg"


def get_ffprobe_command():
    """Get the FFprobe command (either 'ffprobe' or full path)."""
    if 'FFMPEG_PATH' in globals():
        # Replace ffmpeg.exe with ffprobe.exe in the path
        ffmpeg_path = globals()['FFMPEG_PATH']
        return ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')
    return "ffprobe"


def get_music_files(mood="epic"):
    """Get all music files for a specific mood."""
    mood_dir = os.path.join(MUSIC_DIR, mood)
    
    if not os.path.exists(mood_dir):
        print(f"⚠️ Warning: Music directory not found: {mood_dir}")
        return []
    
    # Supported audio formats
    extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
    music_files = []
    
    for ext in extensions:
        music_files.extend(Path(mood_dir).glob(f"*{ext}"))
    
    return [str(f) for f in music_files]


def select_random_music(mood="epic"):
    """Randomly select a background music track for the given mood."""
    music_files = get_music_files(mood)
    
    if not music_files:
        print(f"⚠️ No music files found for mood: {mood}")
        print(f"📁 Please add music files to: {os.path.join(MUSIC_DIR, mood)}")
        return None
    
    selected = random.choice(music_files)
    print(f"🎵 Selected music: {os.path.basename(selected)}")
    return selected


def get_audio_duration(audio_path):
    """Get the duration of an audio file in seconds."""
    try:
        cmd = [
            get_ffprobe_command(),
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"⚠️ Error getting audio duration: {e}")
        return 0


def mix_audio_with_music(
    voice_path,
    output_path=None,
    mood="epic",
    music_path=None,
    music_volume=MUSIC_VOLUME,
    enable_ducking=True
):
    """
    Mix voice audio with background music using FFmpeg.
    
    Args:
        voice_path: Path to the voice audio file
        output_path: Path for the output file (optional)
        mood: Music mood (epic, emotional, uplifting)
        music_path: Specific music file to use (optional, overrides mood selection)
        music_volume: Background music volume (0.0 to 1.0)
        enable_ducking: Enable automatic ducking (music dips when voice speaks)
    
    Returns:
        Path to the output file or None if failed
    """
    
    # Check FFmpeg
    if not check_ffmpeg():
        print("❌ FFmpeg not found! Please install FFmpeg first.")
        print("📥 Download from: https://ffmpeg.org/download.html")
        return None
    
    # Validate voice file
    if not os.path.exists(voice_path):
        print(f"❌ Voice file not found: {voice_path}")
        return None
    
    # Select music
    if music_path is None:
        music_path = select_random_music(mood)
    
    if music_path is None or not os.path.exists(music_path):
        print("❌ No music file available")
        return None
    
    # Generate output path
    if output_path is None:
        voice_filename = os.path.splitext(os.path.basename(voice_path))[0]
        output_filename = f"{voice_filename}_cinematic_{mood}.mp3"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"🎬 Mixing audio...")
    print(f"🎤 Voice: {os.path.basename(voice_path)}")
    print(f"🎵 Music: {os.path.basename(music_path)}")
    print(f"💾 Output: {os.path.basename(output_path)}")
    
    try:
        # Get voice duration
        voice_duration = get_audio_duration(voice_path)
        
        if enable_ducking:
            # Complex filter with sidechain compression (ducking)
            filter_complex = (
                f"[1:a]volume={music_volume}[music];"
                f"[music]aloop=loop=-1:size=2e+09[music_loop];"
                f"[0:a]asplit[voice_main][voice_side];"
                f"[music_loop][voice_side]sidechaincompress="
                f"threshold={DUCKING_THRESHOLD}dB:"
                f"ratio={DUCKING_RATIO}:"
                f"attack={ATTACK_TIME}:"
                f"release={RELEASE_TIME}[music_ducked];"
                f"[voice_main][music_ducked]amix=inputs=2:duration=first:dropout_transition=2[out]"
            )
            
            cmd = [
                get_ffmpeg_command(),
                "-i", voice_path,
                "-i", music_path,
                "-filter_complex", filter_complex,
                "-map", "[out]",
                "-t", str(voice_duration),
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                "-y",
                output_path
            ]
        else:
            # Simple mixing without ducking
            filter_complex = (
                f"[1:a]volume={music_volume},aloop=loop=-1:size=2e+09[music];"
                f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=2"
            )
            
            cmd = [
                get_ffmpeg_command(),
                "-i", voice_path,
                "-i", music_path,
                "-filter_complex", filter_complex,
                "-t", str(voice_duration),
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                "-y",
                output_path
            ]
        
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"✅ Audio mixed successfully!")
            print(f"📁 Saved to: {output_path}")
            return output_path
        else:
            print(f"❌ FFmpeg error:")
            print(result.stderr)
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg timeout - file too large or system too slow")
        return None
    except Exception as e:
        print(f"❌ Error mixing audio: {e}")
        return None


def batch_mix_audio(voice_files, mood="epic", output_dir=None):
    """
    Mix multiple voice files with background music.
    
    Args:
        voice_files: List of voice file paths
        mood: Music mood for all files
        output_dir: Output directory (optional)
    
    Returns:
        List of output file paths
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    total = len(voice_files)
    
    print(f"🎬 Batch mixing {total} files with {mood} music...")
    
    for i, voice_path in enumerate(voice_files, 1):
        print(f"\n[{i}/{total}] Processing: {os.path.basename(voice_path)}")
        
        output_path = mix_audio_with_music(
            voice_path=voice_path,
            mood=mood,
            output_path=None
        )
        
        if output_path:
            results.append(output_path)
        else:
            print(f"⚠️ Failed to mix: {voice_path}")
    
    print(f"\n✅ Batch complete: {len(results)}/{total} files mixed successfully")
    return results


def get_available_moods():
    """Get list of available music moods."""
    moods = []
    for mood in ["epic", "emotional", "uplifting"]:
        mood_dir = os.path.join(MUSIC_DIR, mood)
        if os.path.exists(mood_dir):
            music_count = len(get_music_files(mood))
            moods.append({
                "name": mood,
                "path": mood_dir,
                "tracks": music_count
            })
    return moods


def print_system_info():
    """Print system information and status."""
    print("=" * 60)
    print("🎬 CINEMATIC AUDIO MIXER - SYSTEM INFO")
    print("=" * 60)
    
    # Check FFmpeg
    ffmpeg_installed = check_ffmpeg()
    print(f"FFmpeg: {'✅ Installed' if ffmpeg_installed else '❌ Not Found'}")
    
    if not ffmpeg_installed:
        print("\n📥 To install FFmpeg:")
        print("1. Download from: https://ffmpeg.org/download.html")
        print("2. Extract and add to system PATH")
        print("3. Restart terminal/IDE")
    
    # Check music directories
    print(f"\n📁 Music Directory: {MUSIC_DIR}")
    print(f"📁 Output Directory: {OUTPUT_DIR}")
    
    print("\n🎵 Available Music:")
    moods = get_available_moods()
    
    if not moods or all(m["tracks"] == 0 for m in moods):
        print("⚠️ No music files found!")
        print("\n📥 To add music:")
        print("1. Download royalty-free music from:")
        print("   - Pixabay: https://pixabay.com/music/")
        print("   - Mixkit: https://mixkit.co/free-stock-music/")
        print("   - FreePD: https://freepd.com/")
        print(f"2. Place files in: {MUSIC_DIR}/[mood]/")
        print("   Moods: epic, emotional, uplifting")
    else:
        for mood_info in moods:
            print(f"  • {mood_info['name'].capitalize()}: {mood_info['tracks']} tracks")
    
    print("=" * 60)


if __name__ == "__main__":
    # Print system info when run directly
    print_system_info()
