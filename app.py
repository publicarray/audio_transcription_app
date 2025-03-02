#!/usr/bin/env python3
"""
Streamlit GUI for Audio Transcription App

This script provides a user-friendly web interface for the audio transcription functionality,
allowing users to upload audio files, specify parameters, and download transcription results.
"""

import os
import io
import tempfile
import streamlit as st
from audiorecorder import audiorecorder
from docx import Document
from docx.shared import RGBColor
from transcribe import AudioProcessor, Transcriber, DocumentCreator


# Function to convert RGB tuple to hex color string for Streamlit display
def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

# Set page configuration
st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="\U0001F399️",
    layout="wide"
)

def process_audio(temp_file_path, num_speakers, speaker_colors, filename="audio"):
    # Show progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Processing audio file...")
        progress_bar.progress(20)
        
        # Process the audio file
        processor = AudioProcessor(temp_file_path)
        
        status_text.text("Splitting audio into segments...")
        progress_bar.progress(40)
        
        # Split the audio into segments
        segments = processor.split_audio()
        
        status_text.text("Transcribing audio with speaker identification...")
        progress_bar.progress(60)
        
        # Transcribe the audio with speaker identification
        transcriber = Transcriber(num_speakers=num_speakers)
        transcription_data = transcriber.identify_speakers(segments)
        
        status_text.text("Creating document with transcription...")
        progress_bar.progress(80)
        
        # Create the Word document
        doc_creator = DocumentCreator()
        
        # Convert our RGB tuples to RGBColor objects for the Word document
        # This is where we handle the transition between our tuples and docx's RGBColor
        doc_creator.speaker_colors = [
            RGBColor(rgb[0], rgb[1], rgb[2]) for rgb in speaker_colors[:num_speakers]
        ]
        
        doc_creator.add_transcription(transcription_data)
        
        # Save the document to a BytesIO object
        docx_file = io.BytesIO()
        doc_creator.document.save(docx_file)
        docx_file.seek(0)
        
        progress_bar.progress(100)
        status_text.text("Transcription complete!")
        
        # Display the transcription
        st.header("Transcription Results")
        
        # Create a legend for speaker colors
        st.subheader("Speakers")
        
        # Display speaker legend with colors
        cols = st.columns(min(num_speakers, 5))
        for i in range(min(num_speakers, len(speaker_colors))):
            # Use our utility function to convert RGB tuple to hex for Streamlit
            hex_color = rgb_to_hex(speaker_colors[i])
            cols[i % 5].markdown(
                f"<span style='color:{hex_color};font-weight:bold;'>Speaker {i+1}</span>", 
                unsafe_allow_html=True
            )
        
        # Display transcription text
        st.subheader("Text")
        for text, speaker_id, start_time, end_time in transcription_data:
            # Convert RGB tuple to hex for Streamlit display
            hex_color = rgb_to_hex(speaker_colors[speaker_id % len(speaker_colors)])
            st.markdown(
                f"<span style='color:{hex_color};font-weight:bold;'>Speaker {speaker_id + 1}:</span> {text}", 
                unsafe_allow_html=True
            )
        
        # Download button for the transcription
        st.download_button(
            label="Download Transcription (DOCX)",
            data=docx_file,
            file_name=f"{filename}_transcription.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        # Clean up
        os.unlink(temp_file_path)
        
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        progress_bar.progress(0)
        status_text.text("Transcription failed")

def main():
    """Main function to run the Streamlit app."""
    
    # Define speaker colors as RGB tuples for Streamlit
    # We use tuples instead of RGBColor objects to avoid compatibility issues
    # RGBColor objects will only be created when needed for the Word document
    speaker_colors = [
        (46, 134, 193),   # Blue
        (231, 76, 60),    # Red
        (39, 174, 96),    # Green
        (142, 68, 173),   # Purple
        (243, 156, 18),   # Orange
        (41, 128, 185),   # Light Blue
        (192, 57, 43),    # Dark Red
        (22, 160, 133),   # Teal
        (155, 89, 182),   # Lavender
        (230, 126, 34)    # Dark Orange
    ]
    
    
    
    # App header
    st.title("🎙️ Audio Transcription App")
    st.markdown("""
    This app transcribes audio files and identifies different speakers in the conversation.
    Upload an audio file (WAV or MP3), specify the number of speakers, and get a color-coded transcription.
    """)
    
    # Sidebar for app settings
    with st.sidebar:
        st.header("Settings")
        num_speakers = st.slider(
            "Number of Speakers", 
            min_value=1, 
            max_value=10, 
            value=3,
            help="Specify the maximum number of speakers to identify in the audio"
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This app uses:
        - SpeechRecognition for transcription
        - Basic speaker diarization
        - Word document formatting
        """)
    
    # Create a tab-based interface
    tab1, tab2 = st.tabs(["Upload File", "Record Audio"])
    
    # File upload tab
    with tab1:
        st.header("Upload Audio File")
        uploaded_file = st.file_uploader(
            "Choose a WAV or MP3 file", 
            type=["wav", "mp3"],
            help="Upload an audio file for transcription"
        )
    
    # Audio recording tab
    with tab2:
        st.header("Record Audio")
        st.markdown("Click the button below to start recording your audio. Click again to stop recording.")
        
        # Add audio recorder component
        audio_bytes = audiorecorder("Click to record", "Recording...")
        
        # If audio has been recorded (non-empty)
        if len(audio_bytes) > 0:
            st.success("Audio recording successful!")
            
            # Create an audio player for the recorded audio
            st.audio(audio_bytes.export().read())
            
            # Display recording information
            st.info("Recording ready for transcription.")
            
            # Create a button to process the recording
            if st.button("Transcribe Recording", type="primary", key="transcribe_recording"):
                # Save recorded audio to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    audio_bytes.export(tmp_file.name, format="wav")
                    temp_file_path = tmp_file.name
                    
                # Set dummy file details for display
                file_details = {
                    "Filename": "recorded_audio.wav",
                    "Source": "Audio recording",
                    "Duration": f"{len(audio_bytes)/1000:.2f} seconds"
                }
                
                # Display file details
                with st.expander("Recording Details", expanded=True):
                    for key, value in file_details.items():
                        st.write(f"**{key}:** {value}")
                
                # Process the recorded audio similarly to uploaded files
                process_audio(temp_file_path, num_speakers, speaker_colors)

    # Process the uploaded file
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' successfully uploaded!")
        
        # File info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1e6:.2f} MB",
            "File type": uploaded_file.type
        }
        
        # Display file details
        with st.expander("File Details", expanded=True):
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
        
        # Transcription section
        st.header("Transcription")
        
        # Start transcription button
        if st.button("Start Transcription", type="primary"):
            # Save uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_file_path = tmp_file.name
            
            # Process the audio file using our refactored function
            filename = os.path.splitext(uploaded_file.name)[0]
            process_audio(temp_file_path, num_speakers, speaker_colors, filename)
    
    elif len(audio_bytes) == 0:
        # When no file is uploaded or recorded, show a placeholder
        st.info("Please upload an audio file or record audio to start the transcription process.")
        
        # Example section
        with st.expander("How to use this app"):
            st.markdown("""
            ## Option 1: Upload a file
            1. Select the 'Upload File' tab
            2. Upload an audio file (WAV or MP3) using the file uploader
            3. Set the number of speakers using the slider in the sidebar
            4. Click the 'Start Transcription' button
            5. View the results and download the transcription as a DOCX file
            
            ## Option 2: Record Audio
            1. Select the 'Record Audio' tab
            2. Click the 'Click to record' button to start recording
            3. Click the button again to stop recording when finished
            4. Set the number of speakers using the slider in the sidebar
            5. Click the 'Transcribe Recording' button
            6. View the results and download the transcription as a DOCX file
            """)

def check_environment():
    """Check if the application is running in the correct Poetry environment."""
    try:
        import pkg_resources
        
        # Check for required packages
        required_packages = ['streamlit', 'pydub', 'SpeechRecognition', 'python-docx']
        missing_packages = []
        
        for package in required_packages:
            try:
                pkg_resources.get_distribution(package)
            except pkg_resources.DistributionNotFound:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"Warning: The following packages are missing: {', '.join(missing_packages)}")
            print("Please install them using Poetry: poetry add " + " ".join(missing_packages))
            return False
            
        return True
    except Exception as e:
        print(f"Error checking environment: {e}")
        return False


if __name__ == "__main__":
    # Check if we're running in the correct Poetry environment
    env_check = check_environment()
    if env_check:
        print("Environment check passed - all required packages are installed.")
    
    # Run the Streamlit app
    main()

