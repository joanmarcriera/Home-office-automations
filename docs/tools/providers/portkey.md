# Portkey AI Gateway

## What it is
Portkey AI Gateway is an open-source, high-performance gateway and control plane designed to route and manage requests to **2,000+ Large Language Models (LLMs)** across 250+ providers. As of June 2026, it serves as the industry-standard "Control Plane for Agentic AI," providing enterprise-grade observability, reliability, and governance through a single, unified API and native **MCP 3.0** support.

## What problem it solves
It solves the complexity of managing multiple LLM providers and models in production agentic loops. By acting as a central proxy, it provides reliability (via fallbacks and retries), efficiency (via semantic caching), and security (via 100+ built-in guardrails). It eliminates "provider lock-in" by allowing agents to switch between Claude 4.8, GPT-5.5, and Gemini 3.5 without code changes.

## Where it fits in the stack
Portkey sits in the **Providers / Infrastructure** layer. It acts as the gateway between agentic applications (like OpenClaw or Agency Agents) and the underlying model providers (OpenAI, Anthropic, Google, Groq, etc.).

## Typical use cases
- **Multi-Model Orchestration**: Routing requests to different models based on reasoning depth (e.g., using GPT-5.5 for planning and Llama 4 for execution).
- **Production Observability**: Real-time tracking of latency, token usage, and costs across all providers via a centralized dashboard.
- **Agentic Reliability**: Implementing automatic retries, provider-level fallbacks, and load balancing to ensure zero-downtime for autonomous agents.
- **Enterprise Governance**: Enforcing PII redaction, budget limits, and audit logs on all model interactions.
- **Prompt Management**: Centralized management and A/B testing of system prompts and tool definitions.

## Strengths
- **Unified SDK**: Connect to 2,000+ models with a single OpenAI-compatible SDK integration.
- **Agentic Protocols**: Native support for the Model Context Protocol (MCP 3.0) and Agentic Tool Calling.
- **High Performance**: Ultra-low latency overhead (<5ms) with local self-hosting options via Docker/K8s.
- **Enterprise Guardrails**: Built-in PII detection, bias filtering, and custom regex-based validation.
- **Virtual Keys**: Manage provider API keys securely in the Portkey vault, using virtual keys in your application code.
- **Semantic Caching**: Reduces costs and improves latency by caching responses based on semantic similarity.

## Limitations
- **Operational Complexity**: Requires managing an additional infrastructure component (if self-hosted).
- **Configuration Overhead**: Complex routing and guardrail policies require precise YAML/JSON configuration.

## When to use it
- When you need to manage multiple LLM providers through a single, unified interface.
- To improve agent reliability using automated fallbacks and load balancing across model tiers.
- When you require production-grade observability (logging, cost tracking, latency monitoring) for AI features.
- To implement centralized prompt versioning and guardrails without modifying core application code.

## When not to use it
- For single-model applications where simple direct SDK access is sufficient.
- In extremely latency-sensitive environments where any proxy overhead (even <5ms) is unacceptable.
- For local-only development using only a single local model provider (e.g., Ollama only).

## Getting started

### Run Locally (Docker)
```bash
docker run -p 8787:8787 portkeyai/gateway
```

### Initial Setup (Python)
```python
from portkey_ai import Portkey

# Initialize Portkey with a Virtual Key
portkey = Portkey(
    api_key="PORTKEY_API_KEY",
    virtual_key="VIRTUAL_KEY"
)
```

## CLI examples
Portkey provides a CLI for managing configurations and testing routes.

```bash
# Install the Portkey CLI
npm install -g @portkey-ai/cli

# Test a request through the gateway
portkey chat --model gpt-5.5 --message "Hello Portkey!"

# List active virtual keys
portkey virtual-keys list

# Validate a config file
portkey config validate ./my-config.json
```

## API examples
Portkey is fully compatible with the OpenAI SDK and provides its own optimized SDK.

### Using the OpenAI Python SDK
```python
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

client = OpenAI(
    api_key="ANY_KEY", # Virtual key is passed in headers
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider="anthropic",
        virtual_key="ANTHROPIC_VIRTUAL_KEY",
        trace_id="agent-run-123"
    )
)

response = client.chat.completions.create(
    model="claude-4-8-opus-20260528",
    messages=[{"role": "user", "content": "Analyze this data."}]
)
```

### Using Portkey Fallbacks (JSON Config)
```json
{
  "strategy": { "mode": "fallback" },
  "targets": [
    { "provider": "openai", "model": "gpt-5.5" },
    { "provider": "anthropic", "model": "claude-4-8-sonnet" }
  ]
}
```

## Related tools / concepts
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) - Unified framework for building AI apps.
- [LiteLLM](../../services/litellm.md) - Lightweight proxy for 100+ LLMs.
- [OpenRouter](../ai_knowledge/openrouter.md) - Model aggregator with specialized routing.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) - Architectural patterns for model selection.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) - Standardized agent-tool communication.
- [Langfuse](../process_understanding/langfuse.md) - Open-source observability and analytics.
- [Helicone](../process_understanding/helicone.md) - LLM observability platform.

## Sources / References
- [Official Website](https://portkey.ai/)
- [Portkey Documentation](https://docs.portkey.ai/)
- [Portkey GitHub Repository](https://github.com/Portkey-AI/gateway)
- [Enterprise AI Gateway Patterns (2026)](https://portkey.ai/blog/agentic-gateway-patterns)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-24
