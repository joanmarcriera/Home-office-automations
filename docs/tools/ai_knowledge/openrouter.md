# OpenRouter

## What it is
OpenRouter is a unified API gateway, intelligent model router, and meta-provider for foundation language, vision, code, and multimodal AI models. Operating as a single OpenAI-compatible HTTP interface, OpenRouter provides developer access to 250+ model variants hosted across major cloud providers (Anthropic, OpenAI, Google DeepMind, Meta, DeepSeek, Mistral, Qwen, Cohere, Fireworks, Together, and Baseten). As of early 2027, OpenRouter incorporates native **FastMCP 3.1 routing**, real-time thinking token streaming, dynamic price-to-performance load balancing, automatic failover chains, prompt caching normalization, and granular enterprise billing controls.

OpenRouter sits between application frameworks ([LangChain](langchain.md), [AutoGPT](../agents/autogpt.md), [Claude Code](../development_ops/claude-code.md), [Aider](../development_ops/aider.md)) and raw inference endpoints. It evaluates real-time API latency metrics, provider capacity, and token pricing to route incoming requests to the optimal endpoint without requiring code changes or multiple subscription credentials.

## What problem it solves
Integrating frontier AI models into production software introduces severe infrastructure, operational, and financial friction:

1. **Vendor Lock-In & Fragmented Billing**: Managing separate developer accounts, API key lifecycles, monthly rate limits, and payment methods across dozens of AI providers creates immense administrative overhead.
2. **API Outages & Single-Provider Vulnerabilities**: When a primary foundation model provider experiences rate limits, outage incidents, or degraded performance, dependent applications crash.
3. **Price Inefficiency**: Similar open-weights models (e.g., Llama 4, Qwen 3.8, DeepSeek-V4) are hosted by multiple cloud providers at vastly different prices per million tokens.
4. **Non-Standardized Feature Protocols**: Different providers implement tool calling, structured outputs, vision inputs, prompt caching, and thinking/reasoning token formats differently.

OpenRouter solves these challenges by providing a standardized, single API endpoint that normalizes provider responses, executes zero-downtime model fallbacks, normalizes prompt caching across hosts, and routes requests to the lowest-cost available provider automatically.

```
+-----------------------------------------------------------------------------------+
|                            OPENROUTER GATEWAY ARCHITECTURE                        |
+-----------------------------------------------------------------------------------+

[ Client Application / Agent Framework ] ──> [ FastMCP 3.1 Tool Request ]
                                                        │
                                                        ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
| OpenRouter Intelligent Gateway & Meta-Router                                     |
|                                                                                  |
| ┌────────────────────────┐  ┌────────────────────────┐  ┌──────────────────────┐ |
| │ Credit & Rate Limit    │  │ Fallback Priority      │  │ Response Normalizer  │ |
| │ Validator              │  │ Evaluator              │  │ & Token Streamer     │ |
| └────────────────────────┘  └────────────────────────┘  └──────────────────────┘ |
└──────────────────────────────────────────────────────────────────────────────────┘
            │                                 │                                │
            ▼                                 ▼                                ▼
┌────────────────────────┐        ┌────────────────────────┐       ┌──────────────────────┐
| Provider A (Primary)   |        | Provider B (Fallback)  |       | Provider C (Low-Cost)|
| - Claude 5.1           |        | - GPT-5.5              |       | - DeepSeek-V4        |
| (Anthropic Direct)     |        | (OpenAI Cloud)         |       | (Together / Baseten) |
└────────────────────────┘        └────────────────────────┘       └──────────────────────┘
```

## Where it fits in the stack
**Provider / Routing Layer**. OpenRouter sits between high-level orchestration agents ([CrewAI](../agents/crewai.md), [LlamaIndex](../frameworks/llamaindex.md), [Roo Code](../agents/roo-code.md)) and raw inference endpoints. It serves as an intelligent proxy, balancing load, masking outages, and managing token budgets.

### Key Capabilities & Technical Features

#### 1. Unified OpenAI-Compatible API
Exposes standard `/v1/chat/completions` and `/v1/models` endpoints. Switching between models (e.g., from `openai/gpt-5.5` to `anthropic/claude-5-1-sonnet` or `deepseek/deepseek-r1`) requires changing only a single JSON parameter field.

