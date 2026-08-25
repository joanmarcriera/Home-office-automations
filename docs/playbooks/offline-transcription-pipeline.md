# Playbook: Offline Transcription Pipeline

## What it is
The Offline Transcription Pipeline is an enterprise-grade, privacy-first architecture for ingesting, transcribing, and extracting semantic tasks from audio and voice streams without sending data to external cloud services. It integrates [faster-whisper](../tools/process_understanding/faster-whisper.md), [Whisper](../services/whisper.md), or Voxtlm for local high-throughput speech-to-text, [Paperless-ngx](../services/paperless-ngx.md) for document archiving, [Obsidian](../tools/ai_knowledge/obsidian.md) for Markdown notes, and [Vikunja](../services/vikunja.md) for automated task creation, orchestrated via [FastMCP 3.1](../tools/automation_orchestration/mcp.md) and [n8n](../services/n8n.md).

## What problem it solves
It solves the "Leaky Audio & Voice Privacy" problem where sensitive voice recordings (meeting audio, personal memos, medical dictation, or financial notes) are exposed to cloud providers during speech recognition. Specifically, it provides:
- **Zero-Trust Audio Ingestion**: Voice and audio streams are processed entirely within the local homelab subnet or air-gapped host.
- **Semantic Extraction at the Edge**: Automatically extracts structured action items and summaries from voice notes using local LLMs (Llama 4, Gemma 3, Qwen 3.6).
- **Searchable Audio Knowledge Base**: Indexes hours of recorded audio into full-text searchable document repositories (Paperless-ngx, Milvus).
- **Network Independence**: Processes multi-gigabyte audio files locally without reliance on external network upload bandwidth.

## Where it fits in the stack
**Category**: Playbook / Information Processing. It serves as the **voice ingestion, normalization, and semantic extraction layer**, bridging local audio capture devices to downstream knowledge (`docs/tools/ai_knowledge/`) and task (`docs/services/`) management engines.

## Typical use cases
- **Voice Memos to Automated Tasks**: Converting phone audio notes into prioritized Vikunja tasks with due dates automatically parsed by local LLMs.
- **Confidential Meeting Archival**: Transcribing local video conferences and pushing formatted Markdown transcripts to Paperless-ngx and Obsidian.
- **Private Journaling & Dictation**: Structuring personal daily audio journal entries into categorized Obsidian vault pages.
- **Local Podcast & Media Ingestion**: Transcribing technical lectures and audiobooks to enrich local vector database collections.

## Strengths
- **SOTA Local Accuracy**: `faster-whisper` and Voxtlm deliver state-of-the-art transcription accuracy on local GPU acceleration.
- **Absolute Data Sovereignty**: 100% offline workflow execution from initial recording to final task database write.
- **Rich Metadata Extraction**: Generates word-level timestamps, confidence scores, and optional offline speaker diarization.
- **FastMCP 3.1 Orchestration**: Standardized FastMCP tool interfaces for seamless integration into agent pipelines.

## Limitations
- **VRAM / Compute Intensive**: Fast-than-real-time transcription of `large-v3` models requires ~5GB VRAM on Apple Silicon or NVIDIA hardware.
- **Multi-Speaker Diarization Overhead**: Accurate offline speaker separation requires additional compute-heavy diarization models.
- **System Wiring Complexity**: Requires coordinating audio watchers, Whisper models, n8n webhooks, and local vector stores.

## When to use it
- Ingesting confidential audio, medical notes, or proprietary business meetings.
- Operating in air-gapped or low-bandwidth environments where cloud speech-to-text APIs are unavailable.
- Automating personal productivity workflows directly from voice inputs.

## When not to use it
- Low-sensitivity, public audio streams where fast cloud API endpoints are preferred and local GPU hardware is absent.

## Getting started

### 1. Deploy Speech Recognition Engine
Install [faster-whisper](../tools/process_understanding/faster-whisper.md) via Docker or python container:
```bash
pip install faster-whisper
```

### 2. Configure Local n8n / FastMCP Ingestion Workflow
Set up an [n8n](../services/n8n.md) or FastMCP 3.1 workflow to:
1. Watch an ingestion folder for new `.mp3`, `.m4a`, or `.wav` audio files.
2. Trigger the local `faster-whisper` engine for JSON transcript generation.
3. Pass transcript text to a local LLM ([Ollama](../services/ollama.md) with Gemma 3) for task extraction.

