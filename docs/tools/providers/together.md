# Together AI

## What it is
Together AI is a cloud platform for building and running generative AI, offering high-performance inference for a wide range of open-source models.

## What problem it solves
Simplifies the deployment of open-source models by providing a fast, serverless API, eliminating the need to manage infrastructure for models like Llama, Qwen, and Mistral.

## Where it fits in the stack
**Inference Provider**. It acts as the backend for applications using open-weights models.

## Typical use cases
- **Multi-Model Testing**: Quickly switching between different open models to find the best fit.
- **Cost Optimization**: Using Together's efficient inference to lower API costs compared to proprietary providers.
- **Fine-Tuning**: Training custom versions of open models on proprietary data.

## Getting started
Install the SDK:
```bash
pip install together
```

Basic API call:
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
- **Model Variety**: Supports hundreds of open-source models across text, image, and code.
- **Speed**: One of the fastest inference providers on the market.
- **Features**: Offers serverless API, dedicated clusters, and fine-tuning.
- **Pricing Tiers**: Offers aggressive **Serverless** pricing (usage-based, very low cost) and **Dedicated Clusters** for predictable performance at scale.

## Limitations
- **Third-Party Dependency**: You are relying on their platform for uptime and security of the open models.
- **Complexity**: Navigating hundreds of models can be overwhelming compared to providers with a few flagship models.

## When to use it
- When you want to use open-source models without the hassle of self-hosting.
- When low latency and high throughput are critical.
- For scaling applications that require fine-tuned open models.

## When not to use it
- If you require the specific reasoning capabilities of proprietary models like Claude 3.5 Sonnet or GPT-4o.
- If you have strict requirements to keep all data within your own on-premise hardware.

## Licensing and cost
- **Open Source**: The platform is proprietary; the models it hosts are mostly open-weights.
- **Cost**: Paid (Usage-based).
- **Self-hostable**: No (Cloud service), but the models can be hosted elsewhere.

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Groq](groq.md)
- [Fireworks AI](fireworks.md)

## Sources / References
- [Official Website](https://www.together.ai/)
- [Together AI Docs](https://docs.together.ai/)
- [Together AI Models](https://www.together.ai/models)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
