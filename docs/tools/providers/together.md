# Together AI

## What it is
Together AI is a enterprise-grade cloud inference and fine-tuning platform for open-source foundation models. As of early January 2027, it provides high-throughput, low-latency API access to the full Llama 4 family, DeepSeek-V4, Qwen 3.6, Gemma 3, and domain-specialized code/math models, all powered by NVIDIA Rubin GPU architecture and proprietary FlashAttention-3 execution kernels.

## What problem it solves
It eliminates the heavy infrastructure overhead of self-hosting open-weights foundation models while preserving data sovereignty and customization control. Together AI offers an open-model alternative to proprietary flagship APIs like Claude 5.1, GPT-5.6, and Gemini 4.0 Ultra, enabling developers to serve customized LoRA adapters and high-frequency agentic tool calls at scale.

## Where it fits in the stack
**Category**: Providers / Model Serving & Fine-Tuning. It functions as an inference backend and custom model adapter registry, connecting agent frameworks (such as [LangGraph](../frameworks/langgraph.md) or [CrewAI](../frameworks/crewai.md)) and FastMCP 3.1 tool servers to high-performance open-weights LLMs and multi-modal models.

## Typical use cases
- **Multi-Model Inference Routing**: Programmatically switching between open models (e.g., Llama 4 70B, DeepSeek-V4) based on cost, latency, and context depth requirements.
- **Custom LoRA Adapter Serving**: Fine-tuning open models on private datasets and serving hot-swappable LoRA adapters with zero cold-start penalty.
- **High-Throughput FastMCP Agent Workflows**: Serving low-latency agent reasoning pipelines that communicate with FastMCP 3.1 tools.
- **Dedicated Cluster Provisioning**: Hosting private, isolated GPU compute clusters for regulated enterprise production environments.

## Strengths
- **Massive Model Catalog**: Broad support for open LLMs, vision-language models, image/video generation models, and embedding models.
- **Extreme Speed and Optimization**: Optimized inference pipeline utilizing FlashAttention-3, Liger Kernels, and FP8/FP4 quantization on NVIDIA Rubin hardware.
- **Serverless & Dedicated Options**: Offers cost-effective pay-per-token serverless endpoints as well as reserved GPU clusters with guaranteed SLA.
- **Native Fine-Tuning Workflows**: Integrated dataset ingestion, LoRA/full fine-tuning, and instant adapter endpoint deployment.

## Limitations
- **Third-Party Service Dependence**: Relies on Together's infrastructure availability, platform rate limits, and service level agreements.
- **Model Catalog Overhead**: Navigating hundreds of fine-tuned variants requires automated model benchmark evaluation.

## When to use it
- When you require production-grade API access to open-weights models (Llama 4, DeepSeek-V4) with enterprise latency guarantees.
- For cost-optimized agentic workloads that require serving hundreds of custom LoRA adapters on demand.
- When building FastMCP 3.1 tool-calling pipelines that benefit from low-latency serverless model endpoints.

## When not to use it
- If your system requires strict air-gapped, on-premises execution without external API connectivity (use [vLLM](../infrastructure/vllm.md) or [Ollama](../../services/ollama.md)).
- If you rely exclusively on proprietary closed-source reasoning endpoints like Claude 5.1 Opus or GPT-5.6.

## Getting started

### Installation
Install the official Together Python client SDK:

```bash
pip install together pydantic
```

### Basic Chat Completion Example

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

response = client.chat.completions.create(
    model="meta-llama/Llama-4-70b-instruct",
    messages=[
        {"role": "system", "content": "You are a senior systems architect specializing in FastMCP 3.1 tool integration."},
        {"role": "user", "content": "Explain how LoRA adapters improve inference efficiency for agent swarms."}
    ],
    temperature=0.2,
    max_tokens=1024,
)

print(response.choices[0].message.content)
```

## CLI examples

```bash
# List all active serverless models in Together AI catalog
together models list

# Stream a completion directly from the command line using Llama 4
together chat "meta-llama/Llama-4-70b-instruct" --prompt "Draft a FastMCP 3.1 tool schema in Python."

# Initiate a LoRA fine-tuning job on a dataset
together fine-tuning create \
  --training-file "s3://my-bucket/training_data.jsonl" \
  --model "meta-llama/Llama-4-8b" \
  --n-epochs 3 \
  --learning-rate 1e-4

# Check status of an active fine-tuning job
together fine-tuning retrieve "ft-job-20270107-001"
```

## API examples

### Fine-Tuning and Hot-Swappable Adapter Endpoint Invocation

```python
import os
from together import Together

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

# Query fine-tuned model adapter endpoint
response = client.chat.completions.create(
    model="accounts/enterprise-org/models/llama-4-8b-fastmcp-adapter",
    messages=[
        {"role": "user", "content": "Generate a Pydantic v2 validation schema for an automated audit log."}
    ],
    temperature=0.1
)

print(response.choices[0].message.content)
```

### Programmatic Fine-Tuning Payload Validation using Pydantic v2
This Python script validates fine-tuning job configurations and hyperparameters prior to submitting to the Together AI API using **Pydantic v2**:

```python
import json
from typing import Dict, Optional, Literal
from pydantic import BaseModel, Field, ValidationError

class TogetherFineTuneJob(BaseModel):
    training_file: str = Field(..., description="URI or ID of the JSONL training dataset")
    model: str = Field(..., description="Base model name, e.g., meta-llama/Llama-4-8b")
    n_epochs: int = Field(default=3, ge=1, le=20, description="Total number of training epochs")
    batch_size: int = Field(default=8, ge=1, description="Training batch size")
    learning_rate: float = Field(default=1e-4, gt=0, description="Learning rate for gradient updates")
    lora_r: int = Field(default=16, ge=4, le=128, description="LoRA rank dimension")
    lora_alpha: int = Field(default=32, ge=8, le=256, description="LoRA scaling factor")
    suffix: Optional[str] = Field(None, description="Custom adapter name suffix")

def validate_finetuning_payload(raw_json: str) -> Optional[TogetherFineTuneJob]:
    try:
        data = json.loads(raw_json)
        job = TogetherFineTuneJob.model_validate(data)
        print(f"Validated Fine-Tuning Job for base model: {job.model}")
        return job
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON input format.")
        return None

# Execution Example
if __name__ == "__main__":
    payload = json.dumps({
        "training_file": "file-2027-01-07-dataset-01",
        "model": "meta-llama/Llama-4-8b",
        "n_epochs": 5,
        "batch_size": 16,
        "learning_rate": 0.0002,
        "lora_r": 32,
        "lora_alpha": 64,
        "suffix": "sota-agent-v1"
    })
    validate_finetuning_payload(payload)
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) — Multi-model API gateway routing across commercial and open providers.
- [Groq](groq.md) — Ultra-low latency LPU inference provider.
- [Fireworks AI](fireworks.md) — Speed-optimized model hosting and fine-tuning engine.
- [Mistral AI](mistral.md) — Leading European open weights provider.
- [vLLM](../infrastructure/vllm.md) — High-throughput self-hosted inference serving engine.
- [TGI](../infrastructure/tgi.md) — Hugging Face Text Generation Inference.
- [Hugging Face](huggingface.md) — Open source model repository and community hub.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open standard for agent tool integration.

## Sources / references
- [Together AI Official Website](https://www.together.ai/)
- [Together AI Documentation](https://docs.together.ai/)
- [Together AI Model Catalog](https://www.together.ai/models)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
