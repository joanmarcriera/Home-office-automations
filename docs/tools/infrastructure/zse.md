# ZSE (Zero-Shot Engine)

## What it is
ZSE (Zero-Shot Engine) is an open-source, ultra-low-latency LLM inference engine engineered specifically for rapid cold starts, dynamic weight streaming, and zero-overhead model switching across cloud, hybrid homelab, and edge environments. Optimized for modern open-weights model architectures—including Llama 4, Gemma 4, Qwen 3, and Mistral NeMo—ZSE achieves cold start times under 3 seconds for 8B parameter models and under 7 seconds for 70B parameter quantized checkpoints.

By utilizing direct GPU memory mapping, asynchronous kernel pre-compilation, zero-copy weight streaming over PCIe 5.0 / NVLink, and fine-grained VRAM reclamation policies, ZSE eliminates the memory fragmentation and warmup delays inherent to traditional inference engines like vLLM or Hugging Face TGI. It serves as an enterprise-grade execution platform for scale-to-zero serverless AI deployments, event-driven agentic pipelines, and local AI microservices integrated via the Model Context Protocol (MCP) and FastMCP 3.1.

## What problem it solves
In modern serverless AI and multi-agent systems, idle GPU VRAM consumption is the single largest driver of infrastructure cost. Traditional inference runners (e.g., vLLM, SGLang, TGI) prioritize steady-state throughput and batching efficiency, often requiring 20 to 90 seconds to load weights, allocate KV cache blocks, and compile execution graphs. As a result, operators are forced to keep expensive GPUs powered and occupied 24/7, even for bursty or infrequent agent workflows.

ZSE solves this fundamental trade-off between latency and cost by introducing:
1. **Sub-3-Second Cold Starts**: Near-instantaneous activation of 8B-class models on consumer and enterprise GPUs.
2. **Aggressive VRAM Reclamation**: Microsecond-level offloading of inactive model layers back to host NVMe or RAM based on configurable Time-To-Live (TTL) contracts.
3. **Zero-Copy Weight Paging**: Paging model weights directly into unified memory spaces (e.g., Apple Silicon MPS / Metal 3 or CUDA Unified Memory) without intermediate CPU memory buffer copies.
4. **Agentic Workload Density**: Hosting dozens of specialized fine-tuned models on a single GPU node by dynamically swapping LoRA adapters and model weights on demand.

## Where it fits in the stack
ZSE operates within the **Execution Plane / Inference Infrastructure** layer of the modern AI stack. It bridges agent orchestration platforms (e.g., FastMCP 3.1, Claude 5.6, GPT-5.6, LangChain, AutoGen) and lower-level GPU hardware abstraction layers (CUDA 12.8+, ROCm 6.3+, Metal 3, vLLM kernels).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Agent Orchestration Layer                          │
│         (Claude 5.6 / GPT-5.6 / FastMCP 3.1 / LangGraph / AutoGen)          │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Protocol: MCP / FastMCP 3.1 / OpenAI REST
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    ZSE (Zero-Shot Engine) Runtime Engine                    │
│                                                                             │
│  ┌─────────────────────────┐ ┌──────────────────────┐ ┌──────────────────┐  │
│  │ Cold Start Controller   │ │ VRAM Pager & TTL     │ │ KV Cache Manager │  │
│  │ (Sub-3s Weight Stream)  │ │ (Memory Offloader)   │ │ (Paged Attention)│  │
│  └─────────────────────────┘ └──────────────────────┘ └──────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │              FastMCP 3.1 Server & OpenAI REST Router                   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Transport: PCIe 5.0 / NVLink / Unified Mem
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                        Hardware & Accelerator Layer                         │
│           (Nvidia H100/A100/RTX 4090, Apple Silicon M3/M4, AMD MI300X)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **Scale-To-Zero Serverless API Gateways**: Deploying cost-effective endpoint infrastructure that auto-scales from zero instances during idle periods to hundreds of concurrent requests without incurring cold-start timeouts.
- **Event-Driven Agent Swarms**: Running multi-agent networks where specialized models (e.g., coder, summarizer, planner, evaluator) are instantiated instantly for task execution and immediately suspended to free hardware capacity.
- **Homelab & Edge Orchestration**: Maximizing hardware utility on single-GPU homeservers or edge gateways by serving diverse LLM checkpoints without running out of VRAM.
- **CI/CD Prompt & Model Evaluation**: Rapidly running batch evaluation suites across dozens of open checkpoints in continuous integration pipelines.
- **Privacy-Preserving On-Premise RAG**: Serving embedding and re-ranking models alongside primary LLMs with automatic memory cycling.

