# Grafana Cloud

## What it is
Grafana Cloud is a fully managed observability platform that provides unified monitoring for metrics, logs, traces, and application performance. It includes hosted versions of Prometheus, Loki, Tempo, and Grafana.

## What problem it solves
It centralizes monitoring from disparate sources into a single dashboarding interface. For AI applications, it enables tracking of LLM latency, token usage, and error rates alongside traditional infrastructure metrics.

## Where it fits in the stack
**Infrastructure / Observability / Eval**.

## Typical use cases
- **Multi-source Dashboards**: Combining AWS CloudWatch, Prometheus, and LLM logs into one view.
- **Alerting**: Setting thresholds for AI response times or API error rates.
- **Log Aggregation**: Using Loki to search through distributed agent logs.

## Strengths
- **Open Standard Support**: Native support for Prometheus and OpenTelemetry.
- **Rich Visualization**: Industry-leading dashboarding capabilities.
- **Scalability**: Managed infrastructure handles high volumes of telemetry data.

## Limitations
- **Complexity**: Setting up advanced dashboards and alerts requires significant knowledge of PromQL or LogQL.
- **Data Silos**: Requires active effort to ensure all relevant data is being ingested.

## When to use it
- When you already use Grafana for infrastructure and want to add AI observability.
- When you need high-performance, long-term storage for logs and metrics.

## When not to use it
- For simple applications where basic logging is sufficient.

## Licensing and cost
- **Open Source**: The core components (Grafana, Loki, etc.) are open source (AGPLv3); the Cloud service is proprietary.
- **Cost**: Freemium (generous free tier, then usage-based).
- **Self-hostable**: Yes (via the LGTM stack).

## Getting started

### Installation
Grafana Cloud doesn't require a local installation for the UI, but you typically need an agent like **Grafana Alloy** or **Promtail** to ship data from your infrastructure.

### Example: Shipping Logs with Promtail (config.yaml)
```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: https://<your_loki_user>:<your_loki_api_key>@logs-prod-us-central1.grafana.net/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
    - targets:
        - localhost
      labels:
        job: varlogs
        __path__: /var/log/*.log
```

### LLM Observability with OpenTelemetry
Grafana Cloud supports OpenTelemetry natively. You can use the OpenTelemetry SDK in Python to send AI metrics:
```python
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

exporter = OTLPMetricExporter(endpoint="https://otlp-gateway-prod-us-central1.grafana.net/v1/metrics")
# ... configure meter and instrument to track token usage
```

## Related tools / concepts
- [Datadog](datadog.md)
- [New Relic AI](new-relic-ai.md)
- [OpenRouter (Log Streaming)](../ai_knowledge/openrouter.md)
- [OpenTelemetry Collector](opentelemetry-collector.md)
- [Prometheus](../../reference-implementations/k8s-infrastructure/monitoring/prometheus-grafana-values.yaml)

## Sources / References
- [Official Website](https://grafana.com/products/cloud/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Grafana Cloud AI Monitoring](https://grafana.com/solutions/ai-monitoring/)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
