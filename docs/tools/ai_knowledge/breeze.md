# Breeze

## What it is
Breeze is an open-source, low-latency local Text-to-Speech (TTS) engine optimized for real-time speech synthesis, voice cloning, and interactive agent pipelines. Designed to run efficiently on consumer GPUs (including NVIDIA 30/40/50 series) and Apple Silicon neural engines, Breeze combines neural codec vocoders with fast transformer backbone models to convert text into highly natural, expressive audio stream chunks in under 100ms time-to-first-audio-chunk. In 2027, Breeze serves as a key local audio generation tier for agentic voice assistants and offline multi-modal systems.

```
+-----------------------------------------------------------------------------------+
|                            BREEZE LOCAL TTS PIPELINE                              |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Input Text Stream   | ----> | Phoneme / G2P          | ---> | Expressive Neural| |
|  | / Agent Dialogue    |       | Normalizer Transformer|      | Codec Acoustic  | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | FastMCP 3.1 Gateway | <---- | Real-time Streaming   | <--- | Fast Vocoder    | |
|  | Audio SSE Stream    |       | Buffer / WebRTC Engine|      | Synthesis Kernel| |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Cloud-based speech synthesis services (such as ElevenLabs or Azure Speech) introduce network latency, expensive per-character API costs, and privacy concerns for sensitive voice applications. Standard local TTS solutions are often cumbersome to install, high in latency (>500ms), or lack natural prosody and voice cloning options. Breeze solves this by delivering ultra-low-latency local neural audio generation, complete with zero-shot voice cloning capabilities and streaming output endpoints compatible with agent interaction frameworks.

## Where it fits in the stack
**AI Knowledge / Audio Processing & Local Speech Synthesis Engine**. Breeze sits alongside local LLM inference engines (such as Ollama or vLLM) to provide the voice output component of fully offline voice agent systems.

## Typical use cases
- **Real-Time Voice Agent Output**: Generating sub-100ms streaming voice responses for interactive voice agents.
- **Offline Voice Cloning & Custom Avatars**: Creating personalized voice profiles locally using zero-shot reference audio.
- **Accessibility & Screen Reading**: Providing natural, offline screen-reading for desktop applications without external network dependency.
- **Podcast & Audio Production**: Batch synthesis of expressive long-form narrations with controllable prosody and emotion.

## Strengths
- **Ultra-Low Latency Streaming**: Delivers streaming audio chunks in under 100ms TTFA (Time to First Audio).
- **Zero-Shot Voice Cloning**: Clones reference target speaker voices using 5-10 second reference audio samples.
- **Cross-Platform Acceleration**: Native support for CUDA, Metal, and ONNX Runtime acceleration.
- **Agent Framework Ready**: Integrates via SSE/WebSockets for streaming audio directly into frontend clients.

## Limitations
- **VRAM Requirements**: Optimal multi-voice performance requires ~2-4GB dedicated GPU VRAM.
- **Multilingual Boundaries**: High-fidelity accent control depends heavily on language-specific phoneme models.

## When to use it
- When building local, private voice assistants requiring real-time conversational speech synthesis.
- When minimizing cloud API expenditures for high-volume audio generation tasks.
- When requiring zero-shot voice cloning capabilities in offline home-lab environments.

## When not to use it
- When requiring simple web browser native speech synthesis where Web Speech API suffices.
- When running on extremely resource-constrained embedded microcontrollers without GPU/NPU hardware.

## Architecture & Technical Deep Dive

Breeze splits speech generation into a two-stage acoustic-vocoder architecture optimized for parallel streaming execution:

```
                         BREEZE TTS ARCHITECTURE PIPELINE

    Raw Input Text / Agent Output Stream
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Grapheme-to-Phoneme (G2P)    │  <--- Normalization & Accent Mapping
     │ Text Normalizer              │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Fast Transformer Acoustic    │  <--- Zero-shot Speaker Embeddings
     │ Feature Generator            │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Neural Codec Vocoder         │  <--- TensorRT / Metal Accelerated
     │ Audio Waveform Generator     │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ FastMCP 3.1 Controller       │  <--- Streaming WebSockets / SSE
     │ & Audio Gateway              │
     └──────────────────────────────┘
```

1. **G2P & Phoneme Normalizer**: Converts raw string inputs into normalized phoneme sequences while handling numbers, dates, and domain abbreviations.
2. **Acoustic Model**: A lightweight transformer model that predicts acoustic latent tokens conditioned on target speaker embeddings.
3. **Neural Codec Vocoder**: Converts latent tokens into 24kHz/48kHz PCM audio waveforms using hardware-optimized convolution kernels.
4. **Streaming Audio Buffer**: Streams PCM audio frames directly through WebSockets or FastMCP SSE channels.

## Getting started

To get started with Breeze locally, install the core library and launch the interactive CLI or server mode:

```bash
# Install Breeze package via PyPI
pip install breeze-tts

# Synthesize a test audio file
breeze-tts --text "Hello! Breeze local text to speech is running smoothly." --output hello.wav --speaker default
```

## CLI examples

```bash
# Run local TTS benchmark with time-to-first-audio latency metrics
breeze-tts bench --model breeze-v2-fast --text "Testing ultra low latency synthesis."

