# Local Vision Models Research

## What it is
A research summary of local vision-language models (VLMs) and transcription models capable of running on homelab hardware for media archival.

## What problem it solves
Automates the tagging and searchability of home video archives (e.g., "Find the video of the birthday party") without relying on cloud services.

## Where it fits in the stack
Processes raw video files stored on TrueNAS/Immich to extract semantic metadata and searchable transcripts.

## Typical use cases
- Generating descriptions for home video frames using CLIP.
- Transcribing family interviews or audiobooks using Whisper.
- Semantic search over video content in a local media management system.

## Strengths
- **CLIP (Contrastive Language-Image Pre-training)**: Excellent at mapping images and text to a shared embedding space for search.
- **Whisper**: Industry-standard accuracy for local transcription across multiple languages.
- **Moondream2**: A tiny VLM (~1.6B parameters) that can run on very low-power hardware while providing decent image descriptions.

## Limitations
- High GPU VRAM requirements for larger models (e.g., LLaVA).
- Processing long video files can be time-consuming on CPU-only nodes.

## When to use it
- Use **Whisper (Faster-Whisper)** for all transcription needs due to its efficiency.
- Use **CLIP** for implementing "search by description" in image/video galleries.
- Use **Moondream2** for generating natural language captions on edge devices.

## When not to use it
- Do not use for real-time video analysis if the hardware lacks a modern GPU (RTX 3060+ or Mac Silicon).

## Related tools / concepts
- [Immich](../../services/immich.md)
- [Whisper](../../services/whisper.md)
- [Ollama](../../services/ollama.md)

## Sources / references
- [OpenAI CLIP](https://github.com/openai/CLIP)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Moondream GitHub](https://github.com/vikhyat/moondream)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
