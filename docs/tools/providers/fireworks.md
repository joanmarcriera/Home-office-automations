# Fireworks AI

## What it is
Fireworks AI is a high-performance inference platform providing an ultra-fast API for running and fine-tuning open-source generative AI models (Llama, Mixtral, Qwen).

## What problem it solves
Provides reliable and cost-effective access to the latest open-source models with proprietary optimizations (FireAttention) that exceed standard GPU deployments.

## Where it fits in the stack
**Inference Provider**. Similar to Together AI and Groq, it provides the low-latency backend for LLM-powered applications.

## Typical use cases
- **High-Throughput Applications**: Production apps requiring many concurrent, low-latency LLM requests.
- **Function Calling**: Using their optimized models for reliable structured data extraction and tool use.
- **Custom Model Deployment**: Deploying specialized fine-tuned models on dedicated, scalable infrastructure.

## Getting started
Install the SDK:
```bash
pip install fireworks-ai
```

Basic API call (Python):
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
- **Speed**: Optimized inference engine (FireAttention) provides exceptionally high tokens per second.
- **Developer Experience**: OpenAI-compatible API makes migration from other providers seamless.
- **Fine-tuning**: Excellent support for LoRA fine-tuning and immediate deployment of adapters.
- **Pricing Tiers**: Features highly competitive **Serverless** usage-based pricing and **On-Demand/Reserved** capacity for large-scale enterprise production.

## Limitations
- **Model Variety**: While broad, they focus on a curated set of high-performance models rather than hosting every niche model.
- **Brand Awareness**: Less name recognition than Together or Groq in the broader enthusiast space.

## When to use it
- When you need high-speed, production-grade inference for Llama 3 or other top open models.
- For high-volume applications requiring high reliability and consistent performance.
- When deploying custom LoRA adapters with low overhead.

## When not to use it
- If you require proprietary "frontier" models like GPT-4o or Claude 3.5.
- For extremely niche or research models not included in their curated performance-optimized list.

## Licensing and cost
- **Open Source**: No (Proprietary optimization stack and platform).
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
- Last reviewed: 2026-03-03
- Confidence: high
