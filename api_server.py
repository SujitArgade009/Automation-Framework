import sys
import os
import json
import uuid
from pathlib import Path
from typing import Optional, List
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Import stage modules
try:
    from ai_video_pipeline.stages import script_gen, voice_gen, video_edit, animation_gen
except ImportError:
    # Fallback for direct imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from stages import script_gen, voice_gen, video_edit, animation_gen

# Initialize FastAPI app
app = FastAPI(
    title="AI Video Pipeline API",
    description="API for generating scripts, voices, and videos using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory setup
BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

# Pydantic models for request/response
class ScriptRequest(BaseModel):
    topic: str = Field(..., description="Video topic/theme")
    length: str = Field(default="medium", description="Script length: short, medium, long")
    style: Optional[str] = Field(default="educational", description="Content style")

class VoiceRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    voice_type: str = Field(default="female", description="Voice type: male, female, neutral")
    speed: str = Field(default="normal", description="Speaking speed: slow, normal, fast")

class VideoRequest(BaseModel):
    script_file: str = Field(..., description="Path to script file")
    style: str = Field(default="modern", description="Video style")
    resolution: str = Field(default="1080p", description="Video resolution")

class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None

# Utility functions
def generate_unique_filename(prefix: str, extension: str) -> str:
    """Generate a unique filename with timestamp and UUID."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{timestamp}_{unique_id}.{extension}"

def save_uploaded_file(upload_file: UploadFile, directory: Path) -> Path:
    """Save an uploaded file and return the path."""
    filename = generate_unique_filename("upload", upload_file.filename.split('.')[-1])
    file_path = directory / filename
    
    with open(file_path, "wb") as buffer:
        content = upload_file.file.read()
        buffer.write(content)
    
    return file_path

# Routes
@app.get("/")
async def index():
    """Serve the main application page."""
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/generate_script/", response_model=APIResponse)
async def generate_script_endpoint(request: ScriptRequest):
    """
    Generate a script based on the provided topic and parameters.
    """
    try:
        # Validate input
        if not request.topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        # Generate script using the script_gen module
        script_path = script_gen.generate_script(
            topic=request.topic,
            length=request.length,
            style=request.style
        )
        
        # Convert to relative path for frontend
        if isinstance(script_path, str):
            script_path = Path(script_path)
        
        relative_path = f"/output/{script_path.name}"
        
        # Read script content for response
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
        except Exception as e:
            script_content = f"Script generated but content could not be read: {str(e)}"
        
        return APIResponse(
            status="success",
            message="Script generated successfully",
            data={
                "script_path": relative_path,
                "script_content": script_content,
                "filename": script_path.name
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate script: {str(e)}")

@app.post("/generate_voice/", response_model=APIResponse)
async def generate_voice_endpoint(request: VoiceRequest):
    """
    Generate voice from text using AI voice synthesis.
    """
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if len(request.text) > 5000:
            raise HTTPException(status_code=400, detail="Text too long (max 5000 characters)")
        
        # Generate voice using the voice_gen module
        voice_path = voice_gen.generate_voice(
            text=request.text,
            voice_type=request.voice_type,
            speed=request.speed
        )
        
        # Convert to relative path for frontend
        if isinstance(voice_path, str):
            voice_path = Path(voice_path)
        
        relative_path = f"/output/{voice_path.name}"
        
        return APIResponse(
            status="success",
            message="Voice generated successfully",
            data={
                "voice_path": relative_path,
                "filename": voice_path.name,
                "duration": "Unknown"  # Could be calculated if needed
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate voice: {str(e)}")

@app.post("/create_video/", response_model=APIResponse)
async def create_video_endpoint(
    script_file: UploadFile = File(...),
    style: str = Form("modern"),
    resolution: str = Form("1080p")
):
    """
    Create a video from a script file.
    """
    try:
        # Validate file
        if not script_file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file extension
        allowed_extensions = ['.txt', '.md']
        file_extension = Path(script_file.filename).suffix.lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file
        script_path = save_uploaded_file(script_file, OUTPUT_DIR)
        
        # Generate video using the video_edit module
        video_path = video_edit.create_video(
            script_path=script_path,
            style=style,
            resolution=resolution
        )
        
        # Convert to relative path for frontend
        if isinstance(video_path, str):
            video_path = Path(video_path)
        
        relative_path = f"/output/{video_path.name}"
        
        # Get file size
        file_size = video_path.stat().st_size if video_path.exists() else 0
        
        return APIResponse(
            status="success",
            message="Video created successfully",
            data={
                "video_path": relative_path,
                "filename": video_path.name,
                "size": f"{file_size / (1024*1024):.1f} MB",
                "duration": "Unknown"  # Could be extracted if needed
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create video: {str(e)}")

@app.post("/upload_script/", response_model=APIResponse)
async def upload_script_endpoint(script_file: UploadFile = File(...)):
    """
    Upload a script file for processing.
    """
    try:
        # Validate file
        if not script_file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file extension
        allowed_extensions = ['.txt', '.md']
        file_extension = Path(script_file.filename).suffix.lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file
        script_path = save_uploaded_file(script_file, OUTPUT_DIR)
        
        return APIResponse(
            status="success",
            message="Script uploaded successfully",
            data={
                "script_path": f"/output/{script_path.name}",
                "filename": script_path.name
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload script: {str(e)}")

@app.get("/list_outputs/")
async def list_outputs():
    """
    List all generated files in the output directory.
    """
    try:
        files = []
        for file_path in OUTPUT_DIR.iterdir():
            if file_path.is_file():
                files.append({
                    "name": file_path.name,
                    "size": f"{file_path.stat().st_size / 1024:.1f} KB",
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    "type": file_path.suffix[1:] if file_path.suffix else "unknown"
                })
        
        return APIResponse(
            status="success",
            message=f"Found {len(files)} files",
            data={"files": files}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list outputs: {str(e)}")

@app.delete("/delete_file/{filename}")
async def delete_file(filename: str):
    """
    Delete a file from the output directory.
    """
    try:
        file_path = OUTPUT_DIR / filename
        
        # Security check - ensure file is in output directory
        if not file_path.resolve().is_relative_to(OUTPUT_DIR.resolve()):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        file_path.unlink()
        
        return APIResponse(
            status="success",
            message=f"File {filename} deleted successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
