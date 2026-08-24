# Grafana Cloud

## What it is
Grafana Cloud is a fully managed, high-performance observability platform that provides unified monitoring for metrics, logs, traces, and application performance. In early January 2027, it includes managed, horizontally-scalable versions of Prometheus, Loki, Tempo, and Grafana, along with specialized, cutting-edge **AI Observability** pipelines for frontier models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.8) and **FastMCP 3.1** agentic workflows.

## What problem it solves
It centralizes and correlates telemetry from diverse, decoupled systems into a single dashboarding and alerting interface. For AI applications, it eliminates the tracking gap by correlating infrastructure behavior with LLM parameters (latency, token usage, cost, error rates, and prompt performance). Its **Actually Useful AI™** suite, including Grafana Assistant, automates incident diagnosis and dashboard generation.

Through the **Grafana Assistant Data Source** integration, operators can query and correlate unified observability metrics across more than 30 diverse data sources via natural language. This eliminates manual timestamp correlation and tool-switching across cloud platforms, databases, and issue trackers by translating natural language requests into complex PromQL, LogQL, TraceQL, or SQL queries.

## Where it fits in the stack
**Infrastructure / Observability / Eval**. It serves as the primary visualization, alerting, and analysis layer for the [OpenTelemetry](opentelemetry-collector.md) and Prometheus ecosystems.

## Typical use cases
- **Multi-source Dashboards**: Combining AWS CloudWatch, Prometheus, and LLM logs into one unified view.
- **AI Agent Monitoring**: Tracking 95th percentile operation duration and cost attribution for complex agentic systems.
- **Log Aggregation**: Using Loki to search through distributed agent logs with trace correlation.
- **VectorDB Observability**: Monitoring query performance and resource utilization for vector databases.

## Strengths
- **Open Standard & FastMCP 3.1 Support**: Native support for Prometheus, OpenTelemetry (OTel), and FastMCP 3.1 protocols.
- **Rich Visualization**: Industry-leading, highly flexible dashboarding and graphing capabilities for multi-model agent clusters.
- **AI-Powered Insights**: Built-in assistants for root cause analysis, log pattern recognition, and incident summaries.
- **Scalability**: Managed infrastructure handles massive volumes of concurrent telemetry data across Llama 4 and Qwen 3.8 deployments.

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

### Shipping LLM Metrics with OpenTelemetry & Pydantic v2 Validation (Python)
Grafana Cloud supports OpenTelemetry natively. You can structure and validate telemetry payloads for **Claude 5.1**, **GPT-5.5**, or **Gemini 4.0 Pro** using Pydantic v2 schemas:

```python
import os
import sys
from pydantic import BaseModel, Field, field_validator

class GrafanaTelemetryMetric(BaseModel):
    model_name: str = Field(..., description="Target frontier model identifier")
    tokens_consumed: int = Field(..., ge=1, description="Number of tokens consumed")
    role: str = Field(default="user", description="Message role (user, assistant, system)")
    environment: str = Field(default="production")
    fastmcp_enabled: bool = Field(default=True)

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed = {"user", "assistant", "system", "tool"}
        if v.lower() not in allowed:
            raise ValueError(f"role must be one of {allowed}")
        return v.lower()

def ship_grafana_telemetry(payload: GrafanaTelemetryMetric) -> bool:
    # Demonstrating Pydantic v2 dump and OTLP telemetry dispatch format
    metric_data = payload.model_dump()
    print(f"Shipping validated metric payload to Grafana Cloud OTLP Gateway: {metric_data}")
    return True

if __name__ == "__main__":
    payload = GrafanaTelemetryMetric(
        model_name="claude-5.1",
        tokens_consumed=450,
        role="assistant"
    )
    success = ship_grafana_telemetry(payload)
    print("Telemetry dispatch status:", success)
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
- [Prometheus](prometheus.md) - Standard for k8s monitoring.
- [Loki](grafana-loki.md) - Horizontally scalable log aggregation.
- [Tempo](tempo.md) - High-volume distributed tracing.

## Sources / references
- [Grafana AI Observability Documentation](https://grafana.com/docs/grafana-cloud/monitor-applications/ai-observability/)
- [Grafana MCP Server](https://grafana.com/docs/grafana/latest/developer-resources/mcp/)
- [Actually Useful AI™ in Grafana Cloud](https://grafana.com/products/cloud/ai-observability/)
- [Llama 4 Maverick Observability Patterns](https://grafana.com/blog/2026/05/monitoring-llama-4-maverick/)
- [Grafana Assistant Expands to More Than 30 Data Sources - InfoQ](https://www.infoq.com/news/2026/07/grafana-assistant-data-source/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
