# OpenTelemetry Collector

## What it is
The OpenTelemetry (OTel) Collector is a vendor-agnostic proxy designed to receive, process, and export telemetry data, including traces, metrics, and logs. It serves as a centralized hub for observability in modern distributed systems, allowing developers to decouple data collection from backend storage and analysis platforms.

## What problem it solves
Managing telemetry in complex AI and cloud architectures often leads to "agent fatigue" and vendor lock-in. The Collector addresses these issues by:
- **Unified Ingestion**: Providing a single endpoint for all telemetry signals (OTLP), removing the need for multiple vendor-specific agents.
- **Data Transformation**: Allowing for real-time processing, such as scrubbing PII (Personally Identifiable Information), adding metadata (e.g., environment, version), and filtering noise before data is exported.
- **Multi-Destination Routing**: Enabling a "send once, route many" pattern where data can be simultaneously sent to multiple backends (e.g., [Datadog](datadog.md) for production monitoring and a local [ClickHouse](clickhouse.md) for long-term audit logs).
- **Protocol Translation**: Converting legacy formats (like Jaeger or Zipkin) into modern OTLP.

## Where it fits in the stack
The OpenTelemetry Collector sits in the **Observability Infrastructure** layer. it is positioned between the instrumented application (or streaming sources like OpenRouter) and the final observability backends.

## Typical use cases
- **AI Telemetry Routing**: Receiving LLM traces from sources like [OpenRouter](../ai_knowledge/openrouter.md) and routing them to [Sentry](sentry.md) for error tracking and [Langfuse](langfuse.md) for performance evaluation.
- **PII Redaction**: Automatically identifying and masking sensitive user data in LLM prompt logs before they are sent to a cloud-based observability provider.
- **Metric Aggregation**: Collecting infrastructure metrics from a K3s cluster and LLM usage metrics from an application, then unifying them in a [Grafana Cloud](grafana-cloud.md) dashboard.
- **Tail-based Sampling**: High-volume AI applications can use the Collector to only export "interesting" traces (e.g., those with high latency or errors) while dropping standard successful requests to save on ingest costs.

## Strengths
- **Vendor Agnostic**: Compatible with almost every major observability platform, ensuring no single-provider lock-in.
- **Highly Extensible**: Modular "Receivers, Processors, and Exporters" architecture allows for custom plugins.
- **Resource Efficiency**: Written in Go and designed for high throughput with minimal CPU and memory overhead.
- **Standardized Schema**: Enforces the OpenTelemetry semantic conventions, making data consistent across different services and teams.

## Limitations
- **Operational Complexity**: Requires managing, scaling, and monitoring the Collector instances themselves.
- **YAML Configuration**: The configuration can become very large and complex as the number of pipelines and transformations increases.
- **Stateful Processing**: Features like tail-sampling or advanced aggregations require the Collector to be stateful, which complicates horizontal scaling.

## When to use it
- When you need to send telemetry data to more than one backend (e.g., a SaaS provider and a local database).
- When you need to transform or filter data (like redacting secrets) at the infrastructure level rather than in application code.
- When you want to standardize your observability stack on the OpenTelemetry protocol to avoid vendor lock-in.
- When you are managing high-volume LLM workloads and need advanced sampling to control observability costs.

## When not to use it
- For small, simple applications where sending data directly from the application to a single backend is easier to manage.
- If you have zero operational capacity to maintain additional infrastructure components.
- If you are using a single SaaS provider that offers a highly specialized agent that provides features not yet available via the OTel Collector.

## Getting started

### Basic Configuration (`config.yaml`)
This configuration receives traces via OTLP/HTTP and exports them to the console and a local [ClickHouse](clickhouse.md) instance.

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: "0.0.0.0:4318"
      grpc:
        endpoint: "0.0.0.0:4317"

processors:
  batch:
  memory_limiter:
    check_interval: 1s
    limit_mib: 1000

exporters:
  logging:
    verbosity: detailed
  otlp/clickhouse:
    endpoint: "clickhouse-server:4317"
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [logging, otlp/clickhouse]
```

### Run via Docker
```bash
docker run -p 4317:4317 -p 4318:4318 \
    -v $(pwd)/config.yaml:/etc/otelcol/config.yaml \
    otel/opentelemetry-collector:latest
```

## CLI examples

### Validate Configuration
Check if your `config.yaml` is syntactically correct before deploying:
```bash
otelcol validate --config=config.yaml
```

### Run with Custom Config
```bash
otelcol --config=config.yaml
```

## API examples

### Python (OTLP Trace Export)
Configure your Python application to send data to the local Collector:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to local Collector (default gRPC port)
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

with tracer.start_as_current_span("ai-agent-run"):
    # Your agent logic here
    print("Telemetry being handled by OTel Collector")
```

## Related tools / concepts
- [Datadog](datadog.md) - Enterprise SaaS observability backend.
- [Sentry](sentry.md) - Error tracking platform with OTLP support.
- [ClickHouse](clickhouse.md) - High-performance database often used as an OTel trace store.
- [Langfuse](langfuse.md) - LLM observability platform that integrates with OTel.
- [AgentOps](agentops.md) - Specialized agent monitoring that can coexist with OTel.
- [Helicone](helicone.md) - Proxy-based observability alternative.
- [OpenRouter](../ai_knowledge/openrouter.md) - Source of streaming LLM logs that can be broadcast via OTLP.
- [Grafana Cloud](grafana-cloud.md) - Unified visualization for OTel metrics and traces.
- [PostHog](posthog.md) - Product analytics that can ingest OTel events.

## Sources / references
- [OpenTelemetry Collector Documentation](https://opentelemetry.io/docs/collector/)
- [OTel Collector GitHub](https://github.com/open-telemetry/opentelemetry-collector)
- [OpenRouter OTel Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/otel-collector)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
