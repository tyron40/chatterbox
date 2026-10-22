# Shared voice service

This repo now includes `voice_api.py`, a separate HTTP API alongside the existing Gradio UI.

## Setup on a GPU-capable Python host

```bash
pip install -r requirements.txt -r requirements-api.txt
pip install faster-whisper   # optional offline speech-to-text
export VOICE_API_KEY='replace-with-a-long-random-secret'
uvicorn voice_api:app --host 127.0.0.1 --port 8000
```

Use a TLS reverse proxy and authenticated server-to-server requests in production. Do **not** embed `VOICE_API_KEY` in browser JavaScript or public mobile app bundles; a trusted backend should call this API. Rate limits, request quotas, abuse controls and user access controls are required before exposing publicly. Do not allow arbitrary public uploads from children.

- `GET /health` public health check, does not prove models are loaded.
- `POST /v1/speech` JSON `{"text":"Hello","voice":"an existing voice name"}`, bearer token, returns WAV.
- `POST /v1/transcriptions` multipart field `file`, bearer token, returns JSON `{"text":"...","language":"en"}`. Needs optional `faster-whisper` package and downloads a pretrained Whisper model on first use.
- STT is processed on the host, not on the caller's device. Temporary uploads are deleted after processing; provider/server logs and hosting configuration still require review.

The API limits speech text to 500 characters and audio uploads to 12 MB; requests are serialized to reduce model contention. This is a development integration, **not a validated production deployment**. Confirm model licenses, output quality, voice consent, child privacy, and hosting capacity before launch.

GitHub hosts code but does not run Python model inference. The hosted browser widget in Tots Learning Adventures uses browser SpeechRecognition and is **not** connected to this API automatically.
