# Portkey AI Gateway

## What it is
Portkey AI Gateway is an open-source, high-performance gateway and control plane designed to route and manage requests to **1,600+ Large Language Models (LLMs)** across 200+ providers. It serves as a "Control Panel for Production AI," providing enterprise-grade observability, reliability, and governance through a single, unified API.

## What problem it solves
It solves the complexity of managing multiple LLM providers and models in production. By acting as a central proxy, it provides reliability (via fallbacks and retries), efficiency (via semantic caching), and security (via 50+ built-in guardrails), while giving developers a single interface to manage all their AI interactions.

## Where it fits in the stack
**Category**: Providers / AI Gateway. It sits at the **Infrastructure & Orchestration Layer**, serving as the gateway between agentic applications and model providers.

## Typical use cases
- **Multi-Model Orchestration**: Routing requests to different models (e.g., GPT-5.4, Claude 3.5, Llama 4) based on performance, cost, or reasoning depth.
- **Production Observability**: Real-time tracking of latency, token usage, and costs across all providers via a centralized dashboard.
- **Reliability Engineering**: Implementing automatic retries, provider-level fallbacks, load balancing, and circuit breakers to ensure zero-downtime AI features.
- **Enterprise Governance**: Enforcing PII redaction, budget limits, and RBAC on all LLM interactions.

## Strengths
- **Massive Model Support**: Connect to 1,600+ models with a single OpenAI-compatible SDK integration.
- **Unified API**: Standardized request/response formats across all providers (including Anthropic's native /messages).
- **Open Source**: The core gateway is open-source and can be run locally or self-hosted.
- **Blazing Fast**: Designed for low latency (negligible overhead).
- **Comprehensive Features**: Built-in caching, load balancing, canary testing, and budget limits.
- **Prompt Management**: Centralized management and versioning of prompts.

## Limitations
- **Proxy Dependency**: Adds a network hop (though minimal latency).
- **Configuration Overhead**: Setting up complex routing and guardrail policies requires initial configuration.

## When to use it
- When you need to manage multiple LLM providers (OpenAI, Anthropic, Google, etc.) through a single, OpenAI-compatible interface.
- To improve application reliability using automated fallbacks, retries, and load balancing across models.
- When production-grade observability (logging, cost tracking, latency monitoring) is required for AI features.
- If you need to implement prompt versioning and guardrails without modifying your application code for every change.

## When not to use it
- For very simple applications using a single model from a single provider where the extra features aren't needed.
- If your environment has extremely strict latency requirements where even a few milliseconds of proxy overhead is unacceptable.

## Getting started

### Run Locally (One Command)
```bash
npx @portkey-ai/gateway
```

### Basic Usage (Portkey SDK)
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
- [Langfuse](../process_understanding/langfuse.md)
- [Helicone](../process_understanding/helicone.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)
- [Prompt Engineering](../../knowledge_base/system_prompts.md)

## Sources / references
- [Official Website](https://portkey.ai/)
- [Portkey Docs](https://docs.portkey.ai/docs/product/ai-gateway)
- [GitHub Repository](https://github.com/Portkey-AI/gateway)
- [Portkey Pricing Guide (Sacra)](https://sacra.com/c/portkey/)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
