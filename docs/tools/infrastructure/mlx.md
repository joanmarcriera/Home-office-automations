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

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

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

## Related tools / concepts
- [llama.cpp](llama-cpp.md)
- [PyTorch](https://pytorch.org/)
- [Apple Silicon](https://www.apple.com/silicon/)

## Sources / References
- [GitHub](https://github.com/ml-explore/mlx)
- [MLX Examples](https://github.com/ml-explore/mlx-examples)
- [Documentation](https://ml-explore.github.io/mlx/build/html/index.html)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
