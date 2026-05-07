# OpenTelemetry Collector

## What it is
The OpenTelemetry (OTel) Collector is a vendor-agnostic proxy that can receive, process, and export telemetry data (traces, metrics, and logs). It acts as a central hub for observability data in modern cloud and AI architectures.

## What problem it solves
It removes the need to run multiple agents or use vendor-specific libraries for each observability backend. By using the Collector, developers can send data once and have it routed to multiple destinations (e.g., Datadog, Sentry, and a local ClickHouse instance) while performing transformations and filtering in between.

## Where it fits in the stack
**Category**: Process & Understanding / Observability Infrastructure

## Typical use cases
- **Telemetry Routing**: Sending LLM traces from OpenRouter to multiple backends simultaneously.
- **Data Processing**: Scrubbing PII (Personally Identifiable Information) from logs before they leave your environment.
- **Metrics Aggregation**: Collecting and normalizing metrics from various parts of a home-lab or enterprise stack.
- **Standardizing Instrumentation**: Using a consistent OTLP (OpenTelemetry Protocol) format across different services.

## Strengths
- **Vendor-Agnostic**: Compatible with almost every major observability platform and open-source tool.
- **Highly Extensible**: Modular architecture allows for custom receivers, processors, and exporters.
- **Unified Pipeline**: Handles traces, metrics, and logs in a single codebase.
- **Resource Efficient**: Designed for high performance and low overhead.

## Limitations
- **Configuration Complexity**: The YAML-based configuration can be extensive and requires understanding of the pipeline model.
- **Operational Overhead**: Requires managing and scaling the Collector instances themselves.
- **State Management**: Some advanced features (like tail-based sampling) require stateful tracking, which can be complex to scale.

## Getting started

### OpenRouter OTLP Broadcast
OpenRouter can send traces via HTTP/protobuf to an OTel Collector.
- **Endpoint**: `https://<your-collector-domain>/v1/traces`
- **Protocol**: OTLP/HTTP

### Basic Configuration (`config.yaml`)
This example shows how to receive AI traces and export them to both Sentry and a local logging service.

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"

processors:
  batch:
  memory_limiter:
    check_interval: 1s
    limit_mib: 1000

exporters:
  otlphttp/sentry:
    endpoint: "https://<sentry-dsn>@o<org-id>.ingest.sentry.io/api/<proj-id>/otlp/"
  logging:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [logging, otlphttp/sentry]
```

### Run via Docker
```bash
docker run -p 4318:4318 \
    -v $(pwd)/config.yaml:/etc/otelcol/config.yaml \
    otel/opentelemetry-collector:latest
```

## CLI examples

### Run with Custom Config
```bash
otelcol --config=config.yaml
```

### Validate Configuration
```bash
otelcol validate --config=config.yaml
```

### Check Version
```bash
otelcol --version
```

## API examples

### Python (OTLP Trace Export)
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize Tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP Exporter to local Collector
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

with tracer.start_as_current_span("agent-interaction"):
    print("Sending telemetry to OTel Collector...")
```

## Related tools / concepts
- [Datadog](datadog.md)
- [Sentry](sentry.md)
- [Grafana Cloud](grafana-cloud.md)
- [New Relic AI](new-relic-ai.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [ClickHouse](clickhouse.md)
- [PostHog](posthog.md)

## Sources / references
- [Official Website](https://opentelemetry.io/docs/collector/)
- [GitHub Repository](https://github.com/open-telemetry/opentelemetry-collector)
- [OpenRouter OTel Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/otel-collector)

## Contribution Metadata
- Last reviewed: 2026-05-24
- Confidence: high
