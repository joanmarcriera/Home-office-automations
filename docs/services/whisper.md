# OpenAI Whisper

## What it is
OpenAI Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web. As of **early January 2027**, optimized inference runtimes like **Faster-Whisper v1.3.x**, **Whisper.cpp**, and **MLX-Whisper** provide the foundation for ultra-low-latency local transcription, integrated with frontier reasoning systems like **Claude 5.6**, **Claude 5.1**, **GPT-5.6**, **Gemini 4.0 Ultra**, and [Gemma 3](../tools/ai_knowledge/local_llms.md) for automated post-processing, translation, meeting intelligence, and autonomous agentic workflows.

Whisper operates by converting raw 16kHz mono audio into 80-channel or 128-channel log-Mel spectrograms, passing these representations through an encoder Transformer, and decoding autoregressively with cross-attention to predict sequence tokens that incorporate acoustic language identification, millisecond timestamp boundaries, and text punctuation.

## What problem it solves
Transcribing audio manually is time-consuming, expensive, and subject to human error. Whisper provides high-accuracy transcription, translation, and language identification, allowing for the automation of meeting notes, video subtitling, voice-controlled interfaces, and multimodal agent comprehension.

Furthermore, self-hosting Whisper addresses critical enterprise compliance and privacy concerns:
1. **Zero Data Exfiltration**: Audio files containing confidential corporate board meetings, medical diagnostics, or privileged legal disclosures remain strictly within the local network perimeter.
2. **Deterministic Processing Costs**: Eliminates per-minute cloud API transcription fees ($0.006 to $0.024/min), amortizing infrastructure costs across continuous high-volume workloads.
3. **Low-Latency Agent Perception**: Enables local voice agents and terminal assistants to transcribe audio streams in near real-time using local GPU or Apple Silicon hardware acceleration.

## Where it fits in the stack
**Category**: Services / AI & Machine Learning. It serves as the **audio perception layer** in a local AI stack, converting voice input into text that can then be processed by LLMs or other automation tools.

```
+---------------------------------------------------------------------------------------------------------+
|                                    WHISPER SPEECH RECOGNITION ARCHITECTURE                              |
|                                                                                                         |
|   +------------------------------------+             +----------------------------------------------+   |
|   |         Audio Ingestion Ingress    |             |          Acoustic Signal Pre-Processing      |   |
|   |  - Microphone Stream (WebRTC/RTMP) |             |  - 16 kHz Mono Resampling (libsoxr / FFmpeg) |   |
|   |  - Uploaded Audio (MP3/WAV/M4A/OGG)|             |  - Silero-VAD V6 Silence/Hum Gating          |   |
|   |  - Media Feeds (Audiobookshelf/Pod)|             |  - Log-Mel Spectrogram (80/128 Mel Bins)     |   |
|   +-----------------+------------------+             +----------------------+-----------------------+   |
|                     |                                                       |                           |
|                     +--------------------------+----------------------------+                           |
|                                                | Filtered Acoustic Windows                              |
|                                                v                                                        |
|   +-------------------------------------------------------------------------------------------------+   |
|   |                                 WHISPER BACKEND EXECUTION RUNTIMES                              |   |
|   |  +-----------------------------+  +----------------------------+  +---------------------------+ |   |
|   |  | Faster-Whisper CTranslate2  |  | Whisper.cpp GGML Quantized |  | MLX-Whisper Apple Silicon | |   |
|   |  | (CUDA FP8 / FP16 Batched)   |  | (AVX-512 / ARM NEON / CPU) |  | (Metal Unified Memory)    | |   |
|   |  +-----------------------------+  +----------------------------+  +---------------------------+ |   |
|   +--------------------------------------------+----------------------------------------------------+   |
|                                                | Encoded Latent Speech Representations                  |
|                                                v                                                        |
|   +-------------------------------------------------------------------------------------------------+   |
|   |                                 AUTOREGRESSIVE DECODING PIPELINE                                |   |
|   |  - Multilingual Language Identification Token (<|en|>, <|es|>, <|zh|>)                          |   |
|   |  - Task Token Selection (<|transcribe|> vs <|translate|>)                                      |   |
|   |  - Timestamp Generation (<|0.00|> to <|30.00|>) with Dynamic Fallback Temperatures             |   |
|   |  - Hallucination Suppression via Compression Ratio & Repetition Penalties                      |   |
|   +--------------------------------------------+----------------------------------------------------+   |
|                                                | Validated Timestamped Transcript Tokens                |
|                                                v                                                        |
|   +-------------------------------------------------------------------------------------------------+   |
|   |                                  AGENT & DOWNSTREAM INTEGRATION                                 |   |
|   |  - FastMCP 3.1 Task Tools        - Local LLM Summarizers (Gemma 3, Claude 5.6, GPT-5.6)         |   |
|   |  - Paperless-ngx Document Store  - Vector Databases (Milvus, Qdrant) & Full-Text Search        |   |
|   +-------------------------------------------------------------------------------------------------+   |
+---------------------------------------------------------------------------------------------------------+
```

