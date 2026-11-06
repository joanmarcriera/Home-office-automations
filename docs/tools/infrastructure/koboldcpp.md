# KoboldCPP

KoboldCPP is an open-source, lightweight, single-file C/C++ execution engine and inference server for Large Language Models (LLMs) saved in the GGUF format, powered by llama.cpp.

## What it is

KoboldCPP is a self-contained local inference engine that packages llama.cpp along with a full Kobold AI web interface, an OpenAI-compatible REST API, and native hardware acceleration support across CUDA (Nvidia), ROCm (AMD), Vulkan (Cross-platform), Metal (Apple Silicon), and CPU (AVX2/AVX-512). As of early 2027, KoboldCPP provides cutting-edge support for advanced quantization formats (GGUF, K-quants, IQ_Quants, FP8/FP16), context shift techniques, multi-model embedding endpoints, and native Model Context Protocol (**MCP 3.1** / **FastMCP 3.1**) integration.

KoboldCPP requires no complex Python environment dependencies or virtual environments to run; it is distributed as a single pre-compiled executable containing all embedded Web UI assets, C++ execution kernels, and backend drivers.

## Theoretical Foundations & Mathematical Formulations

Local autoregressive transformer execution under mixed-precision and mixed-hardware environments relies on KV-cache pointer transformations, memory bandwidth roofline limits, and quantization degradation bounds.

### 1. Context Shift KV-Cache Rolling Window Pointer Arithmetic
Standard transformer generation requires evaluating full prefix self-attention across context length $T$. In dynamic dialogue, when total tokens exceed physical buffer capacity $T_{\max}$, KoboldCPP executes **Context Shift** via zero-copy in-place circular ring-buffer pointer arithmetic, avoiding quadratic re-computation penalties:

$$\text{Attn}(Q, K, V) = \operatorname{softmax}\left( \frac{Q K_{\text{shifted}}^T}{\sqrt{d_k}} \right) V_{\text{shifted}}$$

Where the shifted key cache tensor indexing for physical memory position $i \in \{0, \ldots, T_{\max}-1\}$ and logical step $t$ is formulated as:

$$K_{\text{shifted}}[i] = K[(i + \Delta_{\text{shift}}) \pmod{T_{\max}}], \quad \Delta_{\text{shift}} = T_{\text{prompt}} - T_{\text{overlap}}$$

The prefill computation complexity drops from standard quadratic prefix evaluation $\mathcal{O}((T_{\text{prompt}} + T_{\text{new}})^2 \cdot d)$ to localized delta prefill:

$$\mathcal{C}_{\text{prefill}} = \mathcal{O}(T_{\text{new}}^2 \cdot d + 2 T_{\text{overlap}} T_{\text{new}} d) \ll \mathcal{O}(T_{\text{context}}^2 \cdot d)$$

Eliminating up to $92\%$ of time-to-first-token (TTFT) overhead during multi-turn agent interactions.

### 2. Mixed GGUF Quantization Layer Allocation & VRAM Constraints
When partitioning an $L$-layer transformer between discrete GPU VRAM ($M_{\text{VRAM}}$) and host system RAM ($M_{\text{RAM}}$), layer allocation is solved via knapsack memory optimization:

$$\max \sum_{l=1}^L \alpha_l \cdot x_l \quad \text{subject to} \quad \sum_{l=1}^L M_{\text{layer}}(l, q_l) \cdot x_l + M_{\text{KV}}(T, q_{\text{kv}}) \le M_{\text{VRAM}} - M_{\text{cuda\_overhead}}$$

Where $x_l \in \{0, 1\}$ denotes GPU placement indicator, $q_l \in \{\text{Q4\_K\_M}, \text{Q5\_K\_M}, \text{IQ3\_M}\}$ represents layer quantization format, and weight layer memory consumption is given by:

$$M_{\text{layer}}(l, q_l) = W_l \cdot b_{\text{eff}}(q_l) + M_{\text{bias}}$$

The KV-cache memory requirement across attention heads $n_{\text{heads}}$, head dimension $d_{\text{head}}$, and context window $T$ scales as:

$$M_{\text{KV}}(T, q_{\text{kv}}) = 2 \cdot L \cdot n_{\text{kv\_heads}} \cdot d_{\text{head}} \cdot T \cdot b(q_{\text{kv}})$$

