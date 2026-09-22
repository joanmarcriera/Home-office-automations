# DeepSpeed

## What it is
DeepSpeed is an open-source deep learning optimization library developed by Microsoft that enables training and inferencing extreme-scale deep learning models—including massive Large Language Models (LLMs)—with unprecedented computational efficiency and memory throughput. DeepSpeed implements state-of-the-art distributed training algorithms, such as **ZeRO (Zero Redundancy Optimizer)**, ZeRO-Offload, ZeRO-Infinity, sparse attention, custom CUDA kernels, and 3D parallelism (Tensor, Pipeline, and Data parallelism).

In early 2027, DeepSpeed serves as a primary scaling engine integrated under high-level fine-tuning platforms like [Axolotl](axolotl.md) and Unsloth, allowing developers to fine-tune 70B+ parameter models on consumer or multi-GPU cluster hardware.

## What problem it solves
Training modern LLMs with tens or hundreds of billions of parameters exhausts standard GPU VRAM memory limits. Traditional Data Parallelism (DP) duplicates model states (parameters, gradients, and optimizer states like Adam fp32 momentum/variance) across every GPU, creating extreme memory redundancy.

DeepSpeed addresses this bottleneck by partitioning model states across available GPUs and host CPU/NVMe memory:
- **ZeRO Stage 1**: Partitions optimizer states across GPUs, reducing memory footprint by 4x without communication overhead.
- **ZeRO Stage 2**: Partitions optimizer states and gradients, reducing memory footprint by 8x.
- **ZeRO Stage 3**: Partitions optimizer states, gradients, and model parameters across all GPUs, enabling models that exceed individual GPU memory capacities.
- **ZeRO-Offload / ZeRO-Infinity**: Offloads partitioned model states to CPU RAM or NVMe storage, enabling fine-tuning of multi-billion parameter models on single-GPU workstations.

## Where it fits in the stack
**AI Frameworks & Infrastructure Optimization Layer**. DeepSpeed interfaces between high-level ML frameworks (PyTorch, Hugging Face Transformers, [Axolotl](axolotl.md)) and low-level GPU acceleration hardware (CUDA, ROCm, NCCL).

## Typical use cases
- **Multi-GPU Fine-Tuning of Large Models**: Fine-tuning Llama-3, Qwen, or Mistral architectures in [Axolotl](axolotl.md) across multi-node GPU clusters.
- **Extreme Parameter Memory Offloading**: Fine-tuning 30B–70B models on workstation environments with limited GPU VRAM by offloading memory states to host RAM via ZeRO-Offload.
- **Pipeline & Tensor Parallel Model Pretraining**: Scaling pretraining runs across thousands of GPUs using 3D parallelism.
- **High-Throughput Inference (DeepSpeed-Inference)**: Accelerating low-latency LLM inference via custom transformer kernel fusion and quantization.

## Strengths
- **Massive Memory Efficiency**: ZeRO Stage 3 eliminates memory redundancy, unlocking model scale proportional to total cluster VRAM.
- **Native Integration with PyTorch & Hugging Face**: Drops directly into PyTorch scripts via `deepspeed.initialize()` or Hugging Face `Trainer`.
- **Flexible Offloading**: CPU and NVMe offloading options enable large model runs on budget or consumer hardware.
- **High-Performance CUDA Kernels**: Built-in fused Adam, Transformer layer kernels, and FlashAttention extensions.

## Limitations
- **Inter-GPU Interconnect Sensitivity**: ZeRO Stage 3 requires high bandwidth (NVLink or InfiniBand); slow PCIe buses can cause communication bottlenecks.
- **Configuration Complexity**: DeepSpeed JSON configuration files require tuning parameters (allgather bucket sizes, overlap comms, gradient accumulation).

## When to use it
- When training or fine-tuning models whose size exceeds the VRAM capacity of a single GPU.
- When running fine-tuning jobs in [Axolotl](axolotl.md) across multi-GPU or multi-node clusters.
- When offloading optimizer states to CPU RAM is necessary to avoid Out-Of-Memory (OOM) crashes.

