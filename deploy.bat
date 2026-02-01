@echo off
echo ========================================
echo Chatterbox TTS - GitHub Deployment
echo ========================================
echo.

echo Checking git status...
git status
echo.

echo Adding all changes...
git add .
echo.

echo Committing changes...
git commit -m "Add FastAPI voice upload + generation API with Supabase storage and bulk voice cloning feature"
echo.

echo Pushing to GitHub...
git push origin master
echo.

echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://render.com
echo 2. Create a new Web Service
echo 3. Connect your GitHub repository
echo 4. Follow the instructions in RENDER_DEPLOYMENT.md
echo.
pause
