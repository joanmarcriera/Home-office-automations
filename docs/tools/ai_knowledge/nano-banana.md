# Nano Banana

## What it is
Nano Banana is Google's conversation-driven generative image editor and design assistant integrated directly inside Google AI Studio and Vertex AI. Operating natively on Google's late August 2026 multimodal foundation models, it allows developers and designers to create, refine, inpaint, and edit complex graphical layouts using natural language dialogue instead of manual masking tools.

Key capabilities of the late August 2026 ecosystem include:
- **Unified Interactions API**: Run conversational, multi-turn image generation and modifications, where each turn builds upon the spatial layout of previous iterations.
- **Natural Language Masking & Inpainting**: Describe edits in plain language (e.g., "swap the background for a neon-lit cyberpunk street") without requiring hand-drawn bounding boxes.
- **Identity & Object Preservation**: Advanced spatial-attention mechanisms that maintain consistent facial features, product dimensions, or logos across multiple revisions.
- **Integrated Thinking Pipeline**: Leverages Google's reasoning traces to dynamically analyze layout structure, lighting, and object depth before applying edits.

## What problem it solves
Traditional graphical editing pipelines (e.g., Photoshop, GIMP) are tedious and require deep technical expertise. Early text-to-image models lack revision control—any modification to a prompt generates a completely new image, destroying valuable layout progress. Nano Banana provides true non-destructive, conversational editing with exact continuity.

## Where it fits in the stack
It fits within the **AI Assistants & Knowledge** and **Creative & Communication** layers. It serves as a specialized image manipulation utility for multi-modal AI interactions, particularly for developers utilizing Google's API ecosystem.

## Typical use cases
- **Interactive Prototyping**: Generating and editing user interface layouts, promotional banners, and visual storyboards using high-speed chat.
- **Identity-Consistent Product Design**: Placing an existing base product mockup into varied lifestyle scenes (e.g., "place this water bottle on a marble kitchen counter next to fresh lemons").
- **Asset Localization**: Quickly translating text inside banner graphics or modifying regional elements for global marketing campaigns.
- **Creative Visual Storytelling**: Progressively illustrating graphic novels or video scene concepts turn-by-turn.

## Strengths
- **Logical Continuation**: Maintains high fidelity of untouched elements during localized modifications.
- **Zero Masking Friction**: Natural language understanding eliminates the need for manual cropping or lassoing.
- **High Infill Consistency**: Generates replacement pixels that perfectly match the lighting, shadowing, and grain of the original photograph.

## Limitations
- **Google Cloud Lock-In**: Exclusively tied to Google AI Studio, Vertex AI, and Google's proprietary image model licenses.
- **Fine Pixel Control**: For extreme professional precision (such as exact typography curves or vector paths), manual vector editors are still required.

## When to use it
- When you want to programmatically generate and refine visual elements iteratively through a conversation loop.
- For business workflows requiring rapid, bulk background swaps and object placements with high lighting consistency.
- When building creative co-writing or storyboarding assistants that need continuous visual updates.

## When not to use it
- If your graphic design workflow requires offline processing, local GPU deployment, or open-weight models (use local Stable Diffusion with ControlNet instead).
- If your primary focus is video generation or long-form video editing (use [Sora](sora.md) or Luma Dream Machine).

## Getting started

### 1. Library Installation and Authentication
Configure your environment to run Google's generative interactions APIs.

```bash
pip install google-genai pillow pydantic
```

Obtain a key from Google AI Studio and expose it globally:
```bash
export GEMINI_API_KEY="AIzaSyYourKeyHere..."
```

### 2. Conversational Generation Quickstart
Use Python to generate an initial illustration.

