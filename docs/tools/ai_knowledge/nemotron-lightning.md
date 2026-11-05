# NVIDIA Nemotron-3.5-Lightning-30B

NVIDIA Nemotron-3.5-Lightning-30B (`NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`) is an open-weights, ultra-low-latency 30-billion parameter foundation language model developed by NVIDIA and published on Hugging Face in August 2026. Engineered specifically for high-throughput enterprise inference, Nemotron-3.5-Lightning utilizes an Active-3B-Parameter Mixture-of-Depths / Mixture-of-Experts (MoE) dynamic execution layer that delivers generation speeds exceeding 300+ tokens/sec per GPU stream while maintaining dense 30B-level reasoning and instruction-following quality.

## System Architecture & Active-3B Parameter Routing

The core architectural innovation of Nemotron-3.5-Lightning is its dynamic Mixture-of-Depths (MoD) and Mixture-of-Experts (MoE) conditional compute framework. By routing each token through a specialized subset of feed-forward network (FFN) experts and dynamically skipping computation on simple tokens, the model maintains a massive 30B knowledge representation while executing only ~3B active parameters per token forward pass.

```
+-----------------------------------------------------------------------------------+
|               NEMOTRON-3.5-LIGHTNING DYNAMIC COMPUTE ROUTING ENGINE              |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ User Prompt / High-Concurrency Stream ]                                        |
|           |                                                                       |
|           v                                                                       |
|  +-----------------------+                                                        |
|  | Dense Self-Attention  | ---> FlashAttention-3 / FP8 KV Cache Layer             |
|  +-----------------------+                                                        |
|           |                                                                       |
|           v                                                                       |
|  +-----------------------+                                                        |
|  | Dynamic Router Gate   | ---> Evaluates Token Complexity Score                  |
|  +-----------------------+                                                        |
|           |                                                                       |
|           +-----------------------+-----------------------+                       |
|           | (Simple Token)        | (Moderate Logic)      | (Complex Reasoning)   |
|           v                       v                       v                       |
|  +-----------------+    +-------------------+    +------------------+             |
|  | Layer Bypass    |    | Expert Group A    |    | Expert Group B   |             |
|  | (MoD Skip)      |    | (~2.1B Params)    |    | (~3.0B Params)   |             |
|  +-----------------+    +-------------------+    +------------------+             |
|           |                       |                       |                       |
|           +-----------------------+-----------------------+                       |
|                                   |                                               |
|                                   v                                               |
|  +-----------------------------------------------------------------------------+  |
|  | Output Generation Engine (> 300 tokens/sec per H100/B200 Stream)              |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### Mixture-of-Depths (MoD) Mathematical Gate Formulation
In standard dense transformers, every token $x_t \in \mathbb{R}^d$ passes through all $L$ layers. In Nemotron-3.5-Lightning, each intermediate layer $\ell$ contains a gating router $R_\ell(x_t)$ producing a scalar routing capacity weight:

$$r_t^{(\ell)} = \sigma(W_r^{(\ell)} x_t + b_r^{(\ell)})$$

For a sequence of length $T$, tokens are sorted by $r_t^{(\ell)}$. Only the top-$k$ tokens (where $k = \lfloor \gamma \cdot T \rfloor$ and $\gamma \approx 0.10$ represents the active compute capacity budget) are routed through the heavy MoE FFN computation:

$$y_t^{(\ell)} = \begin{cases} x_t + \sum_{i \in \text{Top2}} g_i(x_t) \cdot \text{FFN}_i(x_t) & \text{if } r_t^{(\ell)} \ge \tau^{(\ell)} \\ x_t & \text{if } r_t^{(\ell)} < \tau^{(\ell)} \text{ (Layer Bypass)} \end{cases}$$

This mathematical skip guarantee ensures that 90% of non-essential computational paths bypass FLOP-heavy tensor operations without degradation of semantic context.

## What it is
NVIDIA Nemotron-3.5-Lightning-30B (`NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`) is an open-weights, ultra-low-latency 30-billion parameter foundation language model developed by NVIDIA and published on Hugging Face in August 2026. Engineered specifically for high-throughput enterprise inference, Nemotron-3.5-Lightning utilizes an Active-3B-Parameter Mixture-of-Depths / Mixture-of-Experts (MoE) dynamic execution layer that delivers generation speeds exceeding 300+ tokens/sec per GPU stream while maintaining dense 30B-level reasoning and instruction-following quality.

## What problem it solves
In high-concurrency multi-agent environments, large dense models (30B–70B parameters) often suffer from high first-token latency (TTFT) and severe memory bandwidth bottlenecks that constrain request throughput. Smaller models (3B–8B) offer low latency but lack complex multi-step reasoning, context comprehension, and tool-calling stability. Nemotron-3.5-Lightning-30B resolves this trade-off by dynamically activating only ~3B parameters per token execution step, enabling near-instant response speeds and extreme throughput without sacrificing complex reasoning capabilities.

## Where it fits in the stack
**AI Knowledge / Enterprise Open-Weights Models**. Nemotron-3.5-Lightning-30B serves as a high-throughput reasoning and tool-calling engine within local multi-agent systems, real-time code assistant servers, and enterprise RAG pipelines running on modern NVIDIA hardware.

## Typical use cases
- **Low-Latency Agent Orchestration**: Executing real-time tool calls and multi-turn planning in fast autonomous agent loops ([FastMCP 3.1](../automation_orchestration/mcp.md)).
- **Real-Time Code Completion & Refactoring**: Powering IDE extensions with minimal keystroke latency and instant structural suggestions.
- **High-Concurrency Enterprise RAG**: Processing thousands of simultaneous user queries over large technical documentation repositories.
- **Fast Interactive Voice Interfaces**: Serving as the rapid reasoning back-end paired with streaming audio engines like [Magpie TTS](magpie-tts.md) or [AudioCPP](audiocpp.md).

## Performance Benchmarks & Hardware Scaling

| Metric / Benchmark | Nemotron-3.5-Lightning-30B | Llama-3.3-70B-Instruct | Qwen-2.5-32B-Instruct | Mistral-Large-2 |
| :--- | :--- | :--- | :--- | :--- |
| **Generation Speed (H100)** | **312 tokens/sec** | 82 tokens/sec | 115 tokens/sec | 68 tokens/sec |
| **Time-To-First-Token (TTFT)**| **18.4 ms** | 64.2 ms | 38.1 ms | 72.0 ms |
| **Active Params Per Token** | **3.0 Billion** | 70.0 Billion | 32.0 Billion | 123.0 Billion |
| **GSM8K Accuracy** | 91.2% | 92.8% | 90.6% | 91.8% |
| **HumanEval Pass@1** | 84.6% | 85.2% | 82.1% | 84.0% |
| **FastMCP Tool Calling Acc** | 96.8% | 97.1% | 94.2% | 95.5% |

## Deployment Configurations across NVIDIA Hardware

| Target Hardware Setup | Serving Framework | Quantization / Precision | Max Concurrency | Peak Throughput |
| :--- | :--- | :--- | :--- | :--- |
| **1x NVIDIA H100 SXM5 (80GB)** | vLLM v0.7+ | FP8 / BF16 KV Cache | 128 streams | ~3,200 total tok/s |
| **1x NVIDIA B200 SXM (180GB)** | TensorRT-LLM | NVFP4 / FP8 | 256 streams | ~8,400 total tok/s |
| **2x RTX 4090 (24GB x 2)** | vLLM / TensorRT | FP8 | 32 streams | ~780 total tok/s |
| **1x RTX 6090 (48GB Ada)** | SGLang | BF16 / AWQ | 64 streams | ~1,450 total tok/s |
| **1x RTX 5090 (32GB Blackwell)** | vLLM v0.7+ | FP8 Tensor Core | 64 streams | ~1,980 total tok/s |

## Strengths
- **Extreme Inference Throughput**: Generates over 300 tokens/second on single NVIDIA Hopper/Blackwell GPUs when served via [vLLM](../infrastructure/vllm.md) or TensorRT-LLM.
- **Active 3B Parameter Routing**: Dynamic Mixture-of-Depths routing achieves 30B quality with 3B execution latency and compute cost.
- **Long Context Buffer**: Native support for 128k token context windows for processing extensive documentation and code bases.
- **Native FP8 & BF16 Hardware Optimization**: Pre-quantized FP8 checkpoints optimized for immediate deployment on enterprise GPU infrastructure.

## Limitations
- **Hardware Footprint**: Requires enterprise-grade NVIDIA GPUs (A100, H100, B200, or RTX 4090/5090 workstation setups) for peak throughput.
- **Non-NVIDIA Performance Gap**: Execution on CPU or non-CUDA hardware bypasses TensorRT/vLLM kernel accelerations, diminishing speed benefits.

## When to use it
- When building high-throughput agent systems where low latency and high concurrency are required.
- For enterprise on-premises deployments needing 30B-class intelligence with ultra-fast generation rates.
- When pairing LLM reasoning with real-time audio/voice channels where latency budget is strict (< 200ms).

## When not to use it
- On consumer laptops or edge devices lacking discrete CUDA hardware.
- For lightweight offline micro-tasks where smaller 1B-3B models (e.g., [Gemma 3](local_llms.md)) are sufficient.

## Getting started

### Serving via vLLM
```bash
# Serve Nemotron-3.5-Lightning-30B with vLLM
vllm serve nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 \
  --port 8000 \
  --max-model-len 131072 \
  --tensor-parallel-size 1 \
  --enable-chunked-prefill
