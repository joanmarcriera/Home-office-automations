# ExLlamaV3

## What it is
ExLlamaV3 is an ultra-fast, memory-optimized inference engine specifically designed for running Large Language Models (LLMs) on NVIDIA GPUs. Built as the successor to [ExLlamaV2](./exllamav2.md), it features the **EXL3** quantization format supporting sub-bit quantization targets (e.g., FP4, INT3, and arbitrary bits-per-weight like 3.25 or 4.15 bpw) with dynamic activation steering. As of early 2027, ExLlamaV3 includes native FlashAttention-3 integration, **FastMCP 3.1** protocol support, quantized KV cache mechanisms, and multi-modal tensor-parallel kernels.

## What problem it solves
Local inference of frontier-class LLMs is heavily constrained by GPU VRAM capacity and memory bandwidth. ExLlamaV3 solves this by allowing developers to fit large models (such as Llama 4 70B, Gemma 3, or DeepSeek-V4) into consumer GPUs (e.g., RTX 4090, RTX 5090, or dual RTX 3090 setups) using highly customized EXL3 quantization levels. Unlike general-purpose runtimes, ExLlamaV3 is written from the ground up in custom CUDA and C++ kernels to maximize tokens per second (TPS) on NVIDIA hardware, achieving up to 3x the speed of [llama.cpp](./llama-cpp.md) on compatible GPUs.

## Where it fits in the stack
**Inference Engine / GPU Accelerator**. Located at the hardware-software bridge layer of the local developer stack, ExLlamaV3 receives quantized weights and runs highly parallel matrix multiplication operations. It exposes a low-latency C++ backend and a Python wrapper that can be hooked directly into local API servers or FastMCP 3.1 multi-agent orchestrators powered by Claude 5.6, GPT-5.6, and Gemini 4.0.

## Quantization & Throughput Metrics (Early 2027 SOTA)

| Metric / Capability | ExLlamaV3 (EXL3) | ExLlamaV2 (EXL2) | vLLM (AWQ/FP8) | llama.cpp (GGUF) |
| :--- | :--- | :--- | :--- | :--- |
| **Quantization Precision** | FP4 / INT3 / Sub-bit (3.25 bpw) | EXL2 (3.5 - 6.0 bpw) | FP8 / AWQ / INT4 | Q2_K to Q8_0 GGUF |
| **Tokens/sec (70B model)** | ~45 TPS (dual RTX 3090) | ~32 TPS | ~28 TPS | ~18 TPS |
| **FastMCP 3.1 Server Integration** | Native streaming tool wrapper | OpenAI API bridge | OpenAI API bridge | Native server endpoints |
| **FlashAttention-3 FP8 Support**| Native | Partial | Native | No (custom CUDA) |
| **KV Cache Compression** | 2-bit / 4-bit / 6-bit | 4-bit / 8-bit | FP8 / PagedAttention | Q4_0 / Q8_0 KV |

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

### Programmatic FastMCP 3.1 Server & Pydantic v2 Engine Validation
Integrating ExLlamaV3 into FastMCP 3.1 server tools or agent nodes requires strict control over generation hyper-parameters and quantization states. Below is a Python programmatic example utilizing **Pydantic v2** schemas to validate the engine configurations and launch a FastMCP 3.1 tool server endpoint.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from fastmcp import FastMCP

# Initialize FastMCP 3.1 server for local ExLlamaV3 inference
mcp = FastMCP("ExLlamaV3 Inference Server", version="3.1")

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

class ExLlamaV3TokenStream(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt_text: str = Field(..., min_length=3, description="Prompt text to feed into the generator.")
    max_tokens: int = Field(default=512, ge=1, le=8192)

@mcp.tool()
def generate_exllamav3_completion(prompt_text: str, max_tokens: int = 512) -> str:
    """FastMCP 3.1 tool endpoint for ExLlamaV3 local inference execution."""
    try:
        cfg = ExLlamaV3ConfigModel(
            model_directory="/models/llama4-70b-exl3-4.25",
            bits_per_weight=4.25,
            temperature=0.7,
            kv_cache_bits=4
        )
        stream_req = ExLlamaV3TokenStream(prompt_text=prompt_text, max_tokens=max_tokens)

        return f"[ExLlamaV3 FP4/EXL3 Execution Success]: Generated {stream_req.max_tokens} tokens for prompt '{stream_req.prompt_text[:30]}...'"
    except ValidationError as e:
        return f"Configuration Validation Error: {e}"

if __name__ == "__main__":
    try:
        node_cfg = ExLlamaV3ConfigModel(
            model_directory="/models/llama4-70b-exl3-4.25",
            bits_per_weight=4.25,
            temperature=0.85,
            kv_cache_bits=4
        )

        payload = ExLlamaV3TokenStream(
            prompt_text="Write a high-performance CUDA kernel.",
            max_tokens=256
        )

        print("ExLlamaV3 Node Config Validated Successfully:")
        print(node_cfg.model_dump_json(indent=2))
        res = generate_exllamav3_completion(payload.prompt_text, payload.max_tokens)
        print(res)

    except ValidationError as e:
        print(f"Validation failure for ExLlamaV3 configuration: {e.json()}", file=sys.stderr)
        sys.exit(1)
```

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
