# Moondream

Moondream is a tiny, high-performance vision-language model (VLM) designed to run efficiently on edge devices and local hardware. As of July 2026, Moondream 3.1 features a sparse mixture-of-experts (MoE) architecture that delivers frontier-level visual reasoning, object detection, and segmentation within a remarkably small parameter footprint.

## What it is
Moondream is a multi-function VLM that excels at interpreting visual data. Unlike traditional large-scale VLMs, Moondream is optimized for speed and resource efficiency, making it the preferred choice for real-time applications like "computer use" agents and mobile vision tasks. It supports complex queries, captioning, object detection, pointing (coordinate extraction), and segmentation.

## What problem it solves
It bridges the gap between massive, resource-heavy vision models and the need for low-latency, privacy-preserving visual intelligence. Many home-office automation tasks—such as describing a security camera still or identifying a button in a UI—do not require the multi-billion parameter overhead of a model like [Claude 4.8](../ai_knowledge/claude.md). Moondream provides high-accuracy visual understanding with minimal VRAM and power consumption.

## Where it fits in the stack
**Perception Layer**. It serves as the visual "eyes" for autonomous agents. Within a [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) ecosystem, Moondream acts as a specialized tool for transforming raw pixels into structured data that reasoning models like [Gemma 3](local_llms.md) can act upon.

## Typical use cases
- **Computer Use Agents**: Identifying UI elements (buttons, fields) for robotic process automation (RPA).
- **Home Security**: Real-time scene tagging and anomaly detection (e.g., "Is there a package on the porch?").
- **Media Cataloging**: Generating descriptive captions for image galleries in [Immich](../../services/immich.md).
- **Accessibility**: Providing real-time visual descriptions for visually impaired users on mobile devices.
- **Edge OCR**: Extracting text from documents and labels in [Paperless-ngx](../../services/paperless-ngx.md) without cloud dependencies.

## Strengths
- **Efficiency**: Extremely low latency; can run on CPUs and mobile NPUs with high throughput.
- **Versatility**: Native support for detection, pointing, and segmentation in addition to standard captioning.
- **Privacy**: Local-first design ensures sensitive visual data never leaves the user's hardware.
- **Commercial Friendly**: Released under permissive licenses suitable for both personal and enterprise use.
- **MoE Architecture**: The 3.1 version uses 9B total parameters with only 2B active during inference, balancing depth and speed.

## Limitations
- **Reasoning Depth**: While excellent for visual tasks, it lacks the deep world-knowledge of frontier models for complex multi-step logical reasoning.
- **Context Window**: Optimized for single-image or short-video bursts; not intended for long-form video analysis like [Gemini](../../tools/ai_knowledge/gemini.md).
- **Niche Optimization**: Best used for specific "what/where" visual questions rather than creative storytelling.

## When to use it
- When you need visual intelligence on a device with limited VRAM (e.g., < 4GB).
- For real-time applications where sub-100ms response times are critical.
- When privacy mandates local processing of camera feeds or screenshots.
- As a specialized visual pre-processor for a larger agentic workflow.

## When not to use it
- For complex visual reasoning that requires deep domain knowledge (e.g., professional medical image analysis).
- For generating long, creative, or stylistically complex descriptions.
- If you have ample VRAM and require the absolute highest reasoning benchmarks (use [InternVL2](../../knowledge_base/vision-models-research.md)).

## Getting started

### Installation
The official Python client is the recommended way to interact with Moondream.

```bash
pip install moondream
```

### Local Deployment (Photon)
To run Moondream locally with high performance, use the Photon inference engine:
1. Download the Moondream weights from Hugging Face.
2. Run the Photon server (requires NVIDIA GPU or Apple Silicon).

```bash
# Example starting the local server
python -m moondream.server --model ./moondream-3b.photon
```

## CLI examples
Moondream provides a straightforward CLI for quick tests and shell scripting.

```bash
# Caption an image
moondream caption --image ./living_room.jpg

# Query an image for specific details
moondream query --image ./shelf.jpg --prompt "How many red boxes are on the middle shelf?"

# Object detection (returns bounding boxes)
moondream detect --image ./street.jpg --prompt "pedestrians"

# Pointing (returns x,y coordinates)
moondream point --image ./desktop.png --prompt "the close window button"
```

## API examples

### Simple Captioning (Python)
This example uses the Moondream Cloud or a local Photon instance.

```python
import moondream as md
from PIL import Image

# Initialize the model (requires MD_API_KEY for cloud or local URL for Photon)
model = md.vl(api_key="YOUR_API_KEY")

image = Image.open("sample.jpg")

# Generate a caption
response = model.caption(image)
print(f"Caption: {response.caption}")

# Specific Query
query_res = model.query(image, "Is there a dog in the image?")
print(f"Query Result: {query_res.answer}")
```

### Object Detection and Pointing
Moondream's specialized functions for agentic interaction.

```python
import moondream as md
from PIL import Image

model = md.vl(api_key="YOUR_API_KEY")
image = Image.open("ui_screenshot.png")

# Detect UI elements
detect_res = model.detect(image, "buttons")
for obj in detect_res.objects:
    print(f"Found button at: {obj.bbox}")

# Point to a specific element for a 'click' action
point_res = model.point(image, "the search bar")
print(f"Click coordinates: x={point_res.x}, y={point_res.y}")
```

## Related tools / concepts
- [Vision Models Research](../../knowledge_base/vision-models-research.md) — Comprehensive VLM landscape.
- [Local LLMs](local_llms.md) — Running reasoning models on-premises.
- [Immich](../../services/immich.md) — Self-hosted photo management.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document archival and OCR.
- [Ollama](../../services/ollama.md) — Alternative local model hosting.
- [Gemma 3](local_llms.md) — Complementary local reasoning model.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Orchestration protocol.
- [Tool Calling & MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Agentic patterns.

## Sources / references
- [Moondream Official Website](https://moondream.ai/)
- [Moondream GitHub Repository](https://github.com/m87-labs/moondream)
- [Moondream PyPI Package](https://pypi.org/project/moondream/)
- [Moondream Examples](https://github.com/m87-labs/moondream-examples)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
