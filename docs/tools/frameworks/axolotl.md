# Axolotl

## What it is
Axolotl is an open-source, configuration-driven LLM fine-tuning framework designed to streamline, standardize, and accelerate the fine-tuning, domain adaptation, and alignment of Large Language Models (LLMs) and Vision-Language Models (VLMs). As of early 2027 (v0.6.x+), Axolotl serves as an industry-standard framework for training state-of-the-art open-weights model families, including Llama 4 Maverick, DeepSeek-V4, Qwen 3.6 VL, Gemma 3, and Mistral NeMo.

Built on top of PyTorch, Hugging Face Transformers, PEFT, TRL, DeepSpeed, and PyTorch Fully Sharded Data Parallel (FSDP), Axolotl eliminates thousands of lines of boilerplate PyTorch code. It allows machine learning engineers and researchers to express complete training runs—including model loading, quantization specs, multi-dataset tokenization, multi-pack sample packing, loss algorithms (SFT, DPO, IPO, KTO, ORPO, GRPO), and multi-GPU cluster scheduling—inside a single, version-controlled YAML configuration file.

## What problem it solves
Training modern LLMs and agentic foundation models introduces significant engineering overhead:
- **Complex Boilerplate & Custom Code**: Writing custom PyTorch distributed loops, gradient accumulation logic, mixed-precision scaling, and dataset tokenizers for every new model architecture is time-consuming and error-prone.
- **Hardware & Multi-GPU Orchestration**: Setting up multi-node multi-GPU clusters using DeepSpeed ZeRO-3 or PyTorch FSDP requires intricate CUDA device synchronization and memory management.
- **Lack of Training Reproducibility**: Inconsistent tokenization settings, prompt templates, and hyperparameter variations make it difficult to replicate experimental fine-tuning runs.
- **Inference Inefficiency & Padding Overhead**: Training on variable-length conversation datasets without sample packing leads to wasted GPU compute on zero-padding tokens.

Axolotl solves these problems by providing a declarative, reproducible YAML interface. It features built-in multi-pack sample packing (which increases GPU throughput by up to 3x), native integration with FlashAttention-4, out-of-the-box DeepSpeed/FSDP distributed launchers, and automatic pre-tokenization dataset validation.

## Where it fits in the stack
**Frameworks / Model Fine-Tuning & Alignment Layer**.

Axolotl operates downstream of synthetic dataset generation pipelines (distilabel, Synthetic Data Generator) and upstream of production inference serving runtimes (vLLM, Baseten, Ollama, TGI).

```
+-----------------------------------------------------------------------------------+
|                        Dataset Generation & Curation                              |
|           (distilabel / Argilla / Hugging Face Datasets / Synthetic Generators)   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v  (Formatted Instruct / DPO Datasets)
+-----------------------------------------------------------------------------------+
|                            Axolotl Fine-Tuning Framework                          |
|                                                                                   |
|  +------------------------+  +------------------------+  +---------------------+  |
|  | Declarative YAML Engine|  | Pre-Tokenization Pipeline|  | Multi-Pack Sampler |  |
|  +------------------------+  +------------------------+  +---------------------+  |
|  | DeepSpeed ZeRO-3 / FSDP|  | FlashAttention-4 / FP8 |  | SFT / DPO / GRPO    |  |
|  +------------------------+  +------------------------+  +---------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v  (Merged Model Weights / LoRA Adapters)
+-----------------------------------------------------------------------------------+
|                        Inference & Agent Execution Stack                          |
|         (vLLM / Baseten / Ollama / FastMCP 3.1 Swarms / Claude Code)              |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Multi-GPU Supervised Fine-Tuning (SFT)**: Fine-tuning 70B+ parameter models across H100/A100 clusters using FSDP2 or DeepSpeed ZeRO-3.
- **Direct Preference Alignment (DPO/GRPO)**: Aligning instruction models against preference datasets to improve reasoning accuracy and reduce hallucinations.
- **Domain Adaptation for Enterprise Knowledge**: Training Llama 4 or Qwen 3.6 on domain-specific medical, legal, or code corpora.
- **Quantized LoRA / QLoRA Training**: Fine-tuning 8B-34B parameter models on single consumer or workstation GPUs (NVIDIA RTX 4090/A6000) using 4-bit/8-bit bitsandbytes quantization.
- **FastMCP 3.1 Tool-Calling Model Customization**: Fine-tuning foundation models specifically on structured JSON tool-calling schemas for agent runtimes.

## Architecture & Core Mechanics

### Architecture Diagram: Axolotl Distributed Training Architecture

```
[ Axolotl YAML Config (config.yml) ]
                 |
                 v
