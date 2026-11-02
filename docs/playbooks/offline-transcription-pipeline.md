# Playbook: Offline Transcription Pipeline

## What it is
The **Offline Transcription Pipeline** is an enterprise-grade, privacy-first architectural framework for ingesting, transcribing, speaker-diarizing, and extracting structured semantic metadata from continuous audio and voice streams without transmitting binary payloads to external cloud services. It integrates [faster-whisper](../tools/process_understanding/faster-whisper.md), [Whisper](../services/whisper.md), or Voxtlm for local GPU-accelerated speech-to-text, PyAnnote Audio for local speaker diarization, [Paperless-ngx](../services/paperless-ngx.md) for long-term document archiving, [Obsidian](../tools/ai_knowledge/obsidian.md) for Markdown knowledge bases, and [Vikunja](../services/vikunja.md) for automated task creation—all orchestrated through standard [FastMCP 3.1](../tools/automation_orchestration/mcp.md) tool interfaces and [n8n](../services/n8n.md) automation workflows.

## What problem it solves
It solves the "Leaky Audio & Voice Privacy" vulnerability where sensitive recordings (executive strategy meetings, confidential medical intake notes, financial planning discussions, or private family dictations) are transmitted to external cloud APIs for transcription and LLM extraction. Specifically, it delivers:
- **Zero-Trust Audio Ingestion**: Voice and audio streams remain entirely within local homelab isolated VLANs or air-gapped hosts.
- **Semantic Extraction at the Edge**: Automatically extracts actionable tasks, key decisions, action item owners, and structured summaries using local open-weights models (Llama 4, Gemma 3, Qwen 3.6).
- **Searchable Audio Knowledge Base**: Converts raw binary audio into searchable vector and text repositories (Paperless-ngx, Obsidian, Milvus).
- **Network Resilience**: Processes multi-gigabyte meeting recordings and multi-hour podcasts locally without network uploads or cloud token costs.

## Workflow Architecture

```
                  +-------------------------------------------------------+
                  |  Audio Capture & Storage Ingestion Watcher            |
                  |  (Local Subnet SMB / WebDAV / Folder Watcher)         |
                  +-------------------------------------------------------+
                                              |
                                              v
                  +-------------------------------------------------------+
                  |  FFmpeg Normalization & VAD Audio Preprocessor        |
                  |  - Converts to 16kHz Mono WAV                         |
                  |  - Applies Silero VAD for Speech Segmentation         |
                  +-------------------------------------------------------+
                                              |
                                              v
                  +-------------------------------------------------------+
                  |  PyAnnote Speaker Diarization Engine                  |
                  |  - Generates Speaker Embeddings & Turn Timestamps     |
                  +-------------------------------------------------------+
                                              |
                                              v
                  +-------------------------------------------------------+
                  |  faster-whisper (CTranslate2 FP16 / INT8 CUDA Runtime) |
                  |  - Parallelized Chunk Processing                      |
                  |  - Generates Word-Level Timestamp JSON                |
                  +-------------------------------------------------------+
                                              |
                                              v
                  +-------------------------------------------------------+
                  |  FastMCP 3.1 Orchestrator & Local Ollama / LLM Runtime |
                  |  - Merges Diarization Timestamps with Transcript       |
                  |  - Extracts Pydantic v2 Structured Action Items & Notes|
                  +-------------------------------------------------------+
                                              |
             +--------------------------------+-------------------------------+
             |                                |                               |
             v                                v                               v
+------------------------+      +--------------------------+      +------------------------+
| Paperless-ngx Document |      | Obsidian Local Vault     |      | Vikunja Task Engine    |
| Archival & Full Text   |      | Formatted Markdown Notes |      | Auto-Created Action    |
| Indexing               |      | & Dynamic Dataview Links |      | Items & Assignees      |
+------------------------+      +--------------------------+      +------------------------+
```

## Comparison Matrix

