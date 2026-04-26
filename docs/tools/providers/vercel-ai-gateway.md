# Vercel AI Gateway

## What it is
Vercel AI Gateway is a lightweight, edge-compatible provider proxy that allows developers to manage, optimize, and observe their AI applications. It sits between your application code and multiple AI providers (OpenAI, Anthropic, Replicate, etc.).

## What problem it solves
It simplifies the operational overhead of running LLM-powered apps by providing built-in caching, rate limiting, and request retries. It also offers a unified dashboard for observing latency, cost, and usage across different models and providers.

## Where it fits in the stack
**Orchestration / Observability Layer**. It acts as a middleware gateway between the application logic and the model providers.

## Key Features
- **Caching**: Edge-based caching of repeated requests to reduce cost and latency.
- **Retries & Fallbacks**: Automatic retry logic on 429s or 5xx errors; fallback to alternative models if a provider is down.
- **Streaming Support**: Native support for LLM response streaming.
- **Edge Deployment**: Runs on Vercel's global edge network for minimal latency.

## Typical use cases
- **Cost Management**: Using caching to avoid redundant LLM calls.
- **Resilience**: Implementing automated model fallbacks (e.g., if OpenAI is down, use Anthropic).
- **Observability**: Tracking token usage and performance metrics in a centralized dashboard.

## Getting started

### Minimal Concepts
1.  **Gateway ID**: A unique identifier for your specific gateway configuration.
2.  **Provider Mapping**: Configuring which API keys map to which upstream providers.

### Python Example
```python
from openai import OpenAI

client = OpenAI(
    # Use the Vercel AI Gateway URL as the base
    base_url="https://gateway.ai.vercel.com/v1/gateways/YOUR_GATEWAY_ID/openai",
    api_key="OPENAI_API_KEY",
)

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "Explain quantum physics to a five year old"}]
)

print(completion.choices[0].message.content)
```

## Strengths
- **Simplicity**: Extremely easy to set up for existing Vercel users.
- **Unified Interface**: Use one base URL pattern for multiple providers.
- **Edge Intelligence**: Caching at the edge provides significant speedups for common queries.

## Limitations
- **Vercel Ecosystem**: While it can be used standalone, it is most powerful when integrated with Vercel's deployment platform.
- **Overhead**: Adds another network hop, though usually mitigated by edge execution.

## Related tools / concepts
- [OpenRouter](openrouter.md) (Alternative model aggregator)
- [LiteLLM](../../services/litellm.md) (Self-hosted gateway alternative)

## Sources / References
- [Vercel AI Gateway Documentation](https://vercel.com/docs/ai/ai-gateway)
- [Vercel Blog: Introducing AI Gateway](https://vercel.com/blog/introducing-ai-gateway)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