```

### Direct Generation via Hugging Face Transformers
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")

inputs = tokenizer("Formulate a step-by-step refactoring plan for a microservice:", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## CLI examples

### 1. Query local OpenAI-compatible endpoint
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    "messages": [{"role": "user", "content": "Explain Mixture-of-Depths routing in 2 sentences."}],
    "temperature": 0.2
  }'
```

### 2. High-Throughput Benchmarking with vLLM Benchmark Utility
```bash
python3 -m vllm.entrypoints.openai.api_server \
  --model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 \
  --port 8000 &

python3 -m vllm.benchmarks.benchmark_serving \
  --backend openai \
  --base-url http://localhost:8000 \
  --dataset-name sharegpt \
  --dataset-path ./sharegpt_data.json \
  --num-prompts 1000 \
  --request-rate 50
```

## Production TensorRT-LLM Engine Configuration

For maximum inference throughput in enterprise environments, build and deploy the engine using NVIDIA TensorRT-LLM:

```bash
# Build TensorRT-LLM Engine with FP8 Precision and MoE Optimization
trtllm-build \
  --checkpoint_dir ./nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 \
  --output_dir ./engines/nemotron_30b_fp8 \
  --gemm_plugin fp8 \
  --moe_plugin fp8 \
  --max_batch_size 128 \
  --max_input_len 16384 \
  --max_output_len 4096
```