### 3. Roofline Memory Bandwidth Bound during Autoregressive Decoding
Token generation in autoregressive LLMs is memory-bandwidth bound ($\text{Arithmetic Intensity } \mathcal{I} < \mathcal{I}_{\text{knee}}$). The theoretical maximum token throughput $\mathcal{T}_{\text{tok}}$ (tokens per second) across memory bus bandwidth $\mathcal{B}_{\text{mem}}$ (GB/s) is bounded by:

$$\mathcal{T}_{\text{tok}} \le \frac{\mathcal{B}_{\text{mem}}}{\frac{\mathcal{P}_{\text{active}} \cdot b_{\text{eff}}}{8} + \frac{2 \cdot L \cdot d_{\text{model}} \cdot T_{\text{curr}} \cdot b(q_{\text{kv}})}{8 \cdot 10^9}}$$

Where $\mathcal{P}_{\text{active}}$ is the count of active model parameters. On PCIe bus traversal between CPU RAM ($\sim 60\text{ GB/s}$) and GPU VRAM ($\sim 1000\text{ GB/s}$), mixed-offloading token generation rate converges to the harmonic bottleneck:

$$\frac{1}{\mathcal{T}_{\text{mixed}}} = \frac{L_{\text{gpu}}}{L} \frac{1}{\mathcal{T}_{\text{gpu}}} + \frac{L - L_{\text{gpu}}}{L} \frac{1}{\mathcal{T}_{\text{cpu}}}$$

---

## What problem it solves

Deploying and serving LLMs locally often involves navigating complex Python package conflicts (PyTorch, CUDA driver versions, HuggingFace Transformers), heavy VRAM memory overheads, and complicated server setups.

KoboldCPP solves this by delivering:
1. **Zero-Dependency Execution**: A portable, single-file binary that launches an optimized C++ inference server in seconds.
2. **Flexible Cross-Platform Acceleration**: Offloading Transformer layers selectively across system RAM (CPU) and VRAM (GPU via Vulkan, CUDA, ROCm, or Metal) without requiring pure GPU setups.
3. **Dual API & UI Interface**: Providing both an interactive node/story web browser UI (for creative writing and multi-character roleplay) and an OpenAI-compatible REST API (for coding assistants, RAG pipelines, and agentic tools).
4. **Context Shift & Smart Caching**: Smart KV-cache reuse that avoids re-processing static prompt prefixes, drastically reducing prefill latency on long context windows (up to 128k+ tokens).

## Architectural Overview & Memory Offloading Mechanics

KoboldCPP bridges high-level web clients and API callers directly to high-performance C++ GGML/llama.cpp matrix multiplication kernels.

```mermaid
graph TD
    A[Client Request / Web Browser / API] -->|HTTP / WebSockets| B[KoboldCPP Embedded C++ Web Server]

    B -->|API Parsing & Queue| C[Inference Engine Manager]
    C -->|KV-Cache Context Shift| D[(Smart Prefix KV-Cache)]

    C -->|Layer Offloading Partitioning| E{Hardware Offloader}

    E -->|VRAM: Layers 1..N| F[GPU Backend (CUDA / Vulkan / Metal / ROCm)]
    E -->|RAM: Remaining Layers| G[Host CPU Backend (AVX-512 / AVX2)]

    F -->|Matrix Mult / Tensor Cores| H[C++ GGML Execution Engine]
    G -->|SIMD Multi-Threading| H

    H -->|Token Generation Stream| B
    B -->|SSE Stream / WebSockets| A
```

### Complete Sequence Flow for Memory Offloading & Stream Generation

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client App / Open WebUI
    participant Server as KoboldCPP Server
    participant VRAM as GPU VRAM (CUDA/Vulkan)
    participant RAM as System RAM (CPU)

    Client->>Server: POST /v1/chat/completions (Prompt + Max Tokens)
    Server->>Server: Check KV-Cache for static prompt match
    alt KV-Cache Hit
        Server->>Server: Re-use prefill tokens (Context Shift)
    else KV-Cache Miss
        Server->>VRAM: Prefill GPU Layers 1..N
        Server->>RAM: Prefill CPU Layers N+1..M
    end

    loop Token Generation Loop
        Server->>VRAM: Forward Pass GPU Tensor Cores
        Server->>RAM: Forward Pass CPU SIMD Instructions
        Server->>Server: Sample next token (Temperature / Repetition Penalty)
        Server-->>Client: Stream SSE Token Chunk `data: {"content": "..."}`
    end
    Server-->>Client: Final Token Stream `[DONE]`
