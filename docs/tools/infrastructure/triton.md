# Triton

## What it is

- **Pythonic GPU Kernel Authoring**: Allows developers to write custom massively-parallel GPU matrix multiplication, attention, and reduction kernels directly in Python using standard decorators (`@triton.jit`).
- **Automated Memory Layout & Thread Optimization**: Compiler automatically handles block-level memory coalescing, shared memory tiling, thread block scheduling, and register allocation across NVIDIA (CUDA) and AMD (ROCm) GPUs.
- **Deep PyTorch Integration**: Native compilation target for `torch.compile`, enabling automatic operator fusion (e.g., fusing LayerNorm + GELU + Matrix Multiply into a single GPU memory pass).
- **Extensible Hardware Backend Architecture**: Compiles Triton IR down to LLVM IR, generating optimized machine code for NVIDIA Hopper, Blackwell, and Rubin GPUs, as well as AMD Instinct MI300/MI400 series accelerators.
- **FastMCP 3.1 & Model Optimization**: Powering custom quantization kernels (FP4, FP8, INT4 AWQ) and low-latency agent tool execution pipelines.


## What problem it solves
- Eliminates the complexity and long development cycles required to write custom CUDA or C++ GPU kernels.
- Solves GPU memory bandwidth bottlenecks by enabling automatic operator fusion in Python.

## Where it fits in the stack
- Sits in the **Low-Level GPU Programming & Kernel Compiler** layer.
- Powers PyTorch , Unsloth fine-tuning kernels, FlashAttention-3, and custom quantization operators.

## Typical use cases

- **Custom Attention Mechanism Authoring**: Writing specialized attention operators (e.g., RingAttention, Sliding Window Attention, Sparse Attention) tailored for long-context models.
- **Fine-Tuning Acceleration (Unsloth)**: Writing hand-tuned fused kernels for Backpropagation, LoRA gradient updates, and dynamic quantization in model training frameworks like Unsloth.
- **Low-Precision Quantization Operators**: Implementing custom FP4, FP8, and INT4 matrix vector multiplication kernels for low-latency inference servers.
- **Custom Agentic Tensor Primitives**: Accelerating non-standard neural operators, vector distance calculations, and custom loss functions in research workflows.


## Strengths

- **High Developer Productivity**: Enables writing high-performance GPU kernels in hours rather than weeks compared to raw CUDA or HIP C++.
- **Hardware Portability**: Compiles the same Pythonic kernel code for both NVIDIA CUDA GPUs and AMD ROCm accelerators with zero source code changes.
- **Competitive CUDA Performance**: Generates machine code that rivals or exceeds hand-written CUDA kernels for fused neural network operations.


## Limitations

- **Debugging Complexity**: Debugging race conditions or out-of-bounds memory access in compiled Triton kernels requires understanding lower-level GPU memory layouts.
- **Block-Level Abstraction Overhead**: Highly specialized low-level hardware features (e.g., specific warp-level inline assembly instructions) may require custom LLVM IR passes.


## When to use it

- When developing custom neural network layer architectures, fused loss functions, or novel attention mechanisms that lack standard PyTorch CUDA implementations.
- When optimizing LLM fine-tuning or inference memory bandwidth by fusing multiple sequential elementwise GPU operations.
- When building hardware-portable AI software targeting both NVIDIA and AMD GPU clusters.


## When not to use it
- When standard PyTorch/TensorFlow high-level neural network operators already meet performance requirements.
- When running workloads exclusively on non-GPU host architectures.

## Getting started

```
+-------------------------------------------------------------------+
| Python Source Kernel (@triton.jit)                               |
|                                                                   |
|   @triton.jit                                                     |
|   def fused_add_kernel(x_ptr, y_ptr, out_ptr, n_elements, ...):  |
|       # Pythonic block-level arithmetic                           |
+-------------------------------------------------------------------+
                                 ||
                 Triton Compiler Front-End (Triton IR)
                                 ||
                                 \/
+-------------------------------------------------------------------+
| LLVM IR & Target Optimization Backend                             |
|                                                                   |
|   - Memory Coalescing & Tiling Allocation                         |
|   - Automatic Thread Block Scheduling                             |
|   - Register Allocation & Warp Optimization                       |
+-------------------------------------------------------------------+
                                 ||
         NVIDIA PTX / AMD HSA Code Generation
                                 ||
                                 \/
+-------------------------------------------------------------------+
| Target Hardware Execution                                         |
| - NVIDIA Hopper / Blackwell / Rubin GPUs                          |
| - AMD Instinct MI300 / MI400 Series Accelerators                  |
+-------------------------------------------------------------------+
```


