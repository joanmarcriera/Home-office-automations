# Text Generation WebUI

## What it is
Text Generation WebUI (often called `oobabooga`) is a feature-rich, Gradio-based web interface and serving platform for open-source large language models. It supports a vast array of inference backends including `llama.cpp` (GGUF), ExLlamaV2, Transformers, AutoGPTQ, HQQ, and AWQ.

## What problem it solves
Running local LLMs across different formats (GGUF, EXL2, Safetensors, AWQ) often requires maintaining separate command-line flags, environments, and serving binaries. Text Generation WebUI provides a unified UI for downloading, configuring, fine-tuning, testing, and serving local models with full parameter control (samplers, context length, specular decoding, character cards, and extensions) alongside OpenAI-compatible and native API endpoints.

## Where it fits in the stack
**Infrastructure / Local Serving & Web UI**. It serves as an all-in-one local LLM workstation hub for home-lab power users and AI researchers.

## Typical use cases
- **Multi-Backend Local LLM Testing**: Comparing GGUF vs ExLlamaV2 vs Transformers inference speed and output quality on identical hardware.
- **Interactive Chat & Roleplay**: Utilizing character cards, chat templates, and persistent memory extensions.
- **Local API Gateway**: Exposing OpenAI-compatible endpoints (`/v1/chat/completions`) for local agent frameworks and FastMCP 3.1 tooling.
- **Model Fine-Tuning & Quantization**: Training LoRA adapters locally via integrated PEFT/Transformers workflows.

## Strengths
- **Unrivaled Backend Support**: Native loader support for llama.cpp, ExLlamaV2, Transformers, AutoGPTQ, HQQ, and TensorRT-LLM.
- **Rich Parameter & Sampler Control**: Granular control over temperature, top-p, min-p, repetition penalty, DRY sampling, and custom logit processors.
- **Extensible Architecture**: Large ecosystem of third-party extensions (TTS, whisper speech-to-text, vector storage, web search).
- **Dual Interface & API**: Full interactive Gradio web UI combined with OpenAI-compatible REST API endpoints.

## Limitations
- **Resource Heavy**: Higher baseline memory footprint compared to minimal head-less binaries like `llama-server`.
- **Power-User Complexity**: Options and settings density can be overwhelming compared to simplified tools like [Ollama](../../services/ollama.md) or [Open WebUI](../../services/open-webui.md).

## When to use it
- When you need a local web interface that can load non-GGUF formats (ExLlamaV2, AWQ, HQQ, Transformers) directly on NVIDIA GPUs.
- When fine-tuning local LoRA adapters or testing granular sampler settings (e.g., DRY, min-p).

## When not to use it
- For clean, minimal multi-user chat deployments on CPU or Apple Silicon — use [Open WebUI](../../services/open-webui.md) with [Ollama](../../services/ollama.md).
- For headless high-throughput API endpoints — use [vLLM](vllm.md) or [llama-swap](llama-swap.md).

## Getting started

### Installation & Launch
```bash
# One-click installers available or clone repository
git clone https://github.com/oobabooga/text-generation-webui.git
cd text-generation-webui
./start_linux.sh --api
```

## CLI examples

### Launching with API server enabled
```bash
./start_linux.sh --api --listen --model llama-4-8b
```

## API examples

### Querying OpenAI-Compatible API Endpoint
```python
from openai import OpenAI

# Start WebUI with --api flag
client = OpenAI(base_url="http://localhost:5000/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="local-model",
    messages=[{"role": "user", "content": "Hello from FastMCP 3.1 client!"}]
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md) — Fast C++ GGUF inference engine integrated into WebUI.
- [Open WebUI](../../services/open-webui.md) — Clean, modern Web UI focused primarily on Ollama and OpenAI backends.
- [Ollama](../../services/ollama.md) — Lightweight CLI-first local model runtime.
- [llama-swap](llama-swap.md) — Dynamic GGUF model hot-swapping proxy.

## Sources / references
- [Text Generation WebUI GitHub Repository](https://github.com/oobabooga/text-generation-webui)
- [Text Generation WebUI Documentation](https://github.com/oobabooga/text-generation-webui/wiki)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