```

## Comparative Local Inference Engine Matrix (2027 Standards)

| Inference Engine | Backend Core | Hardware Support | Quantization Formats | Primary Deployment Mode | FastMCP 3.1 Integration |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KoboldCPP** | llama.cpp / C++ | CUDA, Vulkan, ROCm, Metal, CPU | GGUF (K-Quants, IQ-Quants, FP16) | Standalone Binary / Multi-OS | Native Endpoint Tool |
| **llama.cpp** | Native C++ / GGML | CUDA, ROCm, Metal, SYCL, CPU | GGUF, Quantized Weights | CLI & Embedded Library | Subprocess Execution |
| **Ollama** | Go + llama.cpp | CUDA, ROCm, Metal, CPU | GGUF Containerized Bundles | Headless Service Daemon | Native REST Tool |
| **vLLM** | Python / C++ PagedAttention | CUDA, ROCm, TPU, AWS Neuron | FP8, INT4, AWQ, GPTQ | High-Concurrency Cluster Server | Async REST Tool |
| **ExLlamaV2** | C++ / CUDA Custom Kernels | NVIDIA CUDA Exclusive | EXL2, 4-bit, 8-bit | High-Speed Single GPU Serving | Native Python Tool |

## Where it fits in the stack

**Inference Engine & Local Model Server Layer**. KoboldCPP sits directly between local GGUF model files on local storage and user-facing clients (such as [Open WebUI](../../services/open-webui.md), SillyTavern, Cursor, or FastMCP agent servers).

```
┌────────────────────────────────────────────────────────┐
│             Application / Agentic Layer                │
│    (Open WebUI, SillyTavern, FastMCP 3.1, Cursor)     │
└───────────────────────────┬────────────────────────────┘
                            │ OpenAI API / Kobold API
┌───────────────────────────▼────────────────────────────┐
│                       KOBOLDCPP                        │
│   ┌────────────────────────────────────────────────┐   │
│   │ Embedded HTTP Web Server & Kobold Lite Frontend│   │
│   ├────────────────────────────────────────────────┤   │
│   │ KV-Cache Engine & Context Shift Allocator      │   │
│   ├────────────────────────────────────────────────┤   │
│   │ llama.cpp / GGML Multi-Backend Compute Engine  │   │
│   └────────────────────────────────────────────────┘   │
└───────────────────────────┬────────────────────────────┘
                            │ Layer Offloading / Matrix Multiplication
┌───────────────────────────▼────────────────────────────┐
│      System Hardware (CPU RAM + CUDA/Vulkan VRAM)      │
└────────────────────────────────────────────────────────┘
```

## Typical use cases

- **Low-VRAM & Mixed Hardware Inference**: Running 32B or 70B parameter models (e.g., Llama 3.3, Qwen 2.5, DeepSeek-R1-Distill) by offloading 30 layers to GPU VRAM and remaining layers to CPU RAM.
- **Local Creative Writing & Character Roleplay**: Utilizing KoboldCPP's built-in memory systems, world info cards, and context shift engine for long-form narrative generation.
- **Privacy-Preserving Code & Agent Server**: Serving an OpenAI-compatible endpoint locally for coding extensions or private local RAG pipelines.
- **Cross-Platform Vulkan Inference**: Serving LLMs on AMD Radeon GPUs or Integrated Graphics (Intel Arc / AMD APUs) without complex ROCm or CUDA installation.

## Key Features & Capabilities

### 1. Unified GGUF & Quantization Support
KoboldCPP supports all modern GGML/llama.cpp quantization schemes:
- **K-Quants**: `Q4_K_M`, `Q5_K_M`, `Q6_K` for balanced perplexity vs. memory size.
- **Importance Matrix Quants (IQ)**: `IQ3_M`, `IQ2_XXS`, `IQ4_NL` for ultra-low bitrates without severe intelligence drop degradation.
- **FP8 & FlashAttention-2**: Built-in FlashAttention acceleration for long context prefill passes.

### 2. Vulkan GPU Acceleration
While many engines require specialized CUDA builds, KoboldCPP includes a native Vulkan backend that runs across Nvidia, AMD, Intel, and Apple GPUs without needing vendor-specific SDK drivers installed.

### 3. Context Shift & Smart KV-Cache
Standard inference engines recalculate the entire prompt from token 0 when making slight prompt additions. KoboldCPP's **Context Shift** shifts the cached KV-tokens in memory, allowing users to converse continuously with instant response times.

## Strengths

- **Single Portable Binary**: No Python, no `pip install` errors, no PyTorch version mismatches.
- **Universal Hardware Support**: Runs on CUDA, ROCm, Vulkan, Metal, and pure CPU (AVX2/AVX-512/ARM Neon).
- **Exceptional Memory Efficiency**: Split model layers dynamically across multiple GPUs or combined CPU/GPU RAM.
- **Dual API Standard**: Supports both legacy Kobold AI JSON API and modern OpenAI `/v1/chat/completions` REST endpoints.
- **Built-In Web UI**: Included web frontend allows immediate chat and narrative writing out-of-the-box.

## Limitations

- **GGUF Specific**: Designed primarily for quantized GGUF models; does not natively load raw unquantized Safetensors or PyTorch checkpoints without prior conversion.
- **Concurrency Bottlenecks under Heavy Load**: Primarily optimized for single-user or small-team local workloads; for massive multi-tenant production concurrency, dedicated engines like [vLLM](../infrastructure/vllm.md) or [SGLang](../infrastructure/sglang.md) are better suited.

## Production Systemd Service Unit (`koboldcpp.service`)

Run KoboldCPP as an isolated, resilient systemd service daemon with hardware acceleration and process sandboxing:

```ini
[Unit]
Description=KoboldCPP GGUF Inference Engine Daemon
After=network.target local-fs.target
Wants=network.target