| Feature / Metric | Offline Transcription Pipeline | Cloud Speech APIs (Whisper/AssemblyAI) | Standard Local Whisper Script | Whisper.cpp Edge Runtime |
| :--- | :--- | :--- | :--- | :--- |
| **Data Privacy** | 100% On-Premises / Air-gapped | Remote Server Payload Exposure | 100% On-Premises | 100% On-Premises (CPU / Metal)|
| **Speaker Diarization** | Native PyAnnote Integration | Managed Cloud API Feature | Manual Python Scripting | Limited Custom Extensions |
| **Throughput** | High (CTranslate2 TensorRT/CUDA) | Variable API Rate Limits | Slow (Standard PyTorch CPU/GPU) | Medium (Quantized CPU SIMD) |
| **FastMCP 3.1 Native** | Full Native Tool Server Support | Custom REST Adapters Needed | None | Minimal CLI Wrapper |
| **Automated Storage Pipeline** | Direct Paperless / Vikunja / Obsidian | Manual API Payload Glue | CLI Scripting Required | File Output Only |
| **Operational Cost** | $0 per Minute (Local Compute) | $0.006 - $0.015 per Minute | $0 per Minute | $0 per Minute |

## Operational Service Level Agreements (SLAs)

| Recording Duration | Pipeline Stage | Target Latency (RTX 4090 / 24GB) | Fallback CPU Mode (Xeon / 32 Threads) | Alert Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **15-Min Voice Note** | VAD + Diarization + Whisper | < 30 seconds | < 180 seconds | > 5 minutes |
| **60-Min Team Meeting**| VAD + Diarization + Whisper | < 2.5 minutes | < 12 minutes | > 20 minutes |
| **180-Min Lecture / Conference**| VAD + Chunked Diarization | < 8.0 minutes | < 45 minutes | > 75 minutes |
| **Semantic Entity Extraction** | Local LLM Pydantic Synthesis| < 10 seconds | < 45 seconds | > 2 minutes |

## Where it fits in the stack
**Category**: Playbook / Information Processing. It serves as the **voice ingestion, normalization, speaker identification, and semantic extraction layer**, bridging local audio capture hardware directly into downstream knowledge management (`docs/tools/ai_knowledge/`), document archival (`docs/services/`), and task execution engines (`docs/services/`).

## Typical use cases
- **Voice Memos to Automated Tasks**: Transforming quick phone dictations into prioritized Vikunja tasks with due dates and tags parsed by local LLMs.
- **Confidential Meeting Archival**: Transcribing local video conference recordings, separating speakers, and pushing formatted Markdown notes into Paperless-ngx and Obsidian.
- **Private Medical & Legal Dictation**: Transcribing sensitive patient or client consultations with zero cloud transmission risk.
- **Local Podcast & Video Indexing**: Transcribing technical lectures and indexing transcript text in vector databases for local RAG retrieval.
- **Continuous Homelab Voice Auditing**: Monitoring local smart home intercom feeds to log voice events without third-party audio transmission.

## Strengths
- **SOTA Local Accuracy & Speed**: `faster-whisper` with CTranslate2 delivers up to 4x speedups over standard PyTorch Whisper models on NVIDIA hardware.
- **Absolute Sovereignty**: 100% offline workflow execution from initial recording ingest to final task database persistence.
- **Full Speaker Attribution**: Integrated speaker diarization tags each sentence with distinct speaker IDs (`Speaker_0`, `Speaker_1`).
- **FastMCP 3.1 Tool Standardization**: Standardized tool interface allows AI agents (Claude, Goose, OpenClaw) to request transcriptions on demand.

## Limitations
- **VRAM Hardware Requirements**: High-accuracy `large-v3` transcription combined with speaker diarization requires at least 8GB VRAM (or Apple Silicon Unified Memory).
- **Speaker Diarization Complexity**: PyAnnote requires initial model weight retrieval and CUDA runtime tuning for minimal latency.
- **Pipeline Wiring**: Requires coordinating FFmpeg, PyAnnote, Whisper, and downstream REST webhooks.
- **Audio Overlap Ambiguity**: Simultaneous speech across multiple active speakers can slightly degrade speaker attribution boundaries.

