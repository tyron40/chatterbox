#!/usr/bin/env python3
"""
Example Workflow: Generate TTS + Mix with Cinematic Music
Complete end-to-end example of creating motivational audio
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.generation_functions import generate_turbo_speech
from modules.audio_mixer import mix_audio_with_music, check_ffmpeg, get_available_moods

def create_motivational_audio(text, voice, mood="epic", music_volume=0.15):
    """
    Complete workflow: Generate TTS and mix with cinematic music.
    
    Args:
        text: Text to convert to speech
        voice: Voice name (e.g., "Morgan Freeman_male")
        mood: Music mood (epic, emotional, uplifting)
        music_volume: Background music volume (0.0-1.0)
    
    Returns:
        Path to final mixed audio file
    """
    print("=" * 70)
    print("  🎬 CINEMATIC MOTIVATIONAL AUDIO CREATOR")
    print("=" * 70)
    print()
    
    # Check prerequisites
    print("Checking system...")
    if not check_ffmpeg():
        print("❌ FFmpeg not found! Please install FFmpeg first.")
        print("   Run: winget install FFmpeg")
        return None
    
    moods = get_available_moods()
    mood_tracks = next((m['tracks'] for m in moods if m['name'] == mood), 0)
    if mood_tracks == 0:
        print(f"❌ No music files found for mood: {mood}")
        print(f"   Please add music files to: music/{mood}/")
        print("   Run: python download_sample_music.py")
        return None
    
    print(f"✅ FFmpeg ready")
    print(f"✅ Music library: {mood_tracks} {mood} tracks")
    print()
    
    # Step 1: Generate TTS
    print("=" * 70)
    print("  STEP 1: Generating Speech")
    print("=" * 70)
    print(f"Text: {text[:100]}...")
    print(f"Voice: {voice}")
    print()
    
    audio_path = None
    try:
        for progress, path, status in generate_turbo_speech(text, voice):
            if path:
                audio_path = path
                print(f"✅ Speech generated: {os.path.basename(path)}")
                break
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        return None
    
    if not audio_path:
        print("❌ Failed to generate speech")
        return None
    
    print()
    
    # Step 2: Mix with music
    print("=" * 70)
    print("  STEP 2: Mixing with Cinematic Music")
    print("=" * 70)
    print(f"Mood: {mood}")
    print(f"Music Volume: {music_volume * 100}%")
    print(f"Ducking: Enabled")
    print()
    
    try:
        final_audio = mix_audio_with_music(
            voice_path=audio_path,
            mood=mood,
            music_volume=music_volume,
            enable_ducking=True
        )
        
        if final_audio:
            print()
            print("=" * 70)
            print("  ✅ SUCCESS!")
            print("=" * 70)
            print(f"📁 Final Audio: {final_audio}")
            print()
            print("🎬 Your cinematic motivational audio is ready!")
            print("   Perfect for YouTube, podcasts, social media!")
            print("=" * 70)
            return final_audio
        else:
            print("❌ Failed to mix audio")
            return None
            
    except Exception as e:
        print(f"❌ Error mixing audio: {e}")
        return None


def main():
    """Run example workflows."""
    print()
    print("🎬 CINEMATIC AUDIO MIXER - EXAMPLE WORKFLOWS")
    print()
    
    # Example 1: Epic motivational speech
    print("Example 1: Epic Motivational Speech")
    print("-" * 70)
    
    text1 = """
    You are stronger than you think. Every challenge you face is an opportunity 
    to grow. Don't let fear hold you back. Believe in yourself, take action, 
    and watch as you achieve things you never thought possible. Your potential 
    is unlimited. Now go out there and make it happen!
    """
    
    result1 = create_motivational_audio(
        text=text1.strip(),
        voice="Morgan Freeman_male",
        mood="epic",
        music_volume=0.15
    )
    
    if result1:
        print(f"\n✅ Example 1 complete: {result1}\n")
    
    # Example 2: Emotional inspiration
    print("\n" + "=" * 70)
    print("Example 2: Emotional Inspiration")
    print("-" * 70)
    
    text2 = """
    Sometimes the journey is hard. Sometimes you feel like giving up. 
    But remember why you started. Remember the dreams that keep you going. 
    You've come so far already. Don't stop now. Keep pushing forward, 
    one step at a time. You've got this.
    """
    
    result2 = create_motivational_audio(
        text=text2.strip(),
        voice="Morgan Freeman_male",
        mood="emotional",
        music_volume=0.12
    )
    
    if result2:
        print(f"\n✅ Example 2 complete: {result2}\n")
    
    # Summary
    print("\n" + "=" * 70)
    print("  📊 WORKFLOW COMPLETE")
    print("=" * 70)
    
    if result1 or result2:
        print("\n✅ Successfully created cinematic motivational audio!")
        print("\n📁 Check the 'output' folder for your files")
        print("\n🎬 Ready to upload to YouTube, podcasts, or social media!")
    else:
        print("\n⚠️ Some workflows failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("  1. Ensure FFmpeg is installed: ffmpeg -version")
        print("  2. Add music files to music/[mood]/ folders")
        print("  3. Run: python test_audio_mixer.py")
    
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
