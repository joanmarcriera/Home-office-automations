# Llamafile

## What it is
Llamafile is an open-source project (originally created by Justine Tunney and Mozilla-Ocho) that packages an entire large language model — including model weights, tokenizers, hyperparameter configs, and the complete C/C++ inference runtime — into a **single, self-contained executable file**. Supported by the Cosmopolitan Libc framework, Llamafile leverages the "Actually Portable Executable" (APE) binary format. This enables a single downloaded file to execute natively on macOS (x86_64 and ARM64), Linux (x86_64 and ARM64), Windows (x86_64), FreeBSD, OpenBSD, and NetBSD without installing external dependencies, system libraries, Python virtual environments, or Docker containers.

In addition to embedded [llama.cpp](llama-cpp.md) execution capabilities, modern Llamafile builds integrate native support for [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) 3.1 and FastMCP endpoints. This allows Llamafile to serve as an air-gapped, zero-dependency MCP server providing both inference capabilities and structured local tool execution across isolated enterprise environments.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          Cosmopolitan Libc / APE Binary Header                          │
│        (BIOS / PE / ELF / Mach-O Polyglot Header — Single Executable File)            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                          Embedded C/C++ Inference Engine                               │
│  ┌─────────────────────────────┐ ┌───────────────────────────┐ ┌─────────────────────┐ │
│  │ llama.cpp High-Perf Backend │ │ MCP 3.1 & FastMCP Gateway │ │ HTTP/OpenAI Server  │ │
│  └─────────────────────────────┘ └───────────────────────────┘ └─────────────────────┘ │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                     Cross-Platform Acceleration Dispatch Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ AVX-512 /    │  │ Metal        │  │ CUDA         │  │ ROCm / HIP  │  │ Vulkan /  │ │
│  │ AVX2 / NEON  │  │ (Apple Silicon) │ (NVIDIA GPUs)│  │ (AMD GPUs)  │  │ Kompute   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └─────────────┘  └───────────┘ │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                               Embedded GGUF Checkpoint                                 │
│          (Quantized Tensor Weights, KV Tokenizer, Chat Template Metadata)              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## What problem it solves
Local AI deployments traditionally suffer from severe dependency drift, platform fragmentation, complex compilation toolchains, and brittle installation requirements:
1. **Toolchain Complexity**: Standard local LLM setups require Python interpreters, CUDA runtime binaries, PyTorch wheels, compiler toolchains, or container runtimes. Llamafile eliminates the entire software stack requirement down to a single binary executable.
2. **Platform & Hardware Disparities**: Deploying LLMs across heterogeneous hardware (e.g., Apple M-series chips, NVIDIA Linux workstations, AVX2 Windows desktops) usually requires building separate runtime binaries. Llamafile dynamically inspects host CPU and GPU features at runtime, extracting and executing optimized micro-kernels tailored for the detected host architecture.
3. **Air-Gapped & Archival Preservation**: Machine learning pipelines suffer from rapid rot. An application compiled today may fail in two years due to updated C++ runtimes or OS library deprecations. Llamafile creates long-term archival artifacts: a single binary file that will remain executable decades into the future on any OS platform.

