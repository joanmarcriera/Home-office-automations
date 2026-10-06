# vLLM

**vLLM** is an open-source, high-throughput, and memory-efficient inference engine designed for serving Large Language Models (LLMs) and Multi-Modal Models (VLM). Developed at UC Berkeley and supported by an active global open-source community, vLLM introduces **PagedAttention**, an algorithm that manages Attention Key-Value (KV) cache memory in non-contiguous physical memory blocks—analogous to how virtual memory and paging operate in standard computer operating systems.

As of early January 2027, vLLM serves as a foundational open-source inference layer for private cloud infrastructure, self-hosted enterprise model deployments, and **FastMCP 3.1 Task Protocol-based tool agents** powered by open-weights models (such as Llama 4, Gemma 4, Qwen 3.8, and DeepSeek-V4).

---

## What it is
vLLM is an inference serving system that maximizes token generation throughput while minimizing memory waste. Traditional LLM serving frameworks store KV cache memory for a sequence in contiguous VRAM memory blocks. Because sequence lengths are unpredictable, previous engines pre-allocated memory for the maximum possible context length (e.g., 8k or 32k tokens), causing severe memory fragmentation and wasting up to 60%–80% of GPU VRAM.

vLLM's **PagedAttention** partitions the KV cache into fixed-size physical memory pages, allowing pages to be allocated on-demand and stored non-contiguously.

```
+-----------------------------------------------------------------------------------+
|                            CLIENT / AGENT / API GATEWAY                           |
|                 (FastMCP 3.1 / OpenAI SDK / LangChain / AutoGen)                  |
+-----------------------------------------------------------------------------------+
                                          |
                                          | OpenAI-Compatible API (HTTP / gRPC)
                                          v
+-----------------------------------------------------------------------------------+
|                                vLLM SERVING ENGINE                                |
|                                                                                   |
|  +---------------------------+  +--------------------------+  +----------------+  |
|  | OpenAI API Server Entry   |  | Continuous Batcher       |  | PagedAttention |  |
|  | (Prefix Caching / LoRA)   |  | (Dynamic Request Queue)  |  | KV-Cache Manager| |
|  +---------------------------+  +--------------------------+  +----------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        PHYSICAL GPU ACCELERATION BACKEND                          |
|                  (NVIDIA Rubin / Blackwell / Hopper / Ampere / ROCm)              |
+-----------------------------------------------------------------------------------+
```

---

## What problem it solves
Legacy LLM serving runtimes suffer from three fundamental bottlenecks:
1. **Severe Memory Waste**: Contiguous KV-cache allocation causes high fragmentation and artificial memory exhaustion long before GPU compute capacity is saturated.
2. **Low Batching Concurrency**: Fixed batching schemes leave GPU Tensor Cores idle while waiting for long generation sequences to finish.
3. **High Latency for Long Contexts**: Repeated prompt processing without prefix caching slows down multi-turn agentic workflows.

vLLM solves these issues by achieving near-zero memory waste through PagedAttention, enabling **continuous iteration-level batching**, and incorporating **automatic prefix caching** to eliminate redundant prompt evaluation overhead.

---

## Where it fits in the stack
vLLM operates in the **Infrastructure & Model Serving layer** of the enterprise AI architecture.

```
+-----------------------------------------------------------------------+
|                    AGENT & APPLICATION ORCHESTRATION                  |
|               (Claude Code / FastMCP 3.1 / Agency Swarm)              |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                     API GATEWAY & LOAD BALANCING                      |
|                  (Vercel AI Gateway / LiteLLM Proxy)                  |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                    HIGH-THROUGHPUT INFERENCE LAYER                    |
|                               (vLLM)                                  |
|                                                                       |
|  +-----------------------+  +--------------------+  +--------------+  |
|  | PagedAttention KV     |  | Continuous Batcher |  | LoRA Engine  |  |
|  +-----------------------+  +--------------------+  +--------------+  |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                       HARDWARE EXECUTION LAYER                        |
|             (NVIDIA Rubin R100 / B200 / H100 / AMD Instinct)          |
+-----------------------------------------------------------------------+
```

---