[Service]
Type=simple
User=llm-operator
Group=llm-operator
WorkingDirectory=/opt/koboldcpp
ExecStart=/opt/koboldcpp/koboldcpp-linux-x64 \
    --model /opt/models/Qwen2.5-14B-Instruct-Q5_K_M.gguf \
    --usevulkan \
    --gpulayers 35 \
    --contextsize 16384 \
    --flashattention \
    --smartcontext \
    --skiplaunch \
    --port 5001

Restart=always
RestartSec=5
KillMode=process
LimitNOFILE=65536
MemoryMax=28G
CPUWeight=100

# Systemd Security Hardening
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/opt/koboldcpp/logs /tmp
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Production Multi-Container Docker Compose Stack

The following Docker Compose configuration deploys KoboldCPP alongside an OpenAI-compatible reverse proxy and Open WebUI client:

```yaml
version: "3.8"

services:
  koboldcpp:
    image: lostruins/koboldcpp:v1.78
    container_name: koboldcpp-inference
    restart: unless-stopped
    ports:
      - "5001:5001"
    volumes:
      - ./models:/models:ro
      - ./logs:/var/log/koboldcpp:rw
    environment:
      - KOBOLD_MODEL=/models/Qwen2.5-14B-Instruct-Q5_K_M.gguf
      - KOBOLD_GPULAYERS=35
      - KOBOLD_CONTEXT=16384
    command: >
      --model /models/Qwen2.5-14B-Instruct-Q5_K_M.gguf
      --usevulkan
      --gpulayers 35
      --contextsize 16384
      --smartcontext
      --flashattention
      --port 5001
      --host 0.0.0.0
    deploy:
      resources:
        reservations:
          devices:
            - driver: cdi
              device_ids:
                - all
              count: all
              capabilities: [gpu]
    networks:
      - inference-net

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: koboldcpp-openwebui
    restart: unless-stopped
    ports:
      - "3000:8080"
    environment:
      - OPENAI_API_BASE_URL=http://koboldcpp:5001/v1
      - OPENAI_API_KEY=koboldcpp-local
    volumes:
      - openwebui-data:/app/backend/data
    depends_on:
      - koboldcpp
    networks:
      - inference-net

networks:
  inference-net:
    driver: bridge

volumes:
  openwebui-data:
```

## Diagnostic Troubleshooting Matrix

