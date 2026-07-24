# faster-whisper

## What it is
faster-whisper is a high-performance reimplementation of OpenAI's Whisper speech-to-text model using the [CTranslate2](https://github.com/OpenNMT/CTranslate2) inference engine. It produces identical transcripts as Whisper while running roughly **4x to 6x faster** and using significantly less memory. It features support for 8-bit and float16 quantization on both CPU and GPU, running fully offline once the model is cached. As of late August 2026, it natively supports **Whisper v3-turbo** and advanced CTranslate2 v4.x optimizations.

## What problem it solves
Reference Whisper is accurate but slow and memory-hungry, which makes large transcription backlogs painful on home-lab and consumer hardware. faster-whisper makes local, private transcription highly practical: it transcribes hours of audio quickly on a CPU or a modest GPU, with no cloud speech API dependencies and no audio ever leaving the machine.

## Where it fits in the stack
**Process & Understanding / Speech-to-text.** It is the transcription engine that feeds downstream pipelines — turning voice notes, meeting recordings, or scanned-media audio into text for [Paperless-ngx](../../services/paperless-ngx.md), Obsidian notes, or RAG indexes. It is the engine behind many self-hosted transcription front-ends.

## Typical use cases
- Batch-transcribing a backlog of recordings offline on a TrueNAS box or MacBook.
- Adding searchable transcripts to archived audio/video before ingestion into [Paperless-ngx](../../services/paperless-ngx.md).
- Powering a local voice-to-text step in an [n8n](../../services/n8n.md) automation.
- Generating subtitles/captions for a personal media library or video search indexing.

## Strengths
- **Fast and lightweight:** ~4x to 6x faster than reference Whisper with lower memory via CTranslate2 execution.
- **Whisper v3-turbo Support**: Native support for the ultra-fast turbo models with high-fidelity outputs.
- **Offline and private:** no cloud dependency; audio stays local.
- **Quantization options:** int8/float16 let large models run on commodity hardware.
- **Word-level timestamps & VAD:** built-in Silero voice-activity detection (VAD) improves long-audio accuracy.

## Limitations
- **Library, not an app:** it is a Python package — you build or adopt a front-end around it.
- **Model accuracy ceiling:** inherits Whisper's limits on heavy accents, overlapping speech, and rare languages.
- **GPU setup:** GPU acceleration needs a compatible CUDA/cuDNN or Apple-silicon MLX stack.

## When to use it
- When you need **offline**, fast, private transcription at volume on local hardware.
- As the engine inside a self-hosted transcription or note-taking pipeline.
- When reference Whisper is too slow or too memory-heavy for your machine.

## When not to use it
- When you want a turnkey GUI rather than a library to integrate.
- For real-time, ultra-low-latency streaming at scale (specialized streaming ASR may fit better).
- When the highest possible accuracy on difficult audio outweighs local/offline constraints.

## Getting started

### Installation
```bash
pip install faster-whisper
```

### Basic Usage
```python
from faster_whisper import WhisperModel

# Initialize model (downloads on first run)
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")

# Transcribe audio file
segments, info = model.transcribe("audio.mp3", beam_size=5)

print(f"Detected language '{info.language}' with probability {info.language_probability:.2f}")

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

## CLI examples

### 1. Simple Transcription via Python one-liner
```bash
python3 -c "from faster_whisper import WhisperModel; m=WhisperModel('large-v3-turbo'); s,_=m.transcribe('audio.mp3'); [print(seg.text) for seg in s]"
```

### 2. Using community CLI (whisper-ctranslate2)
```bash
# Install CLI tool
pip install whisper-ctranslate2

# Transcribe with the CLI using large-v3-turbo and float16 on GPU
whisper-ctranslate2 audio.mp3 --model large-v3-turbo --device cuda --compute_type float16
```

## API examples

### 1. Word-level Timestamps & Custom Dictionary
Injecting initial prompt vocabulary to guide model output on technical jargon.
```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cpu")
segments, _ = model.transcribe(
    "audio.mp3",
    word_timestamps=True,
    initial_prompt="PydanticAI, Model Context Protocol, MCP, Claude 5.1"
)

for segment in segments:
    for word in segment.words:
        print(f"[{word.start:.2f}s -> {word.end:.2f}s] {word.word}")
```

### 2. Advanced Voice Activity Detection (VAD) Filtering
```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cpu")
# Enable VAD filter to skip non-speech parts with fine-tuned thresholds
segments, _ = model.transcribe(
    "audio.mp3",
    vad_filter=True,
    vad_parameters=dict(
        threshold=0.5,
        min_speech_duration_ms=250,
        max_speech_duration_s=float('inf'),
        min_silence_duration_ms=500
    )
)

for segment in segments:
    print(segment.text)
```

## Related tools / concepts
- [Whisper](../../services/whisper.md) — The reference model faster-whisper reimplements.
- [Paperless-ngx](../../services/paperless-ngx.md) — Common downstream destination for transcripts.
- [Ollama](../../services/ollama.md) — Pair with a local LLM to summarize transcripts offline.
- [n8n](../../services/n8n.md) — Orchestrate transcription as an automation step.
- [MLX](../infrastructure/mlx.md) — Apple-silicon backend for accelerated local inference.
- [Docling](docling.md) — Local document parser for the text side of ingestion.
- [Audiobookshelf](../../services/audiobookshelf.md) — Self-hosted audio library that benefits from transcripts.
- [Apache Tika](../../services/tika.md) — Content/text extraction companion in ingestion pipelines.
- [Ragas](ragas.md) — Evaluating the quality of transcription-fed RAG pipelines.

## Sources / references
- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [CTranslate2 GitHub](https://github.com/OpenNMT/CTranslate2)
- [OpenAI Whisper](https://github.com/openai/whisper)

## Contribution Metadata
- Last reviewed: 2026-08-03
- Confidence: high