## Typical use cases
- **Production OpenAI-Compatible API Endpoints**: Serving private open-weights models (Llama 4, Gemma 4, Qwen 3.8) for internal corporate teams and agents.
- **High-Concurrency Agentic FastMCP 3.1 Tool Backends**: Providing low-latency inference endpoints for multi-agent frameworks requiring high request parallelism.
- **Multi-Tenant LoRA Serving**: Serving hundreds of fine-tuned domain adapters (LoRA modules) concurrently on top of a single base model without duplicating VRAM footprint.
- **Long-Context RAG Ingestion & Summarization**: Leveraging prefix caching to rapidly evaluate long document contexts across multiple user queries.
- **Speculative Decoding Acceleration**: Deploying speculative decoding (draft model + target model) to dramatically reduce Time-To-First-Token (TTFT) latency for real-time streaming applications.

---

## Strengths
- **State-of-the-Art Concurrency & Throughput**: Delivers up to 2x–4x higher throughput compared to legacy PyTorch or naive Hugging Face Transformers pipelines under heavy concurrent request loads.
- **Near-Zero Memory Waste**: PagedAttention reduces KV cache memory fragmentation to less than 4%.
- **Automatic Prefix Caching**: Automatically reuses KV cache computation across requests with identical prompt prefixes (e.g., shared system instructions or massive document context blocks).
- **Turnkey OpenAI API Compatibility**: Exposes ready-to-use HTTP endpoints matching the OpenAI REST specification (`/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`).
- **Broad Model & Quantization Support**: Native execution for FP16, BF16, FP8, AWQ, GPTQ, and SqueezeLLM quantization schemes.

---

## Limitations
- **Hardware Platform Requirements**: Primarily optimized for CUDA architecture on NVIDIA GPUs (Ampere, Ada Lovelace, Blackwell, Rubin); AMD ROCm support is functional but requires careful driver alignment.
- **Not Designed for Apple Silicon**: Does not support native Metal acceleration on macOS—use [MLX](mlx.md) or [Ollama](../../services/ollama.md) for Apple Silicon setups.
- **Resource Intensity on Low VRAM**: Running 7B+ parameter unquantized FP16 models requires >16GB VRAM; smaller GPUs require AWQ 4-bit or FP8 quantization.

---

## When to use it
- When self-hosting LLMs or VLMs on dedicated GPU servers or cloud instances for production workloads.
- When high concurrency (dozens or hundreds of simultaneous request streams) is required.
- When building FastMCP 3.1 agent systems that invoke local models repeatedly with shared prompt templates.
- When serving multiple LoRA adapters on top of a shared base model.

---

## When not to use it
- For local consumer laptop execution on Apple Silicon macOS hardware (use [MLX](mlx.md) or [Ollama](../../services/ollama.md)).
- For lightweight embedded or CPU-only devices without dedicated high-bandwidth GPU VRAM (use [llama.cpp](llama-cpp.md)).
- For ultra-simple single-user desktop testing where an all-in-one GUI application is preferred over a server daemon.

---

## Getting started

### Installation
```bash
pip install vllm pydantic>=2.0 fastmcp>=3.1.0 requests
```

### Basic Native Python Usage
```python
from vllm import LLM, SamplingParams

prompts = [
    "Explain PagedAttention in three bullet points.",
    "Compare vLLM with llama.cpp for GPU serving."
]

sampling_params = SamplingParams(temperature=0.3, top_p=0.9, max_tokens=200)
llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")

outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print("Prompt:", output.prompt)
    print("Generated Text:", output.outputs[0].text)
    print("-" * 40)
```

---

## Hardware and VRAM Sizing Reference
| Model Parameter Count | Quantization | Recommended Min VRAM | Compatible GPU Hardware |
|---|---|---|---|
| 7B – 8B | FP16 / BF16 | 16 GB VRAM | RTX 4090 / A10G / L4 |
| 7B – 8B | AWQ 4-bit / FP8 | 8 GB VRAM | RTX 3080 / RTX 4070 |
| 13B – 14B | AWQ 4-bit / FP8 | 12 GB VRAM | RTX 4080 / A10G |
| 32B – 35B | AWQ 4-bit / FP8 | 24 GB VRAM | RTX 4090 / A100 40GB |
| 70B+ | AWQ 4-bit / FP8 | 48 GB VRAM (Tensor Parallel 2) | 2x A100 / 2x H100 / B200 |

---

## CLI examples

### Starting an OpenAI-Compatible API Server
```bash
# Serve Llama 4 Maverick with tensor parallelism across 2 GPUs with prefix caching
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-4-8B-Instruct \
    --tensor-parallel-size 2 \
    --enable-prefix-caching \
    --port 8000
```

### Serving LoRA Multi-Adapters
```bash
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.3 \
    --enable-lora \
    --lora-modules sql-adapter=/path/to/sql-lora summary-adapter=/path/to/summary-lora
```

