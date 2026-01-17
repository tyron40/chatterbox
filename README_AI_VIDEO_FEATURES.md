# 🤖 AI Text Generation & Video Creation Features

## Overview

The Batch TTS tab now includes powerful AI-driven features:
- **AI Text Generation** using OpenAI API
- **Automatic Video Creation** using Pixabay API
- Create motivational videos with narrated audio

## Features

### 1. AI Text Generation
- Generate unique motivational quotes and messages
- Powered by OpenAI's GPT-3.5-turbo
- Customizable prompt templates
- Generate text for each of the 50 fields individually

### 2. Video Creation
- Automatically fetch high-quality videos from Pixabay
- Combine videos with generated audio narration
- Customizable video duration (10-60 seconds)
- Search for specific video themes (motivation, success, inspiration, etc.)

## Setup

### Prerequisites

1. **OpenAI API Key** (for AI text generation)
   - Sign up at https://platform.openai.com/
   - Get your API key from https://platform.openai.com/api-keys
   - Pricing: ~$0.002 per 1K tokens (very affordable)

2. **Pixabay API Key** (for video creation)
   - Sign up at https://pixabay.com/accounts/register/
   - Get free API key at https://pixabay.com/api/docs/
   - Free tier: 5,000 requests per month

3. **FFmpeg** (for video processing)
   - Already included if you set up Cinematic Mixer
   - Or run: `install_ffmpeg.bat` (Windows)
   - Or install manually from https://ffmpeg.org/

## How to Use

### Step 1: Enter API Keys

1. Navigate to the **Batch TTS** tab
2. Expand the **"🔑 API Keys Configuration"** section
3. Enter your OpenAI API key (starts with `sk-...`)
4. Enter your Pixabay API key
5. (Optional) Customize the AI prompt template

### Step 2: Generate Text with AI

**Option A: Generate Individual Texts**
1. Click the **"🤖 AI Generate"** button next to any text field
2. The AI will generate unique motivational content
3. Edit the generated text if needed

**Option B: Manual Entry**
- Simply type your text in any field
- Leave empty fields to skip them

### Step 3: Configure Video Settings

1. Expand **"🎥 Video Creation Settings"**
2. Check **"Create videos for each audio"** (enabled by default)
3. Customize:
   - **Video Search Query**: Keywords for Pixabay search (e.g., "motivation success inspiration")
   - **Target Video Duration**: 10-60 seconds (default: 30s)

### Step 4: Generate Audio & Videos

1. Select voice mode (same voice for all or individual)
2. Choose your voice
3. Click **"🎬 Generate All Audio Files & Videos"**
4. Wait for processing:
   - Audio files generate first
   - Videos are created automatically after
   - Progress bar shows current status

### Step 5: Download Results

- Download individual audio/video files
- Or click **"📦 Download All as ZIP"** for batch download

## Example Workflow

### Creating Motivational Video Series

```
1. Enter API Keys:
   - OpenAI: sk-xxxxxxxxxxxxx
   - Pixabay: xxxxxxxxxxxxx

2. Set Prompt Template:
   "Generate a powerful motivational quote about success and perseverance (max 2-3 sentences)"

3. Generate Texts:
   - Click "AI Generate" for fields 1-10
   - Each gets a unique motivational quote

4. Configure Video:
   - Search Query: "success motivation business"
   - Duration: 30 seconds

5. Generate:
   - Click "Generate All Audio Files & Videos"
   - Wait for completion

6. Result:
   - 10 unique motivational videos
   - Each with AI-generated narration
   - Professional background footage
   - Ready to post on social media!
```

## Tips & Best Practices

### AI Text Generation
- **Be Specific**: Customize the prompt template for your needs
- **Vary Content**: Each field gets a variation number for uniqueness
- **Review & Edit**: Always review AI-generated content before using
- **Cost Effective**: ~$0.01 for 50 generations

### Video Creation
- **Search Keywords**: Use specific, relevant keywords
  - Good: "business success motivation entrepreneur"
  - Bad: "video"
- **Video Duration**: Match your audio length
  - Short quotes: 15-20 seconds
  - Longer content: 30-45 seconds
- **Quality**: Pixabay provides HD videos automatically

### Performance
- **Batch Size**: Start with 5-10 videos to test
- **Processing Time**: 
  - Audio: ~5-10 seconds per file
  - Video: ~30-60 seconds per file
- **Storage**: Videos are ~5-15MB each

## Troubleshooting

### "Invalid OpenAI API key"
- Ensure key starts with `sk-`
- Check key is active at https://platform.openai.com/api-keys
- Verify you have credits/billing set up

### "No videos found on Pixabay"
- Check your Pixabay API key is valid
- Try different search keywords
- Ensure you haven't exceeded free tier limit (5,000/month)

### "FFmpeg is not installed"
- Run `install_ffmpeg.bat` (Windows)
- Or install from https://ffmpeg.org/
- Restart the application after installation

### Videos not creating
- Check FFmpeg is installed: `ffmpeg -version`
- Ensure audio files generated successfully first
- Check Pixabay API key and search query
- Try simpler search terms

## API Costs

### OpenAI (GPT-3.5-turbo)
- **Cost**: ~$0.002 per 1K tokens
- **50 Generations**: ~$0.01-0.02
- **Monthly Budget**: $5 = ~25,000 generations

### Pixabay
- **Free Tier**: 5,000 requests/month
- **Cost**: $0 (completely free)
- **Limits**: No attribution required

## Advanced Usage

### Custom Prompts

```python
# Motivational Quotes
"Generate a motivational quote about {topic} (max 2 sentences)"

# Story Narration
"Write a short inspirational story about overcoming challenges (3-4 sentences)"

# Product Descriptions
"Create an engaging product description for {product} highlighting its benefits"

# Educational Content
"Explain {concept} in simple terms for beginners (2-3 sentences)"
```

### Video Themes

```
Motivation: "motivation success inspiration achievement"
Business: "business entrepreneur office meeting"
Nature: "nature landscape peaceful calm"
Technology: "technology innovation future digital"
Fitness: "fitness workout exercise gym"
Travel: "travel adventure explore world"
```

## Support

For issues or questions:
1. Check this README
2. Review error messages in the Status box
3. Check console/terminal for detailed logs
4. Ensure all prerequisites are installed

## Credits

- **OpenAI**: AI text generation
- **Pixabay**: Free stock videos
- **FFmpeg**: Video processing
- **Chatterbox TTS**: Voice synthesis
