# MLX

## What it is
MLX is an array framework designed specifically for machine learning research on Apple Silicon. Developed by Apple's machine learning research team, it is optimized to leverage the unified memory architecture of M-series chips.

## What problem it solves
Standard ML frameworks like PyTorch or TensorFlow often face overhead when moving data between CPU and GPU. MLX solves this by using Apple Silicon's unified memory, allowing arrays to exist in a shared memory space where both the CPU and GPU can perform operations on them without needing data transfers.

## Where it fits in the stack
Infra

## Typical use cases
- Local LLM inference and fine-tuning on MacBooks and Mac Studios.
- Research and development of new ML models on Apple hardware.
- Optimized execution of Stable Diffusion and Whisper on macOS.

## Strengths
- **Unified Memory**: Zero-copy data sharing between CPU and GPU for maximum efficiency.
- **Familiar API**: Python API closely follows NumPy and PyTorch conventions.
- **Lazy Computation**: Computations are only materialized when required.
- **Optimized for M-Series**: Takes full advantage of Apple's hardware accelerators.

## Limitations
- **Hardware Restricted**: Only runs on Apple Silicon (M1, M2, M3, etc.) under macOS.
- **Ecosystem**: Smaller library of pre-built modules compared to the massive PyTorch ecosystem, though growing rapidly via `mlx-lm`.

## When to use it
- If you are developing or running ML models on Apple Silicon hardware.
- When you want the best possible performance and energy efficiency on a Mac.

## When not to use it
- On Linux, Windows, or Intel-based Macs.
- For production deployments on standard cloud servers (NVIDIA GPUs).

## Getting started

### Installation
```bash
pip install mlx-lm
```

### Minimal Python Example
```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

response = generate(
    model,
    tokenizer,
    prompt="Explain quantum entanglement in one sentence.",
    verbose=True
)
print(response)
```

### Minimal CLI Example
```bash
python -m mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit --prompt "Why is the sky blue?"
```

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [llama.cpp](llama-cpp.md)
- [ExLlamaV2](exllamav2.md)
- [Local LLMs](../ai_knowledge/local_llms.md)
- [vLLM](vllm.md)
- [SGLang](sglang.md)
- [Aphrodite Engine](aphrodite-engine.md)
- [Whisper](../../services/whisper.md)
- [Sora](../ai_knowledge/sora.md)
- [Llama Factory](../frameworks/llama-factory.md)

## Performance
- **Benchmarking**: 11 MLX models were benchmarked on M3 Ultra in March 2026, demonstrating its capability as a top-tier local inference platform.

## Sources / References
- [Official Website](https://github.com/ml-explore/mlx)
- [GitHub](https://github.com/ml-explore/mlx)
- [MLX Examples](https://github.com/ml-explore/mlx-examples)
- [Documentation](https://ml-explore.github.io/mlx/build/html/index.html)
- [Benchmarked 11 MLX models on M3 Ultra](https://www.reddit.com/r/LocalLLaMA/comments/1rkcvqa/benchmarked_11_mlx_models_on_m3_ultra_heres_which/)
- [Llama Factory](../frameworks/llama-factory.md)

## Contribution Metadata
- Last reviewed: 2026-06-02
- Confidence: high
