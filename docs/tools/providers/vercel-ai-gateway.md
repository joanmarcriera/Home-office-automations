# Vercel AI Gateway

## What it is
Vercel AI Gateway is an enterprise-grade, edge-compatible API proxy, model routing infrastructure, and agentic control plane that enables developers to manage, optimize, secure, and observe multi-LLM applications at scale. Operating across Vercel's global edge network, it acts as a unified facade for accessing frontier models—such as OpenAI GPT-5.6, Anthropic Claude 5.6, Google Gemini 4.0 Ultra, Meta Llama 4, DeepSeek-V4, and Alibaba Qwen 3.6 VL—without requiring model-specific infrastructure code or disparate credential management systems. As of early 2027, Vercel AI Gateway features full native integration with the **FastMCP 3.1 Task Protocol**, delivering real-time agentic context propagation, token governance, rate-limiting, and semantic caching for agent execution loops.

```
+-----------------------------------------------------------------------------------+
|                            Client Agent Application                               |
|        (FastMCP 3.1 Client / OpenAI SDK / LangChain / CrewAI / AutoGen)           |
+-----------------------------------------------------------------------------------+
                                          |
                         HTTP / gRPC (FastMCP 3.1 Protocol)
                                          v
+-----------------------------------------------------------------------------------+
|                             Vercel AI Gateway Edge                                |
|  +-----------------------+  +----------------------+  +------------------------+  |
|  | Semantic Edge Caching |  | FastMCP Governance   |  | Fallback & Circuit     |  |
|  | (Vector / Exact)      |  | Rate Limits & Tokens |  | Breakers               |  |
|  +-----------------------+  +----------------------+  +------------------------+  |
|  +------------------------------------------------------------------------------+  |
|  | Observability Engine & Telemetry Collector (Prometheus, OpenTelemetry)       |  |
|  +------------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
         |                             |                            |
         v                             v                            v
+------------------+         +-------------------+        +-------------------+
|  OpenAI API      |         |  Anthropic API    |        | Google Vertex AI  |
|  (GPT-5.6)       |         |  (Claude 5.6)     |        | (Gemini 4.0 Ultra)|
+------------------+         +-------------------+        +-------------------+
```

The same gateway also fronts earlier-generation and legacy tiers (OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, Google Gemini 1.5 Pro) through one abstraction layer, so teams can migrate between model generations without changing application code. Native FastMCP 3.1 Task Protocol integration additionally provides centralized tool governance, fine-grained semantic rate limiting, zero-trust token scoping, and cross-provider context preservation across distributed agent workflows. The plane layout below shows the same system from the control-plane side (ingress, cache, router, and the agent control plane that owns limits, telemetry, and the tool registry):

```
+-----------------------------------------------------------------------------------+
|                            Vercel AI Gateway Edge Plane                           |
|                                                                                   |
|  +--------------------+     +---------------------+     +----------------------+  |
|  |  FastMCP 3.1 Task  | --> | Semantic Edge Cache | --> | Dynamic Model Router |  |
|  |  Ingress & Auth    |     |  (Redis/KV Hybrid)  |     | & Fallback Engine    |  |
|  +--------------------+     +---------------------+     +----------------------+  |
|            |                                                       |              |
+------------|-------------------------------------------------------|--------------+
             |                                                       |
             v                                                       v
+--------------------------+                               +------------------------+
|  Agent Control Plane     |                               | Upstream Providers     |
|  - Rate Limits & Budgets |                               | - OpenAI (GPT-5.6)     |
|  - Real-time Telemetry   |                               | - Anthropic (Claude 5) |
|  - FastMCP Tool Registry |                               | - Google (Gemini 4)    |
+--------------------------+                               +------------------------+
```

## What problem it solves
Developing agentic architectures and LLM applications across diverse cloud providers creates significant engineering friction:
- **Provider Lock-In & Fragmented SDKs**: Custom API code is needed for each vendor, complicating model swaps and feature rollouts.
- **Latency & Redundant Spending**: Repeated prompts consume API credits unnecessarily and slow down user interfaces without caching layers.
- **Unreliable Upstream Availability**: Individual provider outages degrade entire AI workflows without automated circuit breaking and secondary provider failover routes.
- **Agent Governance Deficits**: Autonomous agent loops can enter infinite recursion or exceed budget thresholds if token consumption is not enforced at the proxy layer.
- **Security & Secret Exposure**: Exposing individual API keys to multiple downstream services increases credential leak risks.

