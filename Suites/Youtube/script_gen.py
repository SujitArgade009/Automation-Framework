import sys
import os
import datetime
from pathlib import Path

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from config import OPENAI_API_KEY
    import openai
except ImportError:
    # Fallback for missing dependencies
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai = None

def generate_script(topic: str, length: str = "medium", style: str = "educational") -> Path:
    """
    Generate a script based on the provided topic, length, and style.
    
    Args:
        topic (str): The video topic/theme
        length (str): Script length - "short", "medium", "long"
        style (str): Content style - "educational", "entertaining", "professional", "casual"
    
    Returns:
        Path: Path to the generated script file
    """
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in config.py or environment variables.")
    
    if not openai:
        raise ImportError("OpenAI library not installed. Please install it with: pip install openai")
    
    # Configure OpenAI
    openai.api_key = OPENAI_API_KEY
    
    # Define length parameters
    length_params = {
        "short": {"duration": "2-3 minutes", "word_count": "150-250"},
        "medium": {"duration": "5-7 minutes", "word_count": "400-600"},
        "long": {"duration": "10-15 minutes", "word_count": "800-1200"}
    }
    
    # Define style parameters
    style_params = {
        "educational": "educational, informative, clear explanations, step-by-step approach",
        "entertaining": "entertaining, engaging, humorous, captivating storytelling",
        "professional": "professional, formal, business-like, authoritative tone",
        "casual": "casual, conversational, friendly, relaxed tone"
    }
    
    # Get parameters
    length_info = length_params.get(length, length_params["medium"])
    style_info = style_params.get(style, style_params["educational"])
    
    # Create the prompt
    prompt = f"""Write a {length_info['duration']} script for a YouTube video.

Topic: {topic}
Style: {style_info}
Target word count: {length_info['word_count']} words

Structure the script with:
1. Hook (10-15% of content) - Grab attention immediately
2. Introduction (15-20% of content) - Set context and expectations
3. Main Content (60-70% of content) - Core information/entertainment
4. Conclusion (10-15% of content) - Wrap up and call to action

Make it engaging, well-paced, and suitable for {style} content.
Include natural speech patterns and transitions.
Avoid jargon unless necessary for the topic.

Format the output as a clean script with clear sections."""

    try:
        # Generate the script
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional script writer specializing in YouTube content creation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        script_content = response.choices[0].message.content.strip()
        
        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')[:30]  # Limit length
        filename = f"script_{safe_topic}_{length}_{timestamp}.txt"
        
        # Ensure output directory exists
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Save the script
        script_path = output_dir / filename
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(f"# Script: {topic}\n")
            f.write(f"# Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Length: {length_info['duration']}\n")
            f.write(f"# Style: {style}\n")
            f.write("=" * 50 + "\n\n")
            f.write(script_content)
        
        print(f"[SCRIPT] Generated script saved to: {script_path}")
        return script_path
        
    except Exception as e:
        raise Exception(f"Failed to generate script: {str(e)}")

def run(theme="comedy"):
    """
    Legacy function for backward compatibility.
    """
    return generate_script(theme, "medium", "entertaining")
