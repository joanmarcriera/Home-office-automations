# Playbook: Offline Transcription Pipeline

## What it is
The Offline Transcription Pipeline is a privacy-first workflow for converting audio files into structured text and tasks without sending data to cloud services. It integrates [faster-whisper](../tools/process_understanding/faster-whisper.md) for local speech-to-text, [Paperless-ngx](../services/paperless-ngx.md) for archiving, [Obsidian](../tools/ai_knowledge/obsidian.md) for notes, and [Vikunja](../services/vikunja.md) for task management.

## What problem it solves
It solves the "Leaky Audio" problem where sensitive recordings (meetings, medical notes, personal thoughts) are often sent to cloud providers (like OpenAI or Google) for transcription. Specifically, it addresses:
- **Privacy at the Source**: Audio never leaves the local machine.
- **Agentic Integration**: Automatically extracts tasks from voice notes using local LLMs (e.g., Llama 4, Gemma 3, DeepSeek-V4, and Qwen 3.8).
- **Searchable Archives**: Makes hours of audio searchable via indexed transcripts.
- **Latency Independence**: No need for a high-speed connection to upload large audio files.

## Where it fits in the stack
**Category**: Playbook / Information Processing. It acts as the **ingestion and normalization** layer for voice-based data, feeding the `docs/tools/ai_knowledge/` (Knowledge) and `docs/services/` (Storage/Task) layers.

## Typical use cases
- **Voice-to-Task Workflow**: Recording a quick memo on a phone and having it appear as a task in Vikunja minutes later.
- **Meeting Archival**: Transcribing local video conferences and storing the text in Paperless-ngx for full-text search.
- **Private Journaling**: Converting daily voice journals into Obsidian Markdown files.
- **Podcast/Media Ingestion**: Transcribing downloaded media to create local knowledge bases.

## Strengths
- **Superior Accuracy**: `faster-whisper` provides near-SOTA accuracy on local hardware.
- **End-to-End Privacy**: 100% offline from recording to task creation.
- **Durable Metadata**: Includes timestamps, speaker diarization (optional), and confidence scores.
- **Highly Automatable**: Can be triggered by folder watches or n8n webhooks.

## Limitations
- **GPU Intensive**: Requires a decent GPU (e.g., NVIDIA or Apple Silicon) for faster-than-real-time performance.
- **Large Models**: The `large-v3` model requires ~5GB of VRAM/RAM.
- **Diarization Complexity**: Accurately identifying multiple speakers is more complex to set up offline.
- **Initial Configuration**: Requires wiring together several distinct tools (Whisper, n8n, databases).

## When to use it
- For transcribing sensitive or private conversations.
- When you want to automate the extraction of actions from your own voice notes.
- In offline environments where cloud transcription is unavailable.

## When not to use it
- For low-sensitivity, public audio where the speed and convenience of cloud APIs are prioritized.
- If you lack the hardware to run Whisper models efficiently.

## Getting started

### 1. Install Transcription Engine
Deploy [faster-whisper](../tools/process_understanding/faster-whisper.md) via Docker or Python:
```bash
pip install faster-whisper
```

### 2. Configure n8n Ingestion
Create an [n8n](../services/n8n.md) workflow that:
1. Watches a directory (or accepts a webhook) for new `.mp3` or `.wav` files.
2. Calls the local `faster-whisper` API or CLI.
3. Passes the transcript to a local LLM ([Ollama](../services/ollama.md)) for summarization and task extraction.

### 3. Route to Storage
Configure the workflow to:
- POST the transcript and original audio to [Paperless-ngx](../services/paperless-ngx.md).
- Create tasks in [Vikunja](../services/vikunja.md) for any items identified by the LLM.

## CLI examples

### 1. Basic Transcription (faster-whisper)
```bash
whisper-ctranslate2 meeting_audio.mp3 --model large-v3 --output_format txt
```

### 2. Monitoring Transcription Jobs
```bash
# Example if using a task queue like Celery or BullMQ
tasks list --queue transcription
```

### 3. Importing Transcript to Paperless-ngx
```bash
curl -H "Authorization: Token your_token" -F "document=@transcript.txt" -F "title=Meeting Notes" http://paperless.local/api/documents/post_document/
```

## API examples

### Python: Automated Pipeline Script with Pydantic v2 Schema Validation
The following production script utilizes **Pydantic v2** validation to process, structure, and check transcripts and extracted tasks before inserting them into task management and document stores.

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class TaskItem(BaseModel):
    title: str = Field(..., min_length=3, description="Parsed task summary.")
    priority: int = Field(default=3, ge=1, le=5, description="Priority from 1 (high) to 5 (low).")
    due_date: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$", description="Optional YYYY-MM-DD due date.")

class AudioSegment(BaseModel):
    start: float = Field(..., ge=0.0)
    end: float = Field(..., ge=0.0)
    text: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("end")
    @classmethod
    def check_timestamps(cls, v: float, info) -> float:
        # Pydantic v2 validation logic
        start = info.data.get("start")
        if start is not None and v < start:
            raise ValueError("End timestamp must be greater than or equal to start timestamp.")
        return v

class StructuredTranscript(BaseModel):
    audio_file: str
    transcription_model: str
    text_content: str
    segments: List[AudioSegment]
    extracted_tasks: List[TaskItem]

def process_and_validate_pipeline(raw_json_input: str) -> dict:
    try:
        data = json.loads(raw_json_input)
        # Validate using Pydantic v2
        validated_pipeline = StructuredTranscript.model_validate(data)
        return {
            "status": "VALID",
            "payload": validated_pipeline.model_dump()
        }
    except Exception as e:
        return {
            "status": "INVALID",
            "error": str(e)
        }

if __name__ == "__main__":
    # Sample input from a local faster-whisper + Ollama (Gemma 3) extraction
    sample_pipeline_output = """
    {
      "audio_file": "/data/memos/recording_2026-11-20.mp3",
      "transcription_model": "faster-whisper-large-v3",
      "text_content": "We need to fix the leaking pipe in the server room and check database locks by next Friday.",
      "segments": [
        {"start": 0.0, "end": 4.5, "text": "We need to fix the leaking pipe in the server room", "confidence": 0.98},
        {"start": 4.5, "end": 9.2, "text": "and check database locks by next Friday.", "confidence": 0.95}
      ],
      "extracted_tasks": [
        {"title": "Fix leaking pipe in server room", "priority": 1},
        {"title": "Check database locks", "priority": 2, "due_date": "2026-11-27"}
      ]
    }
    """
    result = process_and_validate_pipeline(sample_pipeline_output)
    print("Pipeline Validation Result:\n", json.dumps(result, indent=2))
```

## Related tools / concepts
- [faster-whisper](../tools/process_understanding/faster-whisper.md) — The transcription engine.
- [Whisper](../services/whisper.md) — Original OpenAI model.
- [Ollama](../services/ollama.md) — For extracting tasks from text.
- [Vikunja](../services/vikunja.md) — Local task management.
- [Paperless-ngx](../services/paperless-ngx.md) — Document archival.
- [n8n](../services/n8n.md) — Workflow automation.
- [Audio Transcription Research](../knowledge_base/audio-transcription-research.md) — Background research.
- [Voice-to-Task Research](../knowledge_base/voice-to-task-research.md) — Specialized patterns.

## Sources / References
- [faster-whisper GitHub Repository](https://github.com/SYSTRAN/faster-whisper)
- [Vikunja API Documentation](https://vikunja.io/docs/api/)
- [Paperless-ngx API Reference](https://docs.paperless-ngx.com/api/)
- [OpenAI Whisper Model Card](https://github.com/openai/whisper)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