+------------------------------------+
|  Configuration & Schema Parser     |
|  - Parameter Verification          |
|  - Hardware Profile Check          |
+------------------------------------+
                 |
                 v
+------------------------------------+
|  Pre-tokenization & Sample Pack    |
|  - Dataset Blending & Filtering    |
|  - Multipack Tokenizer (0 Padding) |
+------------------------------------+
                 |
                 v
+------------------------------------+
|  Distributed Execution Launcher    |
|  (Accelerate / DeepSpeed / FSDP)   |
+------------------------------------+
                 |
        +--------+--------+
        |                 |
        v                 v
+---------------+ +---------------+
|  GPU Rank 0   | |  GPU Rank N   |
|  - FlashAttn4 | |  - FlashAttn4 |
|  - LoRA/QLoRA | |  - LoRA/QLoRA |
|  - FP8/BF16   | |  - FP8/BF16   |
+---------------+ +---------------+
        |                 |
        +--------+--------+
                 |
                 v
+------------------------------------+
|  Adapter Export / Weight Merging   |
|  - Hugging Face Hub Push           |
|  - GGUF / vLLM Format Conversion   |
+------------------------------------+
```

### Key Subsystems & Features

1. **Declarative YAML System**: Axolotl abstracts complex PyTorch trainer parameters into clear YAML fields. Settings cover base model paths, dataset mappings, sequence lengths, learning rate schedulers, LoRA rank/alpha, sample packing, and gradient checkpointing.
2. **Multi-Pack Sample Packing Engine**: Standard fine-tuning pads variable-length sequences to `sequence_len`, wasting up to 50% of VRAM and compute. Axolotl's sample packing concatenates multiple short conversation samples into a single full-length context window without cross-sample attention leakage, drastically accelerating training speed.
3. **Loss Algorithm Extensions**:
   - **SFT (Supervised Fine-Tuning)**: Standard cross-entropy loss over target token sequences.
   - **DPO / IPO / KTO**: Direct preference optimization algorithms for aligning models without needing a separate reward model.
   - **GRPO (Group Relative Policy Optimization)**: Advanced reinforcement learning strategy used for reasoning models like DeepSeek-R1/V4.
4. **Hardware Distribution Runtimes**: Out-of-the-box integration with PyTorch Accelerate, DeepSpeed (ZeRO-1, ZeRO-2, ZeRO-3), and PyTorch FSDP/FSDP2 for seamless scaling from single GPUs to multi-node clusters.

## Strengths
- **Declarative Reproducibility**: Complete training experiments defined in single YAML configs that can be committed to Git.
- **Maximum GPU Throughput**: Sample packing and FlashAttention-4 integration maximize token processing speed.
- **Broad Model Family Support**: Native support for Llama 4, Qwen 3.6, DeepSeek-V4, Gemma 3, Mistral, and custom architecture extensions.
- **Extensible Dataset Formats**: Built-in parsers for Alpaca, ShareGPT, ChatML, OpenAI Messages, DPO preference pairs, and custom JSONL schemas.
- **Active Community & Ecosystem**: Maintained by Axolotl AI Cloud with continuous releases for newly open-sourced architectures.

## Limitations
- **Parameter Synergy Complexity**: A typical production YAML configuration can contain over 100 parameters; incorrect combinations (e.g. mismatching `learning_rate` with `gradient_accumulation_steps`) can lead to loss divergence.
- **Obscure Error Traces**: Misconfigured dataset keys or YAML indents can produce cryptic stack traces from deep inside Hugging Face or PyTorch libraries.

## When to use it
- Training or fine-tuning open-weights models across single or multi-GPU environments using a reproducible YAML setup.
- Requiring high training throughput using multi-pack sample packing on large instruction datasets.
- Fine-tuning reasoning or agentic models using preference alignment algorithms like DPO or GRPO.

## When not to use it
- Requiring a GUI/web-based no-code interface (use LLaMA Factory instead).
- Fine-tuning simple 1B-3B models on low-VRAM single consumer GPUs where specialized memory kernels are preferred (use Unsloth instead).

## Getting started

### Installation
Install Axolotl in a Python 3.11/3.12 environment with CUDA 12.x support:

```bash
git clone https://github.com/axolotl-ai-cloud/axolotl
cd axolotl
pip install -e .[flash-attn,deepspeed]
```

### Basic Training Configuration (`config.yml`)

```yaml
base_model: meta-llama/Llama-3.2-3B-Instruct
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: false
load_in_4bit: true