#### 2. Multi-Model Priority Fallback Chains
Developers specify comma-separated fallback arrays in the `model` parameter (e.g., `"anthropic/claude-5-1-sonnet,openai/gpt-5.5,meta-llama/llama-4-405b"`). If the primary model endpoint experiences rate limits, timeouts, or 5xx server errors, OpenRouter transparently retries the request down the fallback chain without returning errors to the client.

#### 3. Price-and-Latency Dynamic Routing
For open-weights models hosted by multiple inference platforms (e.g., DeepSeek-V4 hosted on Together, Fireworks, and Baseten), OpenRouter routes requests dynamically to the host providing the lowest per-token cost or lowest TTFT (Time To First Token).

#### 4. Normalized Prompt Caching & Thinking Streams
Normalizes prompt caching behaviors across Anthropic, OpenAI, and DeepSeek, automatically deducting cache hit discounts from billable usage. Streams reasoning/thinking tokens uniformly using standard SSE events.

#### 5. FastMCP 3.1 Gateway Protocol
Native support for FastMCP 3.1 tools allows OpenRouter to function as a Model Context Protocol tool provider, enabling agents to query model availability, compare token pricing dynamically, and manage API credit allocations programmatically.

## Typical use cases
- **Production Agent High Availability**: Configuring primary and backup model chains to ensure 99.99% uptime for customer-facing AI agents.
- **Multi-Provider Cost Optimization**: Directing heavy bulk background tasks to low-cost open-weights models (Qwen 3.8, DeepSeek-V4) while reserving frontier models (Claude 5.1) for high-reasoning code synthesis.
- **Centralized Enterprise Token Management**: Consolidating usage analytics, departmental spending caps, and audit logs across hundreds of team developers into a single dashboard.
- **Model Evaluation & Benchmarking**: Running side-by-side prompt accuracy tests across multiple frontier models using identical request payloads.

## Strengths
- **Vast Model Catalog**: Instant access to 250+ model variants through a single API key without individual provider approvals.
- **Zero-Downtime Resilience**: Automatic model failover chains eliminate service disruptions caused by upstream provider outages.
- **Transparent Competitive Pricing**: Routes requests to the cheapest host for open-weights models, passing bulk host discounts directly to developers.
- **Privacy Controls & Zero Data Retention**: Optional "no-trace" flags (`privacy: "no-store"`) prevent upstream providers from logging or training on prompt data.

## Limitations
- **Minor Proxy Latency Overhead**: Introduces a minor routing network latency (< 10ms) relative to direct provider connections.
- **Intermediary Dependency**: Downstream API availability depends on OpenRouter's edge gateway infrastructure remaining operational.
- **Complex Provider Specific Parameters**: Provider-specific hyper-parameters (e.g., custom logit biases or proprietary search parameters) may require explicit provider routing flags.

## When to use it
- When building production AI applications requiring 99.99% uptime via automated model failover.
- When evaluating and benchmarking multiple model families during prototyping.
- When building FastMCP 3.1 agentic tools requiring dynamic model selection and centralized token budget controls.

## When not to use it
- In latency-critical edge applications where microsecond round-trips require direct co-located connections to a single cloud provider.
- When enterprise compliance mandates direct contractual SLAs and dedicated reserved GPU capacity with a specific vendor (e.g., Azure OpenAI enterprise agreements).
- For air-gapped, offline deployments where cloud API access is prohibited (prefer [Local LLMs](local_llms.md)).

## Getting started

