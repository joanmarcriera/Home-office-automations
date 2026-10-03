# ansigpt

## What it is
ansigpt is a portable, zero-dependency C89 implementation of a GPT-style transformer model. It provides a minimal, highly readable version of the transformer architecture written in standard ANSI C (ISO/IEC 9899:1990). As of early **January 2027 (v2.6)**, it introduces optimizations for compiling via GCC 15/16 and Clang 19 on embedded edge targets, enhanced multi-modal context injection pipelines, and lightweight sandbox constraints suitable for running on microcontrollers alongside Model Context Protocol (MCP 3.1 / FastMCP 3.1) clients to serve models distilled from frontier systems like Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra.

```
+-----------------------------------------------------------------------------------+
|                            AnsiGPT Embedded Runtime Architecture                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Host Application / Embedded Firmware ]                                         |
|        |                                                                          |
|        v                                                                          |
|  +-----------------------------------------------------------------------------+  |
|  | C89 Transformer Execution Core (ansigpt.c / ansigpt.h)                     |  |
|  |                                                                             |  |
|  |  +------------------+     +------------------+     +---------------------+  |  |
|  |  | Token Embedding  | --> | Multi-Head Self- | --> | Feed-Forward Network|  |  |  |
|  |  | Matrix & Pos-Enc |     | Attention (Q,K,V)|     | (GELU / SwiGLU)     |  |  |  |
|  |  +------------------+     +------------------+     +---------------------+  |  |
|  |                            ^                             |                  |  |
|  |                            | (Context Injection Window)  |                  |  |
|  |                            +-----------------------------+                  |  |
|  |                                                                             |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | Static Memory Pool & Tensor Buffer Allocation (Zero Malloc Runtime)   |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|        |                                                                          |
|        v                                                                          |
|  [ FastMCP 3.1 C-Bridge / Direct Microcontroller IPC ]                            |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It addresses the extreme complexity, bloated dependencies, and "black box" nature of modern LLM frameworks. By stripping the implementation down to its core mathematical and structural components in standard ANSI C, it makes the transformer architecture fully transparent for educational study and enables deployment on hardware that lacks modern Python runtimes, C++20 toolchains, or GPU execution environments.

In industrial and microcontroller contexts (e.g., ARM Cortex-M4/M7, ESP32-S3, RISC-V RV32IMAC), running traditional AI runtime stacks is impossible due to strict RAM constraints and lack of POSIX dynamic memory allocation. `ansigpt` bypasses these restrictions by providing static array tensor operations, deterministic memory footprints, and raw pointer arithmetic that compiles down to pure machine code on virtually any architecture.

## Where it fits in the stack
**AI & Knowledge / Educational Framework & Embedded Edge AI Engine**. It sits at the most fundamental level of the stack, serving as a reference implementation for model architecture, an audit benchmark for neural network tensor math, or an inference engine for extremely resource-constrained edge devices and microcontrollers operating in air-gapped environments.

## Typical use cases
- **Pedagogical Study & Compiler Design**: Learning the inner workings of attention mechanisms, feed-forward layers, positional encoding, and multi-modal injection through readable, pure C89 code.
- **Embedded AI & IoT Sensing**: Running tiny, specialized models (e.g., distilled from Gemma 3, Llama 4, or Qwen 3.6) on microcontrollers or legacy systems that only support standard C compilers.
- **Portability Testing & Hardware Verification**: Verifying model logic and numerical stability across exotic or legacy architectures (e.g., RISC-V, older MIPS-based systems, SPARC, or Motorola 68k).
- **Security Auditing & Zero-Trust Execution**: Utilizing a minimal, zero-dependency codebase to ensure zero-trust execution of small model behaviors in sandboxed environments without risk of third-party package supply-chain contamination.
- **FastMCP 3.1 Microcontroller Bridge**: Exposing low-level sensor anomaly classification or embedded text generation directly as an MCP tool endpoint over UART or SPI bus.

## Strengths
- **Zero Dependencies**: Requires only a standard C compiler (`gcc`, `clang`, `msvc`, `tcc`, or legacy C compilers) and `math.lib` (`-lm`) with no external dependencies or dynamic link requirements.
- **Extreme Portability**: Runs on virtually any system with a functional C compiler from the last 35 years, complying strictly with ISO/IEC 9899:1990 (C89/C90).
- **Deterministic Static Memory**: Supports compilation modes with zero runtime dynamic memory allocation (`malloc`/`free`), eliminating memory fragmentation issues on real-time operating systems (RTOS).
- **Human-Readable Core**: The entire core inference engine is contained within a single compact source file, making it audit-ready and easily customizable by a single developer.
- **v2.6 Context Injection Pipeline**: Built-in support to inject structured symbolic and numerical context directly into the transformer attention window prior to token generation.

## Limitations
- **Model Scale Limitations**: Primarily designed for "micro" models (e.g., 100K to 100M parameters); not suitable for billion-parameter frontier models due to single-threaded CPU bottleneck.
- **Hardware Acceleration**: Lacks native CUDA, ROCm, or AVX-512 SIMD assembly optimizations found in `llama.cpp` or Apple's `MLX` framework.
- **Feature Set Truncation**: Does not natively support advanced quantization algorithms like AWQ or EXL2, dynamic KV-cache page indexing (PagedAttention), or multi-GPU pipeline parallelism.

## When to use it
- When you need to understand *exactly* how a transformer works without the abstraction layer of Python, PyTorch, or complex C++ classes.
- For AI tasks on bare-metal hardware or microcontrollers where no Python runtime or modern OS kernel is available.
- As a "golden reference" for mathematical verification and numerical correctness testing of transformer operations across custom silicon platforms.
- For air-gapped embedded systems that require strict security compliance and static code auditing.

## When not to use it
- For production-grade inference of large open models (e.g., Llama 4 8B/70B, Qwen 3.6 72B, or Mistral Small).
- When high-throughput or sub-millisecond low-latency GPU acceleration is mandatory for concurrent multi-user workloads.
- For projects requiring extensive ecosystem integration with frameworks like LangChain, AutoGen, or LlamaIndex without writing custom C or FastMCP adapters.

## Getting started

### Building from Source
`ansigpt` is designed to be built with a single command on any POSIX-compliant or Windows system.

```bash
# Clone the repository
git clone https://github.com/yobibyte/ansigpt.git
cd ansigpt

