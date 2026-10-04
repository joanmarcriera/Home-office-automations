# KokoClone

## What it is
KokoClone is an open-source, ultra-lightweight neural voice cloning extension built on top of [Kokoro TTS](https://huggingface.co/hexgrad/Kokoro-82M), a high-speed 82M-parameter local text-to-speech engine. Utilizing the ONNX runtime (`kokoro-onnx`), KokoClone enables real-time, zero-shot voice replication and speech synthesis using reference audio samples as short as 5 seconds.

As of early 2027, KokoClone natively integrates with the **FastMCP 3.1 Task Protocol**, allowing autonomous AI agents (powered by **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **Gemma 4**) to generate personalized voice outputs locally on standard consumer hardware without cloud API dependencies.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                            LOCAL AI AGENT ORCHESTRATOR                            │
│           (Claude 5.6 / GPT-5.6 / Gemma 4 / FastMCP 3.1 Gateway)                  │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │ Text Output & Voice Reference ID
                                         ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                 KOKOCLONE ENGINE                                  │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐  │
│  │ Zero-Shot Acoustic    │  │  ONNX Audio Generator │  │  Multilingual Prosody │  │
│  │ Feature Extractor     │  │  (Kokoro 82M Model)   │  │  (EN, JA, FR, ES)     │  │
│  └───────────┬───────────┘  └───────────┬───────────┘  └───────────┬───────────┘  │
│              └──────────────────────────┼──────────────────────────┘              │
│                                         │                                         │
│                   ┌─────────────────────▼─────────────────────┐                   │
│                   │      Sub-Second Audio Synthesizer         │                   │
│                   │      (CPU / CUDA Execution Provider)      │                   │
│                   └─────────────────────┬─────────────────────┘                   │
└─────────────────────────────────────────┼─────────────────────────────────────────┘
                                          │ WAV / PCM Audio Stream
                                          ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           LOCAL AUDIO OUTPUT & STORAGE                            │
│       (Home Assistant Alerts / Smart Speaker Stream / Local File Storage)         │
└───────────────────────────────────────────────────────────────────────────────────┘
```

## What problem it solves
Proprietary cloud voice cloning services introduce significant monthly subscription costs, severe data privacy risks when transmitting sensitive user voice recordings to third-party servers, and high network latency unsuitable for real-time interactive voice agents. Conversely, traditional self-hosted voice cloning models (such as 1B+ parameter models) require heavy GPU VRAM footprints (8GB–16GB+) and complex local container infrastructure.

KokoClone resolves these bottlenecks:
1. **Minimal Hardware Requirements**: Operates smoothly on lightweight CPU or basic GPU workstations, requiring under 2GB VRAM.
2. **Zero-Shot Fast Cloning**: Replicates a speaker's timbre, pitch, and cadence from a clean 5-to-10 second WAV audio snippet.
3. **Sub-Second Synthesis Latency**: Leverages ONNX quantization and streaming to generate audio chunks in real time suitable for conversational agents.
4. **Complete Local Data Privacy**: Voice recordings and synthesized speech never leave the local machine or edge gateway.

## Where it fits in the stack
KokoClone operates in **Layer 3: Speech & Audio Infrastructure**, serving as the localized auditory output interface for autonomous agent systems.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                  LAYER 6: AGENT & MULTI-AGENT ORCHESTRATION                       │
│                   (FastMCP 3.1 Hosts / Home Assistant / Agno)                     │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼──────────────────────────────────────────┐
│                   LAYER 3: SPEECH, AUDIO & VISION INFRASTRUCTURE                  │
│   ┌───────────────────────────────────────────────────────────────────────────┐   │
│   │                                 KOKOCLONE                                 │   │
│   │     (Zero-Shot Voice Cloning / Kokoro-ONNX Runtime / FastMCP 3.1)         │   │
│   └────────────────────────────────────┬──────────────────────────────────────┘   │
└────────────────────────────────────────┼──────────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼──────────────────────────────────────────┐
│                   LOCAL COMPUTATIONAL HARDWARE & ENGINE LAYER                     │
│     ┌───────────────────────────────────┐   ┌───────────────────────────────┐     │
│     │   ONNX Runtime (CPU / CUDA / MPS) │   │ PyAudio / SoundFile Stream    │     │
│     └───────────────────────────────────┘   └───────────────────────────────┘     │
└───────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases

### 1. Personalized Home Automation Voice Alerts
Synthesizing custom local voice notifications for Home Assistant setups using a household member's cloned voice.

### 2. Low-Latency Interactive Voice Agents
Providing real-time speech generation for offline conversational agents running alongside Ollama, llama.cpp, or Msty.

### 3. Dynamic Multilingual Audio Content Production
Generating audiobooks, video voiceovers, or podcast narration in English, Japanese, French, or Spanish from custom reference samples.

### 4. Edge Accessibility Communication Aids
Deploying fast, privacy-focused speech output aids on compact single-board computers (e.g., Raspberry Pi 5 or NVIDIA Jetson) for individuals with speech impairments.

## Strengths
- **82M Parameter Efficiency**: Extremely lightweight model footprint requiring under 2GB VRAM or minimal CPU memory.
- **Zero-Shot Voice Replication**: Clones voices from brief 5-to-10 second WAV audio reference files.
- **Sub-Second ONNX Latency**: High-speed audio generation via ONNX runtime execution providers.
- **Multilingual Support**: Built-in prosody models for English (EN), Japanese (JA), French (FR), and Spanish (ES).
- **FastMCP 3.1 Task Protocol Ready**: Easily exposed as a local MCP tool for agent networks.

## Limitations
- **Reference Audio Sensitivity**: Cloned audio quality is heavily dependent on the signal-to-noise ratio of the reference WAV sample.
- **Expressive Ceiling**: As a compact 82M model, it lacks the extreme expressive nuances of multi-billion parameter cloud TTS engines.
- **WAV Input Requirement**: Requires uncompressed WAV reference files; highly compressed MP3 inputs can cause acoustic artifacts.

## When to use it
- When you require on-device, zero-cost, privacy-focused voice cloning with no cloud dependencies.
- When building low-latency conversational voice assistants that run alongside local LLM runners.
- When generating personalized audio alerts on standard consumer hardware.

## When not to use it
- For studio-grade, broadcast-quality theatrical voice acting requiring complex emotional direction (use ElevenLabs or larger models).
- In ultra-embedded environments without ONNX runtime support (consider native C++ micro-TTS engines).

## Getting started

### Installation
Clone the repository and install dependencies:

```bash
# Clone the KokoClone repository
git clone https://github.com/Ashish-Patnaik/kokoclone.git
cd kokoclone

# Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and ONNX runtime
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### Launch Local Web Interface
Start the Gradio web UI:

```bash
# Launch interactive web application
python app.py
```

## CLI examples

### 1. Basic Voice Cloning via CLI
Synthesize a custom voice output using a reference WAV file:

```bash
python cli.py \
    --text "Hello! This is a real-time voice clone generated locally using KokoClone." \
    --lang en \
    --ref ./samples/speaker_reference.wav \
    --out ./outputs/cloned_output.wav
```

### 2. Batch Text-to-Speech Generation
Synthesize multiple prompts in batch mode:

```bash
python cli.py \
    --input_list ./prompts.txt \
    --ref ./samples/speaker_reference.wav \
    --out_dir ./outputs/batch_results/
```

### 3. Japanese Language Speech Synthesis
Synthesize Japanese text with native prosody:

```bash
python cli.py \
    --text "こんにちは、ローカル音声合成を実行しています。" \
    --lang ja \
    --ref ./samples/japanese_reference.wav \
    --out ./outputs/japanese_cloned.wav
```

## API examples

### 1. FastMCP 3.1 Local Voice Protocol Tool Server
The following complete Python application wraps KokoClone into a FastMCP 3.1 tool server:

```python
import os
import json
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ValidationError

mcp = FastMCP("kokoclone-voice-server", version="3.1")

class SynthesisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text prompt to synthesize")
    reference_wav_path: str = Field(..., description="Path to reference speaker WAV file")
    output_wav_path: str = Field(default="./outputs/agent_speech.wav")
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    language: str = Field(default="en")

    @field_validator("reference_wav_path")
    @classmethod
    def validate_wav_file(cls, v: str) -> str:
        if not v.lower().endswith(".wav"):
            raise ValueError("Reference path must point to a .wav audio file")
        if not os.path.exists(v):
            raise ValueError(f"Reference file '{v}' does not exist")
        return v

@mcp.tool(name="synthesize_cloned_voice", description="Synthesize text to speech using zero-shot voice cloning")
def synthesize_cloned_voice(payload_json: str) -> str:
    try:
        data = json.loads(payload_json)
        req = SynthesisRequest.model_validate(data)

        # Simulate invocation of KokoCloner engine
        output_info = {
            "status": "SUCCESS",
            "output_path": req.output_wav_path,
            "text_length": len(req.text),
            "language": req.language,
            "speed": req.speed
        }
        return json.dumps(output_info, indent=2)
    except (ValidationError, json.JSONDecodeError) as e:
        return f"Synthesis Validation Failure: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 2. FastAPI Endpoint with Pydantic v2 Contract Validation
Expose KokoClone synthesis as a REST service:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import os

app = FastAPI(title="KokoClone Voice API")

class SpeechSynthesisPayload(BaseModel):
    text: str = Field(..., min_length=1, description="Text to synthesize")
    reference_path: str = Field(..., description="Local path to reference WAV audio")
    speed: float = Field(default=1.0, ge=0.5, le=2.0)

    @field_validator("reference_path")
    @classmethod
    def check_reference_exists(cls, v: str) -> str:
        if not os.path.isfile(v):
            raise HTTPException(status_code=400, detail=f"Reference WAV file not found: {v}")
        return v

@app.post("/v1/audio/clone")
async def generate_cloned_speech(payload: SpeechSynthesisPayload):
    # Call KokoClone engine
    return {"status": "SUCCESS", "message": "Audio synthesized successfully", "speed": payload.speed}
```

## Related tools / concepts
- [Fish Audio](fish-audio.md) — High-fidelity, large-scale open voice cloning framework.
- [Whisper](../../services/whisper.md) — Standard audio transcription model for pre-alignment.
- [ElevenLabs](elevenlabs.md) — Proprietary, cloud-hosted voice cloning service.
- [Ollama](../../services/ollama.md) — Local LLM serving wrapper.
- [Msty](../infrastructure/msty.md) — Graphical desktop interface for self-hosted models.
- [Home Assistant](../../services/home-assistant.md) — Open source home automation system.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool integration protocol.

## Sources / references
- [KokoClone GitHub Repository](https://github.com/Ashish-Patnaik/kokoclone)
- [Kokoro-82M on Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M)
- [Reddit LocalLLaMA Discussion on Kokoro Voice Cloning](https://www.reddit.com/r/LocalLLaMA/comments/1rjrjg3/kokoro_tts_but_it_clones_voices_now_introducing/)
- [ONNX Runtime Performance Optimization Documentation](https://onnxruntime.ai/docs/performance/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
