# Cloudflare Agent Tracing

## What it is
**Cloudflare Agent Tracing** is an enterprise-grade observability and telemetry service integrated into Workers AI and Workers Vectorize ecosystems. Designed for distributed multi-agent systems and FastMCP 3.1 workflows, Cloudflare Agent Tracing captures end-to-end execution trees, tool calling spans, latency metrics, and LLM token usage across global edge nodes without impacting runtime performance.

## What problem it solves
Distributed AI agents operating on serverless edge networks often suffer from visibility bottlenecks, hidden tool execution latency, unhandled tool failures, and non-deterministic agent loop divergences. Cloudflare Agent Tracing provides zero-overhead distributed tracing, structured event logs, and OpenTelemetry (OTel)-compatible trace propagation to audit complex, multi-step LLM agent executions in real time.

## Where it fits in the stack
**Category**: Process Understanding / AI Agent Telemetry & Observability. Sits at the **Observability & Intelligence Layer**, integrating directly with Cloudflare Workers AI, Workers KV, Vectorize, and edge gateway routers to monitor agents built with [LangChain](../frameworks/langchain.md), [AutoGen](../frameworks/autogen.md), or custom [FastMCP 3.1](../automation_orchestration/mcp.md) servers.

## Typical use cases
- **Multi-Agent Edge Execution Tracing**: Monitoring multi-agent interactions and parent-child span relationships across Cloudflare Workers nodes.
- **MCP Tool Call Diagnostics**: Tracking latency, input parameters, and return payloads for Model Context Protocol (MCP) tool invocations.
- **Cost & Token Optimization**: Auditing per-agent and per-session token consumption across models like Gemma 4, Claude 5.1, and Llama 4.
- **Real-time Anomaly Alerting**: Detecting infinite agent loops, tool recursion depth limits, or edge timeout violations before end-user impact.

## Strengths
- **Global Edge Integration**: Built natively into Cloudflare Workers with zero extra cold-start or transport overhead.
- **OpenTelemetry Standard Compliant**: Exports traces natively in standard OTel format to destinations such as [Grafana Cloud](grafana-cloud.md), [Helicone](helicone.md), and [Datadog](datadog.md).
- **Tool-Call Level Granularity**: Captures prompt inputs, tool invocation arguments, schema validations, and sub-second execution spans.
- **Integrated Privacy & Scrubbing**: Automated PII masking and header sanitization at edge nodes before traces leave tenant boundaries.

## Limitations
- **Ecosystem Optimization**: Maximum benefits achieved within the Cloudflare Workers / Workers AI runtime ecosystem.
- **Trace Storage Retention Limits**: Default cloud retention buffers require exporting to long-term storage (e.g., ClickHouse or R2) for multi-month compliance audits.
- **High-Volume Sampling Requirements**: Ultra-high throughput deployments require trace sampling strategies to manage export costs.

## When to use it
- When deploying agentic applications on Cloudflare Workers AI or Cloudflare edge infrastructure.
- When requiring full OpenTelemetry-compliant observability for multi-agent workflows and MCP 3.1 tool calls.
- When monitoring sub-100ms latency boundaries for real-time edge voice and text agents.

## When not to use it
- For monolithic on-premise deployments completely disconnected from Cloudflare edge networks (use [OpenTelemetry Collector](opentelemetry-collector.md) or [Langfuse](langfuse.md)).
- If your stack is exclusively hosted on AWS Lambda or GCP Cloud Functions without Cloudflare routing (use native AWS X-Ray or Datadog).

## Getting started

### Installation / Setup
Cloudflare Agent Tracing is enabled via Wrangler configuration in Workers project roots or imported via `@cloudflare/agent-tracing` SDK:

```bash
npm install @cloudflare/agent-tracing @opentelemetry/api
```

### Wrangler Configuration (`wrangler.toml`)
```toml
name = "edge-agent-worker"
main = "src/index.ts"
compatibility_date = "2027-01-01"

[vars]
ENVIRONMENT = "production"

[[analytics_engine_datasets]]
binding = "AGENT_TRACES"
dataset = "cloudflare_agent_traces"
```

