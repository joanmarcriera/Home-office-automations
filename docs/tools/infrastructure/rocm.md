# ROCm

## What it is
ROCm (Radeon Open Compute) is AMD's open-source software platform and unified driver framework for GPU computing, deep learning acceleration, and high-performance computing (HPC). Reaching landmark milestone **ROCm 10.0** in early 2027 (celebrating a decade of open compute), ROCm provides full ecosystem parity and hardware acceleration for training and inferencing frontier open-weights models (such as [Qwen 3.8](../ai_knowledge/qwen.md), [Gemma 4](../ai_knowledge/gemma.md), and [Llama 4](../ai_knowledge/local_llms.md)) across AMD Instinct MI300/MI400 series accelerators as well as consumer Radeon RX 7000/8000 series GPUs.

## What problem it solves
Proprietary vendor lock-in has historically restricted enterprise and self-hosted AI deployments to single-hardware vendor ecosystems. ROCm solves this by delivering open HIP (Heterogeneous-compute Interface for Portability) runtimes, native PyTorch/JAX hardware acceleration, and seamless compatibility for local serving engines like [vLLM](vllm.md), [llama.cpp](llama-cpp.md), and [SGLang](sglang.md) on AMD GPUs.

## Where it fits in the stack
**Infrastructure & Accelerator Compute Layer**. ROCm serves as the underlying GPU compute driver layer beneath machine learning frameworks and local LLM serving engines.

## Typical use cases
- **High-Throughput Enterprise Inference**: Serving large MoE models ([Qwen 3.8 Max](../ai_knowledge/qwen.md), [DeepSeek-V4](../providers/deepseek.md)) on AMD Instinct GPU clusters with vLLM tensor parallelism.
- **Consumer Workstation Local AI**: Running GGUF/EXL2 quantized models locally on Radeon GPUs using ROCm-compiled llama.cpp or Ollama endpoints.
- **Sovereign AI Infrastructure**: Deploying open-source GPU clusters with full stack transparency and zero proprietary licensing overhead.
- **FastMCP 3.1 Accelerated Agents**: Provisioning GPU acceleration for multi-agent swarms using local hardware.

## Strengths
- **Fully Open-Source Ecosystem**: Complete driver, compiler (LLVM-based), and kernel stack source availability.
- **Unified HIP Abstraction**: Simple porting layer converting existing CUDA C++ codebases directly to AMD HIP.
- **Native PyTorch & vLLM Integration**: Out-of-the-box support in upstream PyTorch, vLLM, FlashAttention, and Triton compiler backends.
- **Broad Hardware Scaling**: Supports scale-out topology from single workstation Radeon GPUs up to massive exascale Instinct clusters.

## Limitations
- **Consumer GPU Driver Tuning**: Configuring ROCm on non-official consumer Linux distributions requires specific environment flags (`HSA_OVERRIDE_GFX_VERSION`).
- **Legacy Kernel Porting Overhead**: Custom proprietary CUDA extensions still require HIP translation before native execution.

## When to use it
- When building AI infrastructure on AMD Radeon or AMD Instinct GPU hardware.
- When requiring a fully open-source hardware compute stack without proprietary runtime dependencies.
- When deploying high-throughput model serving nodes with PyTorch, vLLM, or llama.cpp on AMD hardware.

## When not to use it
- When operating exclusively on NVIDIA GPU infrastructure (use CUDA / TensorRT-LLM instead).
- When running CPU-only edge workloads without discrete GPU hardware.

## Getting started
ROCm can be installed via system package manager or utilized within pre-built Docker containers.

```bash
# Verify ROCm driver installation and GPU device availability
rocm-smi

# Run official PyTorch ROCm container
docker run -it --network=host --device=/dev/kfd --device=/dev/dri --group-add render \
  rocm/pytorch:latest python3 -c "import torch; print('ROCm available:', torch.cuda.is_available())"
```

## CLI examples

### 1. GPU Utilization Monitoring with `rocm-smi`
```bash
# Display GPU temperature, VRAM usage, and power consumption
rocm-smi --showuse --showtemp --showmeminfo vram
```

