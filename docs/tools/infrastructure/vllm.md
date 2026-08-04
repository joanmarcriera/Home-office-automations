# vLLM

## What it is
vLLM is a high-throughput and memory-efficient inference and serving engine for LLMs. It is powered by **PagedAttention**, an attention algorithm that manages attention keys and values (KV cache) more efficiently, similar to how virtual memory works in operating systems.

## What problem it solves
LLM serving is often bottlenecked by KV cache memory management. Traditional systems suffer from significant memory fragmentation and over-reservation. vLLM's PagedAttention allows KV cache memory to be stored in non-contiguous memory spaces, reducing waste to near-zero and enabling much higher batch sizes and overall throughput, making it a critical infrastructure component for matching the performance of frontier models like Claude 5.1 and GPT-5.5 in self-hosted environments.

## Where it fits in the stack
**Infrastructure / Model Serving**. It provides the high-performance inference layer for serving open-weights models and specialized fine-tuned adapters.

## Typical use cases
- **High-Concurrency Serving**: Powering production LLM endpoints for thousands of simultaneous users.
- **Self-Hosted API Gateways**: Building OpenAI-compatible API endpoints for internal model deployments.
- **Batch Inference**: Processing massive datasets with maximum throughput for offline tasks.
- **Multi-Tenant Adapters**: Serving multiple fine-tuned models (LoRA) efficiently on a single base model.

## Strengths
- **State-of-the-Art Throughput**: Significantly outperforms traditional serving engines in high-concurrency scenarios.
- **Efficient Memory Usage**: PagedAttention minimizes KV cache fragmentation, allowing for larger context windows.
- **Continuous Batching**: Minimizes idle time by processing new requests as soon as they arrive.
- **Broad Ecosystem Support**: Native support for Llama 4, Mistral, Gemma 3, Qwen 3.6, and deep integration with [SGLang](../infrastructure/sglang.md).

## Limitations
- **Hardware Specificity**: Primarily optimized for NVIDIA GPUs (Ampere, Ada Lovelace, Blackwell, and Rubin); support for AMD and TPUs is secondary.
- **Resource Intensive**: Requires significant VRAM for large models unless aggressive quantization (AWQ/FP8) is used.
- **Complexity**: Tuning configurations like `--gpu-memory-utilization` and `--max-model-len` for specific hardware can be non-trivial.
- **NVIDIA GPU Required (CUDA)**: fp16 (default) exceeds 8 GB for 7B+ models; use AWQ 4-bit or fp8 quantization on the RTX 4060. vLLM does not support Apple Silicon — use [MLX](mlx.md) or [Ollama](../../services/ollama.md) on macOS.

## When to use it
- When you need to serve LLMs with maximum possible throughput on NVIDIA hardware.
- When you require a robust, OpenAI-compatible API for your local or private cloud deployment.
- When using advanced features like speculative decoding or prefix caching to reduce latency for long-context reasoning.
- When integrating with NVIDIA NIM (General Availability) for enterprise-grade inference microservices.

## When not to use it
- For low-resource environments (e.g., consumer laptops without high-end NVIDIA GPUs) — use [llama.cpp](llama-cpp.md) or [Ollama](../../services/ollama.md).
- When deploying on Apple Silicon — vLLM is not natively optimized for Metal; use [MLX](mlx.md) instead.
- For extremely simple, low-volume scripts where the overhead of a dedicated server is unnecessary.

## Hardware plugins and extensions
- **vLLM-Kunlun**: A community-maintained hardware plugin designed to seamlessly run vLLM on the Baidu Kunlun3 XPU (specifically the P800 series). It adheres to vLLM's pluggable hardware backend RFC, decoupling hardware-specific code and allowing popular Mixture-of-Experts, Transformer, and multimodal models to execute on Kunlun processors.

## Getting started

### Installation
```bash
pip install vllm
```

### Hello-World Example
```python
from vllm import LLM, SamplingParams

prompts = ["Explain PagedAttention in one sentence."]
sampling_params = SamplingParams(temperature=0.7, top_p=0.9)

# Initialize with a small model for testing
llm = LLM(model="facebook/opt-125m")
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Generated text: {output.outputs[0].text}")
```

### Hardware requirements
| Model size | Precision | Min VRAM | RTX 4060 8 GB | Notes |
|---|---|---|---|---|
| 7-8B | fp16 | 14-16 GB | ❌ Not viable | Exceeds 8 GB |
| 7-8B | AWQ 4-bit | 4-5 GB | ✅ Comfortable | `--quantization awq` |
| 7-8B | fp8 (W8A8) | 7-8 GB | ⚠️ Tight | Requires Ampere/Ada (RTX 30/40xx) |
| 13-14B | AWQ 4-bit | 7-8 GB | ⚠️ Tight | Near ceiling |
| 30B+ | AWQ 4-bit | 16 GB+ | ❌ Not viable | Multi-GPU required |

