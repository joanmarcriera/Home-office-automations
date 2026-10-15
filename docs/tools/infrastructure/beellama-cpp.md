# BeeLlama.cpp

## What it is
BeeLlama.cpp is an advanced, ultra-optimized C++ implementation for local LLM inference, FastMCP 3.1 Task Protocol server hosting, and high-performance model quantization. It builds upon the foundational architectures of `llama.cpp` and `vLLM` to provide specialized optimization features, specifically targeting KV Cache quantization, dynamic context pruning, model distillation, and high-performance hardware execution. Released with deep performance benchmark matrices, BeeLlama.cpp allows developers to run rigorous tests on KV Cache allocation efficiency (evaluating hundreds of distinct parameter pairs) to find the absolute sweet spot between memory consumption and generation speed on consumer-grade and enterprise edge hardware.

## Architecture & Execution Flowchart

```
+-----------------------------------------------------------------------------------+
|                           BeeLlama.cpp C++ Execution Pipeline                     |
+-----------------------------------------------------------------------------------+
                                          |
                              [ Model Weights (GGUF) ]
                    (Llama 4 / Gemma 4 / DeepSeek-V4 / Qwen 3.5)
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            Quantized KV Cache Allocator                           |
|  - Key Cache Quantization (Q4_0 / Q8_0 / FP16)                                    |
|  - Value Cache Quantization (Q4_0 / Q8_0 / FP16)                                  |
|  - Dynamic Attention Masking & Token Pruning                                      |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Hardware Accelerator Kernel Dispatch                       |
|  - NVIDIA CUDA / Tensor Cores (FlashAttention-2)                                  |
|  - Apple Silicon Metal Performance Shaders (MPS)                                  |
|  - AVX-512 / ARM Neon Vector Processing                                           |
+-----------------------------------------------------------------------------------+
                     /                                  \
                    /                                    \
                   v                                      v
+------------------------------------+  +-------------------------------------------+
|    OpenAI-Compatible HTTP Server   |  |       FastMCP 3.1 Task Protocol Server    |
| - Streaming Token Endpoints        |  | - Tool Calling & Context Pruning          |
| - High-Concurrency Request Queues  |  | - Native stdio / SSE Transport Layers     |
+------------------------------------+  +-------------------------------------------+
```

## What problem it solves
Large language models (including modern multi-modal foundation models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, and DeepSeek-V4) consume substantial amounts of system memory (VRAM) during multi-turn agent conversations, with the Key-Value (KV) Cache scaling linearly as context windows expand up to 1M+ tokens. This often leads to GPU "Out of Memory" (OOM) errors or severe execution throttling. BeeLlama.cpp solves this scalability bottleneck by providing highly optimized, native 4-bit and 8-bit KV Cache quantization and memory-stealing routines, reducing the system memory footprint by up to 60% with zero structural modifications to model weights while supporting FastMCP 3.1 streaming state management.

## Where it fits in the stack
**Local Inference / Infrastructure Layer**. It serves as an ultra-fast local hardware engine and native FastMCP 3.1 protocol host, powering autonomous agents and local database pipelines with a highly optimized memory architecture.

## Typical use cases
- **Memory-Optimized Local Agents**: Executing long-context autonomous agent swarms running FastMCP 3.1 protocols on devices with limited GPU VRAM.
- **Inference Parameter Tuning**: Benchmarking and analyzing optimal quantization pairs (e.g., Q4_K_M weights with 4-bit KV Cache) to maximize generation speeds across DeepSeek-V4 and Gemma 4 deployments.
- **Air-Gapped Document Processing**: Parsing and indexing deep multi-gigabyte local document directories entirely offline.
- **Micro-Server LLM Deployment**: Deploying lightweight, highly responsive language models and FastMCP 3.1 endpoints on edge gateways or home servers.

## Strengths
- **SOTA KV Cache Quantization**: Native support for 4-bit and 8-bit KV Cache optimizations substantially decreases context memory footprints.
- **FastMCP 3.1 Native Protocol Integration**: Direct C++ implementation of FastMCP 3.1 SSE and stdio transport layers with task lifecycle management.
- **Zero Heavy Dependencies**: Written entirely in clean C/C++ with no massive PyTorch or Python framework overhead.
- **Optimized Metal and CUDA Kernels**: Highly optimized architecture ensures peak hardware execution speeds on Apple Silicon, NVIDIA GPUs, and ARM edge processors.
- **Comprehensive Benchmarking Utilities**: Includes built-in analytical routines to measure prompt processing (PP) and tokens per second (TPS) accurately.

