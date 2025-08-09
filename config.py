"""
Configuration file for AI Video Pipeline.
Set your API keys here or use environment variables.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# API Keys (set these in environment variables for production)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
PIKA_API_KEY = os.getenv("PIKA_API_KEY", "")

# Application settings
APP_NAME = "AI Video Pipeline"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# File paths
OUTPUT_DIR = BASE_DIR / "output"
FRONTEND_DIR = BASE_DIR / "frontend"

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
FRONTEND_DIR.mkdir(exist_ok=True)

# API settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = [".txt", ".md", ".mp3", ".mp4", ".wav"]

# Voice generation settings
DEFAULT_VOICE_TYPE = "female"
DEFAULT_VOICE_SPEED = "normal"
MAX_TEXT_LENGTH = 5000

# Video generation settings
DEFAULT_VIDEO_STYLE = "modern"
DEFAULT_VIDEO_RESOLUTION = "1080p"
MAX_VIDEO_DURATION = 300  # 5 minutes

# Script generation settings
DEFAULT_SCRIPT_LENGTH = "medium"
DEFAULT_SCRIPT_STYLE = "educational"

# Security settings (for production)
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validation functions
def validate_api_keys():
    """Validate that required API keys are set."""
    missing_keys = []
    
    if not OPENAI_API_KEY:
        missing_keys.append("OPENAI_API_KEY")
    if not ELEVENLABS_API_KEY:
        missing_keys.append("ELEVENLABS_API_KEY")
    if not PIKA_API_KEY:
        missing_keys.append("PIKA_API_KEY")
    
    if missing_keys:
        print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
        print("Some features may not work without these keys.")
        return False
    
    return True

# Initialize validation
if __name__ == "__main__":
    validate_api_keys()
