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

### Basic Configuration (`config.yaml`)
```yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:

exporters:
  logging:
    verbosity: detailed
  otlp/datadog:
    endpoint: "https://otlp-http-intake.datadoghq.com"
    headers:
      "dd-api-key": "${DD_API_KEY}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging, otlp/datadog]
```

### Run via Docker
```bash
docker run -p 4317:4317 -p 4318:4318 \
    -v $(pwd)/config.yaml:/etc/otelcol/config.yaml \
    otel/opentelemetry-collector:latest
```

## Related tools / concepts
- [Datadog](datadog.md)
- [Sentry](sentry.md)
- [Grafana Cloud](grafana-cloud.md)
- [New Relic AI](new-relic-ai.md)
- [OpenRouter](../ai_knowledge/openrouter.md)

## Sources / references
- [Official Website](https://opentelemetry.io/docs/collector/)
- [GitHub Repository](https://github.com/open-telemetry/opentelemetry-collector)
- [OpenRouter OTel Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/opentelemetry-collector)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
