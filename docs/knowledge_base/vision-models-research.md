# Local Vision Models Research

## What it is
A research summary of local vision-language models (VLMs) and multi-modal models capable of running on homelab hardware. These models allow AI agents to "see" images and videos, providing semantic descriptions, object detection, and visual reasoning as of June 2026.

## What problem it solves
Automates the tagging, captioning, and searchability of home video and image archives (e.g., "Find the video of the birthday party") without relying on cloud services. This ensures family memories remain private while gaining the benefit of modern semantic search and agentic visual understanding.

## Where it fits in the stack
Processes raw video and image files stored on [TrueNAS](../architecture/infrastructure.md) or managed by [Immich](../services/immich.md). It acts as the **Inference Layer** for visual data, feeding structured descriptions into the [Vector Database Comparison](./vector-db-comparison.md) for long-term memory.

## Typical use cases
- **Automated Metadata Generation**: Generating descriptions for home video frames and images.
- **Semantic Media Search**: Natural language search over video content (e.g., "scenes with the dog in the garden").
- **Agentic Visual Reasoning**: Answering questions about the physical world (e.g., "Is the garage door closed in this photo?").
- **Document Analysis**: Advanced OCR and table extraction from complex document images using models like Florence-2.
- **AssistantBench Evaluation**: Using web agents to perform tasks that require visual understanding of web pages.

## Strengths
- **Privacy**: Zero-egress processing of sensitive personal media.
- **Cost**: No per-token or per-image costs common with cloud APIs like GPT-4o or Gemini 3.5.
- **Native Integration**: Directly integrates with local storage and n8n workflows.
- **Low Latency**: High-speed processing on local NVIDIA/Apple Silicon hardware.

## Limitations
- **VRAM Intensive**: 11B+ models require 12GB+ VRAM for comfortable inference.
- **Sequential Processing**: Analyzing high-FPS video requires significant compute; pooling or keyframe extraction is mandatory.
- **Accuracy**: While competitive, local models may still lag behind flagship cloud models like Claude 4.8 or Gemini 3.5 in extreme edge cases.

## Top Local & Cloud Vision Models (June 2026)

| Model | Size | Strengths | Best For |
| :--- | :--- | :--- | :--- |
| **InternVL2** | 1B - 76B | State-of-the-art visual reasoning, excellent OCR. | High-accuracy document & scene analysis. |
| **Claude 4.8 Opus**| Cloud | Unmatched visual reasoning and spatial awareness. | Complex multi-modal orchestration. |
| **Gemini 3.5 Pro** | Cloud | 2M+ context window, native video understanding. | Long-form video analysis and large PDF sets. |
| **Florence-2** | 0.2B - 0.7B | Extremely fast object detection, segmentation, OCR. | High-throughput metadata tagging. |
| **Moondream2** | 1.6B | Compact, efficient, runs on almost any hardware. | Fast, simple image captioning on CPUs. |
| **Qwen2.5-VL** | 2B - 72B | Exceptional at document understanding and multi-image. | Multi-page PDF analysis. |

## When to use it
- Use **Florence-2** for specialized tasks like object detection and regional captioning.
- Use **Moondream2** for generating quick, natural language captions on low-power hardware.
- Use **InternVL2** or **Llama 3.2 Vision** when complex reasoning about an image is required locally.
- Use **Gemini 3.5 Pro** for analyzing entire movies or 1,000+ page document sets.

## When not to use it
- Do not use for real-time video surveillance analysis on low-power CPU-only nodes.
- Do not rely on 100% accuracy for critical forensic identification without human verification.
- Avoid local models for extremely high-resolution "needle in a haystack" visual search.

## Getting started

### Running InternVL2 via Ollama
InternVL2 is the 2026 recommendation for high-accuracy local vision.

```bash
# Pull the InternVL2 model (assuming 8B variant)
ollama pull internvl2:8b

# Query with an image
ollama run internvl2:8b "What is in this image?" --image ./kitchen.jpg
```

## CLI examples

### Keyframe Extraction with FFmpeg
```bash
# Extract one frame every 10 seconds for analysis
ffmpeg -i input.mp4 -vf "fps=1/10" frame_%04d.jpg
```

### Batch Image Captioning (Moondream CLI)
```bash
moondream-cli --image_dir ./photos --output captions.json
```

## API examples

### Python: Document Parsing with Qwen2.5-VL
```python
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from PIL import Image

model = Qwen2_5_VLForConditionalGeneration.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")
processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")

image = Image.open("invoice.pdf_page1.png")
inputs = processor(text="Extract all items from this invoice into a table.", images=image, return_tensors="pt")
generated_ids = model.generate(**inputs)
```

## Related tools / concepts
- [Immich](../services/immich.md) - Primary gallery for local media.
- [Whisper](../services/whisper.md) - For the audio half of video analysis.
- [Ollama](../services/ollama.md) - The standard for running local VLMs.
- [Paperless-ngx](../services/paperless-ngx.md) - For document-centric vision tasks.
- [Architecture](../architecture/README.md) - For high-level service placement.
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md) - For agentic reasoning.
- [Vector DB Comparison](./vector-db-comparison.md) - For storing visual embeddings.
- [OCRmyPDF](../tools/process_understanding/ocrmypdf.md) - For adding searchable layers to documents.
- [Tesseract](../tools/process_understanding/tesseract.md) - Core OCR engine.
- [Claude](../tools/ai_knowledge/claude.md) - Frontier multi-modal model.

## Sources / references
- [Open-GVLab/InternVL GitHub](https://github.com/Open-GVLab/InternVL)
- [Microsoft Florence-2 on Hugging Face](https://huggingface.co/microsoft/Florence-2-large)
- [Meta Llama 3.2 Documentation](https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_2/)
- [AssistantBench: Web Agent Benchmark](https://github.com/clovaai/AssistantBench)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