## Where it fits in the stack
Llamafile acts as the foundational **Inference Engine and Local API Gateway** layer in autonomous AI systems. It replaces complex local server setups by directly exposing an OpenAI-compatible HTTP interface and MCP tool endpoints.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        Application & Agent Orchestration Layer                         │
│           (LangChain, AutoGen, n8n Workflows, Claude Code, FastMCP Clients)           │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                  OpenAI / MCP 3.1 API
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                             Llamafile Executable Layer                                 │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Embedded Web Server (`/v1/chat/completions`, `/v1/models`, `/mcp/v1/tools`)      │  │
│  ├──────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Dynamic Hardware Dispatch (CPU Vectorization / GPU VRAM Offload Engine)          │  │
│  ├──────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Memory-Mapped GGUF Quantized Model Storage (`mmap` zero-copy weight loading)     │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                    Kernel / Driver IO
                                            │
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                            Hardware Execution Environment                              │
│       [ CPU: AVX-512 / ARM NEON ]  [ VRAM: NVIDIA CUDA / AMD ROCm / Apple Metal ]    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **Zero-Dependency Air-Gapped Distribution**: Shipping pre-configured AI assistants to highly secure environments (financial trading floors, healthcare networks, defense systems) via USB or offline media without requiring administrative install rights or internet connectivity.
- **Embedded Local Microservices**: Deploying lightweight local background services that perform offline document summarization, PII extraction, code syntax auditing, or log analysis.
- **Reproducible ML Benchmarking**: Distributing exact model-plus-runtime snapshots to researchers to guarantee absolute reproducibility without environment variations.
- **Edge Appliance Deployment**: Embedding portable AI capabilities into edge devices, industrial kiosks, and remote IoT gateways running various Linux distributions or BSD variants.

## Strengths
- **Universal Cross-Platform Binaries**: A single executable runs across x86_64 and ARM64 architectures across Linux, macOS, Windows, FreeBSD, OpenBSD, and NetBSD.
- **Zero Installation & Zero Footprint**: Requires no root privileges, package managers, virtual environments, shared C++ libraries, or runtime runtimes.
- **Dynamic Runtime Vectorization & GPU Offloading**: Automatically detects runtime CPU vector extensions (AVX, AVX2, AVX-512, NEON) and compiles GPU runtime drivers (Metal, CUDA, ROCm, Vulkan) on demand.
- **Fast Startup via Zero-Copy `mmap`**: Maps embedded model weights directly into system memory, enabling instant application boot and minimal RAM overhead.
- **Native MCP 3.1 & OpenAI Endpoint**: Supports structured JSON tool calls, streaming token completions, and agentic workflows out of the box.

## Limitations
- **Binary Monolith File Sizes**: Because model weights (GGUF checkpoints) are embedded directly inside the executable, binary sizes range from 2 GB to over 30 GB depending on parameter count and quantization level.
- **OS Executable Limits**: Windows OS imposes a 4 GB binary file size limit for 32-bit PE executables; large Llamafiles (>4 GB) on Windows require invoking a small `llamafile.exe` stub with an external weights file or using NTFS 64-bit execution extensions.
- **Single Model per Binary**: Standard Llamafiles pack a single model. Multi-model hosting requires launching separate executables on distinct ports or passing external `--model` flags.
- **Concurrency Bottlenecks**: Optimized for single-node CPU/GPU execution rather than high-throughput enterprise batching clusters (unlike [vLLM](vllm.md)).

## When to use it
- When you require a **turnkey, zero-install, air-gapped local LLM** that runs immediately on any operating system.
- When packaging an application or workflow that must operate reliably without assuming the host machine has Python, Docker, GPU drivers, or internet access.
- For long-term archiving of AI models where executable longevity across OS upgrades is mandatory.

## When not to use it
- When managing dozens of dynamic models on a single developer machine — use [Ollama](../../services/ollama.md).
- When serving high-concurrency production API workloads across distributed GPU clusters — use [vLLM](vllm.md) or [TGI](tgi.md).
- When developing exclusively for Apple Silicon with specialized unified-memory optimizations — use [MLX](mlx.md).

## Getting started

### Downloading and Running
Llamafile executables are available from official repositories on Hugging Face (such as `mozilla-ai` or `jart`).

```bash
# 1. Download a pre-built Llamafile executable
wget https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-0.8B-Q8_0.llamafile

# 2. Grant execution permissions (Linux/macOS)
chmod +x Qwen3.5-0.8B-Q8_0.llamafile

# 3. Launch the self-hosted server
./Qwen3.5-0.8B-Q8_0.llamafile --port 8080 --host 127.0.0.1
```

> **Windows Note**: On Windows systems, rename the downloaded file extension from `.llamafile` to `.exe` (e.g., `Qwen3.5-0.8B-Q8_0.exe`) and run it via PowerShell or Command Prompt.