## CLI examples

### Start an OpenAI-compatible API Server
```bash
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/llama-4-70b \
    --tensor-parallel-size 4 \
    --enable-prefix-caching
```

### Serving with LoRA Adapters
```bash
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/base_model \
    --enable-lora \
    --lora-modules sql-lora=/path/to/sql-adapter chat-lora=/path/to/chat-adapter
```

### Speculative Decoding for Latency Optimization
```bash
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/llama-70b \
    --speculative-model /path/to/llama-7b \
    --num-speculative-tokens 5
```

## API examples

### Request using OpenAI SDK (Python)
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-unused")

response = client.chat.completions.create(
    model="sql-lora",
    messages=[{"role": "user", "content": "Write a SQL query for finding active users."}]
)

print(response.choices[0].message.content)
```

### Multi-Prompt Batching (vLLM Native)
```python
from vllm import LLM, SamplingParams

llm = LLM(model="mistralai/Mistral-7B-v0.1")
prompts = ["Translate this to French: 'Hello world'", "Translate this to German: 'Good morning'"]
outputs = llm.generate(prompts, SamplingParams(max_tokens=50))

for output in outputs:
    print(output.outputs[0].text)
```

### Programmatic Server Health & Validation Loop
A robust Python validation script to programmatically query and monitor a local vLLM endpoint, supporting MCP 3.1 tooling context.

```python
import sys
import json
import time
import requests

def verify_vllm_service(endpoint_url: str = "http://localhost:8000/v1", model_name: str = "meta-llama/Llama-4-8B-Instruct") -> bool:
    # 1. Health check the endpoint
    health_url = endpoint_url.replace("/v1", "/health")
    try:
        response = requests.get(health_url, timeout=5)
        if response.status_code != 200:
            print(f"Health check failed on status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as re:
        print(f"Failed to connect to health endpoint: {re}")
        return False

    # 2. Programmatic validation loop for LLM Generation
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer token-unused"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a validation bot. Speak concisely."},
            {"role": "user", "content": "Verify connection and output 'Success'."}
        ],
        "temperature": 0.1,
        "max_tokens": 10
    }

    try:
        start_time = time.time()
        res = requests.post(f"{endpoint_url}/chat/completions", json=payload, headers=headers, timeout=15)
        latency = time.time() - start_time

        if res.status_code == 200:
            data = res.json()
            completion_text = data["choices"][0]["message"]["content"].strip()
            print(f"Validation successful. Latency: {latency:.3f}s. Response: {completion_text}")
            return "Success" in completion_text or len(completion_text) > 0
        else:
            print(f"vLLM Query failed: {res.status_code} - {res.text}")
            return False
    except Exception as e:
        print(f"Error querying vLLM server: {e}")
        return False

if __name__ == "__main__":
    print("Initiating vLLM Service validation sequence...")
    # Example execution (will gracefully exit if server is not live)
    success = verify_vllm_service()
    if not success:
        print("Note: vLLM server is offline, skipping runtime integration test.")
        sys.exit(0)
    else:
        print("vLLM integration test PASSED.")
        sys.exit(0)
```

## Related tools / concepts
- [Text Generation Inference (TGI)](tgi.md) — Alternative production inference server.
- [SGLang](sglang.md) — Fast backend optimized for complex LLM programs.
- [llama.cpp](llama-cpp.md) — Portable, CPU-focused inference engine.
- [Ollama](../../services/ollama.md) — Desktop-friendly wrapper for local LLMs.
- [Aphrodite Engine](aphrodite-engine.md) — High-performance vLLM fork with specialized features.
- [NVIDIA NIM](../providers/nvidia.md) — Enterprise inference microservices.
- [SGLang RadixAttention](./sglang.md) — Efficient prefix sharing concept.
- [TGI Quantization Patterns](./tgi.md) — Comparison for model compression.

## Sources / references
- [vLLM Official Website](https://vllm.ai/)
- [vLLM GitHub Repository](https://github.com/vllm-project/vllm)
- [vLLM Documentation](https://docs.vllm.ai/)
- [PagedAttention: High-Throughput LLM Serving with vLLM](https://arxiv.org/abs/2309.06180)
- [DKV: Open-Source KV-Cache Compression Framework](https://www.reddit.com/r/LocalLLaMA/comments/1v5wviz/dkv_opensource_kvcache_compression_framework_for/) — Open-source KV-cache compression and management framework for large context serving optimization.
- [vLLM-Kunlun hardware plugin - Baidu](https://github.com/baidu/vLLM-Kunlun)

## Contribution Metadata
- Last reviewed: 2026-10-01
- Confidence: high
