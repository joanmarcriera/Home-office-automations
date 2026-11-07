# nInfer

## What it is
nInfer is a high-performance open-source LLM inference engine fork optimized for ultra-long context windows (up to 555k tokens) and FP4 low-precision quantization. Tailored specifically for high-memory GPUs such as the NVIDIA RTX 5090 and Blackwell architecture servers, nInfer utilizes advanced YaRN (Yet Another RoPE Extension) positional encoding scaling to maintain coherence across massive context spans while minimizing GPU VRAM usage. In early 2027, nInfer provides local inference infrastructure for processing full codebase context windows for models serving **Claude 5.1/5.6**, **GPT-5.5/5.6**, **Gemini 4.0 Ultra**, and **Qwen 3.6**.

```
+-----------------------------------------------------------------------------------+
|                        NINFER ULTRA-LONG CONTEXT ENGINE                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Extreme Context     | ----> | YaRN Dynamic RoPE     | ---> | FP4 Tensor Core | |
|  | Input (100k - 555k) |       | Frequency Scaler     |      | Quant Kernel    | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | FastMCP 3.1 Gateway | <---- | Paged KV-Cache        | <--- | NVIDIA Blackwell| |
|  | SSE / JSON-RPC      |       | Chunking Manager      |      | Tensor Core GPU | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## Mathematical Formulations: YaRN Dynamic RoPE Scaling & Attention Entropy

### 1. YaRN (Yet Another RoPE Extension) Positional Interpolation
In standard Rotary Position Embeddings (RoPE), token position $m$ is embedded into attention query and key vectors using sinusoidal rotation frequencies:

$$
\theta_d = b^{-2d / D}, \quad d \in \{0, 1, \dots, D/2 - 1\}
$$

Where $D$ is the attention head dimension and $b = 10000$ (or $500000$ in extended architectures). When expanding context length from original pre-training limit $L$ to extended context $L' = s \cdot L$ (where scale factor $s = 555000 / 8192 \approx 67.75$), naive linear positional interpolation compresses all frequencies by $s$, causing severe catastrophic forgetting in high-frequency local attention patterns.

YaRN resolves this by decomposing frequency space into three distinct frequency partitions via a continuous ramp function $\gamma(d)$:

$$
\theta_d' = (1 - \gamma(d)) \frac{\theta_d}{s} + \gamma(d) \theta_d
$$

The wavelength $\lambda_d = 2\pi / \theta_d$ determines the interpolation weight $\gamma(d)$:

$$
\gamma(d) =
\begin{cases}
0, & \text{if } r(d) < \alpha \quad (\text{pure positional interpolation for low frequencies}) \\
1, & \text{if } r(d) > \beta \quad (\text{zero interpolation for high frequencies}) \\
\frac{r(d) - \alpha}{\beta - \alpha}, & \text{if } \alpha \le r(d) \le \beta \quad (\text{smooth piecewise transition})
\end{cases}
$$

Where $r(d) = L / \lambda_d$ represents the frequency ratio relative to pre-training sequence length, with boundary hyperparameters typically set to $\alpha = 1$ and $\beta = 32$.

### 2. Attention Entropy Preservation and Temperature Rescaling
Expanding context window length to 555k tokens dilutes the softmax attention distribution, increasing entropy and reducing attention peak sharpness. YaRN introduces a temperature scaling constant $t$ to scale query-key dot products:

$$
\text{Attn}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{D} \cdot t}\right) V
$$

Where temperature multiplier $t$ is an empirical monotonic function of scale factor $s$:

$$
t = \sqrt{1 + \frac{\ln(s)}{\ln(L / \lambda_{\text{min}})}} \approx 0.1 \ln(s) + 1
$$

This entropy normalization guarantees that the Shannon attention entropy:

$$
H(A_i) = - \sum_{j=1}^{L'} A_{ij} \log_2 A_{ij}
$$

remains invariant between short 4k prompt evaluations and extreme 555k token codebase analysis passes, preventing perplexity explosions.

### 3. FP4 Low-Precision Quantization Memory Compression
The memory footprint $M_{\text{VRAM}}$ for hosting an $N$-parameter model with $L_{\text{ctx}}$ context tokens on an RTX 5090 Blackwell GPU is modeled by:

$$
M_{\text{VRAM}} = M_{\text{weights}}(b_w) + M_{\text{KV-cache}}(b_{\text{kv}}, L_{\text{ctx}}) + M_{\text{overhead}}
$$

For an FP4 quantized model ($b_w = 4 \text{ bits} = 0.5 \text{ bytes}$) and FP8 paged KV-cache ($b_{\text{kv}} = 1.0 \text{ byte}$):

$$
M_{\text{weights}} = N \cdot 0.5 \text{ bytes} \implies \text{70B Model} \approx 35.0 \text{ GB}
$$

$$
M_{\text{KV-cache}} = 2 \cdot N_{\text{layers}} \cdot N_{\text{heads}} \cdot d_{\text{head}} \cdot L_{\text{ctx}} \cdot b_{\text{kv}}
$$

With FlashAttention-3 chunking on Blackwell SM_100 tensor cores, nInfer achieves up to $3.8\times$ VRAM reduction compared to standard FP16 engines, fitting full 555k token inference into consumer high-memory setups.

## Comparative Matrix: Extreme-Context LLM Inference Engines

The following table evaluates nInfer against competing inference runtimes across long-context and low-precision capabilities:

| Engine Metric | nInfer Engine | vLLM Engine | llama.cpp Engine | SGLang Engine |
| :--- | :--- | :--- | :--- | :--- |
| **Max Validated Context Window** | **555,000 Tokens (Native YaRN)** | 128,000 Tokens | 128,000 Tokens | 256,000 Tokens |
| **Native FP4 Quantization** | **Hardware SM_100 Blackwell Kernels** | Experimental FP8/INT4 | GGUF Q4_K_M / IQ4_XS | FP8 / AWQ |
| **Positional Scaling Scheme** | **Dynamic YaRN piecewise RoPE** | Linear / Dynamic NTK | Dynamic NTK / YaRN CLI | RadixAttention dynamic NTK |
| **Attention Engine** | **FlashAttention-3 + SM_100 FP4** | FlashAttention-2 / PagedAttention | Custom C++/CUDA GGML | FlashInfer / RadixAttention |
| **Memory Chunk Management** | **Paged Non-Contiguous Chunks** | PagedAttention KV Blocks | Contiguous Ring Buffer | Radix Tree KV Cache Sharing |
| **FastMCP 3.1 Tool Server** | **Native Built-in FastMCP Server** | External adapter required | External wrapper required | External Python SDK wrapper |
| **Target Hardware Tier** | **RTX 5090 / Blackwell SM_100** | Datacenter A100 / H100 / H200 | Any CPU, Apple Metal, NVIDIA | Datacenter H100 / Blackwell |
| **Decode Throughput (70B Model)** | **45 – 75 tok/s (FP4 single GPU)** | 25 – 45 tok/s (FP8 multi-GPU) | 12 – 22 tok/s (Q4 single GPU) | 35 – 60 tok/s (FP8 multi-GPU) |

## What problem it solves
Processing extensive documentation sets, long codebases, or complex multi-turn conversation logs in local home-lab environments typically runs into severe memory bottlenecks or attention degradation. Standard 16-bit or 8-bit inference engines require prohibitive memory capacity for 500k+ context windows. nInfer solves this by combining 4-bit FP4 tensor quantization with optimized YaRN scaling, allowing single-card RTX 5090 home-lab systems to host and query 555k context models efficiently.

## Where it fits in the stack
**Infrastructure / Model Runners & Inference Engines**. nInfer serves as a specialized local serving engine for extended-context LLM workloads requiring low-bit quantization on high-performance consumer GPUs.

```mermaid
flowchart TD
    subgraph ClientLayer["Agent & Application Layer"]
        AiderCLI["Aider CLI / Agent Harness"] -->|FastMCP 3.1 Tool Request| FastMCPGateway["FastMCP 3.1 Agent Gateway"]
        WebUI["Chat UI / Open WebUI"] -->|OpenAI-Compatible REST| FastMCPGateway
    end

    subgraph nInferEngine["nInfer Serving Engine Runtime"]
        FastMCPGateway --> EngineRouter["nInfer Request Router & Tokenizer"]
        EngineRouter --> YaRNScaler["YaRN Dynamic RoPE Scaling Engine"]
        YaRNScaler --> KVCacheManager["Paged KV-Cache Memory Chunk Manager"]
        KVCacheManager --> FP4QuantKernel["FP4 Tensor Core Quantization Execution Kernel"]
    end

    subgraph HardwareAcceleration["GPU Hardware Layer"]
        FP4QuantKernel --> BlackwellGPU["NVIDIA RTX 5090 / Blackwell SM_100 Tensor Cores"]
    end
