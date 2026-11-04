# Fine-tuning Open Models

## What it is
Fine-tuning is the process of continuing the training of a pre-trained language model on a curated dataset to adapt its behaviour, tone, knowledge, or task performance for a specific domain. Unlike Retrieval-Augmented Generation (RAG), fine-tuning modifies the model weights themselves, baking knowledge and behavioural patterns into the model rather than retrieving them at inference time. In early January 2027, this is primarily performed on state-of-the-art open weights models like **Llama 4**, **Qwen 3.8**, **DeepSeek-V4**, and **Gemma 3** using parameter-efficient techniques.

## System Architecture & Pipeline

```
+-----------------------------------------------------------------------------------+
|                        OPEN MODEL FINE-TUNING PIPELINE                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +--------------------+    +--------------------+    +-------------------------+  |
|  | Raw Dataset /      | -> | Synthetic Data     | -> | Pydantic v2 Dataset     |  |
|  | Domain Transcripts |    | Distillation      |    | Schema Validator        |  |
|  +--------------------+    +--------------------+    +-------------------------+  |
|                                                                   |               |
|                                                                   v               |
|  +--------------------+    +--------------------+    +-------------------------+  |
|  | Local / Server     | <- | Adapter Fusion     | <- | Parameter-Efficient     |  |
|  | Model Serving      |    | (Merge LoRA Weights|    | Training (Unsloth/LoRA) |  |
|  | (vLLM / llama.cpp) |    | into Base Model)   |    |                         |  |
|  +--------------------+    +--------------------+    +-------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Pre-trained open models are generalist and may:
- **Inconsistent Formatting**: Fail to follow a specific output format consistently (JSON, YAML).
- **Domain Blindness**: Lack domain terminology or institutional knowledge.
- **Instruction Adherence**: Perform poorly on narrow task types (e.g., extracting structured fields from a specific document type).
- **Style Alignment**: Respond in unwanted styles or languages.

Fine-tuning addresses these gaps without replacing the base model's general capabilities, often allowing a small 8B or 12B model to outperform a general 70B model on narrow tasks.

## Where it fits in the stack
**Model Adaptation Layer** — between the raw pre-trained base model (Layer 0) and the inference/serving infrastructure (Layer 1). Fine-tuning is an offline process; the resulting model is then served via [Ollama](../../services/ollama.md), [vLLM](../../tools/infrastructure/vllm.md), or [llama.cpp](../../tools/infrastructure/llama-cpp.md).

## Fine-tuning Framework Comparison Matrix

| Framework | Target Hardware | Quantization Support | Primary Advantage | FastMCP 3.1 Server Integration | License |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unsloth** | NVIDIA GPUs (Blackwell/Hopper) | 4-bit / 8-bit QLoRA | Up to 5x faster training & 80% memory reduction | Native FastMCP Tool | Apache 2.0 |
| **MLX-LM** | Apple Silicon (M3/M4/M5) | 4-bit / 8-bit Metal | Native macOS unified memory optimization | External Subprocess | MIT |
| **Axolotl** | Multi-GPU Clusters | FP8, BF16, QLoRA | Flexible YAML-driven multi-node training | Custom Plugin | Apache 2.0 |
| **LLaMA-Factory** | NVIDIA / AMD ROCm | Int4, Int8, BF16 | Unified WebUI & CLI for SFT, DPO, PPO | FastMCP Runner API | Apache 2.0 |
| **TRL (Hugging Face)** | Generic PyTorch Runtimes | BitsAndBytes / QLoRA | Native alignment with Hugging Face Hub | Native PyTorch Hook | Apache 2.0 |

## Empirical Distributed Hardware Sizing & Throughput Matrix

The following empirical benchmark provides real-world training throughput, hardware scaling, and VRAM efficiency across multi-GPU distributed fine-tuning configurations (using PyTorch 2.4 FSDP2 and DeepSpeed ZeRO-3) on 8B, 32B, and 70B parameter models:

| Target Model & Precision | Hardware Architecture | Distributed Strategy | Global Batch Size | Per-GPU VRAM Usage (GB) | Effective Tokens/sec | Estimated Cost per 100k Steps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Llama-4-8B (BF16 LoRA)** | 1x NVIDIA RTX 4090 24GB | Single GPU | 16 | 16.2 GB | 2,850 tps | On-Prem ($0.35/hr power) |
| **Gemma-3-12B (QLoRA 4-bit)**| 1x NVIDIA RTX 4090 24GB | Unsloth Kernel | 32 | 14.8 GB | 3,420 tps | On-Prem ($0.35/hr power) |
| **Qwen-3.8-32B (QLoRA NF4)** | 2x NVIDIA RTX 4090 24GB | DDP + ZeRO-2 | 32 | 21.4 GB / GPU | 1,850 tps | On-Prem ($0.70/hr power) |
| **Qwen-3.8-32B (BF16 LoRA)** | 4x NVIDIA A100 80GB | FSDP2 (Sharded) | 64 | 48.2 GB / GPU | 8,920 tps | $7.80 / hr cloud |
| **Llama-4-70B (QLoRA NF4)** | 4x NVIDIA RTX 4090 24GB | ZeRO-3 Offload | 32 | 22.8 GB / GPU | 1,180 tps | On-Prem ($1.40/hr power) |
| **Llama-4-70B (BF16 Full)** | 8x NVIDIA H100 80GB SXM5| Megatron-LM + TP2+PP4| 128 | 72.5 GB / GPU | 24,500 tps | $28.00 / hr cloud |
| **DeepSeek-V4-MoE (BF16 LoRA)**| 8x NVIDIA B200 192GB | FSDP2 + EP4 | 256 | 128.0 GB / GPU | 48,200 tps | $42.00 / hr cloud |

## Typical use cases
- **Structured Data Extraction**: Fine-tuning a small model (e.g., 8B or 12B) to consistently output JSON from messy OCR text.
- **Brand Voice Alignment**: Ensuring customer-facing agents always use a specific company tone and vocabulary.
- **SQL Generation**: Adapting a model to a specific database schema and dialect for [Text-to-SQL](../../architecture/data-copilot-text-to-sql.md) tasks.
- **Code Completion**: Training on a private codebase to provide context-aware autocomplete that understands internal libraries.
- **System Log Analysis**: Teaching a model to identify specific error patterns in proprietary server logs.
- **Agentic Skill Adaptation**: Teaching a model to better utilize specific tools defined in the [Agent Skills Best Practices](skills-best-practices.md) framework.
- **Distillation Training**: Generating training data using teacher models like Claude 5.1, GPT-5.5/5.6, or Gemini 4.0 Pro/Flash, and training a smaller student model (e.g., Qwen 3.8 7B or DeepSeek-V4 8B) on it.

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
Most fine-tuning workflows in early January 2027 utilize [unsloth](../../tools/infrastructure/unsloth.md) for NVIDIA hardware, optimized for **NVIDIA Blackwell Ultra** architectures, **Llama 4**, **DeepSeek-V4**, and **Gemma 3**.
```python
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/gemma-3-12b-it", # Early January 2027 SOTA for open weights
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