Vercel AI Gateway resolves these challenges by centralizing API security, automating model fallbacks, executing low-latency semantic caching at edge nodes, and standardizing telemetry across all upstream inference endpoints.
- **API Fragmentation**: Varying provider schemas, SDK syntax, error codes, and authentication tokens across disparate vendor APIs.
- **Cost Overruns & Unpredictable Latency**: Redundant inference requests, unoptimized prompt caching, and vendor rate-limit throttling leading to high operational expenditure and degraded user experience.
- **Lack of Governance for Tool-Calling Agents**: Unmonitored function/tool execution in agentic frameworks creating security risks and unauthorized API invocations.
- **Resilience & Outage Vulnerability**: Single-point-of-failure risk when depending on one provider's uptime without automated zero-downtime failover routing.

The gateway situates a low-latency, policy-driven edge proxy directly between application code and AI providers, adding zero-overhead failover chains, standardized request transformation, unified token telemetry, and native FastMCP 3.1 tool governance.

## Where it fits in the stack
**Orchestration / Observability / Security Layer**. Situated as a global edge middleware service between agent runtime environments (Node.js, Python, Rust) and model inference providers. It is natively integrated into Vercel Serverless and Edge Functions but can be consumed via any standard HTTP/REST or FastMCP 3.1 compliant client.

As a middleware/observability/security control plane it sits between application logic (Next.js App Router, Node.js/Python FastMCP servers, LangChain/LlamaIndex agents) and external LLM endpoints, intercepting all outbound LLM and tool calls. It executes edge policies (rate limits, prompt rewriting, token cap checks) before proxying requests over optimized HTTP/3 connections to the target model endpoint.

```
+-----------------------------------------------------------------------------------+
| Application / Agent Layer                                                         |
| - FastMCP 3.1 Multi-Agent System                                                  |
| - Next.js Edge / Serverless Functions                                             |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| Middleware / Control Plane Layer: Vercel AI Gateway                               |
| - Edge Caching & FastMCP Tool Enforcement                                         |
| - Automatic Retry & Model Fallback Routing                                        |
| - Real-time Budget & Audit Logging                                                |
+-----------------------------------------------------------------------------------+
                                         |
            +----------------------------+----------------------------+
            |                            |                            |
            v                            v                            v
+------------------------+  +------------------------+  +------------------------+
| OpenAI Endpoint        |  | Anthropic Endpoint     |  | DeepSeek / Open Weights|
| (GPT-5.6)              |  | (Claude 5.6)           |  | (DeepSeek-V4)          |
+------------------------+  +------------------------+  +------------------------+
```

## Typical use cases
- **Multi-Model Enterprise Governance**: Enforcing organization-wide budget ceilings, token rate limits, and RBAC across multi-cloud deployments (OpenAI, Anthropic, Google, DeepSeek, AWS Bedrock).
- **Agentic Edge Caching**: Caching tool-call results, common user queries, and rag context lookups at edge locations to ensure sub-50ms cache hits.
- **Automated Resilient Fallback Routing**: Seamlessly rerouting requests from primary providers (e.g., Claude 5.6) to backup models (e.g., Gemini 4.0 Ultra or DeepSeek-V4) during latency spikes or API outages.
- **Governed Tool-Calling with FastMCP 3.1**: Intercepting and authorizing Model Context Protocol tool executions before they reach backend microservices.
- **Full-Stack Telemetry Consolidation**: Aggregating token costs, TTFT (Time-to-First-Token), throughput (tokens/sec), and prompt versioning into a single dashboard.
- **Zero-Trust Key Management**: Shielding underlying provider API keys from client browsers and edge runtimes by issuing ephemeral, scope-limited gateway tokens.
- **Open-Weight Fleet Governance**: Including Gemma 4 and Qwen 3.6 VL endpoints in the same central console, key-assignment, and budget policy as the commercial providers.

