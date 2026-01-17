# 🎬 Cinematic Audio Mixer for Chatterbox TTS

**Transform your TTS voice into professional motivational audio with automatic background music!**

---

## 🌟 Features

✅ **Automatic Background Music** - Randomly selects from your music library  
✅ **Mood-Based Selection** - Epic, Emotional, Uplifting  
✅ **Automatic Ducking** - Music dips when narrator speaks (sidechain compression)  
✅ **Professional Quality** - 192kbps MP3 output  
✅ **Local Processing** - No APIs, no internet required  
✅ **Royalty-Free Music** - Use Pixabay, Mixkit, FreePD  
✅ **CLI & GUI** - Command-line tool + Gradio web interface  
✅ **Batch Processing** - Mix multiple files at once  

---

## 🚀 Quick Start

### 1. Install FFmpeg

```powershell
# Windows (Winget)
winget install FFmpeg

# Or Chocolatey
choco install ffmpeg

# Verify installation
ffmpeg -version
```

### 2. Add Music Files

Download royalty-free music and organize by mood:

```
music/
├── epic/          # Powerful, cinematic tracks
├── emotional/     # Touching, heartfelt tracks
└── uplifting/     # Motivational, positive tracks
```

**Recommended Sources:**
- [Pixabay Music](https://pixabay.com/music/) - Free, commercial use
- [Mixkit](https://mixkit.co/free-stock-music/) - Free, commercial use
- [FreePD](https://freepd.com/) - Public domain

### 3. Test the System

```bash
# Run test suite
python test_audio_mixer.py

# Check system info
python mix_audio.py --info
```

### 4. Mix Your First Audio

```bash
# CLI method
python mix_audio.py voice.wav --mood epic

# Or use the Gradio UI
python app.py
# Navigate to "Cinematic Mixer" tab
```

---

## 💻 Usage

### Command Line Interface

#### Basic Usage
```bash
# Mix with epic music
python mix_audio.py voice.wav --mood epic

# Mix with emotional music
python mix_audio.py voice.wav --mood emotional

# Mix with uplifting music
python mix_audio.py voice.wav --mood uplifting
```

#### Advanced Options
```bash
# Custom output path
python mix_audio.py voice.wav --output final.mp3

# Adjust music volume (0.0-1.0)
python mix_audio.py voice.wav --volume 0.2

# Disable ducking
python mix_audio.py voice.wav --no-ducking

# Use specific music file
python mix_audio.py voice.wav --music "music/epic/my_track.mp3"
```

#### Batch Processing
```bash
# Mix multiple files
python mix_audio.py voice1.wav voice2.wav voice3.wav --mood epic

# Mix all WAV files in directory
python mix_audio.py *.wav --mood emotional
```

### Python API

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

### Gradio Web Interface

```bash
# Launch web interface
python app.py

# Navigate to "🎬 Cinematic Mixer" tab
# Upload voice file, select mood, click "Mix Audio"
```

---

## 🎯 One-Line Motivational Audio

Generate TTS + Mix with music in one command:

```bash
python -c "from modules.generation_functions import generate_turbo_speech; from modules.audio_mixer import mix_audio_with_music; voice = list(generate_turbo_speech('You are stronger than you think!', 'Morgan Freeman_male'))[-1][1]; mix_audio_with_music(voice, mood='epic')"
```

---

## 📁 Project Structure

```
Chatterbox TTS with Turbo/
├── modules/
│   ├── audio_mixer.py          # Core mixing engine
│   ├── ui_components.py         # Gradio UI components
│   └── ...
├── music/                       # Music library
│   ├── epic/                    # Epic/cinematic tracks
│   ├── emotional/               # Emotional tracks
│   └── uplifting/               # Uplifting tracks
├── output/                      # Mixed audio output
├── mix_audio.py                 # CLI tool
├── test_audio_mixer.py          # Test suite
├── AUDIO_MIXER_SETUP.md         # Detailed setup guide
└── README_CINEMATIC_MIXER.md    # This file
```

---

## 🎵 Music Setup

### Download Recommendations

**Epic/Cinematic:**
- Search: "epic cinematic", "powerful trailer", "heroic adventure"
- Duration: 2-5 minutes
- Style: Orchestral, dramatic, intense

**Emotional:**
- Search: "emotional piano", "touching moments", "heartfelt"
- Duration: 2-4 minutes
- Style: Piano, strings, ambient

**Uplifting:**
- Search: "uplifting motivation", "inspiring success", "positive energy"
- Duration: 2-4 minutes
- Style: Upbeat, energetic, optimistic

### File Organization

```bash
# Place downloaded files in mood folders
music/
├── epic/
│   ├── epic_cinematic_01.mp3
│   ├── powerful_trailer.mp3
│   └── heroic_adventure.mp3
├── emotional/
│   ├── emotional_piano.mp3
│   └── touching_moments.mp3
└── uplifting/
    ├── uplifting_motivation.mp3
    └── inspiring_success.mp3
```

---

## ⚙️ Configuration

### Audio Mixing Parameters

Edit `modules/audio_mixer.py` to customize:

```python
MUSIC_VOLUME = 0.15          # Background music volume (15%)
DUCKING_THRESHOLD = -30      # dB threshold for ducking
DUCKING_RATIO = 4            # Compression ratio
ATTACK_TIME = 0.1            # seconds
RELEASE_TIME = 0.5           # seconds
```

### Output Settings

- **Format**: MP3
- **Bitrate**: 192kbps
- **Codec**: libmp3lame
- **Naming**: `[voice]_cinematic_[mood].mp3`

---

## 🔧 Troubleshooting

### FFmpeg Not Found

```bash
# Install FFmpeg
winget install FFmpeg

# Restart terminal
# Verify installation
ffmpeg -version
```

### No Music Files

```bash
# Check music directory
python mix_audio.py --info

# Download music from:
# - https://pixabay.com/music/
# - https://mixkit.co/free-stock-music/
# - https://freepd.com/

# Place in music/[mood]/ folders
```

### Audio Quality Issues

```bash
# Reduce music volume
python mix_audio.py voice.wav --volume 0.1

# Disable ducking
python mix_audio.py voice.wav --no-ducking
```

---

## 🎬 Example Workflows

### Workflow 1: Generate TTS + Mix

```python
from modules.generation_functions import generate_turbo_speech
from modules.audio_mixer import mix_audio_with_music

# 1. Generate TTS
text = "Believe in yourself. You have unlimited potential!"
voice = "Morgan Freeman_male"

for progress, audio_path, status in generate_turbo_speech(text, voice):
    if audio_path:
        # 2. Mix with cinematic music
        final = mix_audio_with_music(
            voice_path=audio_path,
            mood="epic",
            enable_ducking=True
        )
        print(f"Final audio: {final}")
```

### Workflow 2: Batch Motivational Content

```bash
# Generate multiple motivational audios
python mix_audio.py \
    motivation1.wav \
    motivation2.wav \
    motivation3.wav \
    --mood uplifting \
    --volume 0.15
```

### Workflow 3: Custom Music Selection

```bash
# Use specific music track
python mix_audio.py voice.wav \
    --music "music/epic/my_favorite_track.mp3" \
    --volume 0.2
```

---

## 📊 Performance

- **Mixing Speed**: ~2-5 seconds per minute of audio
- **File Size**: ~2-3 MB per minute (192kbps MP3)
- **CPU Usage**: Moderate (FFmpeg processing)
- **Memory**: Low (~100-200 MB)

---

## 🎯 Use Cases

✅ **YouTube Motivational Videos**  
✅ **Podcast Intros/Outros**  
✅ **Social Media Content**  
✅ **Personal Motivation Audio**  
✅ **Audiobook Narration**  
✅ **E-learning Content**  
✅ **Meditation Guides**  
✅ **Affirmation Tracks**  

---

## 📝 License & Credits

### Software
- **Chatterbox TTS**: Original TTS system
- **FFmpeg**: LGPL/GPL (https://ffmpeg.org/)
- **Audio Mixer**: Custom implementation

### Music
- Always check music licenses before commercial use
- Recommended sources provide royalty-free music
- Attribution may be required (check individual licenses)

---

## 🆘 Support

### Documentation
- [Full Setup Guide](AUDIO_MIXER_SETUP.md)
- [Test Suite](test_audio_mixer.py)
- [CLI Tool](mix_audio.py)

### Diagnostics
```bash
# Run system check
python test_audio_mixer.py

# Check configuration
python mix_audio.py --info

# View help
python mix_audio.py --help
```

---

## 🎉 Ready to Create!

You now have a complete local audio mixing pipeline for creating professional motivational content!

**Next Steps:**
1. ✅ Install FFmpeg
2. ✅ Download music files
3. ✅ Run test suite
4. ✅ Create your first cinematic audio!

```bash
# Quick test
python mix_audio.py your_voice.wav --mood epic
```

**Result**: Professional Motiversity-style motivational audio ready for YouTube, podcasts, and social media! 🎬🎵

---

**Happy Creating! 🚀**