---

## API examples

### FastMCP 3.1 Integration & Pydantic v2 Schema Patterns

Below is a complete FastMCP 3.1 tool server written in Python that monitors vLLM server health, queries metrics, and executes validated completions against a local vLLM instance using **Pydantic v2** schemas.

```python
import time
import requests
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("vLLM-Inference-Provider", version="3.1.0")

# ------------------------------------------------------------------
# 1. Pydantic v2 Validation Schemas
# ------------------------------------------------------------------
class VllmCompletionRequest(BaseModel):
    server_url: str = Field(default="http://localhost:8000/v1", description="Base OpenAI-compatible API URL")
    model_name: str = Field(..., description="Target model identifier served by vLLM")
    prompt: str = Field(..., min_length=1, description="Input user prompt string")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=4096)

    @field_validator("server_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("server_url must start with http:// or https://")
        return v.rstrip("/")

class VllmCompletionResponse(BaseModel):
    model_used: str
    generated_text: str
    latency_ms: float = Field(..., ge=0.0)
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)

# ------------------------------------------------------------------
# 2. FastMCP 3.1 Tools
# ------------------------------------------------------------------
@mcp.tool()
async def check_vllm_health(server_url: str = "http://localhost:8000") -> str:
    """Queries the native health endpoint of a vLLM server instance."""
    clean_url = server_url.rstrip("/")
    health_endpoint = f"{clean_url}/health"
    try:
        res = requests.get(health_endpoint, timeout=5.0)
        if res.status_code == 200:
            return f"vLLM Health Check SUCCESS: Server at '{clean_url}' is ready."
        return f"vLLM Health Check FAILED: HTTP Status {res.status_code}"
    except Exception as e:
        return f"vLLM Health Check Error: Unable to connect to '{clean_url}' - {str(e)}"

@mcp.tool()
async def generate_vllm_text(
    model_name: str,
    prompt: str,
    server_url: str = "http://localhost:8000/v1",
    temperature: float = 0.2,
    max_tokens: int = 256
) -> str:
    """Executes a text generation request against a local or remote vLLM server instance."""
    req_config = VllmCompletionRequest(
        server_url=server_url,
        model_name=model_name,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": req_config.model_name,
        "messages": [{"role": "user", "content": req_config.prompt}],
        "temperature": req_config.temperature,
        "max_tokens": req_config.max_tokens
    }

    try:
        start_time = time.time()
        endpoint = f"{req_config.server_url}/chat/completions"
        res = requests.post(endpoint, json=payload, headers=headers, timeout=30.0)
        latency = (time.time() - start_time) * 1000.0

        if res.status_code == 200:
            data = res.json()
            completion_text = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})

            validated_response = VllmCompletionResponse(
                model_used=data.get("model", req_config.model_name),
                generated_text=completion_text,
                latency_ms=latency,
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0)
            )

            return validated_response.model_dump_json(indent=2)
        else:
            return f"vLLM Generation Error: Received HTTP {res.status_code} - {res.text}"
    except Exception as e:
        return f"vLLM Exception: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

### Python Request Using OpenAI SDK
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-unused")

response = client.chat.completions.create(
    model="meta-llama/Llama-4-8B-Instruct",
    messages=[{"role": "user", "content": "Write a python function to query vLLM over REST."}]
)

print("Generated Output:", response.choices[0].message.content)
```

---

## Related tools / concepts
- [Text Generation Inference (TGI)](tgi.md) — Production inference engine by Hugging Face.
- [SGLang](sglang.md) — High-performance execution engine with RadixAttention.
- [llama.cpp](llama-cpp.md) — CPU/GPU edge engine optimized for local desktop execution.
- [Ollama](../../services/ollama.md) — Desktop manager wrapping llama.cpp for easy local models.
- [Aphrodite Engine](aphrodite-engine.md) — High-throughput vLLM derivative.
- [NVIDIA NIM](../providers/nvidia.md) — Enterprise containerized inference microservices.
- [Pydantic v2](../../reference-implementations/metadata-schemas/pydantic-v2.md) — Schema validation standard for inference outputs.

---

## Sources / references
- [vLLM Official Website](https://vllm.ai/)
- [vLLM GitHub Repository](https://github.com/vllm-project/vllm)
- [vLLM Official Documentation](https://docs.vllm.ai/)
- [PagedAttention Research Paper (SOSP 2023)](https://arxiv.org/abs/2309.06180)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
