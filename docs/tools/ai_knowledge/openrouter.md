# OpenRouter

## What it is
OpenRouter is a unified API gateway, smart router, and intelligent "meta-provider" for Large Language Models (LLMs), Vision Language Models (VLMs), and multimodal foundation models. It provides a single, standardized, OpenAI-compatible REST and WebSocket API to access hundreds of models from providers such as Anthropic, OpenAI, Google, Meta, DeepSeek, Mistral, Qwen, and Cohere. As of early 2027, OpenRouter features native **FastMCP 3.1 routing**, real-time thinking token streams, automatic multi-provider fallback chains, prompt caching optimization, dynamic pricing arbitration, and unified team usage analytics.

```
+-----------------------------------------------------------------------------------+
|                           CLIENT & AGENT APPLICATION LAYER                        |
|    [ FastMCP 3.1 Agent ]     [ LangChain / AutoGen ]     [ Enterprise App ]      |
+-----------------------------------------------------------------------------------+
                                         |
                       (OpenAI API Format / MCP 3.1 Proxy)
                                         v
+-----------------------------------------------------------------------------------+
|                               OPENROUTER GATEWAY                                  |
|                                                                                   |
|  +------------------------+  +------------------------+  +---------------------+  |
|  | Rate Limit Manager     |  | Credit & Billing Core  |  | Thinking Token Stream|  |
|  +------------------------+  +------------------------+  +---------------------+  |
|                                        |                                          |
|                                        v                                          |
|  +-----------------------------------------------------------------------------+  |
|  | DYNAMIC ROUTING & FALLBACK ENGINE                                           |  |
|  | - Comma-Separated Fallback Priority Chain                                   |  |
|  | - Real-time Latency & Health Checks                                         |  |
|  | - Cost Arbitration & Provider Load Balancing                               |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
       |                                 |                                 |
       v                                 v                                 v
+--------------+                 +--------------+                 +--------------+
| ANTHROPIC    |                 | OPENAI       |                 | DEEPSEEK     |
| Claude 5.6   |                 | GPT-5.6      |                 | DeepSeek-V4  |
+--------------+                 +--------------+                 +--------------+
```

## Architecture & System Flow

OpenRouter functions as a high-throughput, low-latency API proxy layer between application runtimes and distributed inference endpoints. When a request enters OpenRouter, the routing engine evaluates client parameters (e.g., fallback lists, max price, data privacy flags, provider latency), verifies client credit balance and rate limits, and routes the request to the optimal downstream host.

```
+-----------------------------------------------------------------------------------+
|                         OPENROUTER ROUTING DECISION TREE                          |
|                                                                                   |
|  Client Request -> [ Validate Key & Credits ]                                     |
|                           |                                                       |
|                           v                                                       |
|                    [ Evaluate Primary Model ]                                     |
|                           |                                                       |
|            +--------------+--------------+                                        |
|            |                             |                                        |
|      (Provider Healthy)          (Outage / Rate Limit / Error)                    |
|            |                             |                                        |
|            v                             v                                        |
|     [ Dispatch Request ]         [ Trigger Fallback Model #1 ]                    |
|            |                             |                                        |
|            |                     +-------+-------+                                |
|            |                     |               |                                |
|            |               (Success)        (Error)                               |
|            |                     |               |                                |
|            |                     v               v                                |
|            |             [ Dispatch ]    [ Trigger Fallback Model #2 ]            |
|            |                     |               |                                |
|            +---------------------+---------------+                                |
|                                  |                                                |
|                                  v                                                |
|                   [ Stream Tokens Back to Client ]                                |
+-----------------------------------------------------------------------------------+
```

## What problem it solves

Managing model integrations across multiple AI providers creates significant engineering and operational friction:
- **API Key & Billing Fragmentations**: Developers must manage separate API keys, invoices, and credit balances across dozens of vendors.
- **Provider Outages & Rate Limit Spikes**: Single-provider downtime halts application pipelines unless complex, custom failover logic is built.
- **Cost Arbitration**: Open-weights models (e.g., Llama 4, DeepSeek-V4, Qwen 3.8) are hosted by multiple providers at vastly different prices and latencies. OpenRouter automatically selects the cheapest/fastest host.
- **Schema & Protocol Disparities**: OpenRouter normalizes response structures, reasoning tokens, tool calling schemas, and FastMCP 3.1 task protocols across all underlying models.

## Where it fits in the stack

**Category**: Provider / Gateway / Routing Layer. It sits between application/agent frameworks (such as [LangChain](langchain.md) or [Claude Code](../development_ops/claude-code.md)) and underlying LLM infrastructure endpoints, functioning as an intelligent proxy, load balancer, and billing aggregator.

