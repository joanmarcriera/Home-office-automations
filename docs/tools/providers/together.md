# Together AI

## What it is
Together AI is a cloud platform for building and running generative AI, offering high-performance inference for a wide range of open-source models (Llama 3, Qwen, Mistral, Gemma).

## What problem it solves
Simplifies the deployment of open-source models by providing a fast, serverless API, eliminating the need to manage complex GPU infrastructure for models.

## Where it fits in the stack
**Inference Provider**. It acts as the backend for applications using open-weights models.

## Typical use cases
- **Multi-Model Testing**: Quickly switching between different open models to find the best fit for a specific task.
- **Cost Optimization**: Using Together's efficient inference to lower API costs compared to proprietary flagship models.
- **Fine-Tuning**: Training and deploying custom LoRA adapters of open models on proprietary data.

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
    model="meta-llama/Llama-3-70b-chat-hf",
    messages=[{"role": "user", "content": "What are the benefits of open source AI?"}],
)
print(response.choices[0].message.content)
```

## Strengths
- **Model Variety**: Supports hundreds of open-source models across text, image, and code (LLMs, Diffusion, etc.).
- **Speed**: One of the fastest inference providers on the market due to specialized optimizations.
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
- If you require the specific proprietary reasoning capabilities of models like Claude 3.5 Sonnet or GPT-4o.
- If you have strict regulatory requirements to keep all data on your own local hardware.

## Licensing and cost
- **Open Source**: The platform is proprietary; the models it hosts are mostly open-weights (Llama, Mistral, etc.).
- **Cost**: Paid (Usage-based).
- **Self-hostable**: No (Cloud service), but the models can be hosted elsewhere if needed.

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Groq](groq.md)
- [Fireworks AI](fireworks.md)

## Sources / References
- [Official Website](https://www.together.ai/)
- [Together AI Docs](https://docs.together.ai/)
- [Together AI Models](https://www.together.ai/models)

## Contribution Metadata
- Last reviewed: 2026-03-03
- Confidence: high
