#!/usr/bin/env python3
"""
Audio Transcription App with Speaker Diarization

This script processes audio files (WAV/MP3), transcribes multi-person conversations,
performs basic speaker diarization to identify different speakers,
and outputs the transcription to a Word document with color-coding for each speaker.

Libraries used:
- pydub: For audio processing and manipulation
- SpeechRecognition: For audio transcription
- python-docx: For creating Word documents
"""

import os
import math
import argparse
from typing import List, Tuple

import speech_recognition as sr
from pydub import AudioSegment
# from faster_whisper import WhisperModel
from docx import Document
from docx.shared import RGBColor

#model_size = "distil-medium.en"
#model = WhisperModel(model_size, device="cpu", compute_type="int8")

class AudioProcessor:
    """Handles audio file processing and segmentation."""
    
    def __init__(self, file_path: str):
        """
        Initialize the audio processor.
        
        Args:
            file_path: Path to the audio file.
        """
        self.file_path = file_path
        self.audio = self._load_audio()
        
    def _load_audio(self) -> AudioSegment:
        """
        Load audio file using pydub.
        
        Returns:
            AudioSegment object containing the audio data.
        """
        print(f"Loading audio file: {self.file_path}")
        file_ext = os.path.splitext(self.file_path)[1].lower()
        
        if file_ext == '.mp3':
            return AudioSegment.from_mp3(self.file_path)
        elif file_ext == '.wav':
            return AudioSegment.from_wav(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Use .wav or .mp3")
    
    def split_audio(self, segment_length_ms: int = 10000, 
                    silence_threshold_db: int = -40, 
                    min_silence_len_ms: int = 500) -> List[AudioSegment]:
        """
        Split audio into segments, trying to split at silence for better speaker separation.
        
        Args:
            segment_length_ms: Maximum length of each segment in milliseconds
            silence_threshold_db: The silence threshold in dB
            min_silence_len_ms: Minimum length of silence to be considered a potential split point
            
        Returns:
            List of audio segments.
        """
        print("Splitting audio into segments...")
        
        segments = []
        total_length_ms = len(self.audio)
        
        # If audio is shorter than segment_length_ms, return it as a single segment
        if total_length_ms <= segment_length_ms:
            return [self.audio]
        
        # Calculate how many segments we need
        num_segments = math.ceil(total_length_ms / segment_length_ms)
        
        # Find silent points that could be good splitting points
        silent_points = []
        for i in range(1, num_segments):
            target_point = i * segment_length_ms
            search_start = max(0, target_point - 2000)
            search_end = min(total_length_ms, target_point + 2000)
            
            # Look for silence around the target point
            for j in range(search_start, search_end, 100):
                segment = self.audio[j:j+min_silence_len_ms]
                if segment.dBFS < silence_threshold_db:
                    silent_points.append(j + min_silence_len_ms // 2)
                    break
            else:
                # If no silence found, just use the target point
                silent_points.append(target_point)
        
        # Split the audio at the identified points
        start_point = 0
        for point in silent_points:
            segments.append(self.audio[start_point:point])
            start_point = point
        
        # Add the last segment
        segments.append(self.audio[start_point:])
        
        print(f"Audio split into {len(segments)} segments")
        return segments
    
    def segment_to_wav(self, segment: AudioSegment, temp_path: str) -> str:
        """
        Convert an audio segment to a temporary WAV file for processing with SpeechRecognition.
        
        Args:
            segment: Audio segment to convert
            temp_path: Path to save the temporary WAV file
            
        Returns:
            Path to the temporary WAV file.
        """
        segment.export(temp_path, format="wav")
        return temp_path


class Transcriber:
    """Handles audio transcription and basic speaker diarization."""
    
    def __init__(self, num_speakers: int = 3):
        """
        Initialize the transcriber.
        
        Args:
            num_speakers: Maximum number of speakers to identify.
        """
        self.recognizer = sr.Recognizer()
        self.num_speakers = num_speakers
    
    def transcribe_segment(self, segment_path: str) -> str:
        """
        Transcribe an audio segment using SpeechRecognition.
        
        Args:
            segment_path: Path to the audio segment file.
            
        Returns:
            Transcribed text.
        """
        with sr.AudioFile(segment_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data)
                ##text = self.recognizer.recognize_faster_whisper(audio_data, language="en", model="turbo")
                return text
            except sr.UnknownValueError:
                return "[Inaudible]"
            except sr.RequestError:
                return "[Error: Could not request results from Google Speech Recognition service]"
    
    def identify_speakers(self, segments: List[AudioSegment]) -> List[Tuple[str, int]]:
        """
        Identify speakers using a basic heuristic approach.
        This simulates speaker diarization by assigning speakers based on segment characteristics.
        
        Args:
            segments: List of audio segments.
            
        Returns:
            List of (transcribed_text, speaker_id) tuples.
        """
        print("Performing transcription with speaker identification...")
        results = []
        temp_path = "temp_segment.wav"
        
        # Analyze audio features to group by potential speakers
        # This is a basic approach - real diarization would use more sophisticated techniques
        segment_features = []
        for i, segment in enumerate(segments):
            # Use volume (dBFS) and other properties as simple features
            segment_features.append({
                'index': i,
                'dBFS': segment.dBFS,
                'duration': len(segment),
                'segment': segment
            })
        
        # Sort segments by volume as a simple way to cluster potential speakers
        segment_features.sort(key=lambda x: x['dBFS'])
        
        # Assign speaker IDs (0, 1, 2) based on sorted volume
        # This is a very simple heuristic and won't be accurate for real conversations
        speaker_assignments = {}
        num_segments = len(segment_features)
        
        for i, feature in enumerate(segment_features):
            segment_idx = feature['index']
            # Divide segments into speaker groups based on volume
            speaker_id = min(int(i * self.num_speakers / num_segments), self.num_speakers - 1)
            speaker_assignments[segment_idx] = speaker_id
        
        # Transcribe each segment and assign speaker
        for i, segment in enumerate(segments):
            # Export segment directly to WAV file instead of using a dummy AudioProcessor
            segment.export(temp_path, format="wav")
            
            text = self.transcribe_segment(temp_path)
            speaker_id = speaker_assignments.get(i, 0)
            
            if text and text != "[Inaudible]":
                results.append((text, speaker_id))
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return results


class DocumentCreator:
    """Creates a Word document with color-coded transcription."""
    
    def __init__(self):
        """Initialize the document creator."""
        self.document = Document()
        self.speaker_colors = [
            RGBColor(0, 0, 200),  # Blue
            RGBColor(200, 0, 0),  # Red
            RGBColor(0, 150, 0),  # Green
        ]
    
    def add_transcription(self, transcription_data: List[Tuple[str, int]]):
        """
        Add the transcribed text to the document with color-coding for each speaker.
        
        Args:
            transcription_data: List of (transcribed_text, speaker_id) tuples.
        """
        print("Creating Word document with color-coded speakers...")
        
        # Add a title
        self.document.add_heading('Transcription with Speaker Identification', 0)
        
        # Create a legend for speaker colors
        legend = self.document.add_paragraph('Speakers: ')
        for i in range(len(self.speaker_colors)):
            speaker_run = legend.add_run(f"Speaker {i+1} ")
            speaker_run.font.color.rgb = self.speaker_colors[i]
        
        self.document.add_paragraph()  # Add a blank line
        
        # Add the transcription
        for text, speaker_id in transcription_data:
            speaker_num = speaker_id + 1  # Convert 0-based to 1-based for display
            p = self.document.add_paragraph()
            
            # Add speaker label
            speaker_label = p.add_run(f"Speaker {speaker_num}: ")
            speaker_label.bold = True
            speaker_label.font.color.rgb = self.speaker_colors[speaker_id % len(self.speaker_colors)]
            
            # Add the transcribed text
            text_run = p.add_run(text)
            text_run.font.color.rgb = self.speaker_colors[speaker_id % len(self.speaker_colors)]
    
    def save_document(self, output_path: str):
        """
        Save the document to the specified path.
        
        Args:
            output_path: Path to save the Word document.
        """
        self.document.save(output_path)
        print(f"Transcription saved to {output_path}")


def main():
    """Main function to run the audio transcription app."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Audio Transcription App with Speaker Diarization")
    parser.add_argument("input_file", help="Path to the input audio file (WAV or MP3)")
    parser.add_argument("--output", "-o", default="transcription.docx", 
                        help="Path to the output Word document (default: transcription.docx)")
    parser.add_argument("--speakers", "-s", type=int, default=3, 
                        help="Maximum number of speakers to identify (default: 3)")
    args = parser.parse_args()
    
    # Process the audio file
    try:
        # Step 1: Process the audio file
        processor = AudioProcessor(args.input_file)
        
        # Step 2: Split the audio into segments
        segments = processor.split_audio()
        
        # Step 3: Transcribe the audio with speaker identification
        transcriber = Transcriber(num_speakers=args.speakers)
        transcription_data = transcriber.identify_speakers(segments)
        
        # Step 4: Create the Word document
        doc_creator = DocumentCreator()
        doc_creator.add_transcription(transcription_data)
        doc_creator.save_document(args.output)
        
        print("Transcription complete!")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

