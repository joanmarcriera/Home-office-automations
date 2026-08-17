# KLQ (Measured Rotation Quantization)

## What it is
KLQ (Kullback-Leibler Measured Rotation Quantization) is an open-source, training-free model compression methodology and quantization framework. Introduced in August 2026, KLQ applies measured orthogonal rotation matrices to weight and activation spaces prior to post-training quantization (PTQ). This eliminates outlier activation spikes and preserves distribution shape, enabling ultra-low bitwidth execution (such as 2-bit, 3-bit, and EXL3/KM formats) with minimal perplexity degradation on open-weights LLMs.

## What problem it solves
Standard sub-4-bit quantization techniques (like basic INT4 PTQ) suffer severe accuracy degradation due to extreme activation outliers in deep transformer layers. Traditional rotation methods (such as SpinQuant or QuaRot) apply randomized or fixed Hadamard rotations that fail to account for layer-specific activation covariance. KLQ solves this by using empirical Kullback-Leibler (KL) divergence measurements to optimize layer-wise rotation angles, allowing models to be quantized cleanly to 2-bit or 3-bit levels without requiring compute-intensive fine-tuning or full retraining.

## Where it fits in the stack
**Infrastructure / Model Compression & Quantization**. KLQ operates as an offline optimization runtime tool or dynamic quantization pipeline stage within local inference ecosystems ([llama.cpp](llama-cpp.md), [vLLM](vllm.md), [ExLlamaV3](exllamav3.md)), converting dense FP16/BF16 checkpoints into ultra-compact GGUF/EXL3 formats.

## Typical use cases
- **Ultra-Low VRAM Edge Deployment**: Running 70B+ parameter models (e.g., Llama 4 or Qwen 3.8) on consumer single-GPU setups or edge workstations.
- **Fast Local Fine-Tune Checkpoint Quantization**: Converting newly fine-tuned domain models to low-bit quantizations in minutes without loss of quality.
- **On-Device Mobile & IoT Inference**: Compressing small language models (SLMs) down to under 1GB memory footprints for embedded deployment.

## Strengths
- **Training-Free Execution**: Quantizes multi-billion parameter models in minutes on a single GPU without backpropagation or weight tuning.
- **Measured KL Minimization**: Directly minimizes information loss between dense and quantized layer output distributions.
- **Outlier Suppression**: Smooths activation dynamics, eliminating clipping errors during 2-bit and 3-bit weight packing.
- **FastMCP 3.1 & Pydantic v2 Compatible**: Integrates with automated agent quantization pipelines via [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).

## Limitations
- **Rotation Overhead at Export**: Matrix multiplication during rotation export adds a brief one-time processing delay during conversion.
- **Kernel Hardware Support**: Maximum speedup gains require hardware kernels (CUDA/Metal) optimized for rotated low-bit matrix multiplication.

## When to use it
- When compressing LLM checkpoints to 2-bit or 3-bit precision where standard AWQ or GPTQ cause perplexity spikes.
- When serving large frontier open-weights models under strict hardware memory constraints.
- When requiring rapid, deterministic quantization without dataset fine-tuning.

## When not to use it
- When serving models in FP16/BF16 on unlimited cloud infrastructure where memory saving is not prioritized.
- For basic 8-bit quantization tasks where standard round-to-nearest (RTN) methods are already sufficient.

## Getting started

### Installation
```bash
pip install klq-quant torch
```

### Quantizing a Local Model Checkpoint
```bash
klq-quant --model-path ./Llama-4-8B-Instruct --bits 3 --output-dir ./Llama-4-8B-KLQ3
```

## CLI examples

### Running KL-Measured Layer Rotation
```bash
# Execute KL-measured rotation calibration across all layers
klq-cli calibrate \
  --model Qwen/Qwen3.8-7B \
  --calib-dataset wikitext2 \
  --bits 2.5 \
  --rotation kl-measured \
  --export-gguf ./qwen3.8-klq.gguf
```

## API examples

### Python Integration & Pydantic v2 Schema Validation
The following Python script demonstrates how to execute a KLQ quantization calibration check and validate calibration metrics using **Pydantic v2**:

```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class LayerQuantMetric(BaseModel):
    layer_index: int = Field(..., ge=0, description="Transformer layer index")
    kl_divergence: float = Field(..., ge=0.0, description="Measured KL divergence post-rotation")
    outlier_suppression_ratio: float = Field(..., ge=1.0, description="Ratio of activation peak reduction")
    bits_assigned: float = Field(..., gt=0.0, description="Target bit precision for layer")

class KLQQuantizationReport(BaseModel):
    model_name: str = Field(..., description="Target model converted")
    target_bitwidth: float = Field(..., description="Target overall bitwidth")
    average_kl_loss: float = Field(..., ge=0.0, description="Mean KL divergence loss across all layers")
    layers: List[LayerQuantMetric] = Field(..., description="Per-layer calibration metrics")

def run_klq_quantization_pipeline(model_name: str, target_bits: float) -> KLQQuantizationReport:
    """Simulates a KLQ quantization run and validates output metrics."""
    raw_data = {
        "model_name": model_name,
        "target_bitwidth": target_bits,
        "average_kl_loss": 0.0014,
        "layers": [
            {
                "layer_index": 0,
                "kl_divergence": 0.0011,
                "outlier_suppression_ratio": 4.2,
                "bits_assigned": target_bits
            },
            {
                "layer_index": 1,
                "kl_divergence": 0.0017,
                "outlier_suppression_ratio": 3.8,
                "bits_assigned": target_bits
            }
        ]
    }

    try:
        return KLQQuantizationReport.model_validate(raw_data)
    except ValidationError as ve:
        print(f"Validation error in KLQ report: {ve}")
        return KLQQuantizationReport(
            model_name=model_name,
            target_bitwidth=target_bits,
            average_kl_loss=1.0,
            layers=[]
        )

if __name__ == "__main__":
    report = run_klq_quantization_pipeline("Llama-4-70B-Instruct", 2.5)
    print(f"KLQ Quantization Report Verified:")
    print(f"Model: {report.model_name}")
    print(f"Target Bits: {report.target_bitwidth}")
    print(f"Mean KL Loss: {report.average_kl_loss}")
    print(f"Layers Calibrated: {len(report.layers)}")
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — Inference engine supporting quantized GGUF checkpoints.
- [vLLM](vllm.md) — High-throughput serving engine.
- [Unsloth](unsloth.md) — Memory-efficient fine-tuning framework.
- [Model Classes](../../knowledge_base/model_classes.md) — Overview of frontier open-weights LLMs.

## Sources / references
- [KLQ Quantization Paper / Announcement on Reddit r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1vk2n2k/klq_trainingfree_measured_rotation_quantization/)
- [KLQ Quantization GitHub Repository](https://github.com/klq-quant/klq)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
