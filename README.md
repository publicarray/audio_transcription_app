# Audio Transcription App

A powerful audio transcription application with advanced speaker diarization and a user-friendly Streamlit GUI. This app transcribes audio files, automatically identifies different speakers, and generates color-coded transcriptions with timestamps.

## Project Overview

This application combines advanced audio processing with a clean, intuitive interface to make transcription accessible to everyone. Key features include:

- **Advanced Speaker Diarization**: Uses AI-powered technology to accurately identify and color-code different speakers
- **Easy-to-use Interface**: Upload audio files and adjust settings with a simple web UI
- **Formatted Output**: View transcriptions in the browser and download as formatted Word documents
- **Modern Development Setup**: Managed with Poetry and pyenv for consistent environments

## Installation

### Prerequisites

- Python 3.11 (managed through pyenv)
- Poetry (for dependency management)
- ffmpeg (for audio processing)
- HuggingFace account and access token (for pyannote.audio models)

### Setup Instructions

1. **Install pyenv** (if not already installed)
   ```bash
   curl https://pyenv.run | bash
   ```
   Follow the prompts to add pyenv to your shell configuration.

2. **Install Python 3.11.11 with pyenv**
   ```bash
   pyenv install 3.11.11
   ```

3. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/audio-transcription-app.git
   cd audio-transcription-app
   ```

4. **Set local Python version**
   ```bash
   pyenv local 3.11.11
   ```

5. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

6. **Configure HuggingFace Access Token**
   
   This application uses pyannote.audio which requires access to models on HuggingFace:
   
   a. Create a HuggingFace account at https://huggingface.co/join
   
   b. Visit https://huggingface.co/pyannote/speaker-diarization and accept the user conditions
   
   c. Visit https://huggingface.co/pyannote/segmentation and accept the user conditions
   
   d. Generate an access token at https://huggingface.co/settings/tokens
   
   e. Set your token as an environment variable:
      ```bash
      export HUGGINGFACE_TOKEN=your_access_token_here
      ```
      
      Or create a `.env` file in the project root with:
      ```
      HUGGINGFACE_TOKEN=your_access_token_here
      ```

## Usage

### Fix ctranslate2 with newer Python

see: https://github.com/OpenNMT/CTranslate2/issues/1849

```bash
patchelf --clear-execstack ~/.cache/pypoetry/virtualenvs/audio-transcription-app-96PhKkBZ-py3.11/lib/python3.11/site-packages/ctranslate2.libs/libctranslate2-bc15bf3f.so.4.5.0
```

### Fix PyInstaller

Fix for `[Errno 2] No such file or directory: '/tmp/.mount_Audio_HjYkvD/_internal/lightning_fabric/version.info'`

see https://github.com/pyannote/pyannote-audio/issues/1400#issuecomment-2144716405

```bash
sed -i s/lightning_fabric/lightning.fabric/g ~/.cache/pypoetry/virtualenvs/audio-transcription-app-96PhKkBZ-py3.11/lib/python3.11/site-packages/pyannote/audio/core/model.py
```

### Running the Application

Start the Streamlit app using Poetry:

```bash
poetry run python run_app.py
```

Or use the Poetry script:

```bash
poetry run app
```

The app will be available at http://localhost:8501 in your web browser.

### Using the Application

1. Upload an audio file (WAV or MP3) using the file uploader
2. Adjust transcription settings in the sidebar if needed
3. Click the "Start Transcription" button to begin processing
4. View the color-coded transcription results with timestamps in the app
5. Download the Word document with the complete transcription

## Dependencies

This project uses the following main dependencies:

- **streamlit**: For the web-based user interface
- **pydub**: For audio file processing
- **SpeechRecognition**: For converting speech to text
- **python-docx**: For generating formatted Word documents
- **pyannote.audio**: For advanced speaker diarization
- **torch**: Required for the pyannote.audio neural networks
- **faster-whisper**: For improved speech recognition accuracy

All dependencies are managed through Poetry and specified in the pyproject.toml file.

## Development

### Adding New Dependencies

```bash
poetry add package-name
```

### Activating the Virtual Environment

```bash
poetry shell
```

### Running Tests

```bash
poetry run pytest
```

## Speaker Diarization

### Advanced Speaker Identification

This application now uses `pyannote.audio` to provide significantly improved speaker identification compared to the previous basic approach:

- **Previous Method**: The original implementation used a simple approach based on audio volume (dBFS) to differentiate speakers, which was not effective for real conversations with background noise or overlapping speech.

- **Current Method**: The new implementation uses pyannote.audio's neural network-based speaker diarization, which:
  - Leverages deep learning models trained on extensive audio datasets
  - Accurately identifies speaker changes even with overlapping speech
  - Provides precise timestamps for each speaker's segments
  - Works well with varying audio conditions and background noise
  - Integrates with faster-whisper for high-quality transcription

The improved speaker diarization process:
1. Uses pyannote.audio to identify who speaks when in the audio
2. Segments the audio based on speaker changes
3. Transcribes each segment using faster-whisper
4. Combines speaker information with transcribed text
5. Displays results with precise timestamps for each segment

### System Requirements

Due to the advanced nature of the speaker diarization models:
- Processing may take longer compared to the basic method
- At least 4GB of RAM is recommended
- GPU acceleration will significantly improve processing speed if available

## Troubleshooting

If you encounter any issues with audio processing, ensure you have ffmpeg installed:

- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

If you encounter issues with pyannote.audio:

- Ensure you've accepted the user conditions for both required models on HuggingFace
- Verify your HuggingFace token is correct and accessible to the application
- Check that you have sufficient memory for running the diarization models
- For Windows users, you may need to install Visual C++ Build Tools for some dependencies

## License

[MIT License](LICENSE)
