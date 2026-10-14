# Home Lab Hardware Guide

## What it is
A comprehensive reference for home lab hardware configurations optimized for AI-assisted automation and self-hosting in early January 2027. This guide details specific compute profiles, VRAM requirements for local LLMs, and hardware-accelerated transcoding, focusing on the hybrid architecture of persistent servers (Intel/AMD) and high-performance development machines (Apple Silicon M5/M6 and Nvidia RTX 50-series).

## What problem it solves
Managing a modern home lab requires balancing power efficiency, cost, and raw inference performance. This guide solves the "placement problem"—deciding whether a workload (e.g., a 70B model vs. a 7B model) should run on a low-power N100 node, a dedicated RTX GPU server, or a unified memory MacBook. It prevents resource bottlenecks and optimizes the lab for "Invisible Kubernetes" operations.

## Where it fits in the stack
This is a **Knowledge Base** document sitting at the **Infrastructure Layer**. It provides the physical foundation upon which the entire Multi-Agent KnowledgeOps stack (Docker, K3s, n8n, Ollama) is built.

```
+-----------------------------------------------------------------------------------+
|                        Home Lab Hardware Topology (2027)                           |
+-----------------------------------------------------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
        v                                 v                                 v
+-----------------------+     +-----------------------+     +-----------------------+
|  Persistent Services  |     |   Dedicated GPU Server|     | Apple Silicon Unified |
|  Intel N100 / N200    |     |   x86 + RTX 4060/5070   |     | M5/M6 Pro / Max Node  |
|                       |     |                       |     |                       |
| - K3s Control Plane   |     | - Fast 3-14B LLMs     |     | - 32-70B+ LLMs        |
| - Home Assistant      |     | - Whisper Transcription|     | - 128k Context Windows|
| - Paperless-ngx       |     | - Flux Image Gen      |     | - MLX Local Studio    |
| - N8n & PostgreSQL    |     | - NVENC Transcoding   |     | - Unified RAM Pool    |
| - 6W-15W Baseline TDP |     | - Sub-10ms Inference  |     | - Ultra-Quiet Burst   |
+-----------------------+     +-----------------------+     +-----------------------+
```

## Typical use cases

### Model Routing and Placement
- **Low-Latency Inference**: Running 3-8B models (DeepSeek-V4, Qwen 3.6 VL) on RTX 4060/5070 GPUs for sub-second agent responses.
- **Large Context Windows**: Utilizing Apple Silicon's unified memory (M5/M6 48GB+) for 32B-70B models with 128k+ context windows.
- **Background Tasks**: Offloading audio transcription (Whisper) and image generation (Flux) to dedicated GPU servers.

### VRAM and Memory Capacity Planning
| Model Size | Min VRAM (Q4_K_M) | Recommended Hardware Profile | Power Draw (Idle / Peak) | Target Latency / TPO |
| :--- | :--- | :--- | :--- | :--- |
| **1-3B** | 2-3 GB | Raspberry Pi 5+, Intel N100 | 5W / 15W | > 60 tokens/sec |
| **7-8B** | 5-6 GB | RTX 4060 8GB, M5 16GB, RTX 5060 | 12W / 115W | > 45 tokens/sec |
| **13-14B** | 9-10 GB | RTX 4060 Ti 16GB, M5 24GB, RTX 5070 | 15W / 165W | > 35 tokens/sec |
| **32-35B** | 20-22 GB | RTX 3090/4090/5080, M5 36GB+ | 25W / 320W | > 25 tokens/sec |
| **70B+** | 40 GB+ | 2x RTX 3090/4090, RTX 5090, M5 Max 64GB+ | 45W / 650W | > 18 tokens/sec |

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
- Use this guide when planning a new home lab build or upgrading existing hardware to support frontier models like Claude 5.6 or GPT-5.6.
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

## FastMCP 3.1 Hardware Resource Management Server
The following FastMCP 3.1 server provides agentic tools to inspect homelab hardware nodes, query GPU memory state, evaluate model placement readiness, and track thermal metrics.

