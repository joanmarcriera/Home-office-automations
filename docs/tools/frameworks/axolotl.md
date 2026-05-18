# Axolotl

## What it is
Axolotl is a powerful, configuration-driven framework designed to streamline the fine-tuning of Large Language Models. It allows researchers and developers to define complex training runs entirely within YAML configuration files, abstracting away the boilerplate code typically required for model loading, dataset processing, and hyperparameter management.

## What problem it solves
Managing the various dependencies, dataset formats, and training parameters for LLM fine-tuning can be error-prone and difficult to reproduce. Axolotl addresses this by:
- **Declarative Configuration**: Moving all logic into a single YAML file, ensuring reproducibility and version control for training experiments.
- **Support for Advanced Techniques**: Native integration with DeepSpeed, FSDP (Fully Sharded Data Parallel), and various quantization methods.
- **Dataset Flexibility**: Built-in support for diverse dataset formats (Alpaca, ShareGPT, JEPA, etc.) and automatic tokenization.

## Where it fits in the stack
Axolotl sits in the **Frameworks/Fine-tuning** layer. It provides a higher-level abstraction over the Hugging Face `transformers` and `peft` libraries, specifically catering to users who want deep control via configuration.

## Typical use cases
- **Multi-GPU Training**: Scaling fine-tuning across multiple GPUs using DeepSpeed or FSDP.
- **Instruction Tuning**: Adapting base models to follow complex, multi-turn instructions.
- **Experiment Tracking**: Maintaining a library of YAML configurations to compare different LoRA alphas, ranks, and learning rates.
- **Dataset Mixing**: Combining multiple datasets with different weights and formats into a single training run.

## Strengths
- **Reproducibility**: The YAML-first approach makes it easy to share and rerun exact training setups.
- **Deep Integration**: Excellent support for the latest Hugging Face features and architectural optimizations.
- **Active Community**: Frequently updated with support for new models and fine-tuning techniques (e.g., DPO, multipack).
- **Flexibility**: Supports a wide range of model architectures and training objectives.

## Limitations
- **Learning Curve**: The YAML configuration can become very complex, with hundreds of possible parameters to tune.
- **Debugging**: Errors in the YAML or dataset mapping can sometimes be cryptic compared to direct Python debugging.
- **Performance**: While efficient, it may not match the specialized, hand-tuned kernel speeds of [Unsloth](../infrastructure/unsloth.md) for supported architectures.

## When to use it
- When you need a highly reproducible and documented training process.
- When you are scaling to multi-node or multi-GPU environments using DeepSpeed.
- When you want to mix multiple datasets or use complex tokenization strategies without writing code.

## When not to use it
- If you prefer an interactive, UI-based approach (use [LLaMA Factory](llama-factory.md) instead).
- If you only have a single GPU and want the absolute fastest possible training speed (use [Unsloth](../infrastructure/unsloth.md)).
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

Run the training:
```bash
accelerate launch -m axolotl.cli.train config.yml
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — The core pattern implemented by Axolotl.
- [Unsloth](../infrastructure/unsloth.md) — A speed-optimized alternative for single-GPU setups.
- [llama-factory](llama-factory.md) — A UI-driven alternative for fine-tuning.
- [distilabel](distilabel.md) — For generating the high-quality synthetic data often used with Axolotl.
- [vLLM](../infrastructure/vllm.md) — For serving models fine-tuned with Axolotl.
- [DeepSpeed](https://github.com/microsoft/DeepSpeed) — Frequently used with Axolotl for large-scale training.

## Sources / references
- [Axolotl GitHub Repository](https://github.com/axolotl-ai-cloud/axolotl)
- [Axolotl Documentation](https://axolotl-ai-cloud.github.io/axolotl/)
- [Open-source LLM Fine-tuning Guide](https://github.com/mlabonne/llm-course)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
