# Gemini 3.1 Flash TTS

## What it is
Gemini 3.1 Flash TTS is a highly optimized, low-latency text-to-speech model developed by Google. Built natively on the Gemini 3.x multimodal architecture, it allows developers to synthesize expressive, human-like speech from raw text without requiring a persistent, high-overhead Live WebSocket session. It supports steerable speech options and emotional markers natively embedded in text streams.

Key capabilities of the late August 2026 release include:
- **Zero-Shot Steerable Voices**: Dynamically change vocal characteristics (e.g., gender, age, breathiness, resonance) through natural language system instructions.
- **In-Context Emotion Tagging**: Interject natural physical responses like laughter, sighs, pauses, or vocal inflections natively using markdown-style tags (e.g., `[laughs]`, `[whispering]`, `[sigh]`).
- **Natively Multilingual Processing**: High-fidelity, accent-aware speech synthesis across more than 75 languages, with automatic pronunciation code switching inside the same text payload.
- **Google Gen AI Unified SDK Support**: Directly integrations with the late 2026 `google-genai` library using the standard `generate_content` and `generate_content_stream` APIs.

## What problem it solves
Traditional text-to-speech architectures rely on a distinct dual-model process: an LLM generates text, and a standalone TTS model synthesizes it. This separation introduces notable round-trip latency and strips away emotional context. Gemini 3.1 Flash TTS unifies these steps into a single multimodal sequence, enabling conversational latency (under 150ms) and highly contextual emotional depth.

## Where it fits in the stack
**AI & Knowledge / Generative Audio**. It serves as the speech generation and output layer for real-time agentic voice assistants and customer support systems.

## Typical use cases
- **Agentic Conversational Coworkers**: Providing natural voice interfaces for desktop coworkers (like Khoj Pipali v2.0).
- **Interactive Narrative Generation**: Voicing dynamically generated role-playing video games with emotional depth.
- **Automated Audio Newsletters**: Automatically parsing daily text summaries (e.g., AI Daily Digests) into high-fidelity morning podcast voiceovers.
- **Sovereign Accessibility Layers**: Creating real-time, context-aware screen readers that adapt their tone based on the urgency of website notifications.

## Strengths
- **Incredible Latency Figures**: Sub-150ms time-to-first-byte (TTFB), ideal for conversational pacing.
- **Rich Emotional Range**: Authentic non-verbal sounds and breath simulations that eliminate the robotic cadence of standard TTS pipelines.
- **Unified Parameter Architecture**: Manage text generation parameters and speech output configurations under a single API call.

## Limitations
- **Google Ecosystem Dependency**: Completely proprietary model gated behind Google AI Studio and Vertex AI API pricing structures.
- **Strict Rate Limits**: High-frequency real-time applications require upfront quota negotiations to prevent 429 errors.

## When to use it
- When building zero-latency interactive voice response (IVR) systems or dynamic conversational agents.
- For applications running natively on Google Cloud Platform that require seamless integration with Google Gen AI frameworks.
- When your voice synthesis needs emotional flexibility that changes on-the-fly depending on the content.

## When not to use it
- If your application requires a completely local, self-hosted, or offline speech-generation loop (use native offline [AudioCPP](../ai_knowledge/audiocpp.md) or Coqui TTS forks instead).
- If you need a cloned voice replication of a specific user with minimal training samples (use [ElevenLabs](elevenlabs.md) or specialized cloning engines).

## Getting started

### 1. SDK Installation and Configuration
To utilize the late 2026 Gemini 3.1 Flash TTS model, you must install the modern Google Gen AI SDK.

```bash
pip install google-genai pydantic
```

Set your API token in your local shell session:
```bash
export GEMINI_API_KEY="AIzaSyYourKeyHere..."
```

### 2. Hello World Voice Generation (Python)
Generate an audio clip using a predefined voice preset.

```python
from google import genai
from google.genai import types

# Initialize the late 2026 client
client = genai.Client()

# Configure response modalities for AUDIO output
config = types.GenerateContentConfig(
    response_modalities=["AUDIO"],
    speech_config={
        "voice_config": {
            "prebuilt_voice_config": {"voice_name": "Kore-Expressive"}
        }
    }
)

response = client.models.generate_content(
    model="gemini-3.1-flash-tts",
    contents="Hello from the unified Google Gen AI library. Audio generation is now fully integrated!",
    config=config
)

# Extract and save inline audio bytes
audio_bytes = response.candidates[0].content.parts[0].inline_data.data
with open("welcome_speech.wav", "wb") as f:
    f.write(audio_bytes)

print("Synthesized audio written to welcome_speech.wav")
```

