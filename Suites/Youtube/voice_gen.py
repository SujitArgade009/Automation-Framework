import sys
import os
import datetime
from pathlib import Path

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import ELEVENLABS_API_KEY
    from elevenlabs import generate, set_api_key
except ImportError:
    # Fallback for missing dependencies
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    generate = None
    set_api_key = None

def generate_voice(text: str, voice_type: str = "female", speed: str = "normal") -> Path:
    """
    Generate voice from text using ElevenLabs API.
    
    Args:
        text (str): Text to convert to speech
        voice_type (str): Voice type - "male", "female", "neutral"
        speed (str): Speaking speed - "slow", "normal", "fast"
    
    Returns:
        Path: Path to the generated audio file
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("ElevenLabs API key not found. Please set ELEVENLABS_API_KEY in config.py or environment variables.")
    
    if not generate or not set_api_key:
        raise ImportError("ElevenLabs library not installed. Please install it with: pip install elevenlabs")
    
    # Configure ElevenLabs
    set_api_key(ELEVENLABS_API_KEY)
    
    # Define voice IDs (you can customize these)
    voice_ids = {
        "male": "21m00Tcm4TlvDq8ikWAM",  # Josh
        "female": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "neutral": "21m00Tcm4TlvDq8ikWAM"  # Default
    }
    
    # Define speed parameters
    speed_params = {
        "slow": 0.8,
        "normal": 1.0,
        "fast": 1.2
    }
    
    # Get parameters
    voice_id = voice_ids.get(voice_type, voice_ids["female"])
    speed_value = speed_params.get(speed, speed_params["normal"])
    
    try:
        # Generate the audio
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"
        )
        
        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_text = "".join(c for c in text[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_text = safe_text.replace(' ', '_')[:20]  # Limit length
        filename = f"voice_{safe_text}_{voice_type}_{timestamp}.mp3"
        
        # Ensure output directory exists
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Save the audio file
        audio_path = output_dir / filename
        with open(audio_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"[VOICE] Generated voice saved to: {audio_path}")
        return audio_path
        
    except Exception as e:
        raise Exception(f"Failed to generate voice: {str(e)}")

def generate_voice_from_file(script_file: Path) -> Path:
    """
    Generate voice from a script file.
    
    Args:
        script_file (Path): Path to the script file
    
    Returns:
        Path: Path to the generated audio file
    """
    if not script_file.exists():
        raise FileNotFoundError(f"Script file not found: {script_file}")
    
    # Read the script text
    try:
        with open(script_file, "r", encoding="utf-8") as f:
            script_text = f.read()
    except Exception as e:
        raise Exception(f"Failed to read script file: {str(e)}")
    
    # Generate voice from the text
    return generate_voice(script_text)

def run(script_file):
    """
    Legacy function for backward compatibility.
    """
    if isinstance(script_file, str):
        script_file = Path(script_file)
    return generate_voice_from_file(script_file)
