# Cloudflare Agent Tracing

## What it is
**Cloudflare Agent Tracing** is an end-to-end observability and distributed tracing capability integrated into Cloudflare Workers AI and Workers platform. It enables real-time monitoring, prompt-response logging, execution timeline tracking, and latency profiling for multi-agent workflows running on edge infrastructure.

## What problem it solves
Multi-agent systems executing across serverless edge networks often suffer from "black box" execution failures, hidden token latency spikes, and complex tool call debugging across asynchronous nodes. Cloudflare Agent Tracing provides low-overhead, distributed telemetry using OpenTelemetry standards, allowing developers to inspect tool invokations, agent state transitions, and LLM API calls with sub-millisecond precision directly at the edge.

## Where it fits in the stack
**Category**: Process Understanding / AI Observability & Tracing. It sits at the **Telemetry & Observability Layer**, integrating with [OpenTelemetry Collector](opentelemetry-collector.md), [Datadog](datadog.md), and Cloudflare Workers AI pipelines to stream trace logs to central observability dashboards.

## Typical use cases
- **Multi-Agent Orchestration Debugging**: Tracking state handoffs between planning, execution, and verification agents in edge-hosted loops.
- **Token Cost & Latency Profiling**: Auditing token usage and execution bottlenecks across distributed Workers.
- **Tool Execution Auditing**: Logging external API payloads, database lookups, and MCP tool invocations with strict data privacy compliance.
- **Failover & Error Inspection**: Pinpointing unhandled exceptions or malformed JSON responses in multi-tier agent chains.

## Strengths
- **Native Edge Integration**: Zero-latency sidecar tracing running directly inside Cloudflare Workers runtime.
- **OpenTelemetry Standard Compliant**: Exportable to Grafana, Datadog, Langfuse, or custom OTLP endpoints.
- **Built-in Prompt & Tool Capture**: Automatically captures prompt context, tool parameters, and model completion metrics.
- **Global Distribution**: Observability collected across 300+ global edge locations without egress bottlenecks.

## Limitations
- **Platform Lock-In**: Deepest integrations require hosting agent runners within Cloudflare Workers or Cloudflare AI Gateway.
- **Storage Retention Limits**: High-volume traces require external exporter configuration for long-term retention.
- **Payload Redaction Complexity**: Strict PII masking requires custom configuration hooks prior to span exporting.

## When to use it
- When hosting AI agents or tool servers on Cloudflare Workers, AI Gateway, or edge serverless architecture.
- When requiring low-latency OpenTelemetry span generation for distributed multi-agent systems.
- When needing real-time visual inspection of agent reasoning steps on edge networks.

## When not to use it
- For monolithic on-premise agent deployments operating entirely offline or without edge network routes.
- When pure local file logging or desktop tracing tools (e.g., [Claude Desktop](../ai_knowledge/claude-desktop.md)) are sufficient.

## Getting started

### Installation
Install Cloudflare Wrangler and the tracing SDK:
```bash
npm install -g wrangler
npm install @cloudflare/agent-tracing @opentelemetry/api
```

### Configuration in wrangler.toml
Enable tracing in your Worker configuration:
```toml
name = "agent-tracing-worker"
main = "src/index.ts"
compatibility_date = "2026-01-01"

[vars]
OTEL_EXPORTER_OTLP_ENDPOINT = "https://telemetry.cloudflare.com/v1/traces"
```

## CLI examples

### Deploy Worker with Tracing Active
```bash
npx wrangler deploy --var ENVIRONMENT:production
```

### Tail Live Agent Tracing Logs
```bash
npx wrangler tail --format=json | grep "agent.trace"
```

## API examples

### TypeScript Agent Tracing Wrapper
The following snippet demonstrates wrapping an edge agent loop with Cloudflare Agent Tracing spans:

```typescript
import { trace, SpanStatusCode } from "@opentelemetry/api";

const tracer = trace.getTracer("cloudflare-agent-tracing");

export async function executeAgentTask(taskPrompt: string): Promise<{ status: string; result: string }> {
  return tracer.startActiveSpan("agent.execute_task", async (span) => {
    span.setAttribute("agent.prompt", taskPrompt);
    try {
      // Execute agent reasoning step
      const result = `Processed task: ${taskPrompt}`;
      span.setAttribute("agent.result", result);
      span.setStatus({ code: SpanStatusCode.OK });
      return { status: "success", result };
    } catch (err: any) {
      span.recordException(err);
      span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
      throw err;
    } finally {
      span.end();
    }
  });
}
```

### Python OTLP Trace Verification with Pydantic v2
Python validation script to parse exported agent trace payloads:

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TraceSpan(BaseModel):
    trace_id: str = Field(..., description="Unique OpenTelemetry trace identifier")
    span_id: str = Field(..., description="Span identifier")
    name: str = Field(..., description="Name of the agent execution step")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Span attributes including prompts and model names")

class CloudflareAgentTracePayload(BaseModel):
    resource_spans: List[TraceSpan] = Field(..., description="List of recorded trace spans")

def validate_trace_event(raw_json: dict) -> CloudflareAgentTracePayload:
    return CloudflareAgentTracePayload.model_validate(raw_json)

if __name__ == "__main__":
    sample_trace = {
        "resource_spans": [
            {
                "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
                "span_id": "00f067aa0ba902b7",
                "name": "agent.tool_call.search",
                "attributes": {"tool_name": "google_search", "latency_ms": 42.5}
            }
        ]
    }
    validated = validate_trace_event(sample_trace)
    print(f"Validated Trace ID: {validated.resource_spans[0].trace_id}")
```

## Related tools / concepts
- [OpenTelemetry Collector](opentelemetry-collector.md)
- [Datadog](datadog.md)
- [Helicone](helicone.md)
- [Grafana Cloud](grafana-cloud.md)
- [Cloudflare Pages](../development_ops/cloudflare-pages.md)

## Sources / references
- [Cloudflare Agent Tracing News Announcement](https://www.infoq.com/news/2026/08/cloudflare-agent-tracing/)
- [Cloudflare Workers AI Documentation](https://developers.cloudflare.com/workers-ai/)
- [OpenTelemetry Specification](https://opentelemetry.io/docs/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
