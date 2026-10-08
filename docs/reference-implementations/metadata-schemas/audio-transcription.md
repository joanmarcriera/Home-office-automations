# Audio Transcription Metadata Schema

## What it is
This document defines the structured metadata schema for personal audio transcriptions (audiobooks, podcasts, personal recordings). It specifies how speaker information, timestamps, and text content are organized to ensure interoperability between transcription pipelines and search interfaces.

As of early January 2027, this schema is the baseline for "Audio-to-Knowledge" workflows, enabling frontier agents like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra/Flash**, **DeepSeek-V4**, and **Qwen 3.6 VL** to reason over spoken content with high temporal precision under **FastMCP 3.1**.

## Architecture & System Overview
The audio transcription metadata pipeline transforms raw acoustic waveforms into structured, multi-speaker JSON schemas indexed for semantic search and agentic retrieval.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      AUDIO TRANSCRIPTION PIPELINE ARCHITECTURE                   │
└──────────────────────────────────────────────────────────────────────────────────┘

   Raw Audio Ingestion             AI Ingest & Diarization          Structured Knowledge
 ┌─────────────────────┐          ┌──────────────────────────┐      ┌────────────────────┐
 │ - MP3 / WAV / FLAC  │─────────>│ - Whisper / Gemini Flash │─────>│ - Pydantic v2 JSON │
 │ - Podcasts / Memos  │          │ - PyAnnote Diarization   │      │ - Vector DB Index  │
 └─────────────────────┘          └──────────────────────────┘      └────────────────────┘
                                               │                              │
                                               ▼                              ▼
                                  ┌──────────────────────────┐      ┌────────────────────┐
                                  │ Chaptering (GPT-5.6 / Qwen)     │ FastMCP 3.1 Server │
                                  └──────────────────────────┘      └────────────────────┘
                                                                              │
                                                                              ▼
                                                                    ┌────────────────────┐
                                                                    │ Agentic Search Tool│
                                                                    └────────────────────┘
```

## What problem it solves
Raw transcription output from various models (Whisper, Fish Audio, etc.) often lacks a consistent structure for speaker diarization, chapter markers, and confidence scores. This schema provides a standardized format that allows the [Unified Search API](../../../scripts/unified_search.py) to index and query audio content as effectively as text-based documents, preventing the "information silo" effect for audio data.

## Where it fits in the stack
This schema belongs to the **Data Contract and Metadata Layer**. It bridges the gap between the **AI Service Layer** (Whisper/Ollama) and the **Knowledge Retrieval Layer** (Vector DBs), ensuring that transcribed audio becomes a first-class citizen in the homelab knowledge base.

## Typical use cases
- **Indexing Podcasts**: Converting downloaded MP3s into searchable text with correct attribution to different speakers.
- **Archiving Meetings**: Storing personal voice memos or recorded calls with high-precision timestamps for quick playback of specific segments.
- **Audiobook Enrichment**: Creating a searchable index of local audiobooks, allowing for keyword search across hundreds of hours of audio.
- **Agentic Search**: An agent can use a FastMCP tool to query the audio transcription database using natural language, retrieving specific segments based on meaning.

## Comparison Matrix

| Dimension | Raw Whisper Output | PyAnnote Output | Audio Transcription Metadata Schema |
| :--- | :--- | :--- | :--- |
| **Speaker Diarization** | Basic / Single Speaker | Speaker BBoxes Only | Integrated Multi-Speaker Attribution |
| **Temporal Alignment** | Word/Segment Timestamps | Time Ranges | Precise Segment & Chapter Alignment |
| **Agentic Accessibility** | Text Block | Raw Matrix | FastMCP 3.1 Native Query Tool |
| **Schema Validation** | None | Custom JSON | Pydantic v2 Strict Model Enforced |
| **Vector DB Indexing** | Text Chunks | No Text | Multi-modal Metadata Aware Chunks |

## Strengths
- **Granular Timing**: Segment-level timestamps allow for deep-linking into audio files (e.g., `#t=300`).
- **Speaker Aware**: Native support for speaker IDs enables filtering searches by specific participants.
- **Confidence Tracking**: Probability scores help identify segments that may require manual correction or human-in-the-loop review.
- **FastMCP Native**: Designed to be served via Model Context Protocol FastMCP 3.1 for seamless multi-agent interaction.

