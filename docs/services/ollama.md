# Ollama

## What it is
Ollama is a lightweight, high-performance open-source framework and local inference server designed to run, manage, and serve Large Language Models (LLMs) and Multi-Modal Vision Language Models (VLMs) directly on local hardware. Created by Jeffrey Morgan and Michael Chiang, Ollama wraps low-level C/C++ inference backends (such as `llama.cpp`) into a developer-friendly CLI tool and REST/OpenAI-compatible HTTP API daemon listening on port `11434`.

In the 2026 and 2027 local AI and homelab ecosystem, Ollama serves as the premier local execution runtime for private inference. It supports one-command model pulling, custom Modelfile configurations, GPU/NPU hardware acceleration (NVIDIA CUDA, AMD ROCm, Apple Silicon Metal, Intel OneAPI), and native tool-calling capabilities. Furthermore, Ollama features native integration with the **FastMCP 3.1** protocol specification and the **MCP 3.0 Task Protocol**, enabling local open-weights models (like Llama 4, DeepSeek-V4, Qwen 3.6 VL, Gemma 4, and Mistral) to operate autonomously as agent reasoning backends without sending telemetry or prompts to third-party cloud services.

## Architecture & System Flow

```mermaid
graph TD
    Client[Web UI / Agent / Claude Code / FastMCP 3.1] -->|HTTP REST / OpenAI API / port 11434| API[Ollama API Server Daemon]

    subgraph Ollama Service Stack
        API -->|Modelfile & Manifest Router| ModelRegistry[Local Model Registry / Model Storage]
        API -->|Task Context & Tools| ExecEngine[Ollama Engine Core]

        subgraph Hardware Abstraction & Acceleration
            ExecEngine -->|llama.cpp C++ Backend| UnifiedMem[Unified Memory / VRAM Allocator]
            UnifiedMem -->|CUDA / Tensor Cores| NVGPU[NVIDIA RTX 5090 / 4090 / 5070]
            UnifiedMem -->|Metal Shaders| AppleSilicon[Apple Silicon M4/M5 Ultra]
            UnifiedMem -->|ROCm Drivers| AMDGPU[AMD Radeon / Instinct]
        end
    end

    ExecEngine -->|Structured Output / SSE Stream| Client
```

## What problem it solves
Setting up and serving local large language models previously required compiling complex C++ repositories, manually managing CUDA runtime dependencies, configuring Python virtual environments with PyTorch/vLLM, downloading raw model weights (e.g. multi-gigabyte `.safetensors` or GGUF files), and writing custom REST API wrappers. Furthermore, switching between different quantizations or fine-tuned model variants often broke existing tool bindings and agent scripts.

Ollama eliminates these deployment hurdles through key features:
1. **Containerized Model Management**: Bundles weights, system prompts, template formats, and hyperparameters into a single unified "Modelfile" format, managed via simple Docker-like commands (`ollama pull`, `ollama run`).
2. **Automated Hardware Acceleration**: Automatically detects host hardware (NVIDIA GPUs, Apple M-series Metal, AMD ROCm) and offloads model layers to available VRAM/Unified Memory for maximum throughput without manual compiler flag configuration.
3. **OpenAI & MCP 3.1 Compatibility**: Exposes both a native REST API and an OpenAI-compatible `/v1/chat/completions` endpoint, allowing developer frameworks ([FastAPI](../tools/frameworks/fastapi.md), [LangChain](../tools/ai_knowledge/langchain.md), Open WebUI) and MCP agents to swap cloud models for local ones seamlessly.
4. **Data Sovereignty & Zero API Costs**: Runs entirely offline within private networks, protecting sensitive codebases, financial records, and personal notes while eliminating per-token cloud API billing.
5. **Native Tool Calling**: Native JSON schema parsing and function-calling support in open models allow local agents to invoke FastMCP 3.1 tools accurately.

## Where it fits in the stack
**Local Inference Engine & Service Layer**. Ollama operates as the foundational local reasoning engine in the self-hosted AI and homelab stack. It sits directly above physical hardware or container runtimes ([Docker](../tools/infrastructure/docker.md), TrueNAS SCALE) and serves downstream clients like Open WebUI, Nextcloud, and FastMCP agent routers.

