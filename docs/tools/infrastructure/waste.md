# WASTE

## What it is
WASTE (Weight-Aware Streaming Tensor Engine) is a dependency-free, embeddable C inference engine designed by the SQLite AI organization. It is engineered specifically to run massive MoE models—such as the 2.78-trillion-parameter Kimi K3 model—on standard consumer laptops and workstations with severely restricted memory configurations (e.g., 64 GB of RAM), by streaming activated parameter weights dynamically from an internal NVMe SSD directly into memory.

## What problem it solves
Large language models like Kimi K3 are typically locked behind proprietary cloud APIs because running their trillion-parameter checkpoint requires multi-GPU server nodes costing tens of thousands of dollars. Local loaders like llama.cpp normally require keeping the entire quantized model materialized in system VRAM/RAM, resulting in out-of-memory errors on consumer machines. WASTE solves this by only keeping the shared model core and the active KV cache resident in RAM while streaming the dynamically routed mixture-of-experts parameters from the NVMe SSD on-the-fly, reducing the memory floor to as low as ~29 GB.

## Where it fits in the stack
**Category**: Infrastructure / Inference Engine. WASTE sits in the local-first serving layer, competing with runtimes like [llama.cpp](llama-cpp.md), [MLX](mlx.md), and [Turbo-fieldfare](turbo-fieldfare.md) (which uses a similar expert streaming logic).

## Typical use cases
- **Massive-Model Local Prototyping**: Running a full 2.78-trillion-parameter Kimi K3 reasoning model locally on a 64 GB workstation.
- **Privacy-First Large Scale Reasoning**: Evaluating massive codebases or highly sensitive data sets with a trillion-parameter model without sharing data with public clouds.
- **Embedded C Inference**: Integrating a high-performance, lightweight C library directly into local native binaries.

## Strengths
- **Incredible VRAM/RAM Savings**: Lowers the physical RAM floor for Kimi K3 from 1.4 TB to approximately 29 GB.
- **Zero External Dependencies**: Built as a pure C11 library with no reliance on heavy AI libraries, BLAS backends, Python runtimes, or CUDA packages for CPU-based execution.
- **Multimodal Support**: Native support for multimodal vision workloads, allowing combined text and image reasoning out-of-the-box.
- **SQLite Philosophy**: Packaged as a clean, embeddable, single-header style library with a robust internal testing suite.

## Limitations
- **SSD I/O Bound**: Inference speed is strongly bound to SSD read performance; running on slower external drives or SATA SSDs will cause significant latency.
- **Conversion Overhead**: Requires converting native PyTorch/Hugging Face Safetensors weights into its optimized `.waste` streaming file format.
- **CPU-First Bottleneck**: Standard paths are highly optimized for CPU thread scaling, meaning massive token-generation throughput is hardware-bounded compared to dedicated GPU clusters.

## When to use it
- When you want to run Kimi K3 or massive mixture-of-expert models locally but your machine only has 64 GB of RAM.
- When you need a dependency-free C library to embed within a native desktop application.

## When not to use it
- If your system has sufficient enterprise GPU memory (e.g., 8x H100) to host the full model resident in VRAM (use [vLLM](vllm.md) or [SGLang](sglang.md) for maximum throughput).
- For smaller models (under 14B parameters) where keeping the entire checkpoint resident in RAM/VRAM via [Ollama](../../services/ollama.md) or [MLX](mlx.md) is much faster.

## Getting started

### Requirements
- A modern C11 compliant compiler and `make`
- Apple Silicon Mac or Linux workstation
- Fast internal NVMe SSD with at least 1 TB of free space (for full Kimi K3 weights)
- Recommended: At least 64 GB of RAM (hard minimum floor is 29.06 GB at 4k context)

### Installation
Clone the repository and compile the native CLI tool:

```bash
git clone https://github.com/sqliteai/waste.git
cd waste
make
make check
```
The `make check` command runs a model-free synthetic verification test suite to ensure the compilation was successful.

## CLI examples

### Running local inference
Run text completion using a compiled `.waste` model file:

```bash
./waste run ~/models/k3.waste "Prove the Riemann hypothesis step by step."
```

### Multimodal Vision Prompting
Run image-to-text queries by passing one or more images:

```bash
./waste run ~/models/k3.waste "Explain the chart in this image" --image chart.png
```

## API examples

### Programmatic Python Interface
The following Python script starts a local `.waste` server container and queries it, validating the structured completion payload utilizing **Pydantic v2**.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field
import requests

# Define Pydantic v2 validation schema
class TextResponse(BaseModel):
    id: str
    content: str = Field(..., description="The completed text stream")
    tokens_evaluated: int
    tok_per_sec: float

class WasteGenerationResult(BaseModel):
    model_name: str
    status: str
    results: List[TextResponse]

def query_waste_engine(prompt: str, url: str = "http://localhost:9091/generate") -> Optional[str]:
    payload = {
        "prompt": prompt,
        "max_new_tokens": 128,
        "temperature": 0.2
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        # Validate output against our Pydantic v2 schemas
        validated = WasteGenerationResult.model_validate(response.json())
        return validated.results[0].content

    except Exception as e:
        print(f"Error querying local WASTE engine API: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initiating local sqliteai/waste validation...")
    out = query_waste_engine("Explain the prime number theorem.")
    if out:
        print(f"Validation successful! Output:\n{out}")
    else:
        print("WASTE inference server is offline. Skipping integration run.")
```

## Related tools / concepts
- [vLLM](vllm.md) — SOTA enterprise high-throughput serving engine.
- [Aphrodite Engine](aphrodite-engine.md) — Memory-efficient vLLM loader.
- [llama.cpp](llama-cpp.md) — The global standard for GGUF-based local inference.
- [MLX](mlx.md) — Native Apple Silicon machine learning execution framework.
- [Turbo-fieldfare](turbo-fieldfare.md) — Expert-streaming Swift loader for Gemma 4.
- [SGLang](sglang.md) — High-concurrency engine for advanced agentic operations.
- [Ollama](../../services/ollama.md) — Simplified model container and manager.
- [ExLlamaV2](exllamav2.md) — SOTA local GPU engine for dense models.

## Sources / references
- [sqliteai/waste GitHub Repository](https://github.com/sqliteai/waste)
- [Reddit r/LocalLLaMA: WASTE engine release discussion](https://www.reddit.com/r/LocalLLaMA/comments/1vdy1nd/github_sqliteaiwaste_run_the_full/)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
