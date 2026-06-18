# OpenAI Whisper

## What it is
OpenAI Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web. As of June 2026, optimizations like **Faster-Whisper v1.2.x** and **Whisper.cpp** provide the foundation for high-performance local transcription, integrated with frontier models like Claude 4.8 Opus for post-processing.

## What problem it solves
Transcribing audio manually is time-consuming and expensive. Whisper provides high-accuracy transcription, translation, and language identification, allowing for the automation of meeting notes, video subtitling, and voice-controlled interfaces. It is particularly notable for its robustness to accents, background noise, and technical language.

## Where it fits in the stack
**Category**: Services / AI & Machine Learning. It serves as the **audio perception layer** in a local AI stack, converting voice input into text that can then be processed by LLMs or other automation tools.

## Typical use cases
- Transcribing recorded meetings or lectures for searchability.
- Generating subtitles for videos in multiple languages.
- Building voice-activated home automation commands.
- Translating foreign language audio into English text.
- Enriching local media libraries (e.g., [Audiobookshelf](audiobookshelf.md)) with full-text search.
- **Hardware-Accelerated Transcription**: Optimized performance across a variety of hardware from Raspberry Pi 5 to NVIDIA RTX 4090.

### Hardware Benchmarking (June 2026)

| Hardware | Model | Backend | Time for 10m Audio | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Raspberry Pi 5 | base | Whisper.cpp | ~8m | CPU-only, slow but viable. |
| Intel i7 (14th Gen) | medium | Faster-Whisper | ~1.5m | Optimized with `int8` quantization. |
| Apple M4 Pro | large-v3 | Whisper.cpp | ~40s | Leveraging CoreML/MLX. |
| NVIDIA RTX 4070 | large-v3 | Faster-Whisper | ~15s | FP16, batched inference. |
| NVIDIA RTX 4090 | large-v3 | Faster-Whisper | ~8s | Peak throughput for batch jobs. |

## Strengths
- **High Accuracy**: Competes with professional human transcribers in many languages.
- **Multilingual**: Supports transcription in dozens of languages and translation into English.
- **Robustness**: Handles background noise and various accents exceptionally well.
- **Local Execution**: Can be run entirely offline (via Whisper.cpp or Faster-Whisper), ensuring data privacy.
- **Batched Inference**: Faster-Whisper v1.2.x supports optimized batched processing for up to 4x speed increases.

## Limitations
- **Resource Intensive**: Larger models (`large-v3-turbo`) require significant GPU VRAM or CPU power.
- **No Real-time (Native)**: The base Whisper model is designed for batch processing, though optimized versions like Whisper.cpp support streaming.
- **Hallucination**: Can occasionally hallucinate text during long periods of silence or music (partially mitigated by Silero-VAD V6).

## When to use it
- When you need high-quality, private, and free transcription of audio files.
- When building local AI assistants that require voice input.
- For processing legacy audio archives at scale.

## When not to use it
- If you require extremely low-latency, real-time transcription on low-power mobile devices (without using optimized C++ ports).
- If you need a managed service with built-in speaker diarization (Whisper identifies *what* was said, but not always *who* said it).

## Getting started

### Installation (Python)
```bash
pip install openai-whisper
```

### Installation (Faster-Whisper)
Optimized version using CTranslate2.
```bash
pip install faster-whisper
```

### Hello World
1. Install Whisper: `pip install openai-whisper`
2. Run via CLI:
```bash
whisper audio.mp3 --model base
```

## CLI examples

The `whisper` CLI is the simplest way to process audio files.

```bash
# Transcribe a file using the medium model
whisper audio.wav --model medium

# Transcribe and translate a Spanish audio file to English
whisper spanish_audio.mp3 --language Spanish --task translate

# Output transcription in specific formats (txt, vtt, srt, tsv, json)
whisper audio.m4a --output_format srt
```

## API examples

### Python (Standard Whisper)
```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")

print(result["text"])
```

### Python (Faster-Whisper v1.2.x)
Featuring **Batched Inference** and **Silero-VAD V6** for improved speed and accuracy.
```python
from faster_whisper import WhisperModel, BatchedInferencePipeline

model_size = "large-v3-turbo"
# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")
batched_model = BatchedInferencePipeline(model)

# Use Silero-VAD V6 for voice activity detection
segments, info = batched_model.transcribe("audio.mp3", batch_size=16)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
```

### Advanced: Transcript Post-processing with Claude 4.8 Opus
Raw transcripts often contain filler words or minor hallucinations. This script demonstrates a cleanup pass using Claude 4.8 Opus via [LiteLLM](litellm.md).

```python
import requests

def cleanup_transcript(text):
    """
    Use Claude 4.8 Opus to clean up transcription artifacts.
    """
    # Using LiteLLM as a unified proxy
    url = "http://localhost:4000/chat/completions"
    headers = {"Authorization": "Bearer sk-1234"}

    prompt = f"Clean up this transcript by removing filler words and fixing grammar, but keep the meaning: {text}"

    payload = {
        "model": "claude-4-8-opus-20260528",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

raw_text = "Um, so, like, the meeting was, uh, scheduled for Tuesday at 3pm."
print(cleanup_transcript(raw_text))
```

### n8n Automation Pattern
For real-time transcription or automated pipelines, Whisper is often integrated into orchestration tools like [n8n](n8n.md).

1. **Trigger**: Webhook or File Watcher.
2. **HTTP Request**: POST to a [Speaches](https://github.com/speaches-ai/speaches) server.
3. **LLM Processing**: Send result to [Ollama](ollama.md) or [LiteLLM](litellm.md) (using Claude 4.8 Opus) for summarization.
4. **Output**: Save to Obsidian or send via Telegram.

## Related tools / concepts
- [Ollama](ollama.md) — for processing transcribed text with local LLMs
- [n8n](n8n.md) — for automating audio ingestion and transcription workflows
- [Audiobookshelf](audiobookshelf.md) — for managing transcribed audio libraries
- [Piper](../tools/ai_knowledge/piper.md) — for local Text-to-Speech (the inverse of Whisper)
- [Home Assistant](home-assistant.md) — for integrating Whisper into voice-controlled home automation
- [SearXNG](searXNG.md) — for searching through transcribed knowledge bases
- [MLX](../tools/frameworks/mlx.md) — for optimized execution on Apple Silicon.
- [LiteLLM](litellm.md) — for unified proxying to frontier models like Claude 4.8 Opus.

## Sources / References
- [Whisper GitHub](https://github.com/openai/whisper)
- [Whisper.cpp GitHub](https://github.com/ggerganov/whisper.cpp)
- [Faster-Whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [Speaches GitHub](https://github.com/speaches-ai/speaches)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
