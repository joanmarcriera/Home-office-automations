# llama.cpp

## What it is
`llama.cpp` is a lightweight C/C++ inference runtime for running GGUF/quantized LLMs locally on commodity hardware.

## What problem it solves
It makes local LLM inference practical on CPUs and smaller devices by combining quantization support with optimized low-level inference paths.

## Where it fits in the stack
**Infrastructure / Inference Runtime**. It is a core local-serving building block used directly or via wrappers.

## Typical use cases
- Running quantized LLMs offline on laptops, servers, or edge devices
- Building local-first AI tools without cloud API dependency
- Powering higher-level local model tools and wrappers

## Strengths
- Lightweight and portable local runtime
- Strong support for quantized model execution
- Large ecosystem and broad community adoption

## Limitations
- Requires manual model/runtime tuning for best performance
- Feature parity can vary across hardware backends
- Large models still require substantial memory/compute

## When to use it
- When privacy, offline operation, or cost control require local inference
- When you need direct control of quantization/runtime tradeoffs

## When not to use it
- When managed cloud APIs are preferred for simplicity and elasticity
- When you need frontier-model quality that local hardware cannot sustain

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free software; infrastructure/hardware costs still apply
- **Self-hostable**: Yes

## Related tools / concepts
- [Local LLMs](../ai_knowledge/local_llms.md)
- [Ollama](../../services/ollama.md)
- [ZSE](zse.md)

## Sources / References
- [llama.cpp repository](https://github.com/ggml-org/llama.cpp)
- [Ultimate guide to running quantized LLMs on CPU with llama.cpp](https://medium.com/red-buffer/ultimate-guide-to-running-quantized-llms-on-cpu-with-llama-cpp-1a26c34bb6dd)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: high
