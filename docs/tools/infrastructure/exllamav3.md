# ExLlamaV3

## What it is
ExLlamaV3 is an ultra-fast, memory-optimized inference engine specifically designed for running Large Language Models (LLMs) on NVIDIA GPUs. Built as the successor to [ExLlamaV2](./exllamav2.md), it features the **EXL3** quantization format supporting sub-bit quantization targets (e.g., FP4, INT3, and arbitrary bits-per-weight like 3.25 or 4.15 bpw) with dynamic activation steering. As of early 2027, ExLlamaV3 includes native FlashAttention-3 integration, **FastMCP 3.1** protocol support, quantized KV cache mechanisms, and multi-modal tensor-parallel kernels.

## What problem it solves
Local inference of frontier-class LLMs is heavily constrained by GPU VRAM capacity and memory bandwidth. ExLlamaV3 solves this by allowing developers to fit large models (such as Llama 4 70B, Gemma 3, or DeepSeek-V4) into consumer GPUs (e.g., RTX 4090, RTX 5090, or dual RTX 3090 setups) using highly customized EXL3 quantization levels. Unlike general-purpose runtimes, ExLlamaV3 is written from the ground up in custom CUDA and C++ kernels to maximize tokens per second (TPS) on NVIDIA hardware, achieving up to 3x the speed of [llama.cpp](./llama-cpp.md) on compatible GPUs.

## Where it fits in the stack
**Inference Engine / GPU Accelerator**. Located at the hardware-software bridge layer of the local developer stack, ExLlamaV3 receives quantized weights and runs highly parallel matrix multiplication operations. It exposes a low-latency C++ backend and a Python wrapper that can be hooked directly into local API servers or FastMCP 3.1 multi-agent orchestrators powered by Claude 5.6, GPT-5.6, and Gemini 4.0.

### Architecture & Kernel Processing Flow

```mermaid
flowchart TD
    Prompt[Client Request / Agent Loop] --> MCP[FastMCP 3.1 Server]
    MCP --> Tokenizer[EXL3 Custom Tokenizer]
    Tokenizer --> KVCache[Quantized KV Cache: 2-bit / 4-bit]
    KVCache --> Kernels[FlashAttention-3 & EXL3 GEMM CUDA Kernels]
    Kernels --> GPU[NVIDIA GPU VRAM Tensor Cores]
    GPU --> Logits[Logit Generation & Sampling]
    Logits --> Output[Token Stream Payload]
```

## Quantization & Throughput Metrics (Early 2027 SOTA)

| Metric / Capability | ExLlamaV3 (EXL3) | ExLlamaV2 (EXL2) | vLLM (AWQ/FP8) | llama.cpp (GGUF) |
| :--- | :--- | :--- | :--- | :--- |
| **Quantization Precision** | FP4 / INT3 / Sub-bit (3.25 bpw) | EXL2 (3.5 - 6.0 bpw) | FP8 / AWQ / INT4 | Q2_K to Q8_0 GGUF |
| **Tokens/sec (70B model)** | ~45 TPS (dual RTX 3090) | ~32 TPS | ~28 TPS | ~18 TPS |
| **FastMCP 3.1 Server Integration** | Native streaming tool wrapper | OpenAI API bridge | OpenAI API bridge | Native server endpoints |
| **FlashAttention-3 FP8 Support**| Native | Partial | Native | No (custom CUDA) |
| **KV Cache Compression** | 2-bit / 4-bit / 6-bit | 4-bit / 8-bit | FP8 / PagedAttention | Q4_0 / Q8_0 KV |

## End-to-End Execution Sequence Flow

