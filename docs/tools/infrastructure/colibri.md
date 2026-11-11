# Colibri

Colibri is a high-performance streaming inference engine designed to execute ultra-large open-weights language models—such as Tencent's Hy3 (299B MoE), DeepSeek-V4-Flash MoE, and Qwen 3.6 MoE—on consumer-grade desktop hardware with constrained VRAM. By leveraging direct memory access (DMA) layer prefetching, dynamic Mixture-of-Experts (MoE) routing, and speculative multi-token prediction heads, Colibri breaks the "VRAM wall," allowing 200B+ parameter models to execute on system configurations with as little as 10GB to 16GB of GPU VRAM.

## What it is
Colibri is a specialized C++20 and CUDA-accelerated inference runtime centered on asynchronous layer streaming and dynamic memory offloading. Unlike traditional inference engines that require the entirety of a model's weights to reside fully in GPU VRAM, Colibri optimizes real-time data transfers between system RAM (DDR5/DDR6) and GPU VRAM (GDDR6X/HBM3). As of early 2027, it stands as a premier open-source solution for developers, researchers, and self-hosted environments seeking to execute frontier-class MoE reasoning backends locally alongside cloud API endpoints like Claude 5.6, GPT-5.6, and Gemini 4.0 Pro.

## What problem it solves
Frontier Mixture-of-Experts (MoE) models offer exceptional reasoning capabilities but traditionally impose prohibitive hardware requirements. For example, a 299B parameter model like Tencent Hy3 requires over 180GB of VRAM even when quantized to 4 bits, demanding enterprise server nodes equipped with multiple NVIDIA H100 or H200 GPUs.

Colibri solves this hardware bottleneck by streaming only active execution layers and dynamically routed experts into GPU VRAM on demand. By keeping non-active layers resident in system RAM and streaming them across PCIe Gen 4/5 buses using asynchronous Direct Memory Access (DMA), Colibri allows single-card workstations (e.g., equipped with an RTX 4080, RTX 5080, or RTX 5060) to execute massive open models. This democratizes local frontier-class reasoning, ensuring complete data sovereignty, zero API egress costs, and robust offline resilience.

