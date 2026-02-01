# Quick Setup for AI Text Generation

## Step 1: Install Required Packages

Run this command in your terminal:

```bash
pip install -r requirements.txt
```

This will install:
- `openai` - OpenAI API client
- `python-dotenv` - For loading environment variables from .env file
- All other required packages

## Step 2: API Key Setup

✅ **Your API key is already configured!**

The `.env` file has been created with your OpenAI API key. The application will automatically load it when you run it.

**Security Note:** The `.env` file is in `.gitignore` to prevent accidentally sharing your API key.

## Step 3: Run the Application

```bash
python app.py
```

## How to Use

1. Go to the **"📦 Batch Generation"** tab
2. Expand **"🤖 AI Text Generation"** section
3. Enter:
   - **Topic:** "motivational speeches"
   - **Duration:** 8 (minutes)
   - **Number of Texts:** 10
4. Click **"🤖 Generate All Texts with AI"**
5. Wait for texts to generate
6. Select a voice
7. Click **"🎵 Generate All Audio Files"**

## Features

- **Generate All:** Fill multiple fields at once
- **Individual Generate:** Click 🤖 button next to any field
- **Duration-based:** AI generates text to match your desired audio length
- **Unique Content:** Each field gets completely different content

## Example

**Topic:** "motivational speeches about overcoming challenges"
**Duration:** 8 minutes
**Result:** 100 unique 8-minute motivational speeches!

Enjoy! 🎉
