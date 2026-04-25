# Fish Audio

## What it is
Fish Audio is an AI audio platform and model family, notably featuring the **Fish Speech** series, which provides controllable and expressive text-to-speech (TTS) capabilities.

## What problem it solves
It offers high-quality, open-source alternatives to proprietary TTS services. Fish Speech supports voice cloning, emotional expression, and fine-grained control over speech synthesis, which is often missing in standard TTS models.

## Where it fits in the stack
**Category**: AI & Knowledge / Audio / TTS. It serves as a tool for local voice synthesis and expressive audio generation.

## Typical use cases
- **Expressive TTS**: Generating speech with specific emotional tones.
- **Voice Cloning**: Creating a digital voice based on a short sample for personalized assistants.
- **Local Audio Generation**: Running TTS locally to maintain privacy and reduce latency.

## Strengths
- **Open Source**: Provides open-weights models like Fish Speech S2.
- **Controllability**: Allows users to influence prosody and expression.
- **Quality**: Competitive with state-of-the-art TTS models in terms of naturalness.

## Limitations
- **Hardware**: Like most modern AI models, it requires significant GPU resources for optimal performance.
- **Complexity**: Setting up and fine-tuning for specific voices can be more complex than using a managed API.

## When to use it
- When you need high-quality, expressive TTS with local control.
- For voice cloning projects where open-source transparency is valued.

## When not to use it
- If a simple, non-expressive voice is sufficient and low resource usage is preferred.
- If you prefer a fully managed cloud service with no setup required.

## Related tools / concepts
- [Kokoro TTS](./kokoclone.md)
- [Gemini 3.1 Flash TTS](./gemini-flash-tts.md)
- [Whisper](../../services/whisper.md) (for the inverse: speech-to-text)

## Sources / References
- [Fish Audio Official Website](https://fish.audio/)
- [Fish Audio Releases S2: open-source, controllable and expressive TTS model](https://www.reddit.com/r/LocalLLaMA/comments/1rptdpl/fish_audio_releases_s2_opensource_controllable/)
- [Fish Speech GitHub](https://github.com/fishaudio/fish-speech)

## Contribution Metadata
- Last reviewed: 2026-03-15
- Confidence: high
