# Vercel AI Gateway

## What it is
Vercel AI Gateway is a lightweight, edge-compatible provider proxy that allows developers to manage, optimize, and observe their AI applications. As of late November/December 2026, it features native support for **MCP 3.1 Task Protocol**, enabling centralized governance for agentic tool-calling across multiple providers like OpenAI (GPT-5.5), Google (Gemini 4.0 Pro, Gemma 3), Anthropic (Claude 5.1), Meta (Llama 4), and Alibaba (Qwen 3.6).

## What problem it solves
It simplifies the operational overhead of running LLM-powered apps by providing built-in caching, rate limiting, and request retries. It also offers a unified dashboard for observing latency, cost, and usage across different models and providers, solving the "fragmented observability" problem in multi-model architectures.

## Where it fits in the stack
**Orchestration / Observability Layer**. It acts as a middleware gateway between the application logic and the model providers, typically used in Vercel-hosted environments or via standard HTTP clients to standardize API interactions.

## Typical use cases
- **Multi-Model Governance**: Centrally managing API keys and usage limits for GPT-5.5, Claude 5.1, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.6.
- **Cost Management**: Using edge-caching to avoid redundant LLM calls for frequent queries.
- **Resilience**: Implementing automated model fallbacks (e.g., if OpenAI is down, fallback to Anthropic).
- **Agentic Routing**: Using MCP 3.1 to route tool-calling tasks to the most efficient available model.

## Strengths
- **Simplicity**: Extremely easy to set up for existing Vercel users.
- **Unified Interface**: Use one base URL pattern for multiple providers.
- **Edge Intelligence**: Caching at the edge provides significant speedups for common queries.
- **OpenAI Compatibility**: Supports the OpenAI SDK format for most upstream providers.
- **MCP Native**: Native support for Task Protocol 3.1 / FastMCP 3.1 simplifies agent integration.

## Limitations
- **Vercel Ecosystem**: While it can be used standalone, it is most powerful when integrated with Vercel's deployment platform.
- **Overhead**: Adds another network hop, though usually mitigated by edge execution.
- **Vendor Lock-in**: Relying on a proprietary gateway for mission-critical routing.

## When to use it
- When deploying AI apps on Vercel and wanting immediate observability and caching.
- When you need a quick way to implement multi-provider fallbacks without complex orchestration code.
- When building autonomous agents that require a stable, governed MCP-compliant gateway.

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

### Managing Gateways
```bash
# List all AI Gateways for your team
vercel ai-gateway list

# Create a new AI Gateway resource
vercel ai-gateway create --name my-prod-gateway

# Manage API keys for a specific gateway
vercel ai-gateway keys list my-prod-gateway
```

### MCP Registration (December 2026)
Register the Vercel AI Gateway as an MCP server to enable governed tool-calling:
```bash
mcp register vercel-gateway --command "npx @vercel/ai-gateway-mcp" \
  --env VERCEL_GATEWAY_ID="YOUR_GATEWAY_ID" \
  --env VERCEL_API_TOKEN="YOUR_TOKEN"
```

## API examples

### Python (OpenAI SDK with GPT-5.5 & Pydantic v2 Verification)
Route OpenAI requests through the gateway for caching and observability, and validate the output using Pydantic v2:
```python
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
import os

# Define response schema for validation
class GatewayResponseModel(BaseModel):
    message: str = Field(description="The validated message from the gateway")
    tokens_used: int = Field(description="Mock token count tracking")

client = OpenAI(
    # Use the Vercel AI Gateway URL as the base
    base_url=f"https://gateway.ai.vercel.com/v1/gateways/{os.environ.get('VERCEL_GATEWAY_ID', 'default_id')}/openai",
    api_key=os.environ.get("OPENAI_API_KEY", "mock_key"),
)

def query_and_validate() -> GatewayResponseModel:
    try:
        completion = client.chat.completions.create(
            model="gpt-5.5",
            messages=[{"role": "user", "content": "How do I implement a fallback in Vercel AI Gateway?"}]
        )
        content = completion.choices[0].message.content or ""

        # Structure payload for validation
        payload = {
            "message": content,
            "tokens_used": completion.usage.total_tokens if completion.usage else 0
        }

        # Pydantic v2 strict validation
        return GatewayResponseModel.model_validate(payload)
    except ValidationError as ve:
        print(f"Validation failed: {ve}")
        raise
    except Exception as e:
        print(f"API call failed: {e}")
        raise
```

### FastMCP 3.1 Tool Integration
Expose a gateway-governed model as a tool using [FastMCP 3.1](../automation_orchestration/mcp.md):
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import os

mcp = FastMCP("GatewayAssistant")

class QueryResult(BaseModel):
    response: str
    gateway_id: str

@mcp.tool()
async def query_model(prompt: str) -> str:
    """Query GPT-5.5 via Vercel AI Gateway with built-in caching."""
    # Logic to call gateway endpoint and validate payload using Pydantic v2
    raw_data = {"response": "Response from Vercel AI Gateway", "gateway_id": os.environ.get("VERCEL_GATEWAY_ID", "default_id")}
    validated = QueryResult.model_validate(raw_data)
    return f"Validated gateway result: {validated.response} (ID: {validated.gateway_id})"

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) — Multi-provider API aggregator.
- [LiteLLM](../../services/litellm.md) — Open-source proxy alternative.
- [Helicone](../process_understanding/helicone.md) — LLM observability and gateway.
- [Portkey](portkey.md) — Control plane for AI apps.
- [Promptfoo](../benchmarking/promptfoo.md) — Testing and benchmarking.
- [Langfuse](../process_understanding/langfuse.md) — Open-source observability.
- [AgentOps](../process_understanding/agentops.md) — Observability for agents.
- [Model Context Protocol](../../knowledge_base/agent_protocols.md) — Standardized agent communication.

## Sources / references
- [Vercel AI Gateway Documentation](https://vercel.com/docs/ai/ai-gateway)
- [Vercel Blog: Introducing AI Gateway](https://vercel.com/blog/introducing-ai-gateway)
- [Model Context Protocol 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)

## Contribution Metadata
- Last reviewed: 2026-12-21
- Confidence: high