```python
from typing import Dict, List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(name="homelab-hardware-monitor")

class HardwareNodeStatus(BaseModel):
    node_id: str = Field(..., description="Unique node identifier")
    platform: str = Field(..., description="Architecture platform (x86_gpu, apple_silicon, low_power_x86)")
    cpu_utilization_pct: float = Field(..., ge=0.0, le=100.0)
    total_ram_gb: float = Field(..., ge=1.0)
    free_ram_gb: float = Field(..., ge=0.0)
    vram_total_gb: float = Field(default=0.0, ge=0.0)
    vram_free_gb: float = Field(default=0.0, ge=0.0)
    gpu_temp_celsius: Optional[float] = Field(default=None)

@mcp.tool()
def get_cluster_hardware_summary() -> List[HardwareNodeStatus]:
    """Retrieves current hardware utilization across all homelab compute nodes."""
    return [
        HardwareNodeStatus(
            node_id="n100-master",
            platform="low_power_x86",
            cpu_utilization_pct=14.2,
            total_ram_gb=16.0,
            free_ram_gb=9.5,
            vram_total_gb=0.0,
            vram_free_gb=0.0,
        ),
        HardwareNodeStatus(
            node_id="rtx-rig-01",
            platform="x86_gpu",
            cpu_utilization_pct=22.8,
            total_ram_gb=64.0,
            free_ram_gb=48.2,
            vram_total_gb=16.0,
            vram_free_gb=11.4,
            gpu_temp_celsius=52.0,
        ),
        HardwareNodeStatus(
            node_id="mac-studio-m6",
            platform="apple_silicon",
            cpu_utilization_pct=8.5,
            total_ram_gb=64.0,
            free_ram_gb=38.0,
            vram_total_gb=48.0,  # Effective unified memory pool
            vram_free_gb=28.5,
            gpu_temp_celsius=41.0,
        ),
    ]

@mcp.tool()
def evaluate_model_placement(
    model_name: str,
    required_vram_gb: float,
    allow_unified_memory: bool = True,
) -> Dict[str, str]:
    """Determines optimal node placement for an incoming model workload based on VRAM requirements."""
    nodes = get_cluster_hardware_summary()
    candidates = []

    for node in nodes:
        available_mem = node.vram_free_gb
        if node.platform == "apple_silicon" and allow_unified_memory:
            available_mem = node.free_ram_gb * 0.75

        if available_mem >= required_vram_gb:
            candidates.append((node.node_id, available_mem))

    if not candidates:
        return {"status": "REJECTED", "reason": f"No single node has {required_vram_gb} GB free VRAM/Unified RAM."}

    # Pick node with smallest adequate margin to preserve large nodes
    candidates.sort(key=lambda x: x[1])
    best_node = candidates[0][0]
    return {
        "status": "APPROVED",
        "target_node": best_node,
        "model_name": model_name,
        "required_vram_gb": str(required_vram_gb),
    }

if __name__ == "__main__":
    mcp.run()
```

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

### Python: Hardware Capacity & Routing Validator (Pydantic v2)
An executable, strict Pydantic v2 validation script to model and assess the homelab capacity of hardware nodes against local model VRAM and RAM constraints in early January 2027:

```python
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

class ComputePlatform(str, Enum):
    X86_GPU = "x86_gpu"
    APPLE_SILICON = "apple_silicon"
    LOW_POWER_X86 = "low_power_x86"
    EDGE_SBC = "edge_sbc"

class HardwareNode(BaseModel):
    node_name: str = Field(..., description="Name of the node in the homelab cluster")
    platform: ComputePlatform = Field(..., description="Underlying architecture / platform type")
    total_ram_gb: float = Field(..., ge=1.0, description="Total system RAM in Gigabytes")
    vram_gb: float = Field(default=0.0, ge=0.0, description="Available VRAM in Gigabytes")
    has_avx_512: bool = Field(default=False, description="Whether the CPU supports AVX-512 instructions")

class TargetModel(BaseModel):
    model_name: str = Field(..., description="Identifier name of the LLM")
    size_params_b: float = Field(..., gt=0.0, description="Model parameter size in Billions")
    quantization: str = Field(default="Q4_K_M", description="Quantization profile")
    estimated_memory_required_gb: float = Field(..., gt=0.0, description="Estimated VRAM/RAM required to run the model")

class HardwareRoutingEngine(BaseModel):
    nodes: Dict[str, HardwareNode] = Field(..., description="Active homelab hardware nodes")

    def find_capable_nodes(self, model: TargetModel) -> List[str]:
        capable = []
        for name, node in self.nodes.items():
            # If the platform is Apple Silicon, it can utilize unified memory (system RAM)
            available_mem = node.vram_gb if node.platform != ComputePlatform.APPLE_SILICON else (node.total_ram_gb * 0.75)

            if available_mem >= model.estimated_memory_required_gb:
                capable.append(name)
            elif node.platform == ComputePlatform.LOW_POWER_X86 and model.size_params_b <= 3.0:
                # Allow low-power CPU nodes to run tiny helper models if they have sufficient RAM
                if node.total_ram_gb >= (model.estimated_memory_required_gb + 2.0):
                    capable.append(name)
        return capable

# Example validation check:
if __name__ == "__main__":
    cluster = HardwareRoutingEngine(
        nodes={
            "n100-server": HardwareNode(node_name="n100-server", platform=ComputePlatform.LOW_POWER_X86, total_ram_gb=16.0, vram_gb=0.0, has_avx_512=True),
            "gpu-rig": HardwareNode(node_name="gpu-rig", platform=ComputePlatform.X86_GPU, total_ram_gb=32.0, vram_gb=16.0, has_avx_512=True),
            "macbook-m6": HardwareNode(node_name="macbook-m6", platform=ComputePlatform.APPLE_SILICON, total_ram_gb=48.0, vram_gb=0.0, has_avx_512=False)
        }
    )

    deepseek_v4_70b = TargetModel(model_name="deepseek-v4:70b", size_params_b=70.0, quantization="Q4_K_M", estimated_memory_required_gb=42.0)
    qwen_36_8b = TargetModel(model_name="qwen3.6:8b", size_params_b=8.0, quantization="Q4_K_M", estimated_memory_required_gb=6.0)

    print(f"Nodes capable of running DeepSeek-V4 70B: {cluster.find_capable_nodes(deepseek_v4_70b)}")
    print(f"Nodes capable of running Qwen 3.6 8B: {cluster.find_capable_nodes(qwen_36_8b)}")
```

