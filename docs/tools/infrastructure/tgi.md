# Text Generation Inference (TGI)

## What it is
Text Generation Inference (TGI) is a specialized toolkit for deploying and serving Large Language Models (LLMs). Developed by Hugging Face, it is designed for high-performance text generation in production environments.

## What problem it solves
TGI addresses the engineering challenges of serving LLMs at scale. It implements advanced optimizations like tensor parallelism for multi-GPU inference, dynamic batching to maximize throughput, and custom Rust kernels for faster generation.

## Where it fits in the stack
**Infra**. It provides the high-performance serving layer for Hugging Face models, bridging the gap between raw weights and a production-ready API.

## Typical use cases
- **Enterprise-grade LLM APIs**: Powering internal or external model services with high reliability.
- **Multi-GPU Deployment**: Serving very large models (e.g., Llama-3-70B) that require tensor parallelism.
- **Real-time Chat**: Production backends for applications like Hugging Chat that require streaming responses.

## Strengths
- **Production-Hardened**: Battle-tested at Hugging Face for their own Inference API.
- **Advanced Optimizations**: Includes Flash Attention, Paged Attention, and optimized kernels.
- **Flexible Serving**: Supports a wide range of Hugging Face models out of the box.
- **Enterprise Features**: Robust monitoring, streaming support, and Prometheus metrics.
- **Multi-LoRA**: Efficiently serve multiple fine-tuned adapters on a single base model.

## Limitations
- **Licensing**: Uses the Hugging Face Optimized Inference License (HFOIL), which has restrictions on commercial redistribution as a service.
- **Setup Complexity**: Docker is the primary and recommended way to run it, which may be a barrier for some environments.

## When to use it
- When you need a highly optimized, production-ready server for LLMs in the Hugging Face ecosystem.
- When you need to scale models across multiple GPUs efficiently.
- When serving multiple LoRA adapters simultaneously is a requirement.

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

### Advanced Serving: Multi-LoRA and Quantization
TGI supports serving multiple LoRA adapters and advanced quantization schemes like AWQ and GPTQ via `bitsandbytes`.

```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
    -v $volume:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Meta-Llama-3-8B-Instruct \
    --quantize bitsandbytes-nf4 \
    --lora-adapters "adapter_1=path/to/lora1,adapter_2=path/to/lora2"
```

### Querying the API
```bash
curl 127.0.0.1:8080/generate \
    -X POST \
    -d '{
        "inputs":"The future of AI is",
        "parameters":{
            "max_new_tokens":20,
            "adapter_id": "adapter_1"
        }
    }' \
    -H 'Content-Type: application/json'
```

## Monitoring and Observability
TGI exposes a `/metrics` endpoint for Prometheus, providing detailed insights into:
- Request latency (TTFT and total generation time).
- Batch sizes and queue lengths.
- GPU memory utilization and throughput (tokens/sec).

## Related tools / concepts
- [vLLM](vllm.md)
- [SGLang](sglang.md)
- [bitsandbytes](../development_ops/bitsandbytes.md)
- [Inference engines](index.md)
- [llama.cpp](llama-cpp.md)
- [Aphrodite Engine](aphrodite-engine.md)
- [Docker](../infrastructure/docker.md)
- [Prometheus](../infrastructure/prometheus.md)

## Sources / References
- [Official Website](https://huggingface.co/docs/text-generation-inference)
- [GitHub](https://github.com/huggingface/text-generation-inference)
- [TGI Documentation: Multi-LoRA](https://huggingface.co/docs/text-generation-inference/conceptual/multi_lora)

## Contribution Metadata
- Last reviewed: 2026-05-17
- Confidence: high
