# MLX

## What it is
MLX is an array framework designed specifically for machine learning research on Apple Silicon. Developed by Apple's machine learning research team, it is optimized to leverage the unified memory architecture of M-series chips (M1 through M4 Ultra as of June 2026).

## What problem it solves
Standard ML frameworks like PyTorch or TensorFlow often face significant overhead when moving data between CPU and GPU. MLX solves this by using Apple Silicon's unified memory, allowing arrays to exist in a shared memory space where both the CPU and GPU can perform operations on them without needing expensive data transfers.

## Where it fits in the stack
**Infrastructure / Inference Framework**. It sits at the foundation of the Apple Silicon AI stack, providing the primitive operations for higher-level libraries like `mlx-lm`.

## Typical use cases
- **Local LLM Inference**: Running frontier-class models (Llama 4, Mistral) at high speed on Mac hardware.
- **On-Device Fine-Tuning**: Efficiently adapting models via LoRA or QLoRA using unified memory.
- **Multimodal Research**: Executing Stable Diffusion 3 and Whisper v3 optimized for Apple's Neural Engine.
- **Agentic Workflows**: Powering local agents that require low-latency reasoning without cloud dependency.

## Strengths
- **Unified Memory**: Zero-copy data sharing between CPU and GPU for maximum throughput.
- **Familiar API**: Python API closely follows NumPy and PyTorch conventions, making it easy for researchers to migrate.
- **Lazy Computation**: Operations are only materialized when needed, optimizing memory use on mobile devices (MacBook Air/Pro).
- **Native M4 Optimization**: Explicit support for the latest hardware accelerators and increased memory bandwidth of the M4 generation.

## Limitations
- **Hardware Restricted**: Only runs on Apple Silicon under macOS; no support for Linux (even on Mac) or Windows.
- **Ecosystem Maturity**: While growing rapidly, the library of pre-built modules is smaller than the decade-old PyTorch ecosystem.
- **Deployment**: Not intended for large-scale data center deployment; restricted to "edge" or "workstation" clusters.

## When to use it
- If your primary development or inference environment is a Mac with an M-series chip.
- When you want the highest possible tokens-per-second (TPS) for local model execution on macOS.
- When performing local fine-tuning where memory efficiency is critical.

## When not to use it
- For production deployments on standard Linux/NVIDIA cloud servers (use [vLLM](vllm.md)).
- If your workflow requires specialized PyTorch kernels or CUDNN features not yet ported to MLX.
- For development on Intel-based Macs or non-Apple hardware.

## Getting started

### Installation
```bash
pip install mlx-lm
```

### Simple Inference Example
```python
from mlx_lm import load, generate

# Load a quantized model from the community
model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

response = generate(
    model,
    tokenizer,
    prompt="Explain the benefits of unified memory in MLX.",
    max_tokens=100
)
print(response)
```

## CLI examples

### Basic Generation
```bash
python -m mlx_lm.generate \
    --model mlx-community/Llama-3.2-3B-Instruct-4bit \
    --prompt "Write a short poem about Apple Silicon."
```

### Model Quantization
Convert a standard Hugging Face model to 4-bit MLX format:
```bash
python -m mlx_lm.convert \
    --hf-path meta-llama/Llama-3.2-3B-Instruct \
    --q-bits 4
```

### Interactive Chat
```bash
python -m mlx_lm.chat --model mlx-community/Llama-3.2-3B-Instruct-4bit
```

## API examples

### Custom Training Loop (LoRA)
MLX provides primitives for efficient parameter-efficient fine-tuning.

```python
import mlx.core as mx
import mlx.nn as nn
from mlx_lm.tuners import LoraConfig, get_lora_model

# Configuration for LoRA
config = LoraConfig(
    r=8,
    alpha=16,
    filter_modules=["gate_proj", "down_proj", "up_proj"]
)

# Apply LoRA to the loaded model
lora_model = get_lora_model(model, config)
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — Cross-platform alternative for local inference.
- [ExLlamaV2](exllamav2.md) — High-speed inference for NVIDIA GPUs.
- [vLLM](vllm.md) — Data center scale inference.
- [Aphrodite Engine](aphrodite-engine.md) — High-throughput local inference.
- [SGLang](sglang.md) — Structured generation often used with MLX backends.
- [Whisper](../../services/whisper.md) — Speech-to-text often optimized via MLX.
- [Llama Factory](../frameworks/llama-factory.md) — UI for fine-tuning that supports MLX.
- [Local LLMs](../ai_knowledge/local_llms.md) — The broader ecosystem.

## Sources / references
- [MLX GitHub Repository](https://github.com/ml-explore/mlx)
- [MLX Examples & Models](https://github.com/ml-explore/mlx-examples)
- [MLX Community on Hugging Face](https://huggingface.co/mlx-community)
- [Apple Machine Learning Research](https://machinelearning.apple.com/)
- [MLX-LM Documentation](https://ml-explore.github.io/mlx/build/html/index.html)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