### Programmatic Resource Routing (LiteLLM)
Configure your hardware endpoints to be consumed by agents:
```yaml
model_list:
  - model_name: "local-fast"
    litellm_params:
      model: "ollama/qwen3.6:8b"
      api_base: "http://n100-server:11434"
  - model_name: "local-large"
    litellm_params:
      model: "ollama/deepseek-v4:70b"
      api_base: "http://macbook-m6:11434"
```

### Checking Hardware Health via Home Assistant
```json
{
  "action": "GET",
  "endpoint": "/api/states/sensor.rtx_4060_temperature",
  "expected_range": "30-80"
}
```

## Operational Troubleshooting & Diagnostics

| Symptom | Probable Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **CUDA Out Of Memory (OOM)** | Model context window or KV cache exceeding physical GPU VRAM | `nvidia-smi` / `dmesg \| grep -i oom` | Reduce `num_ctx` in Ollama, switch to higher quantization (Q4_K_M -> Q3_K_S), or route to Apple Silicon node |
| **Thermal Throttling on Mini PC** | Dusty fan or inadequate air circulation on low-power chassis | `sensors` / `cat /sys/class/thermal/thermal_zone*/temp` | Clean dust filters, adjust fan curve in BIOS, or add external 120mm USB cooling fan |
| **P2P PCIe Bottleneck** | Dual-GPU setup running across PCIe Gen 3 x4 slots without NVLink | `nvidia-smi topo -m` | Re-align GPU slots to PCIe Gen 4/5 x8/x16, or switch to split-tensor parallelism over fast LAN |
| **AVX-512 Instruction Fallback** | CPU backend using slow fallback matrix instructions | `lscpu \| grep -i avx512` | Recompile llama.cpp with `-DGGML_AVX512=ON` flag explicitly set |

## Related tools / concepts
- [Ollama](../services/ollama.md) — The primary engine for running LLMs on this hardware.
- [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md) — Orchestrating the hardware nodes.
- [LiteLLM](../services/litellm.md) — Unifying multi-machine hardware endpoints.
- [MLX](../tools/infrastructure/mlx.md) — Specialized framework for Apple Silicon hardware.
- [NVENC / QuickSync](../services/jellyfin.md) — Hardware-accelerated video transcoding.
- [Infrastructure Architecture](../architecture/infrastructure.md) — Virtualizing hardware resources for the lab.
- [Whisper](../services/whisper.md) — Utilizing GPU for high-speed audio transcription.
- [AVX-512 Requirements](../knowledge_base/patterns/fine-tuning-open-models.md) — Deep dive into CPU instruction sets.

## Sources / references
- [Intel N100 Technical Specifications](https://ark.intel.com/content/www/us/en/ark/products/231803/intel-processor-n100-6m-cache-up-to-3-40-ghz.html)
- [NVIDIA GeForce RTX 50-Series Power Efficiency Guide](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/)
- [Apple Developer: Metal Performance Shaders](https://developer.apple.com/metal/pytorch/)
- [Raspberry Pi 5+ Performance Benchmarks (2026)](https://www.raspberrypi.com/news/pi-5-performance/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
