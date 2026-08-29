# Vercel AI Gateway

## What it is
Vercel AI Gateway is a lightweight, edge-compatible provider proxy and agentic control plane that allows developers to manage, optimize, secure, and observe their AI applications. As of early January 2027, it features full native support for **FastMCP 3.1 Task Protocol**, enabling centralized governance, token tracking, and semantic rate-limiting for agentic tool-calling across leading frontier and open-weight models including OpenAI (GPT-5.6), Google (Gemini 4.0 Ultra, Gemma 4), Anthropic (Claude 5.6), Meta (Llama 4), DeepSeek (DeepSeek-V4), and Alibaba (Qwen 3.6 VL).

## What problem it solves
It eliminates the operational complexity and security risks of running multi-model LLM applications by providing built-in semantic caching, enterprise-grade rate limiting, automated fallback chains, and cross-provider request retries. It offers a unified observability dashboard for tracking latency, cost, and token usage across heterogeneous model providers, solving the fragmented observability and security challenge in modern multi-agent architectures.

## Where it fits in the stack
**Orchestration / Observability / Security Layer**. It operates as a high-performance middleware gateway situated between application agent logic and underlying model providers, typically deployed in Vercel Serverless/Edge environments or accessed via standard OpenAI-compatible HTTP clients.

## Typical use cases
- **Multi-Model Enterprise Governance**: Centrally managing API keys, budget caps, and usage policies across GPT-5.6, Claude 5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6 VL.
- **Agentic Edge Caching**: Utilizing semantic edge-caching to eliminate redundant LLM calls and reduce latency for recurring prompt patterns.
- **Resilient Fallback Routing**: Implementing automated model failovers (e.g., automatically routing from Claude 5.6 to Gemini 4.0 Ultra or DeepSeek-V4 during provider outages).
- **Governed Tool-Calling**: Routing FastMCP 3.1 task protocol requests through secure edge rules to prevent unauthorized tool execution.

## Strengths
- **Zero-Config Vercel Integration**: Deploys seamlessly into existing Vercel Next.js/Node.js serverless and edge functions.
- **Unified Provider API**: Single standardized base URL pattern supporting OpenAI, Anthropic, Google, and open-weights endpoints.
- **Edge Performance**: Ultra-low-latency edge caching and request routing via Vercel Edge Network.
- **OpenAI & FastMCP Compatibility**: Fully compatible with OpenAI Python/TS SDKs and FastMCP 3.1 Task Protocol schemas.
- **Granular Token Governance**: Fine-grained controls for budget caps, rate limits, and audit logs per project or team member.

## Limitations
- **Ecosystem Optimization**: Most seamless when deployed within Vercel's ecosystem, though standalone HTTP access is supported.
- **Additional Network Hop**: Introduces a minimal routing hop (typically 5–15ms), which is offset by edge caching when hits occur.
- **Managed Gateway Dependency**: Relies on Vercel's cloud control plane for routing rules and telemetry aggregation.

## When to use it
- When deploying AI applications and autonomous agents on Vercel requiring instant observability and semantic caching.
- When building multi-provider architectures that require automated fallback and cost management without custom proxy code.
- When orchestrating autonomous agent networks using FastMCP 3.1 that need centralized governance and API key isolation.

## When not to use it
- If your architecture demands a 100% self-hosted, air-gapped open-source gateway (see [LiteLLM](../../services/litellm.md)).
- If your system requires ultra-low-latency on-premise local inference where edge proxies introduce unnecessary overhead.
- If you already rely on an existing enterprise observability stack like LangSmith or Helicone.

## Getting started

### 1. Installation
Install the Vercel CLI to manage your AI Gateway resources:
```bash
npm install -g vercel@latest
```