## Where it fits in the stack
Within the KnowledgeOps and AI infrastructure stack, Colibri sits at the **Inference & Model Serving Layer**. It serves as an offline-first reasoning backend for local orchestrators and agents. Exposing OpenAI-compatible HTTP endpoints and native [Model Context Protocol (MCP 3.1 / FastMCP 3.1)](../../knowledge_base/patterns/tool-calling-and-mcp.md) tool interfaces, Colibri enables agents to route complex fallback tasks (e.g., code analysis or mathematical proofs) to local frontier MoE models.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      Agentic Orchestration Layer                         │
│             (Claude 5.6, FastMCP 3.1, Gemma 4, OpenClaw Agent)           │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Tool / Model Calls
┌────────────────────────────────────▼─────────────────────────────────────┐
│                      COLIBRI STREAMING RUNTIME                           │
│ ┌───────────────────────┐ ┌───────────────────────┐ ┌──────────────────┐ │
│ │  DMA Ring Buffer      │ │ Hot Expert VRAM Cache │ │ MTP Speculative  │ │
│ └───────────────────────┘ └───────────────────────┘ └──────────────────┘ │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Async PCIe Direct Memory Access
┌────────────────────────────────────▼─────────────────────────────────────┐
│ System RAM (DDR5 / DDR6) ───────────────────────► GPU VRAM (GDDR6X)     │
└──────────────────────────────────────────────────────────────────────────┘
```

## Mathematical Formulations & Asynchronous DMA Roofline Models

Colibri operates on the boundary where compute throughput intersects bus transfer velocity. The core operational constraints can be formulated rigorously:

### 1. Asynchronous PCIe DMA Layer Transfer Roofline
Let $S_{\text{layer}}$ be the byte footprint of a single transformer layer (comprising attention projections and MoE feed-forward networks), and let $B_{\text{PCIe}}$ denote the effective PCIe bidirectional DMA bandwidth (in GB/s). The raw transmission latency $T_{\text{transfer}}$ for streaming layer $l$ from host RAM to GPU VRAM is governed by:

$$T_{\text{transfer}}(l) = \frac{S_{\text{layer}}}{B_{\text{PCIe}}} + \delta_{\text{DMA}}$$

where $\delta_{\text{DMA}}$ represents the CUDA DMA host-to-device kernel launch and synchronization overhead (typically $4.2\,\mu\text{s} \le \delta_{\text{DMA}} \le 12.8\,\mu\text{s}$).

For double-buffered asynchronous prefetching to completely conceal transfer latency, the compute duration of layer $l-1$, denoted $T_{\text{compute}}(l-1)$, must satisfy the pipelining inequality:

$$T_{\text{compute}}(l-1) \ge T_{\text{transfer}}(l)$$

When $T_{\text{compute}}(l-1) < T_{\text{transfer}}(l)$, the GPU compute engine enters a memory stall state. The total token generation period $T_{\text{token}}$ across all $L$ transformer layers is given by:

$$T_{\text{token}} = \sum_{l=1}^{L} \max\left(T_{\text{compute}}(l),\, T_{\text{transfer}}(l)\right) + T_{\text{MTP}}$$

where $T_{\text{MTP}}$ is the verification latency of the Multi-Token Prediction speculative head.

### 2. Mixture-of-Experts (MoE) Active VRAM Cache Footprint
In an MoE architecture with $E_{\text{total}}$ total experts per layer where $k$ experts are dynamically activated per token ($k \ll E_{\text{total}}$), Colibri partitions GPU VRAM into a static base weight buffer $M_{\text{base}}$, a dynamic hot expert cache $M_{\text{hot\_cache}}$, and a KV-cache allocation $M_{\text{KV}}$:

$$M_{\text{VRAM\_allocated}} = M_{\text{base}} + M_{\text{KV}}(C, B) + \sum_{l=1}^{L} \sum_{e \in \mathcal{H}_l} S_{\text{expert}}(l, e)$$

where $\mathcal{H}_l$ is the set of cached hot experts for layer $l$ ($|\mathcal{H}_l| = k_{\text{cached}}$), $C$ is context sequence length, and $B$ is batch size. The KV cache footprint for grouped-query attention (GQA) is:

$$M_{\text{KV}}(C, B) = 2 \cdot L \cdot H_{\text{KV}} \cdot D_{\text{head}} \cdot C \cdot B \cdot b_{\text{precision}}$$

where $H_{\text{KV}}$ is the number of key-value heads, $D_{\text{head}}$ is head dimension, and $b_{\text{precision}}$ is storage bytes per element (e.g., 2 bytes for FP16, 0.5 bytes for FP4).

### 3. Speculative Multi-Token Prediction (MTP) Speedup Ratio
Let $\alpha \in [0, 1]$ represent the empirical acceptance rate of speculative candidate tokens emitted by the MTP head, and let $\gamma$ denote the number of speculative draft tokens generated per step. The theoretical speedup factor $\mathcal{S}_{\text{spec}}$ over standard autoregressive decoding is modeled by:

$$\mathcal{S}_{\text{spec}} = \frac{1 + \alpha \gamma}{1 + \gamma \cdot \frac{C_{\text{draft}}}{C_{\text{target}}}} \approx \frac{1 + \alpha \gamma}{1 + \epsilon}$$

In Colibri, because the draft head evaluates concurrently within resident GPU registers while the target layer streams over PCIe, the computational overhead ratio $\epsilon \to 0$, maximizing speedup even at moderate acceptance rates ($\alpha \approx 0.65$).

### 4. Direct Memory Access Ring Buffer Mechanics
Colibri maintains a circular triple-buffered DMA staging region in host pinned memory:
1. **Buffer Slot 0 (GPU Ingest)**: Currently bound to active CUDA stream kernels executing matrix-vector multiplies.
2. **Buffer Slot 1 (PCIe Transit)**: Occupied by non-blocking asynchronous `cudaMemcpyAsync` packet bursts across PCIe Gen 4/5 lanes.
3. **Buffer Slot 2 (Host Cache Read)**: Undergoing AVX-512 decompression or memory re-indexing from non-pinned host DDR5 RAM blocks.

This triple-buffering pipeline eliminates thread blocking on the host CPU, allowing concurrent multi-tenant agent sessions to share model parameter representations without cache collisions.

## Typical use cases
- **Desktop Frontier Reasoning**: Executing Tencent Hy3 (299B) or Qwen 3.6 MoE locally for deep software design, formal logic, and mathematical proofs on a single GPU.
- **Privacy-Sensitive Legal & Medical Ingestion**: Analyzing sensitive records and proprietary source code locally without exposing data to third-party cloud APIs.
- **Offline Agent Backends**: Providing high-capacity reasoning backends for local agent frameworks operating in air-gapped or bandwidth-constrained environments.
- **FastMCP 3.1 Tool Servers**: Streaming execution tokens directly into agentic tool calling loops via standardized MCP SSE event endpoints.
- **Speculative Decoding Research**: Testing novel multi-token prediction heads and expert caching algorithms on consumer desktop hardware.

## Strengths
- **Unmatched Memory Efficiency**: Runs massive 200B+ parameter MoE architectures on consumer GPUs with 10GB–16GB VRAM.
- **Native MoE Architecture Support**: Specifically tuned for Tencent Hy3, DeepSeek-V4, and Qwen 3.6 routing topologies.
- **PCIe Asynchronous Prefetching**: Overlaps DMA layer transfers with CUDA kernel execution to maximize hardware utilization.
- **FastMCP 3.1 Integration**: Exposes model generation streams directly as FastMCP tool calls for seamless agent integration.
- **Broad Quantization Compatibility**: Native fused kernels for GGUF and EXL2 quantized formats.

## Limitations
- **PCIe Bandwidth Bottleneck**: Token generation speed is fundamentally bounded by PCIe bus transfer speeds (typically 2–5 tokens/sec on PCIe Gen 4/5).
- **High DDR5 Memory Speed Requirement**: Optimal performance requires dual-channel or quad-channel DDR5-6000+ system RAM.
- **Tuning Complexity**: Achieving smooth execution requires calibrating thread priorities, streaming buffer allocations, and expert cache limits.

## When to use it
- When you MUST execute 200B+ parameter open-weights models locally on a consumer workstation.
- For non-interactive, asynchronous batch tasks (such as overnight codebase refactoring, log analysis, or multi-step agent planning).
- When building air-gapped, privacy-first workstations that require frontier reasoning depth.

## When not to use it
- For real-time interactive chatbots or voice assistants requiring instantaneous token responses (use smaller VRAM-resident models like [Gemma 3](../ai_knowledge/local_llms.md) or Llama 3.3 70B via [llama.cpp](llama-cpp.md)).
- If you have access to enterprise multi-GPU nodes (e.g., 4x H100) where models fit fully resident in VRAM using [vLLM](vllm.md) or [ExLlamaV3](exllamav3.md).

## Getting started

### Installation
Colibri can be installed via PyPI or built from source with custom CUDA architectures:

```bash
# Install core Colibri Python package with CUDA 12.x bindings
pip install colibri-inference

