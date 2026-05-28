# Ubuntu 26.04 AI Snaps

## What it is
Ubuntu 26.04 (Noble Numbat successor) includes first-party support for AI-optimized Snaps, specifically targeting CUDA and ROCm runtimes. These snaps provide a pre-configured, isolated environment for running AI inference and training workloads on NVIDIA and AMD hardware respectively.

## What problem it solves
Managing CUDA or ROCm versions and their dependencies on Linux can be a significant "dependency hell" challenge. AI Snaps simplify this by packaging the runtimes, drivers (where appropriate), and necessary libraries into a single, versioned, and easily updatable package.

## Where it fits in the stack
**Infrastructure / OS Layer**. It provides the foundational software environment for higher-level tools like Ollama, llama.cpp, or PyTorch to run efficiently on local hardware.

## Typical use cases
- **Homelab AI Server**: Quickly setting up a stable Ubuntu server for LLM inference without manual driver/CUDA configuration.
- **Reproducible ML Environments**: Ensuring consistent runtime versions across multiple development machines.
- **Edge Inference**: Deploying AI-capable apps on Ubuntu-based edge devices with guaranteed hardware acceleration.

## Getting started
In Ubuntu 26.04, these can be installed via the standard `snap` command:

```bash
# Install NVIDIA CUDA runtime snap
sudo snap install cuda-runtime

# Install AMD ROCm runtime snap
sudo snap install rocm-runtime
```

Higher-level tools can then interface with these snaps to access hardware acceleration.

## May 2026 Security Baseline: NVIDIA Driver Update

As of May 19, 2026, a significant wave of 12 security vulnerabilities (including CVE-2026-24187 and CVE-2026-24190) has been disclosed affecting the NVIDIA display driver on Linux. These vulnerabilities include High-severity issues such as use-after-free and heap buffer overflows that could lead to code execution or escalation of privileges.

### Recommended Versions (May 2026)
To ensure system security, users must update to the following driver versions or later:
- **GeForce R590**: 590.48.01
- **GeForce R580**: 580.126.09
- **NVIDIA RTX / Quadro R595**: 595.71.05
- **NVIDIA RTX / Quadro R535**: 535.309.01

**Warning**: The **R570 driver series** has been designated as **End-of-Life (EOL)** and will not receive security updates for these vulnerabilities. Users on R570 should migrate to a supported branch immediately.

## Strengths
- **Simplified Dependency Management**: Eliminates the need to manually manage complex AI driver and library stacks.
- **Isolation**: Snaps keep the AI runtime separate from the core OS, preventing version conflicts.
- **Automatic Updates**: Ubuntu's snap mechanism ensures runtimes stay up-to-date with the latest performance and security patches.
- **Optimized Performance**: First-party optimization from Canonical ensuring the best "out of the box" experience for AI on Ubuntu.

## Limitations
- **Snap Overhead**: Minimal performance overhead due to the snap containerization (though usually negligible for GPU tasks).
- **Version Locking**: Developers may occasionally need a very specific version of CUDA/ROCm that hasn't been snapped yet.

## When to use it
- When setting up a new Ubuntu-based machine for AI development and you want to avoid manual CUDA/ROCm installation.
- To ensure a clean, isolated environment for AI runtimes that won't interfere with your system-wide libraries.
- On edge devices or headless servers where ease of updates and reliability are more important than squeezing out every last drop of performance.

## When not to use it
- If you require extremely low-level control over your driver and CUDA versions for specific research purposes.
- In environments where Snaps are explicitly forbidden or replaced by other containerization technologies like Flatpak or raw Docker (though Snaps can complement Docker).

## Licensing and cost
- **Open Source / Free**: Part of the standard Ubuntu distribution.

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [Local LLMs](../ai_knowledge/local_llms.md)
- [Infrastructure Index](index.md)
- [Docker](docker.md)
- [Kubernetes (K3s)](k3s.md)
- [Invisible Kubernetes](../../knowledge_base/invisible_kubernetes.md)
- [Talos vs Ubuntu K3s](../../knowledge_base/talos-vs-ubuntu-k3s.md)
- [Google Axion](../../knowledge_base/google_axion.md)
- [NVIDIA Security Bulletin May 2026](https://nvidia.custhelp.com/app/answers/detail/a_id/5821)

## Sources / References
- [Ubuntu 26.04 to include Cuda, Rocm snaps and inference models optimised for your hardware](https://www.reddit.com/r/LocalLLaMA/comments/1rnmo3n/ubuntu_2604_to_include_cuda_rocm_snaps_and/)
- [Canonical / Ubuntu Blog](https://ubuntu.com/blog)
- [GamingOnLinux: NVIDIA reveal more GPU driver security flaws for May 2026](https://www.gamingonlinux.com/2026/05/nvidia-reveal-more-gpu-driver-security-flaws-for-may-2026/)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
