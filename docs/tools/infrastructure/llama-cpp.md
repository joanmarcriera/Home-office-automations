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

## Getting started

### Docker Compose Example
Run `llama.cpp` as an OpenAI-compatible server using Docker:

```yaml
services:
  llama-cpp:
    image: ghcr.io/ggerganov/llama.cpp:server
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
    command: "-m /models/llama-3-8b-instruct.Q4_K_M.gguf -c 2048 --host 0.0.0.0 --port 8080"
```

### Python API Example
Use the `openai` library to interact with your local `llama.cpp` server:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="sk-no-key-required")

response = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantization in 3 sentences."}
    ]
)

print(response.choices[0].message.content)
```

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
