# PEFT (Parameter-Efficient Fine-Tuning)

## What it is
PEFT (Parameter-Efficient Fine-Tuning) is an open-source library from Hugging Face that enables efficient adaptation of pre-trained language, vision, and multi-modal foundation models to downstream tasks without fine-tuning all model parameters. By freezing the vast majority of base model weights and training only a small set of additional parameters (typically 0.01% to 1% of total parameters), PEFT dramatically reduces memory requirements and storage overhead. As of early 2027, PEFT techniques—including LoRA, QLoRA, DoRA, Prefix Tuning, and Prompt Tuning—are essential industry tools for fine-tuning frontier open-weight models (Llama 4, Gemma 3, Qwen 3.8) alongside high-efficiency inference frameworks like [Unsloth](unsloth.md) and [vLLM](vllm.md).

## What problem it solves
Full parameter fine-tuning of modern foundation models (7B to 400B+ parameters) incurs prohibitive computational and storage costs:
- **VRAM Memory Exhaustion**: Full fine-tuning requires holding model weights, gradients, and optimizer states in VRAM simultaneously, requiring multi-node enterprise GPU clusters.
- **Enormous Storage Overhead**: Saving full copies of modified models for every domain task generates hundreds of gigabytes per checkpoint.
- **Catastrophic Forgetting**: Updating all weights on a small dataset can degrade general reasoning capabilities across untargeted domains.

PEFT solves these challenges by updating only small low-rank adapter matrices or prefix tensors, reducing VRAM usage by up to 80% and allowing adapter files (often under 100MB) to be swapped dynamically at inference time.

## Where it fits in the stack
**Category**: [Infrastructure](index.md) / Model Optimization & Fine-Tuning. PEFT operates between high-level training frameworks (Hugging Face TRL, PyTorch Lightning, Unsloth) and underlying hardware acceleration backends (CUDA, Triton, Apple Metal), managing adapter initialization, weight merging, and serialization.

## Typical use cases
- **Domain-Specific LLM Fine-Tuning**: Adapting open-weight models (e.g., Llama 4, Qwen 3.8) to specialized legal, medical, or coding instruction datasets on modest GPU setups.
- **Multi-Tenant Adapter Serving**: Loading dozens of specialized LoRA adapters dynamically onto a single shared base model instance in production using vLLM or TGI.
- **Consumer Hardware Model Training**: Training 70B+ parameter models on consumer-grade GPUs (e.g., RTX 4090 / 5090) using 4-bit QLoRA quantization.
- **Continuous Knowledge Updating**: Fine-tuning lightweight adapters on periodically updated enterprise documents without altering base foundation model parameters.

## Key Techniques Matrix

| Method | Full Name | Modifies | VRAM Savings | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **LoRA** | Low-Rank Adaptation | Low-rank decomposition matrices | ~60-70% | General LLM task adaptation & instruction tuning |
| **QLoRA** | Quantized LoRA | Low-rank matrices over 4-bit base weights | ~80-85% | Consumer GPU fine-tuning (e.g., RTX 4090 / 5090) |
| **DoRA** | Weight-Decomposed LoRA | Direction and magnitude components | ~65-75% | High-accuracy fine-tuning matching full-FT stability |
| **Prefix Tuning** | Prefix Tuning | Virtual prompt key-value prefix tensors | ~75% | Task-specific conditional text generation |

## Strengths
- **Massive Resource Efficiency**: Enables fine-tuning 70B+ parameter models on single consumer GPUs when combined with QLoRA 4-bit quantization.
- **Dynamic Adapter Swapping**: Multiple specialized LoRA adapters can be loaded onto a single shared base model instance in memory during serving.
- **Modular Storage**: Adapter checkpoints are tiny (10MB–200MB), enabling rapid deployment and distribution via Git or Hugging Face Hub.
- **Deep Hugging Face Ecosystem Integration**: Native compatibility with `transformers`, `accelerate`, `bitsandbytes`, and `TRL`.

