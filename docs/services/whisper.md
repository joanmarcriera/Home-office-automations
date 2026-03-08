# OpenAI Whisper

Whisper is a versatile speech recognition model.

## Description
It can perform multilingual speech recognition, speech translation, and language identification. In this setup, it is typically run locally (via Whisper.cpp or Faster-Whisper) to provide transcription services.

## Typical use cases
- **Meeting Transcription**: Converting recorded meetings into text for archival and search.
- **Subtitling**: Generating SRT or VTT files for video content.
- **Voice Commands**: Processing local voice input for home automation.
- **Translation**: Translating spoken foreign languages into English text.

## When to use it
- When you need high-accuracy, privacy-preserving speech-to-text.
- When you want to avoid per-minute cloud transcription costs.
- When working with multiple languages or low-quality audio.

## When not to use it
- For real-time, ultra-low latency requirements (unless using optimized versions like `whisper-stream`).
- If you lack sufficient CPU/GPU resources for local inference.

## Getting started

### Installation (Whisper.cpp)
Clone the repository and build the project:

```bash
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
cmake -B build
cmake --build build -j --config Release
```

### Download Model
Download a quantized model (e.g., base):

```bash
./models/download-ggml-model.sh base.en
```

## CLI examples

### Basic Transcription
Transcribe a 16-bit WAV file:

```bash
./build/bin/whisper-cli -m models/ggml-base.en.bin -f samples/jfk.wav
```

### Export to Subtitles
Generate an SRT file:

```bash
./build/bin/whisper-cli -m models/ggml-base.en.bin -f input.wav --output-srt
```

## API examples

### Whisper Server (OpenAI-compatible)
Start the local HTTP server:

```bash
./build/bin/whisper-server -m models/ggml-base.en.bin --port 8080
```

Transcribe via `curl`:

```bash
curl http://localhost:8080/inference \
  -H "Content-Type: multipart/form-data" \
  -F "file=@samples/jfk.wav" \
  -F "temperature=0.0" \
  -F "language=en"
```

## Links
- [GitHub Repository (OpenAI)](https://github.com/openai/whisper)
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)

## Alternatives
- [Deepgram](https://www.deepgram.com/) (Cloud)
- [AssemblyAI](https://www.assemblyai.com/) (Cloud)

## Backlog
- Implement real-time transcription for meetings via n8n.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-08

## Sources / References
- https://github.com/openai/whisper
- https://github.com/ggerganov/whisper.cpp
- https://github.com/ggerganov/whisper.cpp/blob/master/examples/server/README.md
- https://www.deepgram.com/