```python
import base64
from google import genai

client = genai.Client()

# Generate an initial base image using the latest flash image model
interaction = client.interactions.create(
    model="gemini-3.1-flash-image",
    input="A stylized illustration of a computer setup with neon lighting on a wooden desk."
)

# Extract and write base64 image data
image_bytes = base64.b64decode(interaction.output_image.data)
with open("base_setup.png", "wb") as f:
    f.write(image_bytes)

print(f"Generated base image successfully! Saved with Interaction ID: {interaction.id}")
```

## CLI examples
Interact with Google's image models directly using REST and `curl`.

### 1. Generating a Graphic from Text
Request a fresh illustration using standard terminal commands.

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.1-flash-image",
    "input": [{"type": "text", "text": "A minimalist corporate logo featuring a green banana inside a sleek gear."}]
  }' > logo_response.json
```

### 2. Performing an In-Context Edit with an Input Image
Upload an existing file as a base64 string and instruct Nano Banana to alter the clothing color.

```bash
# Encode your local image file to base64
export BASE_IMAGE_B64=$(base64 -w 0 input_photo.png)

curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.1-flash-image",
    "input": [
      {"type": "text", "text": "Swap the gray sweater the person is wearing to a bright yellow hoodie."},
      {"type": "image", "mime_type": "image/png", "data": "'"$BASE_IMAGE_B64"'" }
    ]
  }' > edited_photo_response.json
```

### 3. High-Resolution Studio Quality Request
Leverage Google's professional-grade image model with custom dimensions.

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-pro-image",
    "input": "A cinematic landscape shot of misty mountains at sunrise, ultra-realistic",
    "response_format": {
      "type": "image",
      "image_size": "2048x2048"
    }
  }' > studio_response.json
```

## API examples
For complex multi-turn editing systems, retaining previous interaction contexts is vital.

### 1. Multi-Turn Visual Editing (Python API)
The following script demonstrates how to create a visual design loop where subsequent requests build upon previous outputs using the `previous_interaction_id` field.

```python
import base64
from google import genai

def execute_design_iteration():
    client = genai.Client()

    # Step 1: Generate initial graphic
    step1 = client.interactions.create(
        model="gemini-3.1-flash-image",
        input="A vector illustration of a modern smartwatch displaying health statistics."
    )

    # Write Step 1 output
    with open("watch_step1.png", "wb") as f:
        f.write(base64.b64decode(step1.output_image.data))

    print(f"Initial ID: {step1.id}")

    # Step 2: Instruct model to edit the smartwatch, retaining the design context
    step2 = client.interactions.create(
        model="gemini-3.1-flash-image",
        input="Now change the leather strap of the watch to a modern metallic mesh band.",
        previous_interaction_id=step1.id
    )

    # Write Step 2 output
    with open("watch_step2.png", "wb") as f:
        f.write(base64.b64decode(step2.output_image.data))

    print("Multi-turn visual edit executed successfully!")

if __name__ == "__main__":
    execute_design_iteration()
```

### 2. Batch Background Swapping and Color Harmonization
Programmatically edit multiple variations of a product photo.

```python
from google import genai
import base64

def generate_banner_variants(base_image_path: str, backgrounds: list):
    client = genai.Client()

    with open(base_image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    for idx, bg in enumerate(backgrounds):
        response = client.interactions.create(
            model="gemini-3.1-flash-image",
            input=[
                {"type": "text", "text": f"Isolate the central object and place it on a {bg} background."},
                {"type": "image", "mime_type": "image/png", "data": base64_image}
            ]
        )
        # Process and write response output...
```

## Related tools / concepts
- [Google Gemini](google-gemini.md)
- [Gemini 3.1 Flash TTS](gemini-flash-tts.md)
- [Sora](sora.md)
- [Project Genie](project-genie.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [Midjourney](index.md)
- [Runway ML](runwayml.md)

## Sources / references
- [Google AI Studio Image API Overview](https://aistudio.google.com)
- [Gemini Image Generation Reference Documentation](https://gemini.google/overview/image-generation/)
- [Google Gen AI SDK Quickstart Guides](https://ai.google.dev/gemini-api/docs/quickstart)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
