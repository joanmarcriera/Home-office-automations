# OpenTelemetry Collector

## What it is
The OpenTelemetry (OTel) Collector is a high-performance, vendor-agnostic proxy designed to receive, process, and export telemetry data (traces, metrics, and logs). As of early January 2027, it serves as the universal standard for AI and agentic telemetry pipelines. It allows developers to unify metrics across traditional infrastructure layers and multi-agent workflows running on engines like **Claude 5.6**, **GPT-5.6**, **DeepSeek-V4**, and **Gemini 4.0 Ultra**. It is open-source and highly self-hostable.

## What problem it solves
Managing telemetry in multi-agent environments often introduces high performance overheads, strict vendor lock-in, and compliance risks related to personally identifiable information (PII). The OTel Collector mitigates these concerns by providing:
- **Unified Ingestion**: A single OTLP gateway receiving telemetry signals from all microservices, eliminating the need to deploy distinct vendor-specific monitoring agents.
- **Client-Side Processing**: Real-time scrubbing of sensitive customer fields, prompt content, or API keys directly within the local network prior to routing.
- **Dynamic Routing**: A "receive once, distribute many" setup, sending trace metrics concurrently to cloud metrics providers, security databases, and local archives.
- **Sampling Governance**: Cost-defensive tail-based sampling configurations to drop redundant, successful runs and isolate only anomalous or slow multi-turn traces.
- **FastMCP 3.1 Session Instrumentation**: The ability to translate Model Context Protocol (FastMCP 3.1) Task Protocol connection patterns, tool invocations, and payload responses into standardized OTLP traces.

## Where it fits in the stack
The OpenTelemetry Collector sits in the **Observability Infrastructure** layer, acting as a telemetry router positioned securely between your production agent workflows (or proxies like [OpenRouter](../ai_knowledge/openrouter.md)) and target downstream monitoring platforms.

## Architecture & Telemetry Pipeline Diagram
```
+-----------------------------------------------------------------------------------+
|                        OpenTelemetry Collector Pipeline                           |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Receivers (OTLP gRPC :4317, OTLP HTTP :4318, Prometheus, Jaeger, FastMCP)   |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Processors (Memory Limiter, Batching, PII Scrubbing, Tail-based Sampling)   |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Exporters (ClickHouse, Datadog, Prometheus, Jaeger, Sentry, CloudWatch)    |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

```mermaid
sequenceDiagram
    autonumber
    actor Agent as Multi-Agent Application / FastMCP
    participant Receiver as OTel Receiver (gRPC/HTTP)
    participant Processor as Processor Pipeline (Batch/Scrub)
    participant Sampler as Tail-based Sampler
    participant Exporter as Exporter (ClickHouse/Datadog)

    Agent->>Receiver: Ship Trace Span & Token Usage Metrics (OTLP)
    Receiver->>Processor: Enqueue Spans in Memory Limiter Queue
    Processor->>Processor: Redact Sensitive Passwords / Prompts & Batch
    Processor->>Sampler: Evaluate Trace Duration & Exception Status
    alt Trace Normal (<1000ms & No Errors)
        Sampler-->>Processor: Drop 95% Routine Traces (Cost Control)
    else Trace Anomalous / Exception
        Sampler-->>Processor: Preserve 100% Trace Span
        Processor->>Exporter: Export Batched Spans to Storage Engine
        Exporter-->>Receiver: Acknowledge Ingestion
    end
```

## Typical use cases
- **PII Scrubbing and Safety Guarding**: Processing incoming LLM logs to identify and redact passwords, credentials, and medical data before cloud storage.
- **System and Agentic Cross-Correlation**: Combining standard compute infrastructure telemetry (K3s CPU, memory use) with model-level latency indicators.
- **Model Cost and Tokens Aggregation**: Extracting raw token counts from model payload fields and outputting them as custom prometheus gauges.
- **Anomaly Selection (Tail Sampling)**: Dropping 95% of standard, cheap agent traces, while ensuring 100% of runs that throw exceptions or latency spikes >5000ms are preserved.

## Comprehensive Comparison Matrix: Telemetry Architectures

| Dimension | OTel Collector Pipeline | Direct SaaS SDK Integration | Custom Logging Proxy | Prometheus / Grafana Native |
| :--- | :--- | :--- | :--- | :--- |
| **Vendor Lock-in** | Zero (Vendor Agnostic) | High (Tied to SaaS API) | None (Custom) | Low (Open Standards) |
| **Client Overhead** | Minimal (Asynchronous OTLP) | Medium (SaaS SDK Latency) | Medium (Custom HTTP Calls)| Low (Metrics Scraping) |
| **PII Scrubbing** | On-prem / Local Processing | Cloud-side (Data Risk) | Custom Code | Limited (Label Filtering) |
| **Trace & Metric Union** | Unified Spans + Metrics + Logs | Separate Products | Manual Correlation | Primary Metrics Focus |
| **Tail Sampling** | Native Stateful Processor | Paid SaaS Feature | Hard to Implement | N/A |
| **Protocol Standards** | OTLP / FastMCP 3.1 | Custom REST APIs | Custom Formats | OpenMetrics / Prometheus |

## Service & Daemon Management

### systemd Service Configuration (`/etc/systemd/system/otel-collector.service`)
Deploy the following unit file to operate the OTel Collector as a systemd background service on enterprise hosts:

```ini
[Unit]
Description=OpenTelemetry Collector Daemon & OTLP Telemetry Gateway
Documentation=https://opentelemetry.io/docs/collector/
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=otel
Group=otel
WorkingDirectory=/opt/otel-collector
ExecStart=/usr/local/bin/otelcol-contrib --config=/etc/otel-collector/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
Environment=LOG_LEVEL=info
Environment=GOMAXPROCS=4

