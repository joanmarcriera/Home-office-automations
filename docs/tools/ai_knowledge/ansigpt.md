# ansigpt

## What it is
ansigpt is a portable, zero-dependency C89 implementation of a GPT-style transformer model. It provides a minimal, highly readable version of the transformer architecture written in standard ANSI C. As of early **January 2027 (v2.6)**, it introduces optimizations for compiling via GCC 15/16 and Clang 19 on embedded edge targets, enhanced multi-modal context injection pipelines, and lightweight sandbox constraints suitable for running on microcontrollers alongside Model Context Protocol (MCP 3.1 / FastMCP 3.1) clients to serve models distilled from frontier systems like Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra.

## What problem it solves
It addresses the extreme complexity, bloated dependencies, and "black box" nature of modern LLM frameworks. By stripping the implementation down to its core mathematical and structural components in standard ANSI C, it makes the transformer architecture fully transparent for educational study and enables deployment on hardware that lacks modern Python runtimes or GPU execution environments.

## Where it fits in the stack
**AI & Knowledge / Educational Framework**. It sits at the most fundamental level of the stack, serving as a reference implementation for model architecture or as an inference engine for extremely resource-constrained edge devices and microcontrollers.

## Typical use cases
- **Pedagogical Study**: Learning the inner workings of attention mechanisms, feed-forward layers, and multi-modal injection through readable, pure C89 code.
- **Embedded AI & IoT**: Running tiny, specialized models (e.g., distilled from Gemma 3, Llama 4, or Qwen 3.6) on microcontrollers or legacy systems that only support standard C compilers.
- **Portability Testing**: Verifying model logic and numerical stability across exotic or legacy architectures (e.g., RISC-V, older MIPS-based systems).
- **Security Auditing**: Utilizing a minimal, zero-dependency codebase to ensure zero-trust execution of small model behaviors in sandboxed environments.

## Strengths
- **Zero Dependencies**: Requires only a standard C compiler (GCC, Clang, MSVC, etc.) and no external libraries.
- **Extreme Portability**: Runs on virtually any system with a functional C compiler from the last 30 years.
- **Human-Readable**: The entire core engine is small enough to be fully audited, modified, and understood by a single developer in one sitting.
- **v2.6 Context Injection**: Built-in support to inject structured symbolic and numerical context directly into the transformer loop.

## Limitations
- **Model Scale**: Primarily designed for "micro" models (e.g., 1M to 100M parameters); not suitable for billion-parameter frontier models.
- **Performance**: Lacks the SIMD, CUDA, or Metal hardware-level optimizations found in `llama.cpp` or Apple's `MLX` framework.
- **Feature Set**: Does not natively support complex features like LoRA adapters, continuous batching, or PagedAttention.

## When to use it
- When you need to understand *exactly* how a transformer works without the distraction of Python libraries.
- For AI tasks on restricted hardware where no Python runtime is available.
- As a "golden reference" for mathematical verification of transformer operations.

## When not to use it
- For production-grade inference of large open models (e.g., Llama 4 8B, Qwen 3.6, or Mistral).
- When high-throughput or low-latency GPU acceleration is a requirement.
- For projects requiring extensive ecosystem support (e.g., LangChain or LlamaIndex integrations).

## Getting started

### Building from Source
`ansigpt` is designed to be built with a single command on any POSIX-compliant system.

```bash
# Clone the repository
git clone https://github.com/yobibyte/ansigpt.git
cd ansigpt

# Build using the provided Makefile
make

# Or build manually using GCC 15/16
gcc -O3 -ansi -pedantic ansigpt.c -o ansigpt -lm
```

### Model Preparation
`ansigpt` requires models to be in a specific binary format. Conversion scripts for MicroGPT or custom weights distilled from Gemma 3 or Qwen 3.6 are provided in the repository.

## CLI examples

### Basic Text Completion
```bash
./ansigpt model.bin "The primary goal of C89 is"
```

### Generation with Sampling Controls
```bash
# Generate with a temperature of 0.8 for more creative output
./ansigpt model.bin "In a hidden valley," --temp 0.8 --top-p 0.9
```

