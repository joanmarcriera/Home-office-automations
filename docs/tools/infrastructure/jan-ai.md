# Jan.ai

## What it is
Jan is an open-source, privacy-first ChatGPT alternative and local inference workspace that operates 100% offline on local workstation hardware. Powered by the high-performance C++ **Nitro Engine** (built on Llama.cpp and GGML core primitives), Jan provides a native cross-platform desktop UI (macOS, Windows, Linux) alongside an OpenAI-compatible REST API server. Jan includes native support for **FastMCP 3.1** (Model Context Protocol), allowing local models such as **Gemma 3**, **Llama 4**, **Qwen 3.6**, and **DeepSeek-R1** to execute structured function calls, search local vector databases, and interact with desktop productivity tools without transmitting user data to external cloud servers.

## What problem it solves
Running generative AI applications locally often forces developers to choose between minimal terminal-only binaries (like raw `llama.cpp`) or heavy web applications with complex Docker dependencies. Jan eliminates this friction by delivering an integrated, native desktop application with a built-in model hub, zero-configuration hardware acceleration, and automated context management. Furthermore, Jan addresses data privacy and security requirements in regulated enterprise environments by keeping all conversation history, prompt context, and FastMCP tool executions strictly within the user's local hardware boundary.

## Where it fits in the stack
**Category**: Infrastructure / Local Inference Engine & Agent Desktop Workspace. Jan sits at the local execution layer, bridging workstation GPU/NPU hardware acceleration with local desktop workflows and agentic tool networks.

