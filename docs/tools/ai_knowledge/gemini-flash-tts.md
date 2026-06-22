# Gemini 3.1 Flash TTS

## What it is
Gemini 3.1 Flash TTS is a next-generation text-to-speech model from Google, designed for low latency and high expressiveness. It is part of the Gemini 3.1 model family and supports native audio generation without requiring a Live WebSocket connection.

## What problem it solves
It provides a way to generate high-quality, expressive AI speech with minimal latency, making it suitable for real-time applications, interactive AI assistants, and long-form content narration. It allows for fine-grained control over tone, pace, and emotion using steerable prompts and expressive tags.

## Where it fits in the stack
**AI & Knowledge / Generative Audio**. It serves as the speech synthesis layer for multimodal AI applications.

## Typical use cases
- **Interactive Assistants**: Real-time voice interaction with LLM-based agents.
- **Content Creation**: Generating high-fidelity voiceovers for videos, podcasts, or audiobooks.
- **Accessibility**: Providing natural-sounding audio versions of text content with emotional depth.
- **Dynamic Narration**: Games or apps that require context-aware speech.

## Strengths
- **Low Latency**: Optimized for fast response times and streaming.
- **Expressiveness**: Supports emotional tags like `[laughs]`, `[sigh]`, and steerable prompts for style (e.g., "friendly and amused").
- **Multilingual**: High-quality support for over 70 languages.
- **Integration**: Uses the standard `generate_content` interface within the Google Gen AI SDK.

## Limitations
- **Proprietary**: Access is controlled by Google via their APIs (AI Studio / Vertex AI).
- **Rate Limits**: Subject to Gemini API quota and usage-based pricing.
- **Preview Status**: Some features and voices are in preview (as of 2026).

## When to use it
- When you need low-latency, high-quality speech synthesis within the Google ecosystem.
- For interactive voice applications where emotional nuance and responsiveness are critical.

## When not to use it
- If your application requires a fully open-source or self-hosted TTS solution.
- For offline use cases without internet access.

## Getting started
Gemini 3.1 Flash TTS is accessible via the Google Gen AI SDK.

### 1. Installation
```bash
pip install google-genai
```

### 2. Hello World (Python)
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

config = types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config={
        "voice_config": {
            "prebuilt_voice_config": {"voice_name": "Kore"}
        }
    }
)

response = client.models.generate_content(
    model="gemini-3.1-flash-tts",
    contents="Hello! Welcome to the future of text-to-speech.",
    config=config
)

# Save the generated audio
audio_bytes = response.candidates[0].content.parts[0].inline_data.data
with open("output.wav", "wb") as f:
    f.write(audio_bytes)
```

## CLI examples
Programmatic access is primarily via REST. You can use `curl` to synthesize speech.

### Basic Speech Synthesis
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "Synthesize this text into a warm, professional voice."}]}],
      "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
          "voiceConfig": {"prebuiltVoiceConfig": {"voice_name": "Callirrhoe"}}
        }
      }
    }'
```

### Synthesis with Expressive Tags
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "[laughs] I did NOT expect that. [sigh] Can you believe it!"}]}],
      "generationConfig": {
        "responseModalities": ["AUDIO"]
      }
    }'
```

### Synthesis with Steerable Prompt
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [
        {"role": "system", "parts": [{"text": "You are a friendly and amused narrator."}]},
        {"role": "user", "parts": [{"text": "Tell me a quick joke about bananas."}]}
      ],
      "generationConfig": {
        "responseModalities": ["AUDIO"]
      }
    }'
```

## API examples

### Streaming Speech Generation
```python
from google import genai
from google.genai import types

client = genai.Client()

config = types.GenerateContentConfig(response_modalities=["AUDIO"])

# Use generate_content_stream for low-latency playback
stream = client.models.generate_content_stream(
    model="gemini-3.1-flash-tts",
    contents="This is a long-form content that will be streamed in chunks.",
    config=config
)

for chunk in stream:
    if chunk.candidates[0].content.parts[0].inline_data:
        # Process audio chunk (e.g., feed to a player)
        audio_chunk = chunk.candidates[0].content.parts[0].inline_data.data
        print(f"Received audio chunk of size: {len(audio_chunk)}")
```

## Related tools / concepts
- [Google Gemini](./google-gemini.md)
- [ElevenLabs](./elevenlabs.md)
- [Google Lyria](./google-lyria.md)
- [Fish Audio](fish-audio.md)
- [Kokoclone](kokoclone.md)
- [Sora](sora.md)
- [Project Genie](project-genie.md)
- [Luma Dream Machine](luma-dream-machine.md)

## Sources / References
- [Gemini 3.1 Flash TTS Announcement](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-tts/)
- [Google AI Studio Audio Documentation](https://ai.google.dev/gemini-api/docs/audio)
- [Gemini 3.1 Flash TTS Preview Model Card](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
