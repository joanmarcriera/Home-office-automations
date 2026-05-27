# OpenAI Whisper

## What it is
OpenAI Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web. As of May 2026, optimizations like **Faster-Whisper v1.2.x** and **Whisper.cpp** provide the foundation for high-performance local transcription.

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

### Streaming API (Speaches)
[Speaches](https://github.com/speaches-ai/speaches) (formerly `faster-whisper-server`) provides an OpenAI-compatible API for streaming transcription using Faster-Whisper.

```python
import openai

client = openai.OpenAI(base_url="http://localhost:8000/v1", api_key="cant-be-empty")

with open("audio.wav", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="base",
        file=audio_file,
        response_format="text"
    )
    print(transcription)
```

## Hardware Benchmarking (May 2026)
Whisper performance depends on hardware acceleration and model quantization.

| Hardware | Model | Backend | Time for 10m Audio | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Raspberry Pi 5 | base | Whisper.cpp | ~8m | CPU-only, slow but viable. |
| Intel i7 (14th Gen) | medium | Faster-Whisper | ~1.5m | Optimized with `int8` quantization. |
| Apple M4 Pro | large-v3 | Whisper.cpp | ~40s | Leveraging CoreML/MLX. |
| NVIDIA RTX 4070 | large-v3 | Faster-Whisper | ~15s | FP16, batched inference. |
| NVIDIA RTX 4090 | large-v3 | Faster-Whisper | ~8s | Peak throughput for batch jobs. |

## Advanced: Transcript Post-processing (Python)
Raw transcripts often contain filler words or minor hallucinations. This script demonstrates a cleanup pass using a local LLM (Ollama).

```python
import requests

def cleanup_transcript(text):
    """
    Use a local LLM to clean up transcription artifacts.
    """
    url = "http://localhost:11434/api/generate"
    prompt = f"Clean up this transcript by removing filler words and fixing grammar, but keep the meaning: {text}"

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    return response.json().get('response', '')

raw_text = "Um, so, like, the meeting was, uh, scheduled for Tuesday at 3pm."
print(cleanup_transcript(raw_text))
```

## Real-time & n8n Automation
For real-time transcription or automated pipelines, Whisper is often integrated into orchestration tools like [n8n](n8n.md).

### n8n Workflow Pattern: Automated Transcription
A common pattern involves using a local Whisper server (like Speaches) to process audio files triggered by events (e.g., a new file in a folder or a webhook from a phone).

1. **Trigger**: Webhook or File Watcher (e.g., Local File Trigger).
2. **Binary Data**: Fetch the audio file into a binary property.
3. **HTTP Request**:
    - **Method**: POST
    - **URL**: `http://whisper-server:8000/v1/audio/transcriptions`
    - **Send Binary Data**: Checked.
    - **Body Parameters**: `model=base`, `response_format=json`.
4. **LLM Processing**: Send the resulting text to [Ollama](ollama.md) for summarization or action item extraction.
5. **Output**: Save the transcript to Obsidian or send a notification via Telegram.

## Related tools / concepts
- [Ollama](ollama.md) — for processing transcribed text with local LLMs
- [n8n](n8n.md) — for automating audio ingestion and transcription workflows
- [Audiobookshelf](audiobookshelf.md) — for managing transcribed audio libraries
- [Piper](../tools/ai_knowledge/piper.md) — for local Text-to-Speech (the inverse of Whisper)
- [Home Assistant](home-assistant.md) — for integrating Whisper into voice-controlled home automation
- [SearXNG](searXNG.md) — for searching through transcribed knowledge bases
- [MLX](../tools/frameworks/mlx.md) — for optimized execution on Apple Silicon.

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-26)

## Contribution Metadata
- Last reviewed: 2026-05-26
- Confidence: high

## Sources / References
- [Whisper GitHub](https://github.com/openai/whisper)
- [Whisper.cpp GitHub](https://github.com/ggerganov/whisper.cpp)
- [Faster-Whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [Speaches GitHub](https://github.com/speaches-ai/speaches)