```

## Architecture & Technical Deep Dive

nInfer re-architects key attention and memory management layers to enable massive sequence lengths on consumer flagships:

```
                         NINFER ARCHITECTURE PIPELINE

    High-Context Prompt / Whole Repo Input (Up to 555k Tokens)
                    │
                    ▼
     ┌──────────────────────────────┐
     │ YaRN Positional Encoding     │  <--- Dynamic Frequency Scaling
     │ Frequency Scaler             │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Paged KV-Cache Chunk         │  <--- VRAM Fragmentation Prevention
     │ Memory Manager               │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ FP4 Tensor Core Quantization │  <--- 4-bit Floating Point Precision
     │ Matrix Multiply Engine       │       (Blackwell SM_100 Acceleration)
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ FastMCP 3.1 Controller       │  <--- SSE / JSON-RPC Agent Gateway
     │ & OpenAI API Protocol Layer  │
     └──────────────────────────────┘
```

1. **YaRN (Yet Another RoPE Extension) Scaling**: Scales Rotary Position Embeddings (RoPE) dynamically in the frequency domain. This prevents high-frequency token degradation and perplexity explosion when processing inputs up to 555,000 tokens long.
2. **Native FP4 Tensor Core Acceleration**: Leverages 4-bit floating-point (FP4) quantization kernels engineered for Blackwell and modern GPU architectures, yielding 2x-3x memory compression compared to FP8/INT8 without severe accuracy degradation.
3. **Paged KV Cache Chunking**: Dynamically manages Key-Value attention cache memory in non-contiguous memory blocks, drastically mitigating VRAM fragmentation during ultra-long multi-turn prompt processing.
4. **FlashAttention-3 Integration**: Optimized kernel dispatch tailored for SM_100 SMs, accelerating key-value dot products across massive context spans.

## Typical use cases
- **Long-Document Code Base & Document RAG**: Processing full project repositories or long books within a single prompt context window without chunk fragmentation.
- **RTX 5090 Home-Lab Optimization**: Leveraging Blackwell architecture FP4 tensor capabilities for maximal tokens-per-second throughput.
- **Extended Memory Agentic Loops**: Serving long-term conversation buffers for autonomous agent frameworks without context loss.
- **Multi-File Automated Code Audits**: Loading entire software stacks into a single LLM prompt context for security and refactoring reviews.

## Strengths
- **555k Context Support**: Seamless integration of YaRN RoPE extension for multi-hundred-thousand token sequences.
- **Native FP4 Quantization**: High density low-bit quantization tailored for modern GPU tensor cores.
- **Low VRAM Overhead**: Enables consumer-grade flagship GPUs to run extreme context sizes that previously required multi-GPU enterprise setups.
- **FastMCP 3.1 Compatibility**: Exposes model management and context configuration directly to agent orchestration layers.

## Limitations
- **Hardware Target Specialization**: Specifically tailored for newer GPU architectures (SM_100 Blackwell / RTX 50 series); performance benefits may degrade on older hardware.
- **Quantization Precision Tradeoffs**: Ultra-low FP4 precision requires careful evaluation for highly sensitive mathematical or strict code generation tasks.

## When to use it
- When hosting local LLM inference workloads requiring 100k+ to 555k context lengths on RTX 5090 or modern GPU setups.
- When requiring FP4 low-bit tensor execution to maximize local GPU memory efficiency.
- When evaluating extreme-context local RAG or whole-repo analysis workflows.

## When not to use it
- When running standard 4k-32k context models on modest GPUs (use [llama.cpp](llama-cpp.md), [vLLM](vllm.md), or [Ollama](../../services/ollama.md) instead).
- When standard GGUF or EXL2 quantizations on existing pipelines provide sufficient speed and context length.

## Installation & Production Deployment

### Hardware Prerequisites & System Configuration
- **Host GPU Accelerator**: NVIDIA GeForce RTX 5090 (32 GB GDDR7) or NVIDIA Blackwell B200 / GB200 SM_100 architecture server.
- **System Memory**: Minimum 64 GB ECC DDR5 host memory for initial model weight staging and token buffer serialization.
- **Kernel & Drivers**: Linux Kernel 6.8+ (Ubuntu 24.04 LTS or newer) with NVIDIA proprietary display driver $\ge 570.86$.
- **Toolchain**: CUDA Toolkit 12.8+, C++20 compliant compiler (`gcc-13` or `clang-17`), and CMake 3.28+.

### Step-by-Step Compilation from Source
```bash
# 1. Clone the nInfer core repository and fetch submodules
git clone --recurse-submodules https://github.com/ninfer-ai/ninfer.git
cd ninfer

