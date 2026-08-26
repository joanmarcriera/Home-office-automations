# Turbo-fieldfare

## What it is
Turbo-fieldfare is an open-source, custom Swift 6.2 and Metal 3 inference engine designed specifically for running instruction-tuned Mixture of Experts (MoE) models, such as Gemma 4 26B-A4B and its specialized MoE variants, on Apple Silicon Macs. By implementing an active expert streaming mechanism that serves routed experts directly from high-speed NVMe SSD storage rather than keeping the entire 14.3 GB model materialized in system memory, Turbo-fieldfare executes Gemma 4 with a strictly bounded runtime footprint of only ~2 GB of system RAM.

## What problem it solves
Running modern medium-sized MoE LLMs locally (such as Gemma 4 26B-A4B) typically demands massive amounts of unified memory, requiring 16 GB, 24 GB, or 36 GB hardware configurations. For developers and home-lab operators with base-model 8 GB M-series Macs, loading a 14 GB quantized checkpoint results in severe system swapping or outright Out-Of-Memory (OOM) failures. Turbo-fieldfare solves this by dynamically streaming non-resident routed experts from the SSD as tokens are evaluated, making large local MoE inference accessible on consumer Apple hardware.

## Where it fits in the stack
**Category**: Infrastructure / Inference Layer. Turbo-fieldfare acts as a local model execution runtime specifically targeting macOS systems. It competes with lightweight local runtimes like [llama.cpp](llama-cpp.md) or [MLX](mlx.md) but introduces a unique SSD-streaming approach for MoE architectures. It exposes a native Model Context Protocol (FastMCP 3.1 / MCP 3.1) adapter alongside an OpenAI-compatible HTTP server for integration with agent frameworks powered by SOTA models like Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra.

```
┌──────────────────────────────────────────────┐
│           Agent & MCP Orchestration          │
│       (Claude 5.6, GPT-5.6, FastMCP 3.1)     │
├──────────────────────────────────────────────┤
│       TURBO-FIELDFARE INFERENCE RUNTIME      │ (SSD Expert Streaming Engine)
├──────────────────────────────────────────────┤
│         Metal 3 / Apple Silicon GPU          │ (M1/M2/M3/M4/M5 Unified Architecture)
└──────────────────────────────────────────────┘
```

## Typical use cases
- **Low-RAM Local Inference**: Running state-of-the-art Gemma 4 26B MoE models on an 8 GB M2/M3 MacBook Air at 5–6 tokens per second bounded within ~2 GB RAM.
- **On-Device Private Assistants**: Integrating high-quality local MoE reasoning directly into macOS agent architectures without cloud API dependencies.
- **Resource-Constrained Agent Swarms**: Running multiple localized agents simultaneously where overall process memory allocation must be strictly bounded.
- **FastMCP 3.1 Tool Execution Endpoints**: Offering native Swift-accelerated MoE inference to FastMCP server routines.

## Strengths
- **Extreme Memory Efficiency**: Binds the active memory footprint to ~2 GB of RAM, regardless of total active parameters.
- **Metal 3 Acceleration**: Leverages Apple Silicon's GPU via Metal 3 Performance Shaders for high token decode rates on higher-tier Macs (e.g., 31–35 tokens/sec on M5 Pro).
- **FastMCP 3.1 & OpenAI Protocol Support**: Built-in server supporting streaming completions, native tool-calling schemas, and FastMCP 3.1 protocol transport.
- **No Heavy Python Dependencies**: Built natively in Swift 6.2 with zero reliance on PyTorch, Hugging Face Hub libraries, or heavy python runtimes.

## Limitations
- **SSD Write Wear / I/O Bottlenecks**: High-throughput expert streaming depends entirely on SSD I/O bandwidth and latency, which can degrade speed under concurrent disk-heavy workloads.
- **Model Architecture Lock-In**: Optimized specifically for Gemma 4 26B-A4B and MoE topologies with modular expert routing tables.
- **macOS Exclusive**: Requires Apple Silicon and Metal 3 Performance Shaders; incompatible with Linux or Windows hardware setups.

