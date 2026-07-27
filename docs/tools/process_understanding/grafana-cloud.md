# Grafana Cloud

## What it is
Grafana Cloud is a fully managed observability platform that provides unified monitoring for metrics, logs, traces, and application performance. It includes hosted versions of Prometheus, Loki, Tempo, and Grafana, along with specialized **AI Observability** features for LLM-powered applications.

## What problem it solves
It centralizes monitoring from disparate sources into a single dashboarding interface. For AI applications, it enables tracking of LLM latency, token usage, and error rates alongside traditional infrastructure metrics. Its **Actually Useful AI™** suite, including Grafana Assistant, helps automate incident analysis and dashboard generation.

## Where it fits in the stack
**Infrastructure / Observability / Eval**. It serves as the primary visualization and alerting layer for the [OpenTelemetry](opentelemetry-collector.md) ecosystem.

## Typical use cases
- **Multi-source Dashboards**: Combining AWS CloudWatch, Prometheus, and LLM logs into one view.
- **AI Agent Monitoring**: Tracking 95th percentile operation duration and cost attribution for agentic systems.
- **Log Aggregation**: Using Loki to search through distributed agent logs with trace correlation.
- **VectorDB Observability**: Monitoring query performance and resource utilization for vector databases.

## Strengths
- **Open Standard Support**: Native support for Prometheus and OpenTelemetry.
- **Rich Visualization**: Industry-leading dashboarding capabilities.
- **AI-Powered Insights**: Built-in agents for root cause analysis and incident summaries.
- **Scalability**: Managed infrastructure handles high volumes of telemetry data.

## Limitations
- **Complexity**: Setting up advanced dashboards and alerts requires significant knowledge of PromQL or LogQL.
- **Data Silos**: Requires active effort to ensure all relevant data is being ingested.
- **Public Preview**: Some AI Observability features are still in public preview as of late July 2026.

## When to use it
- When you already use Grafana for infrastructure and want to add AI observability.
- When you need high-performance, long-term storage for logs and metrics.
- When you want to leverage [MCP](../automation_orchestration/mcp.md) to manage dashboards and query data via AI assistants.

## When not to use it
- For simple applications where basic logging is sufficient.
- If you prefer a purely local, lightweight observability stack.

## Getting started

### Installation
Grafana Cloud doesn't require a local installation for the UI, but you typically need an agent like **Grafana Alloy** to ship data.

```bash
# Install Grafana Alloy (debian/ubuntu stable repository setup)
sudo apt-get install alloy
```

### Basic Setup
1. Create a free account at [grafana.com](https://grafana.com/).
2. Navigate to **AI Observability** in the sidebar to enable the public preview features.
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
import os
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from pydantic import BaseModel, Field

class GrafanaConfig(BaseModel):
    api_url: str = Field("https://otlp-gateway-prod-us-central1.grafana.net/v1/metrics", description="OTLP endpoint URL")
    api_token: str = Field(..., description="Grafana Cloud Access Token")

# Configuration with Pydantic v2 validation
config = GrafanaConfig(api_token=os.environ.get("GRAFANA_CLOUD_TOKEN", "fallback-token"))

headers = {
    "Authorization": f"Basic {config.api_token}"
}

exporter = OTLPMetricExporter(endpoint=config.api_url, headers=headers)
# ... configure meter and instrument to track token usage
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
- Last reviewed: 2026-07-27
- Confidence: high
