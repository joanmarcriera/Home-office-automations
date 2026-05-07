# Google Gemini

## What it is
Google Gemini is a family of multimodal large language models developed by Google DeepMind. It represents Google's most capable AI, spanning from mobile-optimized models (Nano) to high-performance frontier models (Pro and Ultra/1.5).

## What problem it solves
It provides state-of-the-art reasoning across text, code, images, audio, and video. Notably, its 1.5 Pro version introduced a massive 1-million to 2-million token context window, solving the problem of analyzing extremely large documents, long video files, or massive codebases in a single pass.

## Where it fits in the stack
**Provider / LLM**. It serves as a primary reasoning engine for agents and applications requiring deep multimodal understanding or extremely large context processing.

## Typical use cases
- **Long Context Analysis**: Processing entire books, hour-long videos, or large repositories.
- **Multimodal Workflows**: Extracting information from images and audio without separate OCR or transcription steps.
- **Enterprise Integration**: Seamlessly connecting with Google Cloud (Vertex AI) and Google Workspace data.

## Strengths
- **Massive Context Window**: Industry-leading token limit (up to 2M).
- **Native Multimodality**: Built from the ground up to reason across different modalities.
- **Integration**: Strong ties to Google Cloud and the Android ecosystem.
- **Performance**: Highly competitive reasoning and coding capabilities, particularly in the 1.5 Pro and Flash variants.

## Limitations
- **Privacy**: Like other proprietary models, data is processed on Google's infrastructure.
- **API Complexity**: Can be more complex to configure compared to simpler text-only APIs.
- **Safety Filtering**: Can sometimes be overly aggressive in its safety guardrails, impacting some technical workflows.

## When to use it
- When your task requires processing contexts larger than 200k-300k tokens.
- For complex multimodal tasks involving video or multi-image reasoning.
- If your infrastructure is already heavily invested in Google Cloud/Vertex AI.

## When not to use it
- For tasks where a local, private model is required.
- For simple, low-latency text tasks where a faster or cheaper model (like DeepSeek or a local Llama) would suffice.

## Getting started
1. Visit [Google AI Studio](https://aistudio.google.com/) and sign in with your Google account.
2. Create an API Key.
3. Use the Chat interface to test prompts or the "Get Code" button to generate snippets for your preferred language.
4. For mobile-first integration, explore the [Gemini Nano](https://ai.google.dev/gemini-api/docs/gemini-nano) documentation.

## CLI examples
Google provides the `gcloud` CLI and specialized SDK wrappers for terminal interaction.

```bash
# Generate content via curl using your API key
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{ "contents": [{ "parts":[{"text": "Write a story about a magic backpack."}]}] }'

# Use the Gemini CLI (if installed via npm/pip wrappers)
gemini-cli chat --model gemini-1.5-pro

# List available models via gcloud
gcloud ai models list --region=us-central1
```

## API examples
The `google-generativeai` Python SDK is the primary way to interact with Gemini.

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("What is the capital of France?")
print(response.text)
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (via Google AI Studio or Vertex AI), with a generous free tier available for developers in AI Studio.
- **Self-hostable**: No (though smaller variants like Gemma are open-weights).

## Related tools / concepts
- [OpenAI](./openai.md)
- [Anthropic](../providers/anthropic.md)
- [DeepSeek](../providers/deepseek.md)
- [OpenRouter](./openrouter.md)
- [Gemini CLI](gemini-cli.md)
- [Gemini for macOS](gemini-macos.md)
- [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md)

## Sources / References
- [Google Gemini Official Page](https://deepmind.google/technologies/gemini/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google API Keys Weren't Secrets. But then Gemini Changed the Rules](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)

## Contribution Metadata
- Last reviewed: 2026-06-01
- Confidence: high
