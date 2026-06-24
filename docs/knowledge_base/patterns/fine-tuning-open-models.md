# Fine-tuning Open Models

## What it is
Fine-tuning is the process of continuing the training of a pre-trained language model on a curated dataset to adapt its behaviour, tone, knowledge, or task performance for a specific domain. Unlike Retrieval-Augmented Generation (RAG), fine-tuning modifies the model weights themselves, baking knowledge and behavioural patterns into the model rather than retrieving them at inference time. In June 2026, this is primarily performed on models like Llama 4, Qwen 2.5/3, and Mistral using parameter-efficient techniques.

## What problem it solves
Pre-trained open models are generalist and may:
- **Inconsistent Formatting**: Fail to follow a specific output format consistently (JSON, YAML).
- **Domain Blindness**: Lack domain terminology or institutional knowledge.
- **Instruction Adherence**: Perform poorly on narrow task types (e.g., extracting structured fields from a specific document type).
- **Style Alignment**: Respond in unwanted styles or languages.

Fine-tuning addresses these gaps without replacing the base model's general capabilities, often allowing a small 3B or 7B model to outperform a general 70B model on narrow tasks.

## Where it fits in the stack
**Model Adaptation Layer** — between the raw pre-trained base model (Layer 0) and the inference/serving infrastructure (Layer 1). Fine-tuning is an offline process; the resulting model is then served via [Ollama](../../services/ollama.md), [vLLM](../../tools/infrastructure/vllm.md), or [llama.cpp](../../tools/infrastructure/llama-cpp.md).

## Typical use cases
- **Structured Data Extraction**: Fine-tuning a small model (e.g., 3B or 7B) to consistently output JSON from messy OCR text.
- **Brand Voice Alignment**: Ensuring customer-facing agents always use a specific company tone and vocabulary.
- **SQL Generation**: Adapting a model to a specific database schema and dialect for [Text-to-SQL](../../architecture/data-copilot-text-to-sql.md) tasks.
- **Code Completion**: Training on a private codebase to provide context-aware autocomplete that understands internal libraries.
- **System Log Analysis**: Teaching a model to identify specific error patterns in proprietary server logs.
- **Agentic Skill Adaptation**: Teaching a model to better utilize specific tools defined in the [Agent Skills Best Practices](skills-best-practices.md) framework.

## Strengths
- **Zero Inference Overhead**: Knowledge is baked into weights; no retrieval latency.
- **Consistent Behavior**: Reliable format adherence and tone even without in-context examples.
- **Privacy**: Training data and model weights stay entirely on-premises.
- **Works with small models**: A fine-tuned 7B model can outperform a general 70B on narrow tasks.

## Limitations
- **Compute cost**: Training run requires significant GPU resources (NVIDIA Blackwell/Hopper) or high-memory Apple Silicon.
- **Static knowledge**: Model does not learn new facts after training cutoff; RAG is needed for dynamic data.
- **Expensive to update**: Retraining needed to incorporate new knowledge or updated schemas.
- **Risk of catastrophic forgetting**: Heavy fine-tuning can degrade general capabilities.
- **Data requirements**: Needs curated, high-quality datasets; bad data = bad model.

## When to use it
- When you need the model to follow a **rigid output format** (e.g., specific JSON schema) every time.
- To instill a **consistent persona or brand voice** across all interactions.
- When performing **narrow, high-repetition tasks** where a generalist model is too slow or expensive.
- To optimize models for **local execution** on edge hardware with limited context windows.

## When not to use it
- For **frequently updated factual information** — use RAG instead.
- If you need the model to **cite its sources** from a specific knowledge base.
- When the **base model already performs perfectly** with simple prompt engineering.
- If the **compute budget** is limited and the iteration speed of RAG is preferred.

## Getting started

### Fine-tuning vs RAG — decision guide

| Criterion | Fine-tune | RAG |
|---|---|---|
| **Knowledge type** | Style, format, task behaviour, domain vocabulary | Factual content, documents, up-to-date information |
| **Update frequency** | Rare (hours to retrain) | Continuous (update vector store) |
| **Cost** | High upfront (compute) | Low incremental (embedding + storage) |
| **Hallucination risk** | Reduced for in-distribution tasks | Reduced by grounding in retrieved context |
| **Privacy** | Weights stay local | Data stays in vector store |
| **Latency** | Zero (knowledge is in weights) | Adds retrieval time (~100–500 ms) |
| **Best for** | Consistent format/tone, narrow task types, instruction following | Q&A over documents, knowledge freshness, citations |

**Rule of thumb**: Use RAG first for factual knowledge. Use fine-tuning when you need the model to **behave** differently.

### Environment Setup (NVIDIA)
Most fine-tuning workflows in 2026 utilize `unsloth` for NVIDIA hardware.
```python
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-7B-Instruct",
    max_seq_length=4096,
    dtype=torch.bfloat16,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=16, lora_dropout=0, bias="none",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    use_gradient_checkpointing="unsloth",
    random_state=42,
)
```

## CLI examples

### MLX Fine-tuning (Apple Silicon)
```bash
# Fine-tune on MacBook M4 or Mac Studio
python -m mlx_lm.lora \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --train --data data/ --iters 1000 --batch-size 4 --lora-layers 16 --adapter-path adapters/

# Fuse adapter back into model
python -m mlx_lm.fuse \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --adapter-path adapters/ --save-path ./fused-model
```

### axolotl & LLaMA-Factory
```bash
# Axolotl YAML-driven training
accelerate launch -m axolotl.cli.train config.yaml

# LLaMA-Factory WebUI
llamafactory-cli webui
```

## API examples

### Hugging Face SFT Trainer
```python
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model, train_dataset=dataset,
    args=TrainingArguments(
        output_dir="./output", num_train_epochs=3,
        per_device_train_batch_size=2, learning_rate=2e-4,
        bf16=True, logging_steps=10
    ),
)
trainer.train()
```

### Dataset sizes & Compute Requirements

| Task type | Min examples | Recommended | Min VRAM (QLoRA) |
|---|---|---|---|
| Format adaptation | 100–500 | 1,000 | 7B Model: 8 GB |
| Domain vocabulary | 500–1,000 | 5,000 | 14B Model: 16 GB |
| Narrow task | 200–500 | 2,000 | 32B Model: 24 GB |

## Related tools / concepts
- [RAG Pattern](rag-pattern.md) — Factual knowledge retrieval.
- [Ollama](../../services/ollama.md) — For serving fine-tuned models locally.
- [vLLM](../../tools/infrastructure/vllm.md) — High-throughput serving engine.
- [llama.cpp](../../tools/infrastructure/llama-cpp.md) — For edge deployment of fine-tuned models.
- [LLaMA-Factory](../../tools/frameworks/llama-factory.md) — Unified training suite.
- [axolotl](../../tools/frameworks/axolotl.md) — Reproducible training pipelines.
- [Distilabel](../../tools/frameworks/distilabel.md) — Synthetic data generation for fine-tuning.
- [Agent Skills Best Practices](skills-best-practices.md) — Behaviors targeted by fine-tuning.

## Sources / references
- [LoRA (Hu et al., 2021)](https://arxiv.org/abs/2106.09685)
- [QLoRA (Dettmers et al., 2023)](https://arxiv.org/abs/2305.14314)
- [Unsloth — Fast LLM Fine-tuning](https://github.com/unslothai/unsloth)
- [MLX Examples — LoRA fine-tuning](https://github.com/ml-explore/mlx-examples/tree/main/llms/mlx_lm)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
