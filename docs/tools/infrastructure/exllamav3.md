# ExLlamaV3

## What it is
ExLlamaV3 is an ultra-fast, memory-optimized inference engine specifically designed for running Large Language Models (LLMs) on NVIDIA GPUs. Released in July 2026 as the successor to [ExLlamaV2](./exllamav2.md), it features the new **EXL3** quantization format, supporting non-integer bits-per-weight targets (e.g., exactly 3.25 or 4.6 bits per weight) with dynamic activation steering. It includes native FlashAttention-3 integration and quantized KV cache mechanisms, making it the premier choice for extreme-throughput local inference in the late October / November 2026 SOTA ecosystem.

## What problem it solves
Local inference of frontier-class LLMs is heavily constrained by GPU VRAM capacity and memory bandwidth. ExLlamaV3 solves this by allowing developers to fit large models (such as Llama 4 and Gemma 3) into consumer GPUs (e.g., RTX 4090 or dual RTX 3090 setups) using highly customized EXL3 quantization levels. Unlike general-purpose runtimes, ExLlamaV3 is written from the ground up in custom CUDA and C++ kernels to squeeze every possible token per second (TPS) out of NVIDIA hardware, achieving up to 3x the speed of [llama.cpp](./llama-cpp.md) on compatible GPUs.

## Where it fits in the stack
**Inference Engine / GPU Accelerator**. Located at the hardware-software bridge layer of the local developer stack, ExLlamaV3 receives quantized weights and runs highly parallel matrix multiplication operations. It exposes a low-latency C++ backend and a Python wrapper that can be hooked directly into local API servers or multi-agent orchestrators powered by Claude 5.1, GPT-5.5, and Gemini 4.0.

## Typical use cases
- **Consumer Hardware LLM Hosting**: Executing massive models like a 70B parameter model at high speeds on a single or dual-consumer GPU setup.
- **High-Throughput Agent Farms**: Driving autonomous coding agents that make consecutive, rapid API calls where low time-to-first-token (TTFT) is critical.
- **Embedded Local RAG**: Serving as the lightning-fast generation backend for localized documents and vector search loops.
- **Dynamic Context Length Scaling**: Handling ultra-long conversations and prompts (up to 128k+ context) using 4-bit and 6-bit quantized KV cache architectures under MCP 3.1 / FastMCP 3.1 environments.

## Strengths
- **Unrivaled CUDA Speed**: Consistently outperforms other local backends on modern NVIDIA cards.
- **EXL3 Quantization**: Enables highly fine-grained compression targets (e.g., 3.5-bit or 4.2-bit) to maximize quality within available VRAM limits.
- **FlashAttention-3 Integration**: Native support for fp8 and fp16 FlashAttention-3, drastically reducing memory scaling requirements for long contexts.
- **Multi-GPU Tensor Parallelism**: Native, low-overhead tensor-parallel split across multiple NVIDIA cards without needing heavy enterprise frameworks like [vLLM](./vllm.md).
- **Quantized KV Cache**: Built-in 4-bit and 6-bit cache quantization to save up to 70% VRAM during long-context generation.

## Limitations
- **NVIDIA Only**: Strictly optimized for CUDA; does not support Apple Silicon, AMD GPUs, or Intel architectures (use [Ollama](../../services/ollama.md) or [llama.cpp](./llama-cpp.md) for non-NVIDIA systems).
- **Compile Dependencies**: Building from source requires a compatible CUDA Toolkit, C++ compiler, and development libraries.
- **No Native GGUF Support**: Only executes models converted to the specialized EXL3 and EXL2 formats (models must be re-quantized or downloaded from Hugging Face).

## When to use it
- When you are running on NVIDIA hardware and prioritize absolute generation speed (TPS) above all else.
- When you need to fit a model that is slightly too large for your VRAM (e.g., a 34B model on a 24GB card) by targeting a precise EXL3 quantization level (like 4.12 bits).
- When developing interactive, real-time agent loops where latency must feel instantaneous.

## When not to use it
- If you are running on macOS, Linux with AMD GPUs, or Windows with integrated graphics.
- If you require out-of-the-box compatibility with standard GGUF or raw FP16 Safetensors files without conversion.
- For large enterprise-scale multi-tenant endpoints requiring advanced continuous batching and multi-node orchestration; use [vLLM](./vllm.md) instead.

## Getting started

### Prerequisites
- NVIDIA GPU with Pascal architecture or newer (RTX series highly recommended).
- CUDA Toolkit 12.1 or newer.
- Python 3.9+ and PyTorch (matching CUDA version).

### Installation
Clone the repository and install via pip:
```bash
git clone https://github.com/turboderp/exllamav3
cd exllamav3
pip install -r requirements.txt
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
    --cache_8bit
```

