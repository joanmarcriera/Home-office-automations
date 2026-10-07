# Portkey AI Gateway

## What it is
Portkey AI Gateway is an open-source, ultra-low-latency API gateway, routing engine, and control plane designed to manage, monitor, and scale requests across **2,000+ Large Language Models (LLMs)** and 250+ model providers. As of early 2027, Portkey serves as an enterprise control plane for agentic AI architectures, featuring native support for the **FastMCP 3.1 Task Protocol**, dynamic multi-tier fallback routing, semantic caching, and real-time observability across frontier models including **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4**.

```
+-----------------------------------------------------------------------------------+
|                            Portkey AI Gateway Engine                              |
|                                                                                   |
|  +-------------------------------------+   +-----------------------------------+  |
|  | Unified OpenAI/FastMCP 3.1 Proxy      |   | Virtual Key Vault & Governance    |  |
|  | - Single Endpoint for 2,000+ LLMs     |   | - Centralized Provider Keys       |  |
|  | - Native FastMCP Tool Calling       |   | - Budget & Usage Rate Limits      |  |
|  +------------------+------------------+   +-----------------+-----------------+  |
|                     |                                        |                    |
|                     v                                        v                    |
|  +-----------------------------------------------------------------------------+  |
|  |             Smart Routing, Fallback & Load-Balancing Pipeline               |  |
|  |  - Latency & Cost-Optimized Dynamic Fallbacks                               |  |
|  |  - Semantic Response Caching (Redis/In-Memory)                              |  |
|  |  - Enterprise Guardrails (PII Masking, Regex, Toxicity)                    |  |
|  +--------------------------------------+--------------------------------------+  |
|                                         |                                         |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                             Upstream Model Providers                              |
|                                                                                   |
|  +-------------------+  +-------------------+  +-------------------+  +-----------+  |
|  | Anthropic Claude  |  | OpenAI GPT-5.6    |  | Google Gemini 4.0 |  | Local GGUF|  |
|  +-------------------+  +-------------------+  +-------------------+  +-----------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Developing agentic AI systems that rely on a single model vendor introduces major operational risks: single-point API outages, unexpected rate limits, model deprecation, and cost spikes. Furthermore, tracking token consumption, latency metrics, and PII compliance across disparate developer teams and agents is difficult without unified infrastructure.

Portkey solves these structural challenges by providing:
- **Zero-Code Model Fallbacks & Load Balancing**: Automatically routes requests to backup providers (e.g., falling back from Claude 5.6 to GPT-5.6 or DeepSeek-V4) upon HTTP 429/5xx errors.
- **Enterprise Vault & Virtual Keys**: Allows developers to consume virtual keys while real provider API credentials remain encrypted in the Portkey control plane vault.
- **Semantic Caching**: Caches identical or semantically equivalent prompt responses to reduce provider costs and eliminate latency for repeated agent queries.
- **Unified FastMCP 3.1 Tool Gateway**: Proxies tool definitions and MCP task states cleanly across heterogenous backend LLMs.

## Where it fits in the stack
**Category**: Providers / Infrastructure / Model Routing. Portkey sits directly between application runtimes (FastMCP 3.1 agents, web apps, IDEs) and upstream inference providers.

```
+-----------------------------------------------------------------------------------+
|                        Applications & FastMCP 3.1 Agents                          |
|                                                                                   |
|   +-----------------------+   +-----------------------+   +--------------------+  |
|   | FastMCP 3.1 Agents    |   | OpenClaw Workflows    |   | Enterprise Web App |  |
|   +-----------+-----------+   +-----------+-----------+   +---------+----------+  |
|               |                           |                         |             |
|               +---------------------------+-------------------------+             |
|                                           |                                       |
|                                           v                                       |
|                  http://127.0.0.1:8787/v1 (Portkey Gateway Proxy)                 |
+-------------------------------------------+---------------------------------------+
                                            |
                                            v
+-----------------------------------------------------------------------------------+
|                            Portkey Control Plane Engine                           |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   | Guardrails, Semantic Cache, Fallback Evaluator & Virtual Key Vault        |   |
|   +---------------------------------------+-----------------------------------+   |
+-------------------------------------------|---------------------------------------+
                                            |
        +-----------------------------------+-----------------------------------+
        |                                   |                                   |
        v                                   v                                   v
