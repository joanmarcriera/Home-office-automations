# LLaMA Factory

## What it is
LLaMA Factory is a unified, efficient fine-tuning framework that supports over 100 Large Language Models (LLMs). In June 2026, it is the industry standard for democratizing model adaptation, supporting everything from Llama 4 Maverick to Qwen 3.6.

## What problem it solves
Fine-tuning different LLM architectures often requires custom code and deep expertise in various libraries (e.g., PEFT, DeepSpeed, TRT-LLM). LLaMA Factory simplifies this by:
- **Standardizing the Workflow**: Providing a single entry point for fine-tuning diverse models.
- **Reducing Technical Barrier**: Offering the "LLaMA Board" no-code web UI for rapid experimentation.
- **Integrating Best Practices**: Built-in support for advanced techniques like GaLore, BAdam, DoRA, and Mixture-of-Experts (MoE) tuning.
- **Optimizing for Frontier Benchmarks**: Enables efficient distillation of reasoning from Claude 4.8 Opus or GPT-5.5 into smaller, task-specific models.

## Where it fits in the stack
**Frameworks / Fine-tuning**. It is an orchestration framework that coordinates lower-level libraries (PyTorch, Transformers, [NVIDIA NIM](../providers/nvidia.md)) to perform complex training tasks.

## Typical use cases
- **Multi-Model Experimentation**: Quickly comparing fine-tuning results across different model families.
- **RLHF & DPO Training**: Implementing Reinforcement Learning from Human Feedback (RLHF) or Direct Preference Optimization (DPO) workflows.
- **Automated Dataset Conversion**: Using built-in scripts to convert raw data into ShareGPT or Alpaca formats.
- **Agentic Fine-tuning**: Training models to better follow [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) schemas using synthetic data from [Glaive](../ai_knowledge/glaive.md).

## Strengths
- **Massive Model Support**: Covers almost all popular open-source LLMs, including Llama 4 Maverick.
- **Web UI (LLaMA Board)**: Exceptional ease of use for beginners and rapid experimentation.
- **Efficiency**: Supports 4-bit/8-bit QLoRA and various memory-saving optimizers like [Unsloth](../infrastructure/unsloth.md) backends.
- **NVIDIA Integration**: Native support for NVIDIA Rubin architecture and NIM GA microservices for training and evaluation.

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
- If you only ever tune one specific architecture and prefer the absolute maximum speed of a raw [Unsloth](../infrastructure/unsloth.md) implementation.
- If your environment is extremely resource-constrained and you cannot afford the management layer overhead.

## Getting started

### Installation
```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[metrics,bitsandbytes,qwen]"
```

### Hello-world (Web UI)
Launch the LLaMA Board to start tuning via your browser:
```bash
llamafactory-cli webui
```

### Hello-world (CLI)
Create a `train.yaml` config and start training:
```bash
llamafactory-cli train train.yaml
```

## CLI examples

```bash
# Start a supervised fine-tuning (SFT) task for Llama 4
llamafactory-cli train examples/train_lora/llama4_lora_sft.yaml

# Export a LoRA-tuned model to a merged checkpoint
llamafactory-cli export examples/merge_lora/llama4_lora_sft.yaml

# Evaluate a model on common benchmarks (GSM8K, HumanEval)
llamafactory-cli eval examples/train_lora/llama4_lora_eval.yaml
```

## API examples

### Python API: Inference
You can use the `ChatModel` for high-level interaction with fine-tuned models.

```python
from llamafactory.chat import ChatModel
from llamafactory.extras.misc import torch_gc

args = {
    "model_name_or_path": "path_to_your_model",
    "template": "llama4",
    "finetuning_type": "lora",
}
model = ChatModel(args)

# query = "Convert this MCP tool definition to a Pydantic schema."
# response = model.chat(query)
# print(response[0].response_text)
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — Standard patterns.
- [Unsloth](../infrastructure/unsloth.md) — Specialized high-speed backend.
- [Axolotl](axolotl.md) — Configuration-driven alternative.
- [Distilabel](distilabel.md) — Synthetic data generation for fine-tuning.
- [vLLM](../infrastructure/vllm.md) — High-throughput model serving.
- [Qwen](../ai_knowledge/qwen.md) — Frontier open-weight model family.
- [Glaive](../ai_knowledge/glaive.md) — Specialized synthetic data for tool-use tuning.
- [NVIDIA](../providers/nvidia.md) — Hardware and software acceleration standard.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Integration target for fine-tuned agents.

## Sources / references
- [LLaMA Factory GitHub](https://github.com/hiyouga/LLaMA-Factory)
- [LLaMA Factory Documentation](https://llama-factory.readthedocs.io/)
- [Hugging Face Blog: Fine-tuning with LLaMA Factory](https://huggingface.co/blog/llama-factory)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
