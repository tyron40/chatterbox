# Supabase Setup Guide for Chatterbox TTS API

This guide will help you set up Supabase storage for your Chatterbox TTS API deployment on Render.

## Step 1: Create a Supabase Account

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub (recommended) or email
4. Verify your email if required

## Step 2: Create a New Project

1. Click "New Project"
2. Fill in the details:
   - **Name**: `chatterbox-tts` (or any name you prefer)
   - **Database Password**: Generate a strong password (save it somewhere safe)
   - **Region**: Choose the closest region to your Render deployment (e.g., US West for Oregon)
   - **Pricing Plan**: Select "Free" (includes 500MB storage)
3. Click "Create new project"
4. Wait 1-2 minutes for the project to be provisioned

## Step 3: Get Your API Credentials

1. In your Supabase project dashboard, click on the **Settings** icon (⚙️) in the left sidebar
2. Click on **API** in the settings menu
3. You'll see two important values:
   - **Project URL**: Copy this (looks like `https://xxxxxxxxxxxxx.supabase.co`)
   - **service_role key**: Click "Reveal" and copy this key (starts with `eyJ...`)

**⚠️ IMPORTANT**: Keep these credentials secure! The service_role key has full access to your database.

## Step 4: Create a Storage Bucket

1. In the left sidebar, click on **Storage**
2. Click "Create a new bucket"
3. Fill in the details:
   - **Name**: `voices` (must be exactly this name)
   - **Public bucket**: Toggle **ON** (so generated audio can be accessed via URL)
   - **File size limit**: Leave default or set to 10MB
   - **Allowed MIME types**: Leave empty (allows all file types)
4. Click "Create bucket"

## Step 5: Configure Bucket Policies

1. Click on the `voices` bucket you just created
2. Click on **Policies** tab
3. Click "New Policy"
4. Select "For full customization" → "Create policy"
5. Fill in:
   - **Policy name**: `Public Access`
   - **Allowed operation**: SELECT
   - **Target roles**: `public`
   - **USING expression**: `true`
6. Click "Review" → "Save policy"

This allows anyone to read/download files from the bucket (needed for audio playback).

## Step 6: Add Credentials to Render

Now that you have your Supabase credentials, you need to add them to your Render deployment:

1. Go to your Render dashboard
2. Find your `chatterbox-api` service
3. Click on "Environment" in the left sidebar
4. Add the following environment variables:
   - **Key**: `SUPABASE_URL`
     - **Value**: Your Project URL from Step 3
   - **Key**: `SUPABASE_SERVICE_ROLE_KEY`
     - **Value**: Your service_role key from Step 3
   - **Key**: `SUPABASE_BUCKET`
     - **Value**: `voices`
5. Click "Save Changes"

Your service will automatically redeploy with the new environment variables.

## Step 7: Verify Setup

Once your Render service is deployed, test the API:

```bash
# Check if API is running
curl https://your-app.onrender.com/

# Upload a test voice
curl -X POST https://your-app.onrender.com/voices/upload \
  -F "file=@path/to/audio.wav" \
  -F "voice_name=test_voice"

# List voices
curl https://your-app.onrender.com/voices/list
```

## Troubleshooting

### "Bucket not found" error
- Make sure the bucket name is exactly `voices`
- Check that the bucket was created successfully in Supabase Storage

### "Unauthorized" error
- Verify your SUPABASE_SERVICE_ROLE_KEY is correct
- Make sure you copied the **service_role** key, not the **anon** key

### Files not accessible
- Check that your bucket is set to **Public**
- Verify the bucket policy allows SELECT for public role

### Storage limit exceeded
- Free tier includes 500MB storage
- Delete old voice files or upgrade to Pro plan

## Next Steps

Once Supabase is set up and your Render service is deployed:

1. Test voice upload via the API
2. Generate speech using uploaded voices
3. Share your API URL with others
4. Monitor usage in Supabase dashboard

## API Endpoints

Your deployed API will have these endpoints:

- `GET /` - API status and documentation
- `POST /voices/upload` - Upload a voice sample
- `GET /voices/list` - List all uploaded voices
- `POST /generate` - Generate speech from text
- `DELETE /voices/{voice_name}` - Delete a voice

For detailed API documentation, visit your deployed API URL.
