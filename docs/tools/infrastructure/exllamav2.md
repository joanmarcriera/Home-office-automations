# ExLlamaV2

## What it is
ExLlamaV2 is a fast inference library optimized for running Large Language Models (LLMs) on modern consumer-class NVIDIA GPUs. It introduces the **EXL2** quantization format, which offers fine-grained control over model compression.

## What problem it solves
Running high-parameter models (like Llama-3 70B) on consumer GPUs with limited VRAM (e.g., 24GB on an RTX 4090) requires aggressive and precise quantization. ExLlamaV2 provides extremely high inference speeds and a flexible format that allows users to target specific bits-per-weight (bpw) to maximize quality within a fixed memory budget.

## Where it fits in the stack
**Infra**. It is the high-performance local inference backend for NVIDIA-based systems.

## Typical use cases
- **High-Performance Local LLMs**: Ultra-fast chat and assistance on consumer hardware.
- **VRAM-Targeted Quantization**: Fitting 70B+ models into specific VRAM envelopes (e.g., dual 3090/4090 setups).
- **Long-Context Inference**: Efficiently managing large KV caches for 128k+ token windows.

## Strengths
- **Exceptional Speed**: One of the fastest inference engines for NVIDIA consumer GPUs, often exceeding 100+ tokens/sec on 8B models.
- **EXL2 Format**: Allows for non-integer "bits-per-weight" targets (e.g., 3.5 bpw, 4.25 bpw) to perfectly optimize quality vs. VRAM.
- **Efficient Memory Usage**: Native support for Flash Attention 2 and 4-bit KV cache quantization.
- **Custom Kernels**: Highly optimized CUDA kernels for NVIDIA architectures from Pascal to Blackwell.

## Limitations
- **NVIDIA Only**: Requires a modern NVIDIA GPU with CUDA support.
- **Format Specificity**: Only supports EXL2 and GPTQ formats; does not support GGUF or AWQ natively.
- **Single-User Focus**: Optimized for low-latency single-user generation rather than high-concurrency serving.

## When to use it
- When you have a modern NVIDIA GPU and want the absolute best local inference performance.
- When you need to squeeze the highest possible quality of a large model into your specific GPU memory limit.
- For interactive applications requiring the lowest possible time-to-first-token (TTFT).

## When not to use it
- On Apple Silicon (use MLX) or AMD hardware (use llama.cpp or vLLM).
- For enterprise production serving with many concurrent users (use vLLM or TGI).

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install exllamav2
```

### Quantization: Target Bits-Per-Weight
EXL2 allows you to target a specific bitrate for the whole model. For example, to target 4.0 bpw:

```bash
python convert.py \
    -i /path/to/hf_model \
    -o /path/to/working_dir \
    -cf /path/to/output_exl2 \
    -b 4.0
```

### Advanced Memory Management: 4-Bit KV Cache
ExLlamaV2 supports 4-bit KV cache quantization to save VRAM on long-context tasks.

```python
from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache_4bit, ExLlamaV2Tokenizer

config = ExLlamaV2Config("/path/to/model")
model = ExLlamaV2(config)
model.load()

tokenizer = ExLlamaV2Tokenizer(config)
# Use 4-bit cache for 2x context capacity
cache = ExLlamaV2Cache_4bit(model, max_seq_len = 32768)
```

### Optimization Flags
ExLlamaV2 supports various environment variables to tune performance:
- `EXLLAMAV2_XFORMERS=1`: Force use of Xformers for attention.
- `NVCC_FLAGS="-O3"`: Optimization flags for custom kernel compilation.

## Related tools / concepts
- [llama.cpp](llama-cpp.md)
- [Aphrodite Engine](aphrodite-engine.md)
- [vLLM](vllm.md)
- [Quantization](../knowledge_base/patterns/quantization.md)
- [NVIDIA CUDA](../infrastructure/nvidia-cuda.md)
- [Long Context](../knowledge_base/long-context.md)

## Sources / References
- [Official Website](https://github.com/turboderp/exllamav2)
- [EXL2 Wiki: Quantization and Measurement](https://github.com/turboderp/exllamav2/wiki/Quantization-and-Measurement)
- [Flash Attention 2 Integration](https://github.com/turboderp/exllamav2#features)

## Contribution Metadata
- Last reviewed: 2026-05-17
- Confidence: high
