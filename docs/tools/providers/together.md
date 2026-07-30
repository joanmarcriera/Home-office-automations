# Together AI

## What it is
Together AI is a cloud platform for building and running generative AI, offering high-performance inference for a wide range of open-source models. As of late October / November 2026, it supports the full Llama 4 family, Gemma 3, Qwen 3.6, and specialized coding models, all running on the latest NVIDIA Rubin architecture.

## What problem it solves
Simplifies the deployment of open-source models by providing a fast, serverless API, eliminating the need to manage complex GPU infrastructure for models. It provides a performance-optimized alternative to cloud giants, often compared to Claude 5.1 and GPT-5.5 for specific vertical tasks and high-throughput agentic workflows.

## Where it fits in the stack
**Inference Provider**. It acts as the backend for applications using open-weights models and custom fine-tuned adapters.

## Typical use cases
- **Multi-Model Testing**: Quickly switching between different open models to find the best fit for a specific task.
- **Cost Optimization**: Using Together's efficient inference to lower API costs compared to proprietary flagship models.
- **Fine-Tuning**: Training and deploying custom LoRA adapters of open models on proprietary data.
- **Agentic Orchestration**: Serving as a reliable backend for agents using MCP 3.1 for tool-integrated reasoning.

## Strengths
- **Model Variety**: Supports hundreds of open-source models across text, image, and code (LLMs, Diffusion, etc.).
- **Speed**: One of the fastest inference providers on the market due to specialized FlashAttention-3 and Liger Kernel optimizations.
- **Features**: Offers serverless API, dedicated clusters, and integrated fine-tuning workflows.
- **Pricing Tiers**: Offers aggressive **Serverless** pricing (usage-based, very low cost) and **Dedicated Clusters** for predictable performance and high throughput.

## Limitations
- **Third-Party Dependency**: Relying on their platform for uptime and security of the hosted open models.
- **Complexity**: Navigating the massive library of models can be overwhelming for beginners.

## When to use it
- When you want to use top-tier open-source models without the hassle of self-hosting.
- When low latency and high throughput are critical for your application.
- For scaling applications that require fine-tuned open models with custom LoRA adapters.

## When not to use it
- If you require the specific proprietary reasoning capabilities of models like Claude 5.1 or GPT-5.5.
- If you have strict regulatory requirements to keep all data on your own local hardware.

## Getting started
Install the SDK:
```bash
pip install together
```

Basic API call (Python):
```python
from together import Together

client = Together()

response = client.chat.completions.create(
    model="meta-llama/Llama-4-70b-chat-hf",
    messages=[{"role": "user", "content": "Benefits of open source AI?"}],
)
print(response.choices[0].message.content)
```

## CLI examples
```bash
# List all available models
together models list

# Query a model directly via CLI
together chat "meta-llama/Llama-4-70b-chat-hf" --prompt "Hello"

# Start a fine-tuning job
together fine-tuning create --training-file "data.jsonl" --model "llama-4-8b"
```

## API examples

### Fine-Tuning and LoRA Deployment
Together AI provides a unified API for fine-tuning open models and deploying them as custom adapters.

```python
from together import Together

client = Together()

# List available fine-tuned models
fine_tuned_models = client.fine_tuning.list()

# Inference with a custom adapter
response = client.chat.completions.create(
    model="accounts/your-account/models/your-finetuned-llama-4",
    messages=[{"role": "user", "content": "How should I summarize this report?"}],
)
print(response.choices[0].message.content)
```

### Dedicated GPU Cluster Usage
For high-volume production, Together allows provisioning dedicated GPU clusters for guaranteed throughput.

```python
# Usage involves pointing your client to the dedicated model endpoint
response = client.chat.completions.create(
    model="meta-llama/Llama-4-70b-chat-hf",
    extra_body={"dedicated_cluster": "cluster-id-123"},
    messages=[{"role": "user", "content": "Batch process these items."}],
)
```

### Programmatic Fine-Tuning Validation using Pydantic v2
This Python script validates Together AI fine-tuning job payload configurations and job parameters prior to submission using **Pydantic v2**:

```python
import json
from typing import Optional, Dict
from pydantic import BaseModel, Field, ValidationError

class TogetherFineTuneJob(BaseModel):
    training_file: str = Field(..., description="Path or HF ID of the .jsonl training file")
    model: str = Field(..., description="The base open weights model to fine-tune (e.g., Llama-4-8b)")
    n_epochs: int = Field(default=3, ge=1, le=10, description="Number of training iterations")
    batch_size: int = Field(default=4, ge=1, description="Size of training batch")
    learning_rate: float = Field(default=1e-5, gt=0, description="Step size for training gradient updates")
    hyperparameters: Optional[Dict[str, float]] = Field(None, description="Optional LoRA configuration dictionary")

def validate_finetuning_payload(raw_json: str) -> Optional[TogetherFineTuneJob]:
    try:
        data = json.loads(raw_json)
        # Validate result object with Pydantic v2 model_validate
        job = TogetherFineTuneJob.model_validate(data)
        return job
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) — Multi-model API gateway.
- [Groq](groq.md) — Ultra-low latency inference engine.
- [Fireworks AI](fireworks.md) — Speed-optimized model hosting provider.
- [Mistral AI](mistral.md) — Leading European open weights provider.
- [vLLM](../infrastructure/vllm.md) — Self-hosted serving layer.
- [TGI](../infrastructure/tgi.md) — Text Generation Inference framework.
- [Hugging Face](huggingface.md) — Open source repository and community.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Open standard for agent tool use.

## Sources / references
- [Official Website](https://www.together.ai/)
- [Together AI Docs](https://docs.together.ai/)
- [Together AI Models](https://www.together.ai/models)

## Contribution Metadata
- Last reviewed: 2026-11-04
- Confidence: high
