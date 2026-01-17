@echo off
echo ========================================
echo FFmpeg Installation Helper
echo ========================================
echo.

echo Step 1: Installing FFmpeg via winget...
winget install FFmpeg

echo.
echo Step 2: Refreshing environment variables...
echo Please close and reopen your terminal after this completes.
echo.

echo Step 3: Verify installation by running:
echo    ffmpeg -version
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo IMPORTANT: You must restart your terminal for FFmpeg to work!
echo.
echo After restarting, verify with: ffmpeg -version
echo.
pause
