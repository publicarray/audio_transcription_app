# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules, copy_metadata
import os
import subprocess
import sys

block_cipher = None

# Collect all necessary packages
streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all('streamlit')
pyannote_datas, pyannote_binaries, pyannote_hiddenimports = collect_all('pyannote')
whisper_datas, whisper_binaries, whisper_hiddenimports = collect_all('whisper')
pydub_datas, pydub_binaries, pydub_hiddenimports = collect_all('pydub')
docx_datas, docx_binaries, docx_hiddenimports = collect_all('docx')
speech_recognition_datas, speech_recognition_binaries, speech_recognition_hiddenimports = collect_all('speech_recognition')
torch_datas, torch_binaries, torch_hiddenimports = collect_all('torch')
numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')
ctranslate2_datas, ctranslate2_binaries, ctranslate2_hiddenimports = collect_all('ctranslate2')
dotenv_datas, dotenv_binaries, dotenv_hiddenimports = collect_all('dotenv')
lightning_fabric_datas = collect_data_files('lightning_fabric')
speechbrain_datas, speechbrain_binaries, speechbrain_hiddenimports = collect_all('speechbrain')

# Combine all collected data
datas = streamlit_datas + pyannote_datas + whisper_datas + pydub_datas + docx_datas + \
        speech_recognition_datas + torch_datas + numpy_datas + ctranslate2_datas + dotenv_datas + speechbrain_datas + lightning_fabric_datas
datas += copy_metadata('streamlit')

binaries = streamlit_binaries + pyannote_binaries + whisper_binaries + pydub_binaries + docx_binaries + \
           speech_recognition_binaries + torch_binaries + numpy_binaries + ctranslate2_binaries + dotenv_binaries + speechbrain_binaries

hiddenimports = streamlit_hiddenimports + pyannote_hiddenimports + whisper_hiddenimports + pydub_hiddenimports + docx_hiddenimports + \
                speech_recognition_hiddenimports + torch_hiddenimports + numpy_hiddenimports + ctranslate2_hiddenimports + dotenv_hiddenimports + speechbrain_hiddenimports

# Add additional hidden imports that might be missed
hiddenimports += [
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.runtime.caching',
    'engineio.async_drivers.threading',
    'speechbrain',
    'faster_whisper',
    'docx',
    'python-docx',
    'pkg_resources.py2_warn',
    'sklearn.metrics',
    'sklearn.neighbors.typedefs',
    'torch.distributions',
    'scipy.special.cython_special',
    'dotenv',
    'pyannote.audio',
    'pyannote.core',
    'pyannote.pipeline',
    'lightning_fabric.version',
    'pytorch_lightning.utilities.memory',
    'pytorch_lightning.utilities.seed',
    'lightning_fabric.utilities',
    'lightning_fabric.core',
]

# Include any data files needed
added_datas = []

# Check if .env file exists before including it
if os.path.exists('.env'):
    added_datas.append(('.env', '.'))  # Include .env file in the root directory
else:
    print("Note: .env file not found. Proceeding without it.")

# Check if models directory exists before including it
if os.path.exists('models') and os.path.isdir('models'):
    added_datas.append(('models', 'models'))  # Include models directory
else:
    print("Note: 'models' directory not found. Proceeding without it.")

# Include app.py in the same directory as run_app.py
added_datas.append(('app.py', '.'))
added_datas.append(('transcribe.py', '.'))

# Include the icon file
icon_path = 'audio_transcription.png'
if os.path.exists(icon_path):
    added_datas.append((icon_path, '.'))

a = Analysis(
    ['run_app.py'],  # Main script
    pathex=[],
    binaries=binaries,
    datas=datas + added_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='audio_transcription_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path if os.path.exists(icon_path) else None,
)


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='audio_transcription_app',
)

# Create AppImage after PyInstaller build
# Only execute this code when running the actual PyInstaller build, not during analysis
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    pass  # Skip when running from the frozen app
else:
    try:
        # Define paths
        dist_dir = os.path.join(os.getcwd(), 'dist')
        app_dir = os.path.join(dist_dir, 'audio_transcription_app')
        
        # Create AppDir structure if it doesn't exist
        appdir_bin = os.path.join(app_dir, 'usr', 'bin')
        os.makedirs(appdir_bin, exist_ok=True)
        
        # Copy desktop file and icon
        desktop_file = 'audio_transcription_app.desktop'
        if os.path.exists(desktop_file):
            import shutil
            shutil.copy(desktop_file, app_dir)
        else:
            # Create desktop file if it doesn't exist
            with open(os.path.join(app_dir, desktop_file), 'w') as f:
                f.write("""[Desktop Entry]
Name=Audio Transcription App
Exec=audio_transcription_app
Icon=audio_transcription
Type=Application
Categories=Audio;Utility;
""")
        
        # Copy icon to the standard locations
        icon_source = icon_path if os.path.exists(icon_path) else None
        if icon_source:
            # Copy to hicolor icons directory (for proper desktop integration)
            appdir_icons = os.path.join(app_dir, 'usr', 'share', 'icons', 'hicolor', '256x256', 'apps')
            os.makedirs(appdir_icons, exist_ok=True)
            shutil.copy(icon_source, os.path.join(appdir_icons, 'audio_transcription.png'))
            
            # Also copy to AppDir root (needed by AppImageTool)
            shutil.copy(icon_source, os.path.join(app_dir, 'audio_transcription.png'))
            print(f"Icon copied to {os.path.join(app_dir, 'audio_transcription.png')}")
        
        # Create AppRun file
        apprun_path = os.path.join(app_dir, 'AppRun')
        with open(apprun_path, 'w') as f:
            f.write("""#!/bin/bash
# Get the directory where this AppRun file is located
HERE="$(dirname "$(readlink -f "${0}")")"
# Execute the application
exec "${HERE}/audio_transcription_app" "$@"
""")
        # Make AppRun executable
        os.chmod(apprun_path, 0o755)
        
        # Use appimagetool to create AppImage if available
        try:
            # Check if appimagetool is installed
            subprocess.run(['which', 'appimagetool'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Create AppImage
            # Set environment variables
            env = os.environ.copy()
            env['ARCH'] = 'x86_64'
            
            subprocess.run([
                'appimagetool',
                app_dir,
                os.path.join(dist_dir, 'Audio_Transcription_App-' + env['ARCH'] + '.AppImage')
            ], check=True, env=env)
            
            print("AppImage created successfully!")
        except subprocess.CalledProcessError:
            print("appimagetool not found. Please install it to create AppImages.")
            print("You can download it from: https://github.com/AppImage/AppImageKit/releases")
            print("The AppDir structure has been prepared in:", app_dir)
    except Exception as e:
        print(f"Error creating AppImage: {e}")