## When to use it
- When you want to run Gemma 4 MoE models locally on an Apple Silicon Mac with 8 GB or 16 GB of unified memory.
- When you need a dependency-free, compile-on-device native Swift application that integrates directly with local macOS agentic tools via FastMCP 3.1.

## When not to use it
- On Linux or Windows servers with NVIDIA hardware (use [vLLM](vllm.md) or [SGLang](sglang.md) instead).
- When running non-MoE dense architectures like Llama 4 8B, where native [MLX](mlx.md) or [llama.cpp](llama-cpp.md) provide superior throughput without expert streaming overhead.

## Getting started

### Requirements
- Apple Silicon Mac (M1, M2, M3, M4, or M5 series)
- macOS 15 or 16
- Xcode or Command Line Tools with Swift 6.2+

### Installation
Build the native release binary from source:

```bash
git clone https://github.com/drumih/turbo-fieldfare.git
cd turbo-fieldfare
swift build -c release
```

Run the application or server to start the streaming model download and repack step:
```bash
.build/release/TurboFieldfareMac
```

## CLI examples

### Starting the Local Server
Launch the OpenAI-compatible and FastMCP 3.1 API server listening on localhost port 8080:

```bash
.build/release/TurboFieldfareMac --server --port 8080 --mcp-enabled
```

### Prompting via curl
Verify the local server's streaming completion endpoint:

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-4-26b-a4b",
    "messages": [
      {"role": "user", "content": "Explain Mixture of Experts streaming on Apple Silicon."}
    ],
    "stream": true
  }'
```

## API examples

### Programmatic Python Verification with Pydantic v2
The following Python script queries the Turbo-fieldfare server and validates the structured model response utilizing strict **Pydantic v2** validation.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
import requests

# Define Pydantic v2 schemas for response validation
class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message author (e.g., assistant)")
    content: str = Field(..., description="The content of the message")

class Choice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None

class TurboFieldfareResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]

    @field_validator("model")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        if "gemma-4" not in v.lower() and "fieldfare" not in v.lower():
            raise ValueError(f"Unexpected model identifier: {v}")
        return v

def query_local_gemma(prompt: str, url: str = "http://localhost:8080/v1/chat/completions") -> Optional[str]:
    payload = {
        "model": "gemma-4-26b-a4b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        # Parse and validate response using Pydantic v2
        validated_data = TurboFieldfareResponse.model_validate(response.json())
        return validated_data.choices[0].message.content

    except Exception as e:
        print(f"Error validating Turbo-fieldfare response: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Testing connection to local Turbo-fieldfare engine...")
    ans = query_local_gemma("Why does expert streaming save RAM?")
    if ans:
        print(f"Validation successful! Response:\n{ans}")
    else:
        print("Validation failed or server offline. Skipping runtime test.")
```

## Related tools / concepts
- [vLLM](vllm.md) — SOTA high-throughput model serving backend for enterprise clusters.
- [Aphrodite Engine](aphrodite-engine.md) — vLLM fork with localized sampling enhancements.
- [SGLang](sglang.md) — High-concurrency agent execution and serving engine.
- [llama.cpp](llama-cpp.md) — Benchmark CPU/GPU inference runtime.
- [MLX](mlx.md) — Apple's official native framework for machine learning on Apple Silicon.
- [Ollama](../../services/ollama.md) — Local model serving utility with simplified configuration.
- [ExLlamaV2](exllamav2.md) — Fast local GPU execution for dense models.
- [ExLlamaV3](exllamav3.md) — Multi-GPU local runtime optimized for low memory.

## Sources / references
- [Turbo-fieldfare GitHub Repository](https://github.com/drumih/turbo-fieldfare)
- [Reddit r/LocalLLaMA: Turbo-fieldfare release discussion](https://www.reddit.com/r/LocalLLaMA/comments/1vasnys/turbofieldfare_opensource_engine_running_gemma_4/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
