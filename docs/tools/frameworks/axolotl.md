# Axolotl

## What it is
Axolotl is a powerful, configuration-driven open-source framework designed to simplify and streamline the fine-tuning of Large Language Models (LLMs). As of late 2026, Axolotl has reached **v0.5.x+**, serving as a standard tool for machine learning practitioners and researchers. It allows developers to define entire training runs—including model loading, dataset tokenization, and hyperparameters—inside a single, reproducible YAML configuration file.

## What problem it solves
Managing the complex software environments, custom tokenization steps, hardware distribution configurations, and dataset blends required to train modern LLMs is highly error-prone. Axolotl addresses this by:
- **Declarative YAML Configurations**: Abstracting away PyTorch and Hugging Face boilerplate code into reproducible, version-controlled YAML settings.
- **Out-of-the-Box Scaling**: Providing first-class support for Multi-GPU and multi-node training using DeepSpeed and Fully Sharded Data Parallel (FSDP).
- **Advanced Training Algorithms**: Built-in implementations for progressive alignment and training techniques, such as DPO, IPO, ORPO, GRPO, and sample-packing.

## Where it fits in the stack
Axolotl sits in the **Frameworks / Fine-Tuning** layer. It sits downstream from data-generation frameworks like [distilabel](distilabel.md) and provides the training engine that produces customized, domain-adapted model weights to be served on highly optimized local backends like [vLLM](../../tools/infrastructure/vllm.md) or Ollama.

## Typical use cases
- **Multi-GPU/Node Supervised Fine-Tuning (SFT)**: Distributing instruction fine-tuning across clusters of GPUs using DeepSpeed or FSDP.
- **Domain Adaptation**: Tuning base models, like the Llama 4 family, Gemma 3, or Qwen 3.6, on proprietary corpus files.
- **Alignment Tuning**: Aligning pre-trained models using Direct Preference Optimization (DPO) or Group Relative Policy Optimization (GRPO).
- **Dataset Blending & Tokenization**: Pre-tokenizing and mixing multiple diverse instruction and conversational datasets.

## Strengths
- **Experimental Reproducibility**: High repeatability; changing model behaviors is as simple as tweaking parameters in a versioned YAML config.
- **Optimized Performance**: Supports cutting-edge architectural optimizations, including FlashAttention-3, multi-pack sample packing, and FP8 precision formats.
- **Active Support**: Rapidly updated with native support for newly released open architectures (e.g., Llama 4, Gemma 3, Qwen 3.6).
- **Enterprise Ready**: Seamlessly integrates with **NVIDIA Rubin** architecture clusters, NIM microservices, and Accelerate launchers.

## Limitations
- **Configuration Complexity**: The YAML file can become large, with hundreds of interrelated parameters that require deep machine learning expertise to coordinate.
- **Debugging Hurdles**: Tokenizer errors, model mismatches, or YAML parsing anomalies can sometimes emit obscure error logs.

## When to use it
- When you require a strictly reproducible, config-driven pipeline for training models on single or multi-GPU systems.
- When fine-tuning larger open architectures that require distributed training solutions like FSDP or DeepSpeed.
- For training runs that mix multiple distinct datasets with custom sampling weights.

## When not to use it
- If you prefer a visual, interactive web interface (use [LLaMA Factory](llama-factory.md) instead).
- If you only have a single small GPU and want the absolute fastest, memory-optimized kernels (use [Unsloth](../../tools/infrastructure/unsloth.md) instead).

## Getting started

### Installation
Axolotl is best installed in an isolated CUDA-enabled virtual environment or Docker container:

```bash
git clone https://github.com/axolotl-ai-cloud/axolotl
cd axolotl
pip install -e .
```

### Hello-world Fine-tuning Configuration
Create a file named `config.yml`:

```yaml
base_model: meta-llama/Llama-3.3-70B-Instruct
datasets:
  - path: vicgalle/alpaca-gpt4
    type: alpaca
val_set_size: 0.05
adapter: lora
lora_r: 32
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
sequence_len: 4096
sample_packing: true
pad_to_sequence_len: true
```

## CLI examples