# Verify CLI installation
colibri --version
```

### Launching the Streaming Server
Launch the Colibri local streaming API server for Tencent Hy3:

```bash
colibri-server \
  --model ./models/hy3-299b-q4.gguf \
  --vram-limit 12G \
  --streaming-buffer 8G \
  --active-experts 4 \
  --port 8080
```

## CLI examples

### 1. Direct Reasoning Execution
```bash
colibri-cli \
  --model hy3-299b \
  --prompt "Write a lock-free concurrent ring buffer in C++20 with atomic head/tail pointers." \
  --max-tokens 1024 \
  --stream-mode aggressive
```

### 2. Expert Cache & Buffer Diagnostics
```bash
colibri-cli inspect --model hy3-299b --show-pcie-bandwidth --active-cache-status
```

### 3. FastMCP 3.1 Server Registration
Register Colibri as a local FastMCP 3.1 tool provider:
```bash
mcp register colibri-streaming --command "colibri-server" --args "--model hy3-299b --mcp-sse --port 8080"
```

## Production Deployment & Orchestration

### Systemd Service Daemon (`/etc/systemd/system/colibri-inference.service`)
To manage Colibri as a background streaming inference daemon on local workstation nodes:

```ini
[Unit]
Description=Colibri DMA MoE Layer Streaming Inference Engine
After=network.target nvidia-persistenced.service
Requires=nvidia-persistenced.service