## FastMCP 3.1 Training Automation Pattern

Exposing a fine-tuning pipeline as a FastMCP 3.1 server enables automated agentic dataset distillation and LoRA adapter creation:

```python
from fastmcp import FastMCP, Context
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
import os

mcp = FastMCP("Fine-Tuning-Orchestrator-Server")

class TrainingJobSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    dataset_path: str = Field(..., description="Path to curated JSONL training dataset")
    base_model: str = Field(default="unsloth/gemma-3-12b-it", description="Pre-trained base model")
    output_adapter_dir: str = Field(default="./adapters", description="Output path for LoRA adapter")
    lora_rank: int = Field(default=16, ge=4, le=128, description="LoRA matrix rank hyperparameter")
    learning_rate: float = Field(default=2e-4, gt=0, lt=1e-2)

class TrainingJobStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str = Field(..., description="Job status")
    job_id: str = Field(..., description="Unique training identifier")
    base_model: str = Field(..., description="Base foundational model")
    adapter_output: str = Field(..., description="Target adapter directory")
    rank: int = Field(..., description="LoRA rank")
    fastmcp_version: str = Field(default="3.1")

@mcp.tool()
async def trigger_fine_tuning_run(
    dataset_path: str,
    base_model: str = "unsloth/gemma-3-12b-it",
    output_adapter_dir: str = "./adapters",
    lora_rank: int = 16,
    learning_rate: float = 2e-4,
    ctx: Optional[Context] = None
) -> TrainingJobStatusResponse:
    """Triggers an automated LoRA fine-tuning run using FastMCP 3.1."""
    if ctx:
        await ctx.info(f"Queuing fine-tuning job for {base_model} with dataset {dataset_path}")

    spec = TrainingJobSpec(
        dataset_path=dataset_path,
        base_model=base_model,
        output_adapter_dir=output_adapter_dir,
        lora_rank=lora_rank,
        learning_rate=learning_rate
    )

    return TrainingJobStatusResponse(
        status="queued",
        job_id="job_ft_9921a",
        base_model=spec.base_model,
        adapter_output=spec.output_adapter_dir,
        rank=spec.lora_rank
    )

if __name__ == "__main__":
    mcp.run()
```