# Hardening measures
ProtectSystem=full
ProtectHome=read-only
ReadWritePaths=/var/log/otel-collector /tmp
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

### Docker Compose Multi-Service Observability Stack (`docker-compose.yml`)
Deploy the OTel Collector alongside Prometheus and Jaeger trace backends:

```yaml
version: '3.8'

services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.118.0
    container_name: otel-collector-gateway
    command: ["--config=/etc/otelcol/config.yaml"]
    volumes:
      - ./config.yaml:/etc/otelcol/config.yaml
    ports:
      - "4317:4317" # OTLP gRPC Receiver
      - "4318:4318" # OTLP HTTP Receiver
      - "8888:8888" # OTel Collector Metrics
    depends_on:
      - prometheus
      - jaeger
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    container_name: otel-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: otel-jaeger
    ports:
      - "16686:16686" # Jaeger Web UI
      - "14250:14250"
    restart: unless-stopped
```

## Strengths
- **Ultimate Vendor Freedom**: Compatible with nearly every commercial and open-source observability engine on the market.
- **Architectural Extensibility**: Modular "Receivers, Processors, and Exporters" pipeline design allows developers to write custom processors in Go.
- **Incredible Efficiency**: Light memory and CPU footprint, capable of handling hundreds of thousands of events per second with sub-millisecond pipeline latency.
- **Semantic Conventions**: Standardized, industry-backed schemas for modeling traces and metric tags uniformly.

## Limitations
- **Substantial Operational Overhead**: Requires setup, management, horizontal scaling, and live-monitoring of the Collector cluster itself.
- **Complex YAML Configurations**: Fine-tuning batching, retry limits, and security layers can result in massive, hard-to-maintain YAML configurations.
- **Stateful Memory Overhead**: Stateful operations like tail-based sampling or metric accumulation require localized storage buffers, complicating container scheduling.

## When to use it
- When routing telemetry data to multiple target platforms (e.g., an enterprise cloud provider and a local database).
- When processing or sanitizing sensitive log text (like user input records) is required before leaving localized firewalls.
- When you are scaling production LLM workloads and need fine-grained control over telemetry collection budgets and trace sampling.
- When building robust multi-agent orchestration systems that demand vendor-agnostic standards.

## When not to use it
- For single-developer script prototypes where directly exporting to a single destination is easier to bootstrap.
- If your team has zero operational capacity or budget to set up and manage additional Docker or Kubernetes infrastructure.
- When utilizing a specialized platform whose distinct, closed-source agent features cannot be easily modeled via OpenTelemetry APIs.

## Getting started

### Basic Configuration (`config.yaml`)
Create an OTel Collector configuration file specifying standard OTLP ingestion, a processing batch queue, and local console and database exporters:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: "0.0.0.0:4317"
      http:
        endpoint: "0.0.0.0:4318"

processors:
  batch:
    send_batch_size: 8192
    timeout: 1s
    send_batch_max_size: 10240
  memory_limiter:
    check_interval: 1s
    limit_percentage: 80
    spike_limit_percentage: 20

exporters:
  otlp/clickhouse:
    endpoint: "clickhouse-server:4317"
    tls:
      insecure: true
  logging:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [logging, otlp/clickhouse]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [logging, otlp/clickhouse]
```

### Run via Docker
Launch the OpenTelemetry Collector container mapping the necessary gRPC and HTTP OTLP ports:

```bash
docker run -d \
    -p 4317:4317 \
    -p 4318:4318 \
    -v $(pwd)/config.yaml:/etc/otelcol/config.yaml \
    --name otel-collector \
    otel/opentelemetry-collector:0.118.0
