"""Run app.py with error handling"""
import sys
import os
import traceback

try:
    print("Starting Chatterbox TTS...")
    print("=" * 50)
    
    # Change to the app directory
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(app_dir)
    
    # Execute app.py as a script
    with open('app.py', 'r', encoding='utf-8') as f:
        app_code = f.read()
    
    exec(app_code, {'__name__': '__main__'})
    
except Exception as e:
    print("\n" + "=" * 50)
    print("ERROR OCCURRED:")
    print("=" * 50)
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nFull traceback:")
    print("-" * 50)
    traceback.print_exc()
    print("=" * 50)
    sys.exit(1)