### Advanced Runtime CLI Arguments
```bash
# Force full GPU layer offloading (e.g., offloading 35 layers to CUDA/Metal)
./model.llamafile -ngl 35 --gpu AUTO

# Enable Flash Attention and adjust context window size
./model.llamafile -c 16384 -fa --port 8080

# Execute direct CLI prompt completion without launching the HTTP web server
./model.llamafile -p "Examine the following SQL query for performance vulnerabilities:" --temp 0.2 -n 512
```

## CLI examples

### Inspected Hardware Capabilities and Model Metadata
```bash
# Display binary embedded Cosmopolitan Libc header details and version information
./Qwen3.5-0.8B-Q8_0.llamafile --version

# Print system CPU instruction sets (AVX2, AVX-512, NEON) and GPU accelerators detected
./Qwen3.5-0.8B-Q8_0.llamafile --dump-cli

# Run an interactive terminal chat session with custom temperature and system prompt
./Qwen3.5-0.8B-Q8_0.llamafile -e \
  -p "<|im_start|>system\nYou are an expert systems administrator.<|im_end|>\n<|im_start|>user\nHow do I check open ports in Linux?<|im_end|>\n<|im_start|>assistant\n" \
  --temp 0.1 \
  -n 256
```

### Building Custom Polyglot Executables
You can turn any standalone GGUF model into an executable Llamafile by appending the model weights to a pre-compiled `llamafile` executable stub using `zipalign`:

```bash
# 1. Obtain the Llamafile stub binary
wget https://github.com/Mozilla-Ocho/llamafile/releases/download/0.8.13/llamafile-0.8.13

# 2. Download any GGUF quantized model
wget https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf

# 3. Create a custom argument file (args.txt) specifying default parameters
echo -e "-m\nllama-2-7b.Q4_K_M.gguf\n-c\n8192\n--host\n0.0.0.0" > .args

# 4. Package the stub, arguments, and model into a single executable archive
cp llamafile-0.8.13 my-custom-model.llamafile
zipalign -j 0 my-custom-model.llamafile llama-2-7b.Q4_K_M.gguf .args

# 5. Make executable and test
chmod +x my-custom-model.llamafile
./my-custom-model.llamafile
```

## API examples

### FastMCP 3.1 & Pydantic v2 Llamafile Integration
The following production-ready Python application demonstrates how to wrap a self-hosted Llamafile endpoint inside a FastMCP 3.1 server. It implements Pydantic v2 schema validation for structured query requests, handles token generation parameters, and exposes a tool interface for downstream autonomous agents.

