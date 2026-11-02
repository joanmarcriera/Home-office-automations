# OpenAI Whisper

## What it is
OpenAI Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web. As of **early January 2027**, optimizations like **Faster-Whisper v1.3.x/v1.4.x** (CTranslate2) and **Whisper.cpp** provide the foundation for ultra-low-latency local transcription, integrated with frontier models like **Claude 5.6**, **Claude 5.1**, **GPT-5.6**, **Gemini 4.0 Ultra**, and [Gemma 3](../tools/ai_knowledge/local_llms.md) for automated post-processing, translation, and agentic reasoning.

Whisper operates by converting log-mel spectrograms computed from 16kHz mono audio into token sequences via an encoder-decoder Transformer architecture. Contemporary deployments leverage quantized linear layers (FP8, INT8, and Q5_K) and voice activity pre-filtering (Silero-VAD V6) to achieve real-time factors below 0.01x on modern GPUs.

## What problem it solves
Transcribing audio manually is time-consuming and expensive. Whisper provides high-accuracy transcription, translation, and language identification, allowing for the automation of meeting notes, video subtitling, and voice-controlled interfaces. It is particularly notable for its robustness to accents, background noise, and technical language.

Furthermore, self-hosting Whisper addresses privacy and compliance requirements by eliminating the need to transmit sensitive enterprise calls, internal dictation, or homelab voice commands to third-party cloud transcription providers.

## Where it fits in the stack
**Category**: Services / AI & Machine Learning. It serves as the **audio perception layer** in a local AI stack, converting voice input into text that can then be processed by LLMs or other automation tools.

```
+-----------------------------------------------------------------------------------+
|                           AUDIO INGESTION / STREAM LAYER                          |
|             (Microphone Feed, WAV/MP3 Upload, RTMP, WebRTC, Media Server)         |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       VOICE ACTIVITY DETECTION (VAD) LAYER                        |
|                  (Silero-VAD V6, Noise Filter & Trimming Buffer)                  |
|                  - Silence Elimination & Adaptive Thresholding                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        WHISPER SPEECH RECOGNITION ENGINE                          |
|     +-------------------------+   +------------------------------------------+    |
|     | Whisper.cpp / CoreML    |   | Faster-Whisper (CTranslate2 / FP16/FP8)  |    |
|     | (Streaming / CPU / Mac) |   | (GPU Batched Inference, CUDA / TensorRT) |    |
|     +-------------------------+   +------------------------------------------+    |
|                                         |                                         |
|                                         v                                         |
|     +------------------------------------------------------------------------+    |
|     | Decoding Mechanics: Beam Search (k=5) + Temperature Fallback Escalation |    |
|     +------------------------------------------------------------------------+    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                         AGENT & POST-PROCESSING LAYER                             |
|          (FastMCP 3.1 Tools, Gemma 3 / Claude 5.6 Summarization & RAG)            |
+-----------------------------------------------------------------------------------+
```

## Detailed Internal Decoding Mechanics

Whisper executes an autoregressive sequence-to-sequence beam search over 80-channel log-mel acoustic filterbanks. To ensure robust transcription across challenging acoustic environments, modern implementations employ a multi-stage decoding pipeline:

```
[16kHz Audio Frame] ──► [Log-Mel Filterbank (80 or 128 channels)]
                                   │
                                   ▼
                   [Audio Transformer Encoder (Conv1D + Pos)]
                                   │ (Encoder Cross-Attention Representations)
                                   ▼
                   [Autoregressive Transformer Decoder]
                                   │
     ┌─────────────────────────────┴─────────────────────────────┐
     ▼                                                           ▼
[Temperature Fallback Loop]                                 [Hallucination Prevention]
(T=0.0 -> T=0.2 -> T=0.4 -> T=0.8)                           - Repetition Penalty (1.2x)
If avg_logprob < -1.0 or no_speech_prob > 0.6                 - Gating via Silero-VAD V6
Escalate beam sampling entropy                              - Word Timestamp Alignment
```