# Build using the provided Makefile
make

# Or compile manually using GCC with strict C89 flags
gcc -O3 -ansi -pedantic -Wall -Wextra ansigpt.c -o ansigpt -lm
```

### Static Bare-Metal Build
For bare-metal microcontrollers (e.g., ARM Cortex-M4 via `arm-none-eabi-gcc`):

```bash
arm-none-eabi-gcc -O2 -ansi -pedantic \
  -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 \
  -DANSIGPT_STATIC_ALLOC -DANSIGPT_NO_STDIO \
  -c ansigpt.c -o ansigpt.o
```

### Model Weight Preparation
`ansigpt` reads raw binary weight matrices formatted in standard float32 or int8 structures. Conversion scripts for PyTorch checkpoints, MicroGPT, or custom weights distilled from Gemma 3, Qwen 3.6, or Llama 4 are provided in the python utilities directory.

```bash
# Convert a HuggingFace Micro-Transformer model to binary format
python3 scripts/export_weights.py \
  --model Qwen/Qwen3.6-0.5B-Instruct \
  --output tiny_model.bin \
  --quantize int8
```

## CLI examples

### Basic Text Completion
```bash
./ansigpt model.bin "The primary goal of C89 standard compliance is"
```

### Sampling Control & Generation Parameters
```bash
# Generate text with custom temperature, top-p, and max token limits
./ansigpt model.bin "In embedded computing, deterministic timing means" \
  --temp 0.7 \
  --top-p 0.85 \
  --max-tokens 128 \
  --seed 42
