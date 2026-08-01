# OpenAI Whisper

## What it is
OpenAI Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web. As of **late October / November 2026**, optimizations like **Faster-Whisper v1.2.x** and **Whisper.cpp** provide the foundation for high-performance local transcription, integrated with frontier models like **Claude 5.1**, **GPT-5.5**, and [Gemma 3](../tools/ai_knowledge/local_llms.md) for automated post-processing, translation, and agentic reasoning.

## What problem it solves
Transcribing audio manually is time-consuming and expensive. Whisper provides high-accuracy transcription, translation, and language identification, allowing for the automation of meeting notes, video subtitling, and voice-controlled interfaces. It is particularly notable for its robustness to accents, background noise, and technical language.

## Where it fits in the stack
**Category**: Services / AI & Machine Learning. It serves as the **audio perception layer** in a local AI stack, converting voice input into text that can then be processed by LLMs or other automation tools.

## Typical use cases
- Transcribing recorded meetings or lectures for searchability.
- Generating subtitles for videos in multiple languages.
- Building voice-activated home automation commands.
- Translating foreign language audio into English text.
- Enriching local media libraries (e.g., [Audiobookshelf](audiobookshelf.md)) with full-text search.
- **Hardware-Accelerated Transcription**: Optimized performance across a variety of hardware from Raspberry Pi 5 to NVIDIA RTX 4090.
- **MCP 3.1 Integration**: Whisper services can be exposed as MCP 3.1 tools, allowing autonomous agents to request on-demand transcription of local media files.

### Hardware Benchmarking (Late 2026)

| Hardware | Model | Backend | Time for 10m Audio | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Raspberry Pi 5 | base | Whisper.cpp | ~8m | CPU-only, slow but viable. |
| Intel i7 (14th Gen) | medium | Faster-Whisper | ~1.5m | Optimized with `int8` quantization. |
| Apple M4 Pro | large-v3 | Whisper.cpp | ~40s | Leveraging CoreML/MLX. |
| NVIDIA RTX 4070 | large-v3 | Faster-Whisper | ~15s | FP16, batched inference. |
| NVIDIA RTX 4090 | large-v3 | Faster-Whisper | ~8s | Peak throughput for batch jobs. |

## Strengths
- **High Accuracy**: Competes with professional human transcribers in many languages.
- **Multilingual**: Supports transcription in dozens of languages and translation into English.
- **Robustness**: Handles background noise and various accents exceptionally well.
- **Local Execution**: Can be run entirely offline (via Whisper.cpp or Faster-Whisper), ensuring data privacy.
- **Batched Inference**: Faster-Whisper v1.2.x supports optimized batched processing for up to 4x speed increases.

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
```

## API examples
Integrate Whisper transcription and AI-driven post-processing into Python scripts or FastMCP 3.1 servers.

### Python: FastMCP 3.1 Server for GPU-Accelerated Batch Transcription
This example showcases a production-ready FastMCP 3.1 tool utilizing Pydantic v2 schemas to trigger local audio transcription, parse voice options, and return structured output for models like **Claude 5.1** and **GPT-5.5**.

```python
import os
import requests
from pydantic import BaseModel, Field, FilePath
from mcp.server.fastmcp import FastMCP
from faster_whisper import WhisperModel, BatchedInferencePipeline

# Initialize FastMCP Server
mcp = FastMCP("SpeechRecognition")

class TranscriptionRequest(BaseModel):
    audio_path: FilePath = Field(description="Absolute local path to the audio file (e.g., .wav, .mp3, .m4a)")
    model_size: str = Field(default="large-v3-turbo", description="Whisper model size: base, medium, or large-v3-turbo")
    language: str = Field(default="en", description="ISO 639-1 language code of the audio source")

class TranscriptSegment(BaseModel):
    start_sec: float = Field(description="Start time of the segment in seconds")
    end_sec: float = Field(description="End time of the segment in seconds")
    text: str = Field(description="Transcribed text within this time window")

class TranscriptionResponse(BaseModel):
    success: bool = Field(description="Whether transcription was completed successfully")
    language_detected: str = Field(description="Auto-detected or enforced source language")
    duration_sec: float = Field(description="Total duration of the processed audio file")
    full_text: str = Field(description="Consolidated string of the entire transcription")
    segments: list[TranscriptSegment] = Field(description="Individual time-coded segment list")

@mcp.tool()
def transcribe_local_audio(request: TranscriptionRequest) -> str:
    """
    Performs GPU-accelerated batched inference with Faster-Whisper, parses time-stamps,
    validates the structured transcript payload via Pydantic v2, and returns a detailed JSON report.
    """
    try:
        # Determine device capabilities (fallback to CPU if CUDA is unavailable)
        device = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"

        # Load models
        model = WhisperModel(request.model_size, device=device, compute_type=compute_type)
        pipeline = BatchedInferencePipeline(model)

        # Run inference
        segments_raw, info = pipeline.transcribe(
            str(request.audio_path),
            batch_size=16,
            language=request.language
        )

        segments_list = []
        full_text_parts = []

        for segment in segments_raw:
            full_text_parts.append(segment.text)
            segments_list.append(
                TranscriptSegment(
                    start_sec=segment.start,
                    end_sec=segment.end,
                    text=segment.text.strip()
                )
            )

        response = TranscriptionResponse(
            success=True,
            language_detected=info.language,
            duration_sec=info.duration,
            full_text=" ".join(full_text_parts).strip(),
            segments=segments_list
        )

        return response.model_dump_json(indent=2)
    except Exception as e:
        return f"Error during transcription: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Ollama](ollama.md) — For processing transcribed text with local LLMs.
- [n8n](n8n.md) — For automating audio ingestion and transcription workflows.
- [Audiobookshelf](audiobookshelf.md) — For managing transcribed audio libraries.
- [Home Assistant](home-assistant.md) — For integrating Whisper into voice-controlled home automation.
- [SearXNG](searXNG.md) — For searching through transcribed knowledge bases.
- [LiteLLM](litellm.md) — For unified proxying to frontier models like Claude 5.1 and GPT-5.5.
- [Plex](plex.md) — Streaming transcoded content and media archives.
- [Jellyfin](jellyfin.md) — General purpose media hub for serving audio collections.
- [Authentik](authentik.md) — Authenticating web triggers for speech endpoints.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Canonical local LLM for transcript reasoning and cleanup.
- [Speaches](https://github.com/speaches-ai/speaches) — OpenAI-compatible Whisper API server.

## Sources / References
- [Whisper GitHub](https://github.com/openai/whisper)
- [Whisper.cpp GitHub](https://github.com/ggerganov/whisper.cpp)
- [Faster-Whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [Speaches GitHub](https://github.com/speaches-ai/speaches)

## Contribution Metadata
- Last reviewed: 2026-11-10
- Confidence: high
