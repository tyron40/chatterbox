# 🚀 Render Manual Deployment Guide

## Issue
Render is still using the old configuration with `port 10000` instead of the updated `$PORT` variable from commit 74e0547.

## Solution: Trigger Manual Deployment

### Step 1: Access Render Dashboard
1. Go to https://dashboard.render.com
2. Log in to your account
3. Find your service (likely named "chatterbox-api" or similar)

### Step 2: Clear Deploy Cache (Recommended)
1. Click on your service
2. Go to **Settings** tab
3. Scroll down to **Build & Deploy** section
4. Click **"Clear build cache & deploy"**
   - This ensures Render uses the latest code without any cached files

### Step 3: Manual Deploy (Alternative)
If you don't want to clear cache:
1. Click on your service
2. Click the **"Manual Deploy"** button in the top right
3. Select **"Deploy latest commit"**
4. Click **"Deploy"**

### Step 4: Monitor Deployment
1. Go to the **"Logs"** tab
2. Watch for these key indicators:

**✅ Success Indicators:**
```
==> Running 'uvicorn api:app --host 0.0.0.0 --port $PORT'
INFO: Uvicorn running on http://0.0.0.0:XXXXX
INFO: Application startup complete
```

**❌ Failure Indicators:**
```
==> Running 'uvicorn api:app --host 0.0.0.0 --port 10000'  ← OLD CONFIG
==> No open ports detected
==> Timed Out
```

### Step 5: Verify Deployment
Once deployment succeeds, test the endpoints:

```bash
# Replace YOUR_APP_URL with your actual Render URL
curl https://YOUR_APP_URL.onrender.com/health

# Expected response:
# {"ok":true,"supabase_connected":false,"device":"cpu"}
# (supabase_connected will be true after you add credentials)
```

## Why This Happened

Render sometimes caches the `render.yaml` configuration. Even though we pushed the fix (commit 74e0547), Render may still be using a cached version of the file.

**Clearing the build cache** forces Render to:
1. Re-read the `render.yaml` from GitHub
2. Rebuild from scratch
3. Use the correct `$PORT` variable

## What Changed

### Before (Commit 1170468 and earlier):
```yaml
startCommand: uvicorn api:app --host 0.0.0.0 --port 10000
```
❌ **Problem**: Hardcoded port doesn't match Render's dynamic port assignment

### After (Commit 74e0547):
```yaml
startCommand: uvicorn api:app --host 0.0.0.0 --port $PORT
```
✅ **Solution**: Uses Render's `$PORT` environment variable

## Expected Timeline

After triggering manual deployment:
- **Build**: ~10-15 minutes (installing dependencies)
- **Deployment**: ~2-3 minutes (starting service)
- **Total**: ~15-20 minutes

## Troubleshooting

### If deployment still fails with "No open ports detected":

1. **Check the logs** - Verify it's using `$PORT` not `10000`
2. **Check GitHub** - Confirm render.yaml has `$PORT`:
   ```bash
   curl https://raw.githubusercontent.com/tyron40/chatterbox/master/render.yaml
   ```
3. **Force rebuild** - Delete and recreate the service (last resort)

### If you see "port 10000" in logs:

This means Render is still using cached config. Solutions:
1. Clear build cache (recommended)
2. Wait 5-10 minutes and try again
3. Contact Render support

## Next Steps After Successful Deployment

1. **Add Supabase Credentials**:
   - Go to Environment tab in Render
   - Add `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`
   - Save (triggers automatic redeploy)

2. **Test All Endpoints**:
   ```bash
   # Health check
   curl https://YOUR_APP.onrender.com/health
   
   # API docs
   https://YOUR_APP.onrender.com/docs
   
   # Upload voice
   curl -X POST https://YOUR_APP.onrender.com/upload-voice \
     -F "file=@voice.wav" \
     -F "name=TestVoice"
   ```

## Summary

✅ **Code is correct** - GitHub has the right configuration
✅ **Commit is pushed** - 74e0547 is on master branch
⚠️ **Render needs manual trigger** - Clear cache and redeploy

---

**Last Updated**: 2026-02-01
**Fix Commit**: 74e0547
**Action Required**: Manual deployment in Render dashboard
