# Together AI

## What it is
Together AI is a cloud platform for building and running generative AI, offering high-performance inference for a wide range of open-source models. As of July 2026, it supports the full Llama 4 family, Gemma 3, Qwen 3.5, and specialized coding models, all running on the latest NVIDIA Rubin architecture.

## What problem it solves
Simplifies the deployment of open-source models by providing a fast, serverless API, eliminating the need to manage complex GPU infrastructure for models. It provides a performance-optimized alternative to cloud giants, often compared to `claude-4-8-opus-20260528` and GPT-5.5 for specific vertical tasks and high-throughput agentic workflows.

## Where it fits in the stack
**Inference Provider**. It acts as the backend for applications using open-weights models and custom fine-tuned adapters.

## Typical use cases
- **Multi-Model Testing**: Quickly switching between different open models to find the best fit for a specific task.
- **Cost Optimization**: Using Together's efficient inference to lower API costs compared to proprietary flagship models.
- **Fine-Tuning**: Training and deploying custom LoRA adapters of open models on proprietary data.
- **Agentic Orchestration**: Serving as a reliable backend for agents using MCP 3.0 for tool-integrated reasoning.

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
- If you require the specific proprietary reasoning capabilities of models like Claude 4.8 Opus or GPT-5.5.
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
    messages=[{"role": "user", "content": "Benefits of open source AI in July 2026?"}],
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

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Groq](groq.md)
- [Fireworks AI](fireworks.md)
- [Mistral](mistral.md)
- [vLLM](../infrastructure/vllm.md)
- [TGI](../infrastructure/tgi.md)
- [ExLlamaV2](../infrastructure/exllamav2.md)
- [Hugging Face](huggingface.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://www.together.ai/)
- [Together AI Docs](https://docs.together.ai/)
- [Together AI Models](https://www.together.ai/models)

## Contribution Metadata
- Last reviewed: 2026-07-01
- Confidence: high