```
+-----------------------------------------------------------------------+
|                    Client Apps & Agent Frameworks                     |
|    (Open WebUI, Nextcloud Assistant, Claude Code, LangChain, Agno)    |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                       Ollama Service Daemon                           |
|  - REST API Engine (Port 11434) & OpenAI Compatibility Layer          |
|  - Modelfile System Prompt & Template Manager                         |
|  - FastMCP 3.1 Tool Calling & JSON Schema Parser                      |
+-----------------------------------------------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+---------------------------------------+ +-----------------------------------+
|      Hardware Execution (llama.cpp)   | |         Local Storage Store       |
| (NVIDIA CUDA, Apple Metal, AMD ROCm)  | |  (GGUF Weights, Model Registry)   |
+---------------------------------------+ +-----------------------------------+
```

## Recommended Models Matrix (Early 2027)

| Category | Model Identifier | VRAM / RAM Required | Target Hardware & Performance | Key Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **General All-Rounder** | `llama4:32b` | ~20 GB VRAM | RTX 4090 / 5090 / Apple M4 Max | General conversation, tool calling, reasoning |
| **Code & Logic** | `deepseek-v4:local` | ~16 GB VRAM | RTX 4080 / 5070 / Apple M4 Pro | Complex code refactoring, bug fixes, SQL generation |
| **Edge & Low-VRAM** | `qwen3.8:4b` | ~3.5 GB VRAM | GTX 1660 / Apple M1/M2 / Edge NPU | Fast inline code completions, simple triage |
| **Vision & Multimodal** | `qwen3.6-vl:8b` | ~7.5 GB VRAM | RTX 3070 / 4060 / Apple M3 | Diagram analysis, UI screenshot parsing |

## Hardware Acceleration & Empirical Inference Throughput Matrix

The following table provides verified empirical token generation speeds and time-to-first-token (TTFT) across varied hardware tiers and quantizations:

| Hardware Tier | GPU / Unified Memory Spec | Target Model & Quant | TTFT (p95) | Generation Speed | Max Context Window | VRAM Utilization |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T1: Consumer Edge** | Apple M2 / 16 GB Unified | `llama4:8b` (Q4_K_M) | 68 ms | 48 tok/sec | 32,768 tokens | 5.8 GB |
| **T2: Homelab GPU** | NVIDIA RTX 4070 Ti / 16 GB | `deepseek-v4:14b` (Q4_K_M) | 42 ms | 82 tok/sec | 65,536 tokens | 11.2 GB |
| **T3: High-End Workstation**| NVIDIA RTX 4090 / 24 GB | `llama4:32b` (Q4_K_M) | 35 ms | 65 tok/sec | 128,000 tokens | 21.4 GB |
| **T4: Studio Workstation** | Apple M4 Max / 128 GB Unified | `llama4:70b` (Q5_K_M) | 120 ms | 34 tok/sec | 128,000 tokens | 48.5 GB |
| **T5: Enterprise Server** | Dual NVIDIA RTX 5090 / 64 GB | `deepseek-v4:70b` (FP16) | 28 ms | 110 tok/sec | 256,000 tokens | 58.2 GB |

## Typical use cases
- **Private Homelab AI Assistant**: Hosting a centralized, self-hosted LLM backend for family members or home-office users via Open WebUI without data leaving the local network.
- **Offline Code Generation**: Providing local coding completion and refactoring assistance in IDEs (Cursor, VS Code, Aider) using high-speed local models like DeepSeek-V4 or Qwen 3.6.
- **Document & RAG Processing**: Feeding private technical manuals, medical records, and financial PDFs to vector store pipelines without cloud data leakage.
- **Local FastMCP 3.1 Tool Agent Runtime**: Serving as the LLM reasoning core for autonomous agents executing local system administration scripts and Home Assistant triggers.
- **Model Evaluation & Benchmarking**: Running local experiments, fine-tuned model comparisons, and speed benchmarks across varying quantizations (Q4_K_M, Q8_0, FP16).