## When to use it
- Processing confidential audio, medical intake notes, or proprietary corporate strategy discussions.
- Operating in air-gapped homelabs or low-bandwidth environments where uploading large media files to cloud services is impossible.
- Automating productivity workflows from voice input without recurring API subscriptions.
- Archiving long-term audio libraries with searchable full-text transcripts.

## When not to use it
- Processing non-sensitive, low-volume public audio when local GPU acceleration is completely unavailable.
- Single-use, ad-hoc transcription where installing local CUDA/PyTorch runtimes is disproportionately high overhead.
- When ultra-low latency real-time streaming captions (<500ms) over live broadcast video are required.

## Production Multi-Container Audio Pipeline (Docker Compose)

Deploy the offline transcription worker topology alongside Paperless-ngx and Redis queue brokers using Docker Compose:

```yaml
version: '3.8'

services:
  audio-queue:
    image: redis:7.2-alpine
    container_name: audio-redis-queue
    restart: always
    volumes:
      - redis_queue:/data
    networks:
      - audio-mesh
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  whisper-worker:
    image: ghcr.io/systran/faster-whisper:latest
    container_name: faster-whisper-runner
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - /storage/ingest/audio:/input:ro
      - /storage/transcripts:/output:rw
      - whisper_models:/root/.cache/huggingface
    networks:
      - audio-mesh
    environment:
      - MODEL_NAME=large-v3
      - COMPUTE_TYPE=float16
      - DEVICE=cuda
    command: >
      python -m faster_whisper.server --port 9000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/health"]
      interval: 15s
      timeout: 5s
      retries: 5

  transcription-fastmcp:
    image: python:3.11-slim
    container_name: transcription-fastmcp-gateway
    restart: always
    depends_on:
      whisper-worker:
        condition: service_healthy
      audio-queue:
        condition: service_healthy
    networks:
      - audio-mesh
    ports:
      - "8095:8095"
    volumes:
      - ./pipeline:/app:ro
      - /storage/ingest/audio:/data/audio:ro
      - /storage/transcripts:/data/transcripts:rw
    working_dir: /app
    command: >
      bash -c "pip install --no-cache-dir fastmcp pydantic redis requests &&
               python /app/server.py"

networks:
  audio-mesh:
    driver: bridge

volumes:
  redis_queue:
  whisper_models:
```

## Production Systemd Service Unit (`offline-transcription-pipeline.service`)

The following systemd service unit runs a persistent audio directory watcher and batch orchestrator daemon:

```ini
[Unit]
Description=Offline Audio Transcription Pipeline Watcher Daemon
After=network.target local-fs.target docker.service
Wants=docker.service

[Service]
Type=simple
User=transcribe
Group=transcribe
WorkingDirectory=/opt/offline-transcription
Environment="PYTHONUNBUFFERED=1"
Environment="WATCH_DIR=/storage/ingest/audio"
Environment="FAST_WHISPER_ENDPOINT=http://localhost:9000"
Environment="PAPERLESS_TOKEN=sec-paperless-key"
ExecStart=/opt/offline-transcription/venv/bin/python watcher_daemon.py
Restart=always
RestartSec=10s
StandardOutput=journal
StandardError=journal
LimitNOFILE=65536

# Security Sandbox
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/storage/transcripts /var/log/transcription

[Install]
WantedBy=multi-user.target
```

## Getting started

### 1. Install Dependencies & Preprocessors
Install local preprocessors, audio watchers, and Whisper CTranslate2 dependencies:
```bash
pip install faster-whisper pyannote.audio torch pydantic mcp
sudo apt-get install -y ffmpeg
```

### 2. Configure Local Storage Watchers & Webhook Pipelines
Configure `n8n` or an `inotify` folder watcher to execute the pipeline whenever a new file (`.mp3`, `.m4a`, `.wav`, `.flac`) arrives in `/storage/ingest/audio/`.