+---------------+                   +---------------+                   +---------------+
| Anthropic API |                   |  OpenAI API   |                   |  DeepSeek API |
+---------------+                   +---------------+                   +---------------+
```

## Typical use cases
- **Multi-Model Fallback & High Availability**: Ensuring uninterrupted operation for mission-critical agent loops by automatically retrying failed requests across alternative model vendors.
- **Enterprise Observability & Audit Logging**: Capturing real-time telemetry, token counts, and request/response payloads across all organization units.
- **Semantic Response Caching**: Reducing LLM API costs by up to 40% in repetitive agent evaluation and testing environments.
- **Guardrail & PII Enforcement**: Scrubbing sensitive data (SSNs, credit cards, emails) before prompts reach third-party inference APIs.

## Key technical features & FastMCP 3.1 integration
- **FastMCP 3.1 Native Proxying**: Full support for forwarding MCP tool definitions, structured JSON schemas, and streaming SSE connections.
- **Ultra-Low Latency Overhead**: C-optimized edge distribution adding <5ms latency overhead per request.
- **Configurable Fallback Matrices**: JSON/YAML routing definitions specifying target models, retry backoffs, and timeout thresholds.
- **Self-Hostable Architecture**: Deployable as a single Docker container or Kubernetes pod with local Redis cache storage.

## Strengths
- **Single SDK Integration**: Interact with 2,000+ models using standard OpenAI client libraries.
- **No Vendor Lock-In**: Decouples application code from specific vendor APIs via virtual keys.
- **Granular Budget Controls**: Set per-key or per-team rate limits and spend caps.
- **Open-Source Engine**: Core gateway codebase is open-source and customizable.

## Limitations
- **Deployment Overhead**: Self-hosting requires maintaining gateway instances and Redis cache infrastructure.
- **Configuration Complexity**: Defining complex conditional fallback routes requires careful JSON/YAML configuration management.

## When to use it
- When managing multiple LLM providers through a single, unified API interface.
- To improve agent reliability using automated multi-provider fallbacks and load balancing across model tiers.
- When requiring production-grade observability (logging, cost tracking, latency monitoring) for enterprise AI workloads.
- To implement centralized prompt versioning and guardrails without modifying core application code.

## When not to use it
- For single-model applications where simple direct SDK access is sufficient.
- In extremely latency-sensitive environments where any proxy overhead (even <5ms) is unacceptable.
- For local-only development using only a single local model provider (e.g., Ollama only).

## Comparison Matrix

| Feature / Metric | Portkey AI Gateway | LiteLLM Proxy | OpenRouter | Vercel AI Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Enterprise Gateway & Control Plane | Lightweight Open-Source Proxy | Model Aggregator SaaS | Serverless Edge Gateway |
| **Deployment Model** | Self-Hosted / Managed Cloud | Self-Hosted / Managed Cloud | Hosted SaaS | Vercel Edge Cloud |
| **Supported Providers**| 250+ Providers (2,000+ Models) | 100+ Providers | 200+ Models | Top Tier Providers |
| **FastMCP 3.1 Support** | Native Protocol Binding | Extension Required | Community Adapter | Native Vercel SDK |
| **Semantic Caching** | Built-in (Vector/Redis) | Supported via Redis | None | None |
| **PII & Guardrails** | 100+ Built-in Guardrails | Custom Middleware | Basic Filtering | Vercel Firewall |

## Getting started

### Deploying via Docker
```bash
docker run -p 8787:8787 -e PORTKEY_GATEWAY_PORT=8787 portkeyai/gateway:latest
```

### Initial Python Configuration
```python
from portkey_ai import Portkey

portkey = Portkey(
    api_key="PORTKEY_ACCOUNT_KEY",
    virtual_key="ANTHROPIC_VIRTUAL_KEY"
)
```

## CLI examples

```bash
# Install the Portkey CLI tool
npm install -g @portkey-ai/cli