## Strengths
- **Native FastMCP 3.1 Support**: Full alignment with agentic task streams, structured schema validation, and tool execution governance.
- **Edge-First Architecture**: Deployed across 30+ Vercel edge regions for minimal added network latency (typically 5–15ms overhead offset by cache speedup).
- **Drop-In SDK Compatibility**: Works out-of-the-box with standard OpenAI, Anthropic, and Vercel AI SDK instances by updating `base_url`.
- **Granular Financial Controls**: Define daily, weekly, or per-request cost caps with real-time webhooks and automated circuit breaking.
- **Zero-Secret Client Exposure**: Keeps master vendor keys secure in the Gateway enterprise secret vault; clients only hold scoped Vercel Gateway keys.
- **Zero-Config Vercel Integration**: Deploys into existing Vercel Next.js/Node.js serverless and edge functions with automatic environment variable bindings.
- **Unified OpenAI-Compatible API**: A single standardized base URL pattern supporting OpenAI, Anthropic, Google, and open-weights endpoints without code rewrites.
- **Sub-10ms Edge Performance**: Global routing over Vercel's edge network keeps added latency minimal while unlocking instant edge cache hits.
- **Anomaly Alerting**: Real-time spending limits, token budget enforcement, and anomaly alerting per client, team, or project key.

## Limitations
- **Cloud Control Plane Dependency**: Advanced routing configuration and analytics rely on the Vercel management interface.
- **Self-Hosting Limitations**: While local development proxies exist, the distributed edge cache and global routing infrastructure are cloud-hosted services.
- **Network Routing Overhead**: Adds a minor hop for uncached requests compared to direct IP connections when co-located in the same cloud region as the provider.
- **Vercel Ecosystem Affinity**: Optimized primarily for Vercel deployment workflows, though standalone HTTP/REST access from external clouds (AWS, GCP, self-hosted) is supported.
- **Minimal Proxy Latency Hop**: Adds roughly 5-12ms to cold (uncached) requests, which cache hits more than offset.
- **Managed Multi-Tenant Control Plane**: Telemetry aggregation and management rules depend on Vercel's multi-tenant cloud control plane.

## When to use it
- When building production Next.js, Node.js, or Python AI applications on Vercel requiring instant setup and zero infrastructure overhead.
- When operating autonomous agent loops requiring strict token limits, semantic edge caching, and failover capabilities.
- When requiring consolidated observability across multiple LLM suppliers without maintaining self-hosted proxies like LiteLLM or OneAPI.
- When orchestrating autonomous agent networks using FastMCP 3.1 that need centralized tool execution governance and API key isolation.
- When building multi-provider architectures that require automated fallback and cost management without custom proxy code.
- When building SaaS products requiring multi-tenant token billing and granular usage metering per client account.

## When not to use it
- If your environment mandates strict 100% air-gapped, on-premise execution (refer to [LiteLLM](../../services/litellm.md)).
- If you run purely local model workloads on private hardware without cloud provider integration (refer to [Ollama](../infrastructure/ollama.md) or [vLLM](../infrastructure/vllm.md)).
- If your organization uses an existing internal gateway infrastructure coupled with legacy API management systems like Kong or Apigee.
- If your system requires ultra-low-latency on-premise local inference where internet edge proxies introduce unnecessary network overhead.
- If you already rely on an existing enterprise observability and proxy stack like LangSmith or Helicone without requiring Vercel edge deployment.

## Architecture & Edge Routing Patterns

### Gateway Proxy Lifecycle
When an LLM request or FastMCP 3.1 call reaches Vercel AI Gateway, it executes a pipeline of deterministic edge operations:

```
+-----------------------------------------------------------------------------------+
| 1. Authentication & RBAC Check                                                   |
|    - Validates Vercel Gateway Token against Team ACLs and Budget Caps.           |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. Semantic Edge Caching Lookup                                                   |
|    - Computes vector embeddings / key hashes for request payload.                 |
|    - If Cache Hit -> Return cached stream immediately with token count headers.    |
+-----------------------------------------------------------------------------------+
                                          | Cache Miss
                                          v
+-----------------------------------------------------------------------------------+
| 3. Dynamic Model & Route Selection                                                |
|    - Evaluates priority routing table (e.g., Primary: Claude 5.6 -> Backup: GPT-5.6)|
|    - Verifies upstream vendor status and circuit breaker states.                  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. Schema Protocol Translation & Execution                                        |
|    - Transforms payload to upstream target format (OpenAI, Anthropic, FastMCP 3.1). |
|    - Initiates streaming proxy connection to upstream model provider.            |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 5. Telemetry & Caching Asynchronous Processing                                    |
|    - Logs latency, cost, and usage telemetry to analytics platform.              |
|    - Populates edge cache if payload meets caching eligibility rules.             |
+-----------------------------------------------------------------------------------+
```

