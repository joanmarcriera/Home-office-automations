# Text Generation Inference (TGI)

## What it is
Text Generation Inference (TGI) is a specialized toolkit for deploying and serving Large Language Models (LLMs). Developed by Hugging Face, it is designed for high-performance text generation in production environments. It is written in Rust and Python, offering a robust solution for serving the most popular open-weight models.

## What problem it solves
TGI addresses the engineering challenges of serving LLMs at scale. It implements advanced optimizations like tensor parallelism for multi-GPU inference, dynamic batching to maximize throughput, and custom Rust kernels for faster generation. By September 2026, it serves as a high-performance alternative to **NVIDIA NIM** (General Availability), optimized for the **NVIDIA Rubin** architecture, and provides a critical backend for developers benchmarking self-hosted models against frontier services like **Claude 5.1** (specifically supporting advanced Model Context Protocol MCP 3.1 tooling and pipelines), **GPT-5.5**, and **Llama 4**.

## Where it fits in the stack
**Infra**. It provides the high-performance serving layer for Hugging Face models, bridging the gap between raw weights and a production-ready API.

## Typical use cases
- **Enterprise-grade LLM APIs**: Powering internal or external model services with high reliability.
- **Multi-GPU Deployment**: Serving very large models (e.g., Llama-4-70B, Qwen-3.6-72B, Gemma-3) that require tensor parallelism.
- **Real-time Chat**: Production backends for applications like Hugging Chat that require streaming responses.
- **Agentic Workflows**: Providing a high-speed completion endpoint for autonomous agents running in [Claude Code](../development_ops/claude-code.md) and those communicating via Model Context Protocol (MCP 3.1) servers.

## Strengths
- **Production-Hardened**: Battle-tested at Hugging Face for their own Inference API.
- **Advanced Optimizations**: Includes Flash Attention-3, Paged Attention, and optimized custom Rust/Triton kernels.
- **Flexible Serving**: Supports a wide range of Hugging Face models out of the box, including Llama 4, Qwen 3.6, and Gemma 3.
- **Enterprise Features**: Robust monitoring via Prometheus, streaming support, and production-ready logging.
- **Multi-LoRA**: Efficiently serve multiple fine-tuned adapters on a single base model.

## Limitations
- **Licensing**: Uses the Hugging Face Optimized Inference License (HFOIL), which has restrictions on commercial redistribution as a service.
- **Setup Complexity**: Docker is the primary and recommended way to run it, which may be a barrier for environments without container support.
- **Hardware Specificity**: Highly optimized for NVIDIA GPUs (specifically Ampere, Ada Lovelace, Blackwell, and Rubin), though support for other accelerators is evolving.

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
model=google/gemma-3-4b-it
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
    --model-id meta-llama/Llama-4-8B-Instruct \
    --quantize bitsandbytes-nf4
```

### 2. Multi-GPU Tensor Parallelism
Serve a large model across 4 GPUs.
```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id Qwen/Qwen3.6-72B-Instruct \
    --num-shard 4
```

### 3. Serving with LoRA Adapters
Enable LoRA support and specify adapter paths.
```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id meta-llama/Llama-4-8B-Instruct \
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

### Streaming Response with MCP 3.1 Task Payload
```bash
curl 127.0.0.1:8080/generate_stream \
    -X POST \
    -d '{
        "inputs": "Explain quantum computing",
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.2
        }
    }' \
    -H 'Content-Type: application/json'
```

### Python Programmatic SDK Integration
```python
import json
import requests

def query_tgi_endpoint(prompt: str, server_url: str = "http://localhost:8080") -> str:
    payload = {
        "inputs": f"[INST] {prompt} [/INST]",
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.1,
            "top_p": 0.95,
            "stop": ["</s>", "[/INST]"]
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{server_url}/generate", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("generated_text", "")
    else:
        raise RuntimeError(f"TGI Request failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Example validation of self-hosted Llama 4 / Qwen 3.6 endpoints
    try:
        completion = query_tgi_endpoint("List three primary benefits of MCP 3.1 task protocol integration.")
        print(f"Completion: {completion}")
    except Exception as e:
        print(f"Error connecting to TGI: {e}")
```

## Related tools / concepts
- [NVIDIA NIM](../../tools/providers/nvidia.md) — Enterprise inference microservices.
- [Aphrodite Engine](aphrodite-engine.md) — High-performance inference engine.
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
- Last reviewed: 2026-09-02
- Confidence: high