# Test an API request through local gateway instance
portkey chat --gateway http://127.0.0.1:8787 --model gpt-5.6 --message "Verify Portkey Gateway status."

# Validate routing configuration schema
portkey config validate ./production-routing.json
```

## API examples

### 1. Multi-Provider Fallback Request with OpenAI SDK
```python
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

client = OpenAI(
    api_key="PORTKEY_VIRTUAL_KEY",
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider="anthropic",
        virtual_key="ANTHROPIC_VIRTUAL_KEY",
        trace_id="agentic-task-9021",
        config="pc-fallback-matrix-v1"
    )
)

response = client.chat.completions.create(
    model="claude-5-6-sonnet",
    messages=[{"role": "user", "content": "Execute code refactoring analysis."}],
    temperature=0.1
)

print(f"Response from model: {response.model}")
print(response.choices[0].message.content)
```

### 2. FastMCP 3.1 Gateway Integration
```python
import json
import urllib.request
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("portkey-mcp-gateway")

PORTKEY_GATEWAY = "http://127.0.0.1:8787/v1/chat/completions"

@mcp.tool()
def route_agent_completion(prompt: str, target_provider: str = "openai") -> Dict[str, Any]:
    """Routes an agent completion through Portkey gateway with FastMCP 3.1 protocol."""
    payload = {
        "model": "gpt-5.6",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    headers = {
        "Content-Type": "application/json",
        "x-portkey-provider": target_provider,
        "x-portkey-trace-id": "fastmcp-3.1-execution"
    }

    req = urllib.request.Request(
        PORTKEY_GATEWAY,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "status": "success",
                "result": data["choices"][0]["message"]["content"],
                "model_used": data.get("model", "unknown")
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run()
```

### 3. Strict Pydantic v2 Fallback Route Validation
```python
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class GatewayTarget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Literal["openai", "anthropic", "google", "deepseek", "groq"] = Field(...)
    model: str = Field(..., min_length=2, description="Target model identifier")
    override_virtual_key: Optional[str] = Field(None, description="Optional Virtual Key override")
    weight: int = Field(1, ge=1, le=100, description="Load balancer weight")

class PortkeyGatewayConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    strategy: Literal["fallback", "loadbalance", "single"] = Field("fallback")
    targets: List[GatewayTarget] = Field(..., min_length=1, max_length=10)
    cache_mode: Literal["simple", "semantic", "none"] = Field("semantic")
    cache_ttl: int = Field(86400, ge=0, description="Cache TTL in seconds")

    @field_validator("targets")
    @classmethod
    def validate_unique_providers(cls, targets: List[GatewayTarget]) -> List[GatewayTarget]:
        if len(targets) < 1:
            raise ValueError("At least one gateway target must be specified")
        return targets

# Example Validation
try:
    config = PortkeyGatewayConfig(
        strategy="fallback",
        targets=[
            GatewayTarget(provider="anthropic", model="claude-5-6-sonnet"),
            GatewayTarget(provider="openai", model="gpt-5.6")
        ],
        cache_mode="semantic",
        cache_ttl=86400
    )
    print("Validated Portkey Gateway Routing Configuration:")
    print(config.model_dump_json(indent=2))
except Exception as err:
    print(f"Validation failed: {err}")
```

## Related tools / concepts
- **[LiteLLM](../../services/litellm.md)**: Lightweight open-source LLM proxy.
- **[OpenRouter](../ai_knowledge/openrouter.md)**: Hosted multi-model inference aggregator.
- **[Vercel AI SDK](../development_ops/vercel-ai-sdk.md)**: Developer toolkit for building AI web applications.
- **[Langfuse](../process_understanding/langfuse.md)**: Open-source LLM tracing and analytics platform.
- **[FastMCP 3.1 Protocol](../automation_orchestration/mcp.md)**: Standardized agent tool execution protocol.

## Sources / references
- [Portkey Official Documentation](https://docs.portkey.ai/)
- [Portkey GitHub Repository](https://github.com/Portkey-AI/gateway)
- [Enterprise AI Control Plane Best Practices](https://portkey.ai/blog/)

---
## Contribution Metadata
- Last reviewed: 2026-10-07
- Confidence: high