1. **Acoustic Front-End**: 30-second audio windows are converted to log-mel spectrograms with a 25ms window size and 10ms hop size.
2. **Encoder Stack**: Two 1D convolutional layers downsample the spectrogram by a factor of 2, followed by positional sinusoidal embeddings and pre-activation Transformer blocks.
3. **Autoregressive Decoder**: Prefix tokens dictate task instructions (`<|startoftranscript|>`, `<|en|>`, `<|transcribe|>`, `<|notimestamps|>`).
4. **Heuristic Temperature Fallback**: When decoding confidence falters (measured by compression ratio exceeding 2.4 or average log probability dropping below -1.0), the engine automatically resets and re-evaluates the segment with higher temperature sampling to escape deterministic token traps.

## Typical use cases
- Transcribing recorded meetings or lectures for searchability.
- Generating subtitles for videos in multiple languages.
- Building voice-activated home automation commands.
- Translating foreign language audio into English text.
- Enriching local media libraries (e.g., [Audiobookshelf](audiobookshelf.md)) with full-text search.
- **Hardware-Accelerated Transcription**: Optimized performance across a variety of hardware from Raspberry Pi 5 to NVIDIA RTX 5090.
- **MCP 3.1 Integration**: Whisper services can be exposed as MCP 3.1 tools, allowing autonomous agents to request on-demand transcription of local media files.

### Hardware Benchmarking (Early 2027)

| Hardware | Model Checkpoint | Backend Runtime | Time for 10m Audio | Real-time Factor (RTF) | VRAM / RAM Usage | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Raspberry Pi 5 (8GB) | base.en | Whisper.cpp | ~7.5m | 0.75x | ~650 MB RAM | CPU-only, slow but viable for voice triggers. |
| Intel i7 (14th Gen) | medium | Faster-Whisper | ~1.2m | 0.12x | ~2.1 GB RAM | Optimized with `int8` AVX-512 quantization. |
| Apple M4 Pro / M5 | large-v3 | Whisper.cpp | ~35s | 0.058x | ~4.2 GB Unified | Leveraging CoreML/MLX matrix co-processors. |
| NVIDIA RTX 4070 (12GB) | large-v3 | Faster-Whisper | ~12s | 0.02x | ~4.8 GB VRAM | FP16, batched inference (batch_size=16). |
| NVIDIA RTX 4080 (16GB) | large-v3-turbo | Faster-Whisper | ~8s | 0.013x | ~3.1 GB VRAM | FP8 TensorRT/CTranslate2 execution. |
| NVIDIA RTX 5090 (32GB) | large-v3 | Faster-Whisper | ~5s | 0.008x | ~5.2 GB VRAM | Peak throughput for high-volume enterprise ingestion. |

## Model Checkpoint Comparison Matrix

| Model Checkpoint | Architecture Parameters | Multilingual Support | Relative Speed vs. Large-v3 | English WER | Multilingual WER | Recommended Hardware |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **tiny / tiny.en** | 39M params | 99+ languages (or EN) | ~32x | ~7.5% | ~14.2% | Embedded IoT, ESP32, Pi Zero 2W |
| **base / base.en** | 74M params | 99+ languages (or EN) | ~16x | ~5.8% | ~11.4% | Raspberry Pi 4/5, Home Assistant Yellow |
| **small / small.en**| 244M params | 99+ languages (or EN) | ~6x | ~4.2% | ~8.6% | Standard Mini PCs (Intel N100) |
| **medium / medium.en**| 769M params | 99+ languages (or EN) | ~2.5x | ~2.9% | ~6.1% | CPU Homelab nodes, Mid-tier GPUs (RTX 3060) |
| **large-v3** | 1550M params | 99+ languages | 1.0x (Baseline) | ~1.8% | ~3.5% | Dedicated NVIDIA GPUs (8GB+ VRAM), Mac Studio |
| **large-v3-turbo** | 809M params (4 dec layers)| 99+ languages | ~8x | ~2.1% | ~4.1% | High-efficiency Production Homelab default |
| **distil-large-v3**| 756M params (2 dec layers)| English only | ~6.5x | ~2.0% | N/A | High-throughput English batch ingestion |

