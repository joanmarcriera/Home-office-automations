# MLX

## What it is
MLX is an array framework designed specifically for machine learning research on Apple Silicon. Developed by Apple's machine learning research team, it is optimized to leverage the unified memory architecture of M-series chips (M1 through M4 Ultra as of July 2026). It supports advanced execution graphs and provides first-class model loading, quantization, and evaluation wrappers for local Large Language Models (LLMs).

## What problem it solves
Standard ML frameworks like PyTorch or TensorFlow often face significant overhead when moving data between CPU and GPU. MLX solves this by using Apple Silicon's unified memory, allowing arrays to exist in a shared memory space where both the CPU and GPU can perform operations on them without needing expensive data transfers. This design eliminates the redundant copy-and-paste latency of traditional GPU acceleration, vastly improving local execution speed and memory bounds.

## Where it fits in the stack
**Infrastructure / Inference Framework**. It sits at the foundation of the Apple Silicon AI stack, providing the primitive operations for higher-level libraries like `mlx-lm`, and integrating with orchestrators and agents that run locally on macOS.

## Typical use cases
- **Local LLM Inference**: Running frontier-class open models (such as Gemma 3, Llama 4, and Qwen 3.6) at extreme throughput on Mac hardware.
- **On-Device Fine-Tuning**: Efficiently adapting open-weights models via parameter-efficient methods like LoRA or QLoRA using unified memory.
- **Multimodal Research**: Executing generative image/video models (Stable Diffusion 3) and speech systems (Whisper v3) optimized directly for Apple's Neural Engine (ANE) and GPU.
- **Agentic Workflows**: Powering local multi-agent sessions that require low-latency tool-calling and reasoning loops without hitting cloud API limits or latency.

## Strengths
- **Unified Memory Architecture**: Zero-copy data sharing between CPU, GPU, and ANE for maximum throughput and efficiency.
- **Familiar API**: Python API closely follows NumPy, PyTorch, and JAX conventions, making it easy for researchers to migrate.
- **Lazy Computation**: Operations are only materialized when needed, optimizing memory allocation and execution graphs on macOS devices.
- **Native M4 Optimization**: Explicit support for modern hardware accelerators, matrix math units, and increased memory bandwidth of the M4 generation.
- **Dynamic Graph Compilation**: Compilation and execution graphs compile dynamically, allowing rapid-fire kernel execution and performance caching.

## Limitations
- **Hardware Restricted**: Only runs on Apple Silicon under macOS; no support for Linux (even on Apple Silicon) or Windows platforms.
- **Ecosystem Maturity**: While growing rapidly, the library of pre-built modules and third-party wrappers is smaller than the legacy PyTorch ecosystem.
- **Deployment Scaling**: Not designed for server-grade multi-node or multi-GPU data center deployments; strictly optimized for consumer-grade "edge" or "workstation" setups.

## When to use it
- When your primary development or inference workstation is a Mac with an M-series chip.
- When you want the highest possible tokens-per-second (TPS) and power efficiency for local model execution on macOS.
- When performing memory-constrained local fine-tuning where unified memory allows loading larger batch sizes or context windows than discrete GPUs.

## When not to use it
- For production deployments on standard Linux/NVIDIA cloud servers (use [vLLM](vllm.md) or [Aphrodite Engine](aphrodite-engine.md)).
- If your workflow requires specialized PyTorch CUDA-only kernels or CUDNN features not ported to MLX.
- For development or inference on Intel-based Macs or standard x86 non-Apple hardware.

## Getting started

### Installation
Install the primary MLX and high-level MLX-LM library via `pip`:
```bash
pip install mlx mlx-lm
```

### Simple Inference Example
```python
from mlx_lm import load, generate

# Load a quantized Gemma 3 model from the community repository
model, tokenizer = load("mlx-community/gemma-3-8b-it-4bit")

response = generate(
    model,
    tokenizer,
    prompt="Explain the benefits of unified memory in Apple Silicon.",
    max_tokens=150,
    verbose=True
)
print(response)
```

## CLI examples

### Basic Generation
```bash
python -m mlx_lm.generate \
    --model mlx-community/gemma-3-8b-it-4bit \
    --prompt "Write a short poem about local LLM inference."
```

### Model Quantization
Convert and quantize a standard Hugging Face model to 4-bit MLX format for optimized Mac execution:
```bash
python -m mlx_lm.convert \
    --hf-path google/gemma-3-8b-it \
    --q-bits 4 \
    --upload-repo mlx-community/gemma-3-8b-it-4bit
```

### Interactive Chat Session
```bash
python -m mlx_lm.chat --model mlx-community/gemma-3-8b-it-4bit
```

## API examples

### Custom Training Loop (LoRA fine-tuning)
MLX provides clean primitives for parameter-efficient fine-tuning via `mlx_lm.tuners`.

```python
import mlx.core as mx
import mlx.nn as nn
from mlx_lm.tuners import LoraConfig, get_lora_model

# Define configuration for LoRA adaptation
config = LoraConfig(
    r=16,
    alpha=32,
    filter_modules=["q_proj", "v_proj"],
    dropout=0.05
)

# Apply LoRA layers to the loaded model base
lora_model = get_lora_model(model, config)

# Perform a forward pass using lazy array computation
inputs = mx.array([[1, 2, 3, 4]])
outputs = lora_model(inputs)
mx.eval(outputs)  # Materialize execution graph
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — Cross-platform alternative for local CPU/GPU inference.
- [ExLlamaV2](exllamav2.md) — Ultra-fast inference engine tailored for NVIDIA GPUs.
- [vLLM](vllm.md) — Production-grade multi-tenant model serving.
- [Aphrodite Engine](aphrodite-engine.md) — High-throughput engine optimized for local and homelab hardware.
- [SGLang](sglang.md) — Structured generation runtime featuring prompt-caching.
- [Whisper](../../services/whisper.md) — Speech-to-text processing often optimized via MLX for macOS.
- [Llama Factory](../frameworks/llama-factory.md) — Unified training framework supporting MLX fine-tuning.
- [Local LLMs](../ai_knowledge/local_llms.md) — Conceptual and architectural ecosystem for edge computing.
- [Ollama](../../services/ollama.md) — Local model management and serving framework.

## Sources / references
- [MLX GitHub Repository](https://github.com/ml-explore/mlx)
- [MLX Examples & Models Catalog](https://github.com/ml-explore/mlx-examples)
- [MLX Community Hub on Hugging Face](https://huggingface.co/mlx-community)
- [Apple Machine Learning Research Group](https://machinelearning.apple.com/)
- [MLX-LM Documentation and API Guides](https://ml-explore.github.io/mlx/build/html/index.html)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