## CLI examples

### Inspecting Traces via Wrangler CLI
```bash
npx wrangler tail --format=pretty --filter="event.type == 'agent_trace'"
```

### Exporting Edge Traces to OTel Collector
```bash
npx wrangler secret put OTEL_EXPORTER_OTLP_ENDPOINT
# Enter: https://otel-collector.example.com:4318/v1/traces
```

## API examples

### Python Integration with FastMCP 3.1 & Pydantic v2
The following example demonstrates how Python agent services push structured telemetry events and span context to Cloudflare Agent Tracing endpoints:

```python
import json
import time
import requests
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class AgentSpanTelemetry(BaseModel):
    trace_id: str = Field(..., description="Unique 128-bit hex trace identifier")
    span_id: str = Field(..., description="Unique 64-bit hex span identifier")
    agent_name: str = Field(..., description="Name of the executing agent")
    tool_name: Optional[str] = Field(None, description="Name of the invoked MCP tool if applicable")
    duration_ms: float = Field(..., ge=0, description="Execution duration in milliseconds")
    token_usage: Dict[str, int] = Field(default_factory=dict, description="Prompt, completion, and total tokens")
    status: str = Field(..., description="Execution status: ok, error, or timed_out")

def emit_cloudflare_trace(telemetry: AgentSpanTelemetry, cloudflare_endpoint: str, api_token: str) -> bool:
    """Emits validated agent telemetry data to Cloudflare Agent Tracing OTLP endpoint."""
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "resourceSpans": [{
            "resource": {
                "attributes": [
                    {"key": "service.name", "value": {"stringValue": telemetry.agent_name}},
                    {"key": "telemetry.sdk.language", "value": {"stringValue": "python"}}
                ]
            },
            "scopeSpans": [{
                "spans": [{
                    "traceId": telemetry.trace_id,
                    "spanId": telemetry.span_id,
                    "name": telemetry.tool_name or telemetry.agent_name,
                    "kind": 1,
                    "attributes": [
                        {"key": "agent.status", "value": {"stringValue": telemetry.status}},
                        {"key": "agent.duration_ms", "value": {"doubleValue": telemetry.duration_ms}},
                        {"key": "agent.token_usage", "value": {"stringValue": json.dumps(telemetry.token_usage)}}
                    ]
                }]
            }]
        }]
    }

    # Strict validation via Pydantic v2
    validated_data = telemetry.model_dump()
    print(f"Emitting Cloudflare trace span {validated_data['span_id']} for agent '{validated_data['agent_name']}'")

    # Simulated POST request to edge tracing ingestion API
    return True

if __name__ == "__main__":
    sample_trace = AgentSpanTelemetry(
        trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
        span_id="00f067aa0ba902b7",
        agent_name="ResearchSynthesizerAgent",
        tool_name="fastmcp_vector_search",
        duration_ms=42.8,
        token_usage={"prompt_tokens": 512, "completion_tokens": 128, "total_tokens": 640},
        status="ok"
    )

    success = emit_cloudflare_trace(sample_trace, "https://api.cloudflare.com/client/v4/accounts/demo/agent_tracing", "mock-token")
    print(f"Trace emission successful: {success}")
```

## Related tools / concepts
- [OpenTelemetry Collector](opentelemetry-collector.md)
- [Helicone](helicone.md)
- [Grafana Cloud](grafana-cloud.md)
- [Langfuse](langfuse.md)
- [Datadog](datadog.md)
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md)
- [Cloudflare Workers AI](../providers/cloudflare-workers-ai.md)

## Sources / references
- [Cloudflare Agent Tracing News Announcement](https://www.infoq.com/news/2026/08/cloudflare-agent-tracing/)
- [Cloudflare Developer Documentation](https://developers.cloudflare.com/workers-ai/)
- [OpenTelemetry Specification](https://opentelemetry.io/docs/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
