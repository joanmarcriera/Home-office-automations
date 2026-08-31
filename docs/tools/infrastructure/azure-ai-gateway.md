# Azure AI Gateway

## What it is
Azure AI Gateway is an enterprise API Management (APIM) tier designed to govern, secure, load-balance, rate-limit, and audit calls to LLMs, provider endpoints, and Model Context Protocol (FastMCP 3.1) servers. Operating inline at the ingress boundary, it manages credentials, tracks token expenditures, enforces PII data loss prevention rules, and handles dynamic multi-provider routing across models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4.

## What problem it solves
Deploying commercial generative AI introduces risks around API availability, provider throttling (HTTP 429), cost overruns, and data leakage. Azure AI Gateway addresses these by providing automated endpoint failover, token-aware rate limiting, real-time PII redaction, and centralized telemetry logging across enterprise multi-model deployments.

## Where it fits in the stack
**AI Infrastructure & Gateway Layer**. It sits between application clients/agent orchestrators and upstream model providers, securing API traffic and managing execution policies.

## Typical use cases
- **Multi-Provider Load Balancing**: Distributing prompt traffic across Azure OpenAI, Anthropic, and secondary endpoints to maximize throughput and resiliency.
- **Automated Fallback Routing**: Rerouting traffic from throttled or failing endpoints (e.g. failing over from GPT-5.6 to Claude 5.6 or DeepSeek-V4).
- **Token Budget Governance**: Applying user- and team-level token rate limits to manage cloud expenses.
- **FastMCP 3.1 Gateway Security**: Intercepting and validating outbound tool calls and agent resource access via FastMCP 3.1 protocols.

## Strengths
- **Enterprise Security Integration**: Native authentication with Microsoft Entra ID for role-based access control.
- **Sub-Millisecond Policy Overhead**: Low-latency XML/JSON policy enforcement for CORS, rate-limiting, and header injection.
- **Granular Token Telemetry**: Native tracking of prompt and completion tokens routed to Azure Monitor and OpenTelemetry receivers.
- **FastMCP 3.1 Governance**: Built-in inspection and security validation for MCP tool definitions and task payloads.

## Limitations
- **Azure Ecosystem Lock-In**: Requires an active Azure API Management subscription, making air-gapped home-lab deployments non-viable.
- **Policy Configuration Overhead**: Designing multi-backend failover rules requires specialized APIM XML/JSON policy syntax.

## When to use it
- When managing enterprise LLM applications requiring multi-region failover and strict compliance auditing.
- For enforcing token quotas and PII scrubbing across multi-team AI initiatives.
- When securing FastMCP 3.1 agent tool execution boundaries in Azure cloud environments.

## When not to use it
- For self-hosted or air-gapped home labs running local runtimes (Ollama, llama.cpp, LocalAI).
- For single-model prototypes where API gateway management adds unnecessary configuration overhead.

## Getting started
1. **Provision Gateway**: Deploy Azure API Management selecting the AI Gateway tier.
2. **Configure Upstream Backends**: Register provider keys in Key Vault and reference them in APIM backends.
3. **Apply Load Balancing Policy**:
   ```xml
   <policies>
       <inbound>
           <base />
           <llm-load-balancer>
               <backend id="openai-primary" weight="70" />
               <backend id="claude-fallback" weight="30" />
           </llm-load-balancer>
       </inbound>
   </policies>
   ```

## CLI examples

```bash
# Register an API backend inside Azure AI Gateway
az apim api register-backend --resource-group "rg-ai" --service-name "ai-gateway" --backend-id "openai-primary" --url "https://api.openai.com/v1" --key "sk-..."

# Apply token rate-limiting policy
az apim api policy apply --resource-group "rg-ai" --service-name "ai-gateway" --api-id "llm-api" --policy-file "./policies/token-rate-limit.xml"
```

## API examples

### Python AI Gateway Telemetry Ingestion & Pydantic v2 Validation
This example demonstrates fetching and parsing token usage metrics from Azure AI Gateway logs, strictly validating the structure using **Pydantic v2** for FastMCP 3.1 governance reporting.

```python
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

class GatewayUsageMetrics(BaseModel):
    prompt_tokens: int = Field(..., alias="promptTokens", ge=0, description="Prompt token count")
    completion_tokens: int = Field(..., alias="completionTokens", ge=0, description="Completion token count")
    total_tokens: int = Field(..., alias="totalTokens", ge=0, description="Total token consumption")
    latency_ms: float = Field(..., alias="latencyMs", gt=0.0, description="Round-trip latency in ms")

class GatewayLogResponse(BaseModel):
    gateway_id: str = Field(..., alias="gatewayId", description="APIM instance identifier")
    client_app_id: str = Field(..., alias="clientAppId", description="Requestor application ID")
    routing_decision: str = Field(..., alias="routingDecision", description="Selected backend endpoint")
    mcp_protocol_version: str = Field(default="3.1", description="FastMCP protocol standard")
    usage: GatewayUsageMetrics = Field(..., description="Token usage metrics")

def parse_gateway_analytics(simulated_data: dict) -> Optional[GatewayLogResponse]:
    try:
        return GatewayLogResponse.model_validate(simulated_data)
    except ValidationError as ve:
        print(f"Pydantic validation error: {ve}")
        return None

if __name__ == "__main__":
    sample_log = {
        "gatewayId": "azure-apim-ai-westus-01",
        "clientAppId": "agent-runner-v5",
        "routingDecision": "claude-5.6-primary-endpoint",
        "mcpProtocolVersion": "3.1",
        "usage": {
            "promptTokens": 1280,
            "completionTokens": 640,
            "totalTokens": 1920,
            "latencyMs": 182.4
        }
    }

    parsed = parse_gateway_analytics(sample_log)
    if parsed:
        print("Azure AI Gateway Log Validated via Pydantic v2:")
        print(f"  Gateway: {parsed.gateway_id}")
        print(f"  App ID: {parsed.client_app_id}")
        print(f"  Route: {parsed.routing_decision}")
        print(f"  Total Tokens: {parsed.usage.total_tokens} ({parsed.usage.latency_ms} ms)")
        print(f"  FastMCP Version: {parsed.mcp_protocol_version}")
```

## Related tools / concepts
- [Azure OpenAI](../providers/azure-openai.md) — Enterprise OpenAI service hosted on Azure.
- [Vercel AI Gateway](../providers/vercel-ai-gateway.md) — Edge-hosted multi-provider API gateway.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol for agent tool and resource governance.

## Sources / references
- [Azure API Management AI Gateway Documentation](https://learn.microsoft.com/en-us/azure/api-management/)
- [Microsoft Azure APIM Policy Reference](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
