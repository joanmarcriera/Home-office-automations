# Aphrodite Engine

## What it is
Aphrodite Engine is a high-performance inference engine for Large Language Models, forked from vLLM. It is specifically designed to bridge the gap between production-grade serving and the features desired by the local LLM community.

## What problem it solves
While vLLM is excellent for data center serving, the local community often uses a wider variety of quantization formats (like GPTQ, AWQ, EXL2, and GGUF) and specific API requirements (like KoboldAI compatibility). Aphrodite maintains vLLM's high-throughput PagedAttention backend while adding support for these formats and advanced sampling features like DRY and XTC.

## Where it fits in the stack
**Infra**. It serves as a bridge between high-performance production serving (vLLM) and feature-rich local inference.

## Typical use cases
- **Local Chat Communities**: High-throughput serving for multi-user chat backends.
- **Enthusiast Frontends**: Primary backend for SillyTavern, KoboldLite, or custom community UIs.
- **Quantized Model Serving**: Running EXL2 or GGUF models with PagedAttention throughput.

## Strengths
- **PagedAttention**: Inherits industry-leading memory management for high throughput and batching.
- **Format Agnostic**: Supports AWQ, GPTQ, GGUF, and native EXL2 backends.
- **Advanced Samplers**: Includes support for **DRY** (Don't Repeat Yourself) and **XTC** (Exclude Top Choices) for more creative/stable output.
- **Dual API Compatibility**: Native support for both OpenAI and KoboldAI API standards.
- **Community-Centric**: Optimized for consumer hardware and diverse model architectures.

## Limitations
- **Hardware**: Primarily optimized for NVIDIA GPUs (CUDA).
- **Update Lag**: As a downstream fork, it periodically syncs with vLLM, which may cause minor delays in new vLLM feature availability.

## Hardware requirements

Aphrodite Engine requires an NVIDIA GPU (CUDA). It does not support Apple Silicon / Metal — use [Ollama](../../services/ollama.md) or [MLX](mlx.md) on macOS.

| Model size | Format | Min VRAM | RTX 4060 8 GB | Notes |
|---|---|---|---|---|
| 3-7B | GGUF Q4/Q5 | 3-5 GB | ✅ Comfortable | Best fit; use `aphrodite-gguf` backend |
| 7-8B | EXL2 4bpw | 4-5 GB | ✅ Comfortable | Better quality/speed than GGUF |
| 13-14B | EXL2 4bpw | 7-8 GB | ⚠️ Tight | Reduce `--gpu-memory-utilization 0.85` |
| 13-14B | EXL2 6bpw | 10-12 GB | ❌ Not viable | Exceeds 8 GB |
| 30B+ | any | 16 GB+ | ❌ Not viable | Multi-GPU or higher VRAM required |

## When to use it
- When you need vLLM's batching performance but require GGUF or EXL2 support.
- When advanced sampling controls (DRY/XTC) are critical for your use case.
- For services requiring native KoboldAI API compatibility.

## When not to use it
- For enterprise deployments strictly requiring the official Hugging Face or vLLM upstream support.
- On non-NVIDIA hardware where llama.cpp or vLLM (ROCm/TPU) might have better native support.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install aphrodite-engine
```

### Advanced Server Configuration
Launch with a GGUF model and enabled DRY/XTC samplers:

```bash
python -m aphrodite.endpoints.openai.api_server \
    --model /path/to/model.gguf \
    --dtype float16 \
    --enable-dry \
    --enable-xtc
```

### EXL2 Backend Support
Aphrodite supports the EXL2 backend for granularly quantized models on NVIDIA GPUs:

```bash
python -m aphrodite.endpoints.openai.api_server \
    --model /path/to/exl2_model/ \
    --backend exl2 \
    --gpu-memory-utilization 0.95
```

## Advanced Sampling: DRY and XTC
- **DRY (Don't Repeat Yourself)**: A penalty mechanism that prevents the model from repeating phrases or patterns without the degradation in quality often seen with standard repetition penalties.
- **XTC (Exclude Top Choices)**: Dynamically excludes the most probable tokens when they are significantly more likely than others, forcing the model to explore more varied and creative paths.

## Related tools / concepts
- [vLLM](vllm.md)
- [ExLlamaV2](exllamav2.md)
- [GGUF](../infrastructure/gguf.md)
- [llama.cpp](llama-cpp.md)
- [DRY Sampler](../knowledge_base/dry-sampler.md)
- [XTC Sampler](../knowledge_base/xtc-sampler.md)
- [SGLang](sglang.md)

## Sources / References
- [Official Website](https://aphrodite.pygmalion.chat/)
- [GitHub](https://github.com/PygmalionAI/aphrodite-engine)
- [Aphrodite Engine Sampler Documentation](https://aphrodite.pygmalion.chat/samplers)

## Contribution Metadata
- Last reviewed: 2026-06-02
- Confidence: high