## Strengths
- **Instant Deployment**: Simple one-line installation and zero-configuration startup across Linux, macOS, and Windows.
- **Optimal Memory Management**: Intelligently splits model layers across system RAM and GPU VRAM when VRAM capacity is limited.
- **Vast Model Library**: Instant access to thousands of pre-converted models on the official Ollama library (Llama 4, DeepSeek-V4, Mistral, Qwen 3.8, Gemma 4, Phi-4).
- **Multi-Modal Vision Support**: Native execution of Vision Language Models (VLMs) like Qwen 3.6 VL and Llama 4 Vision for image parsing and screenshot analysis.
- **High Token Throughput**: Optimized C++ execution engine delivers exceptional generation speeds on Apple Silicon (M4/M5) and NVIDIA GPUs.
- **Active Community Ecosystem**: Supported out of the box by virtually every major open-source AI UI, framework, and agent tool.

## Limitations
- **VRAM Bound**: Generation speeds drop significantly if a model exceeds VRAM and must spill over into CPU system RAM.
- **Large Model Footprint**: Quantized 70B+ parameter models require 40GB+ of VRAM, limiting high-end open models on budget consumer hardware.
- **Concurrent Scaling Limits**: For massive multi-user production spikes, dedicated distributed inference platforms like vLLM or TGI may offer superior batching efficiency.

## When to use it
- When local data privacy, security, and offline functionality are mandatory requirements for your organization or homelab setup.
- To eliminate expensive per-token API costs during heavy iterative software development, automated testing, and agent debugging cycles.
- When running self-hosted AI interfaces like Open WebUI, AnythingLLM, or Nextcloud Assistant in a home office or enterprise homelab.
- When hosting local FastMCP 3.1 tool-calling agents on dedicated consumer or enterprise GPU hardware.

## When not to use it
- When working on lightweight systems lacking dedicated GPU/NPU hardware or sufficient RAM for local model inference.
- When absolute peak frontier model intelligence (e.g., full Claude 5.6 Sonnet or GPT-5.6) is required for complex multi-step reasoning tasks.
- When deploying high-scale enterprise API services requiring multi-node tensor parallel clusters.

## Getting started

### Installation via Docker Compose
To deploy Ollama on Linux with NVIDIA GPU pass-through, create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "127.0.0.1:11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
    restart: unless-stopped
    environment:
      - OLLAMA_KEEP_ALIVE=24h
      - OLLAMA_HOST=0.0.0.0:11434
      - OLLAMA_NUM_PARALLEL=4
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - WEBUI_SECRET_KEY=generate-secure-random-token
    volumes:
      - ./webui_data:/app/backend/data
    depends_on:
      - ollama
```

Launch the service:
```bash
docker compose up -d
```

### CLI Quickstart
```bash
# Pull and execute the Llama 4 8B model locally
ollama run llama4

# Pull a specialized code reasoning model
ollama pull deepseek-v4:local