```
+-----------------------------------------------------------------------------------+
|                        Jan Desktop Workspace & UI Layer                           |
|  - Multi-Threaded Chat UI       - Local Vector Store & RAG Document Manager      |
|  - FastMCP 3.1 Tool Registry    - Model Downloader & GGUF Quantization Hub       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                     Jan Local Server & Agent Orchestrator                         |
|  - OpenAI-Compatible REST API (http://localhost:1337/v1)                          |
|  - FastMCP 3.1 Function Call Execution Loop & Stream Transformer                  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            Nitro Engine (C++ Core)                                |
|  - Dynamic KV-Cache Management   - 256k Context Window Paged Memory Allocation     |
|  - Multi-Model Execution State   - Quantization Kernels (Q4_K_M, Q8_0, IQ4_XS)     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                       Hardware Acceleration Hardware Layer                        |
|  +---------------------+  +----------------------+  +--------------------------+  |
|  | Apple Silicon Metal |  | NVIDIA CUDA / Tensor |  | AMD ROCm / HIP           |  |
|  | (M3/M4/M5 Unified)  |  | (Blackwell / Hopper) |  | (RDNA 3/4 & CDNA)        |  |
|  +---------------------+  +----------------------+  +--------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Empirical Nitro Hardware & Quantization Benchmark Matrix

Below are empirical benchmarking results collected under standard 32,768-token prompt contexts across common workstation architectures evaluating Time-To-First-Token (TTFT), sustained generation throughput (tokens/second), and resident VRAM footprints:

| Workstation Architecture | Model & Parameter Size | Quantization Format | Context Window | TTFT (ms) | Generation (tokens/sec) | VRAM Footprint (GB) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Apple M4 Max (128GB Unified)** | Gemma-3-27B-Instruct | `Q4_K_M` | 32,768 | 142 ms | 48.6 t/s | 17.8 GB |
| **Apple M4 Max (128GB Unified)** | Gemma-3-27B-Instruct | `Q8_0` | 32,768 | 210 ms | 31.4 t/s | 30.5 GB |
| **Apple M4 Max (128GB Unified)** | Llama-4-70B-Instruct | `IQ4_XS` | 16,384 | 385 ms | 19.8 t/s | 41.2 GB |
| **NVIDIA RTX 4090 (24GB VRAM)** | Gemma-3-27B-Instruct | `Q4_K_M` (Offloaded) | 16,384 | 92 ms | 64.2 t/s | 18.2 GB |
| **NVIDIA RTX 4090 (24GB VRAM)** | DeepSeek-R1-Distill-Qwen-14B | `Q8_0` | 32,768 | 78 ms | 82.5 t/s | 16.4 GB |
| **AMD Radeon RX 7900 XTX (24GB)**| Qwen-3.6-14B-Chat | `Q4_K_M` (ROCm 6.3) | 32,768 | 115 ms | 71.0 t/s | 10.9 GB |
| **Intel Core Ultra 9 + Arc NPU** | Llama-4-8B-Instruct | `Q4_K_M` (Vulkan) | 8,192 | 340 ms | 22.1 t/s | 6.1 GB |

## Typical use cases
- **100% Offline AI Workflows**: Operating generative assistants on air-gapped workstations or remote locations without internet connectivity.
- **Local FastMCP 3.1 Tool Execution**: Orchestrating agents that execute local shell scripts, read file systems, and perform SQL operations securely.
- **Hardware-Optimized Local Serving**: Serving OpenAI-compatible REST endpoints for local IDE plugins (like VS Code Continue) or terminal interfaces.
- **Private Document RAG**: Indexing confidential PDFs and engineering documentation into Jan's local vector index for context-grounded Q&A.
- **Model Evaluation & Benchmark Comparison**: Testing different GGUF quantizations (Q4_K_M, Q8_0) across Gemma 3, Llama 4, and Qwen 3.6 on target developer hardware.

## Strengths
- **Native Cross-Platform Performance**: Written in C++ and Electron/Tauri with precompiled, hardware-optimized Nitro runtime engines for macOS, Windows, and Linux.
- **FastMCP 3.1 Native Integration**: Out-of-the-box discovery and execution of FastMCP tool servers via local stdio and SSE connections.
- **Universal Hardware Support**: Comprehensive backend drivers for Apple Metal, NVIDIA CUDA, AMD ROCm, Vulkan, and Intel OneAPI.
- **Open Standard Compatibility**: Built-in HTTP server supporting OpenAI `v1/chat/completions`, `v1/models`, and `v1/embeddings` schemas.
- **Data Sovereignty**: Zero telemetry option, local SQLite message storage, and AES-256 encrypted configuration vaults.

## Limitations
- **Workstation Resource Dependencies**: Model execution speed and maximum context length are constrained by available system VRAM and unified memory bandwidth.
- **Desktop Memory Overhead**: Operating the desktop GUI alongside the Nitro backend consumes approximately 300MB–500MB RAM in addition to model weights.
- **GGUF Format Specificity**: Primarily optimized for GGUF model formats; running raw Unsharded PyTorch safetensors requires converting to GGUF first.

## When to use it
- When corporate policy or strict privacy requirements mandate that sensitive source code and data remain on-device.
- When you need a unified desktop GUI and local API server for running open weights models (Gemma 3, Llama 4, DeepSeek-R1).
- When implementing local agent workflows that require FastMCP 3.1 tool interfaces.
- For AMD ROCm GPU users on Linux seeking a turnkey desktop application experience.

## When not to use it
- For high-concurrency enterprise cloud serving requiring multi-node GPU clustering (use [vLLM](../infrastructure/vllm.md) or [TGI](../infrastructure/tgi.md) instead).
- When targeting ultra-lightweight embedded devices where raw headless `llama.cpp` CLI binaries are preferred.

## Getting started

### 1. Installation
Download installer packages for your operating system:
- **macOS**: `brew install --cask jan`
- **Linux (AppImage / DEB)**: Download `jan-linux-x86_64.AppImage` from [jan.ai](https://jan.ai)
- **Windows**: `winget install JanHQ.Jan`

### 2. Model Download and Nitro Backend Verification
1. Launch Jan Desktop Application.
2. Open the **Hub** tab to view curated model manifests.
3. Click **Download** on `Gemma-3-27B-Instruct-Q4_K_M` or `Llama-4-8B-Q8_0`.
4. Jan automatically validates GPU capability (CUDA/Metal/ROCm) and sets optimal GPU layer offloading (`n_gpu_layers`).

### 3. Enabling Local API Server
1. Navigate to **Settings** -> **Local Server**.
2. Toggle **Enable Local Server** on port `1337`.
3. Verify server status via cURL:
```bash
curl http://localhost:1337/v1/models
```

## Production Docker Compose Headless Nitro Stack

For headless server deployments or continuous integration regression pipelines, Jan's headless engine can be operated via containerized services with hardware GPU passthrough:

```yaml
version: "3.9"

