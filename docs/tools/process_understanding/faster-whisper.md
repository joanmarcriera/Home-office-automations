# faster-whisper

## What it is
faster-whisper is a reimplementation of OpenAI's Whisper speech-to-text model using the [CTranslate2](https://github.com/OpenNMT/CTranslate2) inference engine. It produces the same transcripts as Whisper while running roughly **4x faster** and using significantly less memory, with support for 8-bit and float16 quantization on both CPU and GPU. It runs **fully offline** once a model is downloaded.

## What problem it solves
Reference Whisper is accurate but slow and memory-hungry, which makes large transcription backlogs painful on home-lab hardware. faster-whisper makes local, private transcription practical: it transcribes audio quickly on a CPU or a modest GPU, with no cloud speech API and no audio ever leaving the machine.

## Where it fits in the stack
**Process & Understanding / Speech-to-text.** It is the transcription engine that feeds downstream pipelines — turning voice notes, meeting recordings, or scanned-media audio into text for [Paperless-ngx](../../services/paperless-ngx.md), Obsidian notes, or RAG indexes. It is the engine behind many self-hosted transcription front-ends.

## Typical use cases
- Batch-transcribing a backlog of recordings offline on a TrueNAS box or MacBook.
- Adding searchable transcripts to archived audio/video before ingestion into [Paperless-ngx](../../services/paperless-ngx.md).
- Powering a local voice-to-text step in an [n8n](../../services/n8n.md) automation.
- Generating subtitles/captions for a personal media library.

## Strengths
- **Fast and lightweight:** ~4x faster than reference Whisper with lower memory via CTranslate2.
- **Offline and private:** no cloud dependency; audio stays local.
- **Quantization options:** int8/float16 let large models run on commodity hardware.
- **Word-level timestamps & VAD:** built-in voice-activity detection improves long-audio accuracy.

## Limitations
- **Library, not an app:** it is a Python package — you build or adopt a front-end around it.
- **Model accuracy ceiling:** inherits Whisper's limits on heavy accents, overlapping speech, and rare languages.
- **GPU setup:** GPU acceleration needs a compatible CUDA/cuDNN stack.

## When to use it
- When you need **offline**, fast, private transcription at volume on local hardware.
- As the engine inside a self-hosted transcription or note-taking pipeline.
- When reference Whisper is too slow or too memory-heavy for your machine.

## When not to use it
- When you want a turnkey GUI rather than a library to integrate.
- For real-time, ultra-low-latency streaming at scale (specialized streaming ASR may fit better).
- When the highest possible accuracy on difficult audio outweighs local/offline constraints.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes (runs entirely locally)

## Related tools / concepts
- [Whisper](../../services/whisper.md) — The reference model faster-whisper reimplements.
- [Paperless-ngx](../../services/paperless-ngx.md) — Common downstream destination for transcripts.
- [Ollama](../../services/ollama.md) — Pair with a local LLM to summarize transcripts offline.
- [n8n](../../services/n8n.md) — Orchestrate transcription as an automation step.
- [MLX](../infrastructure/mlx.md) — Apple-silicon backend for accelerated local inference.
- [Docling](docling.md) — Local document parser for the text side of ingestion.
- [Audiobookshelf](../../services/audiobookshelf.md) — Self-hosted audio library that benefits from transcripts.
- [Apache Tika](../../services/tika.md) — Content/text extraction companion in ingestion pipelines.

## Sources / references
- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [CTranslate2](https://github.com/OpenNMT/CTranslate2)
- [OpenAI Whisper](https://github.com/openai/whisper)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
