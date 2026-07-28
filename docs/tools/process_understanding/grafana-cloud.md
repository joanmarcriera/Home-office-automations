# Grafana Cloud

## What it is
Grafana Cloud is a fully managed, enterprise-grade observability and telemetry platform. It centralizes metrics, logs, traces, and application performance profiles into a unified visual dashboard. The platform incorporates hosted variants of Prometheus, Loki, Tempo, and Mimir, and provides native **AI Observability** suites designed specifically to monitor, rate-limit, and audit LLM-powered systems and agent clusters.

## What problem it solves
Managing modern agentic and multi-model deployments produces fragmented logs, distributed latency profiles, and unpredictable API token bills. Grafana Cloud solves this by consolidating raw infrastructure performance alongside LLM transaction metrics (e.g., token usage, cost parameters, and execution durations). Its integrated **Actually Useful AI™** assistant simplifies querying complex LogQL/PromQL logs and automatically pinpoints root causes during system failures.

## Where it fits in the stack
**Infrastructure / Observability / Eval**. Grafana Cloud serves as the primary analytics, visualization, and alerting destination. It acts as a central collector for metrics forwarded via [OpenTelemetry OTLP](opentelemetry-collector.md) or local collector agents like **Grafana Alloy**.

## Typical use cases
- **Multi-Tenant Dashboard Consolidation**: Overlaying host container metrics (CPU/Memory) with vector database response times and downstream LLM provider latencies.
- **Agent Handoff Analysis**: Visualizing agent interaction traces and execution steps to expose loops and bottlenecks.
- **Log Aggregation & Search**: Querying high-volume logs from hundreds of worker nodes using Loki's high-speed LogQL language.
- **Vector DB Health Monitoring**: Monitoring index reads, cluster size, and memory saturation for vectors engines like Qdrant, Chroma, or Milvus.

## Strengths
- **Industry Standard Support**: Zero-boilerplate ingestion of Prometheus metrics and OpenTelemetry (OTLP) data.
- **Advanced UI Visualization**: Customizable panels, graph plots, and real-time dashboard builders.
- **Native MCP 3.1 Server**: Dynamic Model Context Protocol integration allows agents to interact with Grafana logs and build dashboards autonomously.
- **Elastic Scalability**: Offloads database maintenance, indexing, and storage scaling to a highly reliable cloud framework.
- **Tight Loki-Tempo Linkage**: Seamlessly jump from a slow database log statement directly to its corresponding distributed transaction trace.

## Limitations
- **Query Language Friction**: Querying and dashboard configuration require an understanding of PromQL (for metrics) and LogQL (for logs).
- **Cost Ingest Boundaries**: High-frequency trace collection for complex, multi-model workflows can cause rapid data volume growth.
- **Public Preview Gaps**: Certain specialized LLM observability integrations are still in public preview as of late October 2026.

## When to use it
- When monitoring hybrid systems where traditional microservice infrastructure directly interacts with LLMs and agents.
- When establishing secure, long-term, and compliant storage repositories for distributed application telemetry.
- When utilizing OpenTelemetry standards to monitor codebases powered by **Claude 5.1** or **GPT-5.5**.

## When not to use it
- For lightweight, stand-alone scripts where simple terminal output or basic files suffice.
- If you strictly demand a 100% offline, local monitoring ecosystem with zero cloud connectivity.

## Getting started

### Installation
Grafana Cloud relies on remote cloud endpoints, but you typically deploy local logging daemon binaries like **Grafana Alloy** to pipe telemetry:

```bash
# Example Debian/Ubuntu installation command for Grafana Alloy daemon
sudo apt-get update && sudo apt-get install -y alloy
```

### Ingestion Setup
1. Sign up for a free or enterprise tier account at [grafana.com](https://grafana.com/).
2. Under **AI Observability** in your cloud portal, locate your unique OTLP Endpoint, Username, and Access Policy Token.
3. Configure your application or collector daemon to forward raw metrics using standard OTLP headers.

## CLI examples

### Running the Grafana Alloy Ingest Daemon
Start the collector using a local Alloy configuration file:
```bash
alloy run /etc/alloy/config.alloy
```

### Executing Remote Loki Queries via LogCLI
```bash
# Query agent logs on a remote Loki cluster using LogQL
logcli query '{app="llm-orchestrator"}' \
  --addr="https://logs-prod-us-central1.grafana.net" \
  --username="$LOKI_USER" \
  --password="$LOKI_API_KEY"
```

### Managing Grafana CLI Plugins
```bash
# Install the OpenTelemetry collector datasource plugin locally
grafana-cli plugins install grafana-opentelemetry-datasource
```

## API examples

### Shipping LLM Traces with OpenTelemetry (Python)
The script below demonstrates how to configure OpenTelemetry to ship LLM-related metrics directly to Grafana Cloud's OTLP endpoint using safe environment checks and the official OTLP HTTP metrics exporter.

```python
import os
import sys
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

def initialize_grafana_metrics():
    """Configures the OpenTelemetry SDK to ship token usage metrics to Grafana Cloud."""
    otlp_endpoint = os.environ.get("GRAFANA_OTLP_METRICS_ENDPOINT")
    api_token = os.environ.get("GRAFANA_ACCESS_TOKEN")

    if not otlp_endpoint or not api_token:
        print("Warning: Missing Grafana environment keys. Falling back to console logging.", file=sys.stderr)
        return None

    # Define authentication headers for Grafana Cloud
    headers = {
        "Authorization": f"Basic {api_token}"
    }

    # Configure the OTLP exporter to ship metric payloads
    exporter = OTLPMetricExporter(
        endpoint=otlp_endpoint,
        headers=headers
    )

    # Establish the Periodic Metric Reader and Meter Provider
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=15000)
    provider = MeterProvider(metric_readers=[reader])
    metrics.set_meter_provider(provider)

    # Instantiate the meter
    meter = metrics.get_meter("llm_observability_meter")

    # Define counter to track consumed tokens for Claude 5.1 and GPT-5.5
    token_counter = meter.create_counter(
        name="llm_token_usage_total",
        description="Tracks cumulative token consumption across model requests.",
        unit="1"
    )
    return token_counter

if __name__ == "__main__":
    counter = initialize_grafana_metrics()
    if counter:
        # Simulate recording metrics for a Claude 5.1 request
        counter.add(1450, {"model": "claude-5-1-sonnet", "type": "input"})
        counter.add(380, {"model": "claude-5-1-sonnet", "type": "output"})
        print("==> Telemetry metrics exported successfully!")
```

### Retrieving Raw Loki Logs via LogQL HTTP API
```python
import os
import requests

def fetch_recent_agent_logs():
    """Fetch raw agent logs via Loki query endpoint."""
    user = os.environ.get("LOKI_USER")
    api_key = os.environ.get("LOKI_API_KEY")
    url = "https://logs-prod-us-central1.grafana.net/loki/api/v1/query"

    if not user or not api_key:
        return None

    params = {
        'query': '{job="agent-orchestrator", level="error"}'
    }

    response = requests.get(url, params=params, auth=(user, api_key))
    return response.json()
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
- Last reviewed: 2026-10-24
- Confidence: high
