# Audio Transcription Research: Whisper Variants for Long-Form Audio

## What it is
This research document compares various optimized versions of OpenAI's Whisper model and competing architectures like **SenseVoice**. It focuses on engines and architectural modifications designed to handle long-form audio (podcasts, audiobooks, journals) efficiently within a homelab or self-hosted environment using June 2026 standards.

## What problem it solves
The original Whisper implementation is accurate but computationally expensive and prone to "hallucination loops" during long periods of silence or background noise. This research identifies variants that reduce transcription time by up to 10x while maintaining accuracy and hardware compatibility for typical home servers.

## Where it fits in the stack
This document belongs to the **Layer 0: Infrastructure** and **Process Understanding** layers. It provides the technical rationale for the tools used in audio ingestion pipelines (e.g., `scripts/transcribe_audio.py`).

## Typical use cases
- **Podcast Ingestion**: Transcribing weekly podcasts into searchable markdown notes for a personal knowledge base.
- **Audiobook Search**: Converting personal audiobooks into text to enable semantic search across a library.
- **Voice Memos**: Automatically transcribing and tagging "brain dump" voice memos captured on the go.
- **Meeting Notes**: Providing a self-hosted alternative to cloud-based transcription services for private meetings.
- **Native Diarization**: Identifying multiple speakers in family meetings or collaborative research sessions.

## Strengths
- **Hardware Agnostic**: Includes recommendations for both high-end NVIDIA GPUs and low-power CPU-only NAS devices.
- **Hallucination Resistant**: Specifically highlights models (like Distil-Whisper and Whisper Turbo) that solve the "repetition" bug common in standard Whisper.
- **Quantization-Aware**: Evaluates INT8, FP16, and FP8 performance for optimized inference on mobile and desktop.
- **High Throughput**: Native support for batch processing of multiple files in parallel.

## Limitations
- **Language Gaps**: Many high-speed distilled models (Distil-Whisper) are currently limited to English.
- **VRAM Requirements**: The most accurate models still require ~6-10GB of VRAM, which may exceed entry-level homelab hardware.
- **Engine Diversity**: Requires specialized engines like CTranslate2, `whisper.cpp`, or `mlx-whisper` for maximum performance.

## When to use it
- Use it when designing a new automated audio transcription pipeline.
- Use it to troubleshoot "repetition loops" or slow transcription speeds in an existing setup.
- Use it to decide which GPU or CPU to prioritize for a transcription-focused homelab node.

## When not to use it
- Do not use it for real-time live captioning (streaming transcription), as this research focuses on batch processing of files.
- Do not use it for music-to-sheet-music conversion (see specialized audio analysis tools).

## Getting started (Docker/Local Setup)

### Local Environment Setup
1. **CPU Only (x86_64/ARM)**:
   ```bash
   pip install faster-whisper
   # Use CTranslate2 with INT8 quantization for maximum CPU efficiency
   ```
2. **NVIDIA GPU (CUDA)**:
   ```bash
   pip install faster-whisper
   # Ensure CUDA 12.x and cuDNN 9.x are installed for FP16/FP8 support
   ```

### Docker Deployment
```bash
docker run --rm --gpus all -v $(pwd):/data \
  ghcr.io/systran/faster-whisper:latest \
  --model large-v3 --language en --output_dir /data /data/audio.mp3
```

## CLI examples

### Faster-Whisper CLI
Transcribe a file using the Large-v3 model with beam size 5:
```bash
faster-whisper-transcribe audio.mp3 --model large-v3 --beam_size 5 --task transcribe
```

### SenseVoice CLI
Using the official FunASR tool for diarization-aware transcription:
```bash
funasr-cli --input audio.wav --model SenseVoiceSmall --output_dir ./output
```

### whisper.cpp (Quantized)
Run on low-power devices (like a Raspberry Pi 5) using the Q5_K quantization:
```bash
./main -m models/ggml-large-v3-q5_k.bin -f audio.wav -otxt
```

## API examples

### Faster-Whisper (Python API)
The baseline for homelab integration as of June 2026.

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")

segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
```

### SenseVoice Small via FunASR
Best for native diarization and emotion detection in multi-speaker environments.

```python
from funasr import AutoModel

model = AutoModel(model="iic/SenseVoiceSmall", device="cuda:0")

res = model.generate(input="audio.wav", cache={}, language="auto", use_itn=True)
print(res)
```

## Related tools / concepts
- [Whisper](../services/whisper.md) — The base model and service.
- [Ollama](../services/ollama.md) — For post-transcription summarization and speaker naming.
- [Paperless-ngx](../services/paperless-ngx.md) — For storing and indexing markdown transcripts.
- [Audiobookshelf](../services/audiobookshelf.md) — For source audio management.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — Canonical destination for transcribed knowledge.
- [n8n](../services/n8n.md) — Orchestrating the transcription pipeline.
- [Self-Healing Agent Research](self-healing-agent-research.md) — Broader context for automated system triggers.
- [Faster-Whisper (GitHub)](https://github.com/SYSTRAN/faster-whisper) — The core engine for optimized Whisper.

## Sources / References
- [Faster-Whisper v1.3 Release Notes](https://github.com/SYSTRAN/faster-whisper/releases/tag/v1.3.0)
- [SenseVoice GitHub Repository](https://github.com/FunASR/SenseVoice)
- [Silero VAD V6 Documentation](https://github.com/snakers4/silero-vad)
- [MLX Whisper (Apple Silicon Optimization)](https://github.com/ml-explore/mlx-examples/tree/main/whisper)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
