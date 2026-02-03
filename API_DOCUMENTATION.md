# Chatterbox TTS Enhanced API Documentation

## Overview

Complete voice cloning, text-to-speech, voice conversion & multilingual TTS API with 30+ default voices and 23 language support.

**Base URL**: `https://chatterbox-api-99gk.onrender.com`  
**Version**: 2.0.0

---

## 🎯 Features

- ✅ **30+ Default Celebrity & Character Voices** (Morgan Freeman, Elon Musk, Trump, etc.)
- ✅ **Voice Cloning & Upload** (Custom voice support)
- ✅ **23 Language Support** (Arabic, Chinese, Spanish, French, Hindi, etc.)
- ✅ **Voice Conversion** (Voice-to-Voice translation)
- ✅ **Turbo TTS** (3x faster generation)
- ✅ **Paralinguistic Tags** ([laugh], [sigh], [gasp], etc.)

---

## 📚 Endpoints

### 1. Health Check

**GET** `/health`

Check API status and configuration.

**Response:**
```json
{
  "ok": true,
  "supabase_connected": false,
  "device": "cpu",
  "version": "2.0.0"
}
```

---

### 2. Get Default Voices

**GET** `/default-voices`

Get all 30+ default voices available in the system.

**Response:**
```json
{
  "voices": [
    {
      "id": "Morgan Freeman_male",
      "name": "Morgan Freeman",
      "display_name": "Morgan Freeman ♂️",
      "gender": "male",
      "language": "en",
      "is_default": true
    },
    {
      "id": "Elon Musk_male",
      "name": "Elon Musk",
      "display_name": "Elon Musk ♂️",
      "gender": "male",
      "language": "en",
      "is_default": true
    }
  ],
  "count": 30,
  "message": "Found 30 default voices"
}
```

**Available Default Voices:**
- **English**: Morgan Freeman, Elon Musk, Trump, DiCaprio, Matthew McConaughey, Liam Neeson, Jimmy Fallon, Paul, Rocky, Carissa, Laurel, Jessamyn West, Tyron
- **Hindi**: Abhishek, Avdhesh, Amitabh Bachchan, Deepika, Priyanka
- **German**: Angela Merkel
- **Chinese**: Jack Ma
- **French**: Kylian Mbappé
- **Spanish**: Rafael Nadal

---

### 3. List All Voices

**GET** `/voices?include_defaults=true`

List all voices (default + uploaded).

**Parameters:**
- `include_defaults` (optional): Include default voices (default: true)

**Response:**
```json
{
  "voices": [...],
  "count": 35,
  "default_count": 30,
  "uploaded_count": 5
}
```

---

### 4. Upload Custom Voice

**POST** `/upload-voice`

Upload a custom voice file for cloning.

**Parameters:**
- `file` (required): Audio file (WAV, MP3, FLAC, M4A)
- `name` (optional): Voice name
- `gender` (optional): "male" or "female" (default: "male")
- `language` (optional): Language code (default: "en")

**Example (cURL):**
```bash
curl -X POST https://chatterbox-api-99gk.onrender.com/upload-voice \
  -F "file=@my_voice.wav" \
  -F "name=My Custom Voice" \
  -F "gender=male" \
  -F "language=en"
```

**Response:**
```json
{
  "id": "abc123-def456",
  "name": "My Custom Voice",
  "url": "https://...",
  "gender": "male",
  "language": "en",
  "filename": "abc123-def456_male_en.wav",
  "is_default": false
}
```

---

### 5. Delete Voice

**DELETE** `/voices/{voice_id}`

Delete an uploaded voice.

**Example:**
```bash
curl -X DELETE https://chatterbox-api-99gk.onrender.com/voices/abc123-def456
```

---

### 6. Get Supported Languages

**GET** `/languages`

Get list of all 23 supported languages.

**Response:**
```json
{
  "languages": [
    {"code": "en", "name": "English", "has_default_voice": false},
    {"code": "es", "name": "Spanish", "has_default_voice": true},
    {"code": "fr", "name": "French", "has_default_voice": true},
    {"code": "hi", "name": "Hindi", "has_default_voice": true},
    {"code": "zh", "name": "Chinese", "has_default_voice": true}
  ],
  "count": 23
}
```

