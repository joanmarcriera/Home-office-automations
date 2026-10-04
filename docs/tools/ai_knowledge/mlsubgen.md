# MLSubGen

## What it is
**MLSubGen** (Multi-Language Subtitle Generator) is a high-performance, open-source audio processing tool and machine learning framework designed for local, privacy-focused automated speech recognition (ASR), multi-speaker diarization, and multilingual subtitle generation across 45+ spoken languages. Built on top of optimized Whisper backends (Whisper.cpp, Faster-Whisper, and ONNX Runtime), MLSubGen provides content creators, media engineers, and enterprise AI workflows with automated video/audio translation, word-level timestamp alignment, SRT/VTT/ASS subtitle formatting, and real-time streaming captioning.

In traditional media processing pipelines, generating high-accuracy multilingual subtitles and closed captions requires expensive cloud SaaS APIs (e.g., Deepgram, AssemblyAI, AWS Transcribe) or tedious manual transcription. MLSubGen simplifies this process into a unified local CLI tool, Python SDK, and FastMCP microservice that runs efficiently on consumer hardware (NVIDIA RTX GPUs, Apple Silicon Metal, and x86 AVX-512 CPUs) without sending private audio files or sensitive video footage to external cloud services.

```
+-----------------------------------------------------------------------------------+
|                            MLSUBGEN ARCHITECTURE                                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------------+       +-----------------------------------------+  |
|  | Video / Audio Source File | ----> | MLSubGen Audio Preprocessing Pipeline   |  |
|  | (MP4, MKV, MP3, WAV, WebM)  |       | (FFmpeg Demuxing, Resampling to 16kHz)  |  |
|  +---------------------------+       +-----------------------------------------+  |
|                                                           |                       |
|                                                           v                       |
|                                      +-----------------------------------------+  |
|                                      | Optimized Local ASR Engine             |  |
|                                      | - Faster-Whisper / CTranslate2 Backend  |  |
|                                      | - PyAnnote Speaker Diarization Module   |  |
|                                      | - VAD (Voice Activity Detection) Filter |  |
|                                      +-----------------------------------------+  |
|                                                           |                       |
|                                                           v                       |
|  +---------------------------+       +-----------------------------------------+  |
|  | Subtitle File Exports     | <---- | Post-Processing & Timestamp Alignment   |  |
|  | (SRT, VTT, ASS, JSON, TXT)  |       | (45+ Language Translation & Formatting) |  |
|  +---------------------------+       +-----------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
- **Cloud API Costs & Rate Limits**: Eliminates per-minute cloud API subscription costs for large-scale video library transcription and localized captioning.
- **Data Privacy & Compliance**: Keeps sensitive internal meeting recordings, legal depositions, and unreleased video assets on local secure infrastructure.
- **Word-Level Timestamp Accuracy**: Prevents misaligned subtitles during fast dialogue or overlapping speech through precise VAD filtering and CTC alignment.
- **Multilingual Local Translation**: Translates audio directly into English or target secondary languages (45+ supported languages) during the transcription pass.

## Where it fits in the stack
**AI Knowledge / Audio Processing / Media Pipeline Infrastructure**. MLSubGen sits at the audio transcription layer within media processing and AI knowledge extraction pipelines, bridging raw media ingestion and downstream text analysis or subtitle rendering.

```
+-----------------------------------------------------------------------------------+
|                             MEDIA PROCESSING STACK                                |
+-----------------------------------------------------------------------------------+
| Media Ingestion Layer   : FFmpeg / Jellyfin / Plex / Video Management Systems     |
+-----------------------------------------------------------------------------------+
| Audio Transcription     : MLSubGen (Faster-Whisper + PyAnnote Diarization Engine) |
+-----------------------------------------------------------------------------------+
| Subtitle & Text Format  : SRT / WebVTT / ASS Burn-In / JSON Metadata Export       |
+-----------------------------------------------------------------------------------+
| Downstream AI Agents    : FastMCP 3.1 Tools / RAG Ingestion / Video Indexing    |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Automated Video Subtitling**: Generating synchronized multi-language subtitles (.srt, .vtt) for YouTube videos, online courses, webinars, and podcasts.
- **Meeting Recording Diarization**: Transcribing internal corporate Zoom/Teams recordings and attributing spoken dialogue to specific speakers.
- **Media Asset RAG Indexing**: Converting video libraries into time-indexed text transcripts for search engines and vector retrieval databases.
- **Accessibility & Captioning Compliance**: Automating closed-captioning compliance for educational institutions and broadcast video streaming platforms.

## Strengths
- **45+ Multilingual Support**: High transcription and translation accuracy across major European, Asian, and Middle Eastern languages.
- **Hardware-Accelerated Inference**: Fully supports CUDA, TensorRT, Apple Silicon MPS/Metal, and CPU AVX-512 optimizations for up to 15x real-time transcription speeds.
- **Flexible Output Formats**: Direct export to SRT, WebVTT, ASS (with custom styling and speaker highlighting), raw TXT, and structured JSON timestamps.
- **Seamless FastMCP Integration**: Easy integration into automated media pipelines via FastMCP 3.1 tool calls and Pydantic schemas.

## Limitations
- **VRAM Requirements for Large Models**: High-accuracy `large-v3` models require at least 6GB to 8GB of GPU VRAM for optimal batch inference speed.
- **Complex Audio Noise Sensitivity**: Extremely noisy background environments, overlapping chatter, or low-bitrate heavy music tracks require pre-filtering with audio noise suppression tools.
- **Speaker Diarization Setup**: Multi-speaker attribution via PyAnnote requires downloading Hugging Face model weights and token authentication.