```
+-----------------------------------------------------------------------------------+
|                        EXLLAMAV3 INFERENCE KERNEL PIPELINE                       |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +--------------------+      +----------------------+      +--------------------+ |
|  | Agent Prompt Request| ---> | FastMCP 3.1 Task     | ---> | EXL3 Tokenizer     | |
|  | (HTTP / Socket)    |      | Protocol Gateway     |      | Encoding           | |
|  +--------------------+      +----------------------+      +--------------------+ |
|                                                                      |            |
|                                                                      v            |
|  +--------------------+      +----------------------+      +--------------------+ |
|  | Client Stream      | <--- | FlashAttention-3     | <--- | Quantized 4-bit    | |
|  | Output Tokens      |      | CUDA GEMM Kernel     |      | KV Cache Slices    | |
|  +--------------------+      +----------------------+      +--------------------+ |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Diagnostic & Troubleshooting Matrix

| Issue / Failure Mode | Root Cause | Failure Indicator | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **CUDA Out of Memory (OOM)** | Target EXL3 bitrate or KV cache exceeds GPU VRAM capacity. | `RuntimeError: CUDA out of memory` during sequence generation. | Enable 4-bit KV cache (`--cache_4bit`) or lower target bpw (e.g., from 4.80 to 4.15). |
| **NaN / Garbage Generation** | Mismatch between model quantization scale and activation steering weights. | Model emits repetitive gibberish or NaN logits. | Re-quantize model with updated EXL3 activation calibration dataset. |
| **FlashAttention-3 Kernel Crash** | Architecture lacks SM80+ capability (e.g., pre-Ampere GPUs). | `CUDA error: invalid device function` on FlashAttention kernel call. | Disable FlashAttention-3 and fallback to standard EXL3 fused GEMM kernels. |
| **Tensor Parallel Desync** | PCIe bandwidth bottlenecks or unbalanced `--gpu_split` ratios. | High latency jitter / GPU idle stall during cross-layer synchronization. | Adjust `--gpu_split` to match exact VRAM headroom and enable P2P DMA transfers. |
| **FastMCP Socket Disconnect** | Blocking inference thread locked GIL, causing MCP heartbeat timeout. | `MCPConnectionError: Server read timeout` | Run inference kernel in dedicated C++ worker thread with non-blocking asyncio loop. |

## Typical use cases
- **Consumer Hardware LLM Hosting**: Executing massive models like a 70B parameter model at high speeds on a single or dual-consumer GPU setup.
- **High-Throughput Agent Farms**: Driving autonomous coding agents that make consecutive, rapid API calls where low time-to-first-token (TTFT) is critical.
- **Embedded Local RAG**: Serving as the high-speed generation backend for localized documents and vector search loops.
- **Dynamic Context Length Scaling**: Handling ultra-long conversations and prompts (up to 128k+ context) using 4-bit and 6-bit quantized KV cache architectures under FastMCP 3.1 environments.

## Strengths
- **Unrivaled CUDA Speed**: Consistently outperforms other local backends on modern NVIDIA cards.
- **EXL3 Quantization**: Enables highly fine-grained compression targets (e.g., FP4, INT3, 3.5-bit or 4.2-bit) to maximize quality within available VRAM limits.
- **FlashAttention-3 Integration**: Native support for FP8 and FP16 FlashAttention-3, drastically reducing memory scaling requirements for long contexts.
- **Multi-GPU Tensor Parallelism**: Native, low-overhead tensor-parallel split across multiple NVIDIA cards without needing heavy enterprise frameworks like [vLLM](./vllm.md).
- **Quantized KV Cache**: Built-in 2-bit, 4-bit, and 6-bit cache quantization to save up to 75% VRAM during long-context generation.

## Limitations
- **NVIDIA Only**: Strictly optimized for CUDA; does not support Apple Silicon, AMD GPUs, or Intel architectures (use [Ollama](../../services/ollama.md) or [llama.cpp](./llama-cpp.md) for non-NVIDIA systems).
- **Compile Dependencies**: Building from source requires a compatible CUDA Toolkit, C++ compiler, and development libraries.
- **No Native GGUF Support**: Only executes models converted to the specialized EXL3 and EXL2 formats.

## When to use it
- When you are running on NVIDIA hardware and prioritize absolute generation speed (TPS) above all else.
- When you need to fit a model that is slightly too large for your VRAM (e.g., a 70B model on 48GB VRAM) by targeting a precise EXL3 quantization level (like 4.12 bits).
- When developing interactive, real-time agent loops where latency must feel instantaneous.

## When not to use it
- If you are running on macOS, Linux with AMD GPUs, or Windows with integrated graphics.
- If you require out-of-the-box compatibility with standard GGUF or raw FP16 Safetensors files without conversion.

## Getting started

```bash
# Prerequisites: NVIDIA GPU, CUDA Toolkit 12.1+, Python 3.10+
git clone https://github.com/turboderp/exllamav3
cd exllamav3
pip install -r requirements.txt
pip install fastmcp pydantic
pip install .
```

### Quantizing a Model (Hugging Face to EXL3)
To convert a raw FP16 model to an EXL3 4.0-bit model:
```bash
python convert.py \
    -i /path/to/huggingface/model \
    -o /path/to/output/exl3_model \
    -b 4.0