**Supported Languages:**
Arabic (ar), Danish (da), German (de), Greek (el), English (en), Spanish (es), Finnish (fi), French (fr), Hebrew (he), Hindi (hi), Italian (it), Japanese (ja), Korean (ko), Malay (ms), Dutch (nl), Norwegian (no), Polish (pl), Portuguese (pt), Russian (ru), Swedish (sv), Swahili (sw), Turkish (tr), Chinese (zh)

---

## 🎤 Text-to-Speech Generation

### 7. Generate TTS (English)

**POST** `/generate/tts`

Generate English speech with full control over voice parameters.

**Parameters:**
- `text` (required): Text to convert to speech
- `voice_id` (optional): ID of default or uploaded voice
- `voice_url` (optional): URL of voice file
- `exaggeration` (optional): 0.0-1.0 (default: 0.5)
- `temperature` (optional): 0.0-2.0 (default: 0.8)
- `cfg_weight` (optional): 0.0-1.0 (default: 0.5)
- `min_p` (optional): 0.0-1.0 (default: 0.05)
- `top_p` (optional): 0.0-1.0 (default: 1.0)
- `repetition_penalty` (optional): 1.0-2.0 (default: 1.2)
- `seed` (optional): Random seed (0 for random)

**Example (cURL):**
```bash
curl -X POST https://chatterbox-api-99gk.onrender.com/generate/tts \
  -F "text=Hello, this is a test of the text to speech system." \
  -F "voice_id=Morgan Freeman_male" \
  -F "temperature=0.8" \
  --output output.wav
```

**Example (Python):**
```python
import requests

response = requests.post(
    "https://chatterbox-api-99gk.onrender.com/generate/tts",
    data={
        "text": "Hello, this is Morgan Freeman speaking.",
        "voice_id": "Morgan Freeman_male",
        "temperature": 0.8,
        "exaggeration": 0.5
    }
)

with open("output.wav", "wb") as f:
    f.write(response.content)
```

**Response:** Audio file (WAV format)

---

### 8. Generate Multilingual TTS

**POST** `/generate/multilingual`

Generate speech in any of 23 supported languages.

**Parameters:**
- `text` (required): Text to convert to speech
- `language` (required): Language code (ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh)
- `voice_id` (optional): ID of voice
- `voice_url` (optional): URL of voice file
- `exaggeration` (optional): 0.0-1.0 (default: 0.5)
- `temperature` (optional): 0.0-2.0 (default: 0.8)
- `cfg_weight` (optional): 0.0-1.0 (default: 0.5)
- `seed` (optional): Random seed

**Example (Spanish):**
```bash
curl -X POST https://chatterbox-api-99gk.onrender.com/generate/multilingual \
  -F "text=Hola, ¿cómo estás?" \
  -F "language=es" \
  -F "voice_id=Rafael Nadal_male_es" \
  --output spanish.wav
```

**Example (Hindi):**
```bash
curl -X POST https://chatterbox-api-99gk.onrender.com/generate/multilingual \
  -F "text=नमस्ते, आप कैसे हैं?" \
  -F "language=hi" \
  -F "voice_id=Priyanka_female_hi" \
  --output hindi.wav
```

**Response:** Audio file (WAV format)

---

### 9. Generate Turbo TTS

**POST** `/generate/turbo`

Generate speech 3x faster with paralinguistic tag support.

**Parameters:**
- `text` (required): Text with optional tags ([laugh], [sigh], [gasp], etc.)
- `voice_id` (required): ID of voice (REQUIRED for Turbo)
- `voice_url` (optional): URL of voice file

**Supported Tags:**
- `[laugh]` - Laughter
- `[chuckle]` - Light laugh
- `[sigh]` - Sighing
- `[gasp]` - Gasping
- `[cough]` - Coughing
- `[sniff]` - Sniffing
- `[clear_throat]` - Throat clearing
- `[groan]` - Groaning
- `[shush]` - Shushing

**Example:**
```bash
curl -X POST https://chatterbox-api-99gk.onrender.com/generate/turbo \
  -F "text=Well [sigh], that was unexpected [chuckle]. I can't believe it!" \
  -F "voice_id=Trump_male" \
  --output turbo.wav
```

**Python Example:**
```python
import requests

response = requests.post(
    "https://chatterbox-api-99gk.onrender.com/generate/turbo",
    data={
        "text": "Hello there [laugh]! This is amazing [gasp]!",
        "voice_id": "Elon Musk_male"
    }
)

with open("turbo_output.wav", "wb") as f:
    f.write(response.content)
```

