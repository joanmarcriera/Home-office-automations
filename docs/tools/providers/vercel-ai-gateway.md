# Vercel AI Gateway

## What it is
Vercel AI Gateway is a lightweight, edge-compatible provider proxy that allows developers to manage, optimize, and observe their AI applications. It sits between your application code and multiple AI providers (OpenAI, Anthropic, Replicate, etc.).

## What problem it solves
It simplifies the operational overhead of running LLM-powered apps by providing built-in caching, rate limiting, and request retries. It also offers a unified dashboard for observing latency, cost, and usage across different models and providers.

## Where it fits in the stack
**Orchestration / Observability Layer**. It acts as a middleware gateway between the application logic and the model providers, typically used in Vercel-hosted environments or via standard HTTP clients.

## Typical use cases
- **Cost Management**: Using caching to avoid redundant LLM calls.
- **Resilience**: Implementing automated model fallbacks (e.g., if OpenAI is down, use Anthropic).
- **Observability**: Tracking token usage and performance metrics in a centralized dashboard.
- **Developer API Control**: Providing a single, consistent API endpoint for internal teams to consume multiple LLM providers.

## Strengths
- **Simplicity**: Extremely easy to set up for existing Vercel users.
- **Unified Interface**: Use one base URL pattern for multiple providers.
- **Edge Intelligence**: Caching at the edge provides significant speedups for common queries.
- **OpenAI Compatibility**: Supports the OpenAI SDK format for most upstream providers.

## Limitations
- **Vercel Ecosystem**: While it can be used standalone, it is most powerful when integrated with Vercel's deployment platform.
- **Overhead**: Adds another network hop, though usually mitigated by edge execution.
- **Vendor Lock-in**: Relying on a proprietary gateway for mission-critical routing.

## When to use it
- When deploying AI apps on Vercel and wanting immediate observability and caching.
- When you need a quick way to implement multi-provider fallbacks without complex orchestration code.
- To reduce API costs for repetitive prompts in production.

## When not to use it
- If you require a fully self-hosted, open-source gateway (see [LiteLLM](../../services/litellm.md)).
- If your application requires extremely low-latency local inference where a cloud gateway would be a bottleneck.
- If you are already using a more comprehensive AI orchestration platform like LangSmith or Helicone.

## Getting started

### 1. Installation
Install the Vercel CLI to manage your gateway resources:
```bash
npm install -g vercel
```

### 2. Create a Gateway
Create a new gateway via the [Vercel Dashboard](https://vercel.com/dashboard/ai) or CLI. Note your **Gateway ID**.

### Hello World Example
Test your gateway by listing available models through the proxy:
```bash
curl https://ai-gateway.vercel.sh/v1/models
```

## CLI examples
```bash
# List all AI Gateways for your team
vercel ai-gateway list

# Create a new AI Gateway resource
vercel ai-gateway create --name my-prod-gateway

# Manage API keys for a specific gateway
vercel ai-gateway keys list my-prod-gateway
```

## API examples

### Python (OpenAI SDK Mapping)
Route OpenAI requests through the gateway for caching and observability:
```python
from openai import OpenAI
import os

client = OpenAI(
    # Use the Vercel AI Gateway URL as the base
    base_url=f"https://gateway.ai.vercel.com/v1/gateways/{os.environ['VERCEL_GATEWAY_ID']}/openai",
    api_key=os.environ["OPENAI_API_KEY"],
)

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "How do I implement a fallback in Vercel AI Gateway?"}]
)
```

### TypeScript (REST API for Discovery)
Discover available models and their provider endpoints dynamically:
```typescript
const response = await fetch('https://ai-gateway.vercel.sh/v1/models', {
  headers: {
    'Authorization': `Bearer ${process.env.VERCEL_AI_GATEWAY_KEY}`
  }
});
const { data: models } = await response.json();
console.log(models.map(m => m.id));
```

### cURL (Direct Anthropic Proxy)
```bash
curl https://gateway.ai.vercel.com/v1/gateways/YOUR_GATEWAY_ID/anthropic/v1/messages \
  -H "X-API-Key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-3-5-sonnet-20240620",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }'
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md)
- [LiteLLM](../../services/litellm.md)
- [Helicone](../process_understanding/helicone.md)
- [Portkey](portkey.md)
- [Promptfoo](../benchmarking/promptfoo.md)
- [Langfuse](../process_understanding/langfuse.md)
- [AgentOps](../process_understanding/agentops.md)

## Sources / references
- [Vercel AI Gateway Documentation](https://vercel.com/docs/ai/ai-gateway)
- [Vercel Blog: Introducing AI Gateway](https://vercel.com/blog/introducing-ai-gateway)

## Contribution Metadata
- Last reviewed: 2026-07-01
- Confidence: high
