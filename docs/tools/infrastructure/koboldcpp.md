# Koboldcpp

## What it is
Koboldcpp is an extremely versatile local LLM inference engine and graphical user interface (GUI) packaged as a single, self-contained executable. Built on a fork of [llama.cpp](llama-cpp.md), Koboldcpp excels at local-first execution, offering native acceleration for NVIDIA (CUDA), Apple Silicon (Metal), AMD (ROCm), and OpenCL hardware, combined with a feature-rich, interactive web frontend for roleplay, writing, and custom API routing.

## What problem it solves
Setting up local model inference often requires navigating complex command-line arguments, virtual environments, compilation steps, or heavy memory/dependency footprints. Koboldcpp simplifies local AI by offering an "all-in-one" solution that runs immediately out-of-the-box, providing memory-saving context shift mechanisms (SmartContext), dynamic sampling controls (such as DRY and XTC), and an OpenAI-compatible API alongside its classic KoboldAI API client.

## Where it fits in the stack
**Category**: Infrastructure / Inference Engine. Koboldcpp serves as an alternative local serving layer. It sits at the same level as [llama.cpp](llama-cpp.md), [Ollama](../../services/ollama.md), and [LM Studio](lm-studio.md), providing direct model execution of GGUF formatted checkpoints.

## Typical use cases
- **Zero-Dependency Local Hosting**: Spinning up high-performance GGUF models on low-compute configurations with single-click executables.
- **Interactive Writing and Roleplay**: Using Koboldcpp's legacy web UI for deep model steering, custom prompt formats, and memory injection.
- **OpenAI-Compatible Local Endpoints**: Serving local model endpoints to agentic frameworks like AutoGen or Cline.

## Strengths
- **Single Executable Deployment**: No Python, CUDA SDK, or heavy dependencies required for standard execution.
- **Context Shift (SmartContext)**: Avoids costly context reprocessing on consecutive turns by shifting cache segments dynamically.
- **Rich Sampling Suite**: Native support for advanced sampling techniques (such as Mirostat, DRY, XTC, and temperature scaling).
- **Multi-backend Support**: Handles heterogeneous system acceleration (e.g., splitting layers across CUDA and CPU seamlessly).

## Limitations
- **Format Restrictiveness**: Primarily focused on GGUF; does not natively support serving EXL2 or Safetensors without separate conversion.
- **Concurrancy Overhead**: While it supports multi-user request queuing, it is not built for highly parallel enterprise serving (use [vLLM](vllm.md) or [SGLang](sglang.md) for heavy enterprise concurrency).
- **Desktop Focus**: UI and architecture are tailored for single-user desktop configurations rather than headless multi-node container swarms.

## When to use it
- For quick, localized testing of GGUF checkpoints on macOS, Windows, or Linux.
- When running roleplay or interactive writing models where direct prompt manipulation and memory insertion are required.
- When your machine has limited VRAM and you need to split model layers across GPU and system memory with maximum stability.

## When not to use it
- In enterprise production environments with thousands of concurrent, parallel API queries (use [vLLM](vllm.md) or [Aphrodite Engine](aphrodite-engine.md) instead).
- When serving dense EXL2 quantized models where [ExLlamaV2](exllamav2.md) or [ExLlamaV3](exllamav3.md) provide higher native throughput.

## Getting started

### Installation
Koboldcpp is distributed as a pre-compiled executable, but can easily be compiled from source for maximum platform optimization:

```bash
git clone https://github.com/LostRuins/koboldcpp.git
cd koboldcpp
make
```

For GPU acceleration (NVIDIA/CUDA):
```bash
make LLAMA_CUDA=1
```

## CLI examples

### Starting the Koboldcpp Server
Launch Koboldcpp with a GGUF model checkpoint and CUDA acceleration:

```bash
./koboldcpp.py --model ~/models/gemma-4-8b.gguf --usecuda --port 5001
```

### Prompting via KoboldAI API
Query the native KoboldAI text generation endpoint:

```bash
curl http://localhost:5001/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The future of home automation is ",
    "max_length": 50,
    "temperature": 0.7
  }'
```

## API examples

### Programmatic OpenAI-Compatible Client
The following Python script leverages Koboldcpp's OpenAI-compatible endpoint to complete a task and validates the returned payload using **Pydantic v2**.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field
import requests

# Define Pydantic v2 schema for API response validation
class MessagePart(BaseModel):
    role: str
    content: str

class ChoicePart(BaseModel):
    index: int
    message: MessagePart
    finish_reason: Optional[str] = None

class KoboldOpenAIResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChoicePart]

def query_kobold_endpoint(prompt: str, url: str = "http://localhost:5001/v1/chat/completions") -> Optional[str]:
    payload = {
        "model": "local-model",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 100
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()

        # Validate JSON payload using Pydantic v2 model_validate
        validated = KoboldOpenAIResponse.model_validate(response.json())
        return validated.choices[0].message.content

    except Exception as e:
        print(f"Error querying Koboldcpp OpenAI interface: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Connecting to local Koboldcpp inference instance...")
    result = query_kobold_endpoint("Verify standard API interface.")
    if result:
        print(f"Validation success! Output:\n{result}")
    else:
        print("Koboldcpp API offline or unconfigured. Skipping integration verification.")
```

## Related tools / concepts
- [vLLM](vllm.md) — SOTA enterprise-level inference server.
- [Aphrodite Engine](aphrodite-engine.md) — High-performance inference engine based on vLLM.
- [llama.cpp](llama-cpp.md) — Foundational C/C++ local model executor.
- [ExLlamaV2](exllamav2.md) — Specialized local loader for high-speed EXL2 inference.
- [ExLlamaV3](exllamav3.md) — Low-overhead local multi-GPU execution engine.
- [SGLang](sglang.md) — Advanced server optimized for heavy agentic workloads.
- [Ollama](../../services/ollama.md) — Highly popular CLI-based local LLM runner.
- [Jan.ai](jan-ai.md) — Desktop client powered by local loaders.

## Sources / references
- [LostRuins Koboldcpp GitHub Repository](https://github.com/LostRuins/koboldcpp)
- [Reddit r/LocalLLaMA: Koboldcpp Release Announcements](https://www.reddit.com/r/LocalLLaMA/comments/1vd13uv/koboldcpp_v1118_released/)

## Contribution Metadata
- Last reviewed: 2026-11-23
- Confidence: high
