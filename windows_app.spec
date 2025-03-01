# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules, copy_metadata
import os
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

# Combine all collected data
datas = streamlit_datas + pyannote_datas + whisper_datas + pydub_datas + docx_datas + \
        speech_recognition_datas + torch_datas + numpy_datas + ctranslate2_datas + dotenv_datas
datas += copy_metadata('streamlit')
binaries = streamlit_binaries + pyannote_binaries + whisper_binaries + pydub_binaries + docx_binaries + \
           speech_recognition_binaries + torch_binaries + numpy_binaries + ctranslate2_binaries + dotenv_binaries
hiddenimports = streamlit_hiddenimports + pyannote_hiddenimports + whisper_hiddenimports + pydub_hiddenimports + docx_hiddenimports + \
                speech_recognition_hiddenimports + torch_hiddenimports + numpy_hiddenimports + ctranslate2_hiddenimports + dotenv_hiddenimports

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

# Console version (shows console window)
a = Analysis(
    ['run_app.py'],
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

pyz_console = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe_console = EXE(
    pyz_console,
    a.scripts,
    [],
    exclude_binaries=True,
    name='audio_transcription_app_console',
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
    icon=icon_path if os.path.exists(icon_path) else 'NONE',
)

# No console version (hides console window)
b = Analysis(
    ['run_app.py'],
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

pyz_windowed = PYZ(
    b.pure, 
    b.zipped_data,
    cipher=block_cipher
)

exe_windowed = EXE(
    pyz_windowed,
    b.scripts,
    [],
    exclude_binaries=True,
    name='audio_transcription_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path if os.path.exists(icon_path) else 'NONE',
)

# Collect everything for the console version
coll_console = COLLECT(
    exe_console,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='audio_transcription_app_console',
)

# Collect everything for the windowed version
coll_windowed = COLLECT(
    exe_windowed,
    b.binaries,
    b.zipfiles,
    b.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='audio_transcription_app',
)

