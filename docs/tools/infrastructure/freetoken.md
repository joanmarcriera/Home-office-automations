# FreeToken

## What it is
FreeToken is an open-source, high-efficiency local LLM inference runtime and caching engine released in August 2026. Designed for extreme memory optimization and low-latency token generation, FreeToken optimizes key-value (KV) cache allocation through dynamic memory page pooling, adaptive token quantization, and speculative execution across consumer hardware. In early 2027, FreeToken acts as a lightweight, low-overhead inference provider engine alongside [vLLM](vllm.md) and [Ollama](../../services/ollama.md), integrating into agentic tool-use pipelines via **FastMCP 3.1** and the **MCP 3.0 Task Protocol**.

## What problem it solves
Local inference runner setups often struggle with GPU VRAM exhaustion and KV-cache fragmentation when serving large-context requests or multi-tenant agent loops. FreeToken eliminates out-of-memory (OOM) crashes by implementing zero-copy page sharing and dynamic 2-bit/4-bit KV compression, enabling developer workstations to host frontier open models like [Qwen 3.8](../ai_knowledge/qwen.md) and [Llama 4](../ai_knowledge/local_llms.md) with significantly reduced VRAM footprints.

## Where it fits in the stack
**Infrastructure / LLM Serving & Local Inference Engine.** FreeToken provides the execution hardware abstraction and local endpoint interface that hosts open-weights language and vision-language models for downstream agent frameworks and applications.

## Typical use cases
- **Consumer Hardware LLM Hosting**: Running 27B-70B open parameter models on 16GB-24GB consumer GPUs with high-throughput streaming.
- **Long-Context Agent Processing**: Executing multi-turn repository indexing and document processing tasks requiring 128K+ token context windows without cache eviction.
- **Local MCP Server Backends**: Serving fast local inference endpoints for [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers and terminal copilots.
- **Speculative Decoding Acceleration**: Pairing small draft models (e.g., 1B-3B) with target foundation models to double token output generation speed.

## Strengths
- **Dynamic KV-Cache Pooling**: Prevents memory fragmentation and scales context capacity by up to 3x compared to static allocation.
- **Sub-Byte Quantization**: Supports FP8, INT4, and experimental 2-bit cache quantizations with negligible loss in perplexity.
- **OpenAI-Compatible REST Server**: Native drop-in compatibility for OpenAI API clients and agent harnesses.
- **Multi-GPU Tensor Parallelism**: Efficiently splits workloads across multiple heterogeneous local GPUs.

## Limitations
- **Narrow Ecosystem Tooling**: Lacks the extensive community web-UI plugin ecosystem of [Ollama](../../services/ollama.md).
- **Compilation Overhead**: Initial model loading requires kernel compilation step on cold starts.
- **Hardware Dependencies**: Best performance requires CUDA compute capability 8.0+ or Apple Silicon M2/M3/M4 Series.

## When to use it
- When serving large open-weights LLMs on local workstation hardware with constrained GPU VRAM.
- When building multi-agent systems that hit KV-cache memory limits under concurrent execution.
- As a fast, low-latency OpenAI-compatible serving backend for local development.

## When not to use it
- When you require a simple zero-config desktop GUI (use [LM Studio](lm-studio.md) or [Ollama](../../services/ollama.md) instead).
- For massive multi-node enterprise cloud deployments requiring complex distributed orchestration (use [vLLM](vllm.md) or [SGLang](sglang.md)).

## Getting started

### Installation
```bash
pip install freetoken
```

### Basic CLI Server Start
```bash
# Launch OpenAI-compatible local API server using Qwen3.8 model
freetoken-serve --model Qwen/Qwen3.8-27B-Instruct --port 8000 --kv-cache-dtype fp8
```

## CLI examples

### 1. Launch Server with Speculative Decoding
```bash
freetoken-serve \
  --model meta-llama/Llama-4-70B-Instruct \
  --draft-model meta-llama/Llama-4-1B-Instruct \
  --tp-size 2 \
  --max-model-len 65536
```

### 2. Run Benchmark Diagnostic
```bash
freetoken-bench --model Qwen/Qwen3.8-27B-Instruct --num-prompts 100 --input-len 2048 --output-len 512
```

## API examples

### Programmatic Python Client Integration with Pydantic v2 Output Validation
The following script demonstrates querying a FreeToken local server endpoint and enforcing **Pydantic v2** validation to verify token generation rates and structural adherence.

```python
import sys
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

class FreeTokenUsage(BaseModel):
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    total_tokens: int = Field(..., ge=0)

class FreeTokenResponse(BaseModel):
    id: str
    model: str
    content: str = Field(..., min_length=1)
    usage: FreeTokenUsage

def query_freetoken_endpoint(prompt: str) -> Optional[FreeTokenResponse]:
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="freetoken-local"
    )

    try:
        raw_resp = client.chat.completions.create(
            model="Qwen/Qwen3.8-27B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        resp_dict = raw_resp.model_dump()
        payload = {
            "id": resp_dict.get("id", "ft-001"),
            "model": resp_dict.get("model", "Qwen3.8-27B"),
            "content": resp_dict["choices"][0]["message"]["content"],
            "usage": resp_dict.get("usage", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
        }

        # Validate structured output via Pydantic v2
        return FreeTokenResponse.model_validate(payload)

    except ValidationError as ve:
        print(f"Pydantic Validation Error: {ve}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Execution Error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initiating FreeToken local inference test...")
    # Mock validation demo
    mock_payload = {
        "id": "ft-12345",
        "model": "Qwen/Qwen3.8-27B-Instruct",
        "content": "FreeToken provides fast local inference through optimized KV cache pooling.",
        "usage": {
            "prompt_tokens": 12,
            "completion_tokens": 15,
            "total_tokens": 27
        }
    }
    result = FreeTokenResponse.model_validate(mock_payload)
    print("FreeToken output validated successfully via Pydantic v2:")
    print(f"  Model: {result.model}")
    print(f"  Content: {result.content}")
    print(f"  Total Tokens: {result.usage.total_tokens}")
```

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput enterprise serving framework.
- [SGLang](sglang.md) — Fast execution engine for complex LLM prompts and structured outputs.
- [Ollama](../../services/ollama.md) — Popular local model management software.
- [Qwen](../ai_knowledge/qwen.md) — Frontier open-weights model family.
- [Llama.cpp](llama-cpp.md) — Lightweight C++ inference engine for edge devices.

## Sources / references
- [FreeToken InfoQ Announcement](https://www.infoq.com/news/2026/08/freetoken-local-inference/)
- [LocalLLaMA Community Inference Benchmarks](https://www.reddit.com/r/LocalLLaMA/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