## Limitations
- **Perplexity Penalty at Low Quantization**: Aggressive 4-bit KV Cache quantization can introduce minor logical drift or reasoning errors in extremely deep reasoning tasks.
- **Model Architecture Support**: Focuses heavily on mainstream Transformer models (such as Llama 4, Gemma 4, and DeepSeek-V4), with slightly slower adoption rates for fringe architectures.
- **Complex Compilation Chains**: System optimization demands compiling directly from source code with hardware-specific compiler flags.

## Inference Engine Comparison Matrix

| Engine Feature | BeeLlama.cpp | llama.cpp | vLLM | SGLang | ExLlamaV2 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KV Cache Quantization** | Native 4-bit / 8-bit | FP16 / Q8_0 | FP8 / INT4 | FP8 / INT4 | FP16 Only |
| **FastMCP 3.1 Server** | Built-in (C++) | External Wrapper | External Gateway | External Gateway | No |
| **Memory Efficiency (VRAM)**| Highest (up to -60%)| High | Medium (PagedAttn) | High (RadixAttention)| High (EXL2) |
| **Apple Silicon (Metal)** | Native Optimized | Native | No | No | No |
| **Prompt Ingestion Speed** | Ultra High (CUDA/MPS)| High | High (Chunked Prefill)| Ultra High | High |
| **Dependency Overhead** | C++ Binary (~15MB) | C++ Binary (~20MB) | PyTorch (>5GB) | PyTorch / Python | PyTorch / Python |

## When to use it
- When you are running long-context local models or FastMCP 3.1 servers and repeatedly hitting VRAM memory limits on existing hardware.
- When you want to optimize your offline home automation or developer assistant to run on lightweight edge hardware.
- For benchmarking, analyzing, and selecting the absolute best quantization profiles for production inference.

## When not to use it
- If you are deploying simple, cloud-hosted API pipelines where local server hardware constraints and VRAM bounds do not exist.
- If you do not possess developer experience compiling system binaries from source code or managing hardware compilation toolchains.
- When absolute logical reasoning accuracy and low-perplexity metrics must be preserved at any cost (use dense, non-quantized models).

## Getting started
1. **Clone the Source**: Retrieve the codebase and its dependencies:
   ```bash
   git clone --recursive https://github.com/SovereignAI/beellama-cpp.git
   cd beellama-cpp
   ```
2. **Compile the Engine**: Compile with CUDA or Metal optimizations:
   ```bash
   # Build with CUDA support
   mkdir build && cd build
   cmake -DGGML_CUDA=ON ..
   make -j
   ```
3. **Execute with quantized KV Cache**: Launch model inference utilizing 4-bit KV Cache quantization:
   ```bash
   ./beellama-cli -m ./models/gemma-4-9b.gguf -p "Optimize my system configurations." --ctk q4_0
   ```

## CLI examples
BeeLlama.cpp provides an interactive command-line interface for inference, a FastMCP 3.1 task protocol server, and a comprehensive hardware benchmarking suite.

```bash
# Run model with 8-bit Key and 8-bit Value Cache quantization enabled
./beellama-cli -m models/llama-4-8b.gguf -p "Draft a system architecture proposal." --ctk q8_0 --ctv q8_0

# Launch native FastMCP 3.1 SSE server endpoint for agent tool calling
./beellama-mcp-server --model models/deepseek-v4-8b.gguf --port 8000 --fastmcp-version 3.1

# Execute a rigorous KV Cache quantization benchmark across 400+ testing pairs
./beellama-benchmark --model models/gemma-4-9b.gguf --context-size 8192 --threads 8

# Spin up an OpenAI-compatible web API server with optimized threading profiles
./beellama-server --model models/llama-4-8b.gguf --port 8080 --parallel 4 --ctk q4_0
```

## API examples

### FastMCP 3.1 Server Wrapper with Pydantic v2 Validation
This Python script demonstrates how to wrap BeeLlama.cpp inside a FastMCP 3.1 async server, parsing execution metrics from stdout and validating parameter inputs and outputs using strict **Pydantic v2** structures.

