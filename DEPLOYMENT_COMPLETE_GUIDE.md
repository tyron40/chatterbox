# 🚀 Complete Deployment Guide - Chatterbox TTS API

## ✅ What's Been Completed

### 1. Supabase Setup ✓
- **Project Created**: `iwitmebruaqivzkacecs`
- **Storage Bucket**: `voices` (public)
- **Test Upload**: Successful
- **Public URL**: Working

### 2. Code Repository ✓
- **GitHub Repo**: https://github.com/tyron40/chatterbox
- **Branch**: master
- **All Files Pushed**: Yes

### 3. Configuration Files ✓
- `api.py` - FastAPI application
- `render.yaml` - Render Blueprint
- `.env` - Local environment variables
- `setup_supabase.py` - Supabase setup script

---

## 🎯 Deploy to Render (Step-by-Step)

### Step 1: Go to Render Dashboard
1. Visit: https://dashboard.render.com/
2. Sign in with GitHub (or create account)
3. Connect your GitHub account if not already connected

### Step 2: Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Blueprint"**
3. Click **"New Blueprint Instance"**

### Step 3: Connect Repository
1. Search for: `tyron40/chatterbox`
2. Click **"Connect"**
3. If repo not found, click **"Configure account"** and grant access

### Step 4: Configure Blueprint
1. **Blueprint Name**: `chatterbox-api` (or any name you prefer)
2. **Branch**: `master`
3. Click **"Apply"**

### Step 5: Set Environment Variables
Render will prompt you to set these variables:

```
SUPABASE_URL=https://iwitmebruaqivzkacecs.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3aXRtZWJydWFxaXZ6a2FjZWNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTk4MjI2OSwiZXhwIjoyMDg1NTU4MjY5fQ.H_gb3dj7Lz46LhbYY3pc7nBQLOkiyt4yjOj0-58NyCA
SUPABASE_BUCKET=voices
```

### Step 6: Deploy
1. Click **"Create Blueprint Instance"**
2. Wait for deployment (5-10 minutes)
3. Monitor build logs for any errors

### Step 7: Get Your API URL
Once deployed, you'll get a URL like:
```
https://chatterbox-api.onrender.com
```

---

## 🧪 Test Your Deployed API

### 1. Check API Status
```bash
curl https://your-app.onrender.com/
```

Expected response:
```json
{
  "status": "ok",
  "message": "Chatterbox TTS API is running",
  "version": "1.0.0"
}
```

### 2. Upload a Voice
```bash
curl -X POST https://your-app.onrender.com/voices/upload \
  -F "file=@path/to/voice.wav" \
  -F "voice_name=my_voice"
```

### 3. List Voices
```bash
curl https://your-app.onrender.com/voices/list
```

### 4. Generate Speech
```bash
curl -X POST https://your-app.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of the text to speech system.",
    "voice_name": "my_voice",
    "model_type": "main"
  }' \
  --output generated_speech.wav
```

### 5. Delete a Voice
```bash
curl -X DELETE https://your-app.onrender.com/voices/my_voice
```

---

## 📊 API Endpoints Reference

### Health Check
- **GET** `/`
- Returns API status

### Upload Voice
- **POST** `/voices/upload`
- **Form Data**:
  - `file`: WAV audio file
  - `voice_name`: Name for the voice
- **Returns**: Upload confirmation with public URL

### List Voices
- **GET** `/voices/list`
- **Returns**: Array of voice objects with names and URLs

### Generate Speech
- **POST** `/generate`
- **JSON Body**:
  ```json
  {
    "text": "Text to synthesize",
    "voice_name": "voice_name",
    "model_type": "main|multilingual|turbo",
    "language": "en" (optional, for multilingual)
  }
  ```
- **Returns**: WAV audio file

### Delete Voice
- **DELETE** `/voices/{voice_name}`
- **Returns**: Deletion confirmation

### Bulk Clone Voices
- **POST** `/voices/bulk-clone`
- **Form Data**:
  - `files`: Multiple WAV files
  - `voice_names`: Comma-separated names
- **Returns**: Bulk upload results

---

## ⚙️ Configuration Details

### Render Service Settings
- **Type**: Web Service
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
- **Auto-Deploy**: Yes (on git push)

### Free Tier Limitations
- **Sleep after 15 min** of inactivity
- **First request** takes ~30 seconds (cold start)
- **750 hours/month** of runtime
- **100 GB bandwidth/month**

### Supabase Free Tier
- **500 MB storage**
- **50 MB database**
- **2 GB bandwidth/month**

---

## 🔧 Troubleshooting

### Build Fails
1. Check Render build logs
2. Verify `requirements.txt` is correct
3. Ensure Python version compatibility

### API Returns 500 Error
1. Check Render logs: Dashboard → Your Service → Logs
2. Verify environment variables are set correctly
3. Check Supabase credentials

### Voice Upload Fails
1. Verify Supabase bucket is public
2. Check bucket name matches `SUPABASE_BUCKET`
3. Ensure file is valid WAV format

### Slow Response Times
- **First request**: Normal (cold start ~30s)
- **Subsequent requests**: Should be fast
- **Solution**: Keep service warm with periodic pings

---

## 🎨 Optional: Keep Service Warm

Create a cron job or use a service like UptimeRobot to ping your API every 10 minutes:

```bash
# Ping every 10 minutes
curl https://your-app.onrender.com/
```

This prevents the service from sleeping on the free tier.

---

## 📝 Next Steps After Deployment

1. **Test all endpoints** with real voice files
2. **Monitor usage** in Render dashboard
3. **Check Supabase storage** usage
4. **Set up monitoring** (optional)
5. **Share your API** with users!

---

## 🌐 Your Deployment URLs

- **GitHub Repo**: https://github.com/tyron40/chatterbox
- **Supabase Project**: https://supabase.com/dashboard/project/iwitmebruaqivzkacecs
- **Render Service**: (Will be available after deployment)

---

## 📞 Support

If you encounter issues:
1. Check Render logs
2. Check Supabase dashboard
3. Review this guide
4. Check GitHub repo for updates

---

**Deployment Status**: ✅ Ready to Deploy
**Estimated Time**: 10-15 minutes
**Difficulty**: Easy

Good luck with your deployment! 🚀
