# Fish Audio (Fish Speech)

## What it is
Fish Audio (Fish Speech) is a state-of-the-art multilingual text-to-speech (TTS) platform powered by a Dual-Autoregressive (Dual-AR) architecture. It is designed for high-fidelity, expressive voice synthesis and rapid voice cloning with minimal latency.

## What problem it solves
It provides an open-source, high-performance alternative to proprietary TTS services like ElevenLabs. By using a transformer-based architecture isomorphic to LLMs, it enables fine-grained emotional control and achieves industry-leading Real-Time Factor (RTF) using inference acceleration frameworks.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Audio Generation

## Typical use cases
- **Expressive Narrators**: Generating audiobooks or podcast content with precise emotional cues.
- **Conversational AI**: Powering real-time agents that sound natural and responsive.
- **Voice Cloning**: Creating high-fidelity digital twins from as little as 10-30 seconds of reference audio.
- **Multilingual Content**: Synthesizing speech in over 80 languages without phoneme-level preprocessing.

## Strengths
- **Fine-Grained Emotion Control**: Supports inline natural language tags (e.g., `[whisper]`, `[excited]`, `[laughing]`) to control prosody and emotion at the sub-word level.
- **Innovative Dual-AR Architecture**: Combines a 4B parameter "Slow AR" model for semantic prediction with a 400M parameter "Fast AR" model for acoustic detail reconstruction.
- **Extreme Performance**: Powered by [SGLang](../infrastructure/sglang.md), achieving an RTF of ~0.195 and Time-to-First-Audio (TTFA) of ~100ms on high-end GPUs.
- **RL Alignment**: Uses Group Relative Policy Optimization (GRPO) to align generated speech with human acoustic preferences.

## Limitations
- **Hardware Intensity**: The flagship 4B model requires significant VRAM (ideally NVIDIA H200/A100 or RTX 4090) for optimal throughput.
- **Model Size**: While optimized, the combined Dual-AR system is larger than lightweight models like [Kokoro TTS](kokoclone.md).

## When to use it
- **High-Fidelity Audio**: When audio quality and expressiveness are the top priorities.
- **Rapid Voice Cloning**: When you need to clone a voice from a very short sample (30 seconds).
- **GPU-Rich Environments**: When you have access to high-end NVIDIA GPUs to leverage SGLang acceleration.

## When not to use it
- **CPU-Only Deployment**: Performance will be poor on consumer CPUs without dedicated GPU acceleration.
- **Low-Latency Mobile Apps**: The 4B model is too heavy for on-device mobile inference; use [Kokoro TTS](kokoclone.md) instead.
- **Basic Voice Alerts**: For simple notification sounds where expressiveness isn't required.

## Getting started

### Installation
```bash
# Clone the repository
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech

# Install dependencies using uv
uv sync
```

### CLI Inference
```bash
# Generate speech from text using a reference audio for cloning
python -m tools.llama.generate \
    --text "Hello, this is a test of Fish Audio S2 Pro." \
    --prompt-text "Reference audio transcript" \
    --prompt-tokens "path/to/reference.wav" \
    --output "output.wav"
```

### WebUI
```bash
# Launch the Gradio-based interface
python -m tools.webui
```

## Technical details
- **Architecture**: Dual-Autoregressive Transformer + RVQ Audio Codec (10 codebooks, ~21 Hz).
- **Training Data**: Trained on over 10 million hours of audio data across 80+ languages.
- **Optimization**: Supports Continuous Batching, Paged KV Cache, and RadixAttention-based Prefix Caching via SGLang.
- **Alignment**: Employs Reward Models to score semantic accuracy, timbre similarity, and acoustic preference.

## Related tools / concepts
- [KokoClone](kokoclone.md) — Lightweight local alternative for TTS.
- [Whisper](../../services/whisper.md) — SOTA audio transcription.
- [SGLang](../infrastructure/sglang.md) — The inference framework powering Fish Audio's speed.
- [ElevenLabs](elevenlabs.md) — Proprietary industry standard for TTS.
- [ChatTTS](chatgpt.md) — Conversational-focused TTS models.
- [Audiobookshelf](../../services/inventory.md) — Target service for Fish Audio generated content.
- [Jellyfin](jellyfin.md) — Media server for hosting synthesized audio.

## Sources / references
- [Fish Audio GitHub](https://github.com/fishaudio/fish-speech)
- [Fish Audio S2 Technical Report (arXiv:2603.08823)](https://arxiv.org/abs/2603.08823)
- [Fish Audio Blog](https://fish.audio/blog/fish-audio-open-sources-s2/)

## Contribution Metadata
- Last reviewed: 2026-05-17
- Confidence: high
