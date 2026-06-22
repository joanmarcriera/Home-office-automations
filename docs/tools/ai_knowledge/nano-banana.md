# Nano Banana

## What it is
Nano Banana (often associated with Gemini 2.0 Flash or specifically the image generation/editing "tool" within Google AI Studio) is a conversational AI image editor developed by Google. It allows users to create and modify images through natural language dialogue.

## What problem it solves
Traditional image editing (Photoshop, GIMP) requires significant technical skill and familiarity with complex toolsets. Nano Banana lowers the barrier to entry by allowing users to describe changes (e.g., "remove the background," "change the shirt color to blue") and seeing them executed instantly.

## Where it fits in the stack
It fits within the **AI Assistants & Knowledge** and **Creative & Communication** layers. It serves as a specialized utility for multi-modal AI interactions, particularly for users already utilizing the Google AI ecosystem (Gemini, AI Studio).

## Typical use cases
- **Rapid Prototyping:** Quickly iterating on visual concepts via chat.
- **Social Media Content:** Applying stylized edits or background swaps to photos.
- **Inpainting/Outpainting:** Adding or extending elements in an existing image through natural language.
- **Background Removal:** Cleanly isolating subjects without manual masking.

## Strengths
- **Ease of Use:** Conversational interface makes professional-level edits accessible to non-experts.
- **Speed:** Optimized for fast inference (hence the "Nano" naming convention in the Gemini family).
- **Identity Consistency:** Aims to maintain the identity of subjects across multiple edits.
- **Integration:** Part of the broader Google AI Studio toolset.

## Limitations
- **Ecosystem Lock-in:** Primarily available through Google's AI surfaces.
- **Emerging Tech:** As a newer tool, it may occasionally hallucinate or misinterpret complex spatial prompts.
- **Control Precision:** Chat-based editing can sometimes lack the "pixel-perfect" control required by professional designers compared to manual tools.

## When to use it
Use Nano Banana when you need quick, high-quality image edits or generations and prefer describing the result rather than manually manipulating tools.

## When not to use it
Avoid it for highly sensitive or professional-grade design work that requires absolute precision, or if you require an offline, privacy-first image editing workflow.

## Getting started
Nano Banana is accessible via the Google AI Studio interface or programmatically through the Google Gen AI SDK.

### 1. Installation
```bash
pip install google-genai
```

### 2. Hello World (Python)
```python
from google import genai
import base64

client = genai.Client(api_key="YOUR_API_KEY")

# Simple image generation
interaction = client.interactions.create(
    model="gemini-3.1-flash-image",
    input="A futuristic city in the style of cyberpunk, with neon lights and flying cars.",
)

# Save the generated image
with open("output.png", "wb") as f:
    f.write(base64.b64decode(interaction.output_image.data))
```

## CLI examples
Programmatic access is primarily via REST. You can use `curl` to interact with the models directly.

### Generate Image from Text
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.1-flash-image",
    "input": [{"type": "text", "text": "A minimal logo for a tech startup called BananaNano"}]
  }'
```

### Edit Existing Image
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.1-flash-image",
    "input": [
      {"type": "text", "text": "Change the color of the shirt to blue"},
      {"type": "image", "mime_type": "image/png", "data": "'"$(base64 -w 0 image.png)"'"}
    ]
  }'
```

### High-Resolution Generation
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-pro-image",
    "input": "A cinematic wide shot of a desert landscape at sunset",
    "response_format": {"type": "image", "image_size": "4K"}
  }'
```

## API examples
The Interactions API supports multi-turn conversations and advanced "Thinking" processes.

### Multi-turn Image Editing
```python
from google import genai

client = genai.Client()

# Step 1: Generate initial image
interaction = client.interactions.create(
    model="gemini-3.1-flash-image",
    input="Create a vibrant infographic about photosynthesis."
)

# Step 2: Refine the image using the previous interaction ID
interaction_v2 = client.interactions.create(
    model="gemini-3.1-flash-image",
    input="Now translate all text in the image to Spanish.",
    previous_interaction_id=interaction.id
)

# Access the refined image
print(interaction_v2.output_image.mime_type)
```

## Related tools / concepts
- [Gemini](gemini.md)
- [Runway ML](runwayml.md)
- [DALL-E 3 / ChatGPT](chatgpt.md)
- [Project Genie](project-genie.md)
- [Sora](sora.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [Jasper](jasper.md)
- [Copy.ai](copy-ai.md)
- [Midjourney](index.md)

## Sources / references
- [Google AI Studio](https://aistudio.google.com)
- [Gemini Image Generation Overview](https://gemini.google/overview/image-generation/)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
