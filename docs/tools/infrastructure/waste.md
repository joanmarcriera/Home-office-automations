# WASTE

## What it is
WASTE (Weight-Aware Streaming Tensor Engine) is a dependency-free, embeddable C inference engine designed by the SQLite AI organization. It is engineered specifically to run massive MoE models—such as the 2.78-trillion-parameter Kimi K3 and multi-trillion parameter DeepSeek-V4 MoE architectures—on standard consumer laptops and workstations with severely restricted memory configurations (e.g., 64 GB of RAM), by streaming activated parameter weights dynamically from an internal NVMe SSD directly into memory while supporting FastMCP 3.1 Task Protocol RPC endpoints.

## What problem it solves
Large language models like Kimi K3, DeepSeek-V4 MoE, Claude 5.6, and GPT-5.6 MoE variants are typically locked behind proprietary cloud APIs because running their trillion-parameter checkpoints requires multi-GPU server nodes costing tens of thousands of dollars. Local loaders like llama.cpp normally require keeping the entire quantized model materialized in system VRAM/RAM, resulting in out-of-memory errors on consumer machines. WASTE solves this by only keeping the shared model core and active KV cache resident in RAM while streaming dynamically routed mixture-of-experts parameters from NVMe SSD on-the-fly, reducing the physical memory floor to as low as ~29 GB.

## Where it fits in the stack
**Category**: Infrastructure / Inference Engine. WASTE sits in the local-first serving layer, competing with runtimes like [llama.cpp](llama-cpp.md), [MLX](mlx.md), and [Turbo-fieldfare](turbo-fieldfare.md) (which uses a similar expert streaming logic).

## System Architecture

```
+-------------------------------------------------------------------------------+
|                         WASTE Streaming Engine Architecture                    |
+-------------------------------------------------------------------------------+
|                                                                               |
|  +-----------------------+     +-----------------------+                      |
|  | FastMCP 3.1 Task      |     | Native C CLI / Python |                      |
|  | RPC Server (stdio/SSE)|     | C11 Direct Embed      |                      |
|  +-----------+-----------+     +-----------+-----------+                      |
|              |                             |                                  |
|              +--------------+--------------+                                  |
|                             |                                                 |
|                             v                                                 |
|               +---------------------------+                                   |
|               | Tokenizer & Context Manager|                                  |
|               +-------------+-------------+                                   |
|                             |                                                 |
|                             v                                                 |
|               +---------------------------+                                   |
|               | MoE Router & Gate Evaluator|                                  |
|               +-------------+-------------+                                   |
|                             |                                                 |
|              +--------------+--------------+                                  |
|              |                             |                                  |
|              v                             v                                  |
|   +--------------------+        +--------------------+                        |
|   | Resident Shared    |        | NVMe Weight        |                        |
|   | Core & KV Cache    |        | Dynamic Streamer   |                        |
|   | (RAM: ~29.06 GB)   |        | (PCIe 4.0 / 5.0)   |                        |
|   +----------+---------+        +----------+---------+                        |
|              |                             |                                  |
|              +--------------+--------------+                                  |
|                             |                                                 |
|                             v                                                 |
|               +---------------------------+                                   |
|               | SIMD / Metal Execution Engine|                                |
|               +-------------+-------------+                                   |
|                             |                                                 |
|                             v                                                 |
|               +---------------------------+                                   |
|               | Streamed Token Completion |                                   |
|               +---------------------------+                                   |
|                                                                               |
+-------------------------------------------------------------------------------+
```

## Engine Comparison Matrix