```

## CLI examples

### Validate Configuration Syntax
Validate a local YAML configuration file using the built-in validator tool:

```bash
otelcol validate --config=config.yaml
```

### Starting the Collector Manually
Start the OTel collector agent with customized logging levels:

```bash
otelcol --config=config.yaml --log-level=info
```

### Querying Collector Performance Version
Query the installed runtime version specifications:

```bash
otelcol --version
```

## API examples

### FastMCP 3.1 OTel Span Validation Server with Pydantic v2
The following Python code configures a **FastMCP 3.1** telemetry instrumentation tool that validates agent span metadata using **Pydantic v2** and emits OTLP traces to the OpenTelemetry Collector:

```python
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from fastmcp import FastMCP

# Initialize FastMCP 3.1 server
mcp = FastMCP(name="otel-telemetry-instrumentor", version="3.1")

# Configure Tracer Provider
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
provider.add_span_processor(processor)
tracer = trace.get_tracer("agentic-otel-tracer")

class AgentSpanMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    model_name: str = Field(..., description="Target frontier model identifier")
    prompt_tokens: int = Field(..., ge=0, description="Token count in input prompt")
    completion_tokens: int = Field(..., ge=0, description="Token count in output completion")
    agent_id: str = Field(..., description="Unique agent identifier")

    @field_validator("model_name")
    @classmethod
    def validate_model(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Model name cannot be empty")
        return v.lower()

@mcp.tool(name="record_agent_trace", description="Emit validated OpenTelemetry trace span to OTel Collector")
def record_agent_trace(payload: Dict[str, Any]) -> Dict[str, Any]:
    """FastMCP 3.1 tool endpoint for agent trace emission."""
    try:
        meta = AgentSpanMetadata.model_validate(payload)
        with tracer.start_as_current_span("agent-task-routing-span") as span:
            span.set_attribute("llm.model", meta.model_name)
            span.set_attribute("llm.prompt_tokens", meta.prompt_tokens)
            span.set_attribute("llm.completion_tokens", meta.completion_tokens)
            span.set_attribute("agent.id", meta.agent_id)

        return {
            "status": "emitted",
            "agent_id": meta.agent_id,
            "model": meta.model_name,
            "total_tokens": meta.prompt_tokens + meta.completion_tokens
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    test_payload = {
        "model_name": "claude-5-6-sonnet",
        "prompt_tokens": 452,
        "completion_tokens": 128,
        "agent_id": "finance_routing_agent"
    }
    print("Record Agent Trace Result:", record_agent_trace(test_payload))
```

## Troubleshooting Guide

| Issue / Symptom | Probable Cause | Corrective Action |
| :--- | :--- | :--- |
| `Connection Refused on 4317/4318` | Collector container not running or ports not exposed | Check `docker ps` and ensure ports `4317` (gRPC) and `4318` (HTTP) are mapped. |
| `High Memory Consumption / OOM` | Memory limiter limits set too high or batch sizes excessive | Lower `limit_percentage` in `memory_limiter` processor to `70%` and reduce `send_batch_max_size`. |
| `Spans Missing in Downstream DB` | Tail-sampling filter dropping traces or exporter TLS mismatch | Temporarily disable tail-based sampling or enable `verbosity: detailed` in logging exporter. |
| `Malformed OTLP Payload` | Client sending incompatible OTLP version | Upgrade client OpenTelemetry SDKs to align with Collector version `0.118+`. |

## Related tools / concepts
- [Datadog](datadog.md) — Enterprise cloud tracing.
- [Sentry](sentry.md) — Exception tracking with native OTLP integration.
- [ClickHouse](clickhouse.md) — Relational columnar store for high-throughput traces.
- [Langfuse](langfuse.md) — Purpose-built open-source LLM tracing.
- [AgentOps](agentops.md) — High-level agent framework analysis.
- [Helicone](helicone.md) — LLM monitoring and request routing.
- [OpenRouter](../ai_knowledge/openrouter.md) — Broad-scale model routing and metric logs.
- [Grafana Cloud](grafana-cloud.md) — High-level telemetry dashboards.
- [PostHog](posthog.md) — In-app product analytics.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized agent tool-calling protocol.
- [Llama 4](../ai_knowledge/local_llms.md) — Monitored local execution runtime.

## Sources / references
- [OpenTelemetry Official Specification Portal](https://opentelemetry.io/)
- [OpenTelemetry Collector Repository on GitHub](https://github.com/open-telemetry/opentelemetry-collector)
- [W3C Trace Context Standard Spec](https://www.w3.org/TR/trace-context/)
- [OpenTelemetry semantic conventions for AI applications](https://opentelemetry.io/docs/specs/semconv/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
