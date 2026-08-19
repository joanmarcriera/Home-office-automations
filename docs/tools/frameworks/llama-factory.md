# LLaMA Factory

## What it is
LLaMA Factory is a unified, high-efficiency fine-tuning framework that supports over 100 open-source Large Language Model (LLM) architectures. It provides a standardized command-line and graphical web interface ("LLaMA Board") for fine-tuning models ranging from **Llama 4**, **Gemma 3**, and **Qwen 3.8** to specialized MoE (Mixture-of-Experts) architectures on modern NVIDIA Blackwell and Rubin GPUs.

## What problem it solves
Fine-tuning diverse LLM families typically requires writing fragmented, custom boilerplate code across multiple distributed training and quantization libraries (such as PEFT, DeepSpeed, FlashAttention-3, and bitsandbytes). LLaMA Factory eliminates this friction by unifying supervised fine-tuning (SFT), Direct Preference Optimization (DPO), Proximal Policy Optimization (PPO), and ORPO training under a single configuration engine.

## Where it fits in the stack
**Framework / Model Adaptation & Fine-tuning Layer**. LLaMA Factory sits between lower-level acceleration libraries (PyTorch, Triton, DeepSpeed, [Unsloth](../infrastructure/unsloth.md)) and higher-level model serving runtimes ([vLLM](../infrastructure/vllm.md), [TGI](../infrastructure/tgi.md), [NVIDIA NIM](../providers/nvidia.md)). It enables rapid distillation of reasoning traces from frontier APIs like **Claude 5.1** into domain-specific open weights.

## Typical use cases
- **Supervised Fine-Tuning (SFT)**: Adapting open models (**Llama 4 Maverick**, **Qwen 3.8**) on enterprise document schemas or coding tasks.
- **Preference Alignment (DPO / ORPO / KTO)**: Aligning agent outputs with preference datasets to reduce hallucination rates.
- **Agentic Tool-Use Adaptation**: Fine-tuning models to natively emit [FastMCP 3.1](../automation_orchestration/mcp.md) tool invocations using synthetic function-calling datasets.
- **LoRA Adapter Merging & Quantization**: Training parameter-efficient adapters and exporting merged 4-bit / 8-bit GGUF or AWQ checkpoints for deployment.

## Strengths
- **Comprehensive Model Support**: Native compatibility with over 100 model architectures, including Llama 4, Gemma 3, and Qwen 3.8.
- **LLaMA Board Web UI**: No-code web interface for visual hyperparameter configuration, live loss plotting, and interactive chat evaluations.
- **Advanced Parameter Efficiency**: Built-in integration for QLoRA, GaLore, BAdam, DoRA, and Unsloth memory acceleration backends.
- **Multi-GPU & Distributed Training**: DeepSpeed ZeRO-2/ZeRO-3 and FSDP integration out of the box.
- **Dataset Formatting Utilities**: Automated conversion for Alpaca, ShareGPT, and custom OpenAI-style JSONL conversation datasets.

## Limitations
- **Environment Management**: High sensitivity to PyTorch, CUDA, and FlashAttention dependency version alignment.
- **UI Abstraction**: Advanced distributed training configurations or custom loss function modifications require direct YAML/CLI editing rather than the Web UI.
- **Resource Footprint**: Training large 70B+ parameters requires multi-node hardware or aggressive QLoRA quantization.

## When to use it
- When fine-tuning or aligning open-source LLMs without writing custom PyTorch training loops from scratch.
- When evaluating multiple fine-tuning paradigms (e.g., comparing SFT vs. DPO vs. ORPO) on identical datasets.
- When you require a graphical dashboard (LLaMA Board) for non-programmer stakeholders to monitor training progress.

## When not to use it
- If you are building novel neural network architectures or low-level kernel routines from scratch.
- If you only ever fine-tune a single specific model family and require the absolute maximum token/sec training speed of direct [Unsloth](../infrastructure/unsloth.md) Python scripts.
- For pure prompt engineering tasks where weight modification is unnecessary.

## Getting started

### Installation
Clone the official repository and install dependencies with modern PyTorch support:

```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[metrics,bitsandbytes,qwen,deepspeed]" pydantic>=2.10.0
```

### Hello-world (CLI Status)
Verify the installation status:

```bash
llamafactory-cli version
```

### LLaMA Board (Web UI Launch)
Launch the interactive web dashboard:

```bash
llamafactory-cli webui
```

## CLI examples

### 1. Supervised Fine-Tuning (SFT via YAML Config)
Start a LoRA fine-tuning run using a YAML configuration:

```bash
llamafactory-cli train examples/train_lora/llama4_lora_sft.yaml
```

### 2. Exporting & Merging LoRA Weights
Merge LoRA adapter weights back into the full base checkpoint for serving:

```bash
llamafactory-cli export examples/merge_lora/llama4_lora_sft.yaml
```

### 3. Model Evaluation on Benchmark Sets
Run automated evaluation against standard benchmarking datasets:

```bash
llamafactory-cli eval examples/train_lora/llama4_lora_eval.yaml
```

## API examples

### Python High-Level Inference Interface (`ChatModel`)
```python
from typing import List, Dict, Any
from llamafactory.chat import ChatModel

# Configure fine-tuned model checkpoint loading
args: Dict[str, Any] = {
    "model_name_or_path": "meta-llama/Llama-4-Maverick-8B-Instruct",
    "adapter_name_or_path": "saves/llama4-8b/lora/sft",
    "template": "llama4",
    "finetuning_type": "lora",
}

chat_model = ChatModel(args)

# Execute query against fine-tuned model
messages = [{"role": "user", "content": "Generate a FastMCP 3.1 tool definition for system metrics."}]
responses = chat_model.chat(messages)

for response in responses:
    print("Agent Response:", response.response_text)
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — Enterprise patterns and guidelines.
- [Unsloth](../infrastructure/unsloth.md) — Memory-efficient fine-tuning backend.
- [vLLM](../infrastructure/vllm.md) — High-throughput inference server for fine-tuned checkpoints.
- [PEFT (Parameter-Efficient Fine-Tuning)](../infrastructure/peft.md) — Underlying adapter fine-tuning library.
- [Qwen](../ai_knowledge/qwen.md) — Popular target model family for domain adaptation.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol target for tool-calling model fine-tuning.

## Sources / references
- [LLaMA Factory GitHub Repository](https://github.com/hiyouga/LLaMA-Factory)
- [LLaMA Factory Official Documentation](https://llama-factory.readthedocs.io/)
- [DeepSpeed Optimization Library](https://www.deepspeed.ai/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
