# Fine-tuning Open Models

## What it is

Fine-tuning is the process of continuing the training of a pre-trained language model on a curated dataset to adapt its behaviour, tone, knowledge, or task performance for a specific domain. Unlike Retrieval-Augmented Generation (RAG), fine-tuning modifies the model weights themselves, baking knowledge and behavioural patterns into the model rather than retrieving them at inference time.

## What problem it solves

Pre-trained open models are generalist. They may:
- Not follow a specific output format consistently
- Lack domain terminology or institutional knowledge
- Perform poorly on narrow task types (e.g., extracting structured fields from a specific document type)
- Respond in unwanted styles or languages

Fine-tuning addresses these gaps without replacing the base model's general capabilities.

## Where it fits in the stack

**Model Adaptation Layer** — between the raw pre-trained base model (Layer 0) and the inference/serving infrastructure (Layer 1). Fine-tuning is an offline process; the resulting model is then served via Ollama, vLLM, or similar.

```text
┌─────────────────────────────────────────────────────────┐
│         Training (offline, GPU/Apple Silicon)           │
│  Dataset → [Base Model] + [Adapter (LoRA)] → Fine-tuned │
└───────────────────────────┬─────────────────────────────┘
                            │  export GGUF / safetensors
┌───────────────────────────▼─────────────────────────────┐
│        Inference (Ollama / vLLM / llama.cpp)            │
│                                                         │
│  Agents: OpenClaw │ OpenHands │ n8n AI nodes            │
└─────────────────────────────────────────────────────────┘
```

## Fine-tuning vs RAG — decision guide

| Criterion | Fine-tune | RAG |
|---|---|---|
| **Knowledge type** | Style, format, task behaviour, domain vocabulary | Factual content, documents, up-to-date information |
| **Update frequency** | Rare (hours to retrain) | Continuous (update vector store) |
| **Cost** | High upfront (compute) | Low incremental (embedding + storage) |
| **Hallucination risk** | Reduced for in-distribution tasks | Reduced by grounding in retrieved context |
| **Privacy** | Weights stay local | Data stays in vector store |
| **Latency** | Zero (knowledge is in weights) | Adds retrieval time (~100–500 ms) |
| **Best for** | Consistent format/tone, narrow task types, instruction following | Q&A over documents, knowledge freshness, citations |

**Rule of thumb**: Use RAG first for factual knowledge. Use fine-tuning when you need the model to **behave** differently — follow a specific format, adopt a persona, or excel at a narrow task type it currently performs poorly on.

Combine both: fine-tune for behaviour + RAG for factual grounding.

## Approaches

### Parameter-Efficient Fine-Tuning (PEFT)

Trains only a small subset of parameters, dramatically reducing compute and memory requirements. The standard for home-lab and small-team fine-tuning.

**LoRA (Low-Rank Adaptation)**

Adds small rank-decomposition matrices to existing weight matrices. Only the adapter weights are trained; the base model is frozen. Adapters can be merged back into the base model for zero-latency inference.

```text
W_new = W_base + (A × B)    where A ∈ R^(d×r), B ∈ R^(r×k), r << d
```

- **Rank (r)**: Typical values 4–64; higher = more capacity but more VRAM
- **Alpha**: Scaling factor; usually set to 2× rank
- **Target modules**: Usually `q_proj`, `v_proj` (attention); sometimes all linear layers

**QLoRA (Quantised LoRA)**

Loads the base model in 4-bit NF4 quantisation, then trains LoRA adapters in bfloat16. Reduces VRAM by ~75% vs full fine-tuning. Enables fine-tuning 7B models on a 10 GB GPU or a MacBook M4.

**Full Fine-tuning**

All weights updated. Requires substantial VRAM (2× model size in bfloat16). Typically only worthwhile for models < 3B or when compute is unconstrained. Not recommended for home-lab use.

## Tools

### Unsloth

**Best for**: Fast LoRA/QLoRA fine-tuning on NVIDIA GPUs; 2–5× faster than vanilla transformers with 80% less VRAM.

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
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
)
```

```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

**Supports**: Llama 3, Qwen 2.5, Mistral, Gemma, Phi-3, CodeLlama, and more.

### LLaMA-Factory

**Best for**: No-code / low-code UI for training; supports 100+ model architectures; CLI and WebUI.

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"

# Launch WebUI
llamafactory-cli webui

# Or train from config YAML
llamafactory-cli train examples/train_lora/qwen2.5_7b_lora_sft.yaml
```

Includes dataset management, training monitoring, merge + export, and evaluation in one tool.

### axolotl

**Best for**: YAML-driven, reproducible training pipelines; excellent for teams and automation.

```yaml
# config.yaml
base_model: Qwen/Qwen2.5-7B-Instruct
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer

load_in_4bit: true
adapter: lora
lora_r: 16
lora_alpha: 32
lora_target_modules:
  - q_proj
  - v_proj

datasets:
  - path: data/my_dataset.jsonl
    type: sharegpt
    conversation: chatml