## Strengths
- **High Accuracy**: Competes with professional human transcribers in many languages.
- **Multilingual**: Supports transcription in dozens of languages and translation into English.
- **Robustness**: Handles background noise and various accents exceptionally well.
- **Local Execution**: Can be run entirely offline (via Whisper.cpp or Faster-Whisper), ensuring data privacy.
- **Batched Inference**: Faster-Whisper v1.3.x supports optimized batched processing for up to 4x-5x speed increases.

## Limitations
- **Resource Intensive**: Larger models (`large-v3-turbo`) require significant GPU VRAM or CPU power.
- **No Real-time (Native)**: The base Whisper model is designed for batch processing, though optimized versions like Whisper.cpp support streaming.
- **Hallucination**: Can occasionally hallucinate text during long periods of silence or music (partially mitigated by Silero-VAD V6).

## When to use it
- When you need high-quality, private, and free transcription of audio files.
- When building local AI assistants that require voice input.
- For processing legacy audio archives at scale.

## When not to use it
- If you require extremely low-latency, real-time transcription on low-power mobile devices (without using optimized C++ ports).
- If you need a managed service with built-in speaker diarization (Whisper identifies *what* was said, but not always *who* said it).

## Getting started

### Installation (Python)
```bash
pip install openai-whisper
```

### Installation (Faster-Whisper)
Optimized version using CTranslate2.
```bash
pip install faster-whisper
```

### Hello World
1. Install Whisper: `pip install openai-whisper`
2. Run via CLI:
```bash
whisper audio.mp3 --model base
```

## CLI examples

The `whisper` CLI is the simplest way to process audio files.

```bash
# Transcribe a file using the medium model
whisper audio.wav --model medium

# Transcribe and translate a Spanish audio file to English
whisper spanish_audio.mp3 --language Spanish --task translate

# Output transcription in specific formats (txt, vtt, srt, tsv, json)
whisper audio.m4a --output_format srt

# Transcribe via faster-whisper with VAD pre-filtering and FP8 precision
faster-whisper-cli input_podcast.wav \
  --model large-v3-turbo \
  --device cuda \
  --compute_type float8 \
  --vad_filter True \
  --output_format json
```

## API examples

### FastMCP 3.1 Whisper Speech Processing Server Pattern

The following Python script implements a production FastMCP 3.1 server exposing Whisper transcription capabilities to local AI agents with strict Pydantic v2 schemas:

