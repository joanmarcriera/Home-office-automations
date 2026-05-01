# Portkey AI Gateway

## What it is
Portkey AI Gateway is an open-source, high-performance gateway and control plane designed to route and manage requests to 1,600+ Large Language Models (LLMs). It provides enterprise-grade features like observability, guardrails, and cost management through a single, unified API.

## What problem it solves
It solves the complexity of managing multiple LLM providers and models in production. By acting as a central proxy, it provides reliability (via fallbacks and retries), efficiency (via caching), and security (via guardrails), while giving developers a single interface to manage all their AI interactions.

## Where it fits in the stack
**Category**: Providers / AI Gateway

## Typical use cases
- **Multi-Model Routing**: Routing requests to different models (e.g., GPT-4, Claude 3, Llama 3) based on performance, cost, or availability.
- **Production Observability**: Tracking latency, token usage, and costs across all LLM providers in real-time.
- **Reliability Engineering**: Implementing automatic retries, fallbacks to backup providers, and circuit breakers for unstable LLM APIs.
- **Enterprise Guardrails**: Enforcing safety, privacy, and compliance checks on prompts and LLM responses.

## Strengths
- **Unified API**: Connect to 200+ providers with a single, OpenAI-compatible endpoint.
- **Open Source**: The core gateway is open-source and can be run locally or self-hosted.
- **Blazing Fast**: Designed for low latency (negligible overhead).
- **Comprehensive Features**: Built-in caching, load balancing, canary testing, and budget limits.
- **Prompt Management**: Centralized management and versioning of prompts.

## Limitations
- **Proxy Dependency**: Adds a network hop (though minimal latency).
- **Configuration Overhead**: Setting up complex routing and guardrail policies requires initial configuration.

## Getting started

### Run Locally (One Command)
```bash
npx @portkey-ai/gateway
```

### Basic Usage (OpenAI SDK)
```python
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

client = OpenAI(
    api_key="YOUR_OPENAI_KEY",
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider="openai",
        api_key="YOUR_PORTKEY_API_KEY" # Optional for open source
    )
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello via Portkey!"}]
)
```

## Related tools / concepts
- [Vercel AI Gateway](vercel-ai-gateway.md)
- [LiteLLM](../../services/litellm.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [AI Auditing Tools](../process_understanding/ai-auditing-tools.md)

## Sources / references
- [Official Website](https://portkey.ai/)
- [Portkey Docs](https://docs.portkey.ai/docs/product/ai-gateway)
- [GitHub Repository](https://github.com/Portkey-AI/gateway)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