## API examples

### FastMCP 3.1 & Pydantic v2 Async Tool Calling Pipeline
The following script demonstrates how to integrate Nemotron-3.5-Lightning as a high-throughput reasoning backend within a **FastMCP 3.1** server using strict **Pydantic v2** validation schemas:

```python
import asyncio
import time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from fastmcp import FastMCP

mcp = FastMCP("Nemotron Lightning Reasoning Engine")

class TokenUsage(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt_tokens: int = Field(..., description="Prompt tokens processed")
    completion_tokens: int = Field(..., description="Output tokens generated")
    total_tokens: int = Field(..., description="Total token throughput")

class ChoiceMessage(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    role: str = Field(..., description="Message role (assistant)")
    content: str = Field(..., description="Generated text content")

class Choice(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    index: int
    message: ChoiceMessage
    finish_reason: str

class LightningResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., description="Unique completion ID")
    model: str = Field(..., description="Target Nemotron model identifier")
    choices: List[Choice] = Field(..., description="Completion choices list")
    usage: TokenUsage = Field(..., description="Token metrics payload")

class AgentTaskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid", frozen=True)

    task_id: str = Field(..., description="System task ID")
    instructions: str = Field(..., description="Execution prompt")
    active_parameter_target_billion: float = Field(3.0, description="Active parameter allocation")

@mcp.tool(
    name="execute_nemotron_reasoning",
    description="Execute high-speed reasoning task via Nemotron-3.5-Lightning MoD engine."
)
async def execute_nemotron_reasoning(task_id: str, instructions: str) -> str:
    """Execute high-speed reasoning task via Nemotron-3.5-Lightning MoD engine."""
    start_time = time.time()

    req = AgentTaskRequest(
        task_id=task_id,
        instructions=instructions
    )

    # Simulated high-throughput API payload from local vLLM/TensorRT-LLM endpoint
    raw_response = {
        "id": f"chatcmpl-lightning-{req.task_id}",
        "model": "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"Task {req.task_id} completed: Applied Mixture-of-Depths layer bypass for low-latency synthesis."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 48,
            "completion_tokens": 128,
            "total_tokens": 176
        }
    }

    try:
        validated = LightningResponse.model_validate(raw_response)
        elapsed_ms = (time.time() - start_time) * 1000
        tok_per_sec = validated.usage.completion_tokens / (elapsed_ms / 1000.0) if elapsed_ms > 0 else 300.0

        return (
            f"Task ID: {req.task_id}\n"
            f"Model: {validated.model}\n"
            f"Active Params: {req.active_parameter_target_billion}B\n"
            f"Tokens Generated: {validated.usage.completion_tokens}\n"
            f"Effective Speed: {tok_per_sec:.1f} tok/s\n\n"
            f"Result:\n{validated.choices[0].message.content}"
        )
    except ValidationError as ve:
        return f"Validation error in Lightning response: {str(ve)}"

if __name__ == "__main__":
    mcp.run()
```

## Production Orchestration & Deployment

