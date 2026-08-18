# Prometheus

## What it is

- **Dimensional Data Model**: Time series identified by metric name and key/value pairs (labels), enabling granular slicing and dicing of system telemetry.
- **Pull-Based Metrics Collection**: Scrapes HTTP/HTTPS endpoints exporting Prometheus metrics format or OpenTelemetry metrics at configured scrape intervals.
- **PromQL Query Engine**: Flexible expression language to calculate rates, aggregations, percentiles, and dynamic alerting thresholds.
- **Autonomous & Local Architecture**: Single-binary operational model without external distributed storage dependencies, ensuring high reliability during network partitions.
- **FastMCP 3.1 & Agentic Observability Integration**: Native scraping of AI agent runtime metrics, token throughput, model latency, and tool invocation counts.


## What problem it solves
- Solves the challenge of monitoring dynamic cloud-native infrastructure, Kubernetes clusters, and microservices without relying on complex external database dependencies.
- Eliminates blind spots in AI model inference runtimes by tracking real-time request counts, GPU utilization, and token latencies.

## Where it fits in the stack
- Operates in the **Observability & Monitoring** layer of the cloud-native stack.
- Integrates directly with the Grafana LGTM suite, OpenTelemetry Collector, and FastMCP 3.1 agent runtime metrics exporters.

## Typical use cases

- **Kubernetes & Cloud-Native Monitoring**: Collecting node, container, pod, and service control plane metrics via kube-state-metrics and cAdvisor.
- **AI Model Inference Telemetry**: Tracking request throughput, first-token latency, GPU memory utilization, and KV cache hit ratios for vLLM, TGI, and TensorRT-LLM servers.
- **Distributed Agent Telemetry**: Monitoring agentic workflow executions, sub-task runtimes, and MCP tool failure rates across agent swarms.
- **Alerting & Escalation**: Evaluating PromQL rules against threshold criteria and routing notifications through Alertmanager to Slack, PagerDuty, or Webhooks.


## Strengths

- **High Performance**: Optimized time-series storage engine handling millions of samples per second on modest CPU/RAM footprints.
- **Ecosystem Dominance**: Near-universal support across cloud platforms, ingress controllers, databases, and LLM inference runtimes.
- **Service Discovery**: Seamless auto-discovery of targets across Kubernetes, AWS EC2, Consul, Azure, and Google Cloud.


## Limitations

- **Long-Term Storage Limitations**: Local TSDB is designed for operational short-to-medium term retention; long-term analytical storage requires integration with systems like Grafana Mimir, Thanos, or Cortex.
- **No Event Logs or Traces**: Strictly focused on numeric time-series metrics; logs (Loki) and distributed traces (Tempo) require complementary tools in the Grafana LGTM stack.
- **Pull Model Edge Challenges**: Short-lived transient batch jobs or edge devices require a Pushgateway proxy for metric collection.


## When to use it

- When building cloud-native observability for Kubernetes infrastructure and microservice architectures.
- When tracking real-time performance indicators and operational metrics for LLM inference servers and AI agent runtimes.
- When you require a proven, lightweight time-series database and alerting framework without mandatory cloud dependencies.


## When not to use it
- When you require a long-term analytical store for logs or distributed traces (use Loki or Tempo instead).
- When monitoring ephemeral, highly transient batch processes without a Pushgateway.

## Getting started

```
+-------------------------------------------------------------------+
|                        Prometheus Server                          |
|                                                                   |
|   +-------------------+    +----------------+    +------------+   |
|   |  Service          |    |   Retrieval    |    | Local TSDB |   |
|   |  Discovery        |===>| (Scrape Engine)|===>| Storage    |   |
|   +-------------------+    +----------------+    +------------+   |
|                                                          ||       |
|                                                          \/       |
|                            +----------------------------------+   |
|                            |   PromQL Engine & Web UI / API   |   |
|                            +----------------------------------+   |
+-------------------------------------------------------------------+
           ^                                         ||
           | Scrapes HTTP /metrics                   \/
+-----------------------+                    +---------------+
| Targets:              |                    | Alertmanager / |
| - vLLM / TensorRT-LLM |                    | Grafana Cloud |
| - FastMCP 3.1 Agents  |                    +---------------+
| - K8s Nodes / Pods    |
+-----------------------+
```


