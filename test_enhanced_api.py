"""
Test script for Enhanced Chatterbox TTS API
Tests all new features: default voices, voice conversion, multilingual TTS
"""
import requests
import json

# API Base URL (change to deployed URL for production testing)
BASE_URL = "http://localhost:8000"
# BASE_URL = "https://chatterbox-api-99gk.onrender.com"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_health():
    """Test health endpoint"""
    print_section("1. Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get("ok"):
            print("✅ PASS: Health check successful")
            print(f"   - Version: {data.get('version')}")
            print(f"   - Device: {data.get('device')}")
            print(f"   - Supabase: {'Connected' if data.get('supabase_connected') else 'Not configured'}")
        else:
            print("❌ FAIL: Health check failed")
        return True
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

def test_default_voices():
    """Test default voices endpoint"""
    print_section("2. Testing Default Voices Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/default-voices", timeout=10)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        print(f"\n📊 Found {data.get('count', 0)} default voices:")
        print("-" * 70)
        
        # Group voices by language
        voices_by_lang = {}
        for voice in data.get("voices", []):
            lang = voice.get("language", "unknown")
            if lang not in voices_by_lang:
                voices_by_lang[lang] = []
            voices_by_lang[lang].append(voice)
        
        # Display voices grouped by language
        for lang, voices in sorted(voices_by_lang.items()):
            print(f"\n{lang.upper()} ({len(voices)} voices):")
            for voice in voices:
                gender_symbol = "♂️" if voice.get("gender") == "male" else "♀️" if voice.get("gender") == "female" else "❓"
                print(f"  {gender_symbol} {voice.get('name')} (ID: {voice.get('id')})")
        
        print(f"\n✅ PASS: Found {data.get('count')} default voices")
        return data.get("voices", [])
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return []

def test_list_all_voices():
    """Test list all voices endpoint"""
    print_section("3. Testing List All Voices Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/voices?include_defaults=true", timeout=10)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        print(f"\n📊 Voice Summary:")
        print(f"   - Total Voices: {data.get('count', 0)}")
        print(f"   - Default Voices: {data.get('default_count', 0)}")
        print(f"   - Uploaded Voices: {data.get('uploaded_count', 0)}")
        
        print(f"\n✅ PASS: Listed {data.get('count')} total voices")
        return True
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

def test_supported_languages():
    """Test supported languages endpoint"""
    print_section("4. Testing Supported Languages Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/languages", timeout=10)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        print(f"\n🌍 Supported Languages ({data.get('count', 0)}):")
        print("-" * 70)
        
        for lang in data.get("languages", []):
            has_voice = "✅" if lang.get("has_default_voice") else "❌"
            print(f"  {has_voice} {lang.get('code'):3s} - {lang.get('name')}")
        
        print(f"\n✅ PASS: Found {data.get('count')} supported languages")
        return data.get("languages", [])
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return []

def test_generate_tts(voices):
    """Test TTS generation with default voice"""
    print_section("5. Testing TTS Generation (English)")
    
    if not voices:
        print("⚠️  SKIP: No voices available")
        return False
    
    # Find Morgan Freeman voice
    morgan_voice = next((v for v in voices if "Morgan Freeman" in v.get("name", "")), None)
    if not morgan_voice:
        morgan_voice = voices[0]  # Use first available voice
    
    voice_id = morgan_voice.get("id")
    print(f"Using voice: {morgan_voice.get('display_name')} (ID: {voice_id})")
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate/tts",
            data={
                "text": "Hello, this is a test of the text to speech system.",
                "voice_id": voice_id,
                "temperature": 0.8
            },
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Save audio file
            filename = "test_tts_output.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ PASS: Generated audio file")
            print(f"   - File: {filename}")
            print(f"   - Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            return True
        else:
            print(f"❌ FAIL: Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

def test_generate_multilingual(languages):
    """Test multilingual TTS generation"""
    print_section("6. Testing Multilingual TTS Generation")
    
    # Test with Spanish
    spanish = next((l for l in languages if l.get("code") == "es"), None)
    if not spanish:
        print("⚠️  SKIP: Spanish not available")
        return False
    
    print(f"Testing language: {spanish.get('name')} ({spanish.get('code')})")
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate/multilingual",
            data={
                "text": "Hola, ¿cómo estás? Esta es una prueba del sistema de texto a voz.",
                "language": "es",
                "temperature": 0.8
            },
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filename = "test_multilingual_spanish.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ PASS: Generated multilingual audio")
            print(f"   - Language: Spanish")
            print(f"   - File: {filename}")
            print(f"   - Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            return True
        else:
            print(f"❌ FAIL: Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

def test_generate_turbo(voices):
    """Test Turbo TTS generation with paralinguistic tags"""
    print_section("7. Testing Turbo TTS Generation")
    
    if not voices:
        print("⚠️  SKIP: No voices available")
        return False
    
    # Find a suitable voice
    test_voice = next((v for v in voices if "Elon" in v.get("name", "")), voices[0])
    voice_id = test_voice.get("id")
    print(f"Using voice: {test_voice.get('display_name')} (ID: {voice_id})")
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate/turbo",
            data={
                "text": "Well [sigh], that was unexpected [chuckle]. I can't believe it [gasp]!",
                "voice_id": voice_id
            },
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filename = "test_turbo_output.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ PASS: Generated Turbo audio with paralinguistic tags")
            print(f"   - Tags used: [sigh], [chuckle], [gasp]")
            print(f"   - File: {filename}")
            print(f"   - Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            return True
        else:
            print(f"❌ FAIL: Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

def test_voice_conversion():
    """Test voice conversion (requires input audio file)"""
    print_section("8. Testing Voice Conversion (Voice Translator)")
    
    # Check if we have a test audio file
    import os
    test_files = ["test_tts_output.wav", "test_turbo_output.wav"]
    input_file = None
    
    for f in test_files:
        if os.path.exists(f):
            input_file = f
            break
    
    if not input_file:
        print("⚠️  SKIP: No input audio file available")
        print("   (Run TTS generation tests first to create test audio)")
        return False
    
    print(f"Using input file: {input_file}")
    print("Converting to Trump voice...")
    
    try:
        with open(input_file, "rb") as f:
            response = requests.post(
                f"{BASE_URL}/convert-voice",
                files={"input_audio": f},
                data={"target_voice_id": "Trump_male"},
                timeout=60
            )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            filename = "test_voice_converted.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ PASS: Voice conversion successful")
            print(f"   - Input: {input_file}")
            print(f"   - Target: Trump voice")
            print(f"   - Output: {filename}")
            print(f"   - Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            return True
        else:
            print(f"❌ FAIL: Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  CHATTERBOX TTS ENHANCED API - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"\nTesting API at: {BASE_URL}")
    print("=" * 70)
    
    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # Run tests
    voices = []
    languages = []
    
    # Test 1: Health
    if test_health():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 2: Default Voices
    voices = test_default_voices()
    if voices:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 3: List All Voices
    if test_list_all_voices():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 4: Supported Languages
    languages = test_supported_languages()
    if languages:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: TTS Generation
    if test_generate_tts(voices):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Multilingual TTS
    if test_generate_multilingual(languages):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 7: Turbo TTS
    if test_generate_turbo(voices):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 8: Voice Conversion
    if test_voice_conversion():
        results["passed"] += 1
    else:
        results["skipped"] += 1
    
    # Print summary
    print_section("TEST SUMMARY")
    total = results["passed"] + results["failed"] + results["skipped"]
    print(f"\n✅ Passed:  {results['passed']}/{total}")
    print(f"❌ Failed:  {results['failed']}/{total}")
    print(f"⚠️  Skipped: {results['skipped']}/{total}")
    
    if results["failed"] == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed")
    
    print("\n" + "=" * 70)
    print("  Generated Files:")
    print("=" * 70)
    import os
    test_files = [
        "test_tts_output.wav",
        "test_multilingual_spanish.wav",
        "test_turbo_output.wav",
        "test_voice_converted.wav"
    ]
    for f in test_files:
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"  ✅ {f} ({size:,} bytes)")
        else:
            print(f"  ❌ {f} (not created)")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
