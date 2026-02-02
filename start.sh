#!/usr/bin/env bash
# Render startup script with fallback port
# Uses $PORT from Render, falls back to 10000 if not set
uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}
