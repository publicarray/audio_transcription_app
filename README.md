# Audio Transcription App

A powerful audio transcription application with speaker recognition and a user-friendly Streamlit GUI. This app transcribes audio files, automatically identifies different speakers, and generates color-coded transcriptions.

## Project Overview

This application combines advanced audio processing with a clean, intuitive interface to make transcription accessible to everyone. Key features include:

- **Speaker Diarization**: Automatically identifies and color-codes different speakers
- **Easy-to-use Interface**: Upload audio files and adjust settings with a simple web UI
- **Formatted Output**: View transcriptions in the browser and download as formatted Word documents
- **Modern Development Setup**: Managed with Poetry and pyenv for consistent environments

## Installation

### Prerequisites

- Python 3.11 (managed through pyenv)
- Poetry (for dependency management)
- ffmpeg (for audio processing)

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

## Usage

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
2. Adjust the number of speakers in the sidebar if needed (default is 3)
3. Click the "Start Transcription" button to begin processing
4. View the color-coded transcription results in the app
5. Download the Word document with the complete transcription

## Dependencies

This project uses the following main dependencies:

- **streamlit**: For the web-based user interface
- **pydub**: For audio file processing
- **SpeechRecognition**: For converting speech to text
- **python-docx**: For generating formatted Word documents

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

## Troubleshooting

If you encounter any issues with audio processing, ensure you have ffmpeg installed:

- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## License

[MIT License](LICENSE)
