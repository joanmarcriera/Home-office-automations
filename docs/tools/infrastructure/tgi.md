# Text Generation Inference (TGI)

## What it is
Text Generation Inference (TGI) is a specialized toolkit for deploying and serving Large Language Models (LLMs). Developed by Hugging Face, it is designed for high-performance text generation in production environments. It is written in Rust and Python, offering a robust solution for serving the most popular open-weight models.

## What problem it solves
TGI addresses the engineering challenges of serving LLMs at scale. It implements advanced optimizations like tensor parallelism for multi-GPU inference, dynamic batching to maximize throughput, and custom Rust kernels for faster generation. By June 2026, it has become a critical backend for developers benchmarking their self-hosted models against frontier services like **Claude 4.8 Opus** and **GPT-5.5**, providing a performance baseline for local inference.

## Where it fits in the stack
**Infra**. It provides the high-performance serving layer for Hugging Face models, bridging the gap between raw weights and a production-ready API.

## Typical use cases
- **Enterprise-grade LLM APIs**: Powering internal or external model services with high reliability.
- **Multi-GPU Deployment**: Serving very large models (e.g., Llama-4-70B) that require tensor parallelism.
- **Real-time Chat**: Production backends for applications like Hugging Chat that require streaming responses.
- **Agentic Workflows**: Providing a high-speed completion endpoint for autonomous agents running in [Claude Code](../development_ops/claude-code.md).

## Strengths
- **Production-Hardened**: Battle-tested at Hugging Face for their own Inference API.
- **Advanced Optimizations**: Includes Flash Attention, Paged Attention, and optimized kernels.
- **Flexible Serving**: Supports a wide range of Hugging Face models out of the box.
- **Enterprise Features**: Robust monitoring via Prometheus, streaming support, and production-ready logging.
- **Multi-LoRA**: Efficiently serve multiple fine-tuned adapters on a single base model.

## Limitations
- **Licensing**: Uses the Hugging Face Optimized Inference License (HFOIL), which has restrictions on commercial redistribution as a service.
- **Setup Complexity**: Docker is the primary and recommended way to run it, which may be a barrier for environments without container support.
- **Hardware Specificity**: Highly optimized for NVIDIA GPUs, though support for other accelerators is evolving.

## When to use it
- When you need a highly optimized, production-ready server for LLMs in the Hugging Face ecosystem.
- When you need to scale models across multiple GPUs efficiently using tensor parallelism.
- When serving multiple LoRA adapters simultaneously is a requirement for multi-tenant applications.

## When not to use it
- For local development on consumer hardware where simpler tools like [Ollama](../../services/ollama.md) or [llama.cpp](llama-cpp.md) suffice.
- If your commercial use case conflicts with the HFOIL license terms.
- When running on Apple Silicon (use [MLX](mlx.md) instead).

## Getting started

### Installation (Docker)
TGI is best run via Docker to ensure all Rust dependencies and CUDA kernels are correctly configured.

```bash
# Pull the latest TGI image
docker pull ghcr.io/huggingface/text-generation-inference:latest
```

### Hello World
Launch a small model to verify the setup:

```bash
model=google/gemma-2b
volume=$PWD/data

docker run --gpus all --shm-size 1g -p 8080:80 \
    -v $volume:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id $model
```

## CLI examples

### 1. Launch with Quantization
Reduce VRAM requirements using `bitsandbytes` or `4-bit` quantization.
```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Meta-Llama-3-8B \
    --quantize bitsandbytes-nf4
```

### 2. Multi-GPU Tensor Parallelism
Serve a large model across 4 GPUs.
```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Meta-Llama-3-70B \
    --num-shard 4
```

### 3. Serving with LoRA Adapters
Enable LoRA support and specify adapter paths.
```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Meta-Llama-3-8B \
    --lora-adapters "adapter_1=path/to/lora1,adapter_2=path/to/lora2"
```

## API examples

### Basic Generation
```bash
curl 127.0.0.1:8080/generate \
    -X POST \
    -d '{
        "inputs":"The future of AI is",
        "parameters":{
            "max_new_tokens":20,
            "stop": ["\n"]
        }
    }' \
    -H 'Content-Type: application/json'
```

### Streaming Response
```bash
curl 127.0.0.1:8080/generate_stream \
    -X POST \
    -d '{"inputs":"Explain quantum computing"}' \
    -H 'Content-Type: application/json'
```

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput alternative using PagedAttention.
- [SGLang](sglang.md) — Optimized for structured generation.
- [llama.cpp](llama-cpp.md) — The standard for CPU and local inference.
- [Ollama](../../services/ollama.md) — Easy-to-use local model management.
- [MLX](mlx.md) — Apple Silicon native inference.
- [Inference engines](index.md) — Overview of the LLM serving ecosystem.
- [Docker](../infrastructure/docker.md) — Containerization platform for TGI.
- [Prometheus](https://prometheus.io/) — Monitoring system supported by TGI.

## Sources / References
- [Official Website](https://huggingface.co/docs/text-generation-inference)
- [GitHub Repository](https://github.com/huggingface/text-generation-inference)
- [TGI Documentation: Multi-LoRA](https://huggingface.co/docs/text-generation-inference/conceptual/multi_lora)
- [Hugging Face Optimized Inference License](https://huggingface.co/docs/text-generation-inference/conceptual/license)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