## When not to use it
- For lightweight model training (e.g., small scikit-learn or single-GPU BERT models) where standard PyTorch execution is sufficient.
- When single-GPU LoRA/QLoRA fine-tuning fits comfortably within available VRAM without model state partitioning.

## Getting started

### Installation
Install DeepSpeed with CUDA extensions:

```bash
pip install deepspeed
```

Verify installation and environment hardware capabilities:

```bash
ds_report
```

## CLI examples

### Launching Distributed Training with DeepSpeed
```bash
# Launch a multi-GPU training script using DeepSpeed on 4 local GPUs
deepspeed --num_gpus=4 train.py --deepspeed ds_config.json

# Launch across multi-node cluster specified in a hostfile
deepspeed --hostfile=hostfile --num_gpus=8 train.py --deepspeed ds_config.json
```

## API examples

### Python (Initializing DeepSpeed Engine Programmatically)
```python
import torch
import deepspeed

def init_deepspeed_engine(model, optimizer_params, ds_config):
    model_engine, optimizer, _, _ = deepspeed.initialize(
        model=model,
        model_parameters=optimizer_params,
        config=ds_config
    )
    return model_engine, optimizer
```

## Configuration & Code examples

### DeepSpeed ZeRO Stage 3 Configuration (`ds_config.json`)
```json
{
  "fp16": {
    "enabled": true,
    "loss_scale": 0,
    "loss_scale_window": 1000,
    "initial_scale_power": 16,
    "hysteresis": 2,
    "min_loss_scale": 1
  },
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "offload_param": {
      "device": "cpu",
      "pin_memory": true
    },
    "overlap_comm": true,
    "contiguous_gradients": true,
    "sub_group_size": 1e9,
    "reduce_bucket_size": "auto",
    "stage3_prefetch_bucket_size": "auto",
    "stage3_param_persistence_threshold": "auto"
  },
  "gradient_accumulation_steps": "auto",
  "gradient_clipping": "auto",
  "steps_per_print": 200,
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto"
}
```

### PyTorch Training Script Integration
```python
import torch
import torch.nn as nn
import deepspeed
import json

class SimpleLLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(4096, 4096)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(4096, 4096)

    def forward(self, x):
        return self.linear2(self.relu(self.linear1(x)))

def train():
    model = SimpleLLM()
    parameters = filter(lambda p: p.requires_grad, model.parameters())

    with open("ds_config.json", "r") as f:
        ds_config = json.load(f)

    # Initialize DeepSpeed engine
    model_engine, optimizer, _, _ = deepspeed.initialize(
        args=None,
        model=model,
        model_parameters=parameters,
        config=ds_config
    )

    # Simulated training step
    for step in range(10):
        inputs = torch.randn(8, 4096, device=model_engine.device, dtype=torch.float16)
        targets = torch.randn(8, 4096, device=model_engine.device, dtype=torch.float16)

        outputs = model_engine(inputs)
        loss = torch.nn.functional.mse_loss(outputs, targets)

        model_engine.backward(loss)
        model_engine.step()

        if model_engine.is_gradient_accumulation_boundary():
            print(f"Step {step} - Loss: {loss.item():.4f}")

if __name__ == "__main__":
    train()
```

## Related tools / concepts
- [Axolotl](axolotl.md) — Open-source LLM fine-tuning framework with native DeepSpeed ZeRO support.
- [Pydantic AI](pydantic-ai.md) — Agentic framework using structured parameter models for training pipeline orchestration.
- [Docker](../infrastructure/docker.md) — Container runtime for deploying standardized DeepSpeed training images across GPU clusters.

## Sources / references
- [DeepSpeed Official Portal](https://www.deepspeed.ai/)
- [DeepSpeed GitHub Repository](https://github.com/microsoft/DeepSpeed)
- [DeepSpeed Documentation](https://deepspeed.readthedocs.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