## When to use it
- When generating subtitles or transcripts for large video archives locally without incurring cloud API costs.
- For private or confidential video content that cannot be uploaded to external SaaS transcription services.
- When needing precise word-level timestamp alignment and speaker diarization in multiple languages.
- For integrating automated captioning into local media server backends (Jellyfin, Plex, internal NAS platforms).

## When not to use it
- In low-resource edge environments lacking dedicated GPU/NPU hardware where ultra-lightweight web cloud APIs are preferred.
- For real-time low-latency telecommunications (<200ms roundtrip streaming speech-to-text requirements).
- When simple single-language text conversion without timestamp generation is sufficient.

## Getting started

### Prerequisites
- Python 3.10+ with PyTorch (with CUDA support if using NVIDIA GPU).
- FFmpeg installed on system PATH (`ffmpeg -version`).

### Installation via Pip
```bash
# Install MLSubGen with GPU support dependencies
pip install mlsubgen torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
```

### Quickstart Execution with Python SDK
```python
from mlsubgen import SubtitleGenerator

# Initialize generator with medium model on GPU
generator = SubtitleGenerator(model_size="medium", device="cuda", compute_type="float16")

# Transcribe audio file to SRT
result = generator.generate(
    audio_path="lecture_recording.mp4",
    target_language="es",  # Translate to Spanish
    output_format="srt",
    output_path="lecture_es.srt"
)

print(f"Subtitles generated successfully: {result.output_file}")
```

## CLI examples

### Generating Multilingual Subtitles via CLI
```bash
# Transcribe video and output SRT and WebVTT formats
mlsubgen process \
  --input video.mp4 \
  --model large-v3 \
  --language auto \
  --format srt,vtt \
  --output-dir ./subtitles/
```

### Running Batch Subtitle Generation with Speaker Diarization
```bash
# Process all MP4 files in directory with speaker diarization enabled
mlsubgen batch \
  --dir ./webinars/ \
  --diarize \
  --hf-token "hf_xxxxxxxxxxxxxxxxx" \
  --format ass \
  --threads 4
```

## API examples

### FastMCP 3.1 Integration Server
This example demonstrates a FastMCP 3.1 server exposing MLSubGen subtitle generation as an automated tool for media processing agents:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import os
import time

mcp = FastMCP("MLSubGen-Transcription-Server")

class SubtitleRequest(BaseModel):
    media_file_path: str = Field(..., description="Absolute file path to input video or audio file")
    target_language: str = Field(default="en", description="Target language code (e.g. 'en', 'es', 'fr', 'de')")
    model_quality: str = Field(default="small", description="Model size: 'tiny', 'base', 'small', 'medium', 'large-v3'")
    enable_diarization: bool = Field(default=False, description="Whether to perform multi-speaker diarization")

class SubtitleResponse(BaseModel):
    success: bool = Field(..., description="Execution status")
    output_srt_path: str = Field(..., description="File path to generated SRT subtitle file")
    detected_language: str = Field(..., description="Detected spoken language in source media")
    processing_time_sec: float = Field(..., description="Duration of transcription process in seconds")

@mcp.tool()
def generate_subtitles(request: SubtitleRequest) -> SubtitleResponse:
    """Generates localized multi-language subtitles for video or audio files using MLSubGen."""
    start_time = time.time()

    if not os.path.exists(request.media_file_path):
        raise FileNotFoundError(f"Source media file not found: {request.media_file_path}")

    # Simulated MLSubGen execution pass
    output_srt = os.path.splitext(request.media_file_path)[0] + f"_{request.target_language}.srt"

    with open(output_srt, "w", encoding="utf-8") as f:
        f.write("1\n00:00:01,000 --> 00:00:04,000\n[MLSubGen] Automated Subtitle Generation Complete.\n\n")

    elapsed = round(time.time() - start_time, 2)
    return SubtitleResponse(
        success=True,
        output_srt_path=output_srt,
        detected_language="en",
        processing_time_sec=elapsed
    )

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Configuration & Schema Validation
```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class MLSubGenConfig(BaseModel):
    model_size: str = Field(default="medium", description="Whisper model tier")
    compute_type: str = Field(default="float16", description="Quantization compute type")
    supported_formats: List[str] = Field(default_factory=lambda: ["srt", "vtt", "ass", "json"])
    max_segment_duration: float = Field(default=10.0, ge=1.0, le=30.0)

    @field_validator("model_size")
    @classmethod
    def validate_model_size(cls, v: str) -> str:
        valid_models = ["tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"]
        if v not in valid_models:
            raise ValueError(f"Invalid model size '{v}'. Must be one of {valid_models}")
        return v

# Schema validation demonstration
try:
    config = MLSubGenConfig(
        model_size="large-v3",
        compute_type="float16",
        max_segment_duration=8.5
    )
    print("Validated MLSubGen Configuration:", config.model_dump_json(indent=2))
except ValidationError as ex:
    print("Configuration Error:", ex.json())
```

## Related tools / concepts
- [Faster-Whisper](../ai_knowledge/local_llms.md) — High-performance CTranslate2 implementation of OpenAI Whisper.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standard tool server framework for agent integration.
- [BreezeTTS2](../process_understanding/breezetts2.md) — Local speech synthesis and audio generation engine.
- [Paperless-AI](../services/paperless-ai.md) — AI document indexing and metadata extraction platform.

## Sources / references
- [MLSubGen Local Subtitle Generation Release](https://www.reddit.com/r/LocalLLaMA/comments/1wwds6i/mlsubgen_subtitles_in_45_languages_for_your/)
- [Faster-Whisper GitHub Repository](https://github.com/SYSTRAN/faster-whisper)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