output_dir: ./output/qwen-finetuned
sequence_len: 4096
micro_batch_size: 2
gradient_accumulation_steps: 4
num_epochs: 3
learning_rate: 2e-4
```

```bash
pip install axolotl[flash-attn,deepspeed]
accelerate launch -m axolotl.cli.train config.yaml
```

### TRL / SFT Trainer (Hugging Face)

**Best for**: Custom training loops; maximum control; integrates with the full Hugging Face ecosystem.

```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

# Load model in 4-bit
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                 bnb_4bit_compute_dtype="bfloat16")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct", quantization_config=bnb_config, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

dataset = load_dataset("json", data_files="data/train.jsonl", split="train")

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
                          lora_dropout=0.05, bias="none", task_type="CAUSAL_LM")

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    args=SFTConfig(output_dir="./output", num_train_epochs=3,
                   per_device_train_batch_size=2, learning_rate=2e-4),
)
trainer.train()
trainer.save_model("./output/final")
```

### MLX Fine-tuning (Apple Silicon)

**Best for**: Fine-tuning on MacBook M4 or Mac Studio without NVIDIA GPU.

```bash
pip install mlx-lm

# Fine-tune Llama or Qwen using LoRA on Apple Silicon
python -m mlx_lm.lora \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --train \
  --data data/ \
  --iters 1000 \
  --batch-size 4 \
  --lora-layers 16 \
  --adapter-path adapters/

# Fuse adapter back into model
python -m mlx_lm.fuse \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --adapter-path adapters/ \
  --save-path ./fused-model
```

**MacBook M4 (16 GB unified memory)** can fine-tune 4-bit quantised 7B models at ~3–5 tokens/sec training throughput. Sufficient for small-to-medium datasets (< 50k examples).

## Dataset preparation

### Format (ShareGPT / ChatML)

The most common format for instruction fine-tuning:

```jsonl
{"conversations": [{"from": "human", "value": "Extract the invoice number from this document: ..."}, {"from": "gpt", "value": "{\"invoice_number\": \"INV-2024-0042\", ...}"}]}
{"conversations": [{"from": "human", "value": "..."}, {"from": "gpt", "value": "..."}]}
```

### Minimum dataset sizes

| Task type | Min examples | Recommended |
|---|---|---|
| Format adaptation (consistent output structure) | 100–500 | 1,000 |
| Domain vocabulary / tone | 500–1,000 | 5,000 |
| Narrow task type (specific extraction) | 200–500 | 2,000 |
| General instruction following improvement | 5,000 | 50,000+ |

### Data quality > quantity

100 high-quality, diverse examples outperform 1,000 noisy ones. Deduplicate, validate outputs, and include hard negative examples (cases where the model currently fails).

### Creating datasets from existing data

```python
# Convert Paperless-ngx documents to training examples
import json

def convert_paperless_doc(doc):
    """Turn a Paperless document into a fine-tuning example."""
    return {
        "conversations": [
            {
                "from": "human",
                "value": f"Extract key fields from this document:\n\n{doc['content'][:2000]}"
            },
            {
                "from": "gpt",
                "value": json.dumps({
                    "type": doc["document_type"],
                    "date": doc["created"],
                    "correspondent": doc["correspondent"],
                    "amount": doc.get("custom_fields", {}).get("amount")
                }, indent=2)
            }
        ]
    }
```

## Compute requirements

| Model size | Method | Min VRAM | Recommended | Training time (1k steps) |
|---|---|---|---|---|
| 1–3B | QLoRA | 4 GB | 6 GB | 5–10 min (T4) |
| 7B | QLoRA | 8 GB | 16 GB | 15–30 min (T4) |
| 7B | LoRA (bf16) | 16 GB | 24 GB | 20–40 min (A100) |
| 14B | QLoRA | 16 GB | 24 GB | 40–80 min (A100) |
| 32B | QLoRA | 24 GB | 40 GB | 2–4 hrs (A100) |
| 70B | QLoRA + DeepSpeed | 4× A100 80 GB | — | 8–16 hrs |

**Apple Silicon (M4 16 GB)**: Practical up to 7B QLoRA; 14B possible with patience.

## Free and low-cost training platforms

| Platform | Free tier | Notes |
|---|---|---|
| **Google Colab** | T4 GPU (15 GB), limited hours | Best for prototyping; Unsloth works well |
| **Hugging Face AutoTrain** | Pay-per-job (no free) | No-code UI; very easy for standard tasks |
| **Kaggle Notebooks** | 2× T4 (30 GB total), 30 hr/week | Good for 7B QLoRA |
| **Modal** | $30/month free credit | Serverless GPU; great for automation |
| **RunPod** | Pay-as-you-go from $0.20/hr | Best cost/performance for A100 |
| **Vast.ai** | Pay-as-you-go from $0.10/hr | Cheaper than RunPod; spot pricing |
| **Lambda Cloud** | Pay-as-you-go | Reliable; A100 and H100 available |

## Exporting and serving fine-tuned models

### Export to GGUF (for Ollama)

```bash
# After training with Unsloth — export directly to GGUF
model.save_pretrained_gguf(
    "my-model-q4",
    tokenizer,
    quantization_method="q4_k_m"    # q4_k_m is a good default
)