```python
"""
Production FastMCP 3.1 Server for Local Whisper Audio Transcription & Translation.
Enforces strict Pydantic v2 validation and handles both streaming and batched execution.
"""

import os
import time
import json
from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP
from faster_whisper import WhisperModel, BatchedInferencePipeline

mcp = FastMCP(
    "Whisper-ASR-Server",
    version="3.1.0",
    description="FastMCP 3.1 Server for Local Whisper Audio Transcription & Translation"
)

class SegmentInfo(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    start_sec: float = Field(..., ge=0.0, description="Segment start offset in seconds")
    end_sec: float = Field(..., ge=0.0, description="Segment end offset in seconds")
    text: str = Field(..., min_length=1, description="Transcribed audio content")
    avg_logprob: float = Field(..., description="Average token log probability")
    no_speech_prob: float = Field(..., ge=0.0, le=1.0, description="No speech probability estimate")

class ASRRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    audio_path: str = Field(..., description="Absolute local path to the audio file (.wav, .mp3, .m4a)")
    model_size: Literal["base", "medium", "large-v3", "large-v3-turbo"] = Field(
        default="large-v3-turbo",
        description="Whisper model checkpoint name"
    )
    language: Optional[str] = Field(default=None, description="ISO-639-1 language code (auto if null)")
    task: Literal["transcribe", "translate"] = Field(default="transcribe", description="Task mode")
    beam_size: int = Field(default=5, ge=1, le=10, description="Beam search width")
    vad_filter: bool = Field(default=True, description="Enable Silero-VAD filtering")

    @field_validator("audio_path")
    @classmethod
    def validate_file_exists(cls, v: str) -> str:
        clean = v.strip()
        if not clean or not os.path.exists(clean):
            raise ValueError(f"Audio file does not exist at path: {clean}")
        return clean

class ASRResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    audio_file: str = Field(..., description="Processed audio filepath")
    language: str = Field(..., description="Detected or requested language code")
    duration_seconds: float = Field(..., ge=0.0, description="Total media duration in seconds")
    elapsed_time_sec: float = Field(..., ge=0.0, description="Inference runtime in seconds")
    realtime_factor: float = Field(..., ge=0.0, description="RTF processing ratio")
    transcript: str = Field(..., description="Consolidated plain text transcript")
    segments: List[SegmentInfo] = Field(default_factory=list, description="Timestamped segments")

@mcp.tool(description="Transcribe local audio file using GPU-accelerated Faster-Whisper")
def transcribe_audio_file(request_payload: str) -> str:
    """Transcribes local audio and returns timestamped segments validated via Pydantic v2."""
    try:
        data = json.loads(request_payload)
        req = ASRRequest.model_validate(data)

        device = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"

        model = WhisperModel(req.model_size, device=device, compute_type=compute_type)
        start_time = time.time()

        segments_iter, info = model.transcribe(
            audio=req.audio_path,
            language=req.language,
            task=req.task,
            beam_size=req.beam_size,
            vad_filter=req.vad_filter
        )

        segments_list: List[SegmentInfo] = []
        transcript_parts: List[str] = []

        for s in segments_iter:
            txt = s.text.strip()
            if not txt:
                continue
            transcript_parts.append(txt)
            segments_list.append(
                SegmentInfo(
                    start_sec=round(s.start, 3),
                    end_sec=round(s.end, 3),
                    text=txt,
                    avg_logprob=round(s.avg_logprob, 4),
                    no_speech_prob=round(s.no_speech_prob, 4)
                )
            )

        elapsed = time.time() - start_time
        rtf = round(info.duration / elapsed, 2) if elapsed > 0 else 0.0

        result = ASRResult(
            audio_file=req.audio_path,
            language=info.language,
            duration_seconds=round(info.duration, 2),
            elapsed_time_sec=round(elapsed, 2),
            realtime_factor=rtf,
            transcript=" ".join(transcript_parts),
            segments=segments_list
        )
        return result.model_dump_json(indent=2)
    except Exception as exc:
        err = {"status": "ERROR", "message": str(exc)}
        return json.dumps(err, indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Production Docker Compose Stack

To host an enterprise-grade Faster-Whisper transcription server with Silero-VAD pre-filtering and Redis task orchestration:

```yaml
version: "3.9"

services:
  whisper-server:
    image: ghcr.io/systran/faster-whisper:latest-gpu
    container_name: faster-whisper-api
    restart: unless-stopped
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - PYTHONUNBUFFERED=1
      - WHISPER_MODEL=large-v3-turbo
      - WHISPER_COMPUTE_TYPE=float16
    volumes:
      - /opt/homelab/audio/media:/data/media:ro
      - /opt/homelab/audio/outputs:/data/outputs:rw
      - /opt/homelab/cache/huggingface:/root/.cache/huggingface:rw
    ports:
      - "8020:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - whisper-net

  whisper-queue:
    image: redis:7.4-alpine
    container_name: whisper-queue
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--maxmemory", "256mb", "--maxmemory-policy", "noeviction"]
    volumes:
      - /opt/homelab/audio/redis:/data
    networks:
      - whisper-net

networks:
  whisper-net:
    driver: bridge
```

## Production Deployment & Systemd Service Unit
To host the FastMCP 3.1 Whisper Speech Recognition Gateway as a persistent background system daemon, configure the following systemd service unit:

```ini
# /etc/systemd/system/whisper-api.service
[Unit]
Description=Whisper Speech Recognition FastMCP Gateway Service
After=network.target nvidia-persistenced.service docker.service
Wants=network-online.target

[Service]
Type=simple
User=whisper
Group=whisper
WorkingDirectory=/opt/whisper-mcp
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="FASTMCP_PORT=8020"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/opt/whisper-mcp/venv/bin/python3 -m whisper_mcp_server
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Security Hardening & Resource Isolation
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/whisper-mcp /data/media /data/outputs /var/log/whisper
PrivateTmp=true
ProtectControlGroups=true
ProtectKernelModules=true
ProtectKernelTunables=true
NoNewPrivileges=true
MemoryMax=10G
TasksMax=2048

