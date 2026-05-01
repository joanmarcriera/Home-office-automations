# OpenTelemetry Collector

## What it is
The OpenTelemetry Collector is a vendor-agnostic proxy that can receive, process, and export telemetry data (metrics, logs, and traces). It is a core component of the OpenTelemetry project, designed to sit between instrumented applications and various observability backends.

## What problem it solves
It eliminates the need to run and maintain multiple vendor-specific agents for different observability tools. By providing a single codebase that supports many data formats (e.g., OTLP, Jaeger, Prometheus, Fluent Bit), it simplifies the collection pipeline and allows teams to switch backends without re-instrumenting their applications.

## Where it fits in the stack
**Category**: Process & Understanding / Observability Pipeline

## Typical use cases
- **Infrastructure Observability**: Collecting metrics and logs from Kubernetes clusters or virtual machines.
- **Application Performance Monitoring (APM)**: Aggregating and processing traces from microservices.
- **Data Transformation**: Redacting sensitive information or adding metadata (e.g., environment tags) to telemetry data before it reaches a backend.
- **Multi-Backend Export**: Sending the same telemetry data to multiple destinations (e.g., Datadog for monitoring and S3 for archival).

## Strengths
- **Vendor Agnostic**: Supports a wide range of open-source and commercial backends.
- **Highly Extensible**: Customizable via receivers, processors, exporters, and extensions.
- **Unified Pipeline**: Handles traces, metrics, and logs in a single process.
- **Performance**: Designed to be lightweight and handle high throughput with minimal overhead.

## Limitations
- **Configuration Complexity**: Managing large YAML configurations for complex pipelines can be challenging.
- **Operational Overhead**: Requires deployment and monitoring of the collector itself (though often managed as a sidecar or daemonset).

## When to use it
- When you want to decouple your application instrumentation from your observability backend.
- When you need to process or filter telemetry data before exporting it.
- When you are using multiple observability tools and want a unified collection layer.

## When not to use it
- For very small projects where sending data directly from the application to a single backend is simpler.
- If you are exclusively using a single vendor's ecosystem and don't mind the vendor lock-in.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0).
- **Cost**: Free (Self-hosted). Commercial distributions may have associated costs.

## Getting started

### Installation
The Collector can be installed as a binary, a Docker container, or a Kubernetes agent/gateway.

**Docker:**
```bash
docker run -v $(pwd)/config.yaml:/etc/otelcol/config.yaml otel/opentelemetry-collector:latest
```

### Basic configuration
A simple `config.yaml` to receive OTLP data and export to the console:

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
    loglevel: info

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging]
```

## CLI examples
```bash
# Start the collector with a specific config file
otelcol --config=config.yaml

# Check the version
otelcol --version
```

## API examples
The Collector is primarily a configuration-driven service. Applications interact with it via the OpenTelemetry SDKs using the OTLP protocol.

**Python SDK example (sending to local collector):**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize Tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP Exporter to point to the Collector
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

with tracer.start_as_current_span("hello-collector"):
    print("Span sent to OpenTelemetry Collector")
```

## Related tools / concepts
- [Datadog](datadog.md)
- [Sentry](sentry.md)
- [Grafana Cloud](grafana-cloud.md)
- [New Relic AI](new-relic-ai.md)
- [W&B Weave](wb-weave.md)

## Sources / references
- [OpenTelemetry Official Site](https://opentelemetry.io/)
- [Collector Documentation](https://opentelemetry.io/docs/collector/)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
