# Grafana Tempo

## What it is
Grafana Tempo is an open-source, high-scale distributed tracing backend optimized for object storage (AWS S3, Google Cloud Storage, Azure Blob, MinIO). Designed to handle massive OTLP trace ingestion without requiring high-cost full-text search indices like Elasticsearch or OpenSearch, Tempo enables engineering teams to record, search, and analyze complex multi-service span traces across microservices and multi-agent AI swarms.

## What problem it solves
Distributed microservices and multi-agent AI execution loops generate millions of span events per hour. Indexing every attribute in a traditional trace database leads to excessive infrastructure storage costs and complex index management. Tempo resolves this by storing raw trace blocks directly in object storage while using **TraceQL**—a targeted query language—to search spans based on span attributes, execution durations, status codes, and custom agent telemetry tags.

## Where it fits in the stack
**Distributed Observability & Tracing**. Sits in the operational observability layer, ingesting OpenTelemetry traces from API gateways, agent orchestrators, vector search nodes, and background microservices. It integrates directly with Prometheus (metrics) and Grafana Loki (logs) to form the unified LGTM monitoring stack.

## Architecture Diagram
```
+-----------------------------------------------------------------------------------+
|                              Grafana Tempo Architecture                           |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | OpenTelemetry Collector / FastMCP 3.1 Agents (OTLP gRPC / HTTP Tracing)     |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Distributor Component (Load Balances & Validates Incoming OTLP Spans)        |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Ingester Component (Buffers Spans, Writes WAL, Packs Blocks)                |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Object Storage (AWS S3, MinIO, GCS - Long-Term Block Retention)               |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | TraceQL Query Frontend & Engine (Correlates Traces with Grafana UI)          |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Multi-Agent Swarm Tracing**: Tracking agentic workflows, multi-step sub-agent delegation, prompt construction latency, and tool execution call graphs.
- **Microservice Bottleneck Analysis**: Pinpointing long-tail latencies in distributed vector searches, database queries, and third-party API webhooks.
- **Error Root-Cause Analysis**: Isolating exact failure spans, exception stack traces, and status error codes during agent reasoning loops.
- **Token & Cost Allocation Tracing**: Injecting LLM token counts and cost attributes into span attributes to track per-user or per-workflow operational expenditure.

## Strengths
- **Cost Efficiency**: Massive storage savings by utilizing cheap object storage instead of indexed database clusters.
- **High Ingestion Scale**: Microservice architecture designed to handle millions of incoming trace spans per second.
- **LGTM Ecosystem Synergy**: One-click correlation between Loki logs, Prometheus metrics, and Tempo traces within Grafana.
- **TraceQL Engine**: Expressive query language allowing deep filtering by duration, status, resource attributes, and custom tags.

## Limitations
- **Cold Storage Query Latency**: Searching unindexed historical blocks across vast time ranges can require scanning object storage files.
- **Compactor Management**: Requires configuring and running Tempo Compactor instances to handle block merging and retention policies.

## When to use it
- When operating microservices or agent swarms instrumented with OpenTelemetry.
- When requiring cost-effective distributed tracing at scale without managing Elasticsearch/OpenSearch clusters.
- When using Grafana and Prometheus as primary operational dashboards.

## When not to use it
- For basic single-process applications where simple console logging suffices.
- When operating in environments lacking S3-compatible object storage.

## Getting started

### Installation via Helm
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install tempo grafana/tempo-distributed
```

### Basic Docker Compose Setup
```yaml
version: '3.8'
services:
  tempo:
    image: grafana/tempo:latest
    command: [ "-config.file=/etc/tempo.yaml" ]
    volumes:
      - ./tempo.yaml:/etc/tempo.yaml
    ports:
      - "4317:4317" # OTLP gRPC
      - "4318:4318" # OTLP HTTP
      - "3200:3200" # Tempo HTTP Port
```

## CLI examples
```bash
# Query Tempo health status endpoint
curl http://localhost:3200/ready

# Search traces via Tempo API using TraceQL
curl -G http://localhost:3200/api/search \
  --data-urlencode 'q={ .status = error }'
```

## API examples
The following complete Python script demonstrates emitting OpenTelemetry trace spans destined for Grafana Tempo, capturing FastMCP 3.1 tool execution details, and validating span metadata with Pydantic v2:

```python
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# 1. Initialize OpenTelemetry Tracer
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("fastmcp.tempo.tracer", "3.1")

# 2. Define Pydantic v2 Trace Telemetry Model
class AgentTraceSpanSchema(BaseModel):
    workflow_id: str = Field(..., description="Unique workflow identifier")
    agent_role: str = Field(..., description="Role executing the step")
    mcp_tool_name: str = Field(..., description="Name of FastMCP 3.1 tool invoked")
    execution_duration_ms: float = Field(..., ge=0.0, description="Duration in milliseconds")
    status_code: str = Field(..., description="Span status: 'OK' or 'ERROR'")
    token_count: Optional[int] = Field(default=0, ge=0)

    @field_validator("status_code")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"OK", "ERROR"}
        if v.upper() not in allowed:
            raise ValueError(f"status_code must be one of {allowed}")
        return v.upper()

# 3. Emit Trace Function
def trace_mcp_tool_execution(payload: Dict[str, Any]) -> None:
    """Validate trace payload and record an OpenTelemetry span destined for Tempo."""
    validated_span = AgentTraceSpanSchema.model_validate(payload)

    with tracer.start_as_current_span(f"FastMCP Tool: {validated_span.mcp_tool_name}") as span:
        # Inject standard OpenTelemetry & Tempo trace attributes
        span.set_attribute("workflow.id", validated_span.workflow_id)
        span.set_attribute("agent.role", validated_span.agent_role)
        span.set_attribute("mcp.tool", validated_span.mcp_tool_name)
        span.set_attribute("execution.duration_ms", validated_span.execution_duration_ms)
        span.set_attribute("llm.total_tokens", validated_span.token_count or 0)

        if validated_span.status_code == "ERROR":
            span.set_status(trace.StatusCode.ERROR, "Tool execution failed")
        else:
            span.set_status(trace.StatusCode.OK)

        time.sleep(min(validated_span.execution_duration_ms / 1000.0, 0.1))

if __name__ == "__main__":
    sample_trace = {
        "workflow_id": "wf-tempo-99120",
        "agent_role": "DataCopilot",
        "mcp_tool_name": "query_vector_store",
        "execution_duration_ms": 145.2,
        "status_code": "OK",
        "token_count": 850
    }

    print("Emitting trace span to OpenTelemetry / Tempo exporter...")
    trace_mcp_tool_execution(sample_trace)
    print("Trace span recorded successfully.")
```

## Related tools / concepts
- [Grafana Cloud](grafana-cloud.md) — Unified visualization dashboard for Tempo, Loki, and Prometheus.
- [OpenTelemetry Collector](opentelemetry-collector.md) — Telemetry gateway forwarding OTLP traces to Tempo.
- [Logfire](logfire.md) — Python observability framework supporting OTLP output.
- [Loki](loki.md) — Log aggregation engine correlated with Tempo traces.

## Sources / references
- [Grafana Tempo Official Documentation](https://grafana.com/docs/tempo/latest/)
- [Grafana Tempo GitHub Repository](https://github.com/grafana/tempo)
- [TraceQL Language Reference](https://grafana.com/docs/tempo/latest/traceql/)
- [OpenTelemetry Python SDK](https://opentelemetry.io/docs/languages/python/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
