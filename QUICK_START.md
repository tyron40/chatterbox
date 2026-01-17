# 🚀 Quick Start Guide - Cinematic Audio Mixer

Get up and running in 5 minutes!

---

## ⚡ Super Quick Start

```bash
# 1. Run setup wizard (Windows)
"Setup Cinematic Mixer.bat"

# 2. Download music helper
python download_sample_music.py

# 3. Test the system
python test_audio_mixer.py

# 4. Mix your first audio
python mix_audio.py voice.wav --mood epic
```

---

## 📋 Step-by-Step Setup

### Step 1: Install FFmpeg (2 minutes)

**Windows:**
```powershell
winget install FFmpeg
```

**Verify:**
```bash
ffmpeg -version
```

### Step 2: Download Music (5-10 minutes)

```bash
# Open music download helper
python download_sample_music.py
```

**Or manually:**
1. Visit [Pixabay Music](https://pixabay.com/music/)
2. Search for "epic cinematic"
3. Download 2-3 MP3 files
4. Place in `music/epic/` folder

Repeat for `emotional` and `uplifting` moods.

### Step 3: Test System (1 minute)

```bash
python test_audio_mixer.py
```

Expected output:
```
✅ PASS: FFmpeg
✅ PASS: Directories
✅ PASS: Music Files
🎉 ALL TESTS PASSED!
```

### Step 4: Create Your First Cinematic Audio (30 seconds)

```bash
# Mix a voice file with epic music
python mix_audio.py your_voice.wav --mood epic

# Output: output/your_voice_cinematic_epic.mp3
```

---

## 🎯 Common Commands

### Basic Mixing
```bash
# Epic mood
python mix_audio.py voice.wav --mood epic

# Emotional mood
python mix_audio.py voice.wav --mood emotional

# Uplifting mood
python mix_audio.py voice.wav --mood uplifting
```

### Advanced Options
```bash
# Custom output path
python mix_audio.py voice.wav --output final.mp3

# Adjust music volume (quieter)
python mix_audio.py voice.wav --volume 0.1

# Adjust music volume (louder)
python mix_audio.py voice.wav --volume 0.3

# Disable ducking
python mix_audio.py voice.wav --no-ducking
```

### Batch Processing
```bash
# Mix multiple files
python mix_audio.py file1.wav file2.wav file3.wav --mood epic

# Mix all WAV files
python mix_audio.py *.wav --mood emotional
```

### System Info
```bash
# Check system status
python mix_audio.py --info

# Run tests
python test_audio_mixer.py

# Get help
python mix_audio.py --help
```

---

## 🎬 Complete Workflow Example

### Generate TTS + Mix in One Go

```python
# example_workflow.py
from modules.generation_functions import generate_turbo_speech
from modules.audio_mixer import mix_audio_with_music

# 1. Generate TTS
text = "You are capable of amazing things. Never give up on your dreams!"
voice = "Morgan Freeman_male"

print("Generating speech...")
for progress, audio_path, status in generate_turbo_speech(text, voice):
    if audio_path:
        print(f"✅ Speech generated: {audio_path}")
        
        # 2. Mix with cinematic music
        print("Mixing with epic music...")
        final_audio = mix_audio_with_music(
            voice_path=audio_path,
            mood="epic",
            music_volume=0.15,
            enable_ducking=True
        )
        
        if final_audio:
            print(f"🎬 Final audio: {final_audio}")
            print("✅ Done! Ready for YouTube/social media!")
```

Run it:
```bash
python example_workflow.py
```

---

## 🌐 Web Interface

```bash
# Launch Gradio interface
python app.py

# Open browser to: http://127.0.0.1:7860
# Navigate to "🎬 Cinematic Mixer" tab
```

**Steps in UI:**
1. Upload voice file
2. Select mood (epic/emotional/uplifting)
3. Adjust volume (optional)
4. Click "Mix Audio"
5. Download result!

---

## 📁 Directory Structure

```
Chatterbox TTS with Turbo/
├── music/                      # Your music library
│   ├── epic/                   # Epic/cinematic tracks
│   │   ├── track1.mp3
│   │   └── track2.mp3
│   ├── emotional/              # Emotional tracks
│   │   └── track1.mp3
│   └── uplifting/              # Uplifting tracks
│       └── track1.mp3
├── output/                     # Mixed audio output
│   └── voice_cinematic_epic.mp3
├── mix_audio.py                # CLI tool
├── test_audio_mixer.py         # Test suite
└── download_sample_music.py    # Music download helper
```

---

## 🎵 Music Recommendations

### Epic/Cinematic (3-5 tracks)
- Duration: 2-5 minutes
- Style: Orchestral, dramatic
- Search: "epic cinematic", "powerful trailer"

### Emotional (3-5 tracks)
- Duration: 2-4 minutes
- Style: Piano, strings
- Search: "emotional piano", "touching moments"

### Uplifting (3-5 tracks)
- Duration: 2-4 minutes
- Style: Upbeat, energetic
- Search: "uplifting motivation", "inspiring success"

---

## 🔧 Troubleshooting

### FFmpeg Not Found
```bash
# Install FFmpeg
winget install FFmpeg

# Restart terminal
# Verify
ffmpeg -version
```

### No Music Files
```bash
# Check status
python mix_audio.py --info

# Download music
python download_sample_music.py
```

### Audio Too Quiet/Loud
```bash
# Adjust music volume
python mix_audio.py voice.wav --volume 0.1  # Quieter
python mix_audio.py voice.wav --volume 0.3  # Louder
```

---

## 📖 Full Documentation

- **Setup Guide**: `AUDIO_MIXER_SETUP.md`
- **README**: `README_CINEMATIC_MIXER.md`
- **This Guide**: `QUICK_START.md`

---

## ✅ Checklist

- [ ] FFmpeg installed (`ffmpeg -version`)
- [ ] Music files downloaded (3+ per mood)
- [ ] Tests passing (`python test_audio_mixer.py`)
- [ ] First audio mixed successfully
- [ ] Output sounds good

---

## 🎉 You're Ready!

Create professional motivational audio like:
- Motiversity
- Fearless Motivation
- YouTube motivational channels

**One command to rule them all:**
```bash
python mix_audio.py your_voice.wav --mood epic
```

**Result**: Professional cinematic motivational audio! 🎬🎵

---

**Need Help?**
- Run: `python mix_audio.py --help`
- Check: `python test_audio_mixer.py`
- Read: `AUDIO_MIXER_SETUP.md`

**Happy Creating! 🚀**