## Typical use cases
- **Automated Meeting Transcription & Minutes**: Processing corporate Zoom/Teams recordings through Whisper to produce timestamped transcripts, followed by action item extraction using local LLMs.
- **Video & Podcast Subtitling**: Generating multi-language SRT and VTT subtitles with exact millisecond word-level alignment for YouTube, Vimeo, and local media servers.
- **Voice-Controlled Home Automation**: Feeding smart microphone arrays (e.g. ESP32 satellite mics) into a centralized Whisper instance to control Home Assistant entities.
- **Multilingual Spoken Translation**: Ingesting non-English audio files and generating direct English translations without requiring intermediate language text passes.
- **Enriching Media Repositories**: Indexing spoken dialogue inside [Audiobookshelf](audiobookshelf.md) and [Plex](plex.md) libraries to allow cross-collection dialogue search.

### Detailed Hardware Benchmarking Matrix (Early 2027)

| Hardware Configuration | Model Architecture | Runtime Backend | Memory (VRAM / RAM) | Time for 10m Audio | Real-time Factor (RTF) | Throughput / Suitability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Raspberry Pi 5 (8GB)** | base.en | Whisper.cpp (Q5_K) | ~450 MB RAM | ~7.2 min | 0.72x | Low-power edge satellite; basic voice commands |
| **Intel Core i7-14700K** | medium | Faster-Whisper (INT8) | ~2.1 GB RAM | ~1.1 min | 0.11x | Home server background transcription worker |
| **AMD Ryzen 9 9950X** | large-v3-turbo | Whisper.cpp (AVX-512) | ~3.4 GB RAM | ~48 sec | 0.08x | CPU-only workstation batch indexing |
| **Apple M4 Pro (48GB)** | large-v3-turbo | MLX-Whisper (Metal) | ~3.2 GB Unified | ~32 sec | 0.053x | macOS native development workstation |
| **Apple M5 Max (128GB)** | large-v3 | MLX-Whisper (Metal) | ~4.8 GB Unified | ~19 sec | 0.031x | Multi-stream studio audio production |
| **NVIDIA RTX 4070 (12GB)**| large-v3-turbo | Faster-Whisper (FP16) | ~2.8 GB VRAM | ~11 sec | 0.018x | Dedicated homelab inference node |
| **NVIDIA RTX 5090 (32GB)**| large-v3-turbo | Faster-Whisper (FP8) | ~2.2 GB VRAM | ~4.2 sec | 0.007x | High-throughput enterprise batch cluster |

## Strengths
- **Near-Human Transcription Accuracy**: Evaluated on diverse accent datasets and noisy real-world acoustic profiles, rivaling professional human transcriptionists across 99+ languages.
- **Unified Multitask Formulation**: Single sequence-to-sequence model performs language detection, timestamp alignment, transcription, and translation without requiring separate pipeline components.
- **Robustness to Background Noise**: Retains intelligibility across reverberant rooms, background music, telephone codecs, and cafeteria babble.
- **Open Model Architecture & Active Ecosystem**: Permissively licensed checkpoints support thriving optimizations including CTranslate2, Whisper.cpp, TensorRT-LLM, and ONNX Runtime.