## Limitations
- **Processing Overhead**: Generating high-fidelity metadata (especially speaker diarization) significantly increases transcription time.
- **Storage Size**: JSON metadata for long audio files can become quite large due to the high density of segments.
- **Model Drift**: Extraction of chapters using LLMs (like GPT-5.6) may vary slightly between runs if temperature is not zero.

## When to use it
- When building a local RAG (Retrieval-Augmented Generation) system over audio collections.
- When you need to provide a UI that allows users to "jump to" specific words in a long audio recording.
- For legal or administrative recordings where attribution (who said what) is critical.

## When not to use it
- For real-time, transient transcriptions where metadata persistence is not required.
- If only the raw text is needed without any timing or speaker context.
- For extremely short clips (under 5 seconds) where overhead outweighs metadata value.

## Getting started

### 1. Model Selection
Ensure you are using a model capable of producing segment-level timestamps. **Whisper v3**, **Faster-Whisper**, or **Gemini 4.0 Flash** are recommended.

### 2. Implementation logic
When indexing audio transcriptions into the Vector DB or BM25 index:
- **Chunks**: Long transcripts should be chunked by chapters or fixed time intervals (e.g., 5 minutes) with overlapping windows using **Claude 5.6** or **GPT-5.6** for high-quality summarization.
- **Extraction**: Use a diarization model (like `pyannote-audio` v3.3+) as a post-processing step if multiple speakers are detected.

## CLI examples
Use the reference implementation to generate and manage audio metadata.

```bash
# Transcribe an MP3 file and generate schema-compliant JSON
python3 scripts/transcribe_audio.py /path/to/audio.mp3 --output metadata.json --model distil-large-v3

# Index the generated metadata into the local vector store
python3 scripts/unified_search.py --action index --file metadata.json --type audio

# Query the audio collection via CLI
python3 scripts/unified_search.py --query "Where did we discuss the budget?" --filter "source_type=audio"
```

## API examples
The schema is implemented using Pydantic in [transcribe_audio.py](../../../scripts/transcribe_audio.py).

### Pydantic Schema Definition (Pydantic v2 Compliant)
```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class TranscriptionSegment(BaseModel):
    """A single segment of transcribed text with timing under FastMCP 3.1 schemas."""
    model_config = ConfigDict(extra="forbid")

    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    text: str = Field(..., description="Transcribed text for this segment")
    speaker_id: Optional[str] = Field(None, description="Identifier for the speaker")
    probability: float = Field(..., description="Confidence score of the transcription")

    @field_validator('probability')
    @classmethod
    def validate_probability(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError('Probability must be between 0.0 and 1.0')
        return v

class ChapterMarker(BaseModel):
    """Identified chapter or logical section in the audio."""
    model_config = ConfigDict(extra="forbid")

    start: float
    end: float
    title: str
    summary: Optional[str] = None

class AudioTranscriptionMetadata(BaseModel):
    """Top-level metadata for an audio transcription file."""
    model_config = ConfigDict(extra="forbid")

    file_id: str = Field(..., description="Unique identifier for the source audio file")
    title: str
    author_artist: Optional[str] = None
    transcribed_at: datetime = Field(default_factory=datetime.utcnow)
    model_used: str = Field(..., description="e.g., 'distil-large-v3' or 'gemini-4.0-flash'")
    language: str = Field("en", description="ISO 639-1 language code")
    duration_seconds: float
    segments: List[TranscriptionSegment]
    chapters: List[ChapterMarker] = []
    tags: List[str] = []
    full_text: str = Field(..., description="Complete concatenated transcript for indexing")
```

