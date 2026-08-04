# Turbo-fieldfare

## What it is
Turbo-fieldfare is an open-source, custom Swift and Metal inference engine designed specifically for running the instruction-tuned Gemma 4 26B-A4B model on Apple Silicon Macs. By implementing an expert streaming mechanism that serves routed experts directly from high-speed SSD storage rather than keeping the entire 14.3 GB model materialized in system memory, Turbo-fieldfare can execute Gemma 4 with a bounded runtime footprint of only ~2 GB of RAM.

## What problem it solves
Running modern medium-sized LLMs locally (such as Gemma 4 26B) typically demands massive amounts of unified memory, requiring 16 GB or 24 GB hardware variants. For developers and home-lab operators with base-model 8 GB M-series Macs, loading a 14 GB quantized checkpoint results in severe system swapping or outright Out-Of-Memory (OOM) failures. Turbo-fieldfare solves this by streaming non-resident routed experts dynamically from the SSD as tokens are evaluated, making large local model inference accessible on standard consumer hardware.

## Where it fits in the stack
**Category**: Infrastructure / Inference Layer. Turbo-fieldfare acts as a local model execution runtime specifically targeting macOS systems. It competes with lightweight local runtimes like [llama.cpp](llama-cpp.md) or [MLX](mlx.md) but introduces a unique SSD-streaming approach for MoE (Mixture of Experts) architectures.

## Typical use cases
- **Low-RAM Local Inference**: Running a state-of-the-art Gemma 4 26B model on an 8 GB M2 MacBook Air at 5–6 tokens per second.
- **On-Device Private Assistants**: Integrating high-quality local reasoning directly into macOS agent architectures without external API dependencies.
- **Resource-Constrained Agent Swarms**: Running multiple localized agents simultaneously where overall memory allocation must be strictly bounded.

## Strengths
- **Extreme Memory Efficiency**: Binds the active memory footprint to ~2 GB of RAM, regardless of the active parameters.
- **Metal Acceleration**: Leverages Apple Silicon's GPU via Metal Performance Shaders for high token decode rates on higher-tier Macs (e.g., 31–35 tokens/sec on M5 Pro).
- **Embedded OpenAI-Compatible Server**: Features a built-in HTTP server supporting streaming completions and native tool-calling schemas.
- **No Heavy Python Dependencies**: Built natively in Swift 6.2 with no reliance on PyTorch, Hugging Face Hub libraries, or transformers for inference.

## Limitations
- **SSD Write Wear / I/O Bottlenecks**: High-throughput expert streaming depends entirely on SSD I/O latency, which can degrade speed if other heavy disk operations are running.
- **Model Lock-In**: Currently optimized exclusively for Gemma 4 26B-A4B and its specific Mixture of Experts (MoE) configuration.
- **macOS Exclusive**: Requires Apple Silicon and Metal Performance Shaders; not compatible with Linux or Windows setups.

## When to use it
- When you want to run Gemma 4 locally on an Apple Silicon Mac with 8 GB or 16 GB of unified memory.
- When you need a dependency-free, compile-on-device native Swift application that integrates with your local macOS agentic tools.

## When not to use it
- On Linux or Windows servers with NVIDIA hardware (use [vLLM](vllm.md) or [SGLang](sglang.md) instead).
- When running non-MoE dense architectures like Llama 4 8B, where native [MLX](mlx.md) or [llama.cpp](llama-cpp.md) provide superior throughput without expert streaming.

## Getting started

### Requirements
- Apple Silicon Mac (M1, M2, M3, M4, or M5 series)
- macOS 15 or later
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
Launch the OpenAI-compatible API server listening on localhost port 8080:

```bash
.build/release/TurboFieldfareMac --server --port 8080
```

### Prompting via curl
Verify the local server's streaming completion endpoint:

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-4-26b-a4b",
    "messages": [
      {"role": "user", "content": "Explain Mixture of Experts streaming."}
    ],
    "stream": true
  }'
```

## API examples

### Programmatic Python Verification
The following Python script queries the Turbo-fieldfare server and validates the structured model response utilizing **Pydantic v2** validation.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field
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
- [vLLM](vllm.md) — SOTA high-throughput model serving backend for enterprise.
- [Aphrodite Engine](aphrodite-engine.md) — vLLM fork with localized sampling enhancements.
- [SGLang](sglang.md) — High-concurrency agent execution and serving engine.
- [llama.cpp](llama-cpp.md) — The benchmark CPU/GPU inference runtime.
- [MLX](mlx.md) — Apple's official native framework for machine learning on Apple Silicon.
- [Ollama](../../services/ollama.md) — Local model serving utility with simplified configuration.
- [ExLlamaV2](exllamav2.md) — Fast local GPU execution for dense models.
- [ExLlamaV3](exllamav3.md) — Multi-GPU local runtime optimized for low memory.

## Sources / references
- [Turbo-fieldfare GitHub Repository](https://github.com/drumih/turbo-fieldfare)
- [Reddit r/LocalLLaMA: Turbo-fieldfare release discussion](https://www.reddit.com/r/LocalLLaMA/comments/1vasnys/turbofieldfare_opensource_engine_running_gemma_4/)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
