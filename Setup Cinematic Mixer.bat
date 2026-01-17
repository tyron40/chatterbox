@echo off
echo ============================================================
echo    CINEMATIC AUDIO MIXER - SETUP WIZARD
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo [1/4] Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [!] FFmpeg not found!
    echo.
    echo Installing FFmpeg via winget...
    winget install FFmpeg
    if errorlevel 1 (
        echo [ERROR] FFmpeg installation failed!
        echo.
        echo Please install manually:
        echo 1. Download from: https://ffmpeg.org/download.html
        echo 2. Extract and add to PATH
        echo 3. Restart this script
        pause
        exit /b 1
    )
    echo [OK] FFmpeg installed successfully!
) else (
    echo [OK] FFmpeg is already installed
)

echo.
echo [2/4] Creating directory structure...
if not exist "music\epic" mkdir "music\epic"
if not exist "music\emotional" mkdir "music\emotional"
if not exist "music\uplifting" mkdir "music\uplifting"
if not exist "output" mkdir "output"
echo [OK] Directories created

echo.
echo [3/4] Running system tests...
python test_audio_mixer.py
if errorlevel 1 (
    echo [WARNING] Some tests failed. Please review the output above.
) else (
    echo [OK] All tests passed!
)

echo.
echo [4/4] Setup complete!
echo.
echo ============================================================
echo    NEXT STEPS
echo ============================================================
echo.
echo 1. Download royalty-free music:
echo    - Pixabay: https://pixabay.com/music/
echo    - Mixkit: https://mixkit.co/free-stock-music/
echo    - FreePD: https://freepd.com/
echo.
echo 2. Place music files in:
echo    - music\epic\     (for epic/cinematic tracks)
echo    - music\emotional\ (for emotional tracks)
echo    - music\uplifting\ (for uplifting tracks)
echo.
echo 3. Test the mixer:
echo    python mix_audio.py your_voice.wav --mood epic
echo.
echo 4. Or use the web interface:
echo    python app.py
echo    (Navigate to "Cinematic Mixer" tab)
echo.
echo ============================================================
echo.
echo For detailed instructions, see:
echo - README_CINEMATIC_MIXER.md
echo - AUDIO_MIXER_SETUP.md
echo.
pause