### 3. Direct Outputs to Storage & Task Systems
- POST structured transcript text to [Paperless-ngx](../services/paperless-ngx.md).
- Create parsed action items directly in [Vikunja](../services/vikunja.md).

## CLI examples

### 1. Local CLI Transcription Execution
```bash
whisper-ctranslate2 meeting_recording.mp3 --model large-v3 --output_format json
```

### 2. Monitoring Transcription Ingestion Queue
```bash
docker logs -f faster-whisper-server
```

### 3. Pushing Generated Transcript to Paperless-ngx
```bash
curl -X POST -H "Authorization: Token $PAPERLESS_TOKEN" \
     -F "document=@transcript.txt" \
     -F "title=Meeting Recording 2027-01-07" \
     http://localhost:8000/api/documents/post_document/
```

## API examples

### Python: Offline Audio Pipeline Validator & Task Parser (Pydantic v2)
This production script uses **Pydantic v2** validation to process, verify, and validate transcript outputs and extracted task payloads before writing to downstream storage engines.

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class ExtractedTask(BaseModel):
    task_title: str = Field(..., min_length=3, description="Task summary extracted from speech.")
    priority: int = Field(default=3, ge=1, le=5)
    due_date: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")

class TranscriptSegment(BaseModel):
    start_sec: float = Field(..., ge=0.0)
    end_sec: float = Field(..., ge=0.0)
    speaker_id: Optional[str] = Field(default="Speaker_1")
    text: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("end_sec")
    @classmethod
    def validate_timestamps(cls, v: float, info) -> float:
        start = info.data.get("start_sec")
        if start is not None and v < start:
            raise ValueError("end_sec must be greater than or equal to start_sec.")
        return v

class AudioPipelinePayload(BaseModel):
    source_file: str
    engine: str = Field(default="faster-whisper-large-v3")
    full_transcript: str
    segments: List[TranscriptSegment]
    tasks: List[ExtractedTask]

def validate_audio_pipeline(raw_json: str) -> dict:
    try:
        data = json.loads(raw_json)
        payload = AudioPipelinePayload.model_validate(data)
        return {
            "status": "VALID",
            "processed_payload": payload.model_dump()
        }
    except Exception as e:
        return {"status": "INVALID", "error": str(e)}

if __name__ == "__main__":
    sample_json = """
    {
      "source_file": "/storage/audio/memo_2027-01-07.m4a",
      "engine": "faster-whisper-large-v3",
      "full_transcript": "Need to update the backup verification playbook and schedule a server reboot.",
      "segments": [
        {"start_sec": 0.0, "end_sec": 3.2, "speaker_id": "User", "text": "Need to update the backup verification playbook", "confidence": 0.97},
        {"start_sec": 3.2, "end_sec": 6.1, "speaker_id": "User", "text": "and schedule a server reboot.", "confidence": 0.96}
      ],
      "tasks": [
        {"task_title": "Update backup verification playbook", "priority": 1},
        {"task_title": "Schedule server reboot", "priority": 2, "due_date": "2027-01-10"}
      ]
    }
    """
    res = validate_audio_pipeline(sample_json)
    print("Pipeline Validation Output:\n", json.dumps(res, indent=2))
```

## Related tools / concepts
- [faster-whisper](../tools/process_understanding/faster-whisper.md) — Fast CTranslate2 Whisper implementation.
- [Whisper](../services/whisper.md) — Speech recognition engine.
- [Ollama](../services/ollama.md) — Local LLMs for semantic extraction.
- [Vikunja](../services/vikunja.md) — Local task management.
- [Paperless-ngx](../services/paperless-ngx.md) — Document archival service.
- [n8n](../services/n8n.md) — Workflow automation hub.
- [Audio Transcription Research](../knowledge_base/audio-transcription-research.md) — Speech modeling research.
- [Voice-to-Task Research](../knowledge_base/voice-to-task-research.md) — Voice extraction patterns.

## Sources / References
- [faster-whisper Repository](https://github.com/SYSTRAN/faster-whisper)
- [Vikunja API Documentation](https://vikunja.io/docs/api/)
- [Paperless-ngx API Reference](https://docs.paperless-ngx.com/api/)
- [OpenAI Whisper Model Card](https://github.com/openai/whisper)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
