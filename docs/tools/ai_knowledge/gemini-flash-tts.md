# Gemini 3.1 Flash TTS

## What it is
Gemini 3.1 Flash TTS is a next-generation text-to-speech model from Google, designed for low latency and high expressiveness. It is part of the Gemini 3.1 model family.

## What problem it solves
It provides a way to generate high-quality, expressive AI speech with minimal latency, making it suitable for real-time applications and interactive AI assistants.

## Where it fits in the stack
**AI & Knowledge / Generative Audio**. It serves as the speech synthesis layer for multimodal AI applications.

## Typical use cases
- **Interactive Assistants**: Real-time voice interaction with LLM-based agents.
- **Content Creation**: Generating voiceovers for videos or articles.
- **Accessibility**: Providing high-quality audio versions of text content.

## Strengths
- **Low Latency**: Optimized for fast response times.
- **Expressiveness**: Capable of generating natural-sounding speech with varied prosody.
- **Integration**: Part of the broader Google Gemini ecosystem.

## Limitations
- **Proprietary**: Access is controlled by Google via their APIs.
- **Cost**: Usage-based pricing in AI Studio or Vertex AI.

## When to use it
- When you need low-latency, high-quality speech synthesis within the Google ecosystem.
- For interactive voice applications where responsiveness is critical.

## When not to use it
- If your application requires a fully open-source or self-hosted TTS solution.
- For tasks where simple, non-expressive speech is sufficient and cost is the primary concern.

## Getting started

### API Examples (Google AI Studio)

You can use the `gemini-1.5-flash` (or newer) endpoints for TTS tasks.

#### Python Snippet
```python
import os
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel('gemini-1.5-flash')
# Note: Check the latest documentation for specific TTS-dedicated model strings
# or generative audio parameters.

# Experimental audio generation
response = model.generate_content("Generate speech for: 'Hello, welcome to the future of TTS.'")
# Save or stream the response.audio data
```

#### cURL Example
```bash
curl https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GOOGLE_API_KEY \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{"text": "Synthesize this text into a warm, professional voice."}]
      }]
    }'
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

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