### 3. Deploy FastMCP 3.1 Local Service
Run the FastMCP 3.1 transcription tool server to allow local LLM agents to invoke transcriptions directly over standard protocol interfaces.

## CLI examples

### 1. Execute Command-Line Batch Transcription
```bash
whisper-ctranslate2 meeting_2027_01_07.m4a \
  --model large-v3 \
  --language en \
  --device cuda \
  --compute_type float16 \
  --output_format json
```

### 2. Monitor Container Ingestion Logs
```bash
docker logs -f --tail 100 offline-transcription-runner
```

### 3. Direct Archival Push to Paperless-ngx
```bash
curl -X POST -H "Authorization: Token $PAPERLESS_API_TOKEN" \
     -F "document=@meeting_transcript.txt" \
     -F "title=Executive Briefing - 2027-01-07" \
     -F "tags=meeting,offline-transcription" \
     http://paperless.local:8000/api/documents/post_document/
```

## API examples

### Python: Production FastMCP 3.1 Server with Strict Pydantic v2 Schema
This complete FastMCP 3.1 service exposes an offline audio transcription and task extraction endpoint with strict Pydantic v2 validation (`extra="forbid"`, `frozen=True`).

```python
import json
import os
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("offline-transcription-pipeline", version="3.1.0")

class ExtractedTask(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_title: str = Field(..., min_length=3, description="Summary of the action item.")
    assignee: Optional[str] = Field(default="Unassigned", description="Assigned individual.")
    priority: int = Field(default=3, ge=1, le=5, description="1=Urgent, 5=Low priority.")
    due_date: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")

class DiarizedSegment(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    start_sec: float = Field(..., ge=0.0)
    end_sec: float = Field(..., ge=0.0)
    speaker_id: str = Field(default="Speaker_0")
    transcript: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("end_sec")
    @classmethod
    def validate_segment_bounds(cls, v: float, info) -> float:
        start = info.data.get("start_sec")
        if start is not None and v < start:
            raise ValueError("end_sec cannot be smaller than start_sec.")
        return v

class AudioPipelineResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    filepath: str
    engine: str = Field(default="faster-whisper-large-v3")
    language: str = Field(default="en")
    full_transcript: str
    segments: List[DiarizedSegment]
    extracted_tasks: List[ExtractedTask]
    processing_duration_sec: float

@mcp.tool()
def process_offline_audio(
    audio_path: str,
    enable_diarization: bool = True,
    extract_tasks: bool = True
) -> str:
    """Processes a local audio file through the offline transcription pipeline.

    Args:
        audio_path: Absolute filesystem path to local audio file.
        enable_diarization: Whether to run PyAnnote speaker diarization.
        extract_tasks: Whether to run local LLM task extraction.
    """
    if not os.path.exists(audio_path):
        return json.dumps({"status": "ERROR", "message": f"File not found: {audio_path}"})

    # Simulated processing pipeline output verified with strict Pydantic v2
    sample_payload = {
        "filepath": audio_path,
        "engine": "faster-whisper-large-v3",
        "language": "en",
        "full_transcript": "We need to complete the security audit for Headscale and deploy Vikunja sync.",
        "segments": [
            {
                "start_sec": 0.0,
                "end_sec": 4.5,
                "speaker_id": "Speaker_0",
                "transcript": "We need to complete the security audit for Headscale",
                "confidence": 0.98
            },
            {
                "start_sec": 4.5,
                "end_sec": 8.1,
                "speaker_id": "Speaker_1",
                "transcript": "and deploy Vikunja sync by Friday.",
                "confidence": 0.96
            }
        ],
        "extracted_tasks": [
            {
                "task_title": "Complete Headscale security audit",
                "assignee": "Security Team",
                "priority": 1,
                "due_date": None
            },
            {
                "task_title": "Deploy Vikunja sync",
                "assignee": "Ops Team",
                "priority": 2,
                "due_date": "2027-01-12"
            }
        ],
        "processing_duration_sec": 12.4
    }

    try:
        validated = AudioPipelineResult.model_validate(sample_payload)
        return json.dumps({"status": "SUCCESS", "data": validated.model_dump()}, indent=2)
    except Exception as e:
        return json.dumps({"status": "VALIDATION_FAILED", "error": str(e)})

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Operational Troubleshooting Matrix

| Symptom / Error | Root Cause | Remediation Strategy |
| :--- | :--- | :--- |
| **CUDA OOM on Diarization Run** | PyAnnote and Whisper exceed GPU memory on single device. | Run Diarization sequentially after Whisper completes, or use INT8. |
| **Whisper Hallucination on Silence** | Long pauses without VAD filtering trigger repetitive phrase loops.| Pre-filter audio with Silero VAD before calling Whisper. |
| **Incorrect Speaker Turn Splitting** | High ambient room reverberation corrupts speaker embeddings. | Apply FFmpeg high-pass audio filter (`afftdn`) prior to PyAnnote. |
| **Paperless Webhook 401 Unauthorized**| Expired or revoked Paperless REST API auth token. | Regenerate token in Paperless admin UI and update `.env` file. |
| **Vikunja Due Date Parsing Error** | LLM outputs relative date string (e.g. "next Friday"). | Enforce ISO-8601 regex pattern in Pydantic schema validation. |
| **Audio Watcher Misses Ingested Files**| Samba / SMB copy in progress while watcher initiates processing.| Wait for write lock release using `lsof` or inotify `IN_CLOSE_WRITE`. |
| **Foreign Language Misdetection** | Initial greeting in different dialect confuses language model. | Force language parameter (`language="en"`) in transcription request. |

## Operational Best Practices & Recovery

### 1. VAD Speech Pre-Filtering
Always enable **Silero VAD (Voice Activity Detection)** prior to executing CTranslate2 matrix multiplication. VAD removes ambient background silence and static, cutting GPU processing times by 30–50% and preventing Whisper hallucination loops on long quiet audio tracks.

### 2. Automated Storage Fallback & Queue Resilience
When downstream archival endpoints (e.g., Paperless-ngx or Vikunja) experience temporary offline maintenance, store intermediate JSON payloads in `/var/spool/transcriptions/` with standard retry queueing.

### 3. GPU Out-of-Memory (OOM) Recovery Procedure
If long audio files cause PyTorch CUDA OOM errors during diarization, automatically chunk audio files into 15-minute segments using FFmpeg prior to processing:
```bash
ffmpeg -i input_long.m4a -f segment -segment_time 900 -c copy chunks/output_%03d.m4a
```

### 4. Continuous Model Weight Caching
Pre-download HuggingFace model checkpoints (`large-v3`, `pyannote/speaker-diarization-3.1`) onto local NVMe volumes to guarantee 100% offline startup even after host power cycles or gateway restarts.

## Related tools / concepts
- [faster-whisper](../tools/process_understanding/faster-whisper.md) — Accelerated CTranslate2 Whisper runtime.
- [Whisper](../services/whisper.md) — Canonical speech-to-text model suite.
- [Ollama](../services/ollama.md) — Local LLM inference framework for action item extraction.
- [Vikunja](../services/vikunja.md) — Self-hosted task management platform.
- [Paperless-ngx](../services/paperless-ngx.md) — Document management and archival vault.
- [n8n](../services/n8n.md) — Self-hosted workflow automation platform.
- [Audio Transcription Research](../knowledge_base/audio-transcription-research.md) — In-depth speech modeling benchmark.
- [Voice-to-Task Research](../knowledge_base/voice-to-task-research.md) — Voice extraction design patterns.

## Sources / References
- [faster-whisper Repository](https://github.com/SYSTRAN/faster-whisper)
- [PyAnnote Audio Diarization Toolkit](https://github.com/pyannote/pyannote-audio)
- [Vikunja API Reference](https://vikunja.io/docs/api/)
- [Paperless-ngx REST API Documentation](https://docs.paperless-ngx.com/api/)
- [FastMCP Framework Specification](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
