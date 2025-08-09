import sys
import os
import time
import datetime
import requests
from pathlib import Path

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import PIKA_API_KEY
except ImportError:
    # Fallback for missing dependencies
    PIKA_API_KEY = os.getenv("PIKA_API_KEY")

def create_video(script_path: Path, style: str = "modern", resolution: str = "1080p") -> Path:
    """
    Create a video from a script file using Pika Labs API.
    
    Args:
        script_path (Path): Path to the script file
        style (str): Video style - "modern", "minimal", "dynamic", "elegant"
        resolution (str): Video resolution - "720p", "1080p", "4k"
    
    Returns:
        Path: Path to the generated video file
    """
    if not PIKA_API_KEY:
        raise ValueError("Pika Labs API key not found. Please set PIKA_API_KEY in config.py or environment variables.")
    
    if not script_path.exists():
        raise FileNotFoundError(f"Script file not found: {script_path}")
    
    # Read the script content
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
    except Exception as e:
        raise Exception(f"Failed to read script file: {str(e)}")
    
    # Define style prompts
    style_prompts = {
        "modern": "modern, sleek, contemporary design, clean lines, professional",
        "minimal": "minimalist, simple, clean, uncluttered, elegant",
        "dynamic": "dynamic, energetic, vibrant, fast-paced, engaging",
        "elegant": "elegant, sophisticated, refined, polished, high-quality"
    }
    
    # Define resolution parameters
    resolution_params = {
        "720p": {"width": 1280, "height": 720},
        "1080p": {"width": 1920, "height": 1080},
        "4k": {"width": 3840, "height": 2160}
    }
    
    # Get parameters
    style_prompt = style_prompts.get(style, style_prompts["modern"])
    res_params = resolution_params.get(resolution, resolution_params["1080p"])
    
    # Create the animation prompt based on script content
    # Extract key themes from the script (simplified approach)
    script_lines = script_content.split('\n')[:5]  # First 5 lines
    script_summary = ' '.join(script_lines).strip()
    
    animation_prompt = f"A {style_prompt} animated video about: {script_summary[:200]}... Colorful, vibrant, engaging visuals that match the content."
    
    try:
        # Step 1: Create video job
        create_url = "https://api.pika.art/v1/video.create"
        headers = {"Authorization": f"Bearer {PIKA_API_KEY}"}
        payload = {
            "prompt": animation_prompt,
            "aspect_ratio": f"{res_params['width']}:{res_params['height']}",
            "fps": 24,
            "duration": 10  # seconds
        }
        
        print("🎬 Sending request to Pika Labs...")
        response = requests.post(create_url, headers=headers, json=payload)
        
        if not response.ok:
            raise Exception(f"Failed to create video job: {response.text}")
        
        data = response.json()
        if "id" not in data:
            raise Exception(f"Invalid response from Pika Labs: {data}")
        
        video_id = data["id"]
        print(f"✅ Video job created with ID: {video_id}")
        
        # Step 2: Poll for completion
        status_url = f"https://api.pika.art/v1/video.get?id={video_id}"
        video_url = None
        max_attempts = 60  # 5 minutes with 5-second intervals
        attempts = 0
        
        print("⏳ Waiting for Pika Labs to finish rendering...")
        while attempts < max_attempts:
            status_resp = requests.get(status_url, headers=headers)
            
            if not status_resp.ok:
                raise Exception(f"Failed to check video status: {status_resp.text}")
            
            status_data = status_resp.json()
            
            if status_data.get("status") == "completed":
                video_url = status_data.get("video")
                if video_url:
                    print("✅ Video ready!")
                    break
                else:
                    raise Exception("Video completed but no URL provided")
            elif status_data.get("status") == "failed":
                raise Exception("Video generation failed")
            
            attempts += 1
            time.sleep(5)
        
        if not video_url:
            raise Exception("Video generation timed out")
        
        # Step 3: Download the video
        print("⬇ Downloading video...")
        video_resp = requests.get(video_url)
        
        if not video_resp.ok:
            raise Exception(f"Failed to download video: {video_resp.status_code}")
        
        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        script_name = script_path.stem
        filename = f"video_{script_name}_{style}_{resolution}_{timestamp}.mp4"
        
        # Ensure output directory exists
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Save the video file
        video_path = output_dir / filename
        with open(video_path, "wb") as f:
            f.write(video_resp.content)
        
        print(f"🎉 Video saved as {video_path}")
        return video_path
        
    except Exception as e:
        raise Exception(f"Failed to create video: {str(e)}")

def run(script_file=None, style="modern", resolution="1080p"):
    """
    Legacy function for backward compatibility.
    """
    if script_file is None:
        # Use a default script or create one
        script_file = Path(__file__).parent.parent / "output" / "default_script.txt"
        if not script_file.exists():
            # Create a simple default script
            script_file.parent.mkdir(exist_ok=True)
            with open(script_file, "w") as f:
                f.write("This is a default script for video generation.")
    
    if isinstance(script_file, str):
        script_file = Path(script_file)
    
    return create_video(script_file, style, resolution)
