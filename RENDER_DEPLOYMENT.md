# 🚀 Deploy Chatterbox TTS API to Render + Supabase

This guide walks you through deploying your Chatterbox TTS project as a public API using **Render (Free hosting)** + **Supabase Storage (Free voice files)**.

## 📋 What You'll Get

✅ **Public API URL**: `https://your-app.onrender.com`

✅ **Endpoints**:
- `POST /upload-voice` → Upload voice files
- `GET /voices` → List all voices
- `POST /generate` → Generate speech from text
- `DELETE /voices/{voice_id}` → Delete a voice

✅ **Persistent Storage**: Voice files stored forever on Supabase

---

## 🎯 Step 1: Set Up Supabase Storage

### 1.1 Create Supabase Project

1. Go to [Supabase](https://supabase.com)
2. Click **"New Project"**
3. Fill in:
   - **Name**: `chatterbox-voices`
   - **Database Password**: (create a strong password)
   - **Region**: Choose closest to you
4. Click **"Create new project"** (takes ~2 minutes)

### 1.2 Create Storage Bucket

1. In your Supabase project, go to **Storage** (left sidebar)
2. Click **"Create a new bucket"**
3. Settings:
   - **Name**: `voices`
   - **Public bucket**: ✅ **ON** (important!)
4. Click **"Create bucket"**

### 1.3 Get Your Supabase Credentials

1. Go to **Project Settings** → **API**
2. Copy these values (you'll need them for Render):
   - ✅ **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - ✅ **service_role key** (under "Project API keys" - keep this secret!)

---

## 🎯 Step 2: Prepare Your GitHub Repository

### 2.1 Commit Your Changes

Open terminal in your project directory:

```bash
# Add all changes
git add .

# Commit with message
git commit -m "Add FastAPI voice upload + generation with Supabase storage"

# Push to GitHub
git push origin master
```

### 2.2 Verify Files Are Pushed

Make sure these files are in your GitHub repo:
- ✅ `api.py` (FastAPI application)
- ✅ `requirements.txt` (with FastAPI, Supabase dependencies)
- ✅ `modules/` (all your TTS modules)
- ✅ `src/` (Chatterbox source code)

---

## 🎯 Step 3: Deploy to Render

### 3.1 Create Render Account

1. Go to [Render](https://render.com)
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### 3.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Click **"Connect a repository"**
3. Find and select your repository: `tyron40/chatterbox`
4. Click **"Connect"**

### 3.3 Configure Service Settings

**Basic Settings:**
- **Name**: `chatterbox-api` (or your preferred name)
- **Region**: Choose closest to you
- **Branch**: `master` (or `main`)
- **Root Directory**: (leave empty)
- **Environment**: **Python**
- **Build Command**:
  ```
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```
  uvicorn api:app --host 0.0.0.0 --port 10000
  ```

**Instance Type:**
- Select **"Free"** (0 cost)

### 3.4 Add Environment Variables

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** and add these:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | Your Supabase Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Your Supabase service_role key |
| `SUPABASE_BUCKET` | `voices` |

**Important**: Keep `SUPABASE_SERVICE_ROLE_KEY` secret!

### 3.5 Deploy

1. Click **"Create Web Service"**
2. Render will start building your app (takes 5-10 minutes first time)
3. Watch the logs for any errors

---

## 🎯 Step 4: Test Your API

### 4.1 Get Your API URL

Once deployed, Render gives you a URL like:
```
https://chatterbox-api.onrender.com
```

### 4.2 Test Health Check

Open in browser:
```
https://YOUR-RENDER-URL/health
```

Should return:
```json
{
  "ok": true,
  "supabase_connected": true,
  "device": "cpu"
}
```

### 4.3 Test API Documentation

Open:
```
https://YOUR-RENDER-URL/docs
```

You'll see interactive Swagger documentation where you can test all endpoints!

---

## 🎯 Step 5: Use Your API

### Example 1: Upload a Voice

```javascript
const formData = new FormData();
formData.append("file", audioFile); // Your audio file
formData.append("name", "Morgan Freeman");
formData.append("gender", "male");
formData.append("language", "en");

const response = await fetch("https://YOUR-RENDER-URL/upload-voice", {
  method: "POST",
  body: formData
});

const data = await response.json();
console.log(data.url); // Public URL to voice file
```

### Example 2: List All Voices

```javascript
const response = await fetch("https://YOUR-RENDER-URL/voices");
const data = await response.json();
console.log(data.voices); // Array of voice objects
```

### Example 3: Generate Speech

```javascript
const formData = new FormData();
formData.append("text", "Hello! This is a test.");
formData.append("voice_url", "https://xxxxx.supabase.co/storage/v1/object/public/voices/voice.wav");
formData.append("model_type", "turbo");

const response = await fetch("https://YOUR-RENDER-URL/generate", {
  method: "POST",
  body: formData
});

const audioBlob = await response.blob();
const audioUrl = URL.createObjectURL(audioBlob);
// Play or download the audio
```

### Example 4: Delete a Voice

```javascript
const voiceId = "abc-123-def";
const response = await fetch(`https://YOUR-RENDER-URL/voices/${voiceId}`, {
  method: "DELETE"
});

const data = await response.json();
console.log(data.message);
```

---

## ⚠️ Important Notes

### Render Free Tier Limitations

1. **Sleep after inactivity**: Service sleeps after 15 minutes of no requests
   - First request after sleep takes 20-60 seconds to wake up
   - Subsequent requests are fast

2. **750 hours/month**: Free tier gives you 750 hours
   - Enough for most projects
   - Service auto-sleeps when not in use

3. **No persistent disk**: Files uploaded to Render are lost on restart
   - That's why we use Supabase for voice storage! ✅

### Supabase Free Tier

- **500 MB storage**: Plenty for voice files
- **Unlimited API requests**
- **No credit card required**

---

## 🔧 Troubleshooting

### Build Fails on Render

**Issue**: PyTorch installation timeout

**Solution**: Render free tier has limited build time. If PyTorch fails:
1. Use CPU-only PyTorch in requirements.txt:
   ```
   torch==2.7.1+cpu
   torchaudio==2.7.1+cpu
   ```
2. Or upgrade to Render paid tier ($7/month)

### API Returns 500 Error

**Check**:
1. Render logs for errors
2. Verify environment variables are set correctly
3. Test `/health` endpoint first

### Voice Upload Fails

**Check**:
1. Supabase bucket is **public**
2. `SUPABASE_SERVICE_ROLE_KEY` is correct (not anon key)
3. File size < 50MB

---

## 📚 API Reference

### POST /upload-voice

Upload a voice file for cloning.

**Parameters**:
- `file` (required): Audio file
- `name` (optional): Voice name
- `gender` (optional): "male" or "female" (default: "male")
- `language` (optional): Language code (default: "en")

**Response**:
```json
{
  "id": "uuid",
  "name": "Voice Name",
  "url": "https://supabase.co/storage/.../voice.wav",
  "gender": "male",
  "language": "en",
  "filename": "uuid_male_en.wav"
}
```

### GET /voices

List all uploaded voices.

**Response**:
```json
{
  "voices": [
    {
      "id": "uuid",
      "name": "voice.wav",
      "url": "https://...",
      "gender": "male",
      "language": "en"
    }
  ],
  "count": 1
}
```

### POST /generate

Generate speech from text.

**Parameters**:
- `text` (required): Text to synthesize
- `voice_url` (optional): URL of voice file
- `model_type` (optional): "turbo" or "standard" (default: "turbo")

**Response**: WAV audio file (binary)

### DELETE /voices/{voice_id}

Delete a voice by ID.

**Response**:
```json
{
  "success": true,
  "message": "Deleted 1 file(s)",
  "deleted_files": ["uuid_male_en.wav"]
}
```

---

## 🎉 Next Steps

Once your API is deployed:

1. ✅ Test all endpoints using `/docs`
2. ✅ Integrate with your website/app
3. ✅ Add authentication if needed (API keys)
4. ✅ Monitor usage in Render dashboard
5. ✅ Scale up if you need more resources

---

## 💡 Tips

- **Keep service awake**: Use a service like [UptimeRobot](https://uptimerobot.com) to ping your API every 5 minutes
- **Add rate limiting**: Use FastAPI middleware to prevent abuse
- **Add API keys**: Protect your endpoints with authentication
- **Monitor costs**: Both Render and Supabase have free tiers, but monitor usage

---

## 📞 Support

If you encounter issues:
1. Check Render logs
2. Check Supabase logs
3. Test locally first: `uvicorn api:app --reload`
4. Verify environment variables are set

---

**Created by**: The Oracle Guy  
**Project**: Chatterbox TTS Enhanced  
**License**: MIT