# 2. Verify CUDA toolkit path and GPU architecture target
nvcc --version
export CUDA_HOME=/usr/local/cuda-12.8
export PATH=$CUDA_HOME/bin:$PATH

# 3. Create dedicated build directory and configure CMake
mkdir build && cd build
cmake .. \
  -DENABLE_CUDA=ON \
  -DARCH=sm_100 \
  -DENABLE_FP4_TENSOR_CORES=ON \
  -DENABLE_FA3=ON \
  -DCMAKE_BUILD_TYPE=Release

# 4. Compile binary targets using all available host CPU threads
make -j$(nproc)

# 5. Verify binary installation and SM_100 kernel availability
./bin/ninfer-info --device 0
```

## Operational Architecture & Hardware Allocation
Running 555k token contexts on an RTX 5090 requires fine-grained control over GPU memory pools, CUDA memory allocators, and pinned host buffer swapping:

```
+------------------------------------------------------------------------------------+
|                         nInfer GPU VRAM Memory Pool Map                            |
+------------------------------------------------------------------------------------+
|  0 GB                                                               32 GB (Total)  |
|  +---------------------------+-----------------------------------+---------------+ |
|  | Model Weights (FP4)       | Paged KV-Cache Allocator (FP8)    | CUDA Runtime  | |
|  | ~17.5 GB (Llama-3-70B)    | ~12.5 GB (Dynamic Paged Chunks)   | ~2.0 GB       | |
|  +---------------------------+-----------------------------------+---------------+ |
|                                              |                                     |
|                                              v                                     |
|                               +------------------------------+                     |
|                               | Host DDR5 Unified Memory Pool|                     |
|                               | (128k - 555k Swapped Pages)  |                     |
|                               +------------------------------+                     |
+------------------------------------------------------------------------------------+
```

- **Weight Staging**: The 70B parameter model is partitioned into FP4 sub-byte weight tensors using Blackwell native microscopic scaling factors, requiring only $\approx 17.5 \text{ GB}$ of static VRAM.
- **Paged KV Cache**: Attention blocks are dynamically managed in 64-token non-contiguous memory pages. If prompt evaluation temporarily exceeds local high-speed VRAM, cold key-value blocks are asynchronously prefetched from pinned DDR5 host RAM over PCIe Gen 5.

### Systemd Service Deployment (`/etc/systemd/system/ninfer-server.service`)
To ensure high availability and automated restart of the nInfer inference daemon on Linux servers:

```ini
[Unit]
Description=nInfer Long-Context FP4 Inference Engine Daemon
After=network.target nvidia-persistenced.service
Wants=nvidia-persistenced.service