# Synthesize speech using zero-shot voice cloning from a reference sample
breeze-tts clone --ref-audio sample.wav --text "Welcome to the private voice assistant stack." --output cloned_output.wav

# Launch Breeze HTTP/WebSocket streaming server on port 8088
breeze-server --port 8088 --host 0.0.0.0 --device cuda
```

## API examples

### FastMCP 3.1 Integration & Pydantic v2 Audio Engine Configuration
The following Python module demonstrates how to wrap Breeze in a **FastMCP 3.1** server with robust **Pydantic v2** validation.

```python
import os
import base64
import logging
from typing import Optional, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Breeze-TTS-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("breeze-tts-engine")

# Pydantic v2 Speech Synthesis Request Model
class SpeechSynthesisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1, max_length=5000, description="Text string to synthesize into speech")
    speaker_id: str = Field(default="default", description="Speaker voice identifier or profile name")
    sample_rate: int = Field(default=24000, description="Audio sampling rate in Hz (16000, 24000, 48000)")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Playback speed modifier")
    pitch: float = Field(default=0.0, ge=-12.0, le=12.0, description="Pitch shift in semitones")
    output_format: str = Field(default="wav", description="Audio format (wav, mp3, ogg, pcm)")

    @field_validator("sample_rate")
    @classmethod
    def validate_sample_rate(cls, v: int) -> int:
        valid_rates = [16000, 24000, 44100, 48000]
        if v not in valid_rates:
            raise ValueError(f"Sample rate must be one of {valid_rates}")
        return v

    @field_validator("output_format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        valid = ["wav", "mp3", "ogg", "pcm"]
        if v.lower() not in valid:
            raise ValueError(f"Output format must be one of {valid}")
        return v.lower()

@mcp.tool()
async def synthesize_speech(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Synthesizes speech from text using the Breeze TTS engine.

    Args:
        request_dict: Dictionary matching SpeechSynthesisRequest model.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating synthesis request with Pydantic v2...")

    try:
        req = SpeechSynthesisRequest.model_validate(request_dict)
        if ctx:
            await ctx.info(f"Synthesizing {len(req.text)} characters for speaker '{req.speaker_id}'...")

        # Mock synthesis pipeline output
        duration_sec = len(req.text) * 0.06
        return {
            "status": "success",
            "speaker_id": req.speaker_id,
            "sample_rate": req.sample_rate,
            "duration_seconds": round(duration_sec, 2),
            "format": req.output_format,
            "ttfa_ms": 78.4,
            "audio_base64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA..."
        }
    except ValidationError as ve:
        logger.error(f"Validation failure: {ve}")
        raise ValueError(f"Invalid synthesis parameters: {ve}")

@mcp.tool()
async def get_breeze_status(ctx: Optional[Context] = None) -> dict:
    """Queries current hardware backend, loaded voice models, and device memory status."""
    if ctx:
        await ctx.info("Fetching Breeze runtime state...")

    return {
        "engine": "Breeze TTS v2",
        "device": "CUDA (NVIDIA RTX 4090)",
        "vram_allocated_mb": 1840,
        "active_speaker_profiles": ["default", "narrator-male-1", "conversational-female-2"],
        "streaming_latency_ms": 75.2
    }

if __name__ == "__main__":
    mcp.run()
```

## Integration patterns
- **FastMCP Streaming Voice Agent Pipeline**: Combine with vLLM or Ollama to stream textual response tokens directly into Breeze speech generation buffers.
- **WebRTC Local Gateway**: Route Breeze PCM audio output through local WebRTC channels to browser clients with minimum buffer overhead.

## Best practices & Security
- **Input Sanitization**: Validate text length and filter out unwanted SSML markup or malicious system prompts before processing.
- **Voice Clone Ethical Controls**: Protect custom speaker embedding files using secure filesystem permissions and access keys.

## Reference implementation

```python
# Complete standalone test for Breeze Pydantic model validation
from pydantic import ValidationError

def test_breeze_config():
    valid_payload = {
        "text": "Testing Breeze TTS local integration.",
        "speaker_id": "default",
        "sample_rate": 24000,
        "speed": 1.1
    }
    req = SpeechSynthesisRequest.model_validate(valid_payload)
    assert req.text == "Testing Breeze TTS local integration."
    assert req.sample_rate == 24000
    print("Breeze schema validation test passed successfully.")

if __name__ == "__main__":
    test_breeze_config()
```

## Related tools / concepts
- [ElevenLabs](../ai_knowledge/elevenlabs.md) — Cloud speech synthesis platform.
- [Whisper](../ai_knowledge/whisper.md) — Local speech recognition model by OpenAI.
- [Ollama](../infrastructure/ollama.md) — Local LLM runner for voice agent backends.
- [Magpie-TTS](../ai_knowledge/magpie-tts.md) — High-fidelity expressive TTS engine.

## Sources / references
- [Breeze Local TTS Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1wxd404/local_text_to_speech_with_breeze_is_truly/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
