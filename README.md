# YouTube Automation

A Python-based automation pipeline that generates video scripts using ChatGPT, converts them to voiceovers via ElevenLabs, creates animations with Pika Labs, merges audio-video using FFMPEG, and automatically uploads videos to YouTube—streamlining end-to-end video production and publishing.

## 🚀 Features

- **🤖 AI-Powered Script Generation**: Create engaging video scripts using OpenAI's GPT-4
- **🎤 Natural Voice Synthesis**: Convert scripts to natural-sounding voiceovers via ElevenLabs
- **🎬 Animation Creation**: Generate animations using Pika Labs AI
- **✂️ Video Editing**: Merge audio and video using FFMPEG
- **📺 YouTube Upload**: Automatically publish videos to YouTube
- **🌐 Web Interface**: Modern FastAPI-based web application with beautiful UI
- **⚡ Full Pipeline**: End-to-end automation from script to published video

## 🏗️ Project Structure

```
youtube-automation/
├── api_server.py          # FastAPI web server
├── pipeline.py            # Main automation pipeline
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── stages/                # Processing stages
│   ├── script_gen.py      # ChatGPT script generation
│   ├── voice_gen.py       # ElevenLabs voice synthesis
│   ├── animation_gen.py   # Pika Labs animation
│   ├── video_edit.py      # FFMPEG video editing
│   └── upload_youtube.py  # YouTube upload
├── frontend/              # Web interface
│   ├── index.html         # Main page
│   ├── app.js             # JavaScript functionality
│   └── style.css          # Styling
└── output/                # Generated files
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **AI Services**: 
  - OpenAI GPT-4 (Script Generation)
  - ElevenLabs (Voice Synthesis)
  - Pika Labs (Animation Creation)
- **Video Processing**: FFMPEG
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Uvicorn server

## 📋 Prerequisites

- Python 3.8 or higher
- FFMPEG installed on your system
- API keys for:
  - OpenAI (for script generation)
  - ElevenLabs (for voice synthesis)
  - YouTube API (for video upload)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd youtube-automation
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**
   Create a `config.py` file in the project root:
   ```python
   # config.py
   OPENAI_API_KEY = "your-openai-api-key"
   ELEVENLABS_API_KEY = "your-elevenlabs-api-key"
   YOUTUBE_API_KEY = "your-youtube-api-key"
   ```

4. **Install FFMPEG** (if not already installed)
   - **Windows**: Download from [FFMPEG website](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the server**
   ```bash
   python api_server.py
   ```

2. **Access the web interface**
   Open your browser and navigate to `http://localhost:8000`

3. **Use the interface**
   - **Script Generator**: Create video scripts by topic, length, and style
   - **Voice Generator**: Convert text to speech with various voice options
   - **Video Creator**: Generate videos from scripts and animations

### Command Line Interface

1. **Run the full pipeline**
   ```bash
   python pipeline.py
   ```

2. **Run individual stages**
   ```bash
   # Generate script
   python -c "from stages.script_gen import run; run(theme='motivation')"
   
   # Generate voice
   python -c "from stages.voice_gen import run; run('script_file.txt')"
   
   # Create animation
   python -c "from stages.animation_gen import run; run('script_file.txt')"
   ```

## 📊 API Endpoints

The FastAPI server provides the following endpoints:

- `GET /` - Main web interface
- `POST /generate_script/` - Generate video scripts
- `POST /generate_voice/` - Convert text to speech
- `POST /create_video/` - Create videos from scripts
- `GET /list_outputs/` - List generated files
- `DELETE /delete_file/{filename}` - Delete generated files

## 🎨 Supported Content Styles

- **Educational**: Informative, step-by-step explanations
- **Entertaining**: Engaging, humorous, captivating storytelling
- **Professional**: Formal, business-like, authoritative tone
- **Casual**: Conversational, friendly, relaxed tone

## ⏱️ Script Lengths

- **Short**: 2-3 minutes (150-250 words)
- **Medium**: 5-7 minutes (400-600 words)
- **Long**: 10-15 minutes (800-1200 words)

## 🔧 Configuration

### Environment Variables

You can also set API keys using environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
export YOUTUBE_API_KEY="your-youtube-api-key"
```

### Custom Settings

Modify `config.py` to customize:
- Default video resolution
- Output directory paths
- API endpoints
- Voice settings

## 🐛 Troubleshooting

### Common Issues

1. **FFMPEG not found**
   - Ensure FFMPEG is installed and in your system PATH
   - On Windows, add FFMPEG to your system environment variables

2. **API key errors**
   - Verify all API keys are correctly set in `config.py`
   - Check that API keys have sufficient credits/permissions

3. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- ElevenLabs for voice synthesis
- Pika Labs for animation generation
- FastAPI community for the web framework

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the API documentation at `http://localhost:8000/docs` when running

---

**Happy video creating! 🎬**
