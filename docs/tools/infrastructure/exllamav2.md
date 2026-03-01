# ExLlamaV2

## What it is
ExLlamaV2 is a fast inference library optimized for running Large Language Models (LLMs) on modern consumer-class NVIDIA GPUs. It introduces the **EXL2** quantization format, which offers fine-grained control over model compression.

## What problem it solves
Running high-parameter models (like Llama-3 70B) on consumer GPUs with limited VRAM (e.g., 24GB on an RTX 4090) requires aggressive and precise quantization. ExLlamaV2 provides extremely high inference speeds and a flexible format that allows users to target specific bits-per-weight (e.g., 3.5 or 4.25 bits) to maximize quality within a fixed memory budget.

## Where it fits in the stack
Infra

## Typical use cases
- High-performance local LLM chat and assistance.
- Running large quantized models on consumer-grade NVIDIA hardware.
- Backend for roleplay and creative writing tools (e.g., SillyTavern).

## Strengths
- **Exceptional Speed**: One of the fastest inference engines for NVIDIA consumer GPUs.
- **EXL2 Format**: Allows for specific "bits-per-weight" targets to fit models perfectly into VRAM.
- **Efficient Memory Usage**: Native support for Flash Attention 2 and 4-bit KV cache.
- **Minimal Overhead**: Lightweight and optimized for single-user low-latency scenarios.

## Limitations
- **NVIDIA Only**: Requires a modern NVIDIA GPU (Pascal or newer).
- **Format Specificity**: Only supports EXL2 and GPTQ formats; does not support GGUF.
- **Single-User Focus**: Not designed for high-concurrency multi-user serving like vLLM.

## When to use it
- When you have a modern NVIDIA GPU and want the absolute best local inference performance.
- When you want to fit the highest quality version of a model into your specific VRAM limit using EXL2.

## When not to use it
- On Apple Silicon (use MLX) or AMD hardware (use llama.cpp).
- For production enterprise serving with many concurrent users.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install exllamav2
```

### Minimal CLI Example
```bash
python -m exllamav2.test_inference -m /path/to/model/ -p "Tell me a joke."
```

### Minimal Python Example
```python
from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2DynamicGenerator

config = ExLlamaV2Config("/path/to/model")
model = ExLlamaV2(config)
model.load()

tokenizer = ExLlamaV2Tokenizer(config)
cache = ExLlamaV2Cache(model)
generator = ExLlamaV2DynamicGenerator(model, cache, tokenizer)

output = generator.generate_text("The secret of life is", max_new_tokens=50)
print(output)
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md)
- [Aphrodite Engine](aphrodite-engine.md)
- [GPTQ](https://github.com/IST-DASLab/gptq)

## Sources / References
- [GitHub](https://github.com/turboderp/exllamav2)
- [EXL2 Wiki](https://github.com/turboderp/exllamav2/wiki)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
