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
This example demonstrates a complete Python FastMCP 3.1 tool server integrated with Jan's local OpenAI-compatible endpoint.

```python
import asyncio
import json
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import openai

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Jan-Local-Tools")

class LocalSystemStatusRequest(BaseModel):
    include_disk: bool = Field(True, description="Include local disk space metrics")

class LocalSystemStatusResponse(BaseModel):
    hostname: str
    vram_used_gb: float
    cpu_utilization: float
    status: str

@mcp.tool(name="get_local_system_status")
def get_local_system_status(request: LocalSystemStatusRequest) -> LocalSystemStatusResponse:
    """Query local workstation hardware metrics for Jan agent planning."""
    return LocalSystemStatusResponse(
        hostname="dev-workstation-01",
        vram_used_gb=14.2,
        cpu_utilization=22.4,
        status="optimal"
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
                        "include_disk": {"type": "boolean", "default": True}
                    }
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
This Python script validates model runtime parameters, GPU layer allocations, and inference engine metrics using Pydantic v2.

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class GPULayerConfig(BaseModel):
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
    model_id: str = Field(..., alias="modelId")
    context_window: int = Field(..., alias="contextWindow", ge=2048, le=262144)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    gpu_config: GPULayerConfig = Field(..., alias="gpuConfig")
    fastmcp_enabled: bool = Field(default=True, alias="fastmcpEnabled")
    mcp_servers: List[str] = Field(default_factory=list, alias="mcpServers")

class JanServerMetrics(BaseModel):
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
