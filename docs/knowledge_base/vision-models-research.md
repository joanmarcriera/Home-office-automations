# Local Vision Models Research

## What it is
A research summary of local vision-language models (VLMs) and multi-modal models capable of running on homelab hardware. These models allow AI agents to "see" images and videos, providing semantic descriptions, object detection, and visual reasoning as of May 2026.

## What problem it solves
Automates the tagging, captioning, and searchability of home video and image archives (e.g., "Find the video of the birthday party") without relying on cloud services. This ensures family memories remain private while gaining the benefit of modern semantic search and agentic visual understanding.

## Where it fits in the stack
Processes raw video and image files stored on [TrueNAS](../architecture/infrastructure.md) or managed by [Immich](../services/immich.md). It acts as the **Inference Layer** for visual data, feeding structured descriptions into the [Vector Database Comparison](./vector-db-comparison.md) for long-term memory.

## Typical use cases
- **Automated Metadata Generation**: Generating descriptions for home video frames and images.
- **Semantic Media Search**: Natural language search over video content (e.g., "scenes with the dog in the garden").
- **Agentic Visual Reasoning**: Allowing a [Home Admin Agent](./home-admin-agent-architecture.md) to answer questions about the physical world (e.g., "Is the garage door closed in this photo?").
- **Document Analysis**: Advanced OCR and table extraction from complex document images using models like Florence-2.

## Top Local Vision Models (2026)

| Model | Size | Strengths | Best For |
| :--- | :--- | :--- | :--- |
| **InternVL2** | 1B - 76B | State-of-the-art visual reasoning, excellent OCR. | High-accuracy document & scene analysis. |
| **Llama 3.2 Vision** | 11B / 90B | Broad knowledge, excellent instruction following. | General-purpose assistant with vision. |
| **Florence-2** | 0.2B - 0.7B | Extremely fast object detection, segmentation, OCR. | High-throughput metadata tagging. |
| **Moondream2** | 1.6B | Compact, efficient, runs on almost any hardware. | Fast, simple image captioning on CPUs. |
| **Qwen2-VL** | 2B - 72B | Exceptional at document understanding and multi-image. | Multi-page PDF analysis and video-as-images. |

## Strengths
- **Privacy**: Zero-egress processing of sensitive personal media.
- **Cost**: No per-token or per-image costs common with cloud APIs like GPT-4o.
- **Native Integration**: Directly integrates with local storage and n8n workflows.
- **Low Latency**: High-speed processing on local NVIDIA/Apple Silicon hardware.

## Limitations
- **VRAM Intensive**: 11B+ models require 12GB+ VRAM for comfortable inference.
- **Sequential Processing**: Analyzing high-FPS video requires significant compute; pooling or keyframe extraction is mandatory.
- **Accuracy**: While competitive, local models may still lag behind flagship cloud models in extreme edge cases or high-resolution details.

## When to use it
- Use **Whisper** for all audio transcription needs in the homelab.
- Use **CLIP** or **SigLIP** for implementing "search by description" in image/video galleries.
- Use **Florence-2** for specialized tasks like object detection, OCR, and regional captioning.
- Use **Moondream2** for generating quick, natural language captions for personal photos.
- Use **InternVL2** or **Llama 3.2 Vision** when complex reasoning about an image is required.

## When not to use it
- Do not use for real-time video surveillance analysis on low-power CPU-only nodes.
- Do not rely on 100% accuracy for critical forensic identification without human verification.
- Avoid using for long-form video understanding without a robust keyframe extraction or pooling pipeline.

## Implementation Patterns

### 1. Keyframe Extraction (Efficient)
Extract one frame every X seconds or only when significant motion/scene change is detected.
```bash
# Extract one frame every 10 seconds
ffmpeg -i input.mp4 -vf "fps=1/10" frame_%04d.jpg
```

### 2. Video Token Pooling (Advanced)
Some 2026 models support "Video Input" natively by sampling frames and pooling their tokens into a single context window, allowing for better temporal understanding than individual frame analysis.

### 3. Visual RAG
Store image descriptions in a [Vector DB](./vector-db-comparison.md). When a user asks "Where are the photos of the lake?", the agent searches the descriptions to find relevant timestamps/filenames.

## Getting started

### Running InternVL2 via Ollama
InternVL2 is often the 2026 recommendation for high-accuracy local vision.

```bash
# Pull the InternVL2 model (assuming 8B variant)
ollama pull internvl2:8b

# Query with an image
ollama run internvl2:8b "What is in this image?" --image ./kitchen.jpg
```

### Python: Regional Captioning with Florence-2
Florence-2 is superior for finding *where* things are in a frame.

```python
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image

model_id = "microsoft/Florence-2-large"
model = AutoModelForVision2Seq.from_pretrained(model_id, trust_remote_code=True)
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

image = Image.open("backyard.jpg")
prompt = "<DETAILED_CAPTION>"

inputs = processor(text=prompt, images=image, return_tensors="pt")
generated_ids = model.generate(input_ids=inputs["input_ids"], pixel_values=inputs["pixel_values"])
results = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
print(results)
```

## Related tools / concepts
- [Immich](../services/immich.md) — primary gallery for local media.
- [Whisper](../services/whisper.md) — for the audio half of video analysis.
- [Ollama](../services/ollama.md) — the standard for running local VLMs.
- [Paperless-ngx](../services/paperless-ngx.md) — for document-centric vision tasks.
- [Architecture](../architecture/README.md) — for high-level service placement.
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md) — for agentic reasoning over visual data.
- [Vector DB Comparison](./vector-db-comparison.md) — for storing visual embeddings.

## Sources / references
- [Open-GVLab/InternVL GitHub](https://github.com/Open-GVLab/InternVL)
- [Microsoft Florence-2 on Hugging Face](https://huggingface.co/microsoft/Florence-2-large)
- [Meta Llama 3.2 Documentation](https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_2/)
- [Moondream GitHub](https://github.com/vikhyat/moondream)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
