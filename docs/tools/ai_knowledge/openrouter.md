# OpenRouter

## What it is
OpenRouter is a unified interface and "meta-provider" for Large Language Models (LLMs). It provides a single, OpenAI-compatible API to access a vast array of models from providers like OpenAI, Anthropic, Google, Meta, DeepSeek, and Mistral. As of July 2026, OpenRouter has expanded to support **MCP 3.0/3.1 routing**, native reasoning/thinking tokens streaming, and automated model distillation pipelines.

## What problem it solves
It eliminates the complexity of managing multiple API keys, client libraries, and billing accounts for different AI providers. It also solves regional access issues and provides a "safety net" via automatic fallbacks, ensuring that agentic workflows remain operational even if a specific provider or model experiences downtime.

## Where it fits in the stack
**Provider / Routing Layer**. It sits between the Agent/Application layer and the actual LLM infrastructure providers, acting as a gateway, load balancer, and intelligence router.

## Typical use cases
- **Multi-Model Agent Workflows**: Dynamically switching between models (e.g., using Gemini for large context analysis, DeepSeek or Claude for precise code generation) via one endpoint.
- **Unified Billing for Teams**: Consolidating AI spend across dozens of model families into a single prepay account.
- **Accessing Open-Weights Models**: Using Gemma 3, Llama 4, Qwen 3.6, or Mistral models without the overhead of self-hosting or managing niche providers.
- **Automated Fallbacks**: Ensuring 99.9% uptime for AI features by falling back from primary models (e.g., GPT-5.5) to alternates if rate limits are hit.

## Strengths
- **Massive Model Selection**: Access to 200+ model variants with a single API key.
- **Competitive Pricing**: Automatically routes to the cheapest available provider for open models.
- **Standardized API**: Uses the familiar OpenAI chat completions format, making integration trivial.
- **Advanced Features**: Supports tool calling, prompt caching, and "thinking/reasoning" tags across diverse model families.
- **MCP 3.0/3.1 Support**: Native integration with the Model Context Protocol for seamless tool and resource sharing across client sessions.
- **No-Trace Mode**: Optional privacy configurations that prevent third-party providers from caching or training on data.

## Limitations
- **Proxy Latency**: Adds a minor (usually negligible) overhead compared to direct provider access.
- **Privacy Trade-off**: Adds OpenRouter as an intermediary in the data flow, which may require legal review in highly regulated industries.
- **Centralized Dependency**: If OpenRouter's gateway is down, access to all proxied models is lost.

## When to use it
- During development and prototyping to rapidly test and compare different models.
- For hobbyist and homelab projects that benefit from simple, unified billing.
- In production environments where multi-provider redundancy, thinking tokens streaming, and cost optimization are high priorities.

## When not to use it
- For ultra-low latency applications where every millisecond counts.
- When your organization has direct, high-volume enterprise discounts with a specific provider (e.g., Microsoft Azure).
- If your data sovereignty requirements prohibit the use of third-party proxy services.

## Getting started

### 1. API Key Setup
1. Create an account at [openrouter.ai](https://openrouter.ai/).
2. Navigate to Settings -> Keys and generate a new key.
3. Top up your account with credits (OpenRouter uses a prepay model).

### 2. Basic Configuration
OpenRouter is a drop-in replacement for the OpenAI API.

```bash
export OPENROUTER_API_KEY="your_key_here"
```

## CLI examples

### Testing Models via cURL
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "google/gemma-3-27b-it",
    "messages": [{"role": "user", "content": "What is OpenRouter?"}]
  }'
```

### Checking Model Availability
Use the models endpoint to see current pricing and provider status:
```bash
curl https://openrouter.ai/api/v1/models | jq '.data[] | {id, pricing}'
```

## API examples

### Python (OpenAI Library)
```python
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="your-api-key",
)

completion = client.chat.completions.create(
  model="anthropic/claude-5.1-sonnet",
  messages=[{"role": "user", "content": "Explain quantum entanglement."}],
  extra_headers={
    "HTTP-Referer": "https://your-app.com", # Optional, for OpenRouter rankings
    "X-Title": "My Agentic App",
  }
)
print(completion.choices[0].message.content)
```

### Advanced Routing: Model Fallbacks
Specify a comma-separated list of models. OpenRouter will try them in order.

```python
completion = client.chat.completions.create(
  model="openai/gpt-5.5,anthropic/claude-5.1-opus,google/gemini-3.5-pro",
  messages=[{"role": "user", "content": "Perform a complex audit."}]
)
```

## Related tools / concepts
- [LiteLLM](../../services/litellm.md) — Local proxy for multi-model routing.
- [OpenAI](openai.md) — Foundation API standard.
- [Anthropic](../providers/anthropic.md) — Primary frontier model provider.
- [DeepSeek](../providers/deepseek.md) — High-performance open models provider.
- [Groq](../providers/groq.md) — Low-latency open model execution engine.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Architectural patterns for smart selection.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Industry-standard tool registration.
- [Google Gemini](google-gemini.md) — Multimodal and long-context model family.

## Sources / references
- [OpenRouter Official Developer Documentation](https://openrouter.ai/docs)
- [OpenRouter API Reference and Model List](https://openrouter.ai/api/v1/models)
- [OpenRouter Rankings & Benchmarks Tracker](https://openrouter.ai/rankings)
- [Model Context Protocol (MCP) Integration on OpenRouter](https://openrouter.ai/docs#mcp)
- [OpenRouter Blog and Release Logs](https://openrouter.ai/blog)
- [Community Integration Guide](../../knowledge_base/patterns/prompt_requests.md)
- [Unified Billing Architecture and Enterprise Credits](https://openrouter.ai/docs#billing)
- [Antling-30B-Flash on OpenRouter](https://www.reddit.com/r/LocalLLaMA/comments/1v4m5cr/antling30flash_is_now_live_on_openrouter_and_free/) — Antling-30B-Flash live on OpenRouter for free testing.

## Contribution Metadata
- Last reviewed: 2026-10-01
- Confidence: high