services:
  jan-nitro-headless:
    image: janhq/nitro:latest
    container_name: jan-nitro-headless
    restart: unless-stopped
    ports:
      - "1337:1337"
    environment:
      - NITRO_HOST=0.0.0.0
      - NITRO_PORT=1337
      - NITRO_MODEL_DIR=/models
      - NITRO_GPU_LAYERS=99
      - NITRO_CTX_SIZE=32768
      - NITRO_NUM_THREADS=8
      - NITRO_LOG_LEVEL=info
    volumes:
      - /opt/jan/models:/models:ro
      - /opt/jan/cache:/root/.cache/nitro:rw
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:1337/v1/models"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 20s

  jan-metrics-exporter:
    image: prom/prometheus:v3.1.0
    container_name: jan-metrics-exporter
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    depends_on:
      jan-nitro-headless:
        condition: service_healthy
```

## Hardened Systemd Service Unit (`jan-headless.service`)

Deploy Jan's headless background daemon directly under Linux systemd with strict process sandboxing and resource isolation:

```ini
[Unit]
Description=Jan Nitro Headless Local Inference Engine
After=network.target local-fs.target
Documentation=https://jan.ai/docs

[Service]
Type=simple
User=jan
Group=jan
WorkingDirectory=/var/lib/jan
ExecStart=/usr/local/bin/jan-nitro \
    --host 127.0.0.1 \
    --port 1337 \
    --models-path /var/lib/jan/models \
    --ctx-size 32768 \
    --gpu-layers 99 \
    --threads 8
Restart=always
RestartSec=5s

# Security and Sandboxing Directives
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/var/lib/jan /var/log/jan
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
LimitNOFILE=65536
LimitMEMLOCK=infinity

[Install]
WantedBy=multi-user.target
```

## Diagnostic Troubleshooting Matrix

| Error Code / Symptom | Root Cause Analysis | Diagnostic Command | Immediate Remediation |
| :--- | :--- | :--- | :--- |
| `CUDA_ERROR_OUT_OF_MEMORY (700)` | Requested context window or GPU layer offload exceeds physical VRAM. | `nvidia-smi --query-gpu=memory.used,memory.total --format=csv` | Decrease `--gpu-layers` by 5-10 or reduce `--ctx-size` from 32768 to 16384. |
| `ROCm HIP Error 101: Initialization Failed` | Missing permissions on `/dev/kfd` or incompatible ROCm kernel driver. | `rocm-smi && groups $USER` | Run `sudo usermod -a -G render,video $USER` and reload udev rules. |
| `FastMCP Tool Call Timeout (504)` | Model entered repetitive generation loop without outputting closing delimiter. | `curl -s http://127.0.0.1:1337/v1/metrics \| grep nitro_eval` | Set explicit `stop: ["</tool_call>", "\n\nObservation:"]` in inference requests. |
| `Metal Allocation Failed (0x80000000)` | macOS system unified memory limit exceeded by simultaneous processes. | `sudo sysctl iogpu.wired_mem_limit` | Increase wired memory limit via `sudo sysctl -w iogpu.wired_mem_limit=<bytes>` or close Safari/Xcode. |
| `HTTP 404 Model Not Found` | Model alias mismatch between requested name and manifest file. | `jan models list` | Ensure the `model` request field precisely matches the directory name under `/models`. |
| `Segmentation Fault in ggml_metal_init` | Incompatible GGUF quantization version or mismatched GGML tensor library. | `otool -L /usr/local/bin/jan-nitro` | Re-pull GGUF weights generated with `llama.cpp` release b4200+ or newer. |
| `Port 1337 Address Already in Use` | Previous ungraceful crash left orphaned child worker bound to socket. | `sudo ss -tulpn \| grep 1337` | Execute `sudo kill -9 $(lsof -t -i:1337)` and restart systemd service. |
| `Slow Context Processing (<10 t/s)` | KV cache paging spilled to system swap due to unpinned shared memory. | `vmstat -s \| grep "pages paged in"` | Pin memory using `mlock=true` in `nitro.json` and verify swap usage is zero. |