**Response:** Audio file (WAV format)

---

## 🔄 Voice Conversion

### 10. Convert Voice (Voice Translator)

**POST** `/convert-voice`

Convert any voice to sound like a target voice.

**Parameters:**
- `input_audio` (required): Source audio file to convert
- `target_voice_id` (optional): ID of target voice
- `target_voice_url` (optional): URL of target voice file

**Example:**
```bash
curl -X POST https://chatterbox-api-99gk.onrender.com/convert-voice \
  -F "input_audio=@my_recording.wav" \
  -F "target_voice_id=Morgan Freeman_male" \
  --output converted.wav
```

**Python Example:**
```python
import requests

with open("my_voice.wav", "rb") as f:
    response = requests.post(
        "https://chatterbox-api-99gk.onrender.com/convert-voice",
        files={"input_audio": f},
        data={"target_voice_id": "Trump_male"}
    )

with open("converted_voice.wav", "wb") as f:
    f.write(response.content)
```

**Response:** Converted audio file (WAV format)

---

## 📝 Usage Examples

### Complete Workflow Example

```python
import requests

API_URL = "https://chatterbox-api-99gk.onrender.com"

# 1. Get available default voices
voices = requests.get(f"{API_URL}/default-voices").json()
print(f"Available voices: {voices['count']}")

# 2. Generate speech with Morgan Freeman's voice
response = requests.post(
    f"{API_URL}/generate/tts",
    data={
        "text": "I can explain the universe to you, one voice at a time.",
        "voice_id": "Morgan Freeman_male",
        "temperature": 0.9
    }
)
with open("morgan_freeman.wav", "wb") as f:
    f.write(response.content)

# 3. Generate multilingual speech (Spanish)
response = requests.post(
    f"{API_URL}/generate/multilingual",
    data={
        "text": "La inteligencia artificial está cambiando el mundo.",
        "language": "es",
        "voice_id": "Rafael Nadal_male_es"
    }
)
with open("spanish.wav", "wb") as f:
    f.write(response.content)

# 4. Generate with Turbo (faster, with tags)
response = requests.post(
    f"{API_URL}/generate/turbo",
    data={
        "text": "This is incredible [gasp]! I love it [laugh]!",
        "voice_id": "Elon Musk_male"
    }
)
with open("turbo.wav", "wb") as f:
    f.write(response.content)

# 5. Convert your voice to sound like Trump
with open("my_recording.wav", "rb") as f:
    response = requests.post(
        f"{API_URL}/convert-voice",
        files={"input_audio": f},
        data={"target_voice_id": "Trump_male"}
    )
with open("trump_voice.wav", "wb") as f:
    f.write(response.content)

print("All done!")
```

---

## 🚀 Quick Start

### 1. Test the API
```bash
curl https://chatterbox-api-99gk.onrender.com/health
```

### 2. Get Available Voices
```bash
curl https://chatterbox-api-99gk.onrender.com/default-voices
```

### 3. Generate Your First Audio
```bash
curl -X POST https://chatterbox-api-99gk.onrender.com/generate/turbo \
  -F "text=Hello world!" \
  -F "voice_id=Morgan Freeman_male" \
  --output hello.wav
```

---

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (voice not found) |
| 500 | Server Error (model loading failed, etc.) |

---

## 💡 Tips & Best Practices

1. **Voice Selection**: Use `/default-voices` to see all available voices before generation
2. **Long Text**: API automatically chunks long text for better quality
3. **Turbo Model**: Requires a voice reference, but generates 3x faster
4. **Multilingual**: Each language has default voices, or upload your own
5. **Voice Conversion**: Works best with clear audio input (no background noise)
6. **Paralinguistic Tags**: Use sparingly for natural-sounding speech
7. **Temperature**: Higher values (0.9-1.0) = more expressive, Lower (0.5-0.7) = more consistent

---

## 🔗 Links

- **Live API**: https://chatterbox-api-99gk.onrender.com
- **Interactive Docs**: https://chatterbox-api-99gk.onrender.com/docs
- **GitHub**: https://github.com/tyron40/chatterbox

---

## 📞 Support

For issues or questions, please open an issue on GitHub or contact support.

**Version**: 2.0.0  
**Last Updated**: February 2026