```bash
# Start a training run using the accelerate launcher
accelerate launch -m axolotl.cli.train config.yml

# Preprocess and tokenize datasets without starting training
python3 -m axolotl.cli.preprocess config.yml

# Merge LoRA adapters back into the base model weights
python3 -m axolotl.cli.merge_lora config.yml --lora_model_dir="./completed-lora"
```

## API examples

### Python (Config Parser and Strict Pydantic v2 Configuration Validator)
To prevent expensive multi-GPU distributed cluster runs from crashing mid-execution due to typo errors or incompatible parameters, you can write a python parser to pre-validate your Axolotl YAML configurations using **Pydantic v2**:

```python
import yaml
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator

# 1. Define the validation schema for Axolotl YAML files
class AxolotlDataset(BaseModel):
    path: str
    type: str
    train_on_split: Optional[str] = Field(default=None, alias="trainOnSplit")

class AxolotlConfig(BaseModel):
    base_model: str = Field(..., serialization_alias="baseModel", validation_alias="baseModel")
    datasets: List[AxolotlDataset] = Field(default_factory=list)
    val_set_size: float = Field(..., ge=0.0, le=1.0, serialization_alias="valSetSize", validation_alias="valSetSize")
    adapter: Literal["lora", "qlora", "full"] = Field(default="lora")
    lora_r: Optional[int] = Field(default=None, ge=8, le=256, serialization_alias="loraR", validation_alias="loraR")
    lora_alpha: Optional[int] = Field(default=None, ge=8, serialization_alias="loraAlpha", validation_alias="loraAlpha")
    sequence_len: int = Field(..., ge=512, serialization_alias="sequenceLen", validation_alias="sequenceLen")
    sample_packing: bool = Field(default=True, serialization_alias="samplePacking", validation_alias="samplePacking")

    @field_validator("base_model")
    @classmethod
    def validate_base_model(cls, v: str) -> str:
        if not v or "/" not in v:
            raise ValueError("base_model must be a valid Hugging Face repository reference (e.g. 'org/repo')")
        return v

    @model_validator(mode="after")
    def check_lora_params(self) -> 'AxolotlConfig':
        if self.adapter in ["lora", "qlora"]:
            if self.lora_r is None or self.lora_alpha is None:
                raise ValueError("lora_r and lora_alpha must be defined when using lora/qlora adapters.")
        return self

# 2. Simulated Axolotl YAML content
yaml_content = """
baseModel: "meta-llama/Llama-4-Maverick"
valSetSize: 0.1
adapter: "lora"
loraR: 64
loraAlpha: 32
sequenceLen: 8192
samplePacking: true
datasets:
  - path: "argilla/ultrafeedback-binarized-preferences"
    type: "sharegpt"
"""

# 3. Load, parse, and validate
try:
    parsed_dict = yaml.safe_load(yaml_content)
    config = AxolotlConfig(**parsed_dict)
    print("Axolotl YAML configuration validated successfully via Pydantic v2!")
    print(f"Base Model: {config.base_model}")
    print(f"Adapter Type: {config.adapter} (r={config.lora_r}, alpha={config.lora_alpha})")
    print(f"Sequence Length: {config.sequence_len}")
    for d in config.datasets:
        print(f" - Configured Dataset Path: {d.path} [{d.type}]")
except Exception as e:
    print(f"Axolotl config validation failed: {e}")
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — The fundamental training pattern.
- [Unsloth](../../tools/infrastructure/unsloth.md) — Single-GPU performance-optimized fine-tuning alternative.
- [LLaMA Factory](llama-factory.md) — High-quality UI-driven SFT tool.
- [Distilabel](distilabel.md) — Scalable data generation pipeline upstream of Axolotl.
- [vLLM](../../tools/infrastructure/vllm.md) — High-performance inference engine for fine-tuned weights.
- [DeepSpeed](https://github.com/microsoft/DeepSpeed) — Distributed training acceleration engine.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Used to run fine-tuned tool-calling agents.

## Sources / references
- [Axolotl GitHub Repository](https://github.com/axolotl-ai-cloud/axolotl)
- [Axolotl Documentation](https://axolotl-ai-cloud.github.io/axolotl/)
- [Open-Source LLM Fine-Tuning Guide](https://github.com/mlabonne/llm-course)

## Contribution Metadata
- Last reviewed: 2026-12-10
- Confidence: high
