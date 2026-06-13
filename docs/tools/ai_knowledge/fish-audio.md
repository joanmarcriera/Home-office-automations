# Fish Audio (Fish Speech)

## What it is
Fish Audio (Fish Speech) is a state-of-the-art multilingual text-to-speech (TTS) platform powered by a Dual-Autoregressive (Dual-AR) architecture. It is designed for high-fidelity, expressive voice synthesis and rapid voice cloning with minimal latency. It is one of the most advanced open-source audio models available in June 2026.

## What problem it solves
It provides an open-source, high-performance alternative to proprietary TTS services like ElevenLabs. By using a transformer-based architecture isomorphic to LLMs, it enables fine-grained emotional control and achieves industry-leading Real-Time Factor (RTF) using inference acceleration frameworks. It allows `claude-4-8-opus-20260528` and GPT-5.5 based agents to communicate with human-like prosody and emotional depth.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Audio Generation. It serves as the premium audio generation layer for high-end agentic systems.

## Typical use cases
- **Expressive Narrators**: Generating audiobooks or podcast content with precise emotional cues.
- **Conversational AI**: Powering real-time agents that sound natural and responsive in customer service or companionship roles.
- **Voice Cloning**: Creating high-fidelity digital twins from as little as 10-30 seconds of reference audio.
- **Multilingual Content**: Synthesizing speech in over 80 languages without complex phoneme-level preprocessing.

## Strengths
- **Fine-Grained Emotion Control**: Supports inline natural language tags (e.g., `[whisper]`, `[excited]`, `[laughing]`) for sub-word emotional prosody.
- **Innovative Dual-AR Architecture**: Combines a 4B parameter "Slow AR" model for semantic prediction with a 400M parameter "Fast AR" model for acoustic detail.
- **Extreme Performance**: Powered by [SGLang](../infrastructure/sglang.md), achieving an RTF of ~0.195 and TTFA of ~100ms on high-end GPUs.
- **RL Alignment**: Uses Group Relative Policy Optimization (GRPO) to align generated speech with human acoustic preferences.
- **Scalability**: Designed to handle massive batch inference for production workloads.

## Limitations
- **Hardware Intensity**: The flagship 4B model requires significant VRAM (ideally NVIDIA H200/A100 or RTX 4090) for optimal throughput.
- **Model Size**: The combined Dual-AR system is significantly larger than lightweight models like [Kokoro TTS](kokoclone.md).
- **Setup Complexity**: Requires a robust environment with specific CUDA and Python dependencies for maximum performance.

## When to use it
- **High-Fidelity Audio**: When audio quality, realism, and expressiveness are the top priorities.
- **Rapid Voice Cloning**: When you need to clone a voice with high accuracy from a very short sample.
- **GPU-Rich Environments**: When you have access to enterprise-grade NVIDIA GPUs to leverage SGLang acceleration.

## When not to use it
- **CPU-Only Deployment**: Performance is insufficient on consumer CPUs for real-time applications.
- **Low-Latency Mobile Apps**: The 4B model is too heavy for on-device mobile inference; consider [Kokoro TTS](kokoclone.md).
- **Basic Voice Alerts**: For simple notification sounds where expressiveness is unnecessary.

## Getting started
Fish Speech is best installed using `uv` for dependency management. An NVIDIA GPU with at least 24GB VRAM is recommended for the 4B model.

```bash
# Clone and install
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
uv sync --extra accel
```

## CLI examples
### 1. Simple Inference
Generate speech with a reference audio for cloning.
```bash
python -m tools.llama.generate \
    --text "The future of audio generation is open-source." \
    --prompt-text "Reference transcript" \
    --prompt-tokens "path/to/ref.wav" \
    --output "output.wav"
```

### 2. Emotional Tagging
Use natural language tags to control the emotion of the generated speech.
```bash
python -m tools.llama.generate \
    --text "[laughing] I can't believe how good Fish Speech sounds!" \
    --output "laugh.wav"
```

### 3. API Server Mode
Launch the server to handle gRPC or HTTP requests.
```bash
python -m tools.api_server --listen 0.0.0.0:8000
```

## API examples
Programmatic usage via the Fish Speech Python SDK.

```python
from fish_speech import FishSpeech

client = FishSpeech(api_key="your_key_or_local")
audio = client.generate(
    text="Synthesizing expressive speech for June 2026.",
    emotion="excited",
    reference_id="cloned-voice-01"
)
audio.save("output.wav")
```

## Related tools / concepts
- [KokoClone](kokoclone.md) — Efficient, lightweight local TTS alternative.
- [SGLang](../infrastructure/sglang.md) — The inference acceleration framework for Fish Audio.
- [Whisper](../../services/whisper.md) — SOTA speech-to-text for audio processing.
- [ElevenLabs](elevenlabs.md) — The proprietary benchmark for TTS quality.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Connecting Fish Audio to agentic toolsets.
- [Audiobookshelf](../../services/inventory.md) — Popular target for hosting Fish Audio content.
- [Jellyfin](../../services/jellyfin.md) — Media server for streaming synthesized audiobooks.

## Sources / references
- [Fish Audio GitHub](https://github.com/fishaudio/fish-speech)
- [Fish Audio S2 Technical Report (arXiv:2603.08823)](https://arxiv.org/abs/2603.08823)
- [Fish Audio Blog: S2 Open Source Release](https://fish.audio/blog/fish-audio-open-sources-s2/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
