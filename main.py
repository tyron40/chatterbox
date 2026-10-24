"""
Main entrypoint for Render deployment
Imports the FastAPI app from api.py
"""
from api import app
from voice_api import app as authenticated_voice_app

# Preserve the existing public API and mount the new authenticated endpoints.
app.mount('/secure', authenticated_voice_app)

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