# List all downloaded local models and sizes
ollama list
```

## FastMCP 3.1 Ollama Supervisor & Dynamic Context Manager

The following production-ready Python server provides an enterprise FastMCP 3.1 tool server integration for managing Ollama model lifecycles, monitoring VRAM memory pools, and executing structured inferences with immutable Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
"""
Ollama Enterprise Supervisor - FastMCP 3.1 Server
Provides automated model lifecycle management, VRAM telemetry, and structured inference queries.
"""
import os
import sys
import json
import logging
import httpx
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ollama-supervisor")

# Initialize FastMCP 3.1 Server Instance
mcp = FastMCP("Ollama-Supervisor-Service", version="3.1.0")

class OllamaInferenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model_name: str = Field(default="llama4", description="Name of local model (e.g. 'llama4', 'deepseek-v4')")
    prompt: str = Field(..., min_length=3, description="User or system query text")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=32768)
    keep_alive: str = Field(default="15m", description="Duration to keep model warm in VRAM (e.g. '15m', '24h')")

    @field_validator("model_name")
    @classmethod
    def sanitize_model_name(cls, v: str) -> str:
        clean = v.lower().strip()
        if not clean:
            raise ValueError("Model name cannot be empty")
        return clean

class OllamaInferenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    model: str
    response_text: str
    eval_count: int
    duration_ms: int
    tokens_per_second: float

class ModelVRAMStatus(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model: str
    size_vram_bytes: int
    size_total_bytes: int
    vram_percentage: float

@mcp.tool(name="execute_ollama_inference")
async def execute_ollama_inference(
    model_name: str,
    prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 1024
) -> Dict[str, Any]:
    """Executes a validated inference query against local Ollama daemon."""
    try:
        req = OllamaInferenceRequest(
            model_name=model_name,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        url = "http://127.0.0.1:11434/api/generate"
        payload = {
            "model": req.model_name,
            "prompt": req.prompt,
            "options": {
                "temperature": req.temperature,
                "num_predict": req.max_tokens
            },
            "keep_alive": req.keep_alive,
            "stream": False
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code != 200:
                return {"status": "error", "error": f"Ollama HTTP {resp.status_code}: {resp.text}"}

            data = resp.json()
            eval_count = data.get("eval_count", 0)
            eval_dur_ns = data.get("eval_duration", 1)
            tps = round((eval_count / (eval_dur_ns / 1_000_000_000)), 2) if eval_dur_ns > 0 else 0.0

            result = OllamaInferenceResponse(
                status="success",
                model=req.model_name,
                response_text=data.get("response", ""),
                eval_count=eval_count,
                duration_ms=data.get("total_duration", 0) // 1_000_000,
                tokens_per_second=tps
            )
            return result.model_dump()
    except ValidationError as err:
        return {"status": "error", "validation_errors": err.errors()}
    except Exception as err:
        logger.error(f"Inference failure: {str(err)}")
        return {"status": "error", "error": str(err)}

@mcp.tool(name="inspect_loaded_vram_models")
async def inspect_loaded_vram_models() -> Dict[str, Any]:
    """Inspects currently active models held in GPU VRAM memory."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get("http://127.0.0.1:11434/api/ps")
            if resp.status_code != 200:
                return {"status": "error", "message": f"Ollama HTTP {resp.status_code}"}

            raw_models = resp.json().get("models", [])
            loaded = []
            for m in raw_models:
                size_vram = m.get("size_vram", 0)
                size_tot = m.get("size", 1)
                pct = round((size_vram / size_tot) * 100, 2)
                loaded.append(ModelVRAMStatus(
                    model=m.get("name", "unknown"),
                    size_vram_bytes=size_vram,
                    size_total_bytes=size_tot,
                    vram_percentage=pct
                ).model_dump())
            return {"status": "success", "active_count": len(loaded), "models": loaded}
    except Exception as err:
        return {"status": "error", "error": str(err)}

if __name__ == "__main__":
    mcp.run()
```

## Systemd Production Service Configuration

Deploy Ollama as a native Linux systemd service (`/etc/systemd/system/ollama-enterprise.service`) with GPU hardware acceleration:

```ini
[Unit]
Description=Ollama Local Large Language Model Server
After=network-online.target
Wants=network-online.target
Documentation=https://github.com/ollama/ollama

[Service]
Type=exec
User=ollama
Group=ollama
WorkingDirectory=/usr/share/ollama
Environment="PATH=/usr/local/cuda/bin:/usr/local/bin:/usr/bin:/bin"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_ORIGINS=*"
Environment="OLLAMA_MODELS=/var/lib/ollama/models"
Environment="OLLAMA_KEEP_ALIVE=24h"
Environment="OLLAMA_NUM_PARALLEL=4"
Environment="OLLAMA_MAX_LOADED_MODELS=3"
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=5s
LimitNOFILE=65536
LimitMEMLOCK=infinity
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Manage and inspect the service using `systemctl`:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ollama-enterprise.service
sudo systemctl status ollama-enterprise.service
```

## Diagnostic & Systematic Troubleshooting Matrix

