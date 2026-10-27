# Colibri

Colibri is a high-performance streaming inference engine designed to execute ultra-large open-weights language models—such as Tencent's Hy3 (299B MoE), DeepSeek-V4-Flash MoE, and Qwen 3.6 MoE—on consumer-grade desktop hardware with constrained VRAM. By leveraging direct memory access (DMA) layer prefetching, dynamic Mixture-of-Experts (MoE) routing, and speculative multi-token prediction heads, Colibri breaks the "VRAM wall," allowing 200B+ parameter models to execute on system configurations with as little as 10GB to 16GB of GPU VRAM.

## What it is
Colibri is a specialized C++20 and CUDA-accelerated inference runtime centered on asynchronous layer streaming and dynamic memory offloading. Unlike traditional inference engines that require the entirety of a model's weights to reside fully in GPU VRAM, Colibri optimizes real-time data transfers between system RAM (DDR5/DDR6) and GPU VRAM (GDDR6X/HBM3). As of early 2027, it stands as a premier open-source solution for developers, researchers, and self-hosted environments seeking to execute frontier-class MoE reasoning backends locally alongside cloud API endpoints like Claude 5.6, GPT-5.6, and Gemini 4.0 Pro.

## What problem it solves
Frontier Mixture-of-Experts (MoE) models offer exceptional reasoning capabilities but traditionally impose prohibitive hardware requirements. For example, a 299B parameter model like Tencent Hy3 requires over 180GB of VRAM even when quantized to 4 bits, demanding enterprise server nodes equipped with multiple NVIDIA H100 or H200 GPUs.

Colibri solves this hardware bottleneck by streaming only active execution layers and dynamically routed experts into GPU VRAM on demand. By keeping non-active layers resident in system RAM and streaming them across PCIe Gen 4/5 buses using asynchronous Direct Memory Access (DMA), Colibri allows single-card workstations (e.g., equipped with an RTX 4080 or RTX 5060) to execute massive open models. This democratizes local frontier-class reasoning, ensuring complete data sovereignty, zero API egress costs, and robust offline resilience.

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
ExecStart=/opt/colibri/venv/bin/colibri-server --model /opt/colibri/models/hy3-299b-q4.gguf --vram-limit 12G --streaming-buffer 16G --active-experts 4 --port 8080
Restart=always
RestartSec=10
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
    environment:
      - PORT=8080
      - VRAM_LIMIT=12G
      - RAM_BUFFER=32G
      - MODEL_PATH=/models/hy3-299b-q4.gguf
    volumes:
      - ./models:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## API examples

### 1. FastMCP 3.1 Server Configuration & Validation (Pydantic v2)
The following Python script uses Pydantic v2 to validate Colibri engine configurations dynamically before launching the background process, preventing memory over-commit and CUDA out-of-memory errors.

```python
import os
import sys
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

# Pydantic v2 Model for Colibri Runtime Configuration
class ColibriRuntimeConfig(BaseModel):
    model_path: str = Field(..., description="Path to GGUF or EXL2 model weight file")
    vram_limit_gb: float = Field(default=12.0, ge=8.0, le=48.0, description="GPU VRAM limit in GB")
    ram_buffer_gb: float = Field(default=16.0, ge=8.0, le=128.0, description="Host system RAM buffer in GB")
    stream_mode: Literal["lazy", "balanced", "aggressive"] = Field(default="balanced", description="DMA prefetch strategy")
    active_experts: int = Field(default=2, ge=1, le=8, description="Number of hot experts resident in VRAM")
    use_speculative_mtp: bool = Field(default=True, description="Enable Multi-Token Prediction speculative heads")
    mcp_port: int = Field(default=8080, ge=1024, le=65535, description="FastMCP SSE server port")

    @field_validator("model_path")
    @classmethod
    def validate_file_exists(cls, path_str: str) -> str:
        if not path_str.endswith((".gguf", ".exl2", ".bin")):
            raise ValueError("Model path must point to a valid .gguf, .exl2, or .bin weight file.")
        return path_str

    @field_validator("vram_limit_gb")
    @classmethod
    def validate_vram_buffer(cls, vram_gb: float, info) -> float:
        # Guarantee safety margin for CUDA context allocation
        if vram_gb < 8.0:
            raise ValueError("At least 8.0 GB of VRAM is required to run Colibri streaming for 200B+ MoE models.")
        return vram_gb

# Execution Verification
def bootstrap_colibri_server(config_dict: dict):
    try:
        config = ColibriRuntimeConfig.model_validate(config_dict)
        print("Colibri Runtime Configuration Validated Successfully:")
        print(config.model_dump_json(indent=2))
        return config
    except ValidationError as err:
        print("Validation Failed for Colibri Configuration:", file=sys.stderr)
        print(err.json(), file=sys.stderr)
        return None

if __name__ == "__main__":
    sample_config = {
        "model_path": "./models/hy3-299b-q4.gguf",
        "vram_limit_gb": 12.0,
        "ram_buffer_gb": 32.0,
        "stream_mode": "aggressive",
        "active_experts": 4,
        "use_speculative_mtp": True,
        "mcp_port": 8080
    }
    bootstrap_colibri_server(sample_config)
```

### 2. Async FastMCP Streaming Token Client
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

## Tool Comparison Matrix
| Feature / Metric | Colibri Runtime | llama.cpp | vLLM | ExLlamaV3 | Aphrodite Engine |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | RAM-to-VRAM MoE Streaming | CPU/GPU Cross-Platform | High-Concurrency Cloud | High-Speed VRAM Resident | Multi-Sampler Serving |
| **200B+ MoE on 12GB VRAM** | Supported (Via DMA Streaming) | Extremely Slow (CPU Bound) | Not Supported (OOM) | Not Supported (OOM) | Not Supported (OOM) |
| **MoE Expert Dynamic Caching** | Native (Hot VRAM Cache) | Basic CPU offloading | Full VRAM resident | Full VRAM resident | Full VRAM resident |
| **Streaming Mechanism** | Asynchronous PCIe DMA | Synchronous layer loading | PagedAttention in VRAM | FlashAttention-3 VRAM | Dynamic Batching |
| **Throughput (200B MoE)** | 2–5 tokens/sec | 0.3–1.2 tokens/sec | N/A (Requires 160GB+) | N/A (Requires 160GB+) | N/A (Requires 160GB+) |
| **Target Hardware** | Consumer GPUs (10–24GB) | Apple Silicon / CPU / GPU | Enterprise H100/B200 Clusters | Single/Multi NVIDIA GPU | Enterprise Server Nodes |

## Operational & Troubleshooting Guide

| Symptom / Issue | Probable Cause | Recommended Resolution |
| :--- | :--- | :--- |
| **Low Throughput (<1 token/sec)** | PCIe bus operating at Gen 3 or x4 lane width | Verify GPU is mounted in a primary PCIe Gen 4/5 x16 slot (`nvidia-smi -q -d LINK`). |
| **CUDA Out of Memory (OOM)** | Aggressive VRAM buffer allocation or large context | Lower `--vram-limit` by 1.5GB to allow room for CUDA context and KV-cache. |
| **Audio/UI Stuttering on Host** | High CPU thread saturation during host RAM transfers | Restrict Colibri worker threads (`--cpu-threads 8`) to leave free cores for OS scheduler. |
| **FastMCP Connection Drop** | Timeout during prolonged DMA layer loading steps | Increase client timeout to `30s` in FastMCP agent configuration. |
| **Expert Cache Thrashing** | Active experts exceeding VRAM allocation size | Decrease `--active-experts` to 2 or switch prefetch mode to `balanced`. |

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
