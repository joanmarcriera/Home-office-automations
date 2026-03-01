# Text Generation Inference (TGI)

## What it is
Text Generation Inference (TGI) is a specialized toolkit for deploying and serving Large Language Models (LLMs). Developed by Hugging Face, it is designed for high-performance text generation in production environments.

## What problem it solves
TGI addresses the engineering challenges of serving LLMs at scale. It implements advanced optimizations like tensor parallelism for multi-GPU inference, dynamic batching to maximize throughput, and custom Rust kernels for faster generation.

## Where it fits in the stack
Infra

## Typical use cases
- Powering enterprise-grade LLM APIs.
- Serving very large models that require multi-GPU setups via tensor parallelism.
- Production backends for chat applications (e.g., Hugging Chat).

## Strengths
- **Production-Hardened**: Battle-tested at Hugging Face for their own Inference API.
- **Advanced Optimizations**: Includes Flash Attention, Paged Attention, and optimized kernels.
- **Flexible Serving**: Supports a wide range of Hugging Face models out of the box.
- **Enterprise Features**: Robust monitoring, streaming support, and Prometheus metrics.

## Limitations
- **Licensing**: Uses the Hugging Face Optimized Inference License (HFOIL), which has restrictions on commercial redistribution as a service.
- **Setup Complexity**: Docker is the primary and recommended way to run it, which may be a barrier for some environments.

## When to use it
- When you need a highly optimized, production-ready server for LLMs in the Hugging Face ecosystem.
- When you need to scale models across multiple GPUs efficiently.

## When not to use it
- For local development on consumer hardware where simpler tools like Ollama or llama.cpp suffice.
- If your commercial model conflicts with the HFOIL license terms.

## Licensing and cost
- **Open Source**: Yes (HFOIL v1.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation (Docker)
Docker is the recommended way to run TGI.

### Minimal CLI Example
```bash
model=google/gemma-2b
volume=$PWD/data

docker run --gpus all --shm-size 1g -p 8080:80 \
    -v $volume:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id $model
```

### Querying the API
```bash
curl 127.0.0.1:8080/generate \
    -X POST \
    -d '{"inputs":"The future of AI is","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
```

## Related tools / concepts
- [vLLM](vllm.md)
- [SGLang](sglang.md)
- [Inference engines](index.md)

## Sources / References
- [GitHub](https://github.com/huggingface/text-generation-inference)
- [Official Docs](https://huggingface.co/docs/text-generation-inference)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
