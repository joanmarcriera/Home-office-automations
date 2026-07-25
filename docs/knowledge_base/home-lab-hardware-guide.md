# Home Lab Hardware Guide

## What it is
A comprehensive reference for home lab hardware configurations optimized for AI-assisted automation and self-hosting in late August 2026. This guide details specific compute profiles, VRAM requirements for local LLMs, and hardware-accelerated transcoding, focusing on the hybrid architecture of persistent servers (Intel/AMD) and high-performance development machines (Apple Silicon M5/M6 and Nvidia RTX 50-series).

## What problem it solves
Managing a modern home lab requires balancing power efficiency, cost, and raw inference performance. This guide solves the "placement problem"—deciding whether a workload (e.g., a 70B model vs. a 7B model) should run on a low-power N100 node, a dedicated RTX GPU server, or a unified memory MacBook. It prevents resource bottlenecks and optimizes the lab for "Invisible Kubernetes" operations.

## Where it fits in the stack
This is a **Knowledge Base** document sitting at the **Infrastructure Layer**. It provides the physical foundation upon which the entire Multi-Agent KnowledgeOps stack (Docker, K3s, n8n, Ollama) is built.

## Typical use cases

### Model Routing and Placement
- **Low-Latency Inference**: Running 3-8B models (Llama 4, Qwen 3.6) on RTX 4060/5070 GPUs for sub-second agent responses.
- **Large Context Windows**: Utilizing Apple Silicon's unified memory (M5/M6 48GB+) for 32B-70B models with 128k+ context windows.
- **Background Tasks**: Offloading audio transcription (Whisper) and image generation (Flux) to dedicated GPU servers.

### VRAM and Memory Capacity Planning
| Model Size | Min VRAM (Q4_K_M) | Hardware Recommendation |
| :--- | :--- | :--- |
| **1-3B** | 2-3 GB | Raspberry Pi 5+, Intel N100 |
| **7-8B** | 5-6 GB | RTX 4060 8GB, M5 16GB, RTX 5060 |
| **13-14B** | 9-10 GB | RTX 4060 Ti 16GB, M5 24GB, RTX 5070 |
| **32-35B** | 20-22 GB | RTX 3090/4090/5080, M5 36GB+ |
| **70B+** | 40 GB+ | 2x RTX 3090/4090, RTX 5090, M5 Max 64GB+ |

## Strengths
- **Hybrid Performance**: Combines the 24/7 reliability of x86 servers with the burst inference power of Apple Silicon.
- **Unified Memory**: Apple's architecture allows for massive context windows that consumer GPUs (limited to 24GB) cannot match without multi-GPU setups.
- **Efficiency**: Highlights "value kings" like the Intel N100 for persistent, non-inference services.
- **Native Acceleration**: Leverage AVX-512 on modern CPUs for significantly faster CPU-based inference.

## Limitations
- **VRAM Bottlenecks**: Consumer GPUs are strictly limited by their fixed memory pools, requiring aggressive quantization (Q4/Q5) for larger models.
- **Power and Heat**: Dedicated GPU servers can consume 300W+ under load, necessitating cooling and power management planning.
- **Apple Silicon Cost**: While efficient, the "Apple Tax" on RAM upgrades remains a significant entry barrier for high-memory configurations.

## When to use it
- Use this guide when planning a new home lab build or upgrading existing hardware to support frontier models like Claude 5.1 or GPT-5.5.
- Use it to calibrate your [Model Routing Guide](../knowledge_base/model_routing_guide.md) based on your specific VRAM availability.

## When not to use it
- Do not use this for enterprise-grade data center planning where power delivery and rack-scale management require different standards.
- Not intended for purely cloud-based setups where local hardware constraints do not apply.

## Getting started

### 1. The Value Baseline (Intel N100 / N200)
For persistent services like n8n, Home Assistant, and Paperless-ngx, the **Intel N100** mini PC is the 2026 standard.
- **Pros**: 6W-15W TDP, AVX-512 support, integrated QuickSync for 4K transcoding.
- **Ideal For**: Lightweight Docker services and 1B-3B "helper" LLMs.

### 2. The SBC Standard (Raspberry Pi 5+ / 500)
The **Raspberry Pi 5+** (or Pi 500) serves as the primary "Edge" device.
- **AVX-equivalent**: Utilizing specialized ARM instructions for improved local processing.
- **Use case**: External-DNS, secondary VPN nodes, and low-priority sensor ingestion.

### 3. The Inference King (RTX 4060 Ti 16GB & RTX 5070 16GB)
The 16GB variants of the **RTX 4060 Ti** and the new **RTX 5070** are the recommended mid-range entry points for 24/7 inference servers due to their high VRAM-per-watt efficiency.

## CLI examples

### Hardware Inventory Check
```bash
# Check for AVX-512 support on Linux
grep -o "avx512" /proc/cpuinfo | head -n 1

# List GPU VRAM and utilization
nvidia-smi --query-gpu=memory.total,memory.free,utilization.gpu --format=csv
```

### hw-check.py (Custom Diagnostic)
```bash
# Verify local hardware readiness for a specific model size
python3 scripts/hw-check.py --model-size 7b --quant q4_k_m
```

## API examples

### Programmatic Resource Routing (LiteLLM)
Configure your hardware endpoints to be consumed by agents:
```yaml
model_list:
  - model_name: "local-fast"
    litellm_params:
      model: "ollama/qwen2.5:7b"
      api_base: "http://n100-server:11434"
  - model_name: "local-large"
    litellm_params:
      model: "ollama/llama3.3:70b"
      api_base: "http://macbook-m5:11434"
```

### Checking Hardware Health via Home Assistant
```json
{
  "action": "GET",
  "endpoint": "/api/states/sensor.rtx_4060_temperature",
  "expected_range": "30-80"
}
```

## Related tools / concepts
- [Ollama](../services/ollama.md) — The primary engine for running LLMs on this hardware.
- [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md) — Orchestrating the hardware nodes.
- [LiteLLM](../services/litellm.md) — Unifying multi-machine hardware endpoints.
- [MLX](../tools/infrastructure/mlx.md) — Specialized framework for Apple Silicon hardware.
- [NVENC / QuickSync](../services/jellyfin.md) — Hardware-accelerated video transcoding.
- [Proxmox](../tools/infrastructure/proxmox.md) — Virtualizing hardware resources for the lab.
- [Whisper](../services/whisper.md) — Utilizing GPU for high-speed audio transcription.
- [AVX-512 Requirements](../knowledge_base/patterns/fine-tuning-open-models.md) — Deep dive into CPU instruction sets.

## Sources / References
- [Intel N100 Technical Specifications](https://ark.intel.com/content/www/us/en/ark/products/231803/intel-processor-n100-6m-cache-up-to-3-40-ghz.html)
- [NVIDIA GeForce RTX 50-Series Power Efficiency Guide](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/)
- [Apple Developer: Metal Performance Shaders](https://developer.apple.com/metal/pytorch/)
- [Raspberry Pi 5+ Performance Benchmarks (2026)](https://www.raspberrypi.com/news/pi-5-performance/)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