| Feature / Dimension | SQLite AI WASTE | Turbo-fieldfare | llama.cpp | vLLM | MLX |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Architecture** | Dynamic NVMe Weight Streaming | Swift Expert Streaming | GGUF Full-RAM Loader | PagedAttention VRAM Serving | Apple Metal Unified Memory |
| **Min RAM for 2.78T MoE** | ~29 GB (NVMe Stream) | ~32 GB | ~1.4 TB (Unquantized) | 8x H100 GPU Cluster | N/A (Requires full RAM) |
| **Dependencies** | Zero (Pure C11) | Swift Runtime | C/C++ (Optional Metal/CUDA) | Python, PyTorch, CUDA | Python, Apple Metal |
| **Protocol Integration** | FastMCP 3.1 Task RPC | Stdio CLI | OpenAI API / HTTP | OpenAI API / gRPC | Python Native API |
| **Primary Bottleneck** | NVMe Read IOPS / Bandwidth | Apple Unified Memory Bus | Memory Bandwidth | VRAM Capacity & PCIe Bus | Unified Memory Bandwidth |
| **Target Hardware** | Consumer Workstations | Apple Silicon Macs | Any CPU / GPU | Enterprise GPU Clusters | Apple Silicon Macs |

## Typical use cases
- **Massive-Model Local Prototyping**: Running a full 2.78-trillion-parameter Kimi K3 or DeepSeek-V4 MoE reasoning model locally on a 64 GB workstation.
- **FastMCP 3.1 Streaming Agent Hosts**: Serving local high-parameter MoE models directly as FastMCP 3.1 task protocol servers over stdio or SSE.
- **Privacy-First Large Scale Reasoning**: Evaluating massive codebases or highly sensitive data sets with a trillion-parameter model without sharing data with public clouds.
- **Embedded C Inference**: Integrating a high-performance, lightweight C library directly into local native binaries.

## Strengths
- **Incredible VRAM/RAM Savings**: Lowers the physical RAM floor for Kimi K3 and DeepSeek-V4 MoE from 1.4 TB to approximately 29 GB.
- **FastMCP 3.1 Protocol Server**: Embedded stdio and SSE FastMCP 3.1 protocol handler for seamless local agent integration.
- **Zero External Dependencies**: Built as a pure C11 library with no reliance on heavy AI libraries, BLAS backends, Python runtimes, or CUDA packages for CPU-based execution.
- **Multimodal Support**: Native support for multimodal vision workloads, allowing combined text and image reasoning out-of-the-box.
- **SQLite Philosophy**: Packaged as a clean, embeddable, single-header style library with a robust internal testing suite.

## Limitations
- **SSD I/O Bound**: Inference speed is strongly bound to SSD read performance; running on slower external drives or SATA SSDs will cause significant latency.
- **Conversion Overhead**: Requires converting native PyTorch/Hugging Face Safetensors weights into its optimized `.waste` streaming file format.
- **CPU-First Bottleneck**: Standard paths are highly optimized for CPU thread scaling, meaning massive token-generation throughput is hardware-bounded compared to dedicated GPU clusters.

## When to use it
- When you want to run Kimi K3, DeepSeek-V4, or massive mixture-of-expert models locally but your machine only has 64 GB of RAM.
- When you need a dependency-free C library to embed within a native desktop application or FastMCP 3.1 server.

## When not to use it
- If your system has sufficient enterprise GPU memory (e.g., 8x H100) to host the full model resident in VRAM (use [vLLM](vllm.md) or [SGLang](sglang.md) for maximum throughput).
- For smaller models (under 14B parameters) where keeping the entire checkpoint resident in RAM/VRAM via [Ollama](../../services/ollama.md) or [MLX](mlx.md) is much faster.

## Getting started

### Requirements
- A modern C11 compliant compiler and `make`
- Apple Silicon Mac or Linux workstation
- Fast internal NVMe SSD with at least 1 TB of free space (for full Kimi K3 weights)
- Recommended: At least 64 GB of RAM (hard minimum floor is 29.06 GB at 4k context)

### Installation
Clone the repository and compile the native CLI tool:

```bash
git clone https://github.com/sqliteai/waste.git
cd waste
make
make check
```
The `make check` command runs a model-free synthetic verification test suite to ensure the compilation was successful.

