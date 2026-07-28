# Grafana Cloud

## What it is
Grafana Cloud is a fully managed, high-performance observability platform that provides unified monitoring for metrics, logs, traces, and application performance. It includes managed, horizontally-scalable versions of Prometheus, Loki, Tempo, and Grafana, along with specialized, cutting-edge **AI Observability** pipelines for LLM-powered applications and agentic workflows.

## What problem it solves
It centralizes and correlates telemetry from diverse, decoupled systems into a single dashboarding and alerting interface. For AI applications, it eliminates the tracking gap by correlating infrastructure behavior with LLM parameters (latency, token usage, cost, error rates, and prompt performance). Its **Actually Useful AI™** suite, including Grafana Assistant, automates incident diagnosis and dashboard generation.

## Where it fits in the stack
**Infrastructure / Observability / Eval**. It serves as the primary visualization, alerting, and analysis layer for the [OpenTelemetry](opentelemetry-collector.md) and Prometheus ecosystems.

## Typical use cases
- **Multi-source Dashboards**: Combining AWS CloudWatch, Prometheus, and LLM logs into one unified view.
- **AI Agent Monitoring**: Tracking 95th percentile operation duration and cost attribution for complex agentic systems.
- **Log Aggregation**: Using Loki to search through distributed agent logs with trace correlation.
- **VectorDB Observability**: Monitoring query performance and resource utilization for vector databases.

## Strengths
- **Open Standard Support**: Native support for Prometheus and OpenTelemetry (OTel) standards.
- **Rich Visualization**: Industry-leading, highly flexible dashboarding and graphing capabilities.
- **AI-Powered Insights**: Built-in assistants for root cause analysis, log pattern recognition, and incident summaries.
- **Scalability**: Managed infrastructure handles massive volumes of concurrent telemetry data.

## Limitations
- **Complexity**: Setting up advanced dashboards and alerts requires significant knowledge of PromQL or LogQL.
- **Data Silos**: Requires active instrumentation effort to ensure all relevant data is being ingested.
- **Evolving AI Features**: Some AI Observability features are still being actively extended and refined as of late September 2026.

## When to use it
- When you already use Grafana for infrastructure and want to add specialized AI observability.
- When you need high-performance, long-term storage for logs, metrics, and distributed traces.
- When you want to leverage [MCP](../automation_orchestration/mcp.md) to manage dashboards and query telemetry data via AI assistants.

## When not to use it
- For simple applications where basic logging is sufficient.
- If you prefer a purely local, lightweight observability stack.

## Getting started

### Installation
Grafana Cloud doesn't require a local installation for the UI, but you typically need an agent like **Grafana Alloy** to ship data.

```bash
# Install Grafana Alloy (Debian/Ubuntu)
sudo apt-get install alloy
```

### Basic Setup
1. Create a free account at [grafana.com](https://grafana.com/).
2. Navigate to **AI Observability** in the sidebar to enable LLM monitoring features.
3. Configure your LLM providers (e.g., [Claude](../ai_knowledge/claude.md) or OpenAI) to ship OpenTelemetry data to your Grafana endpoint.

## CLI examples

### Using Grafana Alloy to ship logs
```bash
# Start Grafana Alloy with a local config
alloy run config.alloy
```

### Querying Loki logs via LogCLI
```bash
# Query logs for a specific job
logcli query '{job="varlogs"}' --addr="https://logs-prod-us-central1.grafana.net"
```

### Managing Dashboards via Grafana CLI
```bash
# List installed plugins
grafana-cli plugins ls
```

## API examples

### Shipping LLM Metrics with OpenTelemetry (Python)
Grafana Cloud supports OpenTelemetry natively. You can use the OpenTelemetry SDK to track token usage for models like **Claude 5.1** or **GPT-5.5**.

```python
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

API_URL = "https://otlp-gateway-prod-us-central1.grafana.net/v1/metrics"
API_TOKEN = "your_grafana_cloud_token"

headers = {
    "Authorization": f"Basic {API_TOKEN}"
}

# Set up the exporter and reader
exporter = OTLPMetricExporter(endpoint=API_URL, headers=headers)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("llm-observability")
token_counter = meter.create_counter(
    "llm.tokens.total",
    description="Total tokens consumed by model calls",
    unit="tokens"
)

# Record token usage example
token_counter.add(150, {"model": "claude-5.1", "role": "user"})
```

### Querying Loki via API
```python
import requests

API_URL = "https://<your_loki_user>:<your_loki_api_key>@logs-prod-us-central1.grafana.net/loki/api/v1/query"
params = {'query': '{job="agent-logs"}'}

response = requests.get(API_URL, params=params)
print(response.json())
```

## Related tools / concepts
- [Datadog](datadog.md) - Enterprise-grade observability and security.
- [New Relic AI](new-relic-ai.md) - Full-stack AI monitoring and alerting.
- [OpenTelemetry Collector](opentelemetry-collector.md) - Vendor-neutral telemetry proxy.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Standard for connecting agents to data.
- [Claude](../ai_knowledge/claude.md) - Frontier LLM for orchestration.
- [LlamaIndex](../ai_knowledge/llamaindex.md) - Data framework for LLM applications.
- [Prometheus](../../reference-implementations/k8s-infrastructure/monitoring/prometheus-grafana-values.yaml) - Standard for k8s monitoring.
- [Loki](../../services/loki.md) - Horizontally scalable log aggregation.
- [Tempo](../../services/tempo.md) - High-volume distributed tracing.

## Sources / references
- [Grafana AI Observability Documentation](https://grafana.com/docs/grafana-cloud/monitor-applications/ai-observability/)
- [Grafana MCP Server](https://grafana.com/docs/grafana/latest/developer-resources/mcp/)
- [Actually Useful AI™ in Grafana Cloud](https://grafana.com/products/cloud/ai-observability/)
- [Llama 4 Maverick Observability Patterns](https://grafana.com/blog/2026/05/monitoring-llama-4-maverick/)

## Contribution Metadata
- Last reviewed: 2026-10-01
- Confidence: high
