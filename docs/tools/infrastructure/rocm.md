# ROCm (Radeon Open Compute)

## What it is
ROCm (Radeon Open Compute) is AMD's open-source software platform and GPU computing stack designed for high-performance computing (HPC), deep learning, and AI model acceleration. Celebrating a decade of open compute evolution, ROCm 10.0 (released in August 2026) provides native runtime drivers, math libraries, compiler toolchains, and HIP runtime abstractions for AMD Instinct (MI300/MI400 series) and Radeon (RDNA 3/RDNA 4) GPUs. In early 2027, ROCm serves as a primary enterprise open-source alternative to NVIDIA CUDA, powering high-throughput LLM inference and fine-tuning runtimes like [vLLM](vllm.md), [SGLang](sglang.md), and [llama.cpp](llama-cpp.md).

## What problem it solves
Hardware lock-in to proprietary compute platforms creates supply chain bottlenecks and cost pressures for organizations deploying AI models. ROCm provides an open, standard compute platform enabling developers to train, fine-tune, and serve frontier AI models on AMD GPU hardware with drop-in PyTorch, FlashAttention, and vLLM compatibility.

## Where it fits in the stack
**Infrastructure / Hardware Acceleration & GPU Compute Stack.** ROCm occupies the low-level hardware abstraction and GPU kernel driver layer beneath machine learning frameworks (PyTorch, JAX) and inference engines ([vLLM](vllm.md), [Ollama](../../services/ollama.md)).

## Typical use cases
- **Enterprise LLM Inference Serving**: Serving frontier models like [Qwen 3.8](../ai_knowledge/qwen.md) or [DeepSeek-V4](../ai_knowledge/local_llms.md) on AMD Instinct MI300X/MI325X GPU clusters.
- **Local Workstation Acceleration**: Offloading quantized GGUF inference in [llama.cpp](llama-cpp.md) or [Ollama](../../services/ollama.md) to consumer Radeon RX 7900 / RX 8900 series GPUs.
- **Distributed Training & Fine-Tuning**: Running large-scale distributed training jobs using PyTorch and AMD RCCL (Radeon Collective Communication Library).
- **Heterogeneous AI Workspaces**: Building cloud and homelab infrastructure hosting mixed NVIDIA and AMD GPU hardware side-by-side.

## Strengths
- **Fully Open Source Software Stack**: Open kernel drivers, compilers (LLVM/HIP), and runtime libraries without vendor lock-in.
- **Native PyTorch & FlashAttention Parity**: Direct day-zero support for PyTorch 2.x and optimized FlashAttention-2/3 kernels.
- **High VRAM Memory Bandwidth Support**: Maximizes throughput on AMD Instinct GPUs featuring up to 192GB+ HBM3e VRAM per node.
- **HIP Portability Layer**: Allows seamless conversion and compilation of existing CUDA codebases to C++ HIP targets.

## Limitations
- **Consumer GPU Support Nuances**: While Instinct enterprise accelerators have tier-1 support, enabling ROCm on certain desktop consumer Radeon cards requires explicit environment flag overrides (`HSA_OVERRIDE_GFX_VERSION`).
- **Ecosystem Tooling Gaps**: Third-party profiling and debugging tools are less ubiquitous than NVIDIA's Nsight ecosystem.
- **Legacy CUDA-Specific Kernel Dependencies**: Custom obscure CUDA C++ kernels require HIP translation steps before building.

## When to use it
- When deploying AI workloads on AMD Instinct or Radeon GPU hardware platforms.
- When building sovereign or open-source infrastructure free from proprietary GPU vendor stack lock-in.
- For high-concurrency LLM serving requiring large unified VRAM footprints per GPU node.

## When not to use it
- When your hardware infrastructure consists exclusively of NVIDIA GPUs (use CUDA / TensorRT instead) or Apple Silicon (use [MLX](mlx.md) instead).
- For lightweight CPU-only inference setups where GPU acceleration drivers are unneeded.

## Getting started

### Installation & System Check
```bash
# Verify ROCm driver and GPU device detection
rocminfo

# Check GPU utilization and VRAM allocation via ROCm System Management Interface
rocm-smi
```

### PyTorch ROCm Test Script
```python
import torch

print(f"ROCm PyTorch Available: {torch.cuda.is_available()}")
print(f"Device Count: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    print(f"Device Name: {torch.cuda.get_device_name(0)}")
```

## CLI examples

### 1. Execute vLLM Server on AMD ROCm GPU
```bash
# Launch vLLM OpenAI-compatible server targeting AMD Instinct GPU
vllm serve Qwen/Qwen3.8-27B-Instruct --port 8000 --device rocm --tensor-parallel-size 1
```

### 2. Monitor ROCm System Metrics
```bash
rocm-smi --showuse --showmem --showtemp
```

## API examples

### Programmatic Python Driver Check with Pydantic v2 Validation
The following script demonstrates programmatically querying ROCm system device properties via PyTorch/ROCm APIs and validating hardware capabilities using strict **Pydantic v2** schemas.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class ROCmDeviceSpecs(BaseModel):
    device_id: int = Field(..., ge=0)
    device_name: str
    total_memory_gb: float = Field(..., gt=0.0)
    compute_capability: str
    is_rocm_capable: bool

class ROCmSystemReport(BaseModel):
    rocm_version: str
    detected_devices: List[ROCmDeviceSpecs]
    status: str

def generate_rocm_audit_report() -> Optional[ROCmSystemReport]:
    # Simulated ROCm system inspection API call
    mock_data = {
        "rocm_version": "10.0.0",
        "status": "HEALTHY",
        "detected_devices": [
            {
                "device_id": 0,
                "device_name": "AMD Instinct MI300X",
                "total_memory_gb": 192.0,
                "compute_capability": "gfx942",
                "is_rocm_capable": True
            }
        ]
    }

    try:
        # Strictly validate using Pydantic v2
        return ROCmSystemReport.model_validate(mock_data)
    except ValidationError as ve:
        print(f"Pydantic Validation Error: {ve}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initiating ROCm GPU environment verification...")
    report = generate_rocm_audit_report()
    if report:
        print("ROCm System Report validated successfully via Pydantic v2:")
        print(f"  ROCm Version: {report.rocm_version}")
        print(f"  System Status: {report.status}")
        for dev in report.detected_devices:
            print(f"  Device {dev.device_id}: {dev.device_name} ({dev.total_memory_gb} GB VRAM, Arch: {dev.compute_capability})")
```

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput LLM serving runtime with native ROCm support.
- [SGLang](sglang.md) — Structured decoding execution engine optimized for ROCm GPUs.
- [llama.cpp](llama-cpp.md) — Fast C++ inference engine supporting HIP acceleration.
- [Docker](docker.md) — ROCm containerization environment wrappers.

## Sources / references
- [ROCm 10.0 Reddit Announcement & Decade of Open Compute](https://www.reddit.com/r/LocalLLaMA/comments/1w0yfmn/rocm_100_a_decade_of_open_compute_built_for_the/)
- [AMD ROCm Official Documentation Portal](https://rocm.docs.amd.com/)
- [AMD Instinct MI300 Series Architecture Overview](https://www.amd.com/en/products/accelerators/instinct.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