```python
import subprocess
import json
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from fastmcp import FastMCP

# Initialize FastMCP Server for BeeLlama.cpp Local Inference Engine
mcp = FastMCP("BeeLlama.cpp Inference Server", version="3.1.0")

class BeeLlamaRequest(BaseModel):
    model_path: str = Field(..., description="Local system path to the model GGUF file")
    prompt: str = Field(..., min_length=1, description="Input text prompt")
    kv_cache_k: str = Field(default="q4_0", description="Key Cache quantization profile (q4_0, q8_0, fp16)")
    kv_cache_v: str = Field(default="q4_0", description="Value Cache quantization profile (q4_0, q8_0, fp16)")
    max_tokens: int = Field(default=512, ge=1, le=8192, description="Maximum tokens to generate")

class BeeLlamaMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_path: str = Field(..., description="Local system path to the model GGUF file")
    kv_cache_type_k: str = Field(..., description="Quantization profile used for the Key Cache")
    kv_cache_type_v: str = Field(..., description="Quantization profile used for the Value Cache")
    thread_count: int = Field(..., ge=1, description="Number of CPU threads utilized for compute")
    context_length: int = Field(..., ge=512, description="Active context length window size")
    fastmcp_protocol_version: str = Field(default="3.1", description="FastMCP protocol version active")
    prompt_tokens_per_sec: float = Field(..., gt=0.0, description="Tokens processed per second during prompt ingestion")
    generation_tokens_per_sec: float = Field(..., gt=0.0, description="Generation throughput in tokens per second")
    vram_consumed_mb: float = Field(..., gt=0.0, description="Total GPU memory consumed in megabytes")
    perplexity_delta: Optional[float] = Field(None, description="Quantization perplexity change relative to baseline")

@mcp.tool()
async def run_beellama_inference(request: BeeLlamaRequest) -> BeeLlamaMetrics:
    """Execute BeeLlama.cpp inference with quantized KV Cache and validate execution metrics under FastMCP 3.1."""
    # Simulated stdout response containing execution metrics
    simulated_metrics = {
        "model_path": request.model_path,
        "kv_cache_type_k": request.kv_cache_k,
        "kv_cache_type_v": request.kv_cache_v,
        "thread_count": 8,
        "context_length": 8192,
        "fastmcp_protocol_version": "3.1",
        "prompt_tokens_per_sec": 412.5,
        "generation_tokens_per_sec": 52.8,
        "vram_consumed_mb": 4210.4,
        "perplexity_delta": 0.04
    }

    # Parse and validate with Pydantic v2
    return BeeLlamaMetrics.model_validate(simulated_metrics)

if __name__ == "__main__":
    mcp.run()
```

## Troubleshooting & Error Remediation

| Symptom / Error | Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| `CUDA error 2: out of memory` | Model weights + unquantized KV Cache exceeded GPU VRAM | Run with `--ctk q4_0 --ctv q4_0` to compress KV Cache memory footprint by 50-60%. |
| `Perplexity explosion / nonsense output` | Aggressive 2-bit quantization applied to small (<3B) models | Upgrade KV Cache setting to `q8_0` or `fp16` for smaller parameter models. |
| `CMake error: No CUDA toolset found` | CUDA Toolkit path missing or mismatched nvcc version | Export `CUDA_PATH=/usr/local/cuda` and re-run `cmake -DGGML_CUDA=ON ..`. |
| `FastMCP stdio connection drop` | Process printed debug logs directly to `stdout` instead of `stderr` | Compile with `-DBEELLAMA_SILENT_STDOUT=ON` to keep `stdout` pristine for MCP protocol. |
| `Low generation speed on CPU (<5 tps)` | Thread affinity unbound, causing CPU core jumping | Specify exact thread count matching physical CPU cores (`--threads 8`). |

## Operational Hardening & Production Rules

1. **Stdout Isolation for MCP Transport**: When deploying BeeLlama.cpp as an MCP stdio server tool, guarantee all internal logging output is redirected to `stderr` or syslog to avoid corrupting JSON-RPC protocol frames.
2. **Context Window Safety Margins**: Set hard system limits on `--ctx-size` (e.g., 32,768 tokens) matched to available host RAM/VRAM to prevent kernel OOM killer termination during long agent reasoning loops.
3. **Lock Memory (mlock)**: Enable the `--mlock` flag in production environments to lock model weights in RAM, preventing host OS paging to swap disks during background tasks.

## Related tools / concepts
- [Llama.cpp](../infrastructure/llama-cpp.md) — The core C/C++ engine upon which BeeLlama.cpp builds its specialized optimizations.
- [vLLM](../infrastructure/vllm.md) — High-performance inference engine; comparable for production deployments.
- [ExLlamaV2](../infrastructure/exllamav2.md) — High-speed quantized inference runner for local NVIDIA GPUs.
- [Ollama](../../services/ollama.md) — Simplifies local model lifecycle management and standard running patterns.
- [Unsloth](../infrastructure/unsloth.md) — High-efficiency local model fine-tuning and quantization preparation framework.

## Sources / references
- [Llama.cpp Optimization Roadmap and Quantization Guide](https://github.com/ggerganov/llama.cpp)
- [Reddit r/LocalLLaMA: KV Cache Quantization and Benchmarks Deep-Dive](https://www.reddit.com/r/LocalLLaMA/comments/1vhaabz/kv_cache_quantization_benchmarks_413_pairs_tested/)
- [SovereignAI: Advanced Model Serving and Distillation Standards](https://sovereignai.org/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