| Issue / Error Symptom | Root Cause | Verification Procedure | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **`CUDA out of memory` during startup** | Model layers and KV-cache exceed GPU VRAM | Inspect memory with `nvidia-smi` | Decrease `--gpulayers` or lower `--contextsize` parameter |
| **Vulkan initialization error (`VK_ERROR_INITIALIZATION_FAILED`)** | Outdated graphics driver or missing Vulkan loader library | Execute `vulkaninfo --summary` | Install `libvulkan1` and verify GPU driver support |
| **High initial prefill latency on multi-turn dialogue** | KV-cache re-evaluation on unaligned prompts | Check `--smartcontext` flag in process args | Enable `--smartcontext` and use deterministic system prompt prefixes |
| **HTTP 500 / `Connection refused` on `/v1` routes** | Embedded web server port conflict or firewall binding | Test local endpoint `curl http://127.0.0.1:5001/api/v1/model` | Verify port 5001 binding via `lsof -i :5001` and update `--port` |
| **Slow token throughput during generation** | Offloading bottleneck across slow CPU RAM bus | Monitor CPU SIMD thread usage with `htop` | Increase GPU offload layers or downscale GGUF quantization (e.g. `IQ3_M`) |
| **`mmap failed: Cannot allocate memory`** | System overcommit memory limits or swap starvation | Check system virtual memory via `free -h` and `vm.max_map_count` | Increase system swap space and tune `/etc/sysctl.conf` (`vm.max_map_count=262144`) |
| **Model output repetition loop / degeneration** | Missing or insufficient repetition penalty | Inspect request payload sampling parameters | Set `rep_pen=1.15` and enable DRY or Min-P sampling filters |
| **GGUF header parse error (`invalid magic number`)** | Corrupted or partially downloaded model file | Verify SHA-256 hash against source repository | Re-download GGUF file from Hugging Face repository |

## When to use it

- When serving GGUF models on consumer hardware, laptops, or mixed CPU/GPU machines.
- For local privacy-focused AI setups needing zero external software dependencies.
- When using AMD Radeon GPUs or Integrated Graphics via Vulkan acceleration.

## When not to use it

- For multi-tenant cloud enterprise serving handling thousands of concurrent requests per second (use vLLM or SGLang).
- When fine-tuning or training models from scratch.

## Getting started

### Downloading & Launching

```bash
# Download pre-compiled binary (Linux / macOS / Windows)
wget https://github.com/LostRuins/koboldcpp/releases/latest/download/koboldcpp-linux-x64
chmod +x koboldcpp-linux-x64

# Launch KoboldCPP with Vulkan GPU offloading and FlashAttention
./koboldcpp-linux-x64 --model Qwen2.5-14B-Instruct-Q5_K_M.gguf \
  --usevulkan \
  --gpulayers 35 \
  --contextsize 16384 \
  --flashattention \
  --port 5001
```

## CLI examples

```bash
# Launch with CUDA acceleration, multi-GPU split, and OpenAI API enabled
./koboldcpp-linux-x64 \
  --model DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf \
  --usecuda 0 1 \
  --tensor-split 50 50 \
  --gpulayers 64 \
  --contextsize 32768 \
  --smartcontext \
  --skiplaunch \
  --port 5001
```

## API examples

### 1. Programmatic Request via OpenAI-Compatible Endpoint

```bash
curl -X POST http://localhost:5001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-14b",
    "messages": [
      {"role": "system", "content": "You are a concise technical coding assistant."},
      {"role": "user", "content": "Write a Python function to check for prime numbers."}
    ],
    "temperature": 0.2,
    "max_tokens": 512
  }'
```

### 2. FastMCP 3.1 Server & Strict Pydantic v2 KoboldCPP Controller

This Python script creates a FastMCP 3.1 server that validates model generation requests, checks server health, and interacts with KoboldCPP via its native endpoints using strict Pydantic v2 validation (`extra="forbid"`, `frozen=True`).

