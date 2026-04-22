# Audio Transcription Metadata Schema

This document defines the structured metadata schema for personal audio transcriptions (audiobooks, podcasts, personal recordings) to ensure interoperability between the transcription pipeline and the unified search API.

## Pydantic Schema Definition

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class TranscriptionSegment(BaseModel):
    """A single segment of transcribed text with timing."""
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    text: str = Field(..., description="Transcribed text for this segment")
    speaker_id: Optional[str] = Field(None, description="Identifier for the speaker")
    probability: float = Field(..., description="Confidence score of the transcription")

class ChapterMarker(BaseModel):
    """Identified chapter or logical section in the audio."""
    start: float
    end: float
    title: str
    summary: Optional[str] = None

class AudioTranscriptionMetadata(BaseModel):
    """Top-level metadata for an audio transcription file."""
    file_id: str = Field(..., description="Unique identifier for the source audio file")
    title: str
    author_artist: Optional[str] = None
    transcribed_at: datetime = Field(default_factory=datetime.utcnow)
    model_used: str = Field(..., description="e.g., 'distil-large-v3'")
    language: str = Field("en", description="ISO 639-1 language code")
    duration_seconds: float
    segments: List[TranscriptionSegment]
    chapters: List[ChapterMarker] = []
    tags: List[str] = []
    full_text: str = Field(..., description="Complete concatenated transcript for indexing")

```

## Integration with Unified Search

When indexing audio transcriptions into the Vector DB or BM25 index:

1.  **Chunks**: Long transcripts should be chunked by chapters or fixed time intervals (e.g., 5 minutes) with overlapping windows.
2.  **Metadata Fields**:
    *   `source_type`: `audio`
    *   `title`: The name of the audiobook or podcast episode.
    *   `timestamp`: The start time of the specific chunk in the audio file.
    *   `url`: Local path or internal server link to the audio file (e.g., `nfs://nas/audio/podcasts/episode1.mp3#t=300`).

## Extraction Logic

1.  **Speaker ID**: Use a diarization model (like `pyannote-audio`) as a post-processing step if multiple speakers are detected.
2.  **Chapters**: If the source file doesn't have metadata chapters, use an LLM to identify topic transitions from the text segments.

- Last reviewed: 2025-05-15
- Confidence: high

## Sources / references
- [OpenAI Whisper Segment Schema](https://github.com/openai/whisper)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