## Limitations
- **Adapter Merging Overhead**: Merging LoRA weights back into the base model requires an initial compilation step prior to export.
- **Slight Latency Penalty if Unmerged**: Serving unmerged adapters alongside base models can introduce minor inference latency overhead during multi-tenant token generation.
- **Hyperparameter Sensitivity**: Choosing rank ($r$), alpha ($\alpha$), and targeted linear layers requires careful calibration for optimal convergence.

## When to use it
- When adapting large pre-trained LLMs to domain-specific datasets with limited GPU hardware resources.
- When serving multiple specialized task models from a single base model instance.
- When implementing parameter-efficient fine-tuning pipelines using frameworks like [Unsloth](unsloth.md).

## When not to use it
- When training a new model from scratch or performing massive pre-training on trillions of tokens.
- When fine-tuning extremely small models (<100M parameters) where full parameter fine-tuning fits comfortably in standard VRAM.

## Getting started

### 1. Installation
```bash
pip install peft transformers torch bitsandbytes
```

### 2. Configure LoRA for an LLM
```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

# Define LoRA Configuration
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Wrap model with PEFT adapter
model = get_peft_model(base_model, peft_config)
model.print_trainable_parameters()
```

## CLI examples

### Inspect PEFT Adapter Checkpoint
```bash
# Verify adapter metadata and configuration
cat ./lora-adapter-checkpoint/adapter_config.json
```

### Merge PEFT Adapter with Base Model via Script
```bash
# Run CLI utility to merge LoRA adapter into base weights for deployment
python3 -m peft.merge_adapter --base_model_name_or_path "meta-llama/Llama-3.1-8B" --adapter_path "./lora-adapter" --output_path "./merged-model"
```

## API examples

The following Python script utilizes **Pydantic v2** to validate a PEFT LoRA configuration schema before initializing training runs.

```python
from pydantic import BaseModel, Field, Literal
from typing import List, Optional
import json

class LoraAdapterConfigSchema(BaseModel):
    r: int = Field(16, ge=1, le=256, description="LoRA rank dimension.")
    lora_alpha: int = Field(32, ge=1, description="LoRA scaling factor.")
    target_modules: List[str] = Field(..., description="Target linear layer names for decomposition.")
    lora_dropout: float = Field(0.05, ge=0.0, le=0.5, description="Dropout probability for LoRA layers.")
    bias: Literal["none", "all", "lora_only"] = Field("none", description="Bias parameter training policy.")
    task_type: str = Field("CAUSAL_LM", description="Task type classification.")
    use_dora: bool = Field(False, description="Enable Weight-Decomposed LoRA (DoRA).")

def validate_peft_configuration(raw_config: dict) -> str:
    """Validates PEFT LoRA hyperparameters using Pydantic v2."""
    try:
        config = LoraAdapterConfigSchema.model_validate(raw_config)

        # Compute recommended scaling ratio
        scaling_ratio = config.lora_alpha / config.r

        return json.dumps({
            "status": "valid",
            "rank": config.r,
            "scaling_ratio": scaling_ratio,
            "target_modules_count": len(config.target_modules),
            "dora_enabled": config.use_dora
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "invalid",
            "error": str(e)
        }, indent=2)

if __name__ == "__main__":
    sample_lora_config = {
        "r": 32,
        "lora_alpha": 64,
        "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
        "lora_dropout": 0.1,
        "bias": "none",
        "task_type": "CAUSAL_LM",
        "use_dora": True
    }
    print(validate_peft_configuration(sample_lora_config))
```

## Related tools / concepts
- [Unsloth](unsloth.md) — High-performance fine-tuning library leveraging optimized PEFT kernels.
- [vLLM](vllm.md) — High-throughput LLM serving engine with multi-LoRA adapter support.
- [TGI](tgi.md) — Text Generation Inference engine supporting dynamic LoRA loading.

## Sources / references
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft/index)
- [Hugging Face PEFT GitHub Repository](https://github.com/huggingface/peft)
- [LoRA Research Paper (Hu et al., 2021)](https://arxiv.org/abs/2106.09685)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
