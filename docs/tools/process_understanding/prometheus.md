# Prometheus

## What it is
Prometheus is an open-source, CNCF-graduated systems monitoring and alerting toolkit built for cloud-native infrastructure, microservices, and AI inference runtimes. In January 2027, it serves as the foundation for modern operational telemetry, featuring:
- **Dimensional Data Model**: Time series identified by metric name and key/value pairs (labels), enabling granular slicing and dicing of system telemetry.
- **Pull-Based Metrics Collection**: Scrapes HTTP/HTTPS endpoints exporting Prometheus metrics format or OpenTelemetry metrics at configured scrape intervals.
- **PromQL Query Engine**: Flexible expression language to calculate rates, aggregations, percentiles, and dynamic alerting thresholds.
- **Autonomous & Local Architecture**: Single-binary operational model without external distributed storage dependencies, ensuring high reliability during network partitions.
- **FastMCP 3.1 & Agentic Observability Integration**: Native scraping of AI agent runtime metrics, token throughput, model latency, and tool invocation counts.

```
+-----------------------------------------------------------------------------------+
|                        Prometheus Scraping & Alerting Architecture                |
|                                                                                   |
|  +--------------------+    +----------------------+    +-----------------------+  |
|  | Service Discovery  |===>| Scrape Engine        |===>| Local TSDB Storage    |  |
|  | (K8s / Consul)     |    | (Pull HTTP /metrics) |    | (Chunked Head Memory) |  |
|  +--------------------+    +----------------------+    +-----------------------+  |
|                                                                    ||             |
|                                                                    \/             |
|  +-----------------------------------------------------------------------------+  |
|  |                         PromQL Query Engine & Rules Engine                  |  |
|  +-----------------------------------------------------------------------------+  |
|           ||                                                       ||             |
|           \/                                                       \/             |
|  +--------------------+                                   +--------------------+  |
|  | Grafana Dashboards |                                   | Alertmanager       |  |
|  | (Visualization)    |                                   | (PagerDuty / Slack)|  |
|  +--------------------+                                   +--------------------+  |
+-----------------------------------------------------------------------------------+
```

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

## Time-Series Monitoring Platform Comparison

| Feature | Prometheus | Datadog | VictoriaMetrics | Grafana Mimir |
| :--- | :--- | :--- | :--- | :--- |
| **Model Type** | Open-Source Autonomous TSDB | SaaS Commercial Platform | Open-Source TSDB | Cloud-Native Distributed TSDB |
| **Data Collection** | Pull-Based (Scrape) | Push Agent | Dual (Pull & Push) | Remote Write Push Receiver |
| **Query Language** | PromQL | Datadog Query Syntax | MetricsQL (PromQL Compatible)| PromQL |
| **Storage Model** | Local Compressed Blocks | Proprietary Cloud | High-Compression Local/Cloud | S3 / GCS Object Storage |
| **FastMCP 3.1 Support** | Native Metric Exporter | Custom Integration | Direct PromQL Endpoint | Remote Write Gateway |
| **Long-Term Retention**| Requires Thanos/Mimir | Managed by SaaS | Native Long-Term Engine | Native Infinite Scale |

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

Install the Prometheus Python client alongside Pydantic v2 and FastMCP:

```bash
pip install prometheus_client pydantic mcp
```

Validate configuration files using `promtool`:

```bash
promtool check config prometheus.yml
```

## CLI examples

### Verify Prometheus Rules File
Check alert rule syntax before deploying to production:
```bash
promtool check rules alerts.yml
```

### Query Instant Vector via API
Fetch current agent execution error count using `curl`:
```bash
curl -g 'http://localhost:9090/api/v1/query?query=sum(agent_requests_total{status="error"})'
```

### Evaluate PromQL Expression via promtool
Query metric rates directly from terminal:
```bash
promtool query instant http://localhost:9090 'rate(agent_requests_total[5m])'
```

## API examples

### FastMCP 3.1 Metrics Exporter Integration
This example demonstrates embedding a Prometheus metrics server directly inside a FastMCP 3.1 tool server to monitor tool execution counts and latencies.

```python
from mcp.server.fastmcp import FastMCP
from prometheus_client import Counter, Histogram, start_http_server
import time

# Start Prometheus metrics endpoint on port 8000
start_http_server(8000)

mcp = FastMCP("Observed-Agent-Tool-Server")

TOOL_EXEC_COUNTER = Counter(
    "fastmcp_tool_executions_total",
    "Total executions of FastMCP tools",
    ["tool_name", "status"]
)

TOOL_LATENCY_HISTOGRAM = Histogram(
    "fastmcp_tool_latency_seconds",
    "FastMCP tool execution duration in seconds",
    ["tool_name"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

@mcp.tool()
def execute_database_query(sql_query: str) -> str:
    """Execute a database query with Prometheus operational instrumentation."""
    start_time = time.time()
    try:
        # Simulated DB execution
        time.sleep(0.12)
        TOOL_EXEC_COUNTER.labels(tool_name="execute_database_query", status="success").inc()
        return f"Executed query: {sql_query}"
    except Exception as e:
        TOOL_EXEC_COUNTER.labels(tool_name="execute_database_query", status="error").inc()
        raise e
    finally:
        duration = time.time() - start_time
        TOOL_LATENCY_HISTOGRAM.labels(tool_name="execute_database_query").observe(duration)

if __name__ == "__main__":
    print("FastMCP Server running with Prometheus metrics on port 8000...")
    mcp.run()
```

### Python Metrics Exporter with Pydantic v2 Telemetry Validation
Prometheus scrapes metrics formatted as plain text time-series measurements. The following Python example demonstrates exposing custom AI inference and FastMCP 3.1 agent metrics using the official Prometheus Python client, validated via strict **Pydantic v2** models before recording metric observations.

```python
import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, start_http_server
from pydantic import BaseModel, Field, field_validator

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

## Operational Best Practices

### High-Cardinality Management & TSDB Tuning
1. **Control Label Cardinality**: Avoid placing dynamic user IDs, raw prompt texts, or unconstrained timestamp values in metric label dimensions. High cardinality leads to excessive TSDB index size and memory pressure.
2. **Scrape Interval vs Retention**: Standardize scrape intervals to 15 seconds for production LLM runtimes (`vLLM` / `FastMCP`). Set local retention (`--storage.tsdb.retention.time=15d`) and stream long-term metrics to Grafana Mimir or Thanos using `remote_write`.
3. **Recording Rules**: Pre-compute expensive PromQL rate calculations (e.g., `job:agent_error_rate:5m = sum(rate(agent_requests_total{status="error"}[5m])) / sum(rate(agent_requests_total[5m]))`) using Prometheus recording rules to keep Grafana dashboard load sub-second.

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