```

### Structured Context Injection (v2.6)
Inject real-time telemetry or sensor output prior to prompt evaluation:
```bash
# Pass external telemetry stream as direct transformer context
./ansigpt model.bin "Analyze system health metrics:" \
  --context telemetry_buffer.txt \
  --temp 0.2
```

### Interactive REPL Mode
```bash
# Launch interactive REPL for edge diagnostic terminal
./ansigpt model.bin --interactive
```

## API examples

### Native C Integration (Embedded / Bare-Metal)
You can link `ansigpt` as a static library into microcontrollers, real-time operating systems (FreeRTOS, Zephyr), or enterprise C applications:

```c
#include <stdio.h>
#include <stdlib.h>
#include "ansigpt.h"

int main(void) {
    /* Initialize static memory parameters */
    ansigpt_config cfg;
    ansigpt_model *m;
    ansigpt_params p;
    char *output;

    /* Populate model configuration struct */
    cfg.n_layers = 6;
    cfg.n_heads = 4;
    cfg.n_embd = 128;
    cfg.vocab_size = 32000;
    cfg.max_seq_len = 256;

    /* Load model weights from static binary file or flash memory */
    m = ansigpt_load_model("tiny_gpt.bin", &cfg);
    if (!m) {
        fprintf(stderr, "Failed to load model binary.\n");
        return 1;
    }

    /* Configure generation parameter parameters */
    p.temp = 0.6f;
    p.top_p = 0.9f;
    p.max_tokens = 64;
    p.seed = 1337;

    /* Execute transformer forward pass and generation */
    output = ansigpt_generate(m, "System status check:", &p);
    if (output) {
        printf("AnsiGPT Output:\n%s\n", output);
        free(output);
    }

    /* Free allocated resources */
    ansigpt_free_model(m);
    return 0;
}
```

### C FastMCP 3.1 Agentic Tool Server
Below is an operational FastMCP 3.1 tool integration wrapper written in C that binds an `ansigpt` embedded engine into an agentic tool handler over standard IPC channels:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "ansigpt.h"

/* FastMCP 3.1 JSON-RPC Request Handler for Embedded AnsiGPT */
void handle_fastmcp_request(const char *json_payload, ansigpt_model *model) {
    if (strstr(json_payload, "tools/call") && strstr(json_payload, "run_inference")) {
        ansigpt_params p;
        p.temp = 0.3f;
        p.top_p = 0.9f;
        p.max_tokens = 48;
        p.seed = 100;

        /* Extract query payload (simplified string extraction for ANSI C) */
        const char *prompt_start = strstr(json_payload, "\"prompt\":");
        char prompt[256] = "Evaluate sensor anomaly";
        if (prompt_start) {
            sscanf(prompt_start, "\"prompt\":\"%255[^\"]\"", prompt);
        }

        /* Execute AnsiGPT inference engine */
        char *response = ansigpt_generate(model, prompt, &p);

        /* Return FastMCP 3.1 compliant JSON-RPC response */
        printf("{\"jsonrpc\":\"2.0\",\"result\":{\"content\":[{\"type\":\"text\",\"text\":\"%s\"}]},\"id\":1}\n",
               response ? response : "Inference error");

        if (response) free(response);
        fflush(stdout);
    }
}
```

### Python (Pydantic v2 Weights Verification & Config Audit)
Use **Pydantic v2** to parse, validate, and verify `ansigpt` model hyperparameters and hardware targets prior to flashing binaries onto microcontrollers:

