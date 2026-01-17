"""Run app.py with comprehensive error logging"""
import sys
import os
import traceback
from datetime import datetime

# Create logs directory
os.makedirs("logs", exist_ok=True)
log_file = f"logs/debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(message):
    """Log to both console and file"""
    print(message)
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    except:
        pass  # If file writing fails, just print

try:
    log("=" * 60)
    log(f"Starting Chatterbox TTS Debug - {datetime.now()}")
    log("=" * 60)
    log(f"Python: {sys.version}")
    log(f"Working Directory: {os.getcwd()}")
    log("")
    
    log("Step 1: Changing to app directory...")
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    log(f"✓ Changed to: {os.getcwd()}")
    
    # Create logs directory after changing to app dir
    os.makedirs("logs", exist_ok=True)
    log("")
    
    log("Step 2: Reading app.py...")
    with open('app.py', 'r', encoding='utf-8') as f:
        app_code = f.read()
    log(f"✓ Read {len(app_code)} characters")
    log("")
    
    log("Step 3: Executing app.py...")
    log("-" * 60)
    exec(app_code, {
        '__name__': '__main__',
        '__file__': os.path.join(os.getcwd(), 'app.py')
    })
    
except Exception as e:
    log("")
    log("=" * 60)
    log("ERROR OCCURRED!")
    log("=" * 60)
    log(f"Error Type: {type(e).__name__}")
    log(f"Error Message: {str(e)}")
    log("")
    log("Full Traceback:")
    log("-" * 60)
    log(traceback.format_exc())
    log("=" * 60)
    
    print(f"\n\nError details saved to: {log_file}")
    sys.exit(1)
