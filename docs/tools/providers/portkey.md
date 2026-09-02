# Portkey AI Gateway

## What it is
Portkey AI Gateway is an open-source, high-performance gateway and control plane designed to route and manage requests to **2,000+ Large Language Models (LLMs)** across 250+ providers. As of early January 2027, it serves as the industry-standard "Control Plane for Agentic AI," providing enterprise-grade observability, reliability, and governance through a single, unified API and native **FastMCP 3.1 Task Protocol** routing capabilities, optimized for frontier models such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**.

## What problem it solves
It solves the complexity of managing multiple LLM providers and models in production agentic loops. By acting as a central proxy, it provides reliability (via fallbacks and retries), efficiency (via semantic caching), and security (via 100+ built-in guardrails). It eliminates "provider lock-in" by allowing agents to switch dynamically between Claude 5.6, GPT-5.6, and Llama 4 without code changes.

## Where it fits in the stack
Portkey sits in the **Providers / Infrastructure** layer. It acts as the gateway between agentic applications (like OpenClaw or Agency Agents) and the underlying model providers (OpenAI, Anthropic, Google, Groq, etc.).

## Typical use cases
- **Multi-Model Orchestration**: Routing requests to different models based on reasoning depth (e.g., using GPT-5.6 for planning and Llama 4 for execution).
- **Production Observability**: Real-time tracking of latency, token usage, and costs across all providers via a centralized dashboard.
- **Agentic Reliability**: Implementing automatic retries, provider-level fallbacks, and load balancing to ensure zero-downtime for autonomous agents.
- **Enterprise Governance**: Enforcing PII redaction, budget limits, and audit logs on all model interactions.
- **Prompt Management**: Centralized management and A/B testing of system prompts and tool definitions.

## Strengths
- **Unified SDK**: Connect to 2,000+ models with a single OpenAI-compatible SDK integration.
- **FastMCP 3.1 Task Protocol Native**: Native support for Model Context Protocol Task Protocol and Agentic Tool Calling, routing tool calls smoothly to backend servers.
- **High Performance**: Ultra-low latency overhead (<5ms) with local self-hosting options via Docker/K8s.
- **Enterprise Guardrails**: Built-in PII detection, bias filtering, custom regex-based validation, and LLM-based policy evaluators.
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
portkey chat --model gpt-5.6-preview --message "Hello Portkey!"

# List active virtual keys
portkey virtual-keys list

# Validate a config file
portkey config validate ./my-config.json
```

## API examples

### Using the OpenAI Python SDK (Early January 2027 specs)
```python
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

client = OpenAI(
    api_key="ANY_KEY", # Virtual key is passed in headers
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider="anthropic",
        virtual_key="ANTHROPIC_VIRTUAL_KEY",
        trace_id="agent-run-123",
        metadata={"user_tier": "enterprise", "mcp_version": "3.1"}
    )
)

response = client.chat.completions.create(
    model="claude-5-6-sonnet",
    messages=[{"role": "user", "content": "Analyze this data."}]
)
```

### Programmatic Route Configuration with Strict Pydantic v2 Validation
This example validates a complex Portkey gateway routing and fallback configuration programmatically before sending it to the Portkey API, preventing runtime execution failures caused by malformed targets or missing parameters.
```python
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class TargetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", freeze=True)

    provider: Literal["openai", "anthropic", "google", "cohere", "groq", "azure-openai"] = Field(
        ...,
        description="Supported Portkey API provider"
    )
    model: str = Field(..., description="Target model name (e.g., gpt-5.6-preview, claude-5-6-sonnet)")
    override_api_key: Optional[str] = Field(default=None, description="Optional target-specific key override")
    weight: Optional[int] = Field(default=1, ge=1, description="Routing weight for load-balanced targets")

    @field_validator("model")
    @classmethod
    def validate_model_name(cls, value: str) -> str:
        clean = value.strip()
        if len(clean) < 3:
            raise ValueError("Model name must be at least 3 characters long.")
        return clean

class PortkeyRouteConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    strategy: Literal["fallback", "loadbalance", "single"] = Field(
        default="single",
        description="Portkey routing and execution strategy"
    )
    targets: List[TargetConfig] = Field(..., min_length=1, description="List of target providers/models")
    cache_mode: Literal["simple", "semantic", "none"] = Field(default="none")
    cache_ttl: Optional[int] = Field(default=86400, ge=0, description="Cache duration in seconds")

    @field_validator("targets")
    @classmethod
    def validate_targets_limit(cls, targets: List[TargetConfig]) -> List[TargetConfig]:
        if len(targets) > 10:
            raise ValueError("Portkey gateway configs support a maximum of 10 targets in fallback/loadbalance paths.")
        return targets

# Example programmatic generation and validation of a Portkey JSON configuration
try:
    config_data = {
        "strategy": "fallback",
        "targets": [
            {"provider": "openai", "model": "gpt-5.6-preview", "weight": 1},
            {"provider": "anthropic", "model": "claude-5-6-sonnet", "weight": 1}
        ],
        "cache_mode": "semantic",
        "cache_ttl": 86400
    }

    # Run strict Pydantic v2 validation
    validated_config = PortkeyRouteConfig.model_validate(config_data)
    json_payload = validated_config.model_dump_json(indent=2, exclude_none=True)
    print("Validated Portkey JSON Config payload:")
    print(json_payload)
except Exception as e:
    print("Invalid Portkey Configuration detected:", e)
```

## Related tools / concepts
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) - Unified framework for building AI apps.
- [LiteLLM](../../services/litellm.md) - Lightweight proxy for 100+ LLMs.
- [OpenRouter](../ai_knowledge/openrouter.md) - Model aggregator with specialized routing.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) - Architectural patterns for model selection.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) - Standardized agent-tool communication.
- [Langfuse](../process_understanding/langfuse.md) - Open-source observability and analytics.
- [Helicone](../process_understanding/helicone.md) - LLM observability platform.

## Sources / references
- [Official Website](https://portkey.ai/)
- [Portkey Documentation](https://docs.portkey.ai/)
- [Portkey GitHub Repository](https://github.com/Portkey-AI/gateway)
- [Enterprise AI Gateway Patterns (2026)](https://portkey.ai/blog/agentic-gateway-patterns)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