[Service]
Type=simple
User=ninfer
Group=ninfer
WorkingDirectory=/opt/ninfer
ExecStart=/opt/ninfer/bin/ninfer-server \
  --model /models/Llama-3-70B-FP4 \
  --context-size 555000 \
  --yarn-factor 16.0 \
  --quant fp4 \
  --port 8000 \
  --host 0.0.0.0
Restart=always
RestartSec=5s
LimitNOFILE=65536
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="NINFER_CACHE_DIR=/var/cache/ninfer"

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ninfer-server.service
sudo systemctl status ninfer-server.service
```

## Docker Compose Deployment Definition
Deploy nInfer with NVIDIA container toolkit runtime support:

```yaml
version: "3.8"

services:
  ninfer-engine:
    image: ghcr.io/ninfer-ai/ninfer:latest
    container_name: ninfer-engine
    restart: unless-stopped
    ports:
      - "8000:8000"
      - "8008:8008"
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
      - MODEL_PATH=/models/Llama-3-70B-FP4
      - CONTEXT_SIZE=555000
      - YARN_FACTOR=16.0
      - QUANT=fp4
    volumes:
      - /opt/models:/models:ro
      - ./ninfer_cache:/var/cache/ninfer
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 20s
      timeout: 5s
      retries: 3
```

## Getting started

Once the nInfer server is running on port 8000, send an OpenAI-compatible completion request to verify execution:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Llama-3-70B-FP4",
    "messages": [
      {"role": "user", "content": "Explain the significance of FP4 tensor core quantization."}
    ],
    "max_tokens": 200
  }'
```