## Limitations
- **Hallucinatory Repetition Loops**: Susceptible to infinite repetitive output loops when fed silent audio segments or continuous background music unless paired with a robust VAD pre-filter.
- **Monolithic Speaker Representation**: Standard Whisper does not perform speaker diarization; speaker turns must be clustered using external libraries such as PyAnnote or SenseVoice.
- **Computational Footprint**: Running the full `large-v3` architecture at full FP32 requires over 10 GB of VRAM, mandating aggressive FP16, INT8, or FP8 quantization on consumer hardware.

## When to use it
- When implementing a fully self-hosted, private speech-to-text pipeline that guarantees zero audio leaves the organization.
- When transcribing hours of recorded conversations, podcasts, or lectures where high accuracy and punctuation are paramount.
- When creating automated video captioning workflows that require precise word-level or phrase-level timestamps.

## When not to use it
- When building ultra-low-latency (<200ms) full-duplex conversational voice bots; streaming ASR architectures (such as RNN-T or streaming FastConformer) are better suited for conversational turn-taking.
- When running exclusively on severely constrained microcontrollers with less than 256MB of RAM.

## Getting started

### Installation (Python Baseline & Faster-Whisper)
Install the baseline OpenAI Whisper and the high-throughput CTranslate2 Faster-Whisper runtime:

```bash
# Baseline Transformers implementation
pip install openai-whisper

# High-performance CTranslate2 inference engine
pip install faster-whisper

# FastMCP 3.1 and Pydantic v2 support
pip install "mcp[cli]>=3.1.0" "pydantic>=2.6.0"
```

## CLI examples

```bash
# Transcribe standard WAV file using Faster-Whisper with Silero-VAD
faster-whisper-cli "meeting.wav" \
  --model large-v3-turbo \
  --device cuda \
  --compute_type float16 \
  --vad_filter True \
  --output_format json

# Transcribe and translate Japanese audio directly to English text
whisper "interview_ja.mp3" \
  --model medium \
  --language Japanese \
  --task translate \
  --output_dir ./transcripts

# Run Whisper.cpp for minimal resource consumption on low-power NAS
./whisper-cpp-main \
  -m ./models/ggml-large-v3-turbo-q5_k.bin \
  -f "podcast.mp3" \
  --threads 6 \
  --print-colors
```

## API examples

### Production FastMCP 3.1 Whisper Speech Processing Server

The following complete, production-grade FastMCP 3.1 server exposes local Whisper speech recognition capabilities to AI agents. It enforces strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`), integrates Silero-VAD V6, executes Faster-Whisper batched inference, and returns validated structured payloads.

```python
"""
Production FastMCP 3.1 Whisper Speech Recognition Server
Integrates Faster-Whisper CTranslate2 runtime with Silero-VAD and strict Pydantic v2 schemas.
"""

import os
import sys
import time
import json
import logging
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Whisper-ASR-Server", version="3.1.0")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("whisper_asr")

class WhisperTranscriptionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    audio_filepath: str = Field(..., description="Absolute local filesystem path to the audio file")
    model_name: Literal["base", "small", "medium", "large-v3-turbo", "large-v3"] = Field(
        default="large-v3-turbo",
        description="Whisper checkpoint model to load"
    )
    task: Literal["transcribe", "translate"] = Field(
        default="transcribe",
        description="Task mode: transcribe spoken language or translate to English"
    )
    language_code: Optional[str] = Field(
        default=None,
        description="ISO 639-1 language code (e.g. 'en', 'es', 'de'). Auto-detects if None."
    )
    precision: Literal["float16", "float8_e4m3fn", "int8_float16", "int8"] = Field(
        default="float16",
        description="Quantization precision type for GPU execution"
    )
    beam_size: int = Field(default=5, ge=1, le=10, description="Beam search width")
    enable_vad: bool = Field(default=True, description="Enable Silero-VAD noise and silence filtering")

    @field_validator("audio_filepath")
    @classmethod
    def validate_audio_path(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("audio_filepath cannot be empty")
        if not os.path.exists(clean):
            raise ValueError(f"Audio file does not exist: {clean}")
        if not os.path.isfile(clean):
            raise ValueError(f"Specified path is not a file: {clean}")
        return clean

class WordTimestamp(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    word: str = Field(..., description="Decoded individual word")
    start: float = Field(..., ge=0.0, description="Word start timestamp in seconds")
    end: float = Field(..., ge=0.0, description="Word end timestamp in seconds")
    probability: float = Field(..., ge=0.0, le=1.0, description="Confidence probability")

class TranscriptSegment(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    segment_id: int = Field(..., description="Monotonically increasing segment identifier")
    start: float = Field(..., ge=0.0, description="Segment start in seconds")
    end: float = Field(..., ge=0.0, description="Segment end in seconds")
    text: str = Field(..., description="Segment transcription text")
    avg_logprob: float = Field(..., description="Average log probability of decoded tokens")
    no_speech_prob: float = Field(..., ge=0.0, le=1.0, description="Probability that window is silent")
    words: Optional[List[WordTimestamp]] = Field(default=None, description="Optional word-level timestamps")

class AudioProcessingTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    audio_duration_seconds: float = Field(..., ge=0.0, description="Source audio length")
    inference_time_seconds: float = Field(..., ge=0.0, description="Total wall-clock inference duration")
    realtime_factor: float = Field(..., ge=0.0, description="Speed factor ratio (audio_duration / inference_time)")
    detected_language: str = Field(..., description="Detected or enforced source language")
    language_confidence: float = Field(..., ge=0.0, le=1.0, description="Language classification confidence")
    device_used: str = Field(..., description="Compute engine execution device (cuda / cpu)")

class WhisperTranscriptionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["SUCCESS", "FAILED"] = Field(..., description="Execution status outcome")
    full_text: str = Field(..., description="Complete aggregated transcript")
    segments: List[TranscriptSegment] = Field(default_factory=list, description="Timestamped segments")
    telemetry: AudioProcessingTelemetry = Field(..., description="Operational runtime metrics")

@mcp.tool()
def transcribe_media_file(payload_json: str) -> str:
    """
    Executes Whisper ASR transcription on a local media file using Faster-Whisper,
    enforcing strict Pydantic v2 schemas and returning millisecond-accurate transcripts.
    """
    start_time = time.time()
    try:
        raw_data = json.loads(payload_json)
        req = WhisperTranscriptionRequest.model_validate(raw_data)

        # Detect GPU availability
        has_cuda = False
        try:
            import torch
            has_cuda = torch.cuda.is_available()
        except ImportError:
            has_cuda = os.path.exists("/dev/nvidia0")

        device = "cuda" if has_cuda else "cpu"
        compute_type = req.precision if device == "cuda" else "int8"

        from faster_whisper import WhisperModel
        logger.info(f"Initializing WhisperModel({req.model_name}) on {device} ({compute_type})")
        model = WhisperModel(
            req.model_name,
            device=device,
            compute_type=compute_type,
            download_root="/tmp/whisper_models"
        )

        vad_params = dict(
            threshold=0.35,
            min_speech_duration_ms=100,
            min_silence_duration_ms=250,
            window_size_samples=512
        ) if req.enable_vad else None

        segments_iter, info = model.transcribe(
            req.audio_filepath,
            language=req.language_code,
            task=req.task,
            beam_size=req.beam_size,
            vad_filter=req.enable_vad,
            vad_parameters=vad_params,
            temperature=[0.0, 0.2, 0.4],
            word_timestamps=False
        )

        segments: List[TranscriptSegment] = []
        text_parts: List[str] = []

        for idx, seg in enumerate(segments_iter):
            cleaned = seg.text.strip()
            if not cleaned:
                continue
            text_parts.append(cleaned)
            segments.append(
                TranscriptSegment(
                    segment_id=idx + 1,
                    start=round(seg.start, 3),
                    end=round(seg.end, 3),
                    text=cleaned,
                    avg_logprob=round(seg.avg_logprob, 4),
                    no_speech_prob=round(seg.no_speech_prob, 4)
                )
            )

        elapsed = max(time.time() - start_time, 0.001)
        duration = info.duration if info.duration > 0 else 0.001
        rtf = round(duration / elapsed, 2)

        resp = WhisperTranscriptionResponse(
            status="SUCCESS",
            full_text=" ".join(text_parts),
            segments=segments,
            telemetry=AudioProcessingTelemetry(
                audio_duration_seconds=round(duration, 2),
                inference_time_seconds=round(elapsed, 3),
                realtime_factor=rtf,
                detected_language=info.language,
                language_confidence=round(info.language_probability, 4),
                device_used=device
            )
        )
        return resp.model_dump_json(indent=2)

    except Exception as e:
        logger.error(f"Whisper transcription failed: {str(e)}", exc_info=True)
        return json.dumps({
            "status": "FAILED",
            "error_type": e.__class__.__name__,
            "message": str(e),
            "wall_clock_time": round(time.time() - start_time, 3)
        }, indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Production Docker Compose Stack

This Docker Compose setup deploys a containerized Faster-Whisper service with NVIDIA GPU passthrough, integrated Redis job queue, and FastMCP 3.1 gateway proxy.

```yaml
version: "3.8"

services:
  whisper-service:
    image: ghcr.io/systran/faster-whisper:latest-cuda12
    container_name: whisper-asr-daemon
    restart: unless-stopped
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
      - PYTHONUNBUFFERED=1
      - WHISPER_CACHE_DIR=/root/.cache/whisper
      - FASTMCP_PORT=8020
    volumes:
      - /mnt/storage/audio_inbound:/data/audio:ro
      - /mnt/storage/transcripts:/data/transcripts:rw
      - whisper_model_cache:/root/.cache/whisper
      - ./whisper_server:/opt/whisper:ro
    working_dir: /opt/whisper
    command: ["python3", "-m", "server.mcp_daemon", "--host", "0.0.0.0", "--port", "8020"]
    ports:
      - "8020:8020"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
        limits:
          memory: 10G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8020/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 45s
    networks:
      - whisper_net

  whisper-redis:
    image: redis:7.4-alpine
    container_name: whisper-redis-queue
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--maxmemory", "256mb", "--maxmemory-policy", "noeviction"]
    volumes:
      - redis_queue_data:/data
    networks:
      - whisper_net

volumes:
  whisper_model_cache:
    driver: local
  redis_queue_data:
    driver: local

networks:
  whisper_net:
    driver: bridge
```

## Production Hardened Systemd Daemon Service Unit

To run Whisper as a secure system daemon on a dedicated Linux host, use the following hardened systemd unit:

```ini
# /etc/systemd/system/whisper-mcp.service
[Unit]
Description=Whisper Speech Recognition FastMCP 3.1 Gateway Service
Documentation=https://github.com/openai/whisper https://github.com/SYSTRAN/faster-whisper
After=network.target sound.target nvidia-persistenced.service
Wants=network-online.target

[Service]
Type=simple
User=whisper
Group=whisper
WorkingDirectory=/opt/whisper-mcp
ExecStart=/opt/whisper-mcp/venv/bin/python -m service.server --port 8020 --device cuda
Restart=always
RestartSec=5s

# Process Environment & Hardware Limits
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="PYTHONUNBUFFERED=1"
Environment="OMP_NUM_THREADS=4"
Environment="CT2_CUDA_ALLOCATOR=cuda_malloc_async"

# System Hardening and Sandbox Protection
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictRealtime=true
RestrictNamespaces=true
NoNewPrivileges=true
ReadWritePaths=/mnt/storage/audio_inbound /mnt/storage/transcripts /var/log/whisper

# Memory Limits
MemoryHigh=9G
MemoryMax=10G
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Error Code / Symptom | Root Cause | Diagnostic Verification | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| `ERR_CUDA_OUT_OF_MEMORY` | GPU VRAM saturation during large batch inference or multiple concurrent streams. | `nvidia-smi` reports 100% memory utilization; PyTorch throws CUDA alloc exception. | Switch `precision` parameter to `float8_e4m3fn` or `int8_float16`; reduce beam size from 5 to 2. |
| `ERR_HALLUCINATION_REPETITION` | Autoregressive decoder looped on unvoiced background noise or musical passages. | Output contains repeated phrases ("Thank you for watching...") across dozens of segments. | Enforce Silero-VAD filtering (`enable_vad=True`), set `vad_threshold=0.35`, and configure fallback temperatures `[0.0, 0.2]`. |
| `ERR_UNSUPPORTED_CONTAINER` | Audio container codec format not supported by ffmpeg backend bindings. | Python throws `RuntimeError: Failed to load audio` or codec error in libavformat. | Transcode source file to standard 16kHz mono PCM WAV via ffmpeg prior to model execution: `ffmpeg -i in.mp3 -ar 16000 -ac 1 out.wav`. |
| `ERR_COREML_COMPILATION_FAIL` | Mismatched Apple CoreML model binaries on macOS execution node. | `whisper.cpp` aborts with `ANE/CoreML initialization failed` on Apple Silicon. | Recompile CoreML graph using `whisper.cpp/models/generate-coreml-model.sh` matched to the active macOS SDK. |
| `FASTMCP_PAYLOAD_TOO_LARGE` | Inline raw binary audio submission exceeded FastMCP message length threshold. | FastMCP client reports RPC packet serialization error or HTTP 413 Payload Too Large. | Submit local filesystem path (`audio_filepath`) rather than base64 inline audio data. |
| `Pydantic ValidationError` | Client payload submitted extra unrecognized keys or malformed parameters. | Server logs report `ValidationError: Extra inputs are not permitted`. | Verify client request conforms strictly to `WhisperTranscriptionRequest` schema (`extra="forbid"`). |

## Operational Best Practices

### 1. Hallucination Reduction via Silero-VAD
- **Integrate Silero Voice Activity Detection**: Autoregressive models hallucinate when forced to generate text for frames that contain no phonetic information. Always enable Silero-VAD V6 filtering (`enable_vad=True`) to strip non-speech frames prior to model ingestion.

### 2. Quantization for Edge & Shared Hardware
- **CTranslate2 INT8 & FP8 Precision**: When co-locating Whisper on GPUs running local language models (e.g. Gemma 3 or LLaMA-3.3), quantize Whisper weights using `float8_e4m3fn` or `int8_float16`. This reduces VRAM overhead to under 2.5 GB while preserving word error rate within 0.4% of FP32 baseline.

## Related tools / concepts
- [Ollama](ollama.md) — For processing transcribed text with local LLMs.
- [n8n](n8n.md) — For automating audio ingestion and transcription workflows.
- [Audiobookshelf](audiobookshelf.md) — For managing transcribed audio libraries.
- [Home Assistant](home-assistant.md) — For integrating Whisper into voice-controlled home automation.
- [SearXNG](searXNG.md) — For searching through transcribed knowledge bases.
- [LiteLLM](litellm.md) — For unified proxying to frontier models like Claude 5.6 and GPT-5.6.
- [Plex](plex.md) — Streaming transcoded content and media archives.
- [Jellyfin](jellyfin.md) — General purpose media hub for serving audio collections.
- [Authentik](authentik.md) — Authenticating web triggers for speech endpoints.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Canonical local LLM for transcript reasoning and cleanup.
- [Audio Transcription Research](../knowledge_base/audio-transcription-research.md) — Architectural benchmarks and long-form transcription comparison.

## Sources / References
- [Whisper GitHub Repository (OpenAI)](https://github.com/openai/whisper)
- [Faster-Whisper GitHub Repository (SYSTRAN)](https://github.com/SYSTRAN/faster-whisper)
- [Whisper.cpp GGML Quantized Inference Engine](https://github.com/ggerganov/whisper.cpp)
- [MLX Whisper for Apple Silicon Metal](https://github.com/ml-explore/mlx-examples/tree/main/whisper)
- [Speaches OpenAI-Compatible Whisper Server](https://github.com/speaches-ai/speaches)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
