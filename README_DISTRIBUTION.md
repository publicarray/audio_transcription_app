# Audio Transcription App - Distribution Guide

This guide provides comprehensive instructions for building, packaging, and distributing the Audio Transcription Application for both Linux (AppImage) and Windows (executable) platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Building for Linux (AppImage)](#building-for-linux-appimage)
- [Building for Windows (.exe)](#building-for-windows-exe)
- [Cross-Platform Building](#cross-platform-building)
- [Troubleshooting](#troubleshooting)
- [Distribution to End Users](#distribution-to-end-users)
- [Installation Instructions for End Users](#installation-instructions-for-end-users)

## Prerequisites

### General Requirements

- Python 3.8+ installed
- Poetry package manager
- Git (for cloning the repository)
- Internet connection (for downloading dependencies)
- PyInstaller (installed via Poetry: `poetry add pyinstaller`)

### Linux-Specific Requirements

- AppImageTool ([Download from GitHub](https://github.com/AppImage/AppImageKit/releases))
- Required system libraries:
  ```bash
  sudo apt-get update
  sudo apt-get install -y libportaudio2 libasound-dev libpulse-dev
  sudo apt-get install -y fuse libfuse2
  ```

### Windows-Specific Requirements

- Visual C++ Redistributable for Visual Studio 2015-2022
- Windows SDK (for some audio dependencies)

## Building for Linux (AppImage)

### 1. Prepare the Environment

```bash
# Clone the repository if you haven't already
git clone https://github.com/yourusername/audio_transcription_app.git
cd audio_transcription_app

# Install dependencies
poetry install

# Create .env file with HuggingFace token
echo "HF_TOKEN=your_token_here" > .env

# Install system dependencies
sudo apt-get update
sudo apt-get install -y libportaudio2 libasound-dev libpulse-dev
```

### 2. Install the Correct ctranslate2 Version

Since we encountered issues with specific versions of ctranslate2, use:

```bash
poetry run pip install ctranslate2==4.5.0 faster-whisper --force-reinstall
```

### 3. Build with PyInstaller

```bash
# Using our prepared spec file
poetry run pyinstaller linux_app.spec
```

### 4. Create AppImage

After running PyInstaller, create the AppImage:

```bash
# Download AppImageTool
wget -O appimagetool "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
chmod +x appimagetool

# Create AppDir structure 
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Copy PyInstaller output to AppDir
cp -r dist/audio_transcription_app/* AppDir/usr/bin/
cp assets/audio_transcription_app.desktop AppDir/usr/share/applications/
cp assets/audio_transcription_app.png AppDir/usr/share/icons/hicolor/256x256/apps/

# Create AppImage
./appimagetool AppDir

# The output will be AudioTranscriptionApp-x86_64.AppImage
```

## Building for Windows (.exe)

### 1. Prepare the Environment

```powershell
# Clone the repository
git clone https://github.com/yourusername/audio_transcription_app.git
cd audio_transcription_app

# Install dependencies with Poetry
poetry install

# Create .env file with HuggingFace token
echo "HF_TOKEN=your_token_here" > .env
```

### 2. Install the Correct Dependencies

```powershell
poetry run pip install ctranslate2==4.5.0 faster-whisper --force-reinstall
```

### 3. Build with PyInstaller

```powershell
# Using our prepared spec file
poetry run pyinstaller windows_app.spec
```

The output will be in the `dist` folder:
- `audio_transcription_app/` (folder containing all files)
- `audio_transcription_app.exe` (standalone executable)

## Cross-Platform Building

If you want to build for both platforms from a single system, you can use:

### Linux → Windows (using Wine)

```bash
# Install Wine
sudo apt-get install wine64 mingw-w64

# Set up Python in Wine
wine pip install pyinstaller

# Build Windows version
wine pyinstaller windows_app.spec
```

### Windows → Linux (using WSL)

```powershell
# Set up WSL and build the Linux version there
# This is more complex and requires setting up an Ubuntu environment in WSL
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "ctranslate2 dependency issue detected"

**Solution**: Install a compatible version:
```bash
poetry run pip install ctranslate2==4.5.0 faster-whisper --force-reinstall
```

#### 2. "ImportError: libctranslate2-bc15bf3f.so.4.5.0: cannot enable executable stack"

**Solution**: This is a system-level issue. Try:
```bash
sudo sysctl -w vm.mmap_min_addr=0
```
Or switch to using standard whisper:
```bash
poetry run pip install openai-whisper
```

#### 3. Missing .env file or HF_TOKEN not being read

**Solution**: Make sure you have a .env file in the root directory:
```bash
echo "HF_TOKEN=your_token_here" > .env
```

#### 4. "ModuleNotFoundError" in the packaged application

**Solution**: Add the missing module to the hidden-imports in the .spec file:
```python
hiddenimports=['missing_module_name']
```

#### 5. Audio libraries not found

**Solution**: On Linux:
```bash
sudo apt-get install -y libportaudio2 libasound-dev
```
On Windows, install the Visual C++ Redistributable package.

## Distribution to End Users

### Hosting and Distribution Platforms

1. **GitHub Releases**
   - Create a new release
   - Attach both AppImage and .exe files
   - Include release notes

2. **Personal Website or Server**
   - Host the files on your web server
   - Provide direct download links

3. **Package Managers** (Advanced)
   - For Linux: Create a PPA (Ubuntu) or RPM/DEB package
   - For Windows: Create an MSI installer

### Creating an Installer for Windows

```powershell
# Install NSIS (Nullsoft Scriptable Install System)
# Create an installer.nsi script
# Run: makensis installer.nsi
```

### Making the AppImage Executable

When distributing the AppImage, remind users to make it executable:

```bash
chmod +x AudioTranscriptionApp-x86_64.AppImage
```

## Installation Instructions for End Users

Include these instructions in your distribution:

### Linux Users

1. Download the AppImage file
2. Make it executable: `chmod +x AudioTranscriptionApp-x86_64.AppImage`
3. Run it: `./AudioTranscriptionApp-x86_64.AppImage`

Optional integration:
```bash
# Create a desktop entry
mkdir -p ~/.local/share/applications/
cp path/to/audio_transcription_app.desktop ~/.local/share/applications/
```

### Windows Users

1. Download the .exe file
2. If using the installer:
   - Run the installer and follow the prompts
3. If using the standalone .exe:
   - Extract the zip file (if provided in a zip)
   - Run audio_transcription_app.exe
   
Note: You might need to approve Windows SmartScreen warnings since the app is not signed with a certificate.

### First Run Setup for Both Platforms

On first run, users will need:

1. A HuggingFace account and token for full functionality
2. Internet access to download the models
3. Environment setup:
   - Either create a .env file with `HF_TOKEN=your_token_here`
   - Or set the environment variable temporarily:
     - Linux: `export HF_TOKEN=your_token_here`
     - Windows: `SET HF_TOKEN=your_token_here`

## Advanced: Continuous Integration

For automated builds, set up a GitHub Actions workflow to:
1. Build the application for both platforms on each release
2. Run tests
3. Create and upload artifacts

Example workflow file (.github/workflows/build.yml) is included in the repository.

---

Good luck building and distributing your Audio Transcription Application! If you encounter any issues not covered in this guide, please open an issue on the repository.