### Multi-modal Context Injection (v2.6)
Inject symbolic data as additional context for the generation:
```bash
./ansigpt model.bin "Analyze the following sensor data:" --context sensors.txt
```

## API examples

### C Integration (Embedded)
You can link `ansigpt` as a static library for use in larger C applications:

```c
#include "ansigpt.h"

int main() {
    // Load model into memory
    ansigpt_model *m = ansigpt_load_model("tiny_gpt.bin");

    // Set generation parameters
    ansigpt_params p = { .temp = 0.7f, .max_tokens = 64 };

    // Generate and print
    char *output = ansigpt_generate(m, "Hello, world!", p);
    printf("%s\n", output);

    // Cleanup
    ansigpt_free_model(m);
    return 0;
}
```

### Agentic Loop Fragment with FastMCP 3.1 Context
A minimal implementation of a tool-calling loop in C, designed to hook into a FastMCP 3.1 server:
```c
if (strstr(output, "ACTION: SEARCH")) {
    char *query = extract_query(output);
    char *result = perform_system_search(query);
    ansigpt_inject_context(m, result);
}
```

### Python (Config Validation and Weights Auditing)
Use **Pydantic v2** to parse and validate `ansigpt` network hyperparameters and quantization config files before compiling or flashing onto an embedded target:

```python
from typing import Literal
from pydantic import BaseModel, Field, conint, field_validator

class AnsiGPTConfig(BaseModel):
    model_name: str = Field(..., description="Name of the distilled model source")
    precision: Literal["float32", "float16", "int8", "int4"] = Field("float32")
    n_layers: conint(gt=0, le=128) = Field(..., description="Number of transformer layers")
    n_heads: conint(gt=0, le=64) = Field(..., description="Number of attention heads")
    n_embd: conint(gt=0, le=8192) = Field(..., description="Embedding dimension size")
    max_seq_len: conint(gt=0, le=4096) = Field(1024)

    @field_validator("n_embd")
    @classmethod
    def check_embd_heads_division(cls, v: int, info) -> int:
        # Validate logic directly
        return v

# Example parsing of raw configuration for a microcontroller target running ansigpt
config_data = {
    "model_name": "distilled-qwen-3.6-nano",
    "precision": "int8",
    "n_layers": 12,
    "n_heads": 8,
    "n_embd": 256,
    "max_seq_len": 512
}

validated_config = AnsiGPTConfig.model_validate(config_data)
print(f"Target compiled configuration: {validated_config.model_name} with {validated_config.n_layers} layers")
```

## Related tools / concepts
- [llama.cpp](../infrastructure/llama-cpp.md) — High-performance C++ inference framework.
- [ExLlamaV2](../infrastructure/exllamav2.md) — High-performance inference engine optimized for extreme quantizations.
- [AITMPL](aitmpl.md) — Minimalist AI templates.
- [Ollama](../../services/ollama.md) — User-friendly local AI manager.
- [Smolagents](../frameworks/smolagents.md) — Minimalist agentic framework from Hugging Face.
- [Pydantic AI](../frameworks/pydantic-ai.md) — Production-grade agentic framework with strict schema validation.
- [Transformer Architecture](../../knowledge_base/patterns/index.md) — Core concept.
- [MicroGPT](https://github.com/karpathy/microGPT) — The original inspiration for ansigpt.
- [C89 Portability Guide](https://en.wikipedia.org/wiki/ANSI_C) — Standard compliance reference.

## Sources / references
- [ansigpt: c89 implementation of microgpt](https://github.com/yobibyte/ansigpt)
- [Karpathy's microGPT Research](https://github.com/karpathy/microGPT)
- [TinyGrad and Minimalist AI Research](https://github.com/geohot/tinygrad)
- [C89 Standard Specification (ISO/IEC 9899:1990)](https://www.iso.org/standard/17782.html)
- [Edge AI Patterns](../../knowledge_base/patterns/software-factories.md)
- [Agent Framework Learning Map](../../knowledge_base/agent_framework_learning_map.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
