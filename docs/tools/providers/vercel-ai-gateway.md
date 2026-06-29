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
Install the Vercel CLI to manage AI Gateway resources:
```bash
npm install -g vercel
```

### 2. Quick Setup
Create a new AI Gateway and get your Gateway ID:
```bash
vercel ai-gateway create --name my-gateway
```

### Minimal Concepts
1.  **Gateway ID**: A unique identifier for your specific gateway configuration.
2.  **Provider Mapping**: Configuring which API keys map to which upstream providers.

### Python Example (OpenAI SDK)
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

print(completion.choices[0].message.content)
```

### cURL Example (Direct API)
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

## CLI examples
The Vercel CLI allows managing AI Gateway resources directly from the terminal.

```bash
# List all AI Gateways for the current team
vercel ai-gateway list

# Create a new AI Gateway API key with a budget
vercel ai-gateway api-keys create --name "Production Key" --budget 500 --refresh-period monthly

# Add a routing rule to rewrite models (e.g., fallback/upgrade)
vercel ai-gateway rules add --type rewrite \
  --source "openai/gpt-4" \
  --destination "openai/gpt-4o"
```

## API examples
Vercel AI Gateway supports universal model routing and provider-specific headers via its REST interface.

### Model Routing with Fallback (Python)
```python
import requests
import os

gateway_url = f"https://gateway.ai.vercel.com/v1/gateways/{os.environ['VERCEL_GATEWAY_ID']}/openai"

payload = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "What is the capital of France?"}],
    "gateway": {
        "cache": True,
        "retry": {"count": 3}
    }
}

headers = {
    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    "Content-Type": "application/json"
}

response = requests.post(f"{gateway_url}/chat/completions", json=payload, headers=headers)
print(response.json()['choices'][0]['message']['content'])
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
