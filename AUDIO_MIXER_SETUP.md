# 🎬 Cinematic Audio Mixer Setup Guide

Complete guide to set up and use the automatic background music mixing system.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [FFmpeg Installation](#ffmpeg-installation)
3. [Music Setup](#music-setup)
4. [Quick Start](#quick-start)
5. [CLI Usage](#cli-usage)
6. [Python API](#python-api)
7. [Gradio UI Integration](#gradio-ui-integration)
8. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

- **OS**: Windows 10/11
- **Python**: 3.8+
- **FFmpeg**: Latest version
- **Disk Space**: 500MB+ for music files

---

## 📥 FFmpeg Installation

### Method 1: Winget (Recommended)
```powershell
winget install FFmpeg
```

### Method 2: Chocolatey
```powershell
choco install ffmpeg
```

### Method 3: Manual Installation

1. **Download FFmpeg**
   - Visit: https://ffmpeg.org/download.html
   - Click "Windows builds from gyan.dev"
   - Download: `ffmpeg-release-essentials.zip`

2. **Extract Files**
   ```powershell
   # Extract to C:\ffmpeg
   Expand-Archive -Path ffmpeg-release-essentials.zip -DestinationPath C:\ffmpeg
   ```

3. **Add to PATH**
   ```powershell
   # Add FFmpeg to system PATH
   $env:Path += ";C:\ffmpeg\bin"
   
   # Make permanent (run as Administrator)
   [Environment]::SetEnvironmentVariable(
       "Path",
       [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\ffmpeg\bin",
       "Machine"
   )
   ```

4. **Verify Installation**
   ```powershell
   ffmpeg -version
   ```

---

## 🎵 Music Setup

### Directory Structure
```
Chatterbox TTS with Turbo/
├── music/
│   ├── epic/          # Epic/cinematic tracks
│   ├── emotional/     # Emotional/touching tracks
│   └── uplifting/     # Uplifting/motivational tracks
└── output/            # Mixed audio output
```

### Download Royalty-Free Music

#### 1. Pixabay Music (Recommended)
- **URL**: https://pixabay.com/music/
- **License**: Free for commercial use
- **Genres**: Epic, Emotional, Uplifting, Cinematic

**Download Steps:**
1. Visit Pixabay Music
2. Search for: "epic cinematic", "emotional piano", "uplifting motivation"
3. Download MP3 files
4. Place in appropriate mood folders

**Recommended Tracks:**
- Epic: "Epic Cinematic", "Powerful Trailer", "Heroic Adventure"
- Emotional: "Emotional Piano", "Touching Moments", "Heartfelt"
- Uplifting: "Uplifting Motivation", "Inspiring Success", "Positive Energy"

#### 2. Mixkit
- **URL**: https://mixkit.co/free-stock-music/
- **License**: Free for commercial use
- **Categories**: Cinematic, Ambient, Upbeat

#### 3. FreePD
- **URL**: https://freepd.com/
- **License**: Public Domain
- **Genres**: Orchestral, Ambient, Electronic

### Quick Music Setup Script

```powershell
# Create a PowerShell script to organize music
$musicUrls = @{
    "epic" = @(
        "https://example.com/epic1.mp3",
        "https://example.com/epic2.mp3"
    )
    "emotional" = @(
        "https://example.com/emotional1.mp3"
    )
    "uplifting" = @(
        "https://example.com/uplifting1.mp3"
    )
}

# Note: Replace with actual download URLs
# Manual download recommended for quality control
```

---

## 🚀 Quick Start

### 1. Check System Status
```bash
python mix_audio.py --info
```

Expected output:
```
============================================================
🎬 CINEMATIC AUDIO MIXER - SYSTEM INFO
============================================================
FFmpeg: ✅ Installed

📁 Music Directory: C:\...\music
📁 Output Directory: C:\...\output

🎵 Available Music:
  • Epic: 5 tracks
  • Emotional: 3 tracks
  • Uplifting: 4 tracks
============================================================
```

### 2. Test with Sample Audio

Create a test voice file or use existing TTS output:
```bash
# Mix with epic music
python mix_audio.py "path/to/voice.wav" --mood epic

# Output: output/voice_cinematic_epic.mp3
```

---

## 💻 CLI Usage

### Basic Commands

#### Single File Mixing
```bash
# Mix with epic music (default)
python mix_audio.py voice.wav

# Mix with emotional music
python mix_audio.py voice.wav --mood emotional

# Mix with uplifting music
python mix_audio.py voice.wav --mood uplifting
```

#### Custom Output Path
```bash
python mix_audio.py voice.wav --output "final_motivational.mp3"
```

#### Use Specific Music File
```bash
python mix_audio.py voice.wav --music "music/epic/my_favorite.mp3"
```

#### Adjust Music Volume
```bash
# Louder music (30% volume)
python mix_audio.py voice.wav --volume 0.3

# Quieter music (10% volume)
python mix_audio.py voice.wav --volume 0.1
```

#### Disable Ducking
```bash
# No automatic volume reduction
python mix_audio.py voice.wav --no-ducking
```

### Batch Processing

```bash
# Mix multiple files with same mood
python mix_audio.py voice1.wav voice2.wav voice3.wav --mood epic

# Mix all WAV files in directory
python mix_audio.py *.wav --mood emotional
```

### One-Line Motivational Audio Generation

```bash
# Complete workflow: Generate TTS + Mix with music
python -c "from modules.generation_functions import generate_turbo_speech; from modules.audio_mixer import mix_audio_with_music; voice = list(generate_turbo_speech('You are stronger than you think. Keep pushing forward!', 'Morgan Freeman_male'))[-1][1]; mix_audio_with_music(voice, mood='epic')"
```

---

## 🐍 Python API

### Basic Usage

```python
from modules.audio_mixer import mix_audio_with_music

# Mix voice with background music
output = mix_audio_with_music(
    voice_path="voice.wav",
    mood="epic",
    music_volume=0.15,
    enable_ducking=True
)

print(f"Output: {output}")
```

### Advanced Usage

```python
from modules.audio_mixer import (
    mix_audio_with_music,
    batch_mix_audio,
    get_available_moods,
    select_random_music
)

# Check available moods
moods = get_available_moods()
for mood in moods:
    print(f"{mood['name']}: {mood['tracks']} tracks")

# Select specific music
music_file = select_random_music("epic")

# Mix with custom settings
output = mix_audio_with_music(
    voice_path="voice.wav",
    music_path=music_file,
    output_path="custom_output.mp3",
    music_volume=0.2,
    enable_ducking=True
)

# Batch processing
voice_files = ["voice1.wav", "voice2.wav", "voice3.wav"]
results = batch_mix_audio(voice_files, mood="emotional")
```

### Integration with TTS

```python
from modules.generation_functions import generate_turbo_speech
from modules.audio_mixer import mix_audio_with_music

# Generate speech
text = "Believe in yourself. You have the power to achieve greatness!"
voice = "Morgan Freeman_male"

# Generate TTS
for progress, audio_path, status in generate_turbo_speech(text, voice):
    if audio_path:
        # Mix with cinematic music
        final_audio = mix_audio_with_music(
            voice_path=audio_path,
            mood="epic",
            enable_ducking=True
        )
        print(f"Final audio: {final_audio}")
```

---

## 🎨 Gradio UI Integration

The audio mixer is integrated into the Gradio interface with:

- **Mood Selection**: Choose epic, emotional, or uplifting
- **Auto-Mix Toggle**: Enable/disable automatic mixing
- **Volume Control**: Adjust background music volume
- **Preview**: Listen before downloading

Access via the web interface after running:
```bash
python app.py
```

---

## 🔧 Troubleshooting

### FFmpeg Not Found

**Error**: `❌ FFmpeg not found!`

**Solution**:
1. Install FFmpeg (see installation section)
2. Restart terminal/IDE
3. Verify: `ffmpeg -version`

### No Music Files Found

**Error**: `⚠️ No music files found for mood: epic`

**Solution**:
1. Download music from Pixabay/Mixkit/FreePD
2. Place files in correct mood folder:
   - `music/epic/` for epic tracks
   - `music/emotional/` for emotional tracks
   - `music/uplifting/` for uplifting tracks
3. Supported formats: MP3, WAV, M4A, OGG, FLAC

### Audio Quality Issues

**Problem**: Output sounds distorted or too quiet

**Solution**:
```bash
# Adjust music volume
python mix_audio.py voice.wav --volume 0.1  # Quieter music

# Disable ducking if causing issues
python mix_audio.py voice.wav --no-ducking
```

### FFmpeg Timeout

**Error**: `❌ FFmpeg timeout`

**Solution**:
- File may be too large
- Try shorter audio clips
- Check system resources

### Permission Errors

**Error**: `Permission denied` when writing output

**Solution**:
```powershell
# Run as administrator or check folder permissions
icacls "output" /grant Users:F
```

---

## 📊 Audio Mixing Parameters

### Default Settings

```python
MUSIC_VOLUME = 0.15          # 15% of original volume
DUCKING_THRESHOLD = -30      # dB threshold for ducking
DUCKING_RATIO = 4            # Compression ratio
ATTACK_TIME = 0.1            # seconds
RELEASE_TIME = 0.5           # seconds
```

### Customization

Edit `modules/audio_mixer.py` to adjust:
- Volume levels
- Ducking sensitivity
- Attack/release times
- Output format and bitrate

---

## 🎯 Best Practices

1. **Music Selection**
   - Use 2-3 minute tracks minimum
   - Match mood to content
   - Test different tracks for best fit

2. **Volume Balance**
   - Start with 15% music volume
   - Adjust based on voice clarity
   - Enable ducking for better intelligibility

3. **File Organization**
   - Name files descriptively
   - Organize by mood
   - Keep backups of originals

4. **Quality**
   - Use high-quality source audio (192kbps+)
   - Avoid compressed voice files
   - Export at 192kbps MP3 or higher

---

## 📞 Support

For issues or questions:
1. Check this guide
2. Run `python mix_audio.py --info` for diagnostics
3. Verify FFmpeg installation
4. Check music file availability

---

## 🎬 Example Workflow

Complete motivational audio creation:

```bash
# 1. Generate TTS (via Gradio UI or Python)
# 2. Mix with music
python mix_audio.py "generated_voice.wav" --mood epic --volume 0.15

# 3. Output ready at: output/generated_voice_cinematic_epic.mp3
```

**Result**: Professional cinematic motivational audio ready for:
- YouTube videos
- Podcasts
- Social media
- Presentations
- Personal motivation

---

## 📝 License

This audio mixer uses:
- FFmpeg (LGPL/GPL)
- Royalty-free music (various licenses)
- Always check music licenses before commercial use

---

**🎬 Ready to create cinematic motivational audio!**