datasets:
  - path: vicgalle/alpaca-gpt4
    type: alpaca

dataset_prepared_path: ./last_run_prepared
val_set_size: 0.05
output_dir: ./lora-out

adapter: qlora
lora_r: 32
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj

sequence_len: 4096
sample_packing: true
pad_to_sequence_len: true

gradient_accumulation_steps: 4
micro_batch_size: 2
num_epochs: 3
optimizer: adamw_torch
learning_rate: 0.0002

lr_scheduler: cosine
flash_attention: true
bf16: true
```

## CLI examples

```bash
# Preprocess and tokenize datasets to inspect token counts and sample packing
python -m axolotl.cli.preprocess config.yml

# Start distributed training using Accelerate launcher
accelerate launch -m axolotl.cli.train config.yml

# Merge trained QLoRA/LoRA adapter weights back into full base model weights
python -m axolotl.cli.merge_lora config.yml --lora_model_dir="./lora-out"

# Export merged model to Hugging Face Hub
python -m axolotl.cli.merge_lora config.yml --hf_repo_id="my-org/llama-custom-v1"
```

## API examples

### 1. FastMCP 3.1 Training Orchestration & Validation Server

This executable Python script defines a FastMCP 3.1 server exposing an Axolotl configuration validator and training execution tool, using strict Pydantic v2 schemas.

```python
import os
import yaml
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from fastmcp import FastMCP

# Instantiate FastMCP 3.1 Server
mcp = FastMCP(
    name="Axolotl Training Manager",
    version="3.1.0",
    description="FastMCP server for validating Axolotl training configs and initiating fine-tuning runs."
)

# ------------------------------------------------------------------
# Pydantic v2 Configuration Validation Schema
# ------------------------------------------------------------------