## Strengths
- **Extreme Cold Start Performance**: Loads 8B parameter FP8/INT4 weights into active inference state in under 2.8 seconds.
- **FastMCP 3.1 Native Integration**: Exposes engine telemetry, model lifecycle control, and inference tools directly over Model Context Protocol transports.
- **Dynamic Adapter Swapping**: Blazing-fast LoRA adapter loading (<50ms switching overhead) without invalidating base model KV cache blocks.
- **Unified Memory Optimization**: Native Metal 3 and CUDA Unified Memory acceleration for zero-copy memory transfers.
- **Granular Memory Control**: Configurable VRAM TTL timers, background eviction priority queues, and dynamic KV cache expansion.
- **OpenAI Endpoint Compatibility**: Full drop-in replacement for OpenAI `/v1/chat/completions` and `/v1/embeddings` API specifications.

## Limitations
- **High-Concurrency Multi-Tenant Throughput**: Optimized for low latency and fast cold starts rather than maximum continuous token throughput across hundreds of concurrent users (where vLLM excels).
- **Extreme Parameter Scale Constraints**: Running models over 100B parameters requires multi-node tensor parallelism setups that introduce small network synchronization delays.
- **Ecosystem Maturity**: Smaller community tool ecosystem compared to established projects like Ollama or Hugging Face TGI.

## When to use it
- When your architecture requires scale-to-zero capabilities to minimize idle cloud GPU charges.
- When orchestrating complex agentic workflows where specialized models must start up instantly on demand.
- When running resource-constrained edge nodes or homelab servers with limited VRAM.
- When integrating model lifecycle management directly into FastMCP 3.1 agent toolchains.

## When not to use it
- For high-throughput enterprise SaaS backends serving thousands of sustained concurrent queries per second (use [vLLM](vllm.md) or [SGLang](sglang.md)).
- When you require a simple end-user desktop chat application with built-in GUI (use [Ollama](../../services/ollama.md) or [LM Studio](../ai_knowledge/local_llms.md)).
- For specialized multi-GPU cluster training or fine-tuning workloads (use [DeepSpeed](../infrastructure/deepspeed.md) or [TRT-LLM](trt-llm.md)).

## Getting started

### Installation
Install ZSE via Python Package Index or build from source with CUDA / Metal 3 extensions:

```bash
# Basic installation with CPU/CUDA 12 support
pip install zyora-zse

# Installation with Metal 3 acceleration for Apple Silicon
pip install zyora-zse[metal]

# Verify installation and accelerator hardware compatibility
zse system-check
```

### Initializing and Running a Model
Download and initialize a model checkpoint from Hugging Face or local storage:

```bash
# Pull and prepare model weights
zse pull gemma-4-8b-instruct

# Start the ZSE runtime engine with scale-to-zero TTL enabled
zse run gemma-4-8b-instruct --vram-ttl 120 --port 8080
```

### Quick Inference via Python SDK
```python
from zse import ZSEClient

# Connect to local ZSE runtime
client = ZSEClient(base_url="http://localhost:8080")

# Request generation with automatic model spin-up
response = client.chat.completions.create(
    model="gemma-4-8b-instruct",
    messages=[
        {"role": "system", "content": "You are a concise technical assistant."},
        {"role": "user", "content": "Explain zero-copy weight streaming in two sentences."}
    ],
    temperature=0.2,
    max_tokens=150
)

print(f"Response: {response.choices[0].message.content}")
print(f"Cold Start Delay: {response.usage.cold_start_ms} ms")
```

## CLI examples

### Starting the Daemon with FastMCP 3.1 Tool Server Enabled
```bash
zse serve \
  --model meta-llama/Llama-4-8B-Instruct \
  --host 0.0.0.0 \
  --port 8080 \
  --vram-ttl-seconds 300 \
  --max-vram-gb 16 \
  --enable-mcp \
  --mcp-port 9090 \
  --log-level info
```

### Managing Running and Suspended Model Instances
```bash
# List all active, warm, and suspended model instances
zse ps --all

# Manually pre-warm a model into VRAM before peak workload
zse warmup --model Qwen/Qwen3-14B-Instruct --kv-cache-pages 1024

# Purge inactive instances immediately to free VRAM for another application
zse purge --force
```

### Benchmarking Cold Start Latency
```bash
zse benchmark cold-start \
  --model gemma-4-8b-instruct \
  --iterations 5 \
  --unload-between-runs
```

## API examples
ZSE provides a fully typed REST interface alongside native FastMCP 3.1 server support. Below is an enterprise-grade Python integration using **FastMCP 3.1** and **Pydantic v2** for managing ZSE model instances, executing inference, and enforcing runtime parameters.

### FastMCP 3.1 Server Implementation with Pydantic v2 Schemas