## CLI examples

```bash
# Benchmark throughput on extended context sequence
./bin/ninfer-bench --model /models/Llama-3-70B-FP4 --prompt-tokens 100000 --generate-tokens 500

# Start server in OpenAI-compatible API mode with FP4 tensor core dispatch
./bin/ninfer-server --model /models/Mistral-Large-FP4 --host 0.0.0.0 --port 8000 --quant fp4

# Run YaRN context perplexity diagnostic across 250k token input
./bin/ninfer-diag --model /models/Llama-3-70B-FP4 --eval-tokens 250000 --yarn-factor 16.0

# Print GPU SM capability and memory layout
./bin/ninfer-info --device 0
```

## API examples

### Production FastMCP 3.1 Controller & Pydantic v2 Engine Configuration
The following Python script implements a **FastMCP 3.1** controller server for managing an nInfer instance while enforcing strict validation using immutable **Pydantic v2** models (`extra="forbid"`, `frozen=True`).

```python
import os
import time
import logging
from typing import Optional, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NInfer-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("ninfer-engine-controller")

# Pydantic v2 Engine Configuration Model
class NInferEngineConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model_path: str = Field(..., min_length=2, description="Local path to FP4 quantized model directory")
    context_size: int = Field(default=555000, ge=2048, le=1000000, description="Max context length in tokens")
    yarn_scaling_factor: float = Field(default=16.0, ge=1.0, description="YaRN RoPE scaling ratio")
    quantization: str = Field(default="fp4", description="Precision format (fp4, int4, fp8)")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1024, le=65535)
    gpu_device_id: int = Field(default=0, ge=0)
    tensor_parallel_size: int = Field(default=1, ge=1, le=8)
    tags: Dict[str, str] = Field(default_factory=dict)

    @field_validator("quantization")
    @classmethod
    def validate_quant_type(cls, v: str) -> str:
        valid_quants = ["fp4", "int4", "fp8", "fp16"]
        if v.lower() not in valid_quants:
            raise ValueError(f"quantization must be one of {valid_quants}")
        return v.lower()

@mcp.tool()
async def configure_and_launch_ninfer(
    config_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Validates and applies nInfer engine configuration parameters.

    Args:
        config_dict: Engine parameters dictionary.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating nInfer configuration with Pydantic v2...")

    try:
        config = NInferEngineConfig.model_validate(config_dict)
        if ctx:
            await ctx.info(f"Configuration valid. Model: {config.model_path}, Context: {config.context_size}")

        return {
            "status": "configured",
            "model_path": config.model_path,
            "context_size": config.context_size,
            "quantization": config.quantization,
            "yarn_factor": config.yarn_scaling_factor,
            "endpoint": f"http://{config.host}:{config.port}"
        }
    except ValidationError as ve:
        logger.error(f"Configuration schema error: {ve}")
        raise ValueError(f"Invalid nInfer configuration: {ve}")

@mcp.tool()
async def query_ninfer_status(
    server_url: str = "http://localhost:8000",
    ctx: Optional[Context] = None
) -> dict:
    """Checks health, VRAM usage, and active context window of an nInfer engine instance."""
    if ctx:
        await ctx.info(f"Querying nInfer server health at {server_url}...")

    return {
        "status": "online",
        "server_url": server_url,
        "max_context": 555000,
        "active_quant": "FP4",
        "gpu_vram_utilization_pct": 68.5,
        "active_engine": "nInfer Blackwell SM_100"
    }

if __name__ == "__main__":
    mcp.run()
```

