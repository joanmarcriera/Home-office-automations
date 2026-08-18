# Tempo

## What it is

- **Object Storage Architecture**: High-efficiency trace storage backed directly by object stores (AWS S3, Google Cloud Storage, Azure Blob, MinIO) without requiring costly search indexes (Elasticsearch/OpenSearch).
- **OpenTelemetry Native**: Complete native support for OpenTelemetry (OTLP/gRPC and OTLP/HTTP), Jaeger, Zipkin, and OpenTracing formats.
- **Trace Discovery via TraceQL**: Powerful query language (TraceQL) allowing operators to search traces by span attributes, execution duration, error status, resource attributes, and custom agent tags.
- **Metrics-Generator Integration**: Generates RED (Rate, Errors, Duration) operational metrics automatically from incoming trace streams and writes them back to Prometheus or Mimir.
- **Deep Grafana & FastMCP 3.1 Integration**: Direct correlation with Prometheus metrics, Loki logs, and FastMCP 3.1 trace context propagation across distributed multi-agent swarms.


## What problem it solves
- Eliminates high infrastructure storage costs associated with traditional indexed distributed trace databases.
- Resolves complex microservice bottleneck diagnosis and multi-agent execution tracking across distributed clusters.

## Where it fits in the stack
- Sits in the **Distributed Observability & Tracing** layer.
- Integrates with OpenTelemetry Collector, Prometheus metrics, and Grafana Loki logs in the LGTM stack.

## Typical use cases

- **Agentic Execution Tracing**: Visualization of multi-turn agentic workflows, sub-agent task delegation, prompt preparation steps, and tool response latency.
- **Microservice Bottleneck Diagnosis**: Identifying long-tail latency bottlenecks in distributed microservice architectures and vector database queries.
- **Error & Failure Root Cause Analysis**: Pinpointing exact span failure points during agent execution loops or database connectivity drops.
- **Token & Cost Allocation Attribution**: Injecting token counts and cost attributes into span metadata to track operational spending per user or workflow.


## Strengths

- **Cost-Effective Scale**: Massive cost savings compared to traditional indexed trace stores due to object-storage-first architecture.
- **High Ingestion Throughput**: Scalable, horizontally composable microservice architecture capable of ingesting millions of trace spans per second.
- **LGTM Ecosystem Synergy**: One-click jump between logs (Loki), metrics (Prometheus), and traces (Tempo) within Grafana Cloud or self-hosted Grafana.


## Limitations

- **Search Query Latency on Cold Storage**: Searching for unindexed trace spans across massive historical time windows can require scanning object storage blocks.
- **Storage Compaction Management**: Requires running Tempo compactor components to manage block compaction and retention policies in object storage buckets.


## When to use it

- When building distributed, cloud-native microservice platforms or multi-agent orchestration frameworks using OpenTelemetry.
- When you require enterprise distributed tracing without the heavy cost and maintenance overhead of Elasticsearch/OpenSearch clusters.
- When leveraging Grafana and Prometheus as your primary operational monitoring UI.


## When not to use it
- When you only require simple single-process logging without distributed service calls.
- When operating without object storage infrastructure (S3/GCS/MinIO).

## Getting started

```
+-------------------------------------------------------------------+
|                        Grafana Tempo Cluster                      |
|                                                                   |
|   +-------------------+    +----------------+    +------------+   |
|   | Distributor       |===>| Ingester       |===>| Object     |   |
|   | (OTLP Receiver)   |    | (WAL & Blocks) |    | Storage    |   |
|   +-------------------+    +----------------+    +------------+   |
|                                                          ||       |
|                                                          \/       |
|                            +----------------------------------+   |
|                            | TraceQL Query Frontend & Engine  |   |
|                            +----------------------------------+   |
+-------------------------------------------------------------------+
           ^                                         ||
           | OTLP Trace Spans                        \/
+-----------------------+                    +---------------+
| OpenTelemetry         |                    | Grafana Cloud |
| Collector & Agents    |                    | Dashboard UI  |
+-----------------------+                    +---------------+
```


## CLI examples



## API examples

The following Python example demonstrates creating OpenTelemetry trace spans for an AI agentic task execution using the OpenTelemetry SDK, injecting custom trace attributes, and validating span metadata with strict **Pydantic v2** models before telemetry submission.

```python
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Initialize OpenTelemetry Tracer
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("agentic.tempo.tracer", "1.0.0")

# ---------------------------------------------------------------------------
# Pydantic v2 Trace Telemetry Schema
# ---------------------------------------------------------------------------
class AgentTraceSpanSchema(BaseModel):
    workflow_id: str = Field(..., description="Unique workflow identifier")
    agent_role: str = Field(..., description="Role executing the step")
    mcp_tool_name: str = Field(..., description="Name of FastMCP 3.1 tool invoked")
    execution_duration_ms: float = Field(..., ge=0.0, description="Duration in milliseconds")
    status_code: str = Field(..., description="Span status: 'OK' or 'ERROR'")

    @field_validator("status_code")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"OK", "ERROR"}
        if v.upper() not in allowed:
            raise ValueError(f"status_code must be one of {allowed}")
        return v.upper()

def trace_mcp_tool_execution(payload: Dict[str, Any]) -> None:
    """Validate trace metadata and record an OpenTelemetry span destined for Tempo."""
    validated_span = AgentTraceSpanSchema.model_validate(payload)

    with tracer.start_as_current_span(f"MCP Tool: {validated_span.mcp_tool_name}") as span:
        # Inject standard OpenTelemetry & Tempo trace attributes
        span.set_attribute("workflow.id", validated_span.workflow_id)
        span.set_attribute("agent.role", validated_span.agent_role)
        span.set_attribute("mcp.tool", validated_span.mcp_tool_name)
        span.set_attribute("execution.duration_ms", validated_span.execution_duration_ms)

        if validated_span.status_code == "ERROR":
            span.set_status(trace.StatusCode.ERROR, "Tool execution failed")
        else:
            span.set_status(trace.StatusCode.OK)

        time.sleep(validated_span.execution_duration_ms / 1000.0)

if __name__ == "__main__":
    sample_trace_data = {
        "workflow_id": "wf-88392",
        "agent_role": "Code_Executor",
        "mcp_tool_name": "execute_sandboxed_python",
        "execution_duration_ms": 120.5,
        "status_code": "OK"
    }

    print("Emitting trace span to OpenTelemetry / Tempo exporter...")
    trace_mcp_tool_execution(sample_trace_data)
    print("Trace span recorded successfully.")
```


## Related tools / concepts

- **[Grafana Cloud](grafana-cloud.md)**: Unified visualization platform correlating Tempo traces with Prometheus metrics and Loki logs.
- **[OpenTelemetry Collector](opentelemetry-collector.md)**: Primary telemetry ingestion gateway forwarding OTLP trace data to Tempo.
- **[Logfire](logfire.md)**: Python-centric tracing framework supporting OTLP output into Tempo.


## Sources / references

- [Grafana Tempo Official Documentation](https://grafana.com/docs/tempo/latest/)
- [Grafana Tempo GitHub Repository](https://github.com/grafana/tempo)
- [TraceQL Query Language Reference](https://grafana.com/docs/tempo/latest/traceql/)
- [OpenTelemetry Python SDK Documentation](https://opentelemetry.io/docs/languages/python/)



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
