# Fish Audio (Fish Speech)

## What it is
Fish Audio (Fish Speech) is an advanced, open-source multilingual text-to-speech (TTS) platform powered by a revolutionary Dual-Autoregressive (Dual-AR) architecture. It is designed for high-fidelity, expressive voice synthesis and zero-shot voice cloning with extremely low latency, supporting the Model Context Protocol (MCP 3.1) for agentic audio orchestration.

## What problem it solves
It solves the dependency on proprietary, high-latency, and expensive TTS APIs like ElevenLabs. By adopting a transformer-based voice architecture isomorphic to large language models, Fish Speech enables fine-grained emotional control and achieves industry-leading Real-Time Factor (RTF) using modern inference acceleration frameworks (like SGLang, TensorRT-LLM, and NVIDIA NIM) running on H200 or Rubin GPU architectures. It serves as a high-fidelity, real-time voice feedback layer for autonomous agents powered by frontier models like Claude 5.1, GPT-5.5, and Llama 4.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Audio Generation. It integrates with the home-office stack via [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) to provide real-time voice feedback for autonomous agents.

## Typical use cases
- **Expressive Narrators**: Generating audiobooks or podcast content with precise, context-dependent emotional cues.
- **Conversational AI**: Powering real-time agents that sound natural, responsive, and maintain low latency using MCP 3.1 audio streams.
- **Voice Cloning**: Creating high-fidelity digital twins from as little as 10-20 seconds of reference audio.
- **Multilingual Content**: Synthesizing speech in over 80 languages without phoneme-level preprocessing or external alignment tools.

## Strengths
- **Fine-Grained Emotion Control**: Supports inline natural language tags (e.g., `[whisper]`, `[excited]`, `[laughing]`) to control prosody, pacing, and emotion at the sub-word level.
- **Innovative Dual-AR Architecture**: Combines a 4B parameter "Slow AR" model for semantic prediction with a 400M parameter "Fast AR" model for acoustic detail reconstruction.
- **Extreme Performance**: Highly optimized for NVIDIA Rubin GPUs, achieving a Real-Time Factor (RTF) of ~0.15 and Time-to-First-Audio (TTFA) of ~85ms.
- **RL Alignment**: Uses Group Relative Policy Optimization (GRPO) to align generated speech with human acoustic preferences.

## Limitations
- **Hardware Intensity**: The flagship 4B model requires significant VRAM (ideally NVIDIA Rubin R100 or H200) for optimal throughput.
- **Model Size**: While optimized, the combined Dual-AR system is larger than lightweight models like [Kokoro TTS](kokoclone.md).
- **Setup Complexity**: Requires specialized CUDA environments, Docker, or NVIDIA NIM containers for maximum acceleration.

## When to use it
- **High-Fidelity Audio**: When audio quality, natural intonation, and expressiveness are the top priorities.
- **Rapid Voice Cloning**: When you need to clone a voice from a very short sample (less than 30 seconds).
- **GPU-Rich Environments**: When you have access to high-end NVIDIA GPUs to leverage SGLang and TensorRT-LLM acceleration.

## When not to use it
- **CPU-Only Deployment**: Performance is extremely poor on consumer CPUs without dedicated GPU acceleration.
- **Low-Latency Mobile Apps**: The 4B model is too heavy for on-device mobile inference; use [Kokoro TTS](kokoclone.md) instead.
- **Basic Voice Alerts**: For simple notification sounds where expressiveness and complex intonations are unnecessary.

## Getting started

### Installation
```bash
# Clone the repository
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech

# Install dependencies using uv
uv sync --extra vllm
```

### Hello-World
```bash
# Launch the Gradio-based interface
python -m tools.webui
```

## CLI examples

### Generate Speech with Voice Cloning
```bash
python -m tools.llama.generate \
    --text "Hello, this is a test of Fish Audio S2 Pro using the updated late-2026 Dual-AR pipeline." \
    --prompt-text "Reference audio transcript" \
    --prompt-tokens "path/to/reference.wav" \
    --output "output.wav"
```

### Batch Processing from JSON
```bash
python -m tools.llama.generate_batch --config batch_tasks.json --output_dir ./results/
```

### Model Management
```bash
python -m tools.download_models --model-size 4b --lang all
```

## API examples

### Inference via FastAPI (Internal Server)
```python
import requests
from pydantic import BaseModel, Field

class TTSRequest(BaseModel):
    text: str = Field(..., description="The text to synthesize.")
    reference_id: str = Field("target_voice_01", description="Reference speaker ID.")
    format: str = Field("wav", description="Output audio format.")

# Send TTS request to running local instance
response = requests.post(
    "http://localhost:8080/v1/tts",
    json=TTSRequest(
        text="The quick brown fox jumps over the lazy dog [laughing].",
        reference_id="target_voice_01",
        format="wav"
    ).model_dump()
)

with open("output.wav", "wb") as f:
    f.write(response.content)
```

### Using the Python SDK
```python
from fish_speech import FishTTS

tts = FishTTS(model_path="weights/fish-speech-v1.5")
tts.synthesize(
    text="Synthesizing with emotional tags [excited].",
    reference_audio="ref.wav",
    output_path="out.wav"
)
```

## Related tools / concepts
- [KokoClone](kokoclone.md) — Lightweight local alternative for TTS.
- [Whisper](../../services/whisper.md) — SOTA audio transcription.
- [SGLang](../infrastructure/sglang.md) — The inference framework powering Fish Audio's speed.
- [ElevenLabs](elevenlabs.md) — Proprietary industry standard for TTS.
- [NVIDIA](../providers/nvidia.md) — Provider of Rubin GPU architecture and NIM microservices.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for agentic tool and resource connection (MCP 3.1).
- [Audiobookshelf](../../services/inventory.md) — Target service for Fish Audio content.
- [Jellyfin](../../services/jellyfin.md) — Media server for hosting synthesized audio.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Frontier local model often paired with Fish Audio.

## Sources / references
- [Fish Audio GitHub](https://github.com/fishaudio/fish-speech)
- [Fish Audio S2 Technical Report (arXiv:2603.08823)](https://arxiv.org/abs/2603.08823)
- [Fish Audio Blog on Dual-AR Architectures](https://fish.audio/blog/fish-audio-open-sources-s2/)

## Contribution Metadata
- Last reviewed: 2026-09-24
- Confidence: high
