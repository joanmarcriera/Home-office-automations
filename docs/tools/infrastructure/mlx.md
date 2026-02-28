# MLX

## What it is
MLX is an array framework designed for efficient and flexible machine learning research on Apple Silicon. Developed by Apple's machine learning research team, it is optimized to take full advantage of the unified memory architecture found in M1, M2, and M3 chips.

## What problem it solves
Traditional ML frameworks (like PyTorch or TensorFlow) often have overhead when moving data between CPU and GPU. MLX leverages Apple Silicon's unified memory, allowing arrays to live in shared memory so operations can be performed on either device without data transfers.

## Where it fits in the stack
**Infra / Framework** — It is the foundational framework for ML on Apple hardware, similar to how CUDA/PyTorch are used on NVIDIA.

## Typical use cases
- Local LLM inference and fine-tuning on MacBooks and Mac Studios.
- Developing and testing new ML models directly on Apple Silicon.
- Image generation (Stable Diffusion) and speech recognition (Whisper) optimized for Mac.

## Strengths
- **Unified Memory**: Zero-copy data sharing between CPU and GPU.
- **Familiar API**: Python API closely follows NumPy and PyTorch.
- **Lazy Computation**: Computations are only materialized when needed.
- **Dynamic Graph Construction**: Flexible and easy to debug.

## Limitations
- **Apple Silicon Only**: Only runs on Apple hardware (macOS).
- **Ecosystem**: Smaller library of pre-built components compared to PyTorch (though growing rapidly via `mlx-lm`).

## When to use it
- If you are developing or running ML models on a Mac with Apple Silicon.
- When you want the absolute best performance and efficiency on macOS.

## When not to use it
- On Linux, Windows, or Intel-based Macs.
- For production deployments on cloud servers (which typically use NVIDIA GPUs).

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install mlx-lm
```

### Minimal Python Example (Text Generation)
```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

response = generate(
    model,
    tokenizer,
    prompt="Explain gravity in one sentence.",
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
- [Official Documentation](https://ml-explore.github.io/mlx/build/html/index.html)

## Contribution Metadata
- Last reviewed: 2026-02-28
- Confidence: high