## CLI examples



## API examples

Prometheus scrapes metrics formatted as plain text time-series measurements. The following Python example demonstrates exposing custom AI inference and FastMCP 3.1 agent metrics using the official Prometheus Python client, validated via strict **Pydantic v2** models before recording metric observations.

```python
import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, start_http_server
from pydantic import BaseModel, Field, FieldValidationInfo, field_validator

# ---------------------------------------------------------------------------
# Pydantic v2 Telemetry Schema
# ---------------------------------------------------------------------------
class AgentTelemetryEvent(BaseModel):
    agent_id: str = Field(..., description="Unique identifier for the agent instance")
    provider: str = Field(..., description="LLM provider (e.g. Anthropic, OpenAI)")
    model_name: str = Field(..., description="Model identifier")
    mcp_tool: str = Field(..., description="MCP tool invoked by agent")
    latency_seconds: float = Field(..., ge=0.0, description="Execution duration in seconds")
    tokens_used: int = Field(..., ge=0, description="Total prompt and completion tokens consumed")
    status: str = Field(..., description="Execution status: 'success' or 'error'")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"success", "error"}
        if v.lower() not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v.lower()

# ---------------------------------------------------------------------------
# Prometheus Metric Declarations
# ---------------------------------------------------------------------------
AGENT_REQUESTS_TOTAL = Counter(
    "agent_requests_total",
    "Total number of agent tool executions",
    ["agent_id", "provider", "model_name", "mcp_tool", "status"]
)

AGENT_LATENCY_SECONDS = Histogram(
    "agent_latency_seconds",
    "Agent tool execution latency in seconds",
    ["agent_id", "mcp_tool"],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0)
)

AGENT_TOKEN_CONSUMPTION_TOTAL = Counter(
    "agent_token_consumption_total",
    "Total LLM tokens consumed by agent operations",
    ["agent_id", "model_name"]
)

def record_agent_execution(event_data: Dict[str, Any]) -> None:
    """Validate telemetry event and observe metrics in Prometheus."""
    event = AgentTelemetryEvent.model_validate(event_data)

    AGENT_REQUESTS_TOTAL.labels(
        agent_id=event.agent_id,
        provider=event.provider,
        model_name=event.model_name,
        mcp_tool=event.mcp_tool,
        status=event.status
    ).inc()

    AGENT_LATENCY_SECONDS.labels(
        agent_id=event.agent_id,
        mcp_tool=event.mcp_tool
    ).observe(event.latency_seconds)

    AGENT_TOKEN_CONSUMPTION_TOTAL.labels(
        agent_id=event.agent_id,
        model_name=event.model_name
    ).inc(event.tokens_used)

if __name__ == "__main__":
    # Start Prometheus HTTP metrics exporter on port 8000
    start_http_server(8000)
    print("Prometheus metrics exporter running on http://localhost:8000/metrics")

    sample_payload = {
        "agent_id": "agent-researcher-01",
        "provider": "Anthropic",
        "model_name": "claude-5.1-sonnet",
        "mcp_tool": "vector_search",
        "latency_seconds": 0.42,
        "tokens_used": 1250,
        "status": "success"
    }

    record_agent_execution(sample_payload)
    print("Recorded metrics sample successfully.")
```


## Related tools / concepts

- **[Grafana Cloud](grafana-cloud.md)**: Directly query Prometheus metrics alongside Loki logs and Tempo traces in unified dashboards.
- **[OpenTelemetry Collector](opentelemetry-collector.md)**: Export OTel metric pipelines seamlessly into Prometheus scrapers or remote write receivers.
- **[Logfire](logfire.md)**: Operational Python tracing platform with native Prometheus metric bridges.


## Sources / references

- [Prometheus Official Documentation](https://prometheus.io/docs/introduction/overview/)
- [CNCF Prometheus Project Page](https://www.cncf.io/projects/prometheus/)
- [Prometheus Python Client GitHub Repository](https://github.com/prometheus/client_python)
- [PromQL Query Language Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