## CLI examples



## API examples

The following Python example demonstrates defining a fused vector addition kernel using Triton (`@triton.jit`), configuring execution grid launch dimensions, and validating kernel launch configurations with strict **Pydantic v2** validation.

```python
import torch
from typing import Dict, Any
from pydantic import BaseModel, Field, field_validator

# Try importing triton; provide fallback stub if executing outside GPU environment
try:
    import triton
    import triton.language as tl
    HAS_TRITON = True
except ImportError:
    HAS_TRITON = False

# ---------------------------------------------------------------------------
# Pydantic v2 Kernel Launch Config Schema
# ---------------------------------------------------------------------------
class TritonKernelLaunchConfig(BaseModel):
    vector_size: int = Field(..., ge=1, description="Total number of elements in vector")
    block_size: int = Field(default=1024, ge=32, le=4096, description="Threads per block (power of 2)")
    num_warps: int = Field(default=4, ge=1, le=32, description="Number of warps per block")

    @field_validator("block_size")
    @classmethod
    def validate_power_of_two(cls, v: int) -> int:
        if (v & (v - 1)) != 0:
            raise ValueError("block_size must be a power of 2")
        return v

# ---------------------------------------------------------------------------
# Triton Kernel Definition (when Triton is available)
# ---------------------------------------------------------------------------
if HAS_TRITON:
    @triton.jit
    def vector_add_kernel(
        x_ptr, y_ptr, out_ptr,
        n_elements,
        BLOCK_SIZE: tl.constexpr
    ):
        pid = tl.program_id(axis=0)
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements

        x = tl.load(x_ptr + offsets, mask=mask)
        y = tl.load(y_ptr + offsets, mask=mask)
        output = x + y
        tl.store(out_ptr + offsets, output, mask=mask)

def execute_fused_add(config_payload: Dict[str, Any]) -> str:
    """Validate kernel launch config and launch Triton GPU kernel execution."""
    cfg = TritonKernelLaunchConfig.model_validate(config_payload)

    if not HAS_TRITON or not torch.cuda.is_available():
        return f"[Simulated Triton Launch]: Configured vector_add for size {cfg.vector_size} with block_size {cfg.block_size}"

    x = torch.rand(cfg.vector_size, device='cuda', dtype=torch.float32)
    y = torch.rand(cfg.vector_size, device='cuda', dtype=torch.float32)
    out = torch.empty_like(x)

    grid = lambda meta: (triton.cdiv(cfg.vector_size, meta['BLOCK_SIZE']),)
    vector_add_kernel[grid](x, y, out, cfg.vector_size, BLOCK_SIZE=cfg.block_size, num_warps=cfg.num_warps)

    return f"Successfully executed Triton vector addition kernel on GPU for {cfg.vector_size} elements."

if __name__ == "__main__":
    launch_params = {
        "vector_size": 100000,
        "block_size": 1024,
        "num_warps": 4
    }

    msg = execute_fused_add(launch_params)
    print(msg)
```


## Related tools / concepts

- **[Unsloth](../infrastructure/unsloth.md)**: High-speed LLM fine-tuning library leveraging custom Triton kernels.
- **[PEFT](../infrastructure/peft.md)**: Parameter-efficient fine-tuning framework integrated with Triton operations.
- **[TensorRT-LLM](tensorrt-llm.md)**: High-performance inference compiler featuring Triton kernel integration.


## Sources / references

- [OpenAI Triton Official Documentation & Tutorials](https://triton-lang.org/main/index.html)
- [Triton Lang Official GitHub Repository](https://github.com/triton-lang/triton)
- [PyTorch `torch.compile` and Triton Backend Guide](https://pytorch.org/docs/stable/torch.compiler.html)
- [Unsloth Triton Kernel Optimizations Architecture](https://unsloth.ai/)



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