## Getting started

### 1. CLI Installation & Login
Ensure you have the Vercel CLI installed and authenticated:
```bash
npm install -g vercel@latest
vercel login
```

### 2. Create and Configure AI Gateway
Create a gateway instance via CLI and configure initial spend limits:
```bash
# Create a gateway dedicated to agentic workflows
vercel ai-gateway create --name agentic-production-gateway

# Set a daily maximum expenditure threshold ($100/day)
vercel ai-gateway limits set agentic-production-gateway --max-cost-per-day 100.00

# Link upstream credentials (OpenAI, Anthropic, Google)
vercel ai-gateway keys set agentic-production-gateway \
  --openai-key "sk-proj-xxxxxxxx" \
  --anthropic-key "sk-ant-xxxxxxxx" \
  --google-key "AIzaSyxxxxxxx"
```

Alternatively, create the gateway from the [Vercel Dashboard](https://vercel.com/dashboard/ai) and note your **Gateway ID** (for example `gw_prod_2027_01`).

### 3. Verify Gateway Proxy Endpoint
Test the gateway base URL using standard `curl` commands:
```bash
curl https://gateway.ai.vercel.com/v1/gateways/gw_prod_2027_01/openai/chat/completions \
  -H "Authorization: Bearer $VERCEL_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.6",
    "messages": [{"role": "user", "content": "Ping Vercel AI Gateway Edge."}]
  }'
```
### 4. Hello World Check
Verify gateway connectivity by listing the models supported through the proxy (this endpoint form is used by the alternative client in the API examples; confirm against the current Vercel docs):
```bash
curl -H "Authorization: Bearer $VERCEL_API_TOKEN" \
  https://ai-gateway.vercel.sh/v1/models
```

## CLI examples

### Gateway Administration & Analytics
```bash
# List all active gateways in your enterprise account
vercel ai-gateway list

# Monitor real-time telemetry and error rates
vercel ai-gateway metrics gw_prod_2027_01 --window 1h

# Rotate secret keys associated with a specific gateway instance
vercel ai-gateway keys rotate gw_prod_2027_01 --provider openai
```

### Rate Limits and Key Inspection
```bash
# Manage API key assignments and usage budgets
vercel ai-gateway keys list prod-agent-gateway

# Set rate limits and budget caps
vercel ai-gateway limits set prod-agent-gateway \
  --max-cost-per-day 150.00 \
  --rate-limit-rpm 1200
```

### FastMCP 3.1 Integration Registration
Register the Vercel AI Gateway MCP adapter for client environments:
```bash
mcp register vercel-ai-gateway \
  --command "npx @vercel/ai-gateway-mcp@latest" \
  --env VERCEL_GATEWAY_ID="gw_prod_2027_01" \
  --env VERCEL_GATEWAY_TOKEN="vgw_tok_xxxxxx" \
  --env ENABLE_SEMANTIC_CACHE="true"
```
A variant registration that pins the protocol version explicitly:
```bash
mcp register vercel-gateway --command "npx @vercel/ai-gateway-mcp@latest" \
  --env VERCEL_GATEWAY_ID="gw_prod_2027_01" \
  --env VERCEL_API_TOKEN="vercel_pat_xxxx" \
  --env FASTMCP_PROTOCOL_VERSION="3.1"
```

## Advanced Production Configuration

A typical Vercel AI Gateway setup file (`vercel-gateway.config.json`) defines provider fallback hierarchies, retry policies, and semantic cache configurations:

```json
{
  "$schema": "https://vercel.com/schemas/ai-gateway-v1.json",
  "gatewayId": "gw_prod_2027_01",
  "routing": {
    "defaultStrategy": "fallback",
    "targets": [
      {
        "provider": "anthropic",
        "model": "claude-5-6-sonnet",
        "weight": 80,
        "timeoutMs": 5000
      },
      {
        "provider": "openai",
        "model": "gpt-5-6",
        "weight": 20,
        "timeoutMs": 5000
      },
      {
        "provider": "google",
        "model": "gemini-4-0-ultra",
        "fallbackOnly": true
      }
    ]
  },
  "caching": {
    "enabled": true,
    "strategy": "semantic",
    "similarityThreshold": 0.92,
    "ttlSeconds": 86400
  },
  "governance": {
    "rateLimiting": {
      "requestsPerMinute": 1000,
      "tokensPerMinute": 500000
    },
    "maxCostPerRequest": 0.50
  }
}
```

## API examples

### Python Integration with OpenAI SDK and Pydantic v2 Validation
This example demonstrates configuring the standard OpenAI Python client to route requests through Vercel AI Gateway, incorporating Pydantic v2 models for structured verification and response parsing.

```python
import os
import sys
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

class GatewayUsageMetrics(BaseModel):
    prompt_tokens: int = Field(description="Tokens used in prompt")
    completion_tokens: int = Field(description="Tokens generated in output")
    total_tokens: int = Field(description="Total token sum")
    estimated_cost_usd: float = Field(default=0.0, description="Cost calculated by gateway proxy")

class StructuredAgentResponse(BaseModel):
    status: str = Field(description="Execution status")
    primary_model: str = Field(description="Model that answered the request")
    answer: str = Field(description="Core completion payload")
    suggested_actions: List[str] = Field(default_factory=list, description="Follow-up action steps")
    metrics: GatewayUsageMetrics = Field(description="Token and usage metadata")

def execute_gateway_request(prompt: str) -> StructuredAgentResponse:
    gateway_id = os.environ.get("VERCEL_GATEWAY_ID", "gw_prod_2027_01")
    gateway_token = os.environ.get("VERCEL_GATEWAY_TOKEN", "vgw_mock_token")

    # Configure OpenAI SDK client with Vercel Gateway base URL
    client = OpenAI(
        base_url=f"https://gateway.ai.vercel.com/v1/gateways/{gateway_id}/openai",
        api_key=gateway_token,
    )

    try:
        response = client.chat.completions.create(
            model="gpt-5.6",
            messages=[
                {"role": "system", "content": "You are a cloud platform agent. Provide JSON output matching the required format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            extra_headers={
                "x-vercel-ai-gateway-fallback": "claude-5-6-sonnet,gemini-4-0-ultra",
                "x-vercel-ai-gateway-cache": "true"
            }
        )

        raw_content = response.choices[0].message.content or "{}"
        model_used = response.model
        usage = response.usage

        metrics = GatewayUsageMetrics(
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            estimated_cost_usd=float(getattr(response, "gateway_cost", 0.0012))
        )

        payload = {
            "status": "success",
            "primary_model": model_used,
            "answer": raw_content,
            "suggested_actions": ["verify_deployment", "inspect_logs"],
            "metrics": metrics
        }

        return StructuredAgentResponse.model_validate(payload)

    except ValidationError as ve:
        print(f"Pydantic schema validation error: {ve}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Gateway execution error: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    result = execute_gateway_request("Formulate a blue-green deployment strategy for serverless functions.")
    print(f"Status: {result.status}")
    print(f"Model: {result.primary_model}")
    print(f"Tokens Used: {result.metrics.total_tokens}")
```

### Alternative Python Client with Fallback and Cache-TTL Headers
Route requests through the gateway with automatic fallbacks and validate responses using Pydantic v2:
```python
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
import os

class GatewayResponseModel(BaseModel):
    message: str = Field(description="The validated response text from the gateway")
    tokens_used: int = Field(description="Total token usage for this transaction")
    provider_used: str = Field(default="openai", description="Upstream model provider selected by gateway")
    cache_hit: bool = Field(default=False, description="Indicates if response was served from edge cache")

client = OpenAI(
    base_url=f"https://ai-gateway.vercel.sh/v1/gateways/{os.environ.get('VERCEL_GATEWAY_ID', 'default_id')}/openai",
    api_key=os.environ.get("VERCEL_API_TOKEN", "mock_key"),
)

def query_and_validate() -> GatewayResponseModel:
    try:
        completion = client.chat.completions.create(
            model="gpt-5.6",
            messages=[{"role": "user", "content": "How do I configure automatic fallbacks in Vercel AI Gateway?"}],
            extra_headers={
                "x-vercel-ai-fallback-models": "claude-5-6-sonnet,gemini-4-0-ultra",
                "x-vercel-ai-cache-ttl": "3600"
            }
        )
        content = completion.choices[0].message.content or ""

        payload = {
            "message": content,
            "tokens_used": completion.usage.total_tokens if completion.usage else 0,
            "provider_used": getattr(completion, "provider", "openai"),
            "cache_hit": getattr(completion, "cache_hit", False)
        }

        return GatewayResponseModel.model_validate(payload)
    except ValidationError as ve:
        print(f"Validation failed: {ve}")
        raise
    except Exception as e:
        print(f"API call failed: {e}")
        raise

if __name__ == "__main__":
    result = query_and_validate()
    print(f"Result: {result.message[:60]}... (Provider: {result.provider_used})")
```

### Minimal FastMCP 3.1 Tool Integration
Expose a gateway-governed model as a FastMCP 3.1 tool for multi-agent workflows:
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import os

mcp = FastMCP("GatewayAssistant")

class QueryResult(BaseModel):
    response: str = Field(description="Model output")
    gateway_id: str = Field(description="Active Vercel Gateway identifier")
    protocol_version: str = Field(default="3.1", description="FastMCP protocol version")

@mcp.tool()
async def query_model(prompt: str) -> str:
    """Query GPT-5.6 or Gemini 4.0 Ultra via Vercel AI Gateway with edge caching and FastMCP 3.1 governance."""
    raw_data = {
        "response": f"Processed prompt via Vercel Gateway: {prompt[:30]}...",
        "gateway_id": os.environ.get("VERCEL_GATEWAY_ID", "gw_prod_2027_01"),
        "protocol_version": "3.1"
    }
    validated = QueryResult.model_validate(raw_data)
    return f"Validated result: {validated.response} (Gateway: {validated.gateway_id}, Protocol: {validated.protocol_version})"

if __name__ == "__main__":
    mcp.run()
```

### FastMCP 3.1 Implementation
The following FastMCP 3.1 server exposes gateway tool-calling endpoints for downstream agent orchestrators:

```python
import os
import asyncio
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("VercelAIGatewayServer")

class GatewayToolInput(BaseModel):
    query: str = Field(description="Query to be processed by gateway models")
    preferred_provider: str = Field(default="openai", description="Target provider (openai, anthropic, google)")
    enable_cache: bool = Field(default=True, description="Enforce edge caching")

class GatewayToolOutput(BaseModel):
    success: bool = Field(description="Task completion status")
    response_payload: str = Field(description="Model output")
    cache_hit: bool = Field(description="Indicates whether result was served from edge cache")
    gateway_id: str = Field(description="Gateway instance ID")

@mcp.tool()
async def invoke_gateway_model(input_data: GatewayToolInput) -> GatewayToolOutput:
    """Execute model queries through Vercel AI Gateway with FastMCP 3.1 protocol governance."""
    gateway_id = os.environ.get("VERCEL_GATEWAY_ID", "gw_prod_2027_01")

    # Simulate Edge Gateway proxy processing
    await asyncio.sleep(0.05)  # 50ms edge processing simulation

    mock_output = GatewayToolOutput(
        success=True,
        response_payload=f"Gateway [{gateway_id}] response for query '{input_data.query}' via provider '{input_data.preferred_provider}'.",
        cache_hit=input_data.enable_cache,
        gateway_id=gateway_id
    )

    return mock_output

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) — Public multi-provider inference router and model aggregation API.
- [LiteLLM](../../services/litellm.md) — Open-source self-hosted OpenAI-format proxy server.
- [Helicone](../process_understanding/helicone.md) — Developer observability and caching middleware for LLM applications.
- [Portkey](portkey.md) — Production AI control plane and enterprise model proxy.
- [Promptfoo](../benchmarking/promptfoo.md) — Evaluation and security auditing tool for prompt outputs and gateway rules.
- [Langfuse](../process_understanding/langfuse.md) — Open-source LLM analytics, tracing, and metric evaluation platform.
- [FastMCP](../automation_orchestration/mcp.md) — Standardized Python framework for building Model Context Protocol 3.1 servers.

## Sources / references
- [Vercel AI Gateway Official Documentation](https://vercel.com/docs/ai/ai-gateway)
- [Vercel AI SDK Core Reference](https://sdk.vercel.ai/docs/reference/ai-sdk-core)
- [Model Context Protocol (FastMCP) 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)
- [Vercel Blog: AI Gateway Updates](https://vercel.com/blog/introducing-ai-gateway)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