class DatasetConfig(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    path: str = Field(..., description="Hugging Face dataset path or local JSONL file.")
    type: str = Field(..., description="Dataset format (e.g. alpaca, sharegpt, chatml).")


class AxolotlValidationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    base_model: str = Field(..., description="Base model Hugging Face repository or path.")
    val_set_size: float = Field(default=0.05, ge=0.0, le=0.5)
    adapter: Literal["lora", "qlora", "full"] = Field(default="qlora")
    lora_r: Optional[int] = Field(default=32, ge=8, le=512)
    lora_alpha: Optional[int] = Field(default=16, ge=8, le=512)
    sequence_len: int = Field(default=4096, ge=512, le=131072)
    sample_packing: bool = Field(default=True)
    datasets: List[DatasetConfig] = Field(..., min_items=1)

    @field_validator("base_model")
    @classmethod
    def check_model_repo(cls, value: str) -> str:
        if "/" not in value and not os.path.exists(value):
            raise ValueError("base_model must be a valid Hugging Face 'org/repo' string or local directory.")
        return value

    @model_validator(mode="after")
    def check_adapter_settings(self) -> 'AxolotlValidationRequest':
        if self.adapter in ["lora", "qlora"]:
            if not self.lora_r or not self.lora_alpha:
                raise ValueError("lora_r and lora_alpha must be defined when using lora/qlora adapters.")
        return self


class AxolotlValidationResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    is_valid: bool = Field(...)
    summary_message: str = Field(...)
    estimated_vram_gb: float = Field(..., description="Estimated peak VRAM requirement per GPU.")


# ------------------------------------------------------------------
# FastMCP Tool Implementation
# ------------------------------------------------------------------

@mcp.tool(
    name="validate_axolotl_config",
    description="Validates an Axolotl YAML configuration payload against Pydantic v2 schemas before cluster launch."
)
def validate_axolotl_config(config_yaml_str: str) -> AxolotlValidationResponse:
    """
    Parses and validates Axolotl YAML configuration text.
    """
    try:
        raw_dict = yaml.safe_load(config_yaml_str)
        validated_config = AxolotlValidationRequest(**raw_dict)
    except Exception as exc:
        return AxolotlValidationResponse(
            is_valid=False,
            summary_message=f"Validation Error: {str(exc)}",
            estimated_vram_gb=0.0
        )

    # Estimate VRAM usage based on sequence length and adapter
    base_vram = 16.0 if "70b" in validated_config.base_model.lower() else 8.0
    if validated_config.sequence_len > 8192:
        base_vram *= 1.8
    if validated_config.adapter == "full":
        base_vram *= 3.5

    return AxolotlValidationResponse(
        is_valid=True,
        summary_message=f"Configuration valid for base model '{validated_config.base_model}' with adapter '{validated_config.adapter}'.",
        estimated_vram_gb=round(base_vram, 1)
    )


if __name__ == "__main__":
    mcp.run()
```

### 2. Standalone Axolotl Config Parser Script with Pydantic v2

```python
import yaml
from pydantic import BaseModel, Field, ConfigDict

class YAMLConfigWrapper(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    base_model: str = Field(...)
    sequence_len: int = Field(..., ge=1024)
    sample_packing: bool = Field(True)

def verify_and_print_config(yaml_text: str):
    parsed = yaml.safe_load(yaml_text)
    cfg = YAMLConfigWrapper(**parsed)
    print(f"Verified Axolotl Run -> Model: {cfg.base_model} | Seq Len: {cfg.sequence_len}")

if __name__ == "__main__":
    sample_yaml = """
    base_model: "Qwen/Qwen2.5-7B-Instruct"
    sequence_len: 8192
    sample_packing: true
    """
    verify_and_print_config(sample_yaml)
```

## Related tools / concepts
- [Unsloth](../../tools/infrastructure/unsloth.md) — Fast single-GPU fine-tuning engine alternative.
- [LLaMA Factory](llama-factory.md) — Web-UI driven fine-tuning suite.
- [distilabel](distilabel.md) — Synthetic dataset creation framework upstream of Axolotl.
- [vLLM](../../tools/infrastructure/vllm.md) — High-throughput inference backend for serving fine-tuned weights.
- [DeepSpeed](https://github.com/microsoft/DeepSpeed) — Distributed training framework integrated into Axolotl.
- [FastMCP](../automation_orchestration/mcp.md) — Tool execution framework for training tool-calling agent models.

## Sources / references
- [Axolotl Official GitHub Repository](https://github.com/axolotl-ai-cloud/axolotl)
- [Axolotl Documentation Portal](https://axolotl-ai-cloud.github.io/axolotl/)
- [Hugging Face TRL & PEFT Libraries](https://huggingface.co/docs/trl)
- [FastMCP 3.1 Task Protocol Specification](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
