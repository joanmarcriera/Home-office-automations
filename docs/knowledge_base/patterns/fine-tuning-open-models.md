# Fine-tuning Open Models

## What it is
Fine-tuning is the process of continuing the training of a pre-trained language model on a curated dataset to adapt its behaviour, tone, knowledge, or task performance for a specific domain. Unlike Retrieval-Augmented Generation (RAG), fine-tuning modifies the model weights themselves, baking knowledge and behavioural patterns into the model rather than retrieving them at inference time. In late October / November 2026, this is primarily performed on state-of-the-art open weights models like **Llama 4**, **Qwen 3.6**, and **Gemma 3** using parameter-efficient techniques.

## What problem it solves
Pre-trained open models are generalist and may:
- **Inconsistent Formatting**: Fail to follow a specific output format consistently (JSON, YAML).
- **Domain Blindness**: Lack domain terminology or institutional knowledge.
- **Instruction Adherence**: Perform poorly on narrow task types (e.g., extracting structured fields from a specific document type).
- **Style Alignment**: Respond in unwanted styles or languages.

Fine-tuning addresses these gaps without replacing the base model's general capabilities, often allowing a small 8B or 12B model to outperform a general 70B model on narrow tasks.

## Where it fits in the stack
**Model Adaptation Layer** — between the raw pre-trained base model (Layer 0) and the inference/serving infrastructure (Layer 1). Fine-tuning is an offline process; the resulting model is then served via [Ollama](../../services/ollama.md), [vLLM](../../tools/infrastructure/vllm.md), or [llama.cpp](../../tools/infrastructure/llama-cpp.md).

## Typical use cases
- **Structured Data Extraction**: Fine-tuning a small model (e.g., 8B or 12B) to consistently output JSON from messy OCR text.
- **Brand Voice Alignment**: Ensuring customer-facing agents always use a specific company tone and vocabulary.
- **SQL Generation**: Adapting a model to a specific database schema and dialect for [Text-to-SQL](../../architecture/data-copilot-text-to-sql.md) tasks.
- **Code Completion**: Training on a private codebase to provide context-aware autocomplete that understands internal libraries.
- **System Log Analysis**: Teaching a model to identify specific error patterns in proprietary server logs.
- **Agentic Skill Adaptation**: Teaching a model to better utilize specific tools defined in the [Agent Skills Best Practices](skills-best-practices.md) framework.
- **Distillation Training**: Generating training data using teacher models like Claude 5.1, GPT-5.5, or Gemini 4.0-Flash-Lite, and training a smaller student model (e.g., Qwen 3.6 7B) on it.

## Strengths
- **Zero Inference Overhead**: Knowledge is baked into weights; no retrieval latency.
- **Consistent Behavior**: Reliable format adherence and tone even without in-context examples.
- **Privacy**: Training data and model weights stay entirely on-premises.
- **Works with small models**: A fine-tuned 8B model can outperform a general 70B on narrow tasks.

## Limitations
- **Compute cost**: Training run requires significant GPU resources (NVIDIA Blackwell Ultra, Hopper) or high-memory Apple Silicon (M4/M5 Max/Ultra).
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
Most fine-tuning workflows in late October / November 2026 utilize [unsloth](../../tools/infrastructure/unsloth.md) for NVIDIA hardware, optimized for **NVIDIA Blackwell Ultra** architectures, **Llama 4**, and **Gemma 3**.
```python
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/gemma-3-12b-it", # Late 2026 SOTA for open weights
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
# Fine-tune on MacBook M4/M5 or Mac Studio Ultra
python -m mlx_lm.lora \
  --model mlx-community/Qwen3.6-7B-Instruct-4bit \
  --train --data data/ --iters 1000 --batch-size 4 --lora-layers 16 --adapter-path adapters/

# Fuse adapter back into model
python -m mlx_lm.fuse \
  --model mlx-community/Qwen3.6-7B-Instruct-4bit \
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

### Hugging Face SFT Trainer with Pydantic v2 Hyperparameter Validation
We can enforce schema compliance and hyperparameter boundaries on fine-tuning jobs using Pydantic v2.

```python
from pydantic import BaseModel, Field, field_validator
from trl import SFTTrainer
from transformers import TrainingArguments

# Define Pydantic v2 schema for strict hyperparameter validation
class TrainingConfig(BaseModel):
    output_dir: str = Field("./output", description="Output path for weights")
    num_epochs: int = Field(3, ge=1, le=20, description="Number of epochs to train")
    batch_size: int = Field(2, ge=1, le=128, description="Batch size per device")
    learning_rate: float = Field(2e-4, gt=0, lt=1e-2, description="AdamW learning rate")
    bf16: bool = Field(True, description="Enable bfloat16 mixed precision")
    logging_steps: int = Field(10, ge=1)

    @field_validator("learning_rate")
    def check_learning_rate(cls, v: float) -> float:
        if v > 1e-3:
            # Generate a warning or raise error for high learning rates
            raise ValueError("Learning rate is exceptionally high for LoRA fine-tuning")
        return v

# Validate configuration
raw_config = {
    "output_dir": "./output_gemma3",
    "num_epochs": 4,
    "batch_size": 4,
    "learning_rate": 1e-4,
    "bf16": True,
    "logging_steps": 5
}

config = TrainingConfig.model_validate(raw_config)

# Instantiate HF TrainingArguments using validated properties
training_args = TrainingArguments(
    output_dir=config.output_dir,
    num_train_epochs=config.num_epochs,
    per_device_train_batch_size=config.batch_size,
    learning_rate=config.learning_rate,
    bf16=config.bf16,
    logging_steps=config.logging_steps
)

# Trainer setup example (stub)
# trainer = SFTTrainer(
#     model=model, train_dataset=dataset,
#     args=training_args
# )
# trainer.train()
print(f"Validated Fine-Tuning arguments successfully for output directory: {config.output_dir}")
```

### Dataset sizes & Compute Requirements

| Task type | Min examples | Recommended | Min VRAM (QLoRA) |
|---|---|---|---|
| Format adaptation | 100–500 | 1,000 | 8B Model (e.g., Llama 4 8B): 8 GB |
| Domain vocabulary | 500–1,000 | 5,000 | 14B Model (e.g., Qwen 3.6 14B): 16 GB |
| Narrow task | 200–500 | 2,000 | 32B Model (e.g., Qwen 3.6 32B): 24 GB |

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
- Last reviewed: 2026-11-05
- Confidence: high