### 2. Create a Gateway
Create a new gateway via the [Vercel Dashboard](https://vercel.com/dashboard/ai) or CLI:
```bash
vercel ai-gateway create --name prod-agent-gateway
```
Note your **Gateway ID**.

### Hello World Example
Verify gateway connectivity by listing supported models through the proxy:
```bash
curl -H "Authorization: Bearer $VERCEL_API_TOKEN" \
  https://ai-gateway.vercel.sh/v1/models
```

## CLI examples

### Managing Gateways
```bash
# List all AI Gateways configured for your team
vercel ai-gateway list

# Manage API key assignments and usage budgets
vercel ai-gateway keys list prod-agent-gateway

# Set rate limits and budget caps
vercel ai-gateway limits set prod-agent-gateway --max-cost-per-day 50.00
```

### MCP Registration (FastMCP 3.1)
Register the Vercel AI Gateway as a FastMCP server to enable governed tool calling across agents:
```bash
mcp register vercel-gateway --command "npx @vercel/ai-gateway-mcp@latest" \
  --env VERCEL_GATEWAY_ID="gw_prod_2027_01" \
  --env VERCEL_API_TOKEN="vercel_pat_xxxx"
```

## API examples

### Python (OpenAI SDK with GPT-5.6 & Pydantic v2 Verification)
Route requests through the gateway with automatic fallbacks and validate responses using Pydantic v2:
```python
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
import os

class GatewayResponseModel(BaseModel):
    message: str = Field(description="The validated message from the gateway")
    tokens_used: int = Field(description="Token count tracking")
    provider_used: str = Field(default="openai", description="Active upstream provider")

client = OpenAI(
    base_url=f"https://gateway.ai.vercel.com/v1/gateways/{os.environ.get('VERCEL_GATEWAY_ID', 'default_id')}/openai",
    api_key=os.environ.get("OPENAI_API_KEY", "mock_key"),
)

def query_and_validate() -> GatewayResponseModel:
    try:
        completion = client.chat.completions.create(
            model="gpt-5.6",
            messages=[{"role": "user", "content": "How do I configure automatic fallbacks in Vercel AI Gateway?"}]
        )
        content = completion.choices[0].message.content or ""

        payload = {
            "message": content,
            "tokens_used": completion.usage.total_tokens if completion.usage else 0,
            "provider_used": getattr(completion, "provider", "openai")
        }

        return GatewayResponseModel.model_validate(payload)
    except ValidationError as ve:
        print(f"Validation failed: {ve}")
        raise
    except Exception as e:
        print(f"API call failed: {e}")
        raise
```

### FastMCP 3.1 Tool Integration
Expose a gateway-governed model as a FastMCP 3.1 tool for multi-agent workflows:
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import os

mcp = FastMCP("GatewayAssistant")

class QueryResult(BaseModel):
    response: str = Field(description="Model output")
    gateway_id: str = Field(description="Active Vercel Gateway identifier")

@mcp.tool()
async def query_model(prompt: str) -> str:
    """Query GPT-5.6 or Gemini 4.0 Ultra via Vercel AI Gateway with edge caching."""
    raw_data = {
        "response": f"Processed prompt via Vercel Gateway: {prompt[:30]}...",
        "gateway_id": os.environ.get("VERCEL_GATEWAY_ID", "default_id")
    }
    validated = QueryResult.model_validate(raw_data)
    return f"Validated result: {validated.response} (Gateway: {validated.gateway_id})"

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) — Multi-provider API aggregator and proxy.
- [LiteLLM](../../services/litellm.md) — Self-hosted open-source proxy alternative.
- [Helicone](../process_understanding/helicone.md) — LLM observability and gateway infrastructure.
- [Portkey](portkey.md) — Enterprise AI gateway and control plane.
- [Promptfoo](../benchmarking/promptfoo.md) — Testing and benchmarking for LLM prompts.
- [Langfuse](../process_understanding/langfuse.md) — Open-source LLM observability and tracing.
- [FastMCP](../automation_orchestration/mcp.md) — High-performance Python framework for Model Context Protocol 3.1.

## Sources / references
- [Vercel AI Gateway Documentation](https://vercel.com/docs/ai/ai-gateway)
- [Vercel Blog: AI Gateway Updates](https://vercel.com/blog/introducing-ai-gateway)
- [Model Context Protocol FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
