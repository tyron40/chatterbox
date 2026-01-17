#!/usr/bin/env python3
"""
Cinematic Audio Mixer CLI
Command-line tool for mixing voice with background music
"""
import sys
import os
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.audio_mixer import (
    mix_audio_with_music,
    batch_mix_audio,
    get_available_moods,
    print_system_info,
    MUSIC_DIR,
    OUTPUT_DIR
)


def main():
    parser = argparse.ArgumentParser(
        description="🎬 Cinematic Audio Mixer - Add background music to voice files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mix single file with epic music
  python mix_audio.py voice.wav --mood epic
  
  # Mix with specific music file
  python mix_audio.py voice.wav --music my_track.mp3
  
  # Batch mix multiple files
  python mix_audio.py voice1.wav voice2.wav voice3.wav --mood emotional
  
  # Disable ducking (no volume reduction)
  python mix_audio.py voice.wav --mood uplifting --no-ducking
  
  # Custom output path
  python mix_audio.py voice.wav --output final_audio.mp3
  
  # Check system status
  python mix_audio.py --info
        """
    )
    
    parser.add_argument(
        "voice_files",
        nargs="*",
        help="Voice audio file(s) to mix with music"
    )
    
    parser.add_argument(
        "--mood",
        "-m",
        choices=["epic", "emotional", "uplifting"],
        default="epic",
        help="Music mood (default: epic)"
    )
    
    parser.add_argument(
        "--music",
        help="Specific music file to use (overrides mood selection)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (for single file only)"
    )
    
    parser.add_argument(
        "--volume",
        "-v",
        type=float,
        default=0.15,
        help="Background music volume 0.0-1.0 (default: 0.15)"
    )
    
    parser.add_argument(
        "--no-ducking",
        action="store_true",
        help="Disable automatic ducking (music volume reduction)"
    )
    
    parser.add_argument(
        "--info",
        "-i",
        action="store_true",
        help="Show system information and exit"
    )
    
    args = parser.parse_args()
    
    # Show system info
    if args.info:
        print_system_info()
        return 0
    
    # Validate input
    if not args.voice_files:
        print("❌ Error: No voice files specified")
        print("Use --help for usage information")
        return 1
    
    # Validate voice files exist
    for voice_file in args.voice_files:
        if not os.path.exists(voice_file):
            print(f"❌ Error: File not found: {voice_file}")
            return 1
    
    # Validate music file if specified
    if args.music and not os.path.exists(args.music):
        print(f"❌ Error: Music file not found: {args.music}")
        return 1
    
    # Validate volume
    if not 0.0 <= args.volume <= 1.0:
        print("❌ Error: Volume must be between 0.0 and 1.0")
        return 1
    
    # Single file mode
    if len(args.voice_files) == 1:
        print("\n🎬 CINEMATIC AUDIO MIXER")
        print("=" * 60)
        
        result = mix_audio_with_music(
            voice_path=args.voice_files[0],
            output_path=args.output,
            mood=args.mood,
            music_path=args.music,
            music_volume=args.volume,
            enable_ducking=not args.no_ducking
        )
        
        if result:
            print("\n✅ SUCCESS!")
            print(f"📁 Output: {result}")
            return 0
        else:
            print("\n❌ FAILED!")
            return 1
    
    # Batch mode
    else:
        if args.output:
            print("⚠️ Warning: --output ignored in batch mode")
        
        print("\n🎬 CINEMATIC AUDIO MIXER - BATCH MODE")
        print("=" * 60)
        
        results = batch_mix_audio(
            voice_files=args.voice_files,
            mood=args.mood,
            output_dir=OUTPUT_DIR
        )
        
        if results:
            print(f"\n✅ SUCCESS! Mixed {len(results)} files")
            print(f"📁 Output directory: {OUTPUT_DIR}")
            return 0
        else:
            print("\n❌ FAILED!")
            return 1


if __name__ == "__main__":
    sys.exit(main())
