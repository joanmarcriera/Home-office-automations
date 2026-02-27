# Aphrodite Engine

## What it is
Aphrodite Engine is an open-source inference engine designed for high-throughput serving of LLMs. It is a fork of vLLM, specifically tailored to support a wider range of quantization formats and features useful for the local LLM community.

## What problem it solves
While vLLM is excellent for production data centers, the local community often uses a wider variety of models and quantization formats. Aphrodite extends vLLM's PagedAttention performance to formats like AWQ, GPTQ, and EXL2 (partially), and adds features like KoboldAI-compatible APIs.

## Where it fits in the stack
**Infra** — An inference engine that bridges the gap between production-grade throughput (vLLM) and local community needs.

## Typical use cases
- Hosting an LLM backend for local chat communities (e.g., Pygmalion).
- Serving quantized models with high throughput on local hardware.
- Backend for services that require both OpenAI and KoboldAI API compatibility.

## Strengths
- **PagedAttention**: Inherits vLLM's industry-leading memory management.
- **Wider Quantization Support**: Supports GPTQ, AWQ, and SqueezeLLM.
- **Dual API Support**: Provides both OpenAI-compatible and KoboldAI-compatible endpoints.
- **Local Community Focus**: Includes features requested by the local LLM and roleplay communities.

## Limitations
- **Hardware**: Primarily optimized for NVIDIA GPUs.
- **Upstream Sync**: As a fork, there is a delay in receiving the latest updates from the main vLLM project.

## When to use it
- When you want vLLM-like performance but need compatibility with specific quantization formats or local LLM frontends.
- If you are building a service for the roleplay or local chat community.

## When not to use it
- If you need the absolute latest features from vLLM.
- For CPU-only or non-NVIDIA hardware where llama.cpp is more versatile.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install aphrodite-engine
```

### Minimal CLI Example (OpenAI API Server)
```bash
python -m aphrodite.endpoints.openai.api_server --model your-model-path --dtype float16
```

### Minimal CLI Example (KoboldAI API Server)
```bash
python -m aphrodite.endpoints.kobold.api_server --model your-model-path
```

## Related tools / concepts
- [vLLM](vllm.md)
- [ExLlamaV2](exllamav2.md)
- [llama.cpp](llama-cpp.md)

## Sources / References
- [GitHub](https://github.com/PygmalionAI/aphrodite-engine)
- [Official Website](https://aphrodite.pygmalion.chat/)

## Contribution Metadata
- Last reviewed: 2026-02-27
- Confidence: high
