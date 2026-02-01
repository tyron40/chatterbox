# AI Text Generation Guide for Chatterbox TTS

## Overview
The Batch Generation tab now includes AI-powered text generation using OpenAI's GPT-4o-mini model. This feature allows you to automatically generate unique content for all 100 text fields based on a topic and desired audio duration.

## Setup

### 1. Install OpenAI Package
```bash
pip install openai>=1.0.0
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
Set your OpenAI API key as an environment variable:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Permanent Setup (Windows):**
1. Search for "Environment Variables" in Windows
2. Click "Environment Variables" button
3. Under "User variables", click "New"
4. Variable name: `OPENAI_API_KEY`
5. Variable value: Your OpenAI API key
6. Click OK

## How to Use

### Generate All Texts at Once

1. **Open the Batch Generation tab**
2. **Expand the "🤖 AI Text Generation" accordion**
3. **Enter a topic** (e.g., "motivational speeches", "product descriptions", "bedtime stories")
4. **Set duration per text:**
   - Enter a number (e.g., 8)
   - Select unit (minutes or seconds)
5. **Set number of texts** to generate (1-100)
6. **Click "🤖 Generate All Texts with AI"**
7. Wait for AI to generate unique content for each field
8. **Select a voice** and click "🎵 Generate All Audio Files"

### Generate Individual Text

1. **Enter a topic** in the AI Text Generation section
2. **Set duration** for the text
3. **Click the 🤖 button** next to any text field
4. That specific field will be filled with AI-generated content

## Features

### Duration-Based Text Generation
- **Calculation:** ~150 words per minute of speech
- **Example:** 8 minutes = ~1,200 words per text
- **Range:** 0.1 to 60 minutes (or equivalent in seconds)

### Unique Content
- Each of the 100 fields gets **completely different content**
- All content is based on the same topic
- High variation ensures no repetition

### Smart Text Generation
- Natural, conversational tone
- Suitable for text-to-speech
- No special formatting
- Engaging and well-structured

## Example Workflow

### Creating 100 Motivational Speeches (8 minutes each)

1. **AI Text Generation:**
   - Topic: "motivational speeches about overcoming challenges"
   - Duration: 8 minutes
   - Number of texts: 100
   - Click "🤖 Generate All Texts with AI"
   - Wait ~5-10 minutes for all texts to generate

2. **Audio Generation:**
   - Select voice: "Morgan Freeman ♂️"
   - Model: "⚡ Turbo"
   - Click "🎵 Generate All Audio Files"
   - Wait for all audio to generate

3. **Download:**
   - Individual files appear in each Audio field
   - Click "📦 Download All Audio Files" for a zip

## Cost Estimation

**OpenAI GPT-4o-mini Pricing (as of 2024):**
- Input: $0.150 per 1M tokens
- Output: $0.600 per 1M tokens

**Example Cost for 100 texts (8 minutes each):**
- ~1,200 words per text = ~1,600 tokens
- 100 texts = ~160,000 output tokens
- Cost: ~$0.10 USD

## Troubleshooting

### Error: "OPENAI_API_KEY environment variable not set"
- Make sure you've set the environment variable
- Restart your terminal/PowerShell after setting it
- Restart the application after setting the variable

### Error: "Rate limit exceeded"
- You're making too many requests too quickly
- Wait a few minutes and try again
- Consider reducing the number of texts to generate at once

### Generated text is too short/long
- Adjust the duration value
- The AI aims for ~150 words per minute
- Actual length may vary slightly

## Tips for Best Results

1. **Be specific with topics:**
   - Good: "motivational speeches about entrepreneurship for young adults"
   - Bad: "speeches"

2. **Use appropriate durations:**
   - Short content: 30 seconds - 2 minutes
   - Medium content: 2-5 minutes
   - Long content: 5-15 minutes

3. **Generate in batches:**
   - For 100 texts, consider generating 10-20 at a time
   - This helps avoid rate limits and allows you to review quality

4. **Review before audio generation:**
   - Check a few generated texts for quality
   - Regenerate individual fields if needed using the 🤖 button

## Advanced Usage

### Custom Prompts
The AI uses GPT-4o-mini with temperature=0.9 for high variation. Each text gets a unique variation number to ensure diversity.

### Integration with Voice Cloning
1. Clone multiple voices
2. Uncheck "Use same voice for all texts"
3. Assign different voices to different text fields
4. Generate audio with varied voices

Enjoy creating unlimited unique content with AI-powered batch generation!