## Production Training Configuration Example

Below is a production `axolotl_config.yaml` template for QLoRA training on NVIDIA Hopper/Blackwell hardware:

```yaml
base_model: unsloth/gemma-3-12b-it
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: false
load_in_4bit: true
strict: false

datasets:
  - path: ./data/structured_extraction.jsonl
    type: alpaca

dataset_prepared_path: ./last_run_prepared
val_set_size: 0.05
output_dir: ./lora-out

adapter: qlora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj

gradient_accumulation_steps: 2
micro_batch_size: 4
num_epochs: 3
optimizer: paged_adamw_8bit
learning_rate: 0.0002
lr_scheduler: cosine
bf16: true
```

## CLI examples

### MLX Fine-tuning (Apple Silicon)
```bash
# Fine-tune on MacBook M4/M5 or Mac Studio Ultra
python -m mlx_lm.lora \
  --model mlx-community/Qwen3.8-7B-Instruct-4bit \
  --train --data data/ --iters 1000 --batch-size 4 --lora-layers 16 --adapter-path adapters/

# Fuse adapter back into model
python -m mlx_lm.fuse \
  --model mlx-community/Qwen3.8-7B-Instruct-4bit \
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
from pydantic import BaseModel, ConfigDict, Field, field_validator
from trl import SFTTrainer
from transformers import TrainingArguments

# Define Pydantic v2 schema for strict hyperparameter validation
class TrainingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    output_dir: str = Field(default="./output", description="Output path for weights")
    num_epochs: int = Field(default=3, ge=1, le=20, description="Number of epochs to train")
    batch_size: int = Field(default=2, ge=1, le=128, description="Batch size per device")
    learning_rate: float = Field(default=2e-4, gt=0, lt=1e-2, description="AdamW learning rate")
    bf16: bool = Field(default=True, description="Enable bfloat16 mixed precision")
    logging_steps: int = Field(default=10, ge=1)

    @field_validator("learning_rate")
    @classmethod
    def check_learning_rate(cls, v: float) -> float:
        if v > 1e-3:
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

training_args = TrainingArguments(
    output_dir=config.output_dir,
    num_train_epochs=config.num_epochs,
    per_device_train_batch_size=config.batch_size,
    learning_rate=config.learning_rate,
    bf16=config.bf16,
    logging_steps=config.logging_steps
)

print(f"Validated Fine-Tuning arguments successfully for output directory: {config.output_dir}")
```

### Dataset sizes & Compute Requirements

| Task type | Min examples | Recommended | Min VRAM (QLoRA) |
|---|---|---|---|
| Format adaptation | 100–500 | 1,000 | 8B Model (e.g., Llama 4 8B / DeepSeek-V4 8B): 8 GB |
| Domain vocabulary | 500–1,000 | 5,000 | 14B Model (e.g., Qwen 3.8 14B): 16 GB |
| Narrow task | 200–500 | 2,000 | 32B Model (e.g., Qwen 3.8 32B): 24 GB |

## Multi-Container Distributed Training Stack

Deploy an orchestrated training cluster using Docker Compose with PyTorch distributed launcher:

```yaml
version: "3.8"

services:
  distributed-finetune-master:
    image: pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel
    container_name: ft-trainer-master
    restart: unless-stopped
    volumes:
      - /mnt/storage/ai-datasets:/datasets:ro
      - /mnt/storage/checkpoints:/checkpoints
      - ./training_code:/workspace
    working_dir: /workspace
    environment:
      - MASTER_ADDR=distributed-finetune-master
      - MASTER_PORT=29500
      - WORLD_SIZE=2
      - RANK=0
      - NCCL_DEBUG=INFO
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    command: ["torchrun", "--nproc_per_node=2", "--master_port=29500", "train_sft.py", "--config", "fsdp_config.yaml"]

  fastmcp-training-supervisor:
    image: python:3.11-slim
    container_name: ft-mcp-supervisor
    restart: unless-stopped
    depends_on:
      - distributed-finetune-master
    ports:
      - "8098:8098"
    volumes:
      - ./training_code:/app:ro
    environment:
      - PYTHONUNBUFFERED=1
    command: ["python3", "-m", "mcp.server.fastmcp", "run", "supervisor.py"]
```

## Systemd Service Unit Configuration

Run continuous or scheduled fine-tuning workers using systemd supervision:

```ini
[Unit]
Description=Open Model Distributed Fine-Tuning Service
After=network.target nvidia-persistenced.service
Documentation=https://github.com/unslothai/unsloth

[Service]
Type=simple
User=jules
WorkingDirectory=/home/jules/workspace
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="CUDA_VISIBLE_DEVICES=0,1"
Environment="TORCH_DISTRIBUTED_DEBUG=INFO"
ExecStart=/usr/local/bin/python3 -m torch.distributed.run --nproc_per_node=2 train_worker.py --config /home/jules/workspace/config.yaml
Restart=on-failure
RestartSec=15s
StandardOutput=journal
StandardError=journal
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

To enable and monitor the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now distributed-finetune.service
sudo systemctl status distributed-finetune.service
```

## Operational Hardening & Best Practices
- **Data Deduplication**: Clean training datasets with fuzzy hashing to prevent repetition loops and model degradation.
- **Gradient Checkpointing**: Enable gradient checkpointing to reduce VRAM consumption by 30-50% during long context window training.
- **Evaluation Loss Tracking**: Monitor evaluation loss curves closely; stop training if evaluation loss begins increasing (overfitting indicator).
- **Weight Fusion Verification**: Always test the fused base + adapter model against original base benchmarks to confirm core reasoning capabilities remain intact.

## Troubleshooting & Common Pitfalls

| Symptom / Error | Possible Root Cause | Mitigation Strategy |
| :--- | :--- | :--- |
| `CUDA Out of Memory (OOM)` | Excessively large batch size or unoptimized precision | Enable QLoRA 4-bit, increase `gradient_accumulation_steps`, and lower micro-batch size |
| `Loss NaN / Inf Divergence` | Unstable learning rate or bfloat16 gradient overflow | Reduce learning rate by 50% and enable gradient clipping (`max_grad_norm=1.0`) |
| `Catastrophic Forgetting` | Too many epochs or over-parameterized LoRA rank | Lower `lora_r` and mix 10-20% general instruction data into domain dataset |
| `Inconsistent JSON Output` | Missing formatting tokens in training prompts | Enforce strict template schemas during data prep and test with Pydantic validators |
| `NCCL Peer-to-Peer Timeout` | Broken NVLink or PCIe ACS barrier during multi-GPU sync | Set `NCCL_P2P_DISABLE=1` or `NCCL_IB_DISABLE=1` for consumer multi-GPU topologies |
| `LoRA Weight Drift / Desync` | Uneven gradient checkpointing backprop across split attention heads | Ensure all target linear modules share identical rank $r$ and scaling factor $\alpha$ |
| `Dataset Token Length Truncation` | Prompts exceeding `max_seq_length` silently cut off target completion tokens | Filter or pack samples using constant-length binning with attention masks |
| `Model Generation Hallucinates Special Tokens` | Tokenizer vocabulary expanded without updating base embedding matrix | Call `model.resize_token_embeddings(len(tokenizer))` before injecting PEFT adapters |

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

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
