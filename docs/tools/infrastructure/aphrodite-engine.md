# Aphrodite Engine

## What it is
Aphrodite Engine is a high-performance inference engine for Large Language Models, forked from vLLM. It is specifically designed to bridge the gap between production-grade serving and the features desired by the local LLM community.

## What problem it solves
While vLLM is excellent for data center serving, the local community often uses a wider variety of quantization formats (like GPTQ, AWQ, and EXL2) and specific API requirements (like KoboldAI compatibility). Aphrodite maintains vLLM's high-throughput PagedAttention backend while adding support for these formats and local-friendly features.

## Where it fits in the stack
Infra

## Typical use cases
- High-throughput serving for local chat communities.
- Backend for local LLM frontends like SillyTavern or KoboldLite.
- Serving quantized models (AWQ, GPTQ) with vLLM-like performance.

## Strengths
- **PagedAttention**: Inherits industry-leading memory management for high throughput.
- **Wide Format Support**: Supports AWQ, GPTQ, SqueezeLLM, and partial EXL2.
- **Dual API Compatibility**: Supports both OpenAI and KoboldAI API standards.
- **Community-Centric**: Features and updates tailored for local and enthusiast users.

## Limitations
- **Hardware**: Primarily optimized for NVIDIA GPUs.
- **Maintenance**: As a fork, it may lag behind the main vLLM branch for certain upstream features.

## When to use it
- When you need vLLM's performance but require compatibility with KoboldAI or specific local community quantization formats.
- When building community-focused LLM services.

## When not to use it
- If you need the absolute latest, bleeding-edge features from the main vLLM project.
- For non-NVIDIA hardware (consider llama.cpp).

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install aphrodite-engine
```

### Minimal CLI Example (OpenAI Server)
```bash
python -m aphrodite.endpoints.openai.api_server --model /path/to/model/ --dtype float16
```

### Minimal CLI Example (KoboldAI Server)
```bash
python -m aphrodite.endpoints.kobold.api_server --model /path/to/model/
```

## Related tools / concepts
- [vLLM](vllm.md)
- [ExLlamaV2](exllamav2.md)
- [llama.cpp](llama-cpp.md)

## Sources / References
- [GitHub](https://github.com/PygmalionAI/aphrodite-engine)
- [Documentation](https://aphrodite.pygmalion.chat/)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