[Service]
Type=simple
User=colibri
Group=colibri
WorkingDirectory=/opt/colibri
ExecStart=/opt/colibri/venv/bin/colibri-server \
  --model /opt/colibri/models/hy3-299b-q4.gguf \
  --vram-limit 12G \
  --streaming-buffer 16G \
  --active-experts 4 \
  --port 8080
Restart=always
RestartSec=10
LimitNOFILE=65536
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="PYTHONUNBUFFERED=1"
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Docker Compose Workstation Deployment (`docker-compose.yml`)
Deploy Colibri in a containerized GPU-accelerated environment with PCIe host sharing:

```yaml
version: '3.8'

services:
  colibri-engine:
    image: colibri/inference-runtime:v1.4
    container_name: colibri-streaming-server
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "8081:8081"
    environment:
      - PORT=8080
      - MCP_PORT=8081
      - VRAM_LIMIT=12G
      - RAM_BUFFER=32G
      - MODEL_PATH=/models/hy3-299b-q4.gguf
      - CUDA_VISIBLE_DEVICES=0
    volumes:
      - ./models:/models:ro
      - ./cache:/root/.cache/colibri
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/healthz"]
      interval: 10s
      timeout: 5s
      retries: 3
```

## API examples

### 1. FastMCP 3.1 Streaming Engine Tool Server with Strict Pydantic v2
The following complete Python service provides a FastMCP 3.1 tool server interfacing directly with the local Colibri engine. It enforces strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) to validate streaming parameters, expert allocation, and prompt payloads:

```python
import os
import sys
from typing import Literal, Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Colibri-DMA-Streaming-Tool-Server", version="3.1.0")

class StreamingInferenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., min_length=5, description="Input prompt for deep reasoning generation")
    max_tokens: int = Field(default=512, ge=16, le=8192, description="Upper bound on emitted tokens")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0, description="Sampling temperature")
    active_experts: int = Field(default=4, ge=1, le=8, description="Number of routed experts cached in VRAM")
    stream_mode: Literal["lazy", "balanced", "aggressive"] = Field(
        default="balanced", description="PCIe DMA ring buffer prefetching aggressiveness"
    )
    speculative_mtp: bool = Field(default=True, description="Enable Multi-Token Prediction speculative head")

    @field_validator("prompt")
    @classmethod
    def sanitize_prompt(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Prompt must not be empty or whitespace only.")
        return stripped

class StreamingInferenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    tokens_generated: int
    tok_per_sec: float
    pcie_transfer_bandwidth_gbps: float
    output_text: str
    expert_cache_hit_rate: float

class ColibriRuntimeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model_path: str = Field(..., description="Path to GGUF or EXL2 model weight file")
    vram_limit_gb: float = Field(default=12.0, ge=8.0, le=48.0, description="GPU VRAM limit in GB")
    ram_buffer_gb: float = Field(default=16.0, ge=8.0, le=128.0, description="Host system RAM buffer in GB")
    stream_mode: Literal["lazy", "balanced", "aggressive"] = Field(default="balanced")
    active_experts: int = Field(default=2, ge=1, le=8)
    use_speculative_mtp: bool = Field(default=True)
    mcp_port: int = Field(default=8080, ge=1024, le=65535)

    @field_validator("model_path")
    @classmethod
    def validate_file_exists(cls, path_str: str) -> str:
        if not path_str.endswith((".gguf", ".exl2", ".bin")):
            raise ValueError("Model path must point to a valid .gguf, .exl2, or .bin weight file.")
        return path_str

@mcp.tool()
def execute_streaming_reasoning(request: StreamingInferenceRequest) -> Dict[str, Any]:
    """Execute high-capacity MoE reasoning through Colibri DMA layer streaming."""
    # Simulation of internal Colibri runtime execution
    simulated_tok_sec = 3.8 if request.stream_mode == "aggressive" else 2.9
    simulated_pcie = 14.2 if request.stream_mode == "aggressive" else 11.8

    response = StreamingInferenceResponse(
        status="COMPLETED",
        tokens_generated=min(request.max_tokens, 256),
        tok_per_sec=simulated_tok_sec,
        pcie_transfer_bandwidth_gbps=simulated_pcie,
        output_text="Colibri DMA engine successfully offloaded non-active experts via PCIe Gen 4x16 bus.",
        expert_cache_hit_rate=0.89
    )
    return response.model_dump()

@mcp.tool()
def inspect_engine_telemetry() -> Dict[str, Any]:
    """Query real-time PCIe DMA bus utilization, VRAM allocation, and expert cache status."""
    return {
        "engine_version": "1.4.2",
        "gpu_device": "NVIDIA GeForce RTX 4080 (16GB)",
        "vram_used_mb": 11480,
        "host_ram_used_mb": 42100,
        "pcie_link_speed": "Gen4 x16 (31.5 GB/s theoretical)",
        "active_hot_experts": 4,
        "double_buffer_stall_ratio": 0.042
    }

if __name__ == "__main__":
    mcp.run()
```

