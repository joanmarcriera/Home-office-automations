# Breeze

## What it is
Breeze is an open-source, low-latency local Text-to-Speech (TTS) engine optimized for real-time speech synthesis, voice cloning, and interactive agent pipelines. Designed to run efficiently on consumer GPUs (including NVIDIA 30/40/50 series) and Apple Silicon neural engines, Breeze combines neural codec vocoders with fast transformer backbone models to convert text into highly natural, expressive audio stream chunks in under 100ms time-to-first-audio-chunk (TTFA). In 2027, Breeze serves as a key local audio generation tier for agentic voice assistants and offline multi-modal systems.

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
Cloud-based speech synthesis services (such as ElevenLabs or Azure Speech) introduce network latency, expensive per-character API costs, and privacy concerns for sensitive voice applications. Standard local TTS solutions are often cumbersome to install, high in latency (>500ms), or lack natural prosody and zero-shot voice cloning options.

Breeze solves these core constraints:
- **Sub-100ms Latency**: Delivers real-time streaming audio chunks to client WebRTC and SSE gateways with under 100ms Time-To-First-Audio (TTFA).
- **Zero-Shot Voice Cloning**: Generates natural speech matching reference speaker audio samples using short 5-10 second WAV recordings.
- **Privacy & Offline Independence**: Synthesizes speech locally on GPU/NPU hardware without external internet access or cloud API subscriptions.
- **Agentic FastMCP 3.1 Integration**: Exposes streaming tool endpoints compatible with multi-agent orchestration frameworks.

## Where it fits in the stack
**AI Knowledge / Audio Processing & Local Speech Synthesis Engine**. Breeze sits alongside local LLM inference engines (such as [Ollama](../../services/ollama.md) or [vLLM](../infrastructure/vllm.md)) to provide the voice output component of fully offline voice agent systems.

```
+-----------------------------------------------------------------------------------+
|                                ENTERPRISE VOICE STACK                             |
+-----------------------------------------------------------------------------------+
|  [ User Voice Microphone Input ] -> [ Whisper STT Service ]                       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|  [ FastMCP Agent Orchestrator ] -> [ Local vLLM Engine (Gemma 4 / Llama 4) ]     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         BREEZE LOCAL TTS SYNTHESIS ENGINE                         |
|     (G2P Normalizer | Expressive Transformer | Codec Vocoder | WebRTC/SSE)         |
+-----------------------------------------------------------------------------------+
```

## TTS Engine Comparison Matrix

| Feature / Dimension | Breeze TTS | ElevenLabs Cloud | Bark (Suno) | XTTS-v2 (Coqui) |
| :--- | :--- | :--- | :--- | :--- |
| **Execution Platform** | Local GPU / Apple Silicon | Cloud SaaS API | Local PyTorch | Local PyTorch |
| **First Audio Latency** | **< 100 ms** | ~350 - 600 ms | ~1200 - 2500 ms | ~400 - 800 ms |
| **Zero-Shot Voice Clone**| Supported (5-10s sample)| Supported (Cloud) | Supported | Supported |
| **FastMCP 3.1 Support** | Built-in Tool Gateways | External Webhook | Custom Wrapper | Custom Wrapper |
| **VRAM Footprint** | ~1.8 - 3.5 GB VRAM | 0 MB (Cloud) | ~4.5 - 8.0 GB VRAM | ~3.0 - 5.0 GB VRAM |
| **License** | Open-Source (Apache 2.0) | Proprietary Commercial | MIT License | CPML Non-Commercial |

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

## Systemd Production Service Configuration

To run Breeze as an always-on systemd service unit providing low-latency speech synthesis endpoints:

```ini
[Unit]
Description=Breeze Local Text-To-Speech Daemon
After=network.target nvidia-persistenced.service
Wants=nvidia-persistenced.service

[Service]
Type=simple
User=breeze
Group=breeze
WorkingDirectory=/opt/breeze-tts
ExecStart=/usr/local/bin/breeze-server --port 8088 --host 0.0.0.0 --device cuda --model-path /opt/breeze-tts/models/breeze-v2-fast.pt
Restart=always
RestartSec=3s
Environment=CUDA_VISIBLE_DEVICES=0
MemoryMax=4G
ProtectSystem=full
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

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
from typing import Optional, Dict, Any
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

class VoiceCloneRequest(BaseModel):
    reference_audio_base64: str = Field(..., min_length=100, description="Base64 encoded 5-10s WAV reference audio sample")
    new_speaker_id: str = Field(..., min_length=3, max_length=64, description="Target identifier for cloned speaker profile")

@mcp.tool()
async def synthesize_speech(
    request_dict: Dict[str, Any],
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Synthesizes speech from text using the Breeze TTS engine with Pydantic v2 validation.
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
        return {"status": "error", "message": f"Invalid synthesis parameters: {ve}"}

@mcp.tool()
async def register_voice_clone(
    clone_payload: Dict[str, Any],
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Registers a new zero-shot voice profile from reference audio sample."""
    if ctx:
        await ctx.info("Processing zero-shot voice clone registration...")

    try:
        req = VoiceCloneRequest.model_validate(clone_payload)
        return {
            "status": "registered",
            "new_speaker_id": req.new_speaker_id,
            "reference_audio_bytes": len(req.reference_audio_base64),
            "embedding_dim": 512
        }
    except ValidationError as ve:
        return {"status": "error", "message": str(ve)}

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **High TTFA (>300ms)** | Vocoder fallback to CPU or unoptimized TensorRT kernel | `breeze-tts bench --device cuda` | Enable TensorRT acceleration or compile ONNX Runtime backend |
| **Audio Crackle / Underrun**| Audio output buffer size configured too small for SSE | `breeze-server --log-level debug` | Increase WebSocket/SSE chunk size to 1024 frames |
| **CUDA OOM Error** | VRAM overcommitted during concurrent multi-voice synthesis| `nvidia-smi` | Restrict maximum concurrent voice worker threads via `--max-workers 2` |
| **Muffled Voice Clone** | Low quality or noisy reference audio sample provided | `breeze-tts clone --validate-sample` | Supply clean 24kHz mono reference WAV file (5-10 seconds) |
| **G2P Phoneme Failure** | Special characters or missing language dictionary entry | `breeze-tts test-g2p --text "Text"` | Upgrade phoneme normalizer models or apply pre-synthesis text sanitization |

## Integration patterns
- **FastMCP Streaming Voice Agent Pipeline**: Combine with vLLM or Ollama to stream textual response tokens directly into Breeze speech generation buffers.
- **WebRTC Local Gateway**: Route Breeze PCM audio output through local WebRTC channels to browser clients with minimum buffer overhead.

## Best practices & Security
- **Input Sanitization**: Validate text length and filter out unwanted SSML markup or malicious system prompts before processing.
- **Voice Clone Ethical Controls**: Protect custom speaker embedding files using secure filesystem permissions and access keys.

## Related tools / concepts
- [ElevenLabs](../ai_knowledge/elevenlabs.md) — Cloud speech synthesis platform.
- [Whisper](../../services/whisper.md) — Local speech recognition model by OpenAI.
- [Ollama](../../services/ollama.md) — Local LLM runner for voice agent backends.
- [Magpie-TTS](../ai_knowledge/magpie-tts.md) — High-fidelity expressive TTS engine.

## Sources / references
- [Breeze Local TTS Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1wxd404/local_text_to_speech_with_breeze_is_truly/)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