```python
import os
import time
from typing import Dict, Any, List, Optional
import requests
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server instance
mcp = FastMCP(
    name="ZSE-Inference-Gateway",
    version="3.1.0",
    description="FastMCP 3.1 control plane for Zero-Shot Engine model lifecycle & inference"
)

# ---------------------------------------------------------------------------
# Pydantic v2 Data Transfer Models
# ---------------------------------------------------------------------------

class ModelWarmupRequest(BaseModel):
    model_name: str = Field(..., alias="model", description="HuggingFace model ID or local checkpoint path")
    vram_ttl_seconds: int = Field(default=300, ge=10, le=3600, description="VRAM auto-eviction TTL in seconds")
    prewarm_kv_cache: bool = Field(default=True, description="Allocate KV cache pages during warm-up")
    max_gpu_memory_mb: Optional[int] = Field(default=None, ge=2048, description="Maximum GPU VRAM quota")

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("model_name cannot be empty or whitespace.")
        return v.strip()

class InferencePayload(BaseModel):
    model: str = Field(..., description="Target model identifier")
    prompt: str = Field(..., min_length=1, max_length=32768, description="User input prompt")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, gt=0, le=8192)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    stop_sequences: List[str] = Field(default_factory=list)

class InferenceResponseSchema(BaseModel):
    instance_id: str
    generated_text: str
    prompt_tokens: int
    completion_tokens: int
    cold_start_ms: float
    total_execution_ms: float

class EngineStatusSchema(BaseModel):
    active_models: List[str]
    vram_used_mb: int
    vram_total_mb: int
    uptime_seconds: float

# ---------------------------------------------------------------------------
# ZSE Client Driver
# ---------------------------------------------------------------------------

class ZSEServerController:
    def __init__(self, host: str = "http://localhost:8080"):
        self.host = host

    def warmup(self, req: ModelWarmupRequest) -> Dict[str, Any]:
        url = f"{self.host}/v1/control/warmup"
        response = requests.post(url, json=req.model_dump(by_alias=True), timeout=30)
        response.raise_for_status()
        return response.json()

    def generate(self, payload: InferencePayload) -> InferenceResponseSchema:
        url = f"{self.host}/v1/chat/completions"
        formatted_body = {
            "model": payload.model,
            "messages": [{"role": "user", "content": payload.prompt}],
            "temperature": payload.temperature,
            "max_tokens": payload.max_tokens,
            "top_p": payload.top_p,
            "stop": payload.stop_sequences
        }
        start_t = time.perf_counter()
        resp = requests.post(url, json=formatted_body, timeout=60)
        elapsed_ms = (time.perf_counter() - start_t) * 1000.0
        resp.raise_for_status()
        data = resp.json()

        choice = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        return InferenceResponseSchema(
            instance_id=data.get("id", "zse-inst-unknown"),
            generated_text=choice,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            cold_start_ms=float(usage.get("cold_start_ms", 0.0)),
            total_execution_ms=round(elapsed_ms, 2)
        )

    def get_status(self) -> EngineStatusSchema:
        resp = requests.get(f"{self.host}/v1/control/status", timeout=10)
        resp.raise_for_status()
        return EngineStatusSchema.model_validate(resp.json())

controller = ZSEServerController()

# ---------------------------------------------------------------------------
# FastMCP 3.1 Tools
# ---------------------------------------------------------------------------

@mcp.tool(name="warmup_model", description="Pre-warm an LLM checkpoint into ZSE VRAM with TTL")
def warmup_model_tool(model: str, vram_ttl_seconds: int = 300) -> str:
    req = ModelWarmupRequest(model=model, vram_ttl_seconds=vram_ttl_seconds)
    res = controller.warmup(req)
    return f"Model '{model}' successfully warmed up. Instance ID: {res.get('instance_id')}"

@mcp.tool(name="execute_inference", description="Execute low-latency LLM inference via ZSE")
def execute_inference_tool(model: str, prompt: str, temperature: float = 0.7) -> str:
    payload = InferencePayload(model=model, prompt=prompt, temperature=temperature)
    result = controller.generate(payload)
    return (
        f"Result ({result.total_execution_ms}ms total, {result.cold_start_ms}ms cold start):\n"
        f"{result.generated_text}"
    )

@mcp.tool(name="get_engine_status", description="Get current VRAM consumption and active model list")
def get_engine_status_tool() -> str:
    status = controller.get_status()
    return (
        f"ZSE Engine Status:\n"
        f"Active Models: {', '.join(status.active_models) if status.active_models else 'None'}\n"
        f"VRAM Usage: {status.vram_used_mb}MB / {status.vram_total_mb}MB\n"
        f"Uptime: {status.uptime_seconds}s"
    )

if __name__ == "__main__":
    mcp.run()
```

## Production Deployment & Configuration

For enterprise scale-to-zero infrastructure, ZSE is deployed via Docker Compose with dedicated host VRAM paging mounts and NVIDIA Container Toolkit drivers.

