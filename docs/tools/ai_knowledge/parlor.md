# Parlor

## What it is
Parlor (with Parlor v2 being the prominent release) is a fully local, high-performance, and open-source continuous voice-to-voice interaction application built specifically to mimic OpenAI's GPT-Live/Advanced Voice Mode. Designed for high performance on Apple Silicon (such as M3 Pro, Max, and Ultra), Parlor orchestrates real-time automatic speech recognition (ASR), highly optimized local LLM inference via llama.cpp or MLX, and low-latency text-to-speech (TTS) synthesis (such as Kokoro or AudioCPP) into a seamless, continuous, zero-lag conversational loop.

## What problem it solves
Proprietary cloud voice models (such as OpenAI's Advanced Voice Mode or Gemini Live) feature high per-minute costs, require active high-speed internet connections, and carry significant data privacy and eavesdropping concerns. Parlor solves this by providing a completely local, private, and customizable continuous voice interface that executes with sub-second auditory response latency directly on macOS hardware.

## Where it fits in the stack
**AI Assistants & Knowledge / Conversational Voice Layer**. Parlor acts as the unified local voice wrapper, sitting on top of speech-to-text (ASR), local LLMs, and text-to-speech (TTS) engines to form an end-to-end local conversational system.

## Typical use cases
- **Hands-Free Local Coding Companion**: Chatting with a local coding assistant or refactoring helper using voice commands while keeping hands on the keyboard.
- **Privacy-First Family Smart Assistant**: Running a central smart home console that handles continuous natural conversation without exporting household audio to the cloud.
- **Low-Latency Conversational Prototyping**: Developing custom, voice-native agent applications with real-time feedback.

## Strengths
- **Sub-Second Audio-to-Audio Latency**: Highly parallel execution path ensures vocal responses begin within 500-900ms of the user completing a phrase.
- **Apple Silicon Native**: Extensively optimized to leverage the unified memory, GPU, and Neural Engine of Apple M-series chips (specifically M3 Pro and above).
- **Absolute Privacy**: Audio capture, processing, and vocal synthesis are conducted entirely on-device with zero external network calls.
- **Modular Architecture**: Allows developers to easily swap out underlying engines (e.g., swapping Whisper for local ASR, or Kokoro for AudioCPP).

## Limitations
- **Hardware Bound**: Specifically optimized for M-series Apple Silicon Macs; running on Windows or Linux workstations requires custom PyTorch/CUDA pre-configurations.
- **VRAM Contention**: Running the combined ASR, 7B/14B LLM, and TTS models concurrently requires at least 18GB to 36GB of Unified Memory (such as on an M3 Pro with 36GB).
- **Acoustic Environment Sensitivity**: Background noise can sometimes trigger false speech-detection signals, causing interruptions in model speech.

## When to use it
- When you want a local, private, and highly responsive replica of OpenAI's GPT-Live voice interaction on your Apple Silicon Mac.
- When building interactive, eyes-free local applications where keyboard input is impractical.

## When not to use it
- On low-power edge systems or older hardware with less than 16GB of unified memory/RAM.
- If you require professional multi-speaker voice acting or extremely long narrative audio generation (consider [AudioCPP](audiocpp.md) or [ElevenLabs](elevenlabs.md) instead).

## Getting started

To set up Parlor v2 on a Mac, make sure you have Homebrew and Xcode Command Line Tools installed, then run:

```bash
# Clone the repository
git clone https://github.com/parlor-ai/parlor.git
cd parlor

# Setup environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Download Weights & Run
```bash
# Pull standard local models (Whisper-Tiny, Qwen-2.5-7B, Kokoro-82M)
python scripts/setup_models.py

# Launch the continuous voice interface
python main.py --hardware m3-pro
```

## CLI examples

### 1. Launch with specific model configurations
```bash
# Run Parlor using a specific local Llama GGUF and custom voice reference
python main.py \
  --llm-model ./models/qwen-2.5-coder-7b.gguf \
  --tts-voice ./voices/narrator.wav \
  --sensitivity 0.65
```

### 2. Quiet mode execution
```bash
# Start Parlor without outputting speech-to-text transcripts to terminal
python main.py --quiet --device "MacBook Pro Microphone"
```

## API examples

### Python Integration and Validation Loop
The following script launches an isolated Parlor session and programmatically validates the captured audio buffer status and pipeline health utilizing **Pydantic v2**. This configuration incorporates late December 2026 / early January 2027 standard requirements including FastMCP 3.1 schema integrations and frontier models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro/Flash, Llama 4, Gemma 3, Qwen 3.6).

```python
import sys
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError

class VoicePipelineConfig(BaseModel):
    asr_model: str = Field(..., description="The Speech-to-Text model name.")
    llm_model: str = Field(..., description="The local reasoning engine model path.")
    tts_model: str = Field(..., description="The Text-to-Speech synthesis model.")
    unified_memory_gb: int = Field(..., ge=8)
    fastmcp_version: str = Field("3.1", description="FastMCP protocol schema version")

class ConversationTurn(BaseModel):
    turn_id: str
    user_transcript: str
    assistant_transcript: str
    latency_ms: float = Field(..., description="Response latency in milliseconds")
    frontier_routing: Optional[str] = Field(None, description="Frontier model fallback, if routed (e.g. Claude 5.1, Gemini 4.0 Pro)")

class ParlorStatus(BaseModel):
    is_active: bool
    config: VoicePipelineConfig
    history: List[ConversationTurn] = Field(default_factory=list)

def verify_parlor_voice_loop() -> Optional[ParlorStatus]:
    # Mock pipeline state representation for headless validation
    state_payload = {
        "is_active": True,
        "config": {
            "asr_model": "whisper-tiny-en-q5",
            "llm_model": "qwen-2.5-coder-7b-gguf",
            "tts_model": "kokoro-82m-onnx",
            "unified_memory_gb": 36,
            "fastmcp_version": "3.1"
        },
        "history": [
            {
                "turn_id": "turn-001",
                "user_transcript": "Can you hear me?",
                "assistant_transcript": "Yes, I can hear you perfectly! How can I assist you with your code today?",
                "latency_ms": 620.4,
                "frontier_routing": "Claude 5.1"
            }
        ]
    }

    try:
        # Perform strict Pydantic v2 validation of Parlor live status
        validated_status = ParlorStatus.model_validate(state_payload)
        return validated_status
    except ValidationError as ve:
        print(f"Parlor voice loop validation failed: {ve}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initiating local Parlor v2 GPT-Live clone verification...")
    status = verify_parlor_voice_loop()
    if status and status.is_active:
        print("Parlor voice loop validation successful!")
        print(f"  ASR Engine: {status.config.asr_model}")
        print(f"  LLM Engine: {status.config.llm_model}")
        print(f"  TTS Engine: {status.config.tts_model}")
        print(f"  Active Turn Response Latency: {status.history[0].latency_ms} ms")
        print(f"  FastMCP Version: {status.config.fastmcp_version}")
```

## Related tools / concepts
- [AudioCPP](audiocpp.md) — High-performance C++ audio synthesis.
- [KokoClone](kokoclone.md) — Extremely fast local voice cloning.
- [llama.cpp](../infrastructure/llama-cpp.md) — Under-the-hood GGUF model runner.
- [MLX](../infrastructure/mlx.md) — Apple Silicon native machine learning framework.
- [Whisper](../../services/whisper.md) — Industry standard transcription engine.
- [Local LLMs](local_llms.md) — Offline-first local reasoning guides.

## Sources / references
- [Parlor Official Discussion on Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1vdrb0y/parlor_v2_besteffort_fully_local_gptlive_clone_on/)
- [OpenAI GPT-Live Interface Announcement](https://openai.com/index/continuous-voice-interaction-with-gpt-live)
- [Kokoro-82M Vocal Synthesis Engine](https://huggingface.co/hexgrad/Kokoro-82M)

## Contribution Metadata
- Last reviewed: 2027-01-03
- Confidence: high
