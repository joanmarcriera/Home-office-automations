#!/usr/bin/env python3
"""
Audio Transcription Pipeline
Transcribes long-form audio (audiobooks, podcasts) using faster-whisper.
Follows the schema in docs/reference-implementations/metadata-schemas/audio-transcription.md
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from typing import List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def model_dump(self):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    def Field(*args, **kwargs): return None

# Schema Definitions
class TranscriptionSegment(BaseModel):
    start: float
    end: float
    text: str
    speaker_id: Optional[str] = None
    probability: float

class ChapterMarker(BaseModel):
    start: float
    end: float
    title: str
    summary: Optional[str] = None

class AudioTranscriptionMetadata(BaseModel):
    file_id: str
    title: str
    author_artist: Optional[str] = None
    transcribed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_used: str
    language: str = "en"
    duration_seconds: float
    segments: List[TranscriptionSegment]
    chapters: List[ChapterMarker] = []
    tags: List[str] = []
    full_text: str

def transcribe_audio(audio_path: str, model_size: str = "distil-large-v3") -> AudioTranscriptionMetadata:
    """
    Mock transcription process using faster-whisper logic.
    """
    print(f"Transcribing {audio_path} using {model_size}...")

    # Mocked results
    filename = os.path.basename(audio_path)
    mock_segments = [
        TranscriptionSegment(start=0.0, end=5.0, text="Welcome to the family podcast.", probability=0.98),
        TranscriptionSegment(start=5.0, end=10.0, text="Today we are talking about our summer trip.", probability=0.95)
    ]

    full_text = " ".join([s.text for s in mock_segments])

    metadata = AudioTranscriptionMetadata(
        file_id=filename,
        title=filename.split('.')[0].replace('_', ' ').title(),
        transcribed_at=datetime.now(timezone.utc),
        model_used=model_size,
        duration_seconds=10.0,
        segments=mock_segments,
        full_text=full_text,
        tags=["podcast", "family"]
    )

    return metadata

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using faster-whisper.")
    parser.add_argument("input", help="Path to audio file.")
    parser.add_argument("--output", help="Path to save metadata JSON.")
    parser.add_argument("--model", default="distil-large-v3", help="Whisper model size to use.")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File {args.input} not found.")
        sys.exit(1)

    metadata = transcribe_audio(args.input, args.model)

    if hasattr(metadata, 'model_dump') and not isinstance(metadata, dict):
        output_data = metadata.model_dump()
    else:
        output_data = metadata.__dict__

    # Handle datetime serialization
    if isinstance(output_data.get('transcribed_at'), datetime):
        output_data['transcribed_at'] = output_data['transcribed_at'].isoformat()

    # Handle segments serialization if they are objects
    if output_data.get('segments') and not isinstance(output_data['segments'][0], dict):
        output_data['segments'] = [s.model_dump() if hasattr(s, 'model_dump') else s.__dict__ for s in output_data['segments']]

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Transcription saved to {args.output}")
    else:
        print(json.dumps(output_data, indent=2))

if __name__ == "__main__":
    main()