# Or convert from safetensors using llama.cpp
python llama.cpp/convert_hf_to_gguf.py ./output/final --outtype q4_k_m --outfile my-model.gguf
```

### Create an Ollama Modelfile

```text
# Modelfile
FROM ./my-model.gguf

SYSTEM """You are a document extraction assistant for a home office.
Always respond with valid JSON. Never add commentary outside the JSON object."""

PARAMETER temperature 0.1
PARAMETER num_ctx 4096
```

```bash
ollama create my-extraction-model -f Modelfile
ollama run my-extraction-model "Extract fields from: ..."
```

After creating the model in Ollama, it becomes available to all tools in the stack (OpenClaw, OpenHands, n8n, LiteLLM) just like any other model.

## Evaluation

After fine-tuning, evaluate on a held-out test set before deploying:

```python
from trl import create_reference_model
# Compare fine-tuned vs base model on your test set
# Metrics: exact match, ROUGE, format adherence rate, task-specific accuracy
```

Practical checklist:
- [ ] Test on 50–100 held-out examples from the same distribution
- [ ] Test on 10–20 **out-of-distribution** examples (adversarial inputs)
- [ ] Measure format adherence rate (JSON validity, required fields present)
- [ ] Compare against base model on a general benchmark (e.g., MMLU subset) to check for catastrophic forgetting
- [ ] Monitor inference quality in production for the first 2 weeks

## Common failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Model ignores system prompt after fine-tuning | Training data lacked system prompt in correct position | Include system prompt in every training example |
| Repetition / looping | Learning rate too high, or dataset has many near-duplicates | Lower LR; deduplicate dataset |
| Format regression (good format → inconsistent after fine-tuning) | Dataset has inconsistent output formats | Standardise all outputs in dataset |
| Catastrophic forgetting (general capability drops) | Too many epochs or large r | Reduce epochs; lower LoRA rank; mix general data |
| High perplexity on validation set | Dataset too small or overfitting | More data; apply early stopping; increase dropout |

## Strengths

- **Zero inference overhead**: Knowledge is in weights; no retrieval latency
- **Consistent behaviour**: Reliable format adherence and tone even without in-context examples
- **Privacy**: Training data and model stay on-premises
- **Works with small models**: A fine-tuned 3B model can outperform a general 70B on narrow tasks

## Limitations

- **Compute cost**: Training run requires GPU; free tiers have limited hours
- **Static knowledge**: Fine-tuned model does not know about events after training cutoff
- **Expensive to update**: Retraining needed to incorporate new knowledge
- **Risk of catastrophic forgetting**: Heavy fine-tuning can degrade general capabilities
- **Data requirements**: Needs curated, high-quality datasets; bad data = bad model

## When to use it

- When the model needs to **reliably follow a specific output format** (structured JSON, specific template)
- When the model should adopt a **consistent persona or tone** without relying on long system prompts
- When you have a **narrow, repetitive task** (e.g., extracting fields from a specific document type) where general models underperform
- When you want the model's capabilities **without retrieval latency** for a known domain
- When your dataset contains **institutional knowledge** not present in public training data

## When not to use it

- When knowledge needs to be **updated frequently** — use RAG instead
- When you need to **cite sources** — RAG provides provenance, fine-tuning does not
- When the **base model already performs well** on the task with a good system prompt
- When compute budget is limited and RAG can solve the problem — RAG is cheaper to iterate
- When the task requires the full knowledge of a large model that is too expensive to fine-tune

## Related tools / concepts

- [RAG Pattern](rag.md) — complementary approach; fine-tune for behaviour + RAG for facts
- [Ollama](../../services/ollama.md) — serve fine-tuned GGUF models locally
- [vLLM](../../tools/infrastructure/vllm.md) — high-throughput serving of fine-tuned models
- [MLX](../../tools/infrastructure/mlx.md) — Apple Silicon inference and fine-tuning framework
- [llama.cpp](../../tools/infrastructure/llama-cpp.md) — GGUF format reference implementation
- [OpenPipe](../../tools/infrastructure/openpipe.md) — managed fine-tuning pipeline service
- [LM Studio](../../tools/ai_knowledge/lm-studio.md) — local model management and testing
- [Document Preparation for LLM Training](../../playbooks/document-preparation-for-llm-training.md) — playbook for dataset preparation from local documents

## Sources / References

- [LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021)](https://arxiv.org/abs/2106.09685)
- [QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., 2023)](https://arxiv.org/abs/2305.14314)
- [Unsloth — Fast LLM Fine-tuning](https://github.com/unslothai/unsloth)
- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
- [axolotl](https://github.com/axolotl-ai-cloud/axolotl)
- [Hugging Face TRL — SFT Trainer](https://huggingface.co/docs/trl/sft_trainer)
- [MLX Examples — LoRA fine-tuning](https://github.com/ml-explore/mlx-examples/tree/main/llms/mlx_lm)

## Contribution Metadata

- Last reviewed: 2026-03-21
- Confidence: high
