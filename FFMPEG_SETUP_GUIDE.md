# FFmpeg Setup Guide for Windows

## ✅ FFmpeg Installation Complete - Now Make It Work!

The FFmpeg installation via `winget` has completed, but you need to refresh your environment variables for it to work.

---

## 🔧 Quick Fix (Choose One Method)

### Method 1: Restart Terminal (EASIEST)
1. **Close this PowerShell window completely**
2. **Open a new PowerShell window**
3. Test: `ffmpeg -version`
4. ✅ Should now work!

### Method 2: Refresh Environment in Current Terminal
```powershell
# Run this command to refresh PATH:
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Then test:
ffmpeg -version
```

### Method 3: Restart VS Code
1. Close VS Code completely
2. Reopen VS Code
3. Open new terminal
4. Test: `ffmpeg -version`

---

## 🔍 Verify FFmpeg Installation

After refreshing, run:
```powershell
ffmpeg -version
```

**Expected output:**
```
ffmpeg version 8.0.1-full_build
built with gcc 13.2.0 (Rev1, Built by MSYS2 project)
configuration: --enable-gpl --enable-version3 ...
```

---

## 🎬 Test the Cinematic Mixer

Once FFmpeg is working, test the system:

```bash
# Check system status
python mix_audio.py --info

# Should show:
# ✅ FFmpeg: Available
# 📁 Music Library: 0 tracks (add music files)
```

---

## 📥 Download Music Files

After FFmpeg is working, download music:

```bash
# Use the helper script:
python download_sample_music.py

# Or manually download from:
# - Pixabay: https://pixabay.com/music/
# - Mixkit: https://mixkit.co/free-stock-music/
# - FreePD: https://freepd.com/
```

**Place files in:**
- `music/epic/` - Powerful, cinematic tracks
- `music/emotional/` - Touching, heartfelt tracks
- `music/uplifting/` - Motivational, energetic tracks

**Recommended:** 3-5 tracks per mood

---

## 🚀 Start Creating!

### Web Interface:
```bash
python app.py
# Open: http://127.0.0.1:7860
# Navigate to: 🎬 Cinematic Mixer tab
```

### CLI Tool:
```bash
# Mix a voice file with epic music
python mix_audio.py voice.wav --mood epic

# Custom volume
python mix_audio.py voice.wav --mood emotional --volume 0.2

# Batch processing
python mix_audio.py file1.wav file2.wav file3.wav --mood uplifting
```

---

## ❓ Troubleshooting

### FFmpeg Still Not Found?

**Check if FFmpeg was installed:**
```powershell
# Check installation location:
Get-Command ffmpeg -ErrorAction SilentlyContinue

# If nothing shows, reinstall:
winget install FFmpeg --force
```

**Manual PATH Check:**
```powershell
# View current PATH:
$env:Path -split ';'

# Look for FFmpeg directory (usually):
# C:\Program Files\FFmpeg\bin
# or
# C:\Users\YourName\AppData\Local\Microsoft\WinGet\Packages\...
```

**Add FFmpeg to PATH manually (if needed):**
1. Press `Win + X` → System
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find "Path"
5. Click "Edit"
6. Click "New"
7. Add FFmpeg bin directory (e.g., `C:\Program Files\FFmpeg\bin`)
8. Click OK on all windows
9. Restart terminal

---

## 📖 Additional Resources

- **Quick Start**: `QUICK_START.md`
- **Complete Guide**: `README_CINEMATIC_MIXER.md`
- **Setup Guide**: `AUDIO_MIXER_SETUP.md`
- **CLI Help**: `python mix_audio.py --help`

---

## ✅ Next Steps

1. ✅ **Restart terminal** (or refresh PATH)
2. ✅ **Verify FFmpeg**: `ffmpeg -version`
3. ✅ **Download music**: `python download_sample_music.py`
4. ✅ **Test system**: `python mix_audio.py --info`
5. ✅ **Start creating**: `python app.py`

---

**🎬 Once FFmpeg is working, you're ready to create professional Motiversity-style motivational content!**
