# LLaMA Factory

## What it is
LLaMA Factory is a unified, efficient fine-tuning framework that supports over 100 Large Language Models (LLMs). It provides a comprehensive suite of tools, including a web-based UI (LLaMA Board), a command-line interface, and an API, to streamline the entire fine-tuning pipeline from data preparation to model evaluation and deployment.

## What problem it solves
Fine-tuning different LLM architectures often requires custom code and deep expertise in various libraries (e.g., PEFT, DeepSpeed, TRT-LLM). LLaMA Factory simplifies this by:
- **Standardizing the Workflow**: Providing a single entry point for fine-tuning diverse models like Llama, Mistral, Qwen, and Baichuan.
- **Reducing Technical Barrier**: Offering a "no-code" web UI for users who prefer graphical interfaces over CLI.
- **Integrating Best Practices**: Built-in support for advanced techniques like GaLore, BAdam, DoRA, and Mixture-of-Experts (MoE) tuning.

## Where it fits in the stack
LLaMA Factory sits in the **Frameworks/Fine-tuning** layer. It is an orchestration framework that coordinates lower-level libraries (PyTorch, Transformers) to perform complex training tasks.

## Typical use cases
- **Multi-Model Experimentation**: Quickly comparing fine-tuning results across different model families.
- **RLHF & DPO Training**: Implementing Reinforcement Learning from Human Feedback (RLHF) or Direct Preference Optimization (DPO) workflows.
- **Automated Dataset Conversion**: Using its built-in scripts to convert raw data into the required ShareGPT or Alpaca formats.
- **Rapid Prototyping**: Using LLaMA Board to tune hyperparameters visually before scaling to CLI-based production runs.

## Strengths
- **Massive Model Support**: Covers almost all popular open-source LLMs.
- **Web UI (LLaMA Board)**: Exceptional ease of use for beginners and rapid experimentation.
- **Efficiency**: Supports 4-bit/8-bit QLoRA and various memory-saving optimizers (Unsloth, GaLore).
- **Extensible**: Easily integrated into larger pipelines via its Python API or CLI.

## Limitations
- **Complexity Overhead**: For extremely simple one-off tunes, the framework might feel more "heavyweight" than a direct [Unsloth](../infrastructure/unsloth.md) script.
- **Dependency Management**: Requires a specific environment setup to ensure compatibility between CUDA, PyTorch, and the framework's own requirements.
- **UI Constraints**: While powerful, the Web UI might not expose every granular hyperparameter available in the underlying CLI/YAML config.

## When to use it
- When you need to fine-tune a model that isn't yet supported by more specialized tools.
- When you want to use DPO, PPO, or ORPO without writing custom training loops.
- When you want a graphical interface to monitor training metrics and chat with the tuned model immediately.

## When not to use it
- If you are doing extremely low-level kernel development.
- If you only ever tune one specific architecture (e.g., Llama 3) and prefer the absolute maximum speed of [Unsloth](../infrastructure/unsloth.md).
- If your environment is extremely resource-constrained and you cannot afford the overhead of the framework's management layers.

## Getting started

### Installation
```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[metrics,bitsandbytes,qwen]"
```

### Launching LLaMA Board (Web UI)
```bash
llamafactory-cli webui
```

### Hello-world Fine-tuning (CLI)
Create a `train.yaml` config:
```yaml
model_name_or_path: meta-llama/Meta-Llama-3-8B-Instruct
stage: sft
do_train: true
dataset: identity,alpaca_gpt4_en
template: llama3
finetuning_type: lora
lora_target: all
output_dir: llama3_lora_sft
per_device_train_batch_size: 2
gradient_accumulation_steps: 4
learning_rate: 1.0e-4
num_train_epochs: 3.0
lr_scheduler_type: cosine
logging_steps: 10
save_steps: 100
plot_loss: true
overwrite_output_dir: true
```
Then run:
```bash
llamafactory-cli train train.yaml
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — Standard patterns for model adaptation.
- [Unsloth](../infrastructure/unsloth.md) — Specialized backend for maximum fine-tuning speed.
- [axolotl](axolotl.md) — Configuration-driven alternative for advanced users.
- [distilabel](distilabel.md) — For generating the synthetic datasets used in LLaMA Factory.
- [vLLM](../infrastructure/vllm.md) — For serving models fine-tuned with LLaMA Factory.
- [Qwen](../ai_knowledge/qwen.md) — Frequently tuned model family within this framework.
- [Weights & Biases](https://wandb.ai/) — Integrated for experiment tracking.

## Sources / references
- [LLaMA Factory GitHub](https://github.com/hiyouga/LLaMA-Factory)
- [LLaMA Factory Documentation](https://llama-factory.readthedocs.io/)
- [Hugging Face Blog: Fine-tuning with LLaMA Factory](https://huggingface.co/blog/llama-factory)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
