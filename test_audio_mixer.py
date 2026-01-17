#!/usr/bin/env python3
"""
Audio Mixer Test Script
Tests the cinematic audio mixing system
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.audio_mixer import (
    check_ffmpeg,
    get_music_files,
    get_available_moods,
    print_system_info,
    MUSIC_DIR,
    OUTPUT_DIR
)


def test_ffmpeg():
    """Test FFmpeg installation."""
    print("\n" + "="*60)
    print("TEST 1: FFmpeg Installation")
    print("="*60)
    
    if check_ffmpeg():
        print("✅ PASS: FFmpeg is installed and accessible")
        return True
    else:
        print("❌ FAIL: FFmpeg not found")
        print("\n📥 Installation required:")
        print("   winget install FFmpeg")
        print("   OR download from: https://ffmpeg.org/download.html")
        return False


def test_directories():
    """Test directory structure."""
    print("\n" + "="*60)
    print("TEST 2: Directory Structure")
    print("="*60)
    
    required_dirs = [
        MUSIC_DIR,
        OUTPUT_DIR,
        os.path.join(MUSIC_DIR, "epic"),
        os.path.join(MUSIC_DIR, "emotional"),
        os.path.join(MUSIC_DIR, "uplifting")
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        exists = os.path.exists(dir_path)
        status = "✅" if exists else "❌"
        print(f"{status} {dir_path}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✅ PASS: All directories exist")
        return True
    else:
        print("\n❌ FAIL: Some directories missing")
        print("Run: python -c \"from modules.audio_mixer import *\"")
        return False


def test_music_files():
    """Test music file availability."""
    print("\n" + "="*60)
    print("TEST 3: Music Files")
    print("="*60)
    
    moods = get_available_moods()
    total_tracks = sum(m["tracks"] for m in moods)
    
    for mood_info in moods:
        mood = mood_info["name"]
        count = mood_info["tracks"]
        status = "✅" if count > 0 else "⚠️"
        print(f"{status} {mood.capitalize()}: {count} tracks")
        
        if count > 0:
            files = get_music_files(mood)
            for f in files[:3]:  # Show first 3
                print(f"   - {os.path.basename(f)}")
            if count > 3:
                print(f"   ... and {count - 3} more")
    
    if total_tracks > 0:
        print(f"\n✅ PASS: {total_tracks} music tracks available")
        return True
    else:
        print("\n⚠️ WARNING: No music files found")
        print("\n📥 Download royalty-free music:")
        print("   1. Pixabay: https://pixabay.com/music/")
        print("   2. Mixkit: https://mixkit.co/free-stock-music/")
        print("   3. FreePD: https://freepd.com/")
        print(f"\n📁 Place files in: {MUSIC_DIR}/[mood]/")
        return False


def test_sample_generation():
    """Test sample audio generation."""
    print("\n" + "="*60)
    print("TEST 4: Sample Audio Generation")
    print("="*60)
    
    try:
        import numpy as np
        from scipy.io import wavfile
        
        # Generate 3-second test tone
        sample_rate = 24000
        duration = 3
        frequency = 440  # A4 note
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        audio = (audio * 32767).astype(np.int16)
        
        test_file = os.path.join(OUTPUT_DIR, "test_voice.wav")
        wavfile.write(test_file, sample_rate, audio)
        
        if os.path.exists(test_file):
            print(f"✅ PASS: Test audio created")
            print(f"📁 {test_file}")
            return test_file
        else:
            print("❌ FAIL: Could not create test audio")
            return None
            
    except ImportError:
        print("⚠️ SKIP: scipy not available (optional)")
        print("   Install with: pip install scipy")
        return None
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return None


def test_mixing(test_voice_file=None):
    """Test audio mixing."""
    print("\n" + "="*60)
    print("TEST 5: Audio Mixing")
    print("="*60)
    
    if not check_ffmpeg():
        print("⚠️ SKIP: FFmpeg not available")
        return False
    
    moods = get_available_moods()
    if not any(m["tracks"] > 0 for m in moods):
        print("⚠️ SKIP: No music files available")
        return False
    
    if test_voice_file is None or not os.path.exists(test_voice_file):
        print("⚠️ SKIP: No test voice file available")
        return False
    
    try:
        from modules.audio_mixer import mix_audio_with_music
        
        # Find a mood with music
        test_mood = next((m["name"] for m in moods if m["tracks"] > 0), None)
        
        if test_mood:
            print(f"🎬 Testing mix with {test_mood} music...")
            
            output = mix_audio_with_music(
                voice_path=test_voice_file,
                mood=test_mood,
                music_volume=0.15,
                enable_ducking=True
            )
            
            if output and os.path.exists(output):
                file_size = os.path.getsize(output) / 1024  # KB
                print(f"\n✅ PASS: Audio mixed successfully")
                print(f"📁 Output: {output}")
                print(f"📊 Size: {file_size:.1f} KB")
                return True
            else:
                print("\n❌ FAIL: Mixing failed")
                return False
        else:
            print("⚠️ SKIP: No music available for testing")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("🎬 CINEMATIC AUDIO MIXER - TEST SUITE")
    print("="*60)
    
    results = {
        "FFmpeg": test_ffmpeg(),
        "Directories": test_directories(),
        "Music Files": test_music_files(),
    }
    
    # Optional tests
    test_voice = test_sample_generation()
    if test_voice:
        results["Audio Mixing"] = test_mixing(test_voice)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("System is ready to create cinematic motivational audio!")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("Please review the failures above and follow the setup guide.")
    
    print("\n📖 For detailed setup instructions, see: AUDIO_MIXER_SETUP.md")
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