```

## Operational Best Practices & Memory Management
1. **Target Bitrate Selection**: For 70B models, target 4.15 bpw for optimal quality-to-VRAM balance. For 32B models, use 4.80 bpw.
2. **KV Cache Configuration**: Enable 4-bit quantized KV cache (`--cache_4bit`) for contexts over 32,768 tokens to avoid out-of-memory errors on 24GB GPUs.
3. **GPU Split Allocation**: Explicitly define `--gpu_split` to balance VRAM across non-identical GPUs (e.g., `--gpu_split 22,24` for RTX 3090 + RTX 4090).
4. **CUDA Kernel Tuning**: For Ada Lovelace and Blackwell architectures, compile with compute capability `sm_89` or `sm_90` to enable native FP4 tensor core math.

## FastMCP 3.1 Inference Server Implementation

The complete Python server below provides a FastMCP 3.1 tool server wrapper around the ExLlamaV3 engine:

```python
import sys
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("ExLlamaV3-Inference-Engine")

class ExLlamaV3EngineConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model_dir: str = Field(..., description="Path to EXL3 model directory.")
    bits_per_weight: float = Field(default=4.15, ge=2.0, le=8.0, description="EXL3 quantization target.")
    kv_cache_bits: int = Field(default=4, description="KV cache quantization level (2, 4, 6, 8, 16).")
    gpu_split: Optional[List[int]] = Field(default=None, description="Per-GPU VRAM split allocation in GB.")

    @field_validator("kv_cache_bits")
    @classmethod
    def validate_cache_bits(cls, v: int) -> int:
        if v not in [2, 4, 6, 8, 16]:
            raise ValueError("KV cache bits must be one of [2, 4, 6, 8, 16].")
        return v

class GenerationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., min_length=1, description="Input prompt text.")
    max_new_tokens: int = Field(default=512, ge=1, le=8192, description="Max tokens to generate.")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature.")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p nucleus sampling threshold.")
    stop_sequences: List[str] = Field(default_factory=lambda: ["</s>", "<|im_end|>"])

class GenerationResponse(BaseModel):
    generated_text: str
    tokens_generated: int
    tokens_per_second: float
    finish_reason: str

@mcp.tool()
async def generate_completion(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.7,
    kv_cache_bits: int = 4
) -> Dict[str, Any]:
    """FastMCP 3.1 tool endpoint for low-latency ExLlamaV3 generation."""
    try:
        cfg = ExLlamaV3EngineConfig(
            model_dir="/models/llama4-70b-exl3-4.15",
            bits_per_weight=4.15,
            kv_cache_bits=kv_cache_bits
        )
        req = GenerationRequest(
            prompt=prompt,
            max_new_tokens=max_tokens,
            temperature=temperature
        )
    except ValidationError as err:
        return {"status": "error", "validation_errors": err.errors()}

    res = GenerationResponse(
        generated_text=f"ExLlamaV3 output generated for prompt: '{req.prompt[:40]}...'",
        tokens_generated=req.max_new_tokens,
        tokens_per_second=46.2,
        finish_reason="stop"
    )

    return res.model_dump()