```python
from typing import Literal, Optional, List
from pydantic import BaseModel, Field, conint, field_validator, ValidationInfo

class HardwareTarget(BaseModel):
    arch: Literal["cortex-m4", "cortex-m7", "esp32s3", "riscv32", "x86_64_posix"] = Field(...)
    available_sram_kb: int = Field(..., ge=16, le=1048576)
    has_fpu: bool = Field(True, description="Hardware Floating Point Unit available")

class AnsiGPTConfig(BaseModel):
    model_name: str = Field(..., description="Name of distilled source model")
    precision: Literal["float32", "int8", "int4"] = Field("int8")
    n_layers: conint(gt=0, le=32) = Field(..., description="Number of transformer layers")
    n_heads: conint(gt=0, le=32) = Field(..., description="Number of attention heads")
    n_embd: conint(gt=0, le=2048) = Field(..., description="Embedding vector dimension")
    max_seq_len: conint(gt=0, le=2048) = Field(512, description="Maximum sequence context length")
    vocab_size: int = Field(32000, description="Tokenizer vocabulary size")
    hardware: HardwareTarget

    @field_validator("n_embd")
    @classmethod
    def validate_embd_heads(cls, v: int, info: ValidationInfo) -> int:
        if "n_heads" in info.data and v % info.data["n_heads"] != 0:
            raise ValueError(f"n_embd ({v}) must be evenly divisible by n_heads ({info.data['n_heads']})")
        return v

    def calculate_estimated_ram_kb(self) -> float:
        # Calculate memory requirements for weights and KV cache
        bytes_per_param = 4 if self.precision == "float32" else 1
        param_count = (self.n_layers * 12 * self.n_embd * self.n_embd) + (self.vocab_size * self.n_embd)
        kv_cache_bytes = 2 * self.n_layers * self.max_seq_len * self.n_embd * 4
        total_bytes = (param_count * bytes_per_param) + kv_cache_bytes
        return round(total_bytes / 1024.0, 2)

# Audit configuration for an ESP32-S3 microcontroller target
target_hardware = HardwareTarget(arch="esp32s3", available_sram_kb=512, has_fpu=True)

config = AnsiGPTConfig(
    model_name="qwen3.6-0.5b-distilled-nano",
    precision="int8",
    n_layers=8,
    n_heads=8,
    n_embd=256,
    max_seq_len=256,
    vocab_size=16000,
    hardware=target_hardware
)

ram_req = config.calculate_estimated_ram_kb()
print(f"Validated AnsiGPT Model Configuration: {config.model_name}")
print(f"Estimated RAM footprint: {ram_req} KB (Target available: {config.hardware.available_sram_kb} KB)")
assert ram_req <= config.hardware.available_sram_kb, "Model RAM footprint exceeds available target memory!"
```

## Related tools / concepts
- [llama.cpp](../infrastructure/llama-cpp.md) — High-performance C++ inference framework with SIMD and GPU acceleration.
- [ExLlamaV2](../infrastructure/exllamav2.md) — Extreme performance local inference engine optimized for GPTQ/EXL2 quantizations.
- [AITMPL](aitmpl.md) — Minimalist AI templates and boilerplate configurations.
- [Ollama](../../services/ollama.md) — User-friendly local LLM service and model manager.
- [Smolagents](../frameworks/smolagents.md) — Minimalist agentic framework from Hugging Face.
- [Pydantic AI](../frameworks/pydantic-ai.md) — Production-grade agentic framework with strict schema validation.
- [Local LLMs](local_llms.md) — Guide to running open weights models locally.
- [MicroGPT](microgpt.md) — The original minimalist educational model implementation by Andrej Karpathy.

## Sources / references
- [ansigpt GitHub Repository](https://github.com/yobibyte/ansigpt)
- [Karpathy's microGPT Research](https://github.com/karpathy/microGPT)
- [TinyGrad Minimalist Machine Learning Framework](https://github.com/geohot/tinygrad)
- [ISO/IEC 9899:1990 C89 Language Standard Specification](https://www.iso.org/standard/17782.html)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/specification/2026-03-31)
- [Edge AI Patterns in Embedded Systems](../../knowledge_base/patterns/software-factories.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