### 2. Building Llama.cpp with Native ROCm HIP Support
```bash
# Clone and build llama.cpp optimized for AMD GPUs
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DGGML_HIPBLAS=ON -AMDGPU_TARGETS=gfx1100
cmake --build build --config Release -j$(nproc)
```

### 3. Serving vLLM Engine on AMD Instinct GPU
```bash
# Serve Qwen 3.8 27B model via vLLM with ROCm backend
vllm serve Qwen/Qwen3.8-27B --port 8000 --device hip
```

## API examples

### Python Integration with PyTorch ROCm Backend Verification
```python
import torch

def check_rocm_environment():
    is_available = torch.cuda.is_available()
    device_count = torch.cuda.device_count() if is_available else 0
    device_name = torch.cuda.get_device_name(0) if is_available else "N/A"

    # In PyTorch ROCm builds, torch.version.hip indicates the ROCm version
    hip_version = getattr(torch.version, 'hip', None)

    return {
        "rocm_active": is_available and hip_version is not None,
        "device_count": device_count,
        "device_name": device_name,
        "hip_version": hip_version
    }

if __name__ == "__main__":
    env_info = check_rocm_environment()
    print("ROCm Compute Environment Status:", env_info)
```

### Programmatic Python Integration with Pydantic v2 Telemetry Validation
The following script demonstrates querying ROCm GPU telemetry and strictly validating state using **Pydantic v2** models.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class ROCmGpuMetrics(BaseModel):
    gpu_id: int = Field(..., description="GPU device index")
    gpu_name: str = Field(..., description="Device name (e.g. AMD Instinct MI300X or Radeon RX 7900 XTX)")
    vram_used_mb: float = Field(..., description="Allocated VRAM memory in megabytes")
    vram_total_mb: float = Field(..., description="Total available VRAM memory in megabytes")
    gpu_utilization_pct: float = Field(..., description="Compute core utilization percentage")
    temperature_c: float = Field(..., description="GPU die temperature in degrees Celsius")

class ROCmTelemetryReport(BaseModel):
    rocm_version: str = Field(..., description="ROCm release version (e.g. 10.0.0)")
    driver_version: str
    gpus: List[ROCmGpuMetrics]

def parse_rocm_telemetry(raw_data: dict) -> Optional[ROCmTelemetryReport]:
    try:
        return ROCmTelemetryReport.model_validate(raw_data)
    except ValidationError as ve:
        print(f"Pydantic Validation Error for ROCm telemetry: {ve}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Validating ROCm GPU telemetry metrics report...")

    sample_telemetry = {
        "rocm_version": "10.0.0",
        "driver_version": "6.12.0",
        "gpus": [
            {
                "gpu_id": 0,
                "gpu_name": "AMD Instinct MI300X",
                "vram_used_mb": 45200.0,
                "vram_total_mb": 196608.0,
                "gpu_utilization_pct": 87.5,
                "temperature_c": 54.0
            }
        ]
    }

    validated = parse_rocm_telemetry(sample_telemetry)
    if validated:
        print("ROCm Telemetry Validated Successfully:")
        print(f"  ROCm Release: {validated.rocm_version}")
        print(f"  GPU Count: {len(validated.gpus)}")
        gpu = validated.gpus[0]
        print(f"  Device [0]: {gpu.gpu_name} | VRAM: {gpu.vram_used_mb}/{gpu.vram_total_mb} MB | Temp: {gpu.temperature_c}°C")
    else:
        print("Validation failed.", file=sys.stderr)
```

## Related tools / concepts
- [vLLM](vllm.md) — High-throughput serving engine supporting AMD ROCm.
- [llama.cpp](llama-cpp.md) — Cross-platform C++ engine with GGML/HIPBLAS backend.
- [FreeToken](freetoken.md) — Shared KV-cache inference accelerator daemon.
- [ExLlamaV3](exllamav3.md) — Fast GPU inference engine for quantized models.
- [Docker](docker.md) — Containerization platform for deploying ROCm ML runtimes.

## Sources / references
- [Reddit ROCm 10.0 Announcement on LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1w0yfmn/rocm_100_a_decade_of_open_compute_built_for_the/)
- [AMD ROCm Official Documentation](https://rocm.docs.amd.com/)
- [PyTorch ROCm Installation Guide](https://pytorch.org/get-started/locally/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