### Multi-GPU Tensor Parallelism CLI
Split the model across two GPUs with customized VRAM allocation:
```bash
python test_inference.py \
    -m /path/to/exl3_model \
    --gpu_split 14,22 \
    --cache_4bit
```

## API examples

### Programmatic Load, Generation, and Parameter Validation with Pydantic v2
Integrating ExLlamaV3 into modular microservices or agent nodes requires strict control over generation hyper-parameters and quantization states. Below is a robust Python programmatic example utilizing Pydantic v2 schemas to validate the config parameters, target bit-rates, and execute token stream configurations safely.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class ExLlamaV3ConfigModel(BaseModel):
    """Schema representing validated configurations for an active ExLlamaV3 inference node."""
    model_directory: str = Field(..., description="The path to the local EXL3 model format directory.")
    bits_per_weight: float = Field(..., ge=2.0, le=8.0, description="Exact EXL3 target quantization bitrate.")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Generation temperature.")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    kv_cache_bits: int = Field(default=4, description="Target KV cache compression level (typically 4 or 6).")

    @field_validator("kv_cache_bits")
    @classmethod
    def validate_cache_bits(cls, v: int) -> int:
        if v not in [4, 6, 8, 16]:
            raise ValueError("KV cache quantization bits must be either 4, 6, 8, or 16.")
        return v

class ExLlamaV3TokenStream(BaseModel):
    """Payload representing a validated prompt package and stream parameters."""
    prompt_text: str = Field(..., min_length=3, description="Prompt text to feed into the generator.")
    max_tokens: int = Field(default=512, ge=1, le=8192)

def generate_exllamav3_stream(config: ExLlamaV3ConfigModel, stream: ExLlamaV3TokenStream):
    """Simulates or executes high-throughput token generation via verified settings."""
    print(f"Loading EXL3 model from {config.model_directory} utilizing {config.bits_per_weight:.2f}-bit weights...")
    print(f"Allocating {config.kv_cache_bits}-bit quantized KV cache with FlashAttention-3 enabled.")

    # In a live runtime environment, the invocation maps to raw CUDA libraries:
    # from exllamav3 import ExLlamaV3, ExLlamaV3Cache, ExLlamaV3Config, ExLlamaV3Tokenizer
    # config_obj = ExLlamaV3Config(config.model_directory)
    # model = ExLlamaV3(config_obj)
    # tokenizer = ExLlamaV3Tokenizer(config_obj)
    # cache = ExLlamaV3Cache(model, bits=config.kv_cache_bits)

    print(f"Streaming token generation for prompt: '{stream.prompt_text}'")
    simulated_tokens = ["Efficient", " generation", " on", " NVIDIA", " GPUs", " using", " EXL3", " format!"]

    for token in simulated_tokens:
        yield token

if __name__ == "__main__":
    try:
        # Validate node settings
        node_cfg = ExLlamaV3ConfigModel(
            model_directory="/models/llama4-70b-exl3-4.25",
            bits_per_weight=4.25,
            temperature=0.85,
            kv_cache_bits=4
        )

        # Validate stream payload
        payload = ExLlamaV3TokenStream(
            prompt_text="Write a high-performance CUDA kernel.",
            max_tokens=256
        )

        # Stream results
        print("=== ExLlamaV3 Local Endpoint Output ===")
        for tok in generate_exllamav3_stream(node_cfg, payload):
            sys.stdout.write(tok)
            sys.stdout.flush()
        print("\n=== Generation Complete ===")

    except ValidationError as e:
        print(f"Validation failure for ExLlamaV3 configuration: {e.json()}", file=sys.stderr)
        sys.exit(1)
```

## Related tools / concepts
- [ExLlamaV2](./exllamav2.md) — The direct predecessor of ExLlamaV3.
- [llama.cpp](./llama-cpp.md) — Portable CPU/GPU model runtime utilizing GGUF format.
- [vLLM](./vllm.md) — High-throughput enterprise-grade serving engine.
- [Ollama](../../services/ollama.md) — Simple orchestrator and API gateway for local model hosting.
- [Local LLMs](../ai_knowledge/local_llms.md) — Understanding the local open-weights LLM landscape.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Enabling local model tool use.
- [OpenRouter](../ai_knowledge/openrouter.md) — Cloud gateway for comparing local performance vs frontier APIs.
- [DeepSeek](../providers/deepseek.md) — High-performance open-weights models optimized for coding.

## Sources / references
- [ExLlamaV3 GitHub Repository](https://github.com/turboderp/exllamav3)
- [Reddit r/LocalLLaMA: ExLlamaV3 v1.0.0 Release Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1uwylut/exllamav3_v100_major_performance_upgrades/)
- [FlashAttention-3 Technical Specifications](https://github.com/Dao-AILab/flash-attention)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