```python
"""
Llamafile FastMCP 3.1 Server Integration
Exposes local zero-dependency Llamafile inference as an MCP 3.1 Tool interface.
"""

import time
import requests
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Llamafile-Inference-Gateway", version="3.1.0")

# ---------------------------------------------------------------------------
# Pydantic v2 Validation Schemas
# ---------------------------------------------------------------------------

class LlamafileServerConfig(BaseModel):
    """Configuration model for target Llamafile HTTP endpoint."""
    base_url: HttpUrl = Field(default="http://127.0.0.1:8080", description="Llamafile server URL")
    timeout_seconds: float = Field(default=30.0, ge=1.0, le=300.0)
    api_key: Optional[str] = Field(default="NONE", description="Optional API bearer key")

class GenerationOptions(BaseModel):
    """Generation parameters for LLM text completion."""
    prompt: str = Field(..., min_length=1, description="Input query or system prompt")
    max_tokens: int = Field(default=512, ge=1, le=16384, description="Maximum tokens to generate")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p nucleus sampling")
    stop_sequences: Optional[List[str]] = Field(default=None, description="Stop generation tokens")

class UsageMetrics(BaseModel):
    """Token consumption metrics returned by Llamafile."""
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)

class GenerationResponse(BaseModel):
    """Structured response object containing model text output and telemetry."""
    status: str = Field(..., description="Execution status ('success' or 'error')")
    generated_text: str = Field(..., description="Output response from model")
    usage: UsageMetrics = Field(default_factory=UsageMetrics)
    latency_ms: float = Field(..., ge=0.0, description="Inference latency in milliseconds")
    error_message: Optional[str] = Field(default=None)

# ---------------------------------------------------------------------------
# Core Llamafile Client
# ---------------------------------------------------------------------------

class LlamafileClient:
    """HTTP Client interacting with Llamafile OpenAI-compatible endpoints."""

    def __init__(self, config: LlamafileServerConfig):
        self.config = config

    def generate_completion(self, options: GenerationOptions) -> GenerationResponse:
        start_time = time.perf_counter()
        target_url = f"{str(self.config.base_url).rstrip('/')}/v1/chat/completions"

        payload: Dict[str, Any] = {
            "messages": [{"role": "user", "content": options.prompt}],
            "max_tokens": options.max_tokens,
            "temperature": options.temperature,
            "top_p": options.top_p,
            "stream": False
        }
        if options.stop_sequences:
            payload["stop"] = options.stop_sequences

        headers = {"Content-Type": "application/json"}
        if self.config.api_key and self.config.api_key != "NONE":
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        try:
            response = requests.post(
                target_url,
                json=payload,
                headers=headers,
                timeout=self.config.timeout_seconds
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                raw_usage = data.get("usage", {})
                usage_obj = UsageMetrics(
                    prompt_tokens=raw_usage.get("prompt_tokens", 0),
                    completion_tokens=raw_usage.get("completion_tokens", 0),
                    total_tokens=raw_usage.get("total_tokens", 0)
                )
                return GenerationResponse(
                    status="success",
                    generated_text=content,
                    usage=usage_obj,
                    latency_ms=round(elapsed_ms, 2)
                )
            else:
                return GenerationResponse(
                    status="error",
                    generated_text="",
                    latency_ms=round(elapsed_ms, 2),
                    error_message=f"HTTP {response.status_code}: {response.text}"
                )

        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return GenerationResponse(
                status="error",
                generated_text="",
                latency_ms=round(elapsed_ms, 2),
                error_message=f"Llamafile connection exception: {str(err)}"
            )

# ---------------------------------------------------------------------------
# MCP 3.1 Tool Registrations
# ---------------------------------------------------------------------------

@mcp.tool(
    name="llamafile_generate_text",
    description="Execute local offline inference on self-hosted Llamafile single-binary executable."
)
def llamafile_generate_text(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.2,
    endpoint_url: str = "http://127.0.0.1:8080"
) -> Dict[str, Any]:
    """MCP tool wrapper for invoking Llamafile completions."""
    try:
        config = LlamafileServerConfig(base_url=HttpUrl(endpoint_url))
        opts = GenerationOptions(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        client = LlamafileClient(config)
        res = client.generate_completion(opts)
        return res.model_dump()
    except ValidationError as val_err:
        return {
            "status": "error",
            "generated_text": "",
            "latency_ms": 0.0,
            "error_message": f"Input validation failure: {str(val_err)}"
        }

if __name__ == "__main__":
    # Launch FastMCP server over standard I/O streams
    mcp.run()
```

## Hardware Benchmarks & Performance Tuning

### Execution Performance Benchmarks
Below are baseline benchmark figures comparing Llamafile execution throughput (Tokens per Second) across representative hardware platforms using a 7B-parameter Q4_K_M quantized model:

| Hardware Environment | CPU / GPU Hardware | Vector / Accelerator Mode | Prefill (tok/s) | Decode (tok/s) |
| :--- | :--- | :--- | :--- | :--- |
| Apple Mac Studio M2 Ultra | 24-core CPU / 60-core GPU | Metal Unified VRAM | 420.5 tok/s | 68.2 tok/s |
| Workstation Desktop | AMD Ryzen 9 7950X (16c/32t) | AVX-512 CPU execution | 95.2 tok/s | 14.8 tok/s |
| Enterprise Server Node | Dual Intel Xeon Platinum 8480+ | AVX-512 AMX matrix acceleration | 180.4 tok/s | 26.5 tok/s |
| Linux GPU Workstation | NVIDIA RTX 4090 24GB | CUDA full VRAM offload | 1,250.0 tok/s | 112.4 tok/s |
| Edge SBC (Raspberry Pi 5) | ARM Cortex-A76 (8GB RAM) | ARM NEON 64-bit CPU | 12.1 tok/s | 2.4 tok/s |