## CLI examples
You can interface with Google's generative endpoints using standard shell commands and `curl`.

### 1. Standard Audio Generation with Specific Preset Voice
Request speech synthesis for a block of text using the "Callirrhoe" voice preset.

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "Welcome back! Connecting you to your local smart home server now."}]}],
      "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
          "voiceConfig": {"prebuiltVoiceConfig": {"voice_name": "Callirrhoe"}}
        }
      }
    }' > raw_synthesis_response.json
```

### 2. Synthesis using In-Context Expressive Inflections
Pass custom emotional cues within your prompt string to trigger laughter or pauses.

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "[laughs] Oh wow! I completely forgot about that. [sigh] Let me check again."}]}],
      "generationConfig": {
        "responseModalities": ["AUDIO"]
      }
    }' > expressive_response.json
```

### 3. Steerable Tone using a System Instruction
Instruct the narrator to speak in a specific style.

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [
        {"role": "system", "parts": [{"text": "You are a friendly, highly enthusiastic tech support agent."}]},
        {"role": "user", "parts": [{"text": "I solved the bug!"}]}
      ],
      "generationConfig": {
        "responseModalities": ["AUDIO"]
      }
    }' > support_tone_response.json
```

## API examples
For complex software platforms, real-time chunked streaming ensures playback starts before the full response is generated.

### 1. Real-Time Streaming Audio Generation (Python API)
Use `generate_content_stream` to receive audio chunks sequentially as they are synthesized.

```python
import os
from google import genai
from google.genai import types

def stream_speech_to_speaker(text_input: str):
    client = genai.Client()

    # Configure the generation loop for low-latency streaming
    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config={
            "voice_config": {
                "prebuilt_voice_config": {"voice_name": "Puck-Interactive"}
            }
        },
        temperature=0.4
    )

    stream = client.models.generate_content_stream(
        model="gemini-3.1-flash-tts",
        contents=text_input,
        config=config
    )

    chunk_counter = 0
    for chunk in stream:
        try:
            # Check if inline audio data exists in the chunk
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            if inline_data:
                audio_chunk_bytes = inline_data.data
                chunk_counter += 1
                print(f"Received audio chunk #{chunk_counter} - ({len(audio_chunk_bytes)} bytes)")

                # In a live app, you would pass these bytes directly into a PyAudio stream
                # e.g., pyaudio_stream.write(audio_chunk_bytes)
        except (AttributeError, IndexError):
            continue

if __name__ == "__main__":
    test_text = "Let us stream this audio track. Real-time feedback is crucial for voice assistants."
    stream_speech_to_speaker(test_text)
```

### 2. Multi-Turn Speech Generation with Continuous Context
Maintain conversational history so that the synthesizer is aware of previous statements.

```python
from google import genai
from google.genai import types

def generate_conversational_response():
    client = genai.Client()

    chat = client.chats.create(
        model="gemini-3.1-flash-tts",
        config=types.GenerateContentConfig(response_modalities=["AUDIO"])
    )

    # First message
    response_1 = chat.send_message("What is the speed of sound?")
    # Second message (retains context)
    response_2 = chat.send_message("Does it go faster in water?")

    audio_data = response_2.candidates[0].content.parts[0].inline_data.data
    with open("conversational_followup.wav", "wb") as f:
        f.write(audio_data)
    print("Conversational followup voice generated successfully!")
```

## Related tools / concepts
- [Gemini](./gemini.md)
- [ElevenLabs](./elevenlabs.md)
- [Google Lyria](./google-lyria.md)
- [Fish Audio](fish-audio.md)
- [Kokoclone](kokoclone.md)
- [Sora](sora.md)
- [Project Genie](project-genie.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [AudioCPP](../ai_knowledge/audiocpp.md)

## Sources / References
- [Gemini 3.1 Flash TTS Product Page](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-tts/)
- [Google AI Studio Audio Integration Guide](https://ai.google.dev/gemini-api/docs/audio)
- [Google Gen AI SDK Developer Portal](https://ai.google.dev/gemini-api/docs/quickstart)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