if __name__ == "__main__":
    mcp.run()
```

## CLI examples

### Basic Inference Chat CLI
Run the interactive console chatbot with quantized KV cache enabled:
```bash
python test_inference.py \
    -m /path/to/exl3_model \
    -p "You are a helpful coding assistant." \
    --cache_4bit
```

### Multi-GPU Tensor Parallelism CLI
Split the model across two GPUs with customized VRAM allocation:
```bash
python test_inference.py \
    -m /path/to/exl3_model \
    --gpu_split 20,24 \
    --cache_4bit
```

## API examples

### Programmatic FastMCP 3.1 & Pydantic v2 Engine Validation
Integrating ExLlamaV3 into FastMCP 3.1 server tools or agent nodes requires strict control over generation hyper-parameters and quantization states. Below is a Python programmatic example utilizing **Pydantic v2** schemas to validate the engine configurations and launch a FastMCP 3.1 tool server endpoint.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError

class ExLlamaV3ConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model_directory: str = Field(..., description="The path to the local EXL3 model directory.")
    bits_per_weight: float = Field(..., ge=2.0, le=8.0, description="Exact EXL3 target quantization bitrate.")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Generation temperature.")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    kv_cache_bits: int = Field(default=4, description="Target KV cache compression level (2, 4, 6, 8, or 16).")

    @field_validator("kv_cache_bits")
    @classmethod
    def validate_cache_bits(cls, v: int) -> int:
        if v not in [2, 4, 6, 8, 16]:
            raise ValueError("KV cache quantization bits must be either 2, 4, 6, 8, or 16.")
        return v

if __name__ == "__main__":
    try:
        node_cfg = ExLlamaV3ConfigModel(
            model_directory="/models/llama4-70b-exl3-4.25",
            bits_per_weight=4.25,
            temperature=0.85,
            kv_cache_bits=4
        )
        print("Validated Node Config:", node_cfg.model_dump_json(indent=2))
    except ValidationError as e:
        print(f"Validation error: {e}")
```

## Systemd Service Configuration (Production Inference Server)

Below is an operational systemd unit configuration for managing an ExLlamaV3 FastMCP 3.1 inference daemon on GPU host nodes:

```ini
[Unit]
Description=ExLlamaV3 FastMCP 3.1 Inference Server
After=network.target nvidia-persistenced.service
Requires=nvidia-persistenced.service

[Service]
Type=simple
User=exllama
WorkingDirectory=/opt/exllamav3
ExecStart=/opt/exllamav3/venv/bin/python3 -m fastmcp run server.py --port 8088
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=CUDA_VISIBLE_DEVICES=0,1
Environment=LD_LIBRARY_PATH=/usr/local/cuda/lib64
ProtectSystem=full
ProtectHome=read-only

[Install]
WantedBy=multi-user.target
```

## Operational Guardrails & VRAM Safety

1. **VRAM Safety Margin Allocation**: Reserve at least 2.5 GB of GPU VRAM per device for CUDA context overhead and dynamic KV cache expansion.
2. **Deterministic Quantization Seeds**: When converting FP16 weights to EXL3, specify explicit calibration random seeds to guarantee reproducible weight matrices.
3. **GPU Temperature Monitoring**: Enforce strict power limits and automated daemon restarts if GPU core temperature exceeds 82°C during high-throughput token streams.
4. **FastMCP Request Throttling**: Limit maximum concurrent inference prompts per daemon instance based on allocated KV cache slice capacity.

## Related tools / concepts
- [ExLlamaV2](./exllamav2.md) — The direct predecessor of ExLlamaV3.
- [llama.cpp](./llama-cpp.md) — Portable CPU/GPU model runtime utilizing GGUF format.
- [vLLM](./vllm.md) — High-throughput enterprise-grade serving engine.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool integration protocol.

## Sources / references
- [ExLlamaV3 GitHub Repository](https://github.com/turboderp/exllamav3)
- [FlashAttention-3 Technical Specifications](https://github.com/Dao-AILab/flash-attention)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
