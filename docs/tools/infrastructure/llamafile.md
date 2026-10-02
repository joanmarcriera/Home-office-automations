# Llamafile

## What it is
Llamafile is an open-source project (originally created by Mozilla Ocho and led by Justine Tunney) that packages an entire Large Language Model — combining the GGUF model weights, tokenizer, and the C/C++ inference runtime engine — into a **single, portable, executable binary file** that runs natively across macOS (ARM64 and x86_64), Linux, Windows, FreeBSD, NetBSD, and OpenBSD without requiring container isolation, virtual environments, or package installations.

By combining [llama.cpp](llama-cpp.md) with the **Cosmopolitan Libc** "Actually Portable Executable" (APE) loader format, Llamafile turns complex LLM deployments into single-file artifacts. When executed on any x86_64 or ARM64 host, the APE header dynamically detects the operating system kernel and CPU/GPU instructions, self-extracts runtime shims into memory, and launches an embedded high-performance HTTP server offering an OpenAI-compatible REST endpoint alongside native [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) 3.1 tool execution capability. As of early 2027, Llamafile serves as a primary standard for offline model archiving, edge device AI deployment, and deterministic air-gapped agent runtime execution.

## What problem it solves
Deploying open-weight LLMs traditionally suffers from severe environment drift, complex dependency chains (Python versions, PyTorch binaries, CUDA toolkit mismatches, C++ compiler flags), and fragile runtime environments. Llamafile resolves these core operational challenges:

1. **Eliminates Environment Drift & Dependency Hell:** Traditional local setups require managing Python virtual environments, PyTorch wheel dependencies, CUDA drivers, and dynamic libraries (`.so`, `.dylib`, `.dll`). Llamafile bundles all C++ runtime dependencies statically into the binary, ensuring that a file downloaded today will execute identically years later on entirely different operating systems.
2. **Enables True Air-Gapped Zero-Install Distribution:** For field deployment, industrial controls, defense applications, or remote research environments, Llamafile collapses the entire inferencing stack into a single file. Handing a field engineer a USB flash drive containing a 4GB `.llamafile` provides an operational local chat, embeddings, and tool-execution server with zero installation prerequisites.
3. **Cross-Platform Multi-OS Binary Compatibility:** Operators no longer need to maintain separate build artifacts or Docker containers for macOS, Windows, and Linux. A single `.llamafile` binary uses Cosmopolitan Libc headers to execute natively on all major operating systems.
4. **Simplifies Local Agent Tool Integration:** Built-in FastMCP 3.1 and MCP HTTP/SSE transport protocols allow Llamafile to serve both as a raw token-generation engine and as a self-contained autonomous agent tool executor in air-gapped network segments.

## Where it fits in the stack
**Infrastructure / Self-Contained Edge Inference & Archival Runtime.** Llamafile sits at the bottom of the execution stack as an autonomous local inference layer. It exposes an OpenAI-compatible `/v1/chat/completions` REST interface, an `/v1/embeddings` endpoint, and native MCP 3.1 JSON-RPC tool endpoints. Higher-level automation engines like [n8n](../../services/n8n.md), agent frameworks like [smolagents](../frameworks/smolagents.md), or desktop frontends like [Open WebUI](../../services/open-webui.md) connect to Llamafile as if it were a cloud API endpoint.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                Llamafile Binary (.llamafile)                            │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    APE Header (Actually Portable Executable Format)              │  │
│  │     Detects OS Kernel (Linux ELF / macOS Mach-O / Windows PE / BSD ELF)           │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Cosmopolitan Libc System Call Translation Layer                │  │
│  │     Converts C POSIX primitives to Windows Win32 API or Linux/Mach-O Syscalls     │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Embedded Llama.cpp Engine & Compute Acceleration               │  │
│  │     AVX2 / AVX-512 / ARM Neon / CUDA Kernels / Metal Shaders / ROCm HIP          │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Embedded MCP 3.1 & OpenAI REST HTTP / SSE Server              │  │
│  │     /v1/chat/completions  |  /v1/embeddings  |  /mcp/v1/tools/execute             │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Embedded Model Weights & Tokenizer (GGUF V3 Format)            │  │
│  │     Stored as uncompressed Zip archive appended directly to executable binary     │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               Target Hardware Platform                                  │
│  ┌───────────────────────┐ ┌───────────────────────┐ ┌────────────────────────────────┐  │
│  │ Apple Silicon M1-M4   │ │ NVIDIA CUDA GPU Core  │ │ AMD ROCm GPU / x86_64 CPU     │  │
│  │ (Metal API Shaders)   │ │ (NVCC FP16/INT8 PTX)  │ │ (AVX-512 Matrix Vector Ops)   │  │
│  └───────────────────────┘ └───────────────────────┘ └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **Air-Gapped Field Operations:** Distributing deterministic, pre-configured AI assistants to offshore vessels, defense hardware, or remote facilities lacking internet connectivity.
- **Long-Term Model Preservation & Archival:** Storing snapshot models in enterprise digital preservation systems where external Python libraries or runtime containers will break over 5 to 10 year horizons.
- **Embedded Hardware & Kiosk Systems:** Shipping single-file AI capability inside point-of-sale hardware, industrial edge gateways, or local medical diagnostic devices.
- **Rapid Local AI Experimentation:** Instant local LLM evaluation without docker daemons, Python virtual environments, or complex setup steps (`curl -LO ... && chmod +x ... && ./model.llamafile`).
- **Offline MCP Tool Execution:** Running local code generation and document analysis pipelines where tool calling is bound directly to an offline Llamafile instance.

