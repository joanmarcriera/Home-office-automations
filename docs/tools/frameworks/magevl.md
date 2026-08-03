# MageVL

Mage-VL is an efficient, codec-native, proactive-streaming multimodal foundation model developed by Microsoft, designed for high-performance image and video understanding.

## What it is

Mage-VL is a codec-native multimodal foundation model built to handle live, real-time video and image streaming workloads. Trained at a compact 4B parameter scale, Mage-VL utilizes a core visual encoder called **Mage-ViT**. Unlike traditional vision-language models that require massive, pre-trained image-text ViTs, Mage-VL uses a codec-aligned sparsity principle to process visual inputs efficiently, reducing token overhead significantly during long-context and video execution.

## What problem it solves

Conventional Vision-Language Models (VLMs) suffer from severe visual token inflation, where high-resolution images or multi-frame video clips translate into thousands of input tokens. This inflation leads to massive computation costs, high memory usage, and poor real-time streaming latency.

Mage-VL solves this by aligning token allocation directly with the underlying video codec's compression behavior (such as HEVC/H.265 or DCVC-RT neural codecs). By skipping visually stagnant areas and focusing only on motion-salient blocks, it reduces spatial-temporal token redundancy by up to 75% without sacrificing accuracy.

## Where it fits in the stack

**Multimodal Framework / Vision-Language Model**. Sits inside the local model execution or cloud provider layers, enabling agent systems (such as those running on Claude 5.1 or GPT-5.5) to utilize high-fidelity, real-time video understanding tools.

```
┌────────────────────────────────────────┐
│      Agent / Orchestration Layer       │
│           (Claude 5.1, n8n)            │
└───────────────────┬────────────────────┘
                    │ Video/Stream Analysis
┌───────────────────▼────────────────────┐
│      MAGE-VL STREAMING ENGINE (4B)     │
└───────────────────┬────────────────────┘
                    │ Codec-Driven Sparse Tokenization
┌───────────────────▼────────────────────┐
│  Mage-ViT Visual Encoder (Neural/H265) │
└────────────────────────────────────────┘
```

## Typical use cases

- **Proactive Streaming Assistant**: Security or surveillance monitors that analyze live camera streams and alert on unexpected behavior.
- **Home lab video search**: Scanning self-hosted video archives (e.g. from Tube Archivist) for specific events, people, or objects.
- **Drone and Robotics Orchestration**: Lightweight, real-time spatial awareness on localized compute blocks.
- **Interactive Video Chat**: Low-latency, direct Q&A interaction with live video feeds or long-form media files.

## Strengths

- **Codec-Native Processing**: Spends visual tokens where a video codec spends bits, using motion vectors and prediction residuals.
- **Lightweight 4B Architecture**: Highly optimized footprint, allowing execution on edge computers or consumer-grade GPUs.
- **Massive Token Reduction**: Achieves up to 75% reduction in visual token budget (e.g., dropping a 64-frame video down to 4,096 tokens).
- **Trained From Scratch**: Avoids massive image-text ViT initializations, using a 24-layer pre-norm Vision Transformer optimized with a large-scale cluster-discrimination objective on 100M unlabeled images/videos.
- **Spatio-Temporal Awareness**: Features a 3D rotary position encoding (3D RoPE) that preserves structural details despite heavy patch dropping.

## Limitations

- **Not for ultra-static text extraction**: Heavily relies on motion/salience, so static PDF OCR may be less optimal than specialized models.
- **Codec Dependency**: Best performance is unlocked when raw compressed video streams (HEVC/H.265) or specific neural codec streams are fed directly into the pipeline.

## When to use it

- For processing real-time video streams, security cameras, or long-context video files.
- When running multimodal agents on limited hardware where standard visual-token count would overwhelm context lengths.
- When building low-latency, streaming multi-agent triggers.

## When not to use it

- When performing deep document analysis or high-fidelity page scans with zero motion.
- If you lack access to compressed video stream parameters or codec-level metadata.

## Getting started

Mage-VL can be run via Hugging Face model loading.

```bash
# Install required libraries
pip install transformers accelerate torch imageio
```

## CLI examples

```bash
# Evaluate a video stream using the CLI tool with HEVC decoding
magevl-cli --video input_stream.mp4 --codec hevc --prompt "Describe the activity in the room"

# Set a threshold for patch sparsity (token budget)
magevl-cli --video live_feed.rtsp --max-tokens 2048 --alert-on "person entering"
```

## API examples

### Real-Time Video Stream Token Analysis and Pydantic v2 Validation
This Python example demonstrates how to configure the codec-aligned patch selection parameters and validate incoming streaming frames using Pydantic v2 before passing them into the visual encoder.

```python
import torch
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional

class CodecPatchConfig(BaseModel):
    codec_type: Literal["H265", "DCVC-RT"] = Field(default="H265")
    token_budget: int = Field(default=4096, ge=512, le=8192)
    salience_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    video_fps: int = Field(default=30, ge=1, le=120)

    @field_validator("token_budget")
    @classmethod
    def enforce_power_of_two(cls, v: int) -> int:
        if (v & (v - 1)) != 0:
            raise ValueError("Token budget must be a power of two.")
        return v

class StreamFrameMetadata(BaseModel):
    frame_index: int
    timestamp_ms: int
    active_motion_vectors: int
    salient_patches_retained: int = Field(..., description="Number of patches selected by the codec filter")
    is_key_frame: bool

    def compression_ratio(self, total_patches: int = 4096) -> float:
        return 1.0 - (self.salient_patches_retained / total_patches)

# Simulated initialization of CodecPatchConfig
config = CodecPatchConfig(
    codec_type="H265",
    token_budget=2048,
    salience_threshold=0.90,
    video_fps=24
)

# Simulated streaming frame metadata validation
frame_meta = StreamFrameMetadata(
    frame_index=154,
    timestamp_ms=5133,
    active_motion_vectors=1240,
    salient_patches_retained=512,
    is_key_frame=False
)

print(f"Validated Config: {config.model_dump()}")
print(f"Frame {frame_meta.frame_index} parsed successfully.")
print(f"Spatio-temporal token reduction: {frame_meta.compression_ratio() * 100:.2f}%")
```

## Related tools / concepts

- [Hugging Face Hub](../../tools/providers/huggingface.md) — Hosting platform for Mage-VL and Mage-ViT models.
- [vLLM](../../tools/infrastructure/vllm.md) — Fast local model serving, which frequently supports Microsoft models.
- [Gemma 3](../../tools/ai_knowledge/local_llms.md) — SOTA local models with multimodal capabilities.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Tool-use interface standard.

## Sources / references

- [Microsoft Mage-VL on Hugging Face](https://huggingface.co/microsoft/Mage-VL)
- [Microsoft Mage-ViT on Hugging Face](https://huggingface.co/microsoft/Mage-ViT)

## Contribution Metadata

- Last reviewed: 2026-11-23
- Confidence: high