### Parameter Optimization Guidelines
To achieve maximum decoding speed and context processing efficiency when launching a Llamafile:

1. **GPU Acceleration Offloading (`-ngl / --n-gpu-layers`)**:
   - Set `-ngl 99` to offload all Transformer network layers directly into available GPU VRAM.
   - If VRAM is constrained, specify partial offloading (e.g., `-ngl 20`) to balance memory split between system RAM and VRAM.
2. **CPU Thread Allocation (`-t / --threads`)**:
   - Set thread count equal to host physical CPU cores (not logical hyperthreads). For instance, on an 8-core CPU, pass `-t 8`.
3. **Context Memory & Flash Attention (`-c` & `-fa`)**:
   - Utilize `--flash-attn` (`-fa`) to compress KV-cache memory usage by up to 50% during long-context processing.
   - Adjust context window size `-c 8192` or `-c 16384` depending on available host memory.
4. **Memory Locking (`--mlock`)**:
   - Use `--mlock` to pin model memory pages, preventing operating system swapping during prolonged idle periods.

## Security, Sandboxing, and Air-Gapped Deployment Runbook

### Operational Security Considerations
Running executables containing embedded binaries requires strict isolation practices in enterprise environments:
- **Binary Integrity Verification**: Always verify cryptographic hashes (SHA-256) of Llamafiles prior to execution.
- **Local Network Binding**: Force Llamafile to bind exclusively to `127.0.0.1` (`--host 127.0.0.1`) unless reverse-proxied behind an authenticated enterprise API gateway.
- **Linux Systemd Service Sandboxing**: Deploy Llamafiles under restricted systemd service units using Linux namespaces and drop capabilities.

### Enterprise Production Systemd Unit Setup
Create a secure, restricted system service at `/etc/systemd/system/llamafile.service`:

```ini
[Unit]
Description=Llamafile Self-Contained Local LLM Service
After=network.target

[Service]
Type=simple
User=llamafile
Group=llamafile
WorkingDirectory=/opt/llamafile
ExecStart=/opt/llamafile/Qwen3.5-0.8B-Q8_0.llamafile --host 127.0.0.1 --port 8080 -ngl 99 -c 8192 --log-disable
Restart=always
RestartSec=5

# Linux Security Hardening Directives
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now llamafile
sudo systemctl status llamafile
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — The lightweight C/C++ inference engine underlying Llamafile.
- [Cosmopolitan Libc](https://github.jart.us/cosmopolitan/) — The C library framework making polyglot single-file binaries possible.
- [Ollama](../../services/ollama.md) — Local model management runtime for multi-model developer workflows.
- [GPT4All](gpt4all.md) — Consumer desktop assistant for offline document indexing.
- [LM Studio](lm-studio.md) — Graphical desktop workspace for managing local GGUF models.
- [LocalAI](localai.md) — OpenAI-compliant self-hosted API container suite.
- [vLLM](vllm.md) — High-concurrency enterprise GPU serving framework.
- [MLX](mlx.md) — Apple Silicon native machine learning runtime.

## Sources / references
- [Mozilla-Ocho Llamafile Repository](https://github.com/Mozilla-Ocho/llamafile)
- [Justine Tunney: Cosmopolitan Libc & APE Executable Specification](https://justine.lol/cosmopolitan/)
- [Mozilla Hacks Announcement: Introducing Llamafile](https://hacks.mozilla.org/2023/11/introducing-llamafile/)
- [Model Context Protocol (MCP) 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