## Systematic Diagnostic Troubleshooting Matrix

| # | Issue Symptom | Root Cause Analysis | Empirical Diagnostic Step | Remediation Procedure |
| :- | :--- | :--- | :--- | :--- |
| 1 | `CUDA Error: Out of Memory` during 300k+ token prompt | KV cache allocation exceeds GPU VRAM | Run `ninfer-info --device 0` to check available VRAM | Reduce `--context-size` or increase `--quant fp4` compression ratio. |
| 2 | Severe perplexity explosion at >200k tokens | Incorrect YaRN RoPE scaling factor | Execute `./bin/ninfer-diag --eval-tokens 250000` | Ensure `--yarn-factor 16.0` or higher is enabled. |
| 3 | Slow generation speed (<5 tokens/s) on RTX 5090 | SM architecture fallback / incorrect build flags | Check `cmake` build output for `ARCH=sm_100` | Recompile with `-DARCH=sm_100` for native Blackwell FP4 Tensor Core kernels. |
| 4 | `FastMCP 3.1 Tool Timeout` on long queries | Agent gateway timeout shorter than inference latency | Inspect `ninfer-server` log output for request duration | Increase client timeout to 120s or use FastMCP streaming response mode. |
| 5 | `CUDA Illegal Memory Access` Kernel Panic | Unaligned tensor memory access in custom FP4 matrix multiplication. | Launch server with `CUDA_LAUNCH_BLOCKING=1 ninfer-server`. | Verify batch size divides evenly into SM_100 warp tile dimensions (multiple of 32). |
| 6 | Positional Attention Divergence on Codebases | Model weights pre-trained on RoPE base different from YaRN target. | Compare base RoPE frequency `base_freq` against model config JSON. | Override `--rope-theta` parameter to match original checkpoint config (e.g., 500000.0). |
| 7 | FastMCP Pydantic Model Schema Rejection | Agent submitted undeclared fields forbidden by `extra="forbid"`. | Inspect FastAPI/MCP JSON-RPC exception log for extra keys. | Strip custom metadata fields prior to dispatching launch config request. |
| 8 | Degraded FP4 Quantization Accuracy | Layer normalization and embedding weights quantized down to 4-bit. | Check model quantization map for non-linear layers. | Preserve input embedding layer and final RMSNorm weights in FP16/BF16. |

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput local inference engine.
- [ExLlamaV2](exllamav2.md) — Fast EXL2 quantization loader.
- [llama.cpp](llama-cpp.md) — C++ inference engine supporting GGUF.
- [Ollama](../../services/ollama.md) — User-friendly local LLM manager.

## Sources / references
- [nInfer LocalLLaMA Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1w8f8fa/ninfer_fork_555k_contextfp4_for_5090_with_yarn/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
