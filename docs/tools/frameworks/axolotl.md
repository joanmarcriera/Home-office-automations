# Axolotl

## What it is
Axolotl is a powerful, configuration-driven framework designed to streamline the fine-tuning of Large Language Models (LLMs). As of June 2026, it remains a preferred choice for researchers and developers who need to define complex training runs entirely within YAML configuration files, abstracting away the boilerplate code typically required for model loading, dataset processing, and hyperparameter management.

## What problem it solves
Managing the various dependencies, dataset formats, and training parameters for LLM fine-tuning can be error-prone and difficult to reproduce. Axolotl addresses this by:
- **Declarative Configuration**: Moving all logic into a single YAML file, ensuring reproducibility and version control for training experiments.
- **Support for Advanced Techniques**: Native integration with DeepSpeed, FSDP (Fully Sharded Data Parallel), and various quantization methods for models like Claude 4.8 Opus and the Llama 4 family.
- **Dataset Flexibility**: Built-in support for diverse dataset formats (Alpaca, ShareGPT, JEPA, etc.) and automatic tokenization.

## Where it fits in the stack
Axolotl sits in the **Frameworks/Fine-tuning** layer. It provides a higher-level abstraction over the Hugging Face `transformers` and `peft` libraries, specifically catering to users who want deep control via configuration while targeting high-performance inference backends like [vLLM](../../tools/infrastructure/vllm.md).

## Typical use cases
- **Multi-GPU Training**: Scaling fine-tuning across multiple GPUs using DeepSpeed or FSDP.
- **Instruction Tuning**: Adapting base models like Llama 4 Maverick to follow complex, multi-turn instructions.
- **Experiment Tracking**: Maintaining a library of YAML configurations to compare different LoRA alphas, ranks, and learning rates.
- **Dataset Mixing**: Combining multiple datasets with different weights and formats into a single training run using [distilabel](distilabel.md) generated data.

## Strengths
- **Reproducibility**: The YAML-first approach makes it easy to share and rerun exact training setups.
- **Deep Integration**: Excellent support for the latest Hugging Face features and architectural optimizations.
- **Active Community**: Frequently updated with support for new models and fine-tuning techniques (e.g., DPO, multipack).
- **Flexibility**: Supports a wide range of model architectures and training objectives.
- **NVIDIA Rubin Support**: Optimized for the latest NVIDIA GPU architectures and NIM microservices.

## Limitations
- **Learning Curve**: The YAML configuration can become very complex, with hundreds of possible parameters to tune.
- **Debugging**: Errors in the YAML or dataset mapping can sometimes be cryptic compared to direct Python debugging.
- **Performance**: While efficient, it may not match the specialized, hand-tuned kernel speeds of [Unsloth](../../tools/infrastructure/unsloth.md) for supported architectures.

## When to use it
- When you need a highly reproducible and documented training process.
- When you are scaling to multi-node or multi-GPU environments using DeepSpeed.
- When you want to mix multiple datasets or use complex tokenization strategies without writing code.

## When not to use it
- If you prefer an interactive, UI-based approach (use [LLaMA Factory](llama-factory.md) instead).
- If you only have a single GPU and want the absolute fastest possible training speed (use [Unsloth](../../tools/infrastructure/unsloth.md)).
- If you are building a simple prototype and don't want to manage a complex configuration file.

## Getting started

### Installation
Axolotl is best installed in a virtual environment or Docker container:

```bash
git clone https://github.com/axolotl-ai-cloud/axolotl
cd axolotl
pip install -e .
```

### Hello-world Fine-tuning
Create a `config.yml`:

```yaml
base_model: meta-llama/Llama-2-7b-hf
datasets:
  - path: vicgalle/alpaca-gpt4
    type: alpaca
dataset_prepared_path:
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
Axolotl provides a streamlined CLI for training and dataset preparation.

```bash
# Start a training run using the accelerate launcher
accelerate launch -m axolotl.cli.train config.yml

# Prepare the dataset without starting the training
python3 -m axolotl.cli.preprocess config.yml

# Merge LoRA adapters back into the base model
python3 -m axolotl.cli.merge_lora config.yml --lora_model_dir="./completed-model"
```

## API examples
While Axolotl is configuration-driven, it can be interacted with programmatically for custom workflows.

```python
import torch
from axolotl.utils.config import load_config
from axolotl.utils.models import load_model, load_tokenizer

# Load configuration from YAML
config = load_config("config.yml")

# Programmatically load the model and tokenizer as defined in the config
model, tokenizer = load_model(config)

print(f"Model {config['base_model']} loaded with device: {model.device}")
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — The core pattern implemented by Axolotl.
- [Unsloth](../../tools/infrastructure/unsloth.md) — A speed-optimized alternative for single-GPU setups.
- [LLaMA Factory](llama-factory.md) — A UI-driven alternative for fine-tuning.
- [Distilabel](distilabel.md) — For generating high-quality synthetic data for fine-tuning.
- [vLLM](../../tools/infrastructure/vllm.md) — Optimized inference engine for models fine-tuned with Axolotl.
- [DeepSpeed](https://github.com/microsoft/DeepSpeed) — Framework for large-scale distributed training.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — For integrating fine-tuned models into agentic workflows.
- [NVIDIA NIM](../../tools/providers/nvidia.md) — For enterprise-grade inference.

## Sources / references
- [Axolotl GitHub Repository](https://github.com/axolotl-ai-cloud/axolotl)
- [Axolotl Documentation](https://axolotl-ai-cloud.github.io/axolotl/)
- [Open-source LLM Fine-tuning Guide](https://github.com/mlabonne/llm-course)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