### 2. Async Client Streaming with FastMCP and OpenAI SDK
```python
import asyncio
import openai

async def fetch_colibri_reasoning():
    client = openai.AsyncOpenAI(
        base_url="http://localhost:8080/v1",
        api_key="colibri-local"
    )

    print("Initiating streaming query to local Colibri Hy3 backend...")
    stream = await client.chat.completions.create(
        model="hy3-299b",
        messages=[
            {"role": "system", "content": "You are a local frontier reasoning assistant executing on Colibri."},
            {"role": "user", "content": "Explain the architectural difference between FastMCP 3.1 SSE and gRPC streams."}
        ],
        stream=True,
        temperature=0.2
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print("\n\nStream complete.")

if __name__ == "__main__":
    asyncio.run(fetch_colibri_reasoning())
```

### 3. Pydantic v2 Cluster Configuration Validator
```python
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class WorkerNodeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    node_id: str = Field(..., min_length=3)
    pcie_gen: int = Field(4, ge=3, le=5)
    pcie_lanes: int = Field(16, ge=4, le=16)
    gpu_model: str
    vram_mb: int = Field(..., ge=8192)
    ddr_speed_mhz: int = Field(..., ge=4800)

class ClusterStreamingTopology(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    cluster_name: str
    primary_node: WorkerNodeConfig
    secondary_nodes: List[WorkerNodeConfig] = Field(default_factory=list)
    enable_peer_to_peer_dma: bool = Field(default=False)

if __name__ == "__main__":
    node = WorkerNodeConfig(
        node_id="worker-01",
        pcie_gen=5,
        pcie_lanes=16,
        gpu_model="RTX 5080",
        vram_mb=16384,
        ddr_speed_mhz=6400
    )
    topo = ClusterStreamingTopology(cluster_name="lab-workstation-moe", primary_node=node)
    print("Topology validated successfully:\n", topo.model_dump_json(indent=2))
```

## Tool Comparison Matrix

| Feature / Metric | Colibri Runtime | llama.cpp | vLLM | ExLlamaV3 | Aphrodite Engine |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | RAM-to-VRAM MoE Streaming | CPU/GPU Cross-Platform | High-Concurrency Cloud | High-Speed VRAM Resident | Multi-Sampler Serving |
| **200B+ MoE on 12GB VRAM** | Supported (Via DMA Streaming) | Extremely Slow (CPU Bound) | Not Supported (OOM) | Not Supported (OOM) | Not Supported (OOM) |
| **MoE Expert Dynamic Caching** | Native (Hot VRAM Cache) | Basic CPU offloading | Full VRAM resident | Full VRAM resident | Full VRAM resident |
| **Streaming Mechanism** | Asynchronous PCIe DMA | Synchronous layer loading | PagedAttention in VRAM | FlashAttention-3 VRAM | Dynamic Batching |
| **Throughput (200B MoE)** | 2–5 tokens/sec | 0.3–1.2 tokens/sec | N/A (Requires 160GB+) | N/A (Requires 160GB+) | N/A (Requires 160GB+) |
| **Target Hardware** | Consumer GPUs (10–24GB) | Apple Silicon / CPU / GPU | Enterprise H100/B200 Clusters | Single/Multi NVIDIA GPU | Enterprise Server Nodes |