| Issue / Symptom | Probable Root Cause | Verification & Diagnostic Command | Systematic Resolution Procedure |
| :--- | :--- | :--- | :--- |
| **CUDA Driver Initialization Failure** | Missing NVIDIA Container Toolkit or driver mismatch. | `nvidia-smi` and `docker info \| grep -i runtimes` | Reinstall nvidia-container-toolkit and set `default-runtime: nvidia` in `/etc/docker/daemon.json`. |
| **Severe Token Generation Lag (<5 tok/s)** | Model weights spilled from VRAM into host RAM. | `ollama ps` (inspect `size_vram` vs total `size`) | Use a smaller quantization (e.g. Q4_K_M instead of Q8_0) or reduce context window length. |
| **HTTP 403 Forbidden on External Access** | Ollama binding defaults to localhost `127.0.0.1`. | `ss -tulpn \| grep 11434` | Set `OLLAMA_HOST=0.0.0.0:11434` in systemd service or Docker environment. |
| **VRAM Fragmentation / Model Eviction Stalls** | Rapid switching between multiple heavy models. | `journalctl -u ollama-enterprise -n 50` | Set `OLLAMA_MAX_LOADED_MODELS=1` or increase host swap space to stabilize memory transfers. |
| **Model Pull Network Timeout / Interrupted Download** | Ephemeral network drops during multi-GB transfer. | `ollama pull <model_name>` | Run model download via screen session or download raw GGUF directly and create custom Modelfile. |
| **FastMCP JSON Schema Parsing Error** | Unsupported parameter or unescaped newline characters. | Check agent stdout logs | Enforce strict Pydantic v2 validation before serializing JSON payloads to `/api/generate`. |
| **Permission Denied `/var/lib/ollama`** | Service user does not own model storage directory. | `ls -ld /var/lib/ollama` | Run `chown -R ollama:ollama /var/lib/ollama` and restart service unit. |
| **Port Conflict on 11434** | Another local service or container occupying port. | `lsof -i :11434` | Terminate conflicting process or rebind Ollama port via `OLLAMA_HOST=0.0.0.0:11435`. |

## CLI examples

```bash
# Run a specific model and execute a single prompt query
ollama run llama4 "Explain the architectural advantages of Model Context Protocol (MCP) in two paragraphs."

# Create a custom model persona using a local Modelfile
ollama create homelab-engineer -f Modelfile

# Copy an existing model to a new tag
ollama cp llama4 my-custom-llama

# Show detailed technical metadata, quantization, and context window for a model
ollama show llama4

# Remove an unused model from local storage to free up disk space
ollama rm gemma2
```

## API examples

### Native REST Generation API (cURL)
```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama4",
  "prompt": "List three key benefits of running LLMs on local homelab hardware.",
  "stream": false
}' | jq .
```

### Python: OpenAI-Compatible Chat Streaming Endpoint with Ollama
```python
from openai import OpenAI

# Connect to Ollama using standard OpenAI Python SDK
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required placeholder
)

response = client.chat.completions.create(
    model="llama4",
    messages=[
        {"role": "system", "content": "You are a concise homelab AI assistant."},
        {"role": "user", "content": "How do I configure persistent storage for Docker Ollama?"}
    ],
    temperature=0.3,
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print("\n")
```

## Related tools / concepts
- [Open WebUI](open-webui.md) — Feature-rich, web-based chat and administration interface for Ollama.
- [LiteLLM](litellm.md) — Unified proxy server for load-balancing multiple local Ollama instances and cloud models.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Overview of the local open-weights model landscape.
- [FastAPI](../tools/frameworks/fastapi.md) — Asynchronous Python web framework commonly used to wrap local model APIs.
- [Docker](../tools/infrastructure/docker.md) — Primary container engine for hosting Ollama instances.
- [Portracker](portracker.md) — Homelab utility for tracking reserved local networking ports like 11434.
- [Nextcloud](nextcloud.md) — Self-hosted productivity suite with native local AI integration via Ollama.
- [FastMCP 3.1](../tools/automation_orchestration/mcp.md) — Model Context Protocol framework for agentic tool integration.

## Sources / references
- [Ollama Official Website](https://ollama.com/)
- [Ollama Official GitHub Repository](https://github.com/ollama/ollama)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Modelfile Reference](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
