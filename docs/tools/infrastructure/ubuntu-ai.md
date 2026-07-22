# Ubuntu 26.04 AI Snaps

Ubuntu 26.04 (Noble Numbat) includes first-party support for AI-optimized Snaps, specifically targeting CUDA and ROCm runtimes.

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

While AI Snaps provide runtimes, higher-level libraries like PyTorch interface with them. Here is how to check for hardware acceleration in a Python script running within the snap environment:

```python
import torch

# Check if the CUDA runtime snap is providing hardware access
if torch.cuda.is_available():
    print(f"Device Name: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Version: {torch.version.cuda}")
else:
    print("CUDA not available. Check your snap installation and drivers.")
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

- Last reviewed: 2026-07-21
- Confidence: high