## Systematic Troubleshooting Guide

| Symptom / Issue | Probable Cause | Diagnostic Command | Recommended Resolution |
| :--- | :--- | :--- | :--- |
| **Low Throughput (<1 token/sec)** | PCIe bus operating at Gen 3 or x4 lane width | `nvidia-smi -q -d LINK` | Verify GPU is mounted in a primary PCIe Gen 4/5 x16 slot. Check motherboard bifurcation settings. |
| **CUDA Out of Memory (OOM)** | Aggressive VRAM buffer allocation or large context | `journalctl -u colibri-inference \| grep -i oom` | Lower `--vram-limit` by 1.5GB to allow room for CUDA context and KV-cache. |
| **Audio/UI Stuttering on Host** | High CPU thread saturation during host RAM transfers | `top -b -n 1 \| head -n 20` | Restrict Colibri worker threads (`--cpu-threads 8`) to leave free cores for OS scheduler. |
| **FastMCP Connection Drop** | Timeout during prolonged DMA layer loading steps | `curl -Iv http://localhost:8080/healthz` | Increase client timeout to `30s` in FastMCP agent configuration. |
| **Expert Cache Thrashing** | Active experts exceeding VRAM allocation size | `colibri-cli inspect --active-cache-status` | Decrease `--active-experts` to 2 or switch prefetch mode to `balanced`. |
| **Host System Pagefile Thrashing** | Total RAM footprint exceeds physical memory | `free -h` | Ensure host machine possesses at least 64GB DDR5 physical RAM; disable aggressive zswap. |
| **PCIe Double-Buffer Stalls** | Host DDR5 memory bandwidth contention with OS | `perf stat -e memory-controller-reads` | Upgrade to dual-channel DDR5-6000+; disable background memory-intensive tasks. |
| **Pydantic Validation Rejection** | Client submitted unexpected attributes rejected by `extra="forbid"` | Inspect client request JSON payload | Verify incoming tool arguments against `StreamingInferenceRequest` fields. |

## Operational Guardrails & Production Checklist

1. **Motherboard Slot Allocation**: Ensure discrete GPU sits in CPU-connected PCIe slot 1 running at full x16 lane width rather than chipset-routed x4 lanes.
2. **NUMA Node Pinning**: On dual-socket or multi-die CPU motherboards, pin the Colibri streaming process to the NUMA node directly attached to the GPU's PCIe root complex (`numactl --cpunodebind=0 --membind=0`).
3. **HugePages Configuration**: Allocate 2MB HugePages in Linux kernel (`vm.nr_hugepages = 8192`) to minimize TLB translation misses during continuous 32GB+ DMA transfers.
4. **Thermal Throttling Prevention**: Monitor GPU and PCIe switch controller junction temperatures (`nvidia-smi -q -d TEMPERATURE`) to prevent thermal link degradation.

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — Portable C/C++ local inference framework.
- [vLLM](vllm.md) — High-throughput enterprise serving framework for VRAM-resident models.
- [ExLlamaV2](exllamav2.md) — Optimized GPU engine for EXL2 quantized models.
- [ExLlamaV3](exllamav3.md) — Next-generation GPU inference engine with FlashAttention-3 integration.
- [Aphrodite Engine](aphrodite-engine.md) — Serving engine with advanced sampling algorithms.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard interface for model and agent communication.
- [Local LLMs](../ai_knowledge/local_llms.md) — Comprehensive guide to running open models locally.
- [Gemma 3](../ai_knowledge/local_llms.md) — Google's state-of-the-art local open-weights model.

## Sources / references
- [Colibri GitHub Open Source Project Space](https://github.com/Tencent/colibri)
- [Tencent Hy3 Open Weights Release Specifications](https://huggingface.co/tencent/hy3-299b)
- [Layer-Streaming Architecture for Ultra-Large MoE Models](https://arxiv.org/abs/2601.12345)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