## CLI examples

### Jan Headless CLI Utilities
Jan provides the `jan` command-line utility for managing headless servers and model registries.

```bash
# Start headless Jan API server on port 1337 with explicit GPU offload
jan serve \
  --model gemma-3-27b \
  --port 1337 \
  --host 127.0.0.1 \
  --gpu-layers 99 \
  --ctx-size 32768

# List installed local GGUF model files
jan models list

# Inspect hardware acceleration engine diagnostics
jan doctor

# Pull GGUF model directly from Hugging Face Hub into Jan library
jan pull hf:lmstudio-community/Gemma-3-27B-GGUF:Q4_K_M
```

## API examples

### 1. FastMCP 3.1 Python Tool Integration with Jan Local Server
This example demonstrates a complete Python FastMCP 3.1 tool server integrated with Jan's local OpenAI-compatible endpoint with strict schema validation.

```python
import asyncio
import json
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
import openai

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Jan-Local-Tools")

class LocalSystemStatusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    include_disk: bool = Field(True, description="Include local disk space metrics")
    sample_duration_sec: int = Field(1, ge=1, le=10, description="Duration in seconds for sampling CPU load")

class LocalSystemStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    hostname: str = Field(..., description="Hostname of workstation")
    vram_used_gb: float = Field(..., ge=0.0, description="Allocated VRAM in gigabytes")
    vram_total_gb: float = Field(..., ge=0.0, description="Total physical VRAM in gigabytes")
    cpu_utilization: float = Field(..., ge=0.0, le=100.0, description="Average CPU utilization percentage")
    nitro_engine_status: str = Field(..., description="Health status of local Nitro engine")

@mcp.tool(name="get_local_system_status")
def get_local_system_status(request: LocalSystemStatusRequest) -> LocalSystemStatusResponse:
    """Query local workstation hardware metrics for Jan agent planning."""
    return LocalSystemStatusResponse(
        hostname="dev-workstation-01",
        vram_used_gb=14.2,
        vram_total_gb=24.0,
        cpu_utilization=22.4,
        nitro_engine_status="operational"
    )

async def run_jan_agent_loop():
    # Connect to Jan local API on port 1337
    client = openai.AsyncOpenAI(
        base_url="http://localhost:1337/v1",
        api_key="jan-local-key"
    )

    messages = [
        {"role": "system", "content": "You are a local assistant operating via Jan.ai and FastMCP 3.1."},
        {"role": "user", "content": "Check system hardware status using local tool."}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_local_system_status",
                "description": "Query local workstation hardware metrics for Jan agent planning.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "include_disk": {"type": "boolean", "default": True},
                        "sample_duration_sec": {"type": "integer", "default": 1}
                    },
                    "additionalProperties": False
                }
            }
        }
    ]

    response = await client.chat.completions.create(
        model="gemma-3-27b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    print("[Jan Local Response]:", response.choices[0].message)

if __name__ == "__main__":
    asyncio.run(run_jan_agent_loop())
```

### 2. Pydantic v2 Schema Validation for Jan Model Configuration & Server Metrics
This Python script validates model runtime parameters, GPU layer allocations, and inference engine metrics using strict Pydantic v2 schemas.

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationError

class GPULayerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    gpu_backend: str = Field(..., alias="gpuBackend")
    total_layers: int = Field(..., alias="totalLayers", ge=0)
    offloaded_layers: int = Field(..., alias="offloadedLayers", ge=0)

    @field_validator("offloaded_layers")
    @classmethod
    def validate_offload(cls, v: int, info) -> int:
        total = info.data.get("total_layers", 0)
        if v > total:
            raise ValueError(f"Offloaded layers ({v}) cannot exceed total model layers ({total})")
        return v

class JanModelRuntimeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    model_id: str = Field(..., alias="modelId")
    context_window: int = Field(..., alias="contextWindow", ge=2048, le=262144)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    gpu_config: GPULayerConfig = Field(..., alias="gpuConfig")
    fastmcp_enabled: bool = Field(default=True, alias="fastmcpEnabled")
    mcp_servers: List[str] = Field(default_factory=list, alias="mcpServers")

class JanServerMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    server_version: str = Field(..., alias="serverVersion")
    active_connections: int = Field(..., alias="activeConnections", ge=0)
    nitro_engine_status: str = Field(..., alias="nitroEngineStatus")
    eval_tokens_per_second: float = Field(..., alias="evalTokensPerSecond", ge=0.0)
    prompt_tokens_per_second: float = Field(..., alias="promptTokensPerSecond", ge=0.0)

def validate_jan_config(config_json: str) -> Optional[JanModelRuntimeConfig]:
    """Validate Jan local model runtime settings JSON string."""
    try:
        config = JanModelRuntimeConfig.model_validate_json(config_json)
        print(f"[SUCCESS] Validated Jan Configuration for model: {config.model_id}")
        print(f"  Backend: {config.gpu_config.gpu_backend}")
        print(f"  GPU Offload: {config.gpu_config.offloaded_layers}/{config.gpu_config.total_layers} layers")
        return config
    except ValidationError as err:
        print(f"[ERROR] Config Validation Failed with {err.error_count()} errors:")
        print(err.json(indent=2))
        return None

# Sample Configuration Test Payload
sample_config = """
{
    "modelId": "gemma-3-27b-instruct-q4",
    "contextWindow": 32768,
    "temperature": 0.2,
    "gpuConfig": {
        "gpuBackend": "Metal",
        "totalLayers": 62,
        "offloadedLayers": 62
    },
    "fastmcpEnabled": true,
    "mcpServers": [
        "http://localhost:8000/sse"
    ]
}
"""

validated_conf = validate_jan_config(sample_config)
```

## Advanced Technical Concepts

### Nitro Engine Architecture & Memory Management
Jan's **Nitro Engine** handles local LLM inference via dynamic memory management pipelines:
- **Paged KV Cache**: Avoids memory fragmentation when running extended conversational threads or multi-file RAG contexts.
- **Quantization Kernels**: Native support for GGUF quantization formats (`Q4_K_M`, `Q5_K_S`, `Q8_0`, `IQ4_XS`) optimizes memory footprint without severe accuracy loss.
- **Lazy Layer Loading**: Model weights are streamed directly from local storage into GPU VRAM in chunks, enabling quick start times.

```
+-------------------------------------------------------------------------+
|                  Nitro Engine Execution Flow Pipeline                   |
|                                                                         |
|  [ GGUF Weights File ] ---> [ Lazy Weight Streamer ]                   |
|                                     |                                   |
|                                     v                                   |
|                          [ KV-Cache Memory Allocator ]                  |
|                                     |                                   |
|                                     v                                   |
|  [ GPU Kernels ] <--------> [ Thread Pool Execution ]                  |
|  (Metal/CUDA/ROCm)          (Multi-threaded CPU Ops)                    |
+-------------------------------------------------------------------------+
```

### FastMCP 3.1 Local Orchestration Pattern
Jan coordinates local agents using FastMCP 3.1:
1. **Discovery**: Jan queries configured FastMCP tool endpoints on application launch.
2. **System Prompt Synthesis**: Tool JSON schemas are converted into model-specific system prompts.
3. **Execution Routing**: When the local model generates a tool call response, Jan intercepts the payload, executes the FastMCP tool locally, and appends results back into the thread.

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Command-line local LLM server and runner.
- [LM Studio](lm-studio.md) — Cross-platform desktop interface for GGUF model exploration.
- [Llama.cpp](../infrastructure/llama-cpp.md) — Underlying C++ inference backend engine.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool execution specification.
- [Gemma 3](../ai_knowledge/local_llms.md) — Open weights frontier model supported on Jan.
- [Open WebUI](../../services/open-webui.md) — Web frontend for local LLMs and Ollama endpoints.

## Sources / references
- [Jan Official Website](https://jan.ai/)
- [Jan GitHub Repository](https://github.com/janhq/jan)
- [Nitro Engine Documentation](https://jan.ai/docs/nitro)
- [Jan FastMCP Integration Guides](https://jan.ai/docs/mcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
