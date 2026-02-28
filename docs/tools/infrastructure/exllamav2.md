# ExLlamaV2

## What it is
ExLlamaV2 is a fast inference library designed specifically for running LLMs locally on modern consumer-class NVIDIA GPUs. It is a complete rewrite of the original ExLlama and introduces the **EXL2** quantization format.

## What problem it solves
Running large models on consumer GPUs (like the RTX 3090/4090) often requires significant quantization. ExLlamaV2 provides extremely fast inference speeds for these GPUs and supports a versatile quantization format (EXL2) that allows for fine-grained control over bits-per-weight (e.g., 2.5-bit, 4.0-bit, 8.0-bit).

## Where it fits in the stack
**Infra** — A specialized local inference engine for NVIDIA consumer GPUs.

## Typical use cases
- Running 70B+ parameter models on a single or dual 24GB VRAM GPU setup.
- High-performance local chat and creative writing assistants.
- Backend for local LLM frontends like SillyTavern or Text-Generation-WebUI.

## Strengths
- **Speed**: One of the fastest inference engines for NVIDIA consumer GPUs.
- **EXL2 Format**: Allows for specific "bits-per-weight" targets to fit models perfectly into available VRAM.
- **Flash Attention**: Integrated support for Flash Attention 2.
- **Low Overhead**: Designed to be lightweight and efficient.

## Limitations
- **NVIDIA Only**: Requires a modern NVIDIA GPU (Pascal or newer).
- **GGUF Support**: Does not support GGUF; strictly focuses on EXL2 and GPTQ.

## When to use it
- When you have an NVIDIA RTX GPU and want the absolute best performance for local inference.
- When you want to use the EXL2 format to squeeze the best quality model into your specific VRAM limit.

## When not to use it
- If you have an AMD or Apple Silicon GPU (use llama.cpp or MLX).
- If you need to serve many concurrent users (vLLM or TGI are better for throughput).

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install exllamav2
```

### Minimal CLI Example (Test Inference)
```bash
python -m exllamav2.test_inference -m /path/to/exl2_model/ -p "In a world where AI"
```

### Minimal Python Snippet
```python
from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer
from exllamav2.generator import ExLlamaV2DynamicGenerator

config = ExLlamaV2Config("/path/to/model")
model = ExLlamaV2(config)
model.load()

tokenizer = ExLlamaV2Tokenizer(config)
cache = ExLlamaV2Cache(model)
generator = ExLlamaV2DynamicGenerator(model, cache, tokenizer)

output = generator.generate_text("The secret to life is", max_new_tokens=50)
print(output)
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md)
- [Aphrodite Engine](aphrodite-engine.md)
- [GPTQ](https://github.com/IST-DASLab/gptq)

## Sources / References
- [GitHub](https://github.com/turboderp/exllamav2)
- [EXL2 Format Explained](https://github.com/turboderp/exllamav2/wiki/EXL2-quantization)

## Contribution Metadata
- Last reviewed: 2026-02-28
- Confidence: high