```
+-----------------------------------------------------------------------------------+
|                               AGENTIC FRAMEWORKS                                  |
|     [ FastMCP 3.1 Server ]      [ Claude Code ]      [ Agency Swarm / AutoGen ]   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                          OPENROUTER ROUTING GATEWAY                               |
|                     (OpenAI-Compatible / Standardized MCP)                        |
+-----------------------------------------------------------------------------------+
                                         |
       +---------------------------------+---------------------------------+
       |                                 |                                 |
       v                                 v                                 v
+------------------+             +------------------+             +------------------+
| Commercial LLMs  |             | Open-Weights     |             | Multimodal VLMs  |
| Anthropic/OpenAI |             | DeepSeek/Qwen/Llama|            | Gemini/Moondream |
+------------------+             +------------------+             +------------------+
```

## Typical use cases
- **Multi-Model Agent Orchestration**: Toggling between specialized models (e.g., Gemini 4.0 Ultra for long-context retrieval, Claude 5.6 for code synthesis, DeepSeek-V4 for high-volume reasoning) via a single unified client.
- **Consolidated Billing & Organization Controls**: Aggregating enterprise or team AI API usage across dozens of model providers into one invoice with granular per-key spend limits.
- **Hosted Open-Weights Access**: Deploying models like Llama 4, Gemma 3, or Qwen 3.8 without managing local GPU hardware or cloud instances.
- **High-Availability Fallback Chains**: Configuring comma-separated model arrays (e.g., `anthropic/claude-5.6-sonnet,openai/gpt-5.6,deepseek/deepseek-v4`) for 99.99% system availability.
- **Cost-Optimized Batch Processing**: Routing non-urgent offline classification jobs to the lowest-cost provider hosting open-weights models.

## Deep Dive Features & FastMCP 3.1 Capabilities

1. **Thinking Token Streaming**: Normalizes step-by-step reasoning tokens (e.g., DeepSeek-R1/V4, Claude 5.6) into consistent JSON attributes in stream chunks.
2. **Dynamic Provider Quantization Selection**: Users can specify precision preferences (`float16`, `int8`, `int4`) or specific hosts (e.g., Together, DeepInfra, Fireworks, Novita).
3. **Data Privacy Guardrails**: Optional "no-log" privacy headers ensure downstream host providers do not log or store prompt data.
4. **FastMCP 3.1 Protocol Support**: Native support for task routing, tool calling, and structured outputs conforming to FastMCP 3.1 standards.

## Strengths
- **Vast Model Selection**: Instant access to 250+ foundation models through a single API key.
- **Transparent Competitive Pricing**: Routes requests dynamically to the lowest-cost provider hosting open-weights models.
- **Standardized Drop-In API**: Completely OpenAI-compatible `chat/completions` and structured outputs interface.
- **Advanced Capabilities**: Native tool calling, structured outputs, prompt caching, thinking token streams, and FastMCP 3.1 routing.
- **Zero Lock-In**: Migration from single-provider SDKs to OpenRouter requires changing only the `base_url` and `api_key`.

## Limitations
- **Gateway Proxy Latency**: Introduces minimal proxy routing overhead (~5–15ms) relative to direct provider connections.
- **Intermediary Trust**: Requires trusting OpenRouter as a secure proxy in the data path for unencrypted prompts.
- **Single Point of Dependency**: Disruption to OpenRouter's proxy layer affects access to all downstream routed models unless local failover exists.

## When to use it
- During development and prototyping to rapidly evaluate and compare model accuracy, latency, and costs.
- For production agents that require multi-provider failover, model routing, and cost optimization.
- In team environments where centralized budget control and unified usage reporting are required.
- When orchestrating agent workflows that need FastMCP 3.1 tool calling across diverse model providers.

## When not to use it
- For latency-critical edge applications where microsecond round-trips matter.
- When direct enterprise SLAs and reserved compute capacity with a specific provider (e.g., Azure OpenAI) are already established.
- When strict air-gapped data residency policies mandate local-only inference (prefer [Local LLMs](local_llms.md)).

## Getting started

### 1. API Key Setup
1. Create an account at [openrouter.ai](https://openrouter.ai/).
2. Navigate to **Keys** and generate a new secret API key.
3. Pre-fund your account balance or attach enterprise payment details.

### 2. Environment Setup
```bash
export OPENROUTER_API_KEY="sk-or-v1-your_openrouter_api_key_here"
```

## CLI examples

### Testing Endpoint with cURL
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "google/gemma-3-27b-it",
    "messages": [{"role": "user", "content": "Explain FastMCP 3.1 protocol features."}]
  }'
```

### Listing Available Models and Pricing
```bash
curl -s https://openrouter.ai/api/v1/models | jq '.data[] | {id, pricing}' | head -n 20
```

### Multi-Model Fallback Call via cURL
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "HTTP-Referer: https://my-agent.internal" \
  -H "X-Title: Agentic Task Runner" \
  -d '{
    "model": "anthropic/claude-5.6-sonnet,openai/gpt-5.6,deepseek/deepseek-v4",
    "messages": [{"role": "user", "content": "Execute code analysis task."}],
    "temperature": 0.2
  }'
```

## API examples

### Python: OpenAI Client with Fallback Chain & Pydantic v2
Below is a Python example using the standard `openai` SDK directed to OpenRouter's endpoint. It demonstrates multi-model fallback chains and Pydantic v2 model response validation.

