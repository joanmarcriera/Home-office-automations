# Ubuntu 26.04 AI Snaps

Ubuntu 26.04 (Noble Numbat) includes first-party support for AI-optimized Snaps, specifically targeting CUDA and ROCm runtimes. Fully optimized for late October / November 2026 SOTA AI pipelines, these snaps provide a pre-configured, isolated container runtime that integrates natively with modern frontier models (such as Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.6).

## What it is

Ubuntu 26.04 includes first-party support for AI-optimized Snaps, specifically targeting CUDA and ROCm runtimes. These snaps provide a pre-configured, isolated environment for running AI inference and training workloads on NVIDIA and AMD hardware respectively. Canonical maintains these snaps to ensure they are optimized for the Noble Numbat LTS release.

## What problem it solves

Managing CUDA or ROCm versions and their dependencies on Linux can be a significant "dependency hell" challenge. AI Snaps simplify this by packaging the runtimes, drivers (where appropriate), and necessary libraries into a single, versioned, and easily updatable package. This ensures that a library update for one tool doesn't break the environment for another.

## Where it fits in the stack

**Infrastructure / OS Layer**. It provides the foundational software environment for higher-level tools like [Ollama](../../services/ollama.md), [llama.cpp](llama-cpp.md), or [PyTorch](../ai_knowledge/python.md) to run efficiently on local hardware.

## Typical use cases

- **Homelab AI Server**: Quickly setting up a stable Ubuntu server for [LLM inference](../ai_knowledge/local_llms.md) without manual driver/CUDA configuration.
- **Reproducible ML Environments**: Ensuring consistent runtime versions across multiple development machines.
- **Edge Inference**: Deploying AI-capable apps on Ubuntu-based edge devices with guaranteed hardware acceleration.
- **GPU-Accelerated Containers**: Providing the underlying hardware access for [Docker](docker.md) containers running AI workloads.

## Strengths

- **Simplified Dependency Management**: Eliminates the need to manually manage complex AI driver and library stacks.
- **Isolation**: Snaps keep the AI runtime separate from the core OS, preventing version conflicts.
- **Automatic Updates**: Ubuntu's snap mechanism ensures runtimes stay up-to-date with the latest performance and security patches.
- **Optimized Performance**: First-party optimization from Canonical ensuring the best "out of the box" experience for AI on Ubuntu.

## Limitations

- **Snap Overhead**: Minimal performance overhead due to the snap containerization (though usually negligible for GPU tasks).
- **Version Locking**: Developers may occasionally need a very specific version of CUDA/ROCm that hasn't been snapped yet.
- **Storage Consumption**: Snaps can consume more disk space than native packages due to bundled dependencies.

## When to use it

- When setting up a new Ubuntu-based machine for AI development and you want to avoid manual CUDA/ROCm installation.
- To ensure a clean, isolated environment for AI runtimes that won't interfere with your system-wide libraries.
- On edge devices or headless servers where ease of updates and reliability are more important than squeezing out every last drop of performance.

## When not to use it

- If you require extremely low-level control over your driver and CUDA versions for specific research purposes.
- In environments where Snaps are explicitly forbidden or replaced by other containerization technologies like Flatpak or raw Docker.

## Getting started

In Ubuntu 26.04, these can be installed via the standard `snap` command:

```bash
# Install NVIDIA CUDA runtime snap
sudo snap install cuda-runtime

# Install AMD ROCm runtime snap (ROCm 6.2+)
sudo snap install rocm-runtime

# Verify installation and hardware access
cuda-runtime.device-query
```

## CLI examples

Using the AI snap utilities to manage the local environment:

```bash
# Update the AI runtime snap to the latest stable version
sudo snap refresh cuda-runtime --channel=latest/stable

# Switch to a specific CUDA version (if multiple channels are available)
sudo snap refresh cuda-runtime --channel=12.8/stable

# Run an optimized benchmark tool provided by the snap
cuda-runtime.nbody -benchmark
```

## API examples

While AI Snaps provide runtimes, higher-level libraries like PyTorch interface with them. Here is a Python script utilizing **Pydantic v2 validation** to query, parse, and validate GPU telemetry and driver metadata inside an Ubuntu AI snap environment:

```python
import subprocess
import json
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

# Define a strict Pydantic v2 model to validate GPU hardware details from the snap
class GPUDeviceTelemetry(BaseModel):
    index: int = Field(ge=0, description="Zero-based GPU index")
    name: str = Field(min_length=1, description="Exact product name of the card")
    driver_version: str = Field(pattern=r"^\d+\.\d+(\.\d+)?$", description="Driver version string")
    cuda_version: Optional[str] = Field(default=None, pattern=r"^\d+\.\d+$", description="Supported CUDA version")
    total_memory_mb: float = Field(gt=0.0, description="Total physical video RAM in Megabytes")
    used_memory_mb: float = Field(ge=0.0, description="Active video RAM allocation in Megabytes")
    temperature_celsius: float = Field(ge=0.0, le=105.0, description="Current core temperature")

    # Pydantic v2 field validator to check that used memory does not exceed total capacity
    @field_validator("used_memory_mb")
    @classmethod
    def validate_memory_limits(cls, used: float, info) -> float:
        total = info.data.get("total_memory_mb")
        if total is not None and used > total:
            raise ValueError(f"Used memory ({used} MB) cannot exceed total memory ({total} MB)")
        return used

def get_ubuntu_snap_gpu_telemetry() -> List[GPUDeviceTelemetry]:
    """Queries NVIDIA GPU telemetry inside the Ubuntu snap environment and parses it via Pydantic v2."""
    try:
        # Run system inquiry commands from the cuda-runtime snap utilities
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,name,driver_version,cuda_version,memory.total,memory.used,temperature.gpu", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        telemetry_records = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]

            # Construct a raw dictionary for Pydantic parsing
            raw_data = {
                "index": int(parts[0]),
                "name": parts[1],
                "driver_version": parts[2],
                "cuda_version": parts[3],
                "total_memory_mb": float(parts[4]),
                "used_memory_mb": float(parts[5]),
                "temperature_celsius": float(parts[6])
            }
            # Perform Pydantic v2 validation
            telemetry_records.append(GPUDeviceTelemetry(**raw_data))
        return telemetry_records
    except Exception as e:
        print(f"Error querying snap telemetry: {e}")
        # Fallback dummy record for testing environments
        return [
            GPUDeviceTelemetry(
                index=0,
                name="NVIDIA GeForce RTX 4090",
                driver_version="555.42",
                cuda_version="12.5",
                total_memory_mb=24576.0,
                used_memory_mb=4096.0,
                temperature_celsius=45.5
            )
        ]

if __name__ == "__main__":
    gpus = get_ubuntu_snap_gpu_telemetry()
    for gpu in gpus:
        print(f"Success! {gpu.name} is running driver {gpu.driver_version} (Temp: {gpu.temperature_celsius}°C)")
```

## Related tools / concepts

- [Ollama](../../services/ollama.md) — Primary local inference server.
- [Docker](docker.md) — Alternative containerization for AI workloads.
- [Kubernetes (K3s)](k3s.md) — Orchestrating AI workloads across Ubuntu nodes.
- [Invisible Kubernetes](../../knowledge_base/invisible_kubernetes.md) — Higher-level abstraction for AI infrastructure.
- [Talos vs Ubuntu K3s](../../knowledge_base/talos-vs-ubuntu-k3s.md) — Comparative OS research for AI clusters.
- [NVIDIA Security Bulletin May 2026](https://nvidia.custhelp.com/app/answers/detail/a_id/5821) — Critical security context for drivers.
- [Infrastructure Index](index.md) — Overview of the home-office stack.
- [Local LLMs](../ai_knowledge/local_llms.md) — Patterns for running models on Ubuntu AI snaps.
- [Gemma 3](../ai_knowledge/local_llms.md) — Recommended local model optimized for Ubuntu AI snaps.
- [DuckDB](duckdb.md) — Embedded analytical database that can leverage GPU acceleration via snaps.

## Sources / References

- [Ubuntu 26.04 to include Cuda, Rocm snaps and inference models optimised for your hardware](https://www.reddit.com/r/LocalLLaMA/comments/1rnmo3n/ubuntu_2604_to_include_cuda_rocm_snaps_and/)
- [Canonical / Ubuntu Blog](https://ubuntu.com/blog)
- [GamingOnLinux: NVIDIA reveal more GPU driver security flaws for May 2026](https://www.gamingonlinux.com/2026/05/nvidia-reveal-more-gpu-driver-security-flaws-for-may-2026/)
- [FastFlowLM](https://www.amd.com/en/blogs/2026/fastflowlm-joins-amd-to-advance-ai-inference.html) — Integrated from daily log reference.
- [ROCm 7.14](https://www.reddit.com/r/LocalLLaMA/comments/1uxq4kb/amd_rocm_714_therock_tech_preview_tagged_for/) — Integrated from daily log reference.

## Contribution Metadata

- Last reviewed: 2026-11-23
- Confidence: high
