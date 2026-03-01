# Fireworks AI

## What it is
Fireworks AI is an inference platform providing a high-performance API for running and fine-tuning open-source generative AI models.

## What problem it solves
Provides ultra-fast, reliable, and cost-effective access to the latest open-source models with optimizations that exceed standard GPU deployments.

## Where it fits in the stack
**Inference Provider**. Similar to Together AI and Groq, it provides the backend for LLM-powered applications.

## Typical use cases
- **High-Throughput Applications**: Apps requiring many concurrent LLM requests.
- **Function Calling**: Using their optimized models for structured data extraction.
- **Custom Model Deployment**: Deploying fine-tuned models on dedicated infrastructure.

## Getting started
Install the SDK:
```bash
pip install fireworks-ai
```

Basic API call:
```python
import fireworks.client

fireworks.client.api_key = "YOUR_API_KEY"

response = fireworks.client.ChatCompletion.create(
    model="accounts/fireworks/models/llama-v3-70b-instruct",
    messages=[
        {"role": "user", "content": "How do I optimize LLM inference?"}
    ]
)
print(response.choices[0].message.content)
```

## Strengths
- **Speed**: Optimized inference engine (FireAttention) provides high tokens per second.
- **Developer Experience**: OpenAI-compatible API makes migration simple.
- **Fine-tuning**: Excellent support for LoRA fine-tuning and deployment.
- **Pricing Tiers**: Features highly competitive **Serverless** usage-based pricing and **On-Demand/Reserved** capacity for large-scale production needs.

## Limitations
- **Model Variety**: While broad, they focus on a curated set of high-performance models rather than everything available.
- **Brand Awareness**: Less known than Together or Groq in the enthusiast space.

## When to use it
- When you need high-speed inference for Llama 3 or other top open models.
- For production applications requiring high reliability and uptime.
- When deploying custom LoRA adapters.

## When not to use it
- If you require proprietary "frontier" models.
- For extremely niche or obscure models not in their curated list.

## Licensing and cost
- **Open Source**: No (Proprietary platform).
- **Cost**: Paid (Usage-based).
- **Self-hostable**: No (Cloud service).

## Related tools / concepts
- [Together AI](together.md)
- [Groq](groq.md)
- [vLLM](../infrastructure/vllm.md)

## Sources / References
- [Official Website](https://fireworks.ai/)
- [Fireworks AI Docs](https://docs.fireworks.ai/)
- [Model Directory](https://fireworks.ai/models)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
