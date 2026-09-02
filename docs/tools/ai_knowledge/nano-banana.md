# Nano Banana

## What it is
Nano Banana is Google's conversation-driven generative image editor and design assistant integrated directly inside Google AI Studio and Vertex AI. Operating natively on Google's multimodal foundation models (**Gemini 4.0 Ultra** and **Gemini 4.0 Flash Image**), it allows developers and designers to create, refine, inpaint, and edit complex graphical layouts using natural language dialogue instead of manual masking tools.

Key capabilities of the early 2027 ecosystem include:
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
Use Python with `google-genai` and Pydantic v2 schemas to validate image generation requests.

```python
import base64
from google import genai
from pydantic import BaseModel, Field, ConfigDict


class ImageGenerationRequest(BaseModel):
    """Pydantic v2 schema for validating image creation inputs."""
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=5, description="Prompt describing desired image output.")
    model_name: str = Field(default="gemini-4.0-flash-image", description="Target Gemini image model.")


def generate_initial_image(request: ImageGenerationRequest, output_filename: str = "base_setup.png"):
    client = genai.Client()

    interaction = client.interactions.create(
        model=request.model_name,
        input=request.prompt
    )

    image_bytes = base64.b64decode(interaction.output_image.data)
    with open(output_filename, "wb") as f:
        f.write(image_bytes)

    print(f"Generated base image successfully! Saved with Interaction ID: {interaction.id}")
    return interaction.id


if __name__ == "__main__":
    req = ImageGenerationRequest(
        prompt="A stylized illustration of a computer setup with neon lighting on a wooden desk."
    )
    print(f"Validated generation request for model: {req.model_name}")
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
    "model": "gemini-4.0-flash-image",
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
    "model": "gemini-4.0-flash-image",
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
    "model": "gemini-4.0-pro-image",
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
The following script demonstrates multi-turn visual editing using `google-genai` and Pydantic v2.

```python
import base64
from google import genai
from pydantic import BaseModel, Field, ConfigDict


class IterativeEditRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=3)
    previous_interaction_id: str = Field(...)


def execute_design_iteration(request: IterativeEditRequest, output_filename: str = "watch_step2.png"):
    client = genai.Client()

    step2 = client.interactions.create(
        model="gemini-4.0-flash-image",
        input=request.prompt,
        previous_interaction_id=request.previous_interaction_id
    )

    image_bytes = base64.b64decode(step2.output_image.data)
    with open(output_filename, "wb") as f:
        f.write(image_bytes)

    print("Multi-turn visual edit executed successfully!")
    return step2.id


if __name__ == "__main__":
    req = IterativeEditRequest(
        prompt="Now change the leather strap of the watch to a modern metallic mesh band.",
        previous_interaction_id="interaction_12345"
    )
    print(f"Validated edit step for previous interaction ID: {req.previous_interaction_id}")
```

### 2. Batch Background Swapping and Color Harmonization
Programmatically edit multiple variations of a product photo using `google-genai`.

```python
import base64
from google import genai
from pydantic import BaseModel, Field
from typing import List


class BatchSwapRequest(BaseModel):
    backgrounds: List[str] = Field(..., min_items=1)
    base_image_path: str = Field(...)


def generate_banner_variants(request: BatchSwapRequest):
    client = genai.Client()

    with open(request.base_image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    results = []
    for bg in request.backgrounds:
        response = client.interactions.create(
            model="gemini-4.0-flash-image",
            input=[
                {"type": "text", "text": f"Isolate the central object and place it on a {bg} background."},
                {"type": "image", "mime_type": "image/png", "data": base64_image}
            ]
        )
        results.append(response)
    return results


if __name__ == "__main__":
    req = BatchSwapRequest(
        backgrounds=["marble countertop", "wooden terrace"],
        base_image_path="/tmp/product.png"
    )
    print(f"Prepared batch swap for {len(req.backgrounds)} background variations.")
```

## Related tools / concepts
- [Gemini](gemini.md)
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
- Last reviewed: 2027-01-07
- Confidence: high
