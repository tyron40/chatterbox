#!/usr/bin/env bash
set -e  # Exit on error
set -x  # Print commands for debugging

echo "==> Starting Chatterbox TTS API..."
echo "==> PORT environment variable: ${PORT:-not set, using 10000}"
echo "==> Python version:"
python --version
echo "==> Current directory:"
pwd
echo "==> Directory contents:"
ls -la
echo "==> Checking if main.py exists:"
ls -la main.py
echo "==> Testing Python import:"
python -c "from main import app; print('Import successful!')" || {
    echo "ERROR: Failed to import app from main.py"
    echo "Trying to import api.py directly:"
    python -c "from api import app; print('API import successful!')"
    exit 1
}
echo "==> Starting uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000} --log-level debug