### Schema Instantiation & Validation Example
```python
import json

sample_payload = """
{
  "file_id": "aud-10928a",
  "title": "Homelab Sprint Planning January 2027",
  "author_artist": "Jules & User",
  "transcribed_at": "2027-01-07T00:00:00Z",
  "model_used": "gemini-4.0-flash",
  "language": "en",
  "duration_seconds": 120.5,
  "segments": [
    {
      "start": 0.0,
      "end": 12.4,
      "text": "Today we are starting Ralph-loop Batch 545 audits.",
      "speaker_id": "SPEAKER_00",
      "probability": 0.99
    }
  ],
  "chapters": [
    {
      "start": 0.0,
      "end": 12.4,
      "title": "Intro",
      "summary": "Outline of the sprint."
    }
  ],
  "tags": ["homelab", "planning", "january-2027"],
  "full_text": "Today we are starting Ralph-loop Batch 545 audits."
}
"""

metadata = AudioTranscriptionMetadata.model_validate_json(sample_payload)
print(f"Validated transcription of title: {metadata.title} (duration: {metadata.duration_seconds}s)")
```

### FastMCP 3.1 Server Audio Search Tool
Exposes the Audio Transcription Schema via FastMCP 3.1 to enable agents to query spoken content with high temporal accuracy.

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "audio-transcription-search",
    instructions="Provides semantic and timestamped search across indexed audio recordings."
)

class AudioQueryInput(BaseModel):
    query: str = Field(..., description="Natural language search term or topic.")
    speaker_id: Optional[str] = Field(None, description="Optional speaker ID filter (e.g., 'SPEAKER_00').")
    min_confidence: float = Field(0.8, ge=0.0, le=1.0, description="Minimum segment probability threshold.")

@mcp.tool()
async def search_audio_transcripts(input_data: AudioQueryInput) -> List[Dict[str, Any]]:
    """Searches transcribed audio files and returns matching segments with timestamps."""
    # Simulated search engine execution over schema-compliant audio metadata
    matching_segments = [
        {
            "file_id": "aud-10928a",
            "title": "Homelab Sprint Planning January 2027",
            "speaker_id": "SPEAKER_00",
            "start_time": 0.0,
            "end_time": 12.4,
            "matched_text": "Today we are starting Ralph-loop Batch 545 audits.",
            "timestamp_link": "file:///media/audio/aud-10928a.mp3#t=0"
        }
    ]
    return matching_segments

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Troubleshooting
- **Speaker Diarization Alignment**: Ensure audio sampling rates match PyAnnote requirements (16kHz mono recommended) before running speaker separation pipelines.
- **Large Metadata Payload Optimization**: For audio files longer than 2 hours, store individual segment lists in compressed JSON blobs or vector DB payloads to avoid bloating client memory during metadata queries.
- **Timestamp Precision**: Always store timestamps as floating-point seconds relative to the audio start (`0.0`) to allow straightforward playback link generation.

## Related tools / concepts
- [Audio Transcription Research](../../knowledge_base/audio-transcription-research.md) — Baseline research on Whisper and speaker diarization.
- [Whisper Service](../../services/whisper.md) — The primary model used to generate these segments.
- [Ollama](../../services/ollama.md) — Often used for post-transcription chaptering and summarization.
- [Fish Audio](../../tools/ai_knowledge/fish-audio.md) — Alternative models for voice synthesis and transcription.
- [Manuals Schema](manuals.md) — Similar metadata structure for physical document archival.
- [Paperless Tag Taxonomy](../paperless/tag-taxonomy.md) — How transcribed audio is tagged within the broader homelab.
- [Transcription Script](../../../scripts/transcribe_audio.py) — The reference implementation for generating this schema.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — For serving structured audio metadata to agents under FastMCP 3.1.

## Sources / references
- [OpenAI Whisper Segment Schema](https://github.com/openai/whisper)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