```python
import openai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

# 1. Define strict validation schema using Pydantic v2
class CodeAnalysisResult(BaseModel):
    summary: str = Field(..., description="High-level code audit summary")
    vulnerabilities_found: int = Field(..., ge=0, description="Count of identified vulnerabilities")
    severity_rating: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    recommended_patches: List[str] = Field(default_factory=list)
    model_used: Optional[str] = Field(None, description="Actual model that fulfilled request")

# 2. Initialize OpenAI client targeting OpenRouter base URL
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-your_openrouter_api_key_here"
)

def analyze_code_security(code_snippet: str) -> CodeAnalysisResult:
    # OpenRouter accepts comma-separated priority model lists for zero-downtime failover
    fallback_chain = "anthropic/claude-5.6-sonnet,openai/gpt-5.6,deepseek/deepseek-v4"

    response = client.beta.chat.completions.parse(
        model=fallback_chain,
        messages=[
            {"role": "system", "content": "You are a senior security engineer auditing code."},
            {"role": "user", "content": f"Audit this code for security issues:\n\n{code_snippet}"}
        ],
        response_format=CodeAnalysisResult,
        extra_headers={
            "HTTP-Referer": "https://my-ops.internal",
            "X-Title": "KnowledgeOps Security Auditor"
        }
    )

    parsed: CodeAnalysisResult = response.choices[0].message.parsed
    parsed.model_used = response.model
    return parsed

if __name__ == "__main__":
    sample_code = "def query_db(user_input):\n    return db.execute(f'SELECT * FROM users WHERE id = {user_input}')"
    try:
        result = analyze_code_security(sample_code)
        print(f"Model Utilized: {result.model_used}")
        print(f"Severity: {result.severity_rating} | Vulnerabilities: {result.vulnerabilities_found}")
        print(f"Summary: {result.summary}")
    except ValidationError as ve:
        print(f"Validation failed: {ve}")
```

### FastMCP 3.1 OpenRouter Tool Server
Below is a complete FastMCP 3.1 server implementation exposing OpenRouter model routing to downstream agent clients.

```python
import requests
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# 1. Initialize FastMCP 3.1 Server
mcp = FastMCP("OpenRouterGatewayServer", version="3.1.0")

# 2. Pydantic v2 Schemas for Tool Execution
class FastMCPRouterRequest(BaseModel):
    openrouter_api_key: str = Field(..., description="OpenRouter API key")
    prompt: str = Field(..., description="User query prompt")
    models: List[str] = Field(
        default=["anthropic/claude-5.6-sonnet", "openai/gpt-5.6", "deepseek/deepseek-v4"],
        description="Priority ordered model list"
    )
    temperature: float = Field(0.3, ge=0.0, le=2.0)

class RouterResponse(BaseModel):
    status: str
    fulfilled_model: str
    content: str
    prompt_tokens: int
    completion_tokens: int

# 3. FastMCP 3.1 Tool Definition
@mcp.tool()
def dispatch_openrouter_task(
    openrouter_api_key: str,
    prompt: str,
    model_chain: Optional[List[str]] = None,
    temperature: float = 0.3
) -> Dict[str, Any]:
    """Dispatch a prompt across OpenRouter's fallback chain with FastMCP 3.1 routing."""
    if not model_chain:
        model_chain = ["anthropic/claude-5.6-sonnet", "openai/gpt-5.6", "deepseek/deepseek-v4"]

    req_model = FastMCPRouterRequest(
        openrouter_api_key=openrouter_api_key,
        prompt=prompt,
        models=model_chain,
        temperature=temperature
    )

    headers = {
        "Authorization": f"Bearer {req_model.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://fastmcp.internal",
        "X-Title": "FastMCP 3.1 OpenRouter Gateway"
    }

    payload = {
        "model": ",".join(req_model.models),
        "messages": [{"role": "user", "content": req_model.prompt}],
        "temperature": req_model.temperature
    }

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        res.raise_for_status()
        data = res.json()

        choice = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        out = RouterResponse(
            status="success",
            fulfilled_model=data.get("model", "unknown"),
            content=choice,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0)
        )
        return out.model_dump()
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [OpenAI](openai.md) — Primary foundation model provider.
- [Claude](claude.md) — High-reasoning frontier models.
- [Gemini](gemini.md) — Long-context multimodal model series.
- [Local LLMs](local_llms.md) — Self-hosted open-weights models.
- [FastMCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Open protocol for agent tools.
- [LangChain](langchain.md) — Agent orchestration framework.

## Sources / references
- [OpenRouter Official Developer Documentation](https://openrouter.ai/docs)
- [OpenRouter API Reference and Model List](https://openrouter.ai/api/v1/models)
- [OpenRouter Rankings and Benchmarks](https://openrouter.ai/rankings)
- [Antling-30B-Flash on OpenRouter](https://www.reddit.com/r/LocalLLaMA/comments/1v4m5cr/antling30flash_is_now_live_on_openrouter_and_free/) — Antling-30B-Flash live on OpenRouter.

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
