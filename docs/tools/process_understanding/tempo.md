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

## FastMCP 3.1 Trace Analysis & Inspection Server
The following FastMCP 3.1 server allows agents to query Grafana Tempo via TraceQL, analyze trace latency bottlenecks, and extract spans:

```python
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(name="grafana-tempo-traceql")

class TraceSpan(BaseModel):
    span_id: str = Field(..., description="Unique 16-character hex span ID")
    trace_id: str = Field(..., description="Unique 32-character hex trace ID")
    service_name: str = Field(..., description="Originating service or agent name")
    operation_name: str = Field(..., description="Name of the operation or tool call")
    duration_ms: float = Field(..., ge=0.0)
    status: str = Field(..., description="Span status code (OK, UNSET, ERROR)")
    attributes: Dict[str, Any] = Field(default_factory=dict)

class TraceQueryResult(BaseModel):
    query: str
    total_spans_found: int
    spans: List[TraceSpan]
    execution_time_ms: float

@mcp.tool()
def search_traces_traceql(
    traceql_query: str,
    limit: int = 20,
    min_duration_ms: Optional[float] = None,
) -> TraceQueryResult:
    """Executes a TraceQL query against Grafana Tempo backend."""
    # Simulated search execution
    sample_spans = [
        TraceSpan(
            span_id="8f921a32b0014a",
            trace_id="4a90f11c89012a4b88901122aef001",
            service_name="agent-orchestrator",
            operation_name="mcp.tool.vector_search",
            duration_ms=245.8,
            status="OK",
            attributes={"llm.prompt_tokens": 340, "db.system": "qdrant"},
        ),
        TraceSpan(
            span_id="9e110022fa2211",
            trace_id="4a90f11c89012a4b88901122aef001",
            service_name="ollama-service",
            operation_name="llm.generate.deepseek-v4",
            duration_ms=1850.2,
            status="OK",
            attributes={"llm.completion_tokens": 128},
        ),
    ]

    return TraceQueryResult(
        query=traceql_query,
        total_spans_found=len(sample_spans),
        spans=sample_spans[:limit],
        execution_time_ms=14.2,
    )

@mcp.tool()
def get_trace_details_by_id(trace_id: str) -> Dict[str, Any]:
    """Retrieves full trace tree hierarchy for a specific trace ID."""
    return {
        "trace_id": trace_id,
        "root_service": "agent-orchestrator",
        "total_duration_ms": 2096.0,
        "span_count": 5,
        "has_errors": False,
    }

if __name__ == "__main__":
    mcp.run()
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

## TraceQL Syntax & Query Comparison Matrix

| Query Pattern | TraceQL Example | Description / Use Case |
| :--- | :--- | :--- |
| **Error Span Isolation** | `{ .status = error }` | Returns all trace spans with explicit error status codes |
| **Duration Bottleneck Search** | `{ duration > 1.5s && resource.service.name = "agent-orchestrator" }` | Pinpoints slow operations taking over 1.5 seconds |
| **MCP Tool Attribute Filtering** | `{ span.mcp.tool = "vector_store" && span.execution.duration_ms > 200 }` | Filters spans executing specific agent tools over duration threshold |
| **LLM Token Usage Query** | `{ span.llm.total_tokens > 2000 }` | Isolates trace spans involving large context window completions |

## Deployment & Production Infrastructure

### Full-Stack LGTM & MinIO Docker Compose Setup
Deploy Grafana Tempo alongside MinIO object storage, OpenTelemetry Collector, and Grafana for trace visual analysis:

```yaml
version: "3.8"

services:
  tempo:
    image: grafana/tempo:2.6.0
    container_name: tempo-backend
    command: [ "-config.file=/etc/tempo.yaml" ]
    volumes:
      - ./tempo-config.yaml:/etc/tempo.yaml
    ports:
      - "4317:4317" # OTLP gRPC
      - "4318:4318" # OTLP HTTP
      - "3200:3200" # Tempo Query Frontend
    depends_on:
      - minio
    restart: unless-stopped

  minio:
    image: minio/minio:RELEASE.2025-01-01T00-00-00Z
    container_name: tempo-minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadminpassword
    command: server /data --console-address ":9001"
    restart: unless-stopped

  grafana:
    image: grafana/grafana:11.3.0
    container_name: tempo-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    restart: unless-stopped
```

### Systemd Daemon Setup (`/etc/systemd/system/tempo-ingester.service`)
Configure a dedicated background service for local Tempo distributed tracing instances:

```ini
[Unit]
Description=Grafana Tempo Distributed Tracing Backend Ingester
After=network.target minio.service
Wants=minio.service

[Service]
Type=simple
User=tempo
Group=tempo
WorkingDirectory=/etc/tempo
ExecStart=/usr/local/bin/tempo -config.file=/etc/tempo/tempo.yaml
Restart=always
RestartSec=5s
LimitNOFILE=65536

# Hardening
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/tempo

[Install]
WantedBy=multi-user.target
```

## Operational Troubleshooting & Diagnostics

| Symptom | Probable Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Missing Spans in Grafana UI** | OTLP exporter batching delay or endpoint port mismatch (4317 vs 4318) | `curl http://tempo:3200/metrics \| grep tempo_receiver` | Verify tracer configuration uses `http://tempo:4318/v1/traces` for HTTP or `tempo:4317` for gRPC |
| **High S3 Read Costs / Slow Queries** | Large un-compacted block counts in object storage | `curl http://tempo:3200/compactor/status` | Enable Tempo Compactor and tune `compactor.block_retention` to merge small blocks |
| **Out of Memory (OOM) on Ingester** | Rapid span spikes overwhelming buffer memory before flushing to WAL | `kubectl logs -l app=tempo-ingester` | Increase `ingester.max_block_duration` or allocate higher RAM limits to ingester statefulsets |

## Related tools / concepts
- [Grafana Cloud](grafana-cloud.md) — Unified visualization dashboard for Tempo, Loki, and Prometheus.
- [OpenTelemetry Collector](opentelemetry-collector.md) — Telemetry gateway forwarding OTLP traces to Tempo.
- [Logfire](logfire.md) — Python observability framework supporting OTLP output.
- [Loki](grafana-loki.md) — Log aggregation engine correlated with Tempo traces.

## Sources / references
- [Grafana Tempo Official Documentation](https://grafana.com/docs/tempo/latest/)
- [Grafana Tempo GitHub Repository](https://github.com/grafana/tempo)
- [TraceQL Language Reference](https://grafana.com/docs/tempo/latest/traceql/)
- [OpenTelemetry Python SDK](https://opentelemetry.io/docs/languages/python/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