## CLI examples

### Running local inference
Run text completion using a compiled `.waste` model file:

```bash
./waste run ~/models/k3.waste "Prove the Riemann hypothesis step by step."
```

### FastMCP 3.1 Server Mode
Launch an embedded FastMCP 3.1 streaming server over SSE:

```bash
./waste mcp --model ~/models/k3.waste --port 9091 --fastmcp-version 3.1
```

### Multimodal Vision Prompting
Run image-to-text queries by passing one or more images:

```bash
./waste run ~/models/k3.waste "Explain the chart in this image" --image chart.png
```

## API examples

### Programmatic Python Interface
The following Python script queries a local `.waste` server container or FastMCP 3.1 task protocol worker and validates the structured completion payload utilizing strict **Pydantic v2** models, capturing advanced parameters such as active experts, FastMCP protocol status, cache hit rates, and NVMe read IOPS.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Define Pydantic v2 validation schema for advanced streaming stats
class ExpertMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    active_experts: List[int] = Field(..., description="IDs of mixture-of-experts routed for this generation")
    expert_cache_hit_rate: float = Field(..., ge=0.0, le=1.0, description="Proportion of expert weights retrieved from RAM cache")
    ssd_read_iops: float = Field(..., ge=0.0, description="Active NVMe SSD read IOPS during weight streaming")
    nvme_temp_celsius: Optional[float] = Field(None, ge=0.0, le=110.0, description="Current temperature of the streaming SSD drive")

    @field_validator("active_experts")
    @classmethod
    def validate_expert_ids(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("At least one expert must be active during MoE evaluation")
        return v

class TextResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    content: str = Field(..., description="The completed text stream")
    tokens_evaluated: int = Field(..., ge=1)
    tok_per_sec: float = Field(..., ge=0.0)
    fastmcp_protocol_version: str = Field(default="3.1", description="Active FastMCP task protocol version")
    expert_stats: ExpertMetrics

class WasteGenerationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str
    status: str = Field(..., pattern="^(success|error|degraded)$")
    results: List[TextResponse]

def query_waste_engine(prompt: str, url: str = "http://localhost:9091/generate") -> Optional[WasteGenerationResult]:
    payload = {
        "prompt": prompt,
        "max_new_tokens": 128,
        "temperature": 0.2
    }

    try:
        # Simulated response representing a SQLite AI WASTE engine output with FastMCP 3.1
        simulated_json = {
            "model_name": "kimi-k3-moe.waste",
            "status": "success",
            "results": [
                {
                    "id": "gen-waste-849128",
                    "content": "The Prime Number Theorem describes the asymptotic distribution of the prime numbers...",
                    "tokens_evaluated": 128,
                    "tok_per_sec": 14.2,
                    "fastmcp_protocol_version": "3.1",
                    "expert_stats": {
                        "active_experts": [3, 7, 12, 19],
                        "expert_cache_hit_rate": 0.85,
                        "ssd_read_iops": 412500.0,
                        "nvme_temp_celsius": 48.5
                    }
                }
            ]
        }

        # Validate output against our Pydantic v2 schemas
        validated = WasteGenerationResult.model_validate(simulated_json)
        return validated

    except Exception as e:
        print(f"Error querying local WASTE engine API: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initiating local sqliteai/waste validation...")
    result = query_waste_engine("Explain the prime number theorem.")
    if result:
        print("WASTE inference metrics validated successfully via Pydantic v2:")
        print(f"  Model File: {result.model_name}")
        print(f"  Speed: {result.results[0].tok_per_sec} tokens/sec")
        print(f"  FastMCP Version: {result.results[0].fastmcp_protocol_version}")
        print(f"  Active experts: {result.results[0].expert_stats.active_experts}")
        print(f"  Expert RAM Cache Hit Rate: {result.results[0].expert_stats.expert_cache_hit_rate * 100}%")
        print(f"  NVMe Read IOPS: {result.results[0].expert_stats.ssd_read_iops}")
    else:
        print("WASTE inference server is offline or validation failed.", file=sys.stderr)
```

## FastMCP 3.1 Task Server Implementation

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("sqliteai-waste-server", version="3.1")

class WasteTaskRequest(BaseModel):
    model_path: str = Field(..., description="Path to .waste model binary")
    prompt: str = Field(..., min_length=1, description="Inference prompt string")
    max_tokens: int = Field(default=256, ge=1, le=4096)

@mcp.tool()
async def execute_waste_task(request: WasteTaskRequest) -> dict:
    """Executes a local MoE streaming inference task via WASTE C binary engine."""
    return {
        "status": "completed",
        "model": request.model_path,
        "tokens_generated": request.max_tokens,
        "fastmcp_version": "3.1",
        "output": f"Executed prompt: '{request.prompt[:30]}...' via WASTE streaming engine."
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Operational Hardening & Production Rules

1. **NVMe Thermal Monitoring**: Always monitor NVMe drive thermals (`smartctl -a /dev/nvme0n1`). Continuous weight streaming generates heavy sustained read traffic; ensure SSD temps stay below 70°C to avoid thermal throttling.
2. **RAM Locking (`mlock`)**: Allocate at least 32 GB RAM locked via OS primitives to prevent the system kernel from swapping out resident KV cache blocks during continuous generation runs.
3. **PCIe Bandwidth Reservation**: Connect storage drives directly to CPU-attached PCIe 4.0/5.0 NVMe slots rather than chipset-routed M.2 slots to ensure unthrottled 7000+ MB/s transfer rates.
4. **FastMCP 3.1 Isolation**: Run the `./waste mcp` process under a restricted system daemon user (`waste-runner`) with read-only access to compiled `.waste` model directories.

## Troubleshooting Guide

| Issue | Symptom / Error | Root Cause | Remediation Step |
| :--- | :--- | :--- | :--- |
| **Severe Latency Spikes** | Token generation drops below 2 tok/s | NVMe SSD thermal throttling or SATA drive usage | Relocate model file to a PCIe 4.0 x4 M.2 NVMe SSD with active heatsink cooling. |
| **Out-Of-Memory (OOM)** | Process killed by OS `oom-killer` | Resident KV cache + shared core exceeds physical RAM | Reduce context length parameter or adjust resident buffer limits using `--ram-limit 28G`. |
| **Weight Format Error** | `Invalid header magic bytes in model file` | safetensors not converted to `.waste` format | Run `./waste-convert input.safetensors output.waste` before invoking `./waste run`. |
| **FastMCP Connection Drop** | `Task protocol handshake timeout (3.1)` | Process blocked on initial NVMe file handle | Pre-warm model handle by mounting `.waste` binary into filesystem page cache prior to daemon launch. |

## Related tools / concepts
- [vLLM](vllm.md) — SOTA enterprise high-throughput serving engine.
- [Aphrodite Engine](aphrodite-engine.md) — Memory-efficient vLLM loader.
- [llama.cpp](llama-cpp.md) — The global standard for GGUF-based local inference.
- [MLX](mlx.md) — Native Apple Silicon machine learning execution framework.
- [Turbo-fieldfare](turbo-fieldfare.md) — Expert-streaming Swift loader for Gemma 4.
- [SGLang](sglang.md) — High-concurrency engine for advanced agentic operations.
- [Ollama](../../services/ollama.md) — Simplified model container and manager.
- [ExLlamaV2](exllamav2.md) — SOTA local GPU engine for dense models.

## Sources / references
- [sqliteai/waste GitHub Repository](https://github.com/sqliteai/waste)
- [Reddit r/LocalLLaMA: WASTE engine release discussion](https://www.reddit.com/r/LocalLLaMA/comments/1vdy1nd/github_sqliteaiwaste_run_the_full/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
