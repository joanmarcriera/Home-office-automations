# Aphrodite Engine

## What it is
Aphrodite Engine is a high-performance inference engine for Large Language Models, forked from [vLLM](vllm.md). It is specifically designed to bridge the gap between production-grade serving and the features desired by the local LLM community. In June 2026, it is a key component of the 'Agentic Homelab', providing high-throughput serving for quantized models with advanced sampling controls.

## What problem it solves
While [vLLM](vllm.md) is excellent for data center serving, the local community often uses a wider variety of quantization formats (like GPTQ, AWQ, EXL2, and GGUF) and specific API requirements (like KoboldAI compatibility). Aphrodite maintains vLLM's high-throughput PagedAttention backend while adding support for these formats and advanced sampling features like DRY and XTC, which are critical for stable and creative agentic output.

## Where it fits in the stack
**Infrastructure**. It serves as a high-performance model server that exposes an OpenAI-compatible API. It sits between the raw model weights (Hugging Face) and the agentic orchestration layer (e.g., [LangChain](../ai_knowledge/langchain.md) or [Mastra](../frameworks/mastra.md)).

## Typical use cases
- **Local Chat Communities**: High-throughput serving for multi-user chat backends and roleplay.
- **Enthusiast Frontends**: Primary backend for SillyTavern, KoboldLite, or custom community UIs.
- **Quantized Model Serving**: Running EXL2 or GGUF models with PagedAttention throughput on consumer hardware.
- **Agentic Inference Clusters**: Serving as the execution engine for local 'Agentic Ingestion' and reasoning tasks.
- **Creative Writing Assistants**: Utilizing DRY and XTC samplers to ensure varied and high-quality narrative generation.

## Strengths
- **PagedAttention**: Inherits industry-leading memory management for high throughput and continuous batching.
- **Format Agnostic**: Supports AWQ, GPTQ, GGUF, and native EXL2 backends for granular quantization.
- **Advanced Samplers**: Includes native support for **DRY** (Don't Repeat Yourself) and **XTC** (Exclude Top Choices).
- **Dual API Compatibility**: Native support for both OpenAI and KoboldAI API standards.
- **Community-Centric**: Optimized for consumer NVIDIA GPUs and diverse model architectures.

## Limitations
- **Hardware Restricted**: Primarily optimized for NVIDIA GPUs (CUDA); limited support for other accelerators.
- **Apple Silicon**: Does not support Apple Silicon / Metal — use [MLX](mlx.md) or [Ollama](../../services/ollama.md) on macOS.
- **Upstream Sync**: As a fork, it periodically syncs with vLLM, which may cause minor delays in the availability of brand-new vLLM features.

## When to use it
- When you need vLLM's batching performance but require support for GGUF or EXL2 quantization.
- When advanced sampling controls (DRY/XTC) are critical for your agentic or creative use case.
- For services requiring native KoboldAI API compatibility alongside OpenAI standards.
- When maximizing the inference throughput of an NVIDIA-based homelab.

## When not to use it
- For enterprise deployments strictly requiring official Hugging Face or vLLM upstream support.
- On non-NVIDIA hardware (e.g., Mac, AMD, or TPU) where other engines have better native support.
- If you only need a simple, one-click installer (use [Ollama](../../services/ollama.md) instead).

## Getting started
Aphrodite Engine is primarily distributed as a Python package and requires an NVIDIA GPU with CUDA.

### Installation
```bash
pip install aphrodite-engine
```

### Basic Server Launch
```bash
python -m aphrodite.endpoints.openai.api_server --model <model_name_or_path>
```

## CLI examples

### Launch with GGUF Support
```bash
python -m aphrodite.endpoints.openai.api_server \
    --model /path/to/model.gguf \
    --dtype float16 \
    --enable-dry \
    --enable-xtc
```

### Launch with EXL2 Backend
```bash
python -m aphrodite.endpoints.openai.api_server \
    --model /path/to/exl2_model/ \
    --backend exl2 \
    --gpu-memory-utilization 0.95
```

### Multi-GPU Execution (Tensor Parallel)
```bash
python -m aphrodite.endpoints.openai.api_server \
    --model <model_path> \
    --tensor-parallel-size 2
```

## API examples
Aphrodite exposes an OpenAI-compatible API, allowing it to be used with standard LLM clients.

### Python: Chat Completion
```python
import openai

client = openai.OpenAI(base_url="http://localhost:8000/v1", api_key="empty")

response = client.chat.completions.create(
    model="aphrodite-model",
    messages=[{"role": "user", "content": "Explain PagedAttention."}],
    extra_body={"dry_multiplier": 0.8} # Custom Aphrodite sampler parameter
)
print(response.choices[0].message.content)
```

### cURL: Health Check
```bash
curl http://localhost:8000/health
```

## Related tools / concepts
- [vLLM](vllm.md) - The upstream high-performance inference engine.
- [ExLlamaV2](exllamav2.md) - High-speed EXL2 inference library.
- [GGUF](../infrastructure/gguf.md) - Universal quantized model format.
- [llama.cpp](llama-cpp.md) - The foundational library for local LLM inference.
- [Ollama](../../services/ollama.md) - User-friendly local model manager and server.
- [SGLang](sglang.md) - High-performance structured generation engine.
- [DRY Sampler](../knowledge_base/dry-sampler.md) - Pattern-prevention sampling technique.
- [XTC Sampler](../knowledge_base/xtc-sampler.md) - Probabilistic exclusion sampling technique.

## Sources / references
- [Official Aphrodite Engine Website](https://aphrodite.pygmalion.chat/)
- [Aphrodite Engine GitHub Repository](https://github.com/PygmalionAI/aphrodite-engine)
- [Aphrodite Sampler Documentation](https://aphrodite.pygmalion.chat/samplers)
- [Local Inference Benchmarks (June 2026)](https://example.com/local-inference-2026)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