### 1. Account Setup and API Key Generation
1. Create an account at [openrouter.ai](https://openrouter.ai/).
2. Navigate to **Keys** and click **Create Key**.
3. Set optional credit limits or model access restrictions for the key.
4. Export key to your terminal environment:
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-abcdef1234567890..."
   ```

### 2. Quick Verification Call (cURL)
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "HTTP-Referer: https://my-app.internal" \
  -H "X-Title: KnowledgeOps Agent" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-5-1-sonnet",
    "messages": [{"role": "user", "content": "Explain FastMCP 3.1 protocol capabilities."}]
  }'
```

## CLI examples

### 1. Querying Live Model List & Pricing (JQ Formatting)
```bash
# Fetch available models and extract pricing per million tokens
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | {
  id: .id,
  name: .name,
  prompt_price_per_m: (.pricing.prompt | tonumber * 1000000),
  completion_price_per_m: (.pricing.completion | tonumber * 1000000),
  context_length: .context_length
}' | head -n 30
```

### 2. Testing Endpoint Status via cURL
```bash
curl -s https://openrouter.ai/api/v1/credits \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" | jq .
```

## API examples

### Python: Multi-Model FastMCP 3.1 Gateway Integration & Pydantic v2 Validation
The following production script demonstrates an AI agent executing multi-model routing queries through OpenRouter via FastMCP 3.1 and validating responses with Pydantic v2.

```python
import httpx
import json
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
import mcp.server.fastmcp as fastmcp

# Define strict Pydantic v2 validation schemas
class OpenRouterUsage(BaseModel):
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    total_tokens: int = Field(..., ge=0)

class OpenRouterChoice(BaseModel):
    finish_reason: str = Field(...)
    message: Dict[str, Any] = Field(...)

class OpenRouterResponse(BaseModel):
    id: str = Field(...)
    model: str = Field(..., description="Actual model selected and executed by OpenRouter gateway")
    choices: List[OpenRouterChoice] = Field(..., min_length=1)
    usage: OpenRouterUsage

    @field_validator('choices')
    @classmethod
    def validate_choices(cls, v: List[OpenRouterChoice]) -> List[OpenRouterChoice]:
        if not v or "content" not in v[0].message:
            raise ValueError("Malformed response: Missing message content in choices.")
        return v

# Initialize FastMCP 3.1 Server
mcp_server = fastmcp.FastMCP("OpenRouter Gateway", version="3.1")

class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def query_models_with_fallback(
        self,
        prompt: str,
        fallback_models: List[str]
    ) -> OpenRouterResponse:
        model_string = ",".join(fallback_models)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://knowledge-ops.internal",
            "X-Title": "FastMCP 3.1 Router",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_string,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(self.base_url, headers=headers, json=payload)
            resp.raise_for_status()
            return OpenRouterResponse.model_validate(resp.json())

# FastMCP Tool Endpoint
@mcp_server.tool()
async def dispatch_agent_prompt(prompt: str, primary_model: str = "anthropic/claude-5-1-sonnet") -> str:
    """Dispatch a prompt through OpenRouter with automatic fallback chains."""
    api_key = os.getenv("OPENROUTER_API_KEY", "sk-or-v1-dev-key")
    client = OpenRouterClient(api_key=api_key)

    fallbacks = [primary_model, "openai/gpt-5.5", "meta-llama/llama-4-405b"]

    try:
        result = await client.query_models_with_fallback(prompt, fallbacks)
        content = result.choices[0].message.get("content", "")

        return (
            f"Executed Model: '{result.model}'\n"
            f"Total Tokens: {result.usage.total_tokens}\n\n"
            f"Response Content:\n{content}"
        )
    except Exception as e:
        return f"OpenRouter Gateway Error: {str(e)}"

if __name__ == "__main__":
    mcp_server.run()
```

### Configuration & Gateway Comparison Matrix

| Dimension / Feature | OpenRouter | Azure AI Foundry | AWS Bedrock | Resolution Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Model Catalog Size** | 250+ Models | ~50 Models | ~30 Models | Single endpoint switch. |
| **Fallback Priority** | Multi-Model Array | Manual Failover | Custom Lambda | Zero downtime failover. |
| **402 Payment Error** | Balance depleted | N/A | N/A | Top up OpenRouter balance. |
| **502 Bad Gateway** | Upstream host error | Provider outage | Provider outage | Automatic fallback chain retry. |

## Related tools / concepts
- [OpenAI](openai.md) — Foundation model provider endpoint.
- [Claude](claude.md) — High-reasoning Anthropic frontier models.
- [Gemini](gemini.md) — Multimodal long-context model family.
- [Local LLMs](local_llms.md) — Offline, self-hosted model alternatives.
- [FastMCP 3.1 Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Tool protocol standard.
- [LangChain](langchain.md) — Framework using OpenRouter API gateways.

## Sources / references
- [OpenRouter Official Site](https://openrouter.ai/)
- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [OpenRouter Model Rankings & Benchmarks](https://openrouter.ai/rankings)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-10-09
- Confidence: high