[Install]
WantedBy=multi-user.target
```

Enable and start the service with standard systemctl commands:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now whisper-api.service
sudo systemctl status whisper-api.service
```

## Diagnostic & Troubleshooting Matrix

| Error Code / Symptom | Root Cause Analysis | Diagnostic Inspection Command | Immediate Remediation Strategy |
| :--- | :--- | :--- | :--- |
| `ERR_CUDA_OUT_OF_MEMORY` | GPU VRAM saturation during large batch inference or multiple concurrent streams. | `nvidia-smi --query-gpu=memory.used,memory.total --format=csv` | Pass `compute_type="int8_float16"`, set `compute_type="float8"`, or reduce batch size limit (`batch_size=8`). |
| `ERR_HALLUCINATION_REPETITION` | Model looped on silent or background acoustic noise regions without speech. | Inspect segment tokens for repeated n-grams or check `avg_logprob < -1.0`. | Enable Silero-VAD filtering (`vad_filter=True`) and apply temperature fallback (`temperature=[0.0, 0.2, 0.4]`). |
| `ERR_UNSUPPORTED_CONTAINER` | Audio container codec format not decoded by ffmpeg backend bindings. | Check container streams via `ffprobe -i audio_file.m4a`. | Transcode source file to standard 16kHz mono PCM WAV via `ffmpeg -i input -ar 16000 -ac 1 output.wav`. |
| `ERR_COREML_COMPILATION_FAIL` | Missing or mismatched Apple CoreML model binaries on macOS execution node. | Inspect console logs during `whisper.cpp` model initialization. | Execute `whisper.cpp/models/generate-coreml-model.sh` to compile native Apple Silicon models. |
| `FASTMCP_PAYLOAD_TOO_LARGE` | Inline raw binary audio submission exceeded FastMCP message length threshold. | Check HTTP body size in incoming reverse proxy access logs. | Pass local filesystem paths (`FilePath`) or pre-uploaded S3/HTTP URLs rather than raw byte blobs. |
| `ERR_CUDA_DRIVER_MISMATCH` | PyTorch/CTranslate2 binary compiled against CUDA version newer than host driver. | Compare `nvidia-smi` driver CUDA version against `python3 -c "import torch; print(torch.version.cuda)"`. | Upgrade host NVIDIA GPU driver to 550+ or pull container built for CUDA 12.2/12.4. |

## Operational Best Practices & Troubleshooting

### 1. Hallucination Reduction via Silero-VAD
- **Integrate Silero Voice Activity Detection**: Hallucinations occur during long stretches of silence or non-speech background music. Always enable Silero-VAD filtering (`vad_filter=True` in Faster-Whisper) to strip silent segments before sending audio frames to the Whisper transformer.

### 2. Low-Memory Deployment Optimization
- **Quantization for Edge CPU/GPU**: On systems with <8GB VRAM, use `large-v3-turbo` with `int8_float16` or `int8` compute types in CTranslate2 to halve memory consumption while keeping transcript WER (Word Error Rate) within 0.5% of full float16 precision.

### 3. Word-Level Timestamps
- When synchronizing subtitles (SRT/VTT) or feeding transcripts into interactive audio players, enable `word_timestamps=True`. Faster-Whisper leverages cross-attention weight matrix extraction to pinpoint exact word boundaries without requiring an acoustic phoneme alignment pass.

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
- [Audio Transcription Research](../knowledge_base/audio-transcription-research.md) — Deep dive into Whisper variant performance benchmarks.
- [Speaches](https://github.com/speaches-ai/speaches) — OpenAI-compatible Whisper API server.

## Sources / References
- [Whisper GitHub Repository](https://github.com/openai/whisper)
- [Whisper.cpp GitHub Repository](https://github.com/ggerganov/whisper.cpp)
- [Faster-Whisper GitHub Repository](https://github.com/SYSTRAN/faster-whisper)
- [Speaches GitHub Repository](https://github.com/speaches-ai/speaches)
- [Silero-VAD GitHub Repository](https://github.com/snakers4/silero-vad)
- [CTranslate2 Documentation](https://opennmt.net/CTranslate2/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