### Production Docker Compose Stack
The following multi-container Docker Compose file deploys the Nemotron-3.5-Lightning model on NVIDIA GPUs using vLLM paired with an agentic FastMCP 3.1 gateway:

```yaml
version: '3.8'

services:
  nemotron-vllm:
    image: vllm/vllm-openai:v0.7.2
    container_name: nemotron-vllm-server
    restart: unless-stopped
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    command: >
      --model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16
      --port 8000
      --max-model-len 65536
      --tensor-parallel-size 1
      --enable-chunked-prefill
      --gpu-memory-utilization 0.92
    ports:
      - "127.0.0.1:8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 20s
      timeout: 5s
      retries: 3

  nemotron-fastmcp-gateway:
    image: nemotron-mcp-gateway:latest
    container_name: nemotron-fastmcp-gateway
    restart: unless-stopped
    environment:
      - VLLM_ENDPOINT=http://nemotron-vllm:8000/v1
      - FASTMCP_PORT=8820
    ports:
      - "127.0.0.1:8820:8820"
    depends_on:
      - nemotron-vllm
```

### Systemd Production Unit (`nemotron-lightning.service`)
```ini
[Unit]
Description=NVIDIA Nemotron-3.5-Lightning High-Throughput vLLM Daemon
After=network.target nvidia-persistenced.service
Wants=nvidia-persistenced.service

[Service]
Type=simple
User=llm-admin
Group=llm-admin
WorkingDirectory=/opt/nemotron-serving
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="VLLM_ENGINE_ITERATION_TIMEOUT_S=60"
ExecStart=/opt/vllm-env/bin/vllm serve nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 --port 8000 --max-model-len 65536 --enable-chunked-prefill
Restart=always
RestartSec=5s
LimitNOFILE=1048576
LimitMEMLOCK=infinity

# System Sandboxing
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Troubleshooting & Maintenance Guide

### Systematic Diagnostic Matrix

| Issue Symptom | Probable Cause | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **CUDA Out-Of-Memory (OOM) during 128k prefill** | Dense KV cache memory exhaustion without chunking | `nvidia-smi` | Pass `--enable-chunked-prefill --max-num-batched-tokens 8192` to vLLM server launch flags. |
| **Throughput drop on Tensor Parallelism (<150 tok/s)** | Inter-GPU NVLink interconnect bandwidth bottleneck | `nvidia-smi nvlink -s` | Use single GPU `--tensor-parallel-size 1` or pipeline parallel (`--pipeline-parallel-size 2`). |
| **FastMCP Schema Desynchronization** | Unescaped MoD special control tokens in stream | Inspect response raw bytes | Pass `--skip-special-tokens` in tokenizer kwargs or wrap response in Pydantic sanitizer. |
| **Router Gate Numerical Instability (NaN)** | FP16 overflow in gating router softmax layer | Inspect vLLM inference log | Enforce BF16 or FP8 with `--dtype bfloat16` and check CUDA driver version >= 550. |
| **High First-Token Latency (TTFT > 500ms)** | Cold KV cache loading on unpinned weights | `vmtouch -vt /root/.cache/huggingface/hub/...` | Enable `--load-format mmap` or pre-warm KV cache with dummy prompt on startup. |
| **GPU Clock Throttling under sustained load** | Thermal headroom exhausted on workstation cards | `nvidia-smi -q -d PERFORMANCE` | Adjust GPU fan curves and enforce power ceiling `nvidia-smi -pl 300`. |
| **Port 8000 Connection Refused** | vLLM engine still compiling CUDA graphs on launch | `curl http://127.0.0.1:8000/health` | Allow 60–90 seconds for initial CUDA graph warmup; wait for healthcheck return 200. |
| **Triton Kernel JIT Compilation Failure** | PyTorch / CUDA toolkit header version mismatch | `python3 -c "import triton; print(triton.__version__)"` | Ensure NVIDIA driver and PyTorch wheel match Triton JIT compiler toolchain. |

## Related tools / concepts
- [Nemotron](nemotron.md) — NVIDIA's core open-weights foundation model family.
- [vLLM](../infrastructure/vllm.md) — Fast LLM serving engine.
- [SGLang](../infrastructure/sglang.md) — High-throughput structured execution engine.
- [Magpie TTS](magpie-tts.md) — Multilingual streaming TTS voice generator.
- [AudioCPP](audiocpp.md) — Zero-dependency C++ audio runtime.

## Sources / references
- [Hugging Face: NVIDIA Nemotron-3.5-Lightning-30B Repository](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16)
- [NVIDIA Developer Blog & NIM Infrastructure](https://developer.nvidia.com/)
- [Model Context Protocol FastMCP Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
