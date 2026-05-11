# Audio Transcription Metadata Schema

## What it is
This document defines the structured metadata schema for personal audio transcriptions (audiobooks, podcasts, personal recordings). It specifies how speaker information, timestamps, and text content are organized to ensure interoperability between transcription pipelines and search interfaces.

## What problem it solves
Raw transcription output from various models (Whisper, Fish Audio, etc.) often lacks a consistent structure for speaker diarization, chapter markers, and confidence scores. This schema provides a standardized format that allows the [Unified Search API](../../scripts/unified_search.py) to index and query audio content as effectively as text-based documents.

## Where it fits in the stack
This schema belongs to the **data contract and metadata layer**. It bridges the gap between the **AI service layer** (Whisper/Ollama) and the **knowledge retrieval layer** (Vector DBs), ensuring that transcribed audio becomes a first-class citizen in the homelab knowledge base.

## Typical use cases
- **Indexing Podcasts**: Converting downloaded MP3s into searchable text with correct attribution to different speakers.
- **Archiving Meetings**: Storing personal voice memos or recorded calls with high-precision timestamps for quick playback of specific segments.
- **Audiobook Enrichment**: Creating a searchable index of local audiobooks, allowing for keyword search across hundreds of hours of audio.

## Strengths
- **Granular Timing**: Segment-level timestamps allow for deep-linking into audio files.
- **Speaker Aware**: Native support for speaker IDs enables filtering searches by specific participants.
- **Confidence Tracking**: Probability scores help identify segments that may require manual correction or human-in-the-loop review.

## Limitations
- **Processing Overhead**: Generating high-fidelity metadata (especially speaker diarization) significantly increases transcription time.
- **Storage Size**: JSON metadata for long audio files can become quite large due to the high density of segments.

## When to use it
- When building a local RAG (Retrieval-Augmented Generation) system over audio collections.
- When you need to provide a UI that allows users to "jump to" specific words in a long audio recording.

## When not to use it
- For real-time, transient transcriptions where metadata persistence is not required.
- If only the raw text is needed without any timing or speaker context.

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

## Related tools / concepts
- [Audio Transcription Research](../../knowledge_base/audio-transcription-research.md) — Baseline research on Whisper and speaker diarization.
- [Whisper Service](../../services/whisper.md) — The primary model used to generate these segments.
- [Ollama](../../services/ollama.md) — Often used for post-transcription chaptering and summarization.
- [Fish Audio](../../tools/ai_knowledge/fish-audio.md) — Alternative models for voice synthesis and transcription.
- [Manuals Schema](manuals.md) — Similar metadata structure for physical document archival.
- [Paperless Tag Taxonomy](../paperless/tag-taxonomy.md) — How transcribed audio is tagged within the broader homelab.
- [Transcription Script](../../scripts/transcribe_audio.py) — The reference implementation for generating this schema.

## Sources / references
- [OpenAI Whisper Segment Schema](https://github.com/openai/whisper)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
