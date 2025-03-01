#!/usr/bin/env python3
"""
Test Audio Generator for Multi-Speaker Transcription App

This script generates a sample audio file with simulated multiple speakers
for testing the transcription application. It creates a WAV file with
different speech characteristics to simulate different speakers.
"""

import os
import tempfile
from pydub import AudioSegment
from pydub.effects import speedup, low_pass_filter
import subprocess
import sys

# Check if we need to install gTTS
try:
    from gtts import gTTS
except ImportError:
    print("Installing gTTS library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gtts"])
    from gtts import gTTS

def create_audio_segment(text, speaker_id=1):
    """
    Create an audio segment with the given text using gTTS.
    Apply effects based on speaker_id to simulate different speakers.
    
    Args:
        text (str): The text to convert to speech
        speaker_id (int): Speaker identifier (1, 2, or 3)
        
    Returns:
        AudioSegment: The processed audio segment
    """
    # Create a temporary file to store the mp3 from gTTS
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_path = temp_file.name
    
    # Generate speech with gTTS
    # Different languages/accents help simulate different speakers
    if speaker_id == 1:
        tts = gTTS(text=text, lang='en', tld='com')  # US English
    elif speaker_id == 2:
        tts = gTTS(text=text, lang='en', tld='co.uk')  # UK English
    else:
        tts = gTTS(text=text, lang='en', tld='com.au')  # Australian English
    
    tts.save(temp_path)
    
    # Load the mp3 file
    segment = AudioSegment.from_mp3(temp_path)
    
    # Apply different effects based on speaker_id
    if speaker_id == 1:
        # Speaker 1: Normal voice (slight bass boost)
        segment = low_pass_filter(segment, 1800)
    elif speaker_id == 2:
        # Speaker 2: Faster, higher pitch
        segment = speedup(segment, 1.2)
    else:
        # Speaker 3: Slower, lower pitch
        segment = segment.set_frame_rate(int(segment.frame_rate * 0.85))
    
    # Normalize volume
    segment = segment.normalize()
    
    # Delete the temporary file
    os.unlink(temp_path)
    
    return segment

def generate_test_audio(output_path="sample_conversation.wav"):
    """
    Generate a test audio file with multiple simulated speakers
    
    Args:
        output_path (str): Path where the output WAV file will be saved
    """
    # Create conversation segments
    print("Generating speech for Speaker 1...")
    speaker1_segment1 = create_audio_segment(
        "Hello everyone, I think we should discuss the project timeline first.", 
        speaker_id=1
    )
    
    print("Generating speech for Speaker 2...")
    speaker2_segment1 = create_audio_segment(
        "I agree. We're running behind schedule on the development phase.", 
        speaker_id=2
    )
    
    print("Generating speech for Speaker 3...")
    speaker3_segment1 = create_audio_segment(
        "Yes, and we also need to address the budget concerns raised last week.", 
        speaker_id=3
    )
    
    print("Generating speech for Speaker 1...")
    speaker1_segment2 = create_audio_segment(
        "That's a good point. Let's review our current spending and make adjustments.", 
        speaker_id=1
    )
    
    print("Generating speech for Speaker 2...")
    speaker2_segment2 = create_audio_segment(
        "I've prepared some figures for us to review. The main issue is in the testing phase.", 
        speaker_id=2
    )
    
    # Add 500ms silence between speakers
    silence = AudioSegment.silent(duration=500)
    
    # Combine all segments
    print("Combining audio segments...")
    conversation = (
        speaker1_segment1 + silence +
        speaker2_segment1 + silence +
        speaker3_segment1 + silence +
        speaker1_segment2 + silence +
        speaker2_segment2
    )
    
    # Export as WAV
    print(f"Exporting audio to {output_path}...")
    conversation.export(output_path, format="wav")
    print(f"Sample audio file generated successfully: {output_path}")
    print(f"File duration: {len(conversation)/1000:.2f} seconds")
    
    # Return file information
    return {
        "path": output_path,
        "duration_seconds": len(conversation)/1000,
        "speakers": 3,
        "format": "wav"
    }

if __name__ == "__main__":
    # Define the output path (current directory)
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_conversation.wav")
    
    # Generate the test audio
    file_info = generate_test_audio(output_file)
    
    # Print usage instructions
    print("\nTo transcribe this file using the transcription app, run:")
    print(f"python transcribe.py {output_file}")

