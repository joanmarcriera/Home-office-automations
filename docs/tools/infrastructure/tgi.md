# Text Generation Inference (TGI)

## What it is
Text Generation Inference (TGI) is a specialized toolkit for deploying and serving Large Language Models (LLMs). Developed by Hugging Face, it is designed for high-performance text generation in production environments. It is written in Rust, Python, and gRPC.

## What problem it solves
TGI addresses the engineering challenges of serving LLMs at scale. It implements advanced optimizations like tensor parallelism for multi-GPU inference, dynamic batching to maximize throughput, and custom Rust kernels for faster generation. In the June 2026 landscape, it serves as a critical performance baseline for comparing self-hosted model throughput against frontier models like `claude-4-8-opus-20260528` and GPT-5.5.

## Where it fits in the stack
**Infrastructure**. It provides the high-performance serving layer for Hugging Face models, bridging the gap between raw weights and a production-ready API.

## Typical use cases
- **Enterprise-grade LLM APIs**: Powering internal or external model services with high reliability.
- **Multi-GPU Deployment**: Serving very large models (e.g., Llama-4 Maverick) that require tensor parallelism.
- **Real-time Chat**: Production backends for applications like Hugging Chat that require streaming responses.

## Strengths
- **Production-Hardened**: Battle-tested at Hugging Face for their own Inference API.
- **Advanced Optimizations**: Includes Flash Attention, Paged Attention, and optimized Rust kernels.
- **Flexible Serving**: Supports a wide range of Hugging Face models out of the box.
- **Enterprise Features**: Robust monitoring via Prometheus, streaming support, and gRPC interfaces.
- **Multi-LoRA**: Efficiently serve multiple fine-tuned adapters on a single base model.

## Limitations
- **Licensing**: Uses the Hugging Face Optimized Inference License (HFOIL), which has restrictions on commercial redistribution as a service.
- **Setup Complexity**: Docker is the primary and recommended way to run it, which may be a barrier for some environments.
- **Hardware Requirement**: Heavily optimized for NVIDIA GPUs; while AMD support exists, it is less mature than NVIDIA/CUDA.

## When to use it
- When you need a highly optimized, production-ready server for LLMs in the Hugging Face ecosystem.
- When you need to scale models across multiple GPUs efficiently using tensor parallelism.
- When serving multiple LoRA adapters simultaneously is a requirement for multi-tenant applications.

## When not to use it
- For local development on consumer hardware where simpler tools like Ollama or llama.cpp suffice.
- If your commercial model deployment conflicts with the HFOIL license terms.
- For non-transformer architectures that are not supported by the TGI kernels.

## Getting started
Docker is the recommended way to run TGI. Ensure you have the NVIDIA Container Toolkit installed.

```bash
model=google/gemma-2-9b-it
volume=$PWD/data

docker run --gpus all --shm-size 1g -p 8080:80 \
    -v $volume:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id $model
```

## CLI examples
### 1. Basic Server Launch
Launch a server with a specific model and port mapping.
```bash
text-generation-launcher --model-id meta-llama/Meta-Llama-3.1-8B-Instruct --port 8080
```

### 2. Quantized Inference
Run a model with 4-bit quantization to save VRAM.
```bash
text-generation-launcher --model-id meta-llama/Meta-Llama-3.1-70B-Instruct --quantize bitsandbytes-nf4
```

### 3. Multi-GPU Tensor Parallelism
Shard a large model across 4 GPUs.
```bash
text-generation-launcher --model-id meta-llama/Llama-4-Maverick-70B --num-shard 4
```

## API examples
Querying the TGI server using `curl`.

```bash
curl 127.0.0.1:8080/generate \
    -X POST \
    -d '{
        "inputs":"The future of AI in June 2026 involves",
        "parameters":{
            "max_new_tokens":50,
            "temperature": 0.7
        }
    }' \
    -H 'Content-Type: application/json'
```

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput inference engine using PagedAttention.
- [SGLang](sglang.md) — Fast serving with RadixAttention.
- [Inference engines](index.md) — Overview of the LLM serving ecosystem.
- [llama.cpp](llama-cpp.md) — Local LLM inference for consumer hardware.
- [Aphrodite Engine](aphrodite-engine.md) — High-performance inference for creative writing.
- [Docker](../infrastructure/docker.md) — Containerization standard for TGI deployment.
- [vLLM Benchmark CLI](../benchmarking/llmperf.md) — Standardized performance testing.

## Sources / references
- [Official Website](https://huggingface.co/docs/text-generation-inference)
- [GitHub](https://github.com/huggingface/text-generation-inference)
- [TGI Documentation: Multi-LoRA](https://huggingface.co/docs/text-generation-inference/conceptual/multi_lora)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
