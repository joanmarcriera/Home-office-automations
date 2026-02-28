# Text Generation Inference (TGI)

## What it is
Text Generation Inference (TGI) is a toolkit developed by Hugging Face for deploying and serving Large Language Models (LLMs). It is written in Rust and Python and is designed for high-performance text generation in production environments.

## What problem it solves
TGI addresses the complexities of serving LLMs at scale. It implements advanced optimizations like tensor parallelism for multi-GPU inference, dynamic batching to increase throughput, and optimized kernels (Flash Attention, Paged Attention) for faster generation.

## Where it fits in the stack
**Infra** — It is a production-grade inference server used to host models as an API service.

## Typical use cases
- Powering the Hugging Face Inference API and Hugging Chat.
- Self-hosting models for enterprise applications with strict performance requirements.
- Serving very large models that require multi-GPU setups.

## Strengths
- **Production Ready**: Battle-tested by Hugging Face.
- **Advanced Optimizations**: Flash Attention, Paged Attention, and custom kernels.
- **Tensor Parallelism**: Efficiently scales models across multiple GPUs.
- **Rich Feature Set**: Supports streaming, stop sequences, and logprobs.

## Limitations
- **Licensing**: Uses the HFOIL v1.0 license, which has some restrictions on commercial use (specifically for selling TGI as a main product).
- **Complexity**: Setup can be more involved than simpler tools like Ollama.

## When to use it
- When you need a highly optimized, production-grade server for LLMs.
- When you are using the Hugging Face ecosystem and want seamless integration.
- When you need to serve large models across multiple GPUs.

## When not to use it
- For simple local experimentation (Ollama or llama.cpp might be easier).
- If your commercial use case conflicts with the HFOIL license.

## Licensing and cost
- **Open Source**: Yes (HFOIL v1.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation (Docker recommended)
The easiest way to run TGI is via Docker.

### Minimal CLI Example (Docker)
```bash
model=google/gemma-2b
volume=$PWD/data # share a volume with the container to avoid downloading the model every time

docker run --gpus all --shm-size 1g -p 8080:80 \
    -v $volume:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id $model
```

### Querying the Server
```bash
curl 127.0.0.1:8080/generate \
    -X POST \
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
```

## Related tools / concepts
- [vLLM](vllm.md)
- [llama.cpp](llama-cpp.md)
- [SGLang](sglang.md)

## Sources / References
- [GitHub](https://github.com/huggingface/text-generation-inference)
- [Official Documentation](https://huggingface.co/docs/text-generation-inference)

## Contribution Metadata
- Last reviewed: 2026-02-28
- Confidence: high
