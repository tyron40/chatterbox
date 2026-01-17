"""Test if all imports work"""
import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "src"))

print("Testing imports...")

try:
    import gradio as gr
    print("✓ gradio imported")
except Exception as e:
    print(f"✗ gradio failed: {e}")

try:
    from modules.config import LANGUAGE_CONFIG, SUPPORTED_LANGUAGES
    print("✓ modules.config imported")
except Exception as e:
    print(f"✗ modules.config failed: {e}")

try:
    from modules.voice_manager import load_voices
    print("✓ modules.voice_manager imported")
except Exception as e:
    print(f"✗ modules.voice_manager failed: {e}")

try:
    from modules.generation_functions import generate_batch_turbo_speech, create_batch_zip
    print("✓ modules.generation_functions imported")
except Exception as e:
    print(f"✗ modules.generation_functions failed: {e}")

try:
    from modules.audio_mixer import mix_audio_with_music
    print("✓ modules.audio_mixer imported")
except Exception as e:
    print(f"✗ modules.audio_mixer failed: {e}")

try:
    from modules.ui_components import create_batch_tab
    print("✓ modules.ui_components imported")
except Exception as e:
    print(f"✗ modules.ui_components failed: {e}")

print("\nAll imports tested!")