## Strengths
- **Single-File Zero-Dependency Executable:** No runtime dependencies, Python interpreters, dynamic linking libraries, or container engines required.
- **Cross-Platform Compatibility:** Runs natively across macOS, Linux, Windows, FreeBSD, NetBSD, and OpenBSD using a single compiled APE binary.
- **High Performance Acceleration:** Leverages llama.cpp vector math with runtime auto-detection for AVX2, AVX-512, ARM Neon, Apple Metal GPU, NVIDIA CUDA, and AMD ROCm GPU backends.
- **Native Standards Compliance:** Provides OpenAI REST API endpoints (`/v1/chat/completions`, `/v1/embeddings`) alongside FastMCP 3.1 JSON-RPC protocol interfaces.
- **Permissive Open-Source Licensing:** Apache 2.0 licensing for the Llamafile framework allows unencumbered commercial redistribution and embedding into proprietary hardware or software packages.

## Limitations
- **Monolithic File Sizes:** Because model weights (GGUF) are embedded directly inside the binary executable, single-file downloads typically range from 2 GB to over 30 GB.
- **Operating System File Size Limits:** Certain legacy file systems (e.g., FAT32's 4 GB limit) or Windows command-line execution caps require special extraction flags (`--extract-gguf`) or 64-bit NTFS drives.
- **Multi-Model Management Overhead:** Unlike [Ollama](../../services/ollama.md), which maintains a centralized model registry and background service manager, Llamafile operates as an isolated executable per model checkpoint.
- **Multi-Tenant Serving Throughput Limits:** Optimized primarily for low-concurrency edge, single-user, or small-team serving; high-throughput enterprise token serving is better suited for [vLLM](vllm.md).

## When to use it
- When you require a **zero-install, standalone offline executable** that runs on heterogeneous operating systems without setup scripts.
- For long-term software archiving, hardware kiosk distribution, or air-gapped field deployments.
- When building lightweight edge applications where bundling the model and runtime into one single installer simplifies user onboarding.

## When not to use it
- When you frequently swap between dozens of fine-tuned models on a single developer workstation — use [Ollama](../../services/ollama.md).
- When building centralized, multi-tenant enterprise inference clusters requiring tensor parallel distribution across multi-node GPU clusters — use [vLLM](vllm.md) or [ExLlamaV2](exllamav2.md).
- For strict Apple-silicon-only high-concurrency memory-bandwidth workflows — use [MLX](mlx.md).

## Getting started

### Installation & Execution
Llamafile requires no formal installation step. You download an APE binary from Hugging Face or compile custom weights into an APE executable.

### Hello World CLI Example
```bash
# 1. Download a pre-compiled Llamafile (e.g., Qwen 3.5 0.8B Q8_0)
curl -LO https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-0.8B-Q8_0.llamafile

# 2. Grant executable permissions (macOS / Linux)
chmod +x Qwen3.5-0.8B-Q8_0.llamafile

# 3. Launch the native server (opens local web UI & starts REST server at http://127.0.0.1:8080)
./Qwen3.5-0.8B-Q8_0.llamafile

# Note for Windows users:
# Rename the file extension to .exe before running in PowerShell or Command Prompt:
# ren Qwen3.5-0.8B-Q8_0.llamafile Qwen3.5-0.8B-Q8_0.exe
# .\Qwen3.5-0.8B-Q8_0.exe
```

### Packaging Custom GGUF Model Weights into Llamafile
You can convert any custom GGUF model into a standalone Llamafile binary using the `llamafile-convert` utility or zip appending:

```bash
# Obtain the base llamafile runtime executable
curl -LO https://github.com/Mozilla-Ocho/llamafile/releases/download/0.8.16/llamafile-0.8.16

# Prepare your GGUF model file and a custom system prompt file (args.txt)
cat << 'EOF' > args.txt
-m
custom-model-q4_k_m.gguf
-c
8192
--host
0.0.0.0
--port
8080
EOF

# Package runtime, args, and GGUF model into an APE binary using uncompressed zip storage
cp llamafile-0.8.16 my-custom-model.llamafile
zip -0 my-custom-model.llamafile custom-model-q4_k_m.gguf args.txt
chmod +x my-custom-model.llamafile

# Run the newly generated custom Llamafile
./my-custom-model.llamafile
```

## CLI examples

### Server Operations with GPU Offloading
```bash
# Start server offloading all layers to an NVIDIA CUDA or Apple Metal GPU
./Qwen3.5-0.8B-Q8_0.llamafile --n-gpu-layers 99 --host 0.0.0.0 --port 9000

# Limit context window length to 16,384 tokens and specify CPU threads
./Qwen3.5-0.8B-Q8_0.llamafile -c 16384 -t 12 --nobrowser

# Extract embedded GGUF weights to disk for inspection or use in llama.cpp
./Qwen3.5-0.8B-Q8_0.llamafile --extract-gguf
```

### Direct CLI Prompt Generation
```bash
# Perform one-shot text completion directly in terminal without starting server
./Qwen3.5-0.8B-Q8_0.llamafile \
  --prompt "<|im_start|>system\nYou are a senior DevOps engineer.<|im_end|>\n<|im_start|>user\nWrite a Bash script to monitor disk usage and alert via webhook.<|im_end|>\n<|im_start|>assistant\n" \
  -n 512 \
  --temp 0.2 \
  --silent-prompt
```

### MCP 3.1 Tool Execution Mode
```bash
# Launch Llamafile in native MCP 3.1 server mode over stdin/stdout transport
./Qwen3.5-0.8B-Q8_0.llamafile --mcp --mcp-transport stdio --mcp-tools-dir ./local_tools/
```

## API examples

### FastMCP 3.1 Llamafile Tool Orchestrator Server
Below is a complete FastMCP 3.1 Python server implementation that manages local Llamafile server instances, executes token inference queries, and performs automated system resource validation using strict **Pydantic v2** models.

```python
import os
import subprocess
import time
import requests
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 server instance
mcp = FastMCP("Llamafile-Infrastructure-Manager")

# ============================================================================
# Pydantic v2 Models for API Schemas & Configuration
# ============================================================================

class LlamafileLaunchConfig(BaseModel):
    binary_path: str = Field(..., description="Absolute path to the .llamafile executable")
    host: str = Field(default="127.0.0.1", description="Binding network interface host")
    port: int = Field(default=8080, ge=1024, le=65535, description="HTTP server listening port")
    gpu_layers: int = Field(default=99, ge=0, description="Number of model layers to offload to GPU")
    context_size: int = Field(default=8192, ge=512, le=131072, description="Maximum context window size")
    threads: int = Field(default=8, ge=1, description="Number of CPU processing threads")

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant|tool)$")
    content: str = Field(..., min_length=1)

class ChatCompletionRequest(BaseModel):
    model: str = Field(default="local-llamafile", description="Target model identifier")
    messages: List[ChatMessage] = Field(..., min_items=1)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1)
    stream: bool = Field(default=False)

class ChatUsage(BaseModel):
    prompt_tokens: int = Field(default=0)
    completion_tokens: int = Field(default=0)
    total_tokens: int = Field(default=0)

class ChatChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = Field(default="stop")

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = Field(default="chat.completion")
    created: int
    model: str
    choices: List[ChatChoice]
    usage: ChatUsage

class LlamafileHealthStatus(BaseModel):
    status: str = Field(..., description="Connection status: healthy, degraded, or unreachable")
    endpoint: HttpUrl
    loaded_model: Optional[str] = None
    response_time_ms: float = Field(default=0.0)

# Global process tracking registry
ACTIVE_PROCESSES: Dict[int, subprocess.Popen] = {}

# ============================================================================
# FastMCP 3.1 Tools Definition
# ============================================================================

@mcp.tool(
    name="llamafile_health_check",
    description="Validates the operational health and connectivity of a local Llamafile instance."
)
def check_llamafile_health(server_url: str = "http://127.0.0.1:8080") -> str:
    start_time = time.time()
    endpoint = f"{server_url.rstrip('/')}/v1/models"
    try:
        response = requests.get(endpoint, timeout=5)
        latency = (time.time() - start_time) * 1000.0
        if response.status_code == 200:
            data = response.json()
            models = data.get("data", [])
            model_id = models[0].get("id") if models else "unknown"
            status = LlamafileHealthStatus(
                status="healthy",
                endpoint=server_url, # type: ignore
                loaded_model=model_id,
                response_time_ms=round(latency, 2)
            )
            return status.model_dump_json(indent=2)
    except Exception as err:
        return LlamafileHealthStatus(
            status="unreachable",
            endpoint=server_url, # type: ignore
            response_time_ms=0.0
        ).model_dump_json(indent=2)

    return f"Error: Received HTTP status {response.status_code}"

@mcp.tool(
    name="llamafile_generate_chat",
    description="Sends an OpenAI-compatible chat completion request to a running Llamafile instance."
)
def generate_chat_completion(
    prompt: str,
    system_prompt: str = "You are a helpful local technical assistant.",
    server_url: str = "http://127.0.0.1:8080",
    temperature: float = 0.2,
    max_tokens: int = 512
) -> str:
    payload = ChatCompletionRequest(
        messages=[
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=prompt)
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    endpoint = f"{server_url.rstrip('/')}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, json=payload.model_dump(), headers=headers, timeout=60)
        if response.status_code == 200:
            parsed = ChatCompletionResponse.model_validate(response.json())
            return parsed.choices[0].message.content
        else:
            return f"Llamafile API Error ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Execution Failure: {str(e)}"

@mcp.tool(
    name="llamafile_launch_instance",
    description="Launches a new Llamafile executable process in the background with configured parameters."
)
def launch_llamafile_instance(
    binary_path: str,
    port: int = 8080,
    gpu_layers: int = 99,
    threads: int = 8
) -> str:
    if not os.path.exists(binary_path):
        return f"Error: Binary path '{binary_path}' does not exist on disk."

    config = LlamafileLaunchConfig(
        binary_path=binary_path,
        port=port,
        gpu_layers=gpu_layers,
        threads=threads
    )

    cmd = [
        config.binary_path,
        "--host", config.host,
        "--port", str(config.port),
        "--n-gpu-layers", str(config.gpu_layers),
        "--threads", str(config.threads),
        "--nobrowser"
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        ACTIVE_PROCESSES[config.port] = proc
        time.sleep(2) # Brief delay to allow initial server socket binding

        if proc.poll() is not None:
            stderr = proc.stderr.read() if proc.stderr else ""
            return f"Failed to start Llamafile. Exit code: {proc.returncode}. Error: {stderr}"

        return f"Successfully launched Llamafile binary PID {proc.pid} on port {config.port}."
    except Exception as ex:
        return f"Launch Exception: {str(ex)}"

if __name__ == "__main__":
    mcp.run()
```

## Hardware Acceleration & Performance Benchmark Matrix
Llamafile includes built-in compute backends that auto-detect hardware capabilities at launch. The matrix below illustrates typical decoding performance across hardware architectures using Qwen 3.5 8B Q4_K_M weights.

| Hardware Architecture | Compute Backend | Layer Offload | Context Window | Prompt Eval (tok/s) | Generation (tok/s) | Power Draw (W) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Apple M4 Max (64GB Unified)** | Metal GPU API | 100% (33/33) | 32,768 tok | 480 tok/s | 68.5 tok/s | 38 W |
| **NVIDIA RTX 4090 (24GB VRAM)** | CUDA 12.x PTX | 100% (33/33) | 32,768 tok | 1,250 tok/s | 112.0 tok/s | 280 W |
| **AMD Ryzen 9 7950X (x86_64)** | AVX-512 Vector | 0% (CPU Only) | 8,192 tok | 85 tok/s | 14.2 tok/s | 125 W |
| **Intel Core i7-13700K (x86_64)**| AVX2 Matrix | 0% (CPU Only) | 8,192 tok | 62 tok/s | 10.8 tok/s | 95 W |
| **Raspberry Pi 5 (8GB ARM64)** | ARM Neon FP16 | 0% (CPU Only) | 2,048 tok | 18 tok/s | 3.2 tok/s | 12 W |

## Operational & Air-Gapped Deployment Runbook

### Scenario: Deploying an Air-Gapped Llamafile Assistant to an Industrial Gateway
1. **Prepare Distribution Media:**
   - Download the target `.llamafile` executable on an internet-connected staging machine.
   - Verify sha256 checksum against official repository manifests:
     ```bash
     sha256sum Qwen3.5-0.8B-Q8_0.llamafile > checksum.txt
     ```
   - Copy the binary and checksum file to write-once USB media or local network share.

2. **Target Node Provisioning:**
   - Mount USB storage on target air-gapped node (e.g., Ubuntu 24.04 LTS or Windows Server 2025).
   - Validate checksum on target node:
     ```bash
     sha256sum -c checksum.txt
     ```

3. **Configure Systemd Background Service (Linux Edge Nodes):**
   Create `/etc/systemd/system/llamafile.service`:
   ```ini
   [Unit]
   Description=Llamafile Air-Gapped Local LLM Server
   After=network.target

   [Service]
   Type=simple
   User=llamafile
   Group=llamafile
   WorkingDirectory=/opt/llamafile
   ExecStart=/opt/llamafile/Qwen3.5-0.8B-Q8_0.llamafile --host 0.0.0.0 --port 8080 --n-gpu-layers 99 --nobrowser
   Restart=always
   RestartSec=5
   LimitNOFILE=65536

   [Install]
   WantedBy=multi-user.target
   ```

4. **Service Activation & Verification:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now llamafile
   sudo systemctl status llamafile
   curl http://127.0.0.1:8080/v1/models
   ```

5. **Troubleshooting Common Edge Errors:**
   - **Error: `WINA32 / Exec format error` on Linux:** Ensure the execute permission is granted (`chmod +x filename.llamafile`). If running inside WSL or older Linux kernels lacking binfmt_misc support, execute explicitly via `/bin/sh ./filename.llamafile`.
   - **Error: `mmap failed: Out of memory`:** The system lacks sufficient RAM/swap to map the embedded GGUF weights. Pass `--no-mmap` to force buffer allocation or add a swapfile.
   - **Error: CUDA driver mismatch:** Ensure `nvidia-smi` reports CUDA driver version 12.0 or higher. Pass `--disable-gpu` to force CPU AVX-512 fallback if CUDA libraries fail to load.

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — The core C++ inference engine embedded inside Llamafile.
- [Ollama](../../services/ollama.md) — Workstation model manager providing background daemon serving and multi-model CLI pulls.
- [GPT4All](gpt4all.md) — Desktop client providing offline RAG and local model execution.
- [LM Studio](lm-studio.md) — Graphical desktop environment for discovering and running local GGUF models.
- [vLLM](vllm.md) — High-throughput, tensor-parallel serving engine for enterprise GPU clusters.
- [MLX](mlx.md) — Apple Silicon native array framework for fine-tuning and running LLMs on Mac hardware.
- [Kiwix](../../services/kiwix.md) — Zero-install offline document reader used alongside Llamafile in air-gapped knowledge stacks.

## Sources / references
- [Llamafile Official GitHub Repository (Mozilla-Ocho)](https://github.com/Mozilla-Ocho/llamafile)
- [Cosmopolitan Libc Architecture & APE Specification](https://github.com/jart/cosmopolitan)
- [Mozilla Hacks: Introducing Llamafile](https://hacks.mozilla.org/2023/11/introducing-llamafile/)
- [Justine Tunney Blog: Actually Portable Executables](https://jart.org/m1)
- [Model Context Protocol (MCP) 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