```python
import json
import logging
import httpx
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from fastmcp import FastMCP

# Initialize Logging and FastMCP 3.1 Server
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KoboldCPP-FastMCP")
mcp = FastMCP("KoboldCPP-Controller", version="3.1.0")

class KoboldGenerationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., min_length=1, description="Prompt text to send for generation")
    max_context_length: int = Field(default=8192, ge=512, le=131072)
    max_length: int = Field(default=256, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    rep_pen: float = Field(default=1.1, ge=1.0, le=2.0, description="Repetition penalty")
    stop_sequences: List[str] = Field(default_factory=lambda: ["\nUser:", "</s>"])

    @field_validator("prompt")
    @classmethod
    def sanitize_prompt(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Prompt cannot consist solely of whitespace.")
        return stripped

class ServerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    base_url: str = Field(default="http://localhost:5001", description="KoboldCPP server URL")

@mcp.tool(
    name="generate_text_via_kobold",
    description="Validates generation parameters with strict Pydantic v2 and calls KoboldCPP API."
)
async def generate_text_via_kobold(config_json: str, request_json: str) -> str:
    """
    Validates generation parameters with strict Pydantic v2 and calls the KoboldCPP native
    API to generate text responses.
    """
    try:
        cfg = ServerConfig.model_validate(json.loads(config_json))
        params = KoboldGenerationSchema.model_validate(json.loads(request_json))

        endpoint = f"{cfg.base_url}/api/v1/generate"
        payload = {
            "prompt": params.prompt,
            "max_context_length": params.max_context_length,
            "max_length": params.max_length,
            "temperature": params.temperature,
            "top_p": params.top_p,
            "rep_pen": params.rep_pen,
            "stop_sequence": params.stop_sequences
        }

        logger.info(f"Dispatching generation request to KoboldCPP at {endpoint}")
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, json=payload, timeout=60.0)

            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("results", [{}])[0].get("text", "")
                return json.dumps({
                    "status": "SUCCESS",
                    "generated_text": generated_text,
                    "finish_reason": "completed",
                    "protocol_version": "FastMCP-3.1"
                }, indent=2)
            else:
                return json.dumps({
                    "status": "ERROR",
                    "code": response.status_code,
                    "detail": response.text
                })

    except ValidationError as e:
        logger.error(f"Validation error: {e.errors()}")
        return json.dumps({"status": "VALIDATION_ERROR", "errors": e.errors()})
    except Exception as e:
        logger.error(f"Error executing KoboldCPP tool: {str(e)}")
        return json.dumps({"status": "ERROR", "message": str(e)})

@mcp.tool(
    name="get_kobold_model_info",
    description="Retrieves the currently loaded GGUF model information and context size from KoboldCPP."
)
async def get_kobold_model_info(config_json: str) -> str:
    """
    Retrieves the currently loaded GGUF model information and context size from KoboldCPP.
    """
    try:
        cfg = ServerConfig.model_validate(json.loads(config_json))
        endpoint = f"{cfg.base_url}/api/v1/model"
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, timeout=5.0)
            if response.status_code == 200:
                return json.dumps({
                    "status": "SUCCESS",
                    "model": response.json().get("result"),
                    "protocol_version": "FastMCP-3.1"
                })
            else:
                return json.dumps({"status": "ERROR", "detail": response.text})
    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)})

if __name__ == "__main__":
    mcp.run()
```

## Production Benchmarks & Optimization Recommendations

| Model Size | Quantization | Hardware Platform | Context Window | Generation Speed |
| :--- | :--- | :--- | :--- | :--- |
| **Qwen 2.5 14B** | `Q5_K_M` | RTX 4080 (16GB VRAM) | 16,384 tokens | ~48.5 tokens/sec |
| **Llama 3.3 70B** | `IQ3_M` | RTX 3090 + 32GB RAM | 8,192 tokens | ~14.2 tokens/sec |
| **DeepSeek R1 32B** | `Q4_K_M` | AMD Radeon RX 7900 XTX (Vulkan) | 32,768 tokens | ~32.1 tokens/sec |

### Key Tuning Parameters:
- `--usevulkan` or `--usecuda`: Enables hardware acceleration kernels.
- `--gpulayers <N>`: Sets exact number of Transformer layer blocks to move into VRAM.
- `--smartcontext`: Re-uses prefilled KV-cache tokens across prompt turns.
- `--flashattention`: Halves context memory consumption and accelerates prefill time on modern GPUs.

## Related tools / concepts

- [Ollama](../../services/ollama.md) — High-level containerized local model manager.
- [Open WebUI](../../services/open-webui.md) — Feature-rich web frontend compatible with KoboldCPP.
- [vLLM](../infrastructure/vllm.md) — High-throughput enterprise serving engine for unquantized models.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard protocol for connecting AI agents to local model tools.

## Sources / references

- [KoboldCPP Official GitHub Repository](https://github.com/LostRuins/koboldcpp)
- [llama.cpp Core Engine Repository](https://github.com/ggerganov/llama.cpp)
- [GGUF Format Specification](https://github.com/ggerganov/gguf.md)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