### Production `docker-compose.yml`
```yaml
version: "3.8"

services:
  zse-engine:
    image: ghcr.io/zyora-dev/zse-runtime:v2.4.0
    container_name: zse-inference-runtime
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "9090:9090"
    environment:
      - ZSE_LOG_LEVEL=info
      - ZSE_VRAM_TTL_DEFAULT=300
      - ZSE_ENABLE_FAST_MCP=true
      - ZSE_CACHE_DIR=/root/.cache/huggingface
      - ZSE_CUDA_ALLOC_CONF=expandable_segments:True
    volumes:
      - /mnt/nvme/huggingface_cache:/root/.cache/huggingface
      - /etc/zse/config.toml:/etc/zse/config.toml:ro
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/v1/control/health"]
      interval: 15s
      timeout: 5s
      retries: 3
```

### Production Engine Configuration (`/etc/zse/config.toml`)
```toml
[server]
host = "0.0.0.0"
port = 8080
mcp_port = 9090
cors_origins = ["*"]

[memory]
max_vram_gb = 24.0
vram_ttl_seconds = 300
eviction_policy = "lru_with_ttl"
enable_unified_paging = true

[inference]
default_temperature = 0.7
max_concurrent_requests = 32
kv_cache_block_size = 16
enable_flash_attention = true

[mcp]
enabled = true
protocol_version = "3.1"
expose_telemetry_tools = true
```

## Performance & Benchmark Metrics

The following performance metrics were captured on an Nvidia RTX 4090 (24GB VRAM) over PCIe 4.0 x16 using ZSE v2.4 against vLLM and Ollama:

| Metric / Scenario | ZSE v2.4 | vLLM v0.6.0 | Ollama v0.3.12 |
| :--- | :--- | :--- | :--- |
| **8B Model Cold Start Latency** | **2.65 s** | 18.40 s | 8.20 s |
| **14B Model Cold Start Latency** | **5.80 s** | 32.10 s | 14.50 s |
| **VRAM Reclamation Time (TTL Expire)** | **< 15 ms** | N/A (Holds VRAM) | ~2500 ms |
| **LoRA Adapter Switch Latency** | **42 ms** | 180 ms | N/A |
| **Single-Stream Token Generation (8B)** | **94 tok/s** | 102 tok/s | 82 tok/s |
| **Idle Engine VRAM Footprint** | **180 MB** | 4,200 MB | 1,100 MB |

## Operational Runbook & Troubleshooting

### Diagnostic Checklist
When experiencing unexpected performance degradation or cold start delays:

1. **Verify GPU Accelerator Access**:
   Ensure driver communication and NVLink/PCIe bus transfers are uninhibited:
   ```bash
   zse system-check --verbose
   nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.free --format=csv
   ```

2. **Check Cold Start Bottlenecks**:
   If model weights take longer than 5 seconds to stream into VRAM, inspect host NVMe read speeds. ZSE weight streaming requires at least 3,500 MB/s sequential NVMe read throughput:
   ```bash
   fio --name=read_test --filename=/mnt/nvme/huggingface_cache/test.dat --size=4G --rw=read --bs=1M
   ```

3. **VRAM Memory Fragmentation Relief**:
   If out-of-memory (OOM) errors occur during rapid model switching, force a memory defragmentation cycle:
   ```bash
   zse control defrag
   ```

4. **MCP Transport Debugging**:
   Inspect FastMCP 3.1 session connection state:
   ```bash
   curl -s http://localhost:9090/mcp/sessions | jq .
   ```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Popular local model runner for desktop environments.
- [vLLM](vllm.md) — High-throughput continuous batching inference engine.
- [SGLang](sglang.md) — Framework for structured and agentic LLM serving.
- [Local LLMs](../ai_knowledge/local_llms.md) — Overview of open-weights models and edge execution patterns.
- [Aphrodite Engine](aphrodite-engine.md) — High-throughput engine optimized for batch inference.
- [LiteLLM](../../services/litellm.md) — Unified API proxy layer for routing and load-balancing requests across ZSE nodes.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol standard for tool calling and context integration.
- [ExLlamaV3](exllamav3.md) — Quantized local runtime designed for extreme VRAM efficiency.
- [llama.cpp](llama-cpp.md) — Cross-platform C/C++ model execution engine.

## Sources / references
- [ZSE Official GitHub Repository](https://github.com/Zyora-Dev/zse)
- [Zyora Engineering Blog: Accelerating Cold-Starts for Scale-to-Zero Inference](https://zyora.dev/blog/zse-benchmarks)
- [FastMCP 3.1 Specification & Model Context Protocol](https://modelcontextprotocol.io/spec)
- [NVIDIA Developer Guide: Zero-Copy Memory Paging and Unified Memory Architecture](https://developer.nvidia.com/cuda-toolkit)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
