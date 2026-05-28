# Local Vision Models Research

## What it is
A research summary of local vision-language models (VLMs) and transcription models capable of running on homelab hardware for media archival. These models allow AI agents to "see" and "hear" local media files to extract structured information.

## What problem it solves
Automates the tagging, captioning, and searchability of home video and image archives (e.g., "Find the video of the birthday party") without relying on cloud services. This ensures family memories remain private while gaining the benefit of modern semantic search.

## Where it fits in the stack
Processes raw video and image files stored on [TrueNAS](../architecture/infrastructure.md) or managed by [Immich](../services/immich.md) to extract semantic metadata and searchable transcripts. It acts as the **Inference Layer** for visual data.

## Typical use cases
- Generating descriptions for home video frames using CLIP.
- Transcribing family interviews, audiobooks, or meeting recordings using Whisper.
- Semantic search over video content (Action-based or Object-based).
- Automated OCR and table extraction from complex document images.

## Strengths
- **CLIP (Contrastive Language-Image Pre-training)**: Excellent at mapping images and text to a shared embedding space for natural language search.
- **Whisper**: Industry-standard accuracy for local transcription across multiple languages, with high efficiency in `faster-whisper` implementations.
- **Moondream2 / Florence-2**: Compact VLMs (under 2B parameters) that provide impressive image descriptions and object detection on consumer hardware.
- **Privacy**: Zero-egress processing of sensitive personal media.

## Limitations
- **VRAM Requirements**: Large-scale VLMs (e.g., LLaVA 13B+) require significant GPU VRAM (12GB+) for acceptable performance.
- **Processing Time**: Analyzing every frame of a long video is computationally expensive; keyframe extraction is usually required.
- **Accuracy Drift**: Small models may hallucinate details in complex visual scenes.

## When to use it
- Use **Whisper** for all audio transcription needs in the homelab.
- Use **CLIP** or **SigLIP** for implementing "search by description" in image/video galleries.
- Use **Florence-2** for specialized tasks like object detection, OCR, and regional captioning.
- Use **Moondream2** for generating quick, natural language captions for personal photos.

## When not to use it
- Do not use for real-time video surveillance analysis on low-power CPU-only nodes.
- Do not rely on 100% accuracy for critical forensic identification without human verification.

## Getting started

### Keyframe Extraction for VLM Analysis
Before sending video to a vision model, extract representative keyframes to save compute.

```bash
# Extract one frame every 5 seconds from a video
ffmpeg -i input_video.mp4 -vf "fps=1/5" out%03d.jpg
```

### Python: Image Captioning with Moondream2
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

model_id = "vikhyat/moondream2"
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)

image = Image.open("home_video_frame.jpg")
enc_image = model.encode_image(image)
print(model.answer_question(enc_image, "Describe this scene.", tokenizer))
```

## CLI examples

```bash
# Run Whisper transcription via CLI (requires whisper-cli or faster-whisper)
whisper home_interview.mp3 --model medium --output_format txt

# Using Ollama for visual reasoning (if LLaVA is pulled)
ollama run llava "describe this image: ./frame.jpg"
```

## Related tools / concepts
- [Immich](../services/immich.md) — primary gallery for local media.
- [Whisper](../services/whisper.md) — engine for audio transcription.
- [Ollama](../services/ollama.md) — for running VLMs like LLaVA or BakLLaVA.
- [Paperless-ngx](../services/paperless-ngx.md) — for document-centric vision tasks (OCR).
- [Architecture](../architecture/README.md) — high-level service placement.
- [Voice-to-Task Research](./voice-to-task-research.md) — for speech-driven interactions.
- [Vector DB Comparison](./vector-db-comparison.md) — for storing visual/audio embeddings.
- [Standards](../standards.md) — for metadata conventions.

## Sources / references
- [OpenAI CLIP GitHub](https://github.com/openai/CLIP)
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [Microsoft Florence-2 on Hugging Face](https://huggingface.co/microsoft/Florence-2-large)
- [Moondream GitHub](https://github.com/vikhyat/moondream)
- [Faster-Whisper Implementation](https://github.com/SYSTRAN/faster-whisper)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
