#!/usr/bin/env python3
"""
Sample Music Download Helper
Provides links and instructions for downloading royalty-free music
"""
import os
import webbrowser

MUSIC_SOURCES = {
    "Pixabay": {
        "url": "https://pixabay.com/music/",
        "license": "Free for commercial use",
        "attribution": "Not required",
        "searches": {
            "epic": "epic cinematic",
            "emotional": "emotional piano",
            "uplifting": "uplifting motivation"
        }
    },
    "Mixkit": {
        "url": "https://mixkit.co/free-stock-music/",
        "license": "Free for commercial use",
        "attribution": "Not required",
        "searches": {
            "epic": "cinematic",
            "emotional": "ambient",
            "uplifting": "upbeat"
        }
    },
    "FreePD": {
        "url": "https://freepd.com/",
        "license": "Public Domain",
        "attribution": "Not required",
        "searches": {
            "epic": "orchestral",
            "emotional": "piano",
            "uplifting": "electronic"
        }
    }
}

def print_header():
    print("=" * 70)
    print("  🎵 ROYALTY-FREE MUSIC DOWNLOAD HELPER")
    print("=" * 70)
    print()

def print_source_info(name, info):
    print(f"📁 {name}")
    print(f"   URL: {info['url']}")
    print(f"   License: {info['license']}")
    print(f"   Attribution: {info['attribution']}")
    print()
    print("   Recommended Searches:")
    for mood, search in info['searches'].items():
        print(f"     • {mood.capitalize()}: \"{search}\"")
    print()

def open_music_sites():
    """Open music download sites in browser."""
    print("Opening music download sites in your browser...")
    print()
    
    for name, info in MUSIC_SOURCES.items():
        print(f"Opening {name}...")
        try:
            webbrowser.open(info['url'])
        except Exception as e:
            print(f"  ⚠️ Could not open browser: {e}")
            print(f"  Please visit manually: {info['url']}")
    
    print()
    print("✅ Sites opened in browser!")

def print_download_instructions():
    print("=" * 70)
    print("  📥 DOWNLOAD INSTRUCTIONS")
    print("=" * 70)
    print()
    print("1. Browse the opened websites")
    print("2. Search for music using the recommended searches above")
    print("3. Download MP3 files (2-5 minutes duration recommended)")
    print("4. Save files to the appropriate mood folder:")
    print()
    print("   music/")
    print("   ├── epic/          ← Epic/cinematic tracks")
    print("   ├── emotional/     ← Emotional/touching tracks")
    print("   └── uplifting/     ← Uplifting/motivational tracks")
    print()
    print("5. Aim for 3-5 tracks per mood for variety")
    print()

def print_recommendations():
    print("=" * 70)
    print("  🎯 TRACK RECOMMENDATIONS")
    print("=" * 70)
    print()
    
    print("EPIC/CINEMATIC:")
    print("  • Duration: 2-5 minutes")
    print("  • Style: Orchestral, dramatic, intense")
    print("  • Keywords: epic, cinematic, powerful, heroic, trailer")
    print()
    
    print("EMOTIONAL:")
    print("  • Duration: 2-4 minutes")
    print("  • Style: Piano, strings, ambient")
    print("  • Keywords: emotional, touching, heartfelt, piano, sad")
    print()
    
    print("UPLIFTING:")
    print("  • Duration: 2-4 minutes")
    print("  • Style: Upbeat, energetic, optimistic")
    print("  • Keywords: uplifting, motivational, inspiring, positive")
    print()

def check_music_folders():
    """Check current music folder status."""
    print("=" * 70)
    print("  📊 CURRENT MUSIC LIBRARY STATUS")
    print("=" * 70)
    print()
    
    music_dir = "music"
    moods = ["epic", "emotional", "uplifting"]
    
    total_tracks = 0
    for mood in moods:
        mood_dir = os.path.join(music_dir, mood)
        if os.path.exists(mood_dir):
            files = [f for f in os.listdir(mood_dir) 
                    if f.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg', '.flac'))]
            count = len(files)
            total_tracks += count
            status = "✅" if count > 0 else "⚠️"
            print(f"{status} {mood.capitalize()}: {count} tracks")
            if count > 0:
                for f in files[:3]:  # Show first 3
                    print(f"     - {f}")
                if count > 3:
                    print(f"     ... and {count - 3} more")
        else:
            print(f"⚠️ {mood.capitalize()}: Folder not found")
    
    print()
    print(f"Total: {total_tracks} tracks")
    
    if total_tracks == 0:
        print()
        print("⚠️ No music files found! Please download some tracks.")
    elif total_tracks < 9:
        print()
        print("💡 Tip: Add more tracks for better variety (aim for 3-5 per mood)")
    else:
        print()
        print("✅ Great! You have a good music library.")
    print()

def main():
    print_header()
    
    print("This helper will:")
    print("  1. Show you where to download royalty-free music")
    print("  2. Open music sites in your browser")
    print("  3. Provide download instructions")
    print()
    
    # Check current status
    check_music_folders()
    
    # Show sources
    print("=" * 70)
    print("  🌐 MUSIC SOURCES")
    print("=" * 70)
    print()
    
    for name, info in MUSIC_SOURCES.items():
        print_source_info(name, info)
    
    # Ask to open sites
    response = input("Open these sites in your browser? (y/n): ").strip().lower()
    if response == 'y':
        open_music_sites()
    
    # Show instructions
    print_download_instructions()
    print_recommendations()
    
    print("=" * 70)
    print("  ✅ READY TO DOWNLOAD!")
    print("=" * 70)
    print()
    print("After downloading music:")
    print("  1. Place files in music/[mood]/ folders")
    print("  2. Run: python test_audio_mixer.py")
    print("  3. Test: python mix_audio.py your_voice.wav --mood epic")
    print()
    print("Happy creating! 🎬🎵")
    print()

if __name__ == "__main__":
    main()
