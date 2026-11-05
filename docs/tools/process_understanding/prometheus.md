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

---

## Mathematical Formulation: PromQL Rate Calculation & Histogram Quantiles

### 1. Counter Rate Calculation over Range Vectors
Prometheus counters are monotonically increasing values that reset to zero upon process restart. Given a time window $[t - \Delta t, t]$ with samples $(t_1, v_1), (t_2, v_2), \dots, (t_n, v_n)$, the per-second rate calculation accounts for counter resets and sample duration extrapolation:

$$
\Delta v_{\text{adj}} = \sum_{i=1}^{n-1} \max\left(0, v_{i+1} - v_i\right)
$$

If a reset occurs ($v_{i+1} < v_i$), Prometheus assumes the counter reset to zero and rose to $v_{i+1}$. To extrapolate across the entire requested evaluation interval $\Delta t$:

$$
\text{rate}(v[\Delta t]) = \frac{\Delta v_{\text{adj}}}{t_n - t_1} \times \frac{\Delta t}{t_n - t_1 + \delta t_{\text{avg}}}
$$

Where $\delta t_{\text{avg}} = \frac{t_n - t_1}{n - 1}$ represents the average scrape interval.

### 2. Linear Approximation of Histogram Quantiles
Prometheus tracks latency distributions across predefined cumulative bucket boundaries $b_1 < b_2 < \dots < b_m = +\infty$ with cumulative sample counts $c_1 \le c_2 \le \dots \le c_m = N$.

To calculate the $\phi$-quantile ($0 < \phi \le 1$), the target rank is $R = \phi \times N$. The engine locates bucket index $k$ such that $c_{k-1} < R \le c_k$. Assuming uniform distribution of samples within bucket $[b_{k-1}, b_k]$:

$$
q_{\phi} = b_{k-1} + \left(b_k - b_{k-1}\right) \times \frac{R - c_{k-1}}{c_k - c_{k-1}}
$$

For exponential histograms (OpenTelemetry native metrics), dynamic bin scaling replaces linear interpolation, minimizing quantile estimation error under heavy-tailed latency curves.

---

## What problem it solves
- Solves the challenge of monitoring dynamic cloud-native infrastructure, Kubernetes clusters, and microservices without relying on complex external database dependencies.
- Eliminates blind spots in AI model inference runtimes by tracking real-time request counts, GPU utilization, and token latencies.
- Standardizes alert routing and multi-channel notification dispatch through Alertmanager deduplication and grouping.

---

## Where it fits in the stack
- Operates in the **Observability & Monitoring** layer of the cloud-native stack.
- Integrates directly with the Grafana LGTM suite, OpenTelemetry Collector, and FastMCP 3.1 agent runtime metrics exporters.

---

## Typical use cases
- **Kubernetes & Cloud-Native Monitoring**: Collecting node, container, pod, and service control plane metrics via kube-state-metrics and cAdvisor.
- **AI Model Inference Telemetry**: Tracking request throughput, first-token latency, GPU memory utilization, and KV cache hit ratios for vLLM, TGI, and TensorRT-LLM servers.
- **Distributed Agent Telemetry**: Monitoring agentic workflow executions, sub-task runtimes, and MCP tool failure rates across agent swarms.
- **Alerting & Escalation**: Evaluating PromQL rules against threshold criteria and routing notifications through Alertmanager to Slack, PagerDuty, or Webhooks.

---

## Time-Series Monitoring Platform Comparison

| Feature / System | Prometheus | VictoriaMetrics | Grafana Mimir | Datadog | InfluxDB 3.0 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Model Type** | Open-Source Autonomous TSDB | Open-Source TSDB | Cloud-Native Distributed TSDB | SaaS Commercial Platform | Columnar Analytical TSDB |
| **Data Collection** | Pull-Based (Scrape) | Dual (Pull & Push) | Remote Write Push Receiver | Push Agent | Push (Line Protocol / Arrow) |
| **Query Language** | PromQL | MetricsQL (PromQL Compatible)| PromQL | Datadog Query Syntax | SQL / InfluxQL |
| **Storage Model** | Local Compressed Blocks | High-Compression Local/Cloud | S3 / GCS Object Storage | Proprietary Cloud | Apache Parquet / Object Store |
| **FastMCP 3.1 Support** | Native Metric Exporter | Direct PromQL Endpoint | Remote Write Gateway | Custom Integration | Community Flight Gateway |
| **Long-Term Retention**| Requires Thanos/Mimir | Native Long-Term Engine | Native Infinite Scale | Managed by SaaS | Native Object Storage |
| **HA Architecture** | Redundant Pair Scrapes | Horizontal Clustering | Microservice Sharding | Fully Managed SaaS | Clustered Engine |

---

## Strengths
- **High Performance**: Optimized time-series storage engine handling millions of samples per second on modest CPU/RAM footprints.
- **Ecosystem Dominance**: Near-universal support across cloud platforms, ingress controllers, databases, and LLM inference runtimes.
- **Service Discovery**: Seamless auto-discovery of targets across Kubernetes, AWS EC2, Consul, Azure, and Google Cloud.
- **Autonomous Architecture**: Single binary without mandatory clustering or external database dependencies prevents observability blindness during network splits.

---

## Limitations
- **Long-Term Storage Limitations**: Local TSDB is designed for operational short-to-medium term retention; long-term analytical storage requires integration with systems like Grafana Mimir, Thanos, or Cortex.
- **No Event Logs or Traces**: Strictly focused on numeric time-series metrics; logs (Loki) and distributed traces (Tempo) require complementary tools in the Grafana LGTM stack.
- **Pull Model Edge Challenges**: Short-lived transient batch jobs or edge devices require a Pushgateway proxy for metric collection.

---

## Production Multi-Container Orchestration (`docker-compose.yml`)

The following stack deploys Prometheus, Alertmanager, Node Exporter, and Grafana with automated scraping and persistent data volumes:

```yaml
version: "3.8"

services:
  prometheus:
    image: prom/prometheus:v2.54.0
    container_name: prometheus-core
    restart: always
    user: "65534:65534"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./config/alerts.yml:/etc/prometheus/alerts.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
      - '--web.enable-lifecycle'
      - '--web.listen-address=0.0.0.0:9090'
    ports:
      - "9090:9090"
    healthcheck:
      test: ["CMD", "wget", "-q", "--tries=1", "--spider", "http://localhost:9090/-/healthy"]
      interval: 10s
      timeout: 3s
      retries: 3

  alertmanager:
    image: prom/alertmanager:v0.27.0
    container_name: alertmanager
    restart: always
    volumes:
      - ./config/alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    ports:
      - "9093:9093"

  node-exporter:
    image: prom/node-exporter:v1.8.2
    container_name: node-exporter
    restart: always
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - "9100:9100"

  grafana:
    image: grafana/grafana:11.2.0
    container_name: grafana
    restart: always
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin_secure_pass
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml:ro
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  prometheus_data:
    driver: local
  alertmanager_data:
    driver: local
  grafana_data:
    driver: local
```

---

## Service & Daemon Management (systemd Unit Configuration)

To operate Prometheus as a high-availability background monitoring service on enterprise Linux servers, deploy the systemd service configuration below at `/etc/systemd/system/prometheus.service`:

```ini
[Unit]
Description=Prometheus Time-Series Monitoring Daemon
Documentation=https://prometheus.io/docs/
After=network-online.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
WorkingDirectory=/var/lib/prometheus
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/data \
  --storage.tsdb.retention.time=15d \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries \
  --web.listen-address=0.0.0.0:9090 \
  --web.enable-lifecycle
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
LimitNOFILE=65536

# Process Hardening Measures
ProtectSystem=full
ProtectHome=read-only
NoNewPrivileges=true
ReadWritePaths=/var/lib/prometheus/data
CapabilityBoundingSet=

[Install]
WantedBy=multi-user.target
```

---

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Possible Cause | Verification Procedure | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **Scrape Target Down (`up == 0`)** | Target endpoint down, crashed, or blocked by firewall | Run `curl -v http://<target>:8000/metrics` from Prometheus host | Verify network security rules, service port, and container health status. |
| **TSDB Memory Spike / OOM** | High metric cardinality due to dynamic labels (e.g. prompt text, UUIDs) | Execute `topk(10, count by (__name__) ({__name__=~".+"}))` in PromQL | Remove high-cardinality labels from client exporter code. |
| **Out of Order Samples Dropped** | Clock skew between target exporter host and Prometheus server | Inspect `prometheus_tsdb_out_of_order_samples_total` metric | Synchronize system clocks using `chrony` or `ntp` across all worker nodes. |
| **PromQL Query Timeout** | Unindexed long-range regex aggregation over raw range vectors | Inspect Prometheus logs for `query execution timed out` | Define pre-aggregated recording rules for frequent heavy dashboard queries. |
| **WAL Corruption on Crash** | Sudden power disruption or SIGKILL before checkpoint flush | Review `/var/lib/prometheus/data/wal` log entries | Run `prometheus --storage.tsdb.wal-segment-size=32MB` or repair corrupt segment. |
| **Disk Full / TSDB Locked** | Retention time too high for local disk capacity | Check disk space via `df -h /var/lib/prometheus` | Lower retention time `--storage.tsdb.retention.time=7d` and reload config. |
| **Alertmanager Dispatch Fails** | Invalid webhook auth token or network route partition | Test Alertmanager health: `curl http://localhost:9093/-/ready` | Update `alertmanager.yml` webhook URL and reload via `curl -X POST http://localhost:9093/-/reload`. |
| **Pydantic Validation Error** | Exporter received telemetry payload with negative latency or invalid enum | Inspect FastMCP agent exporter logs | Enforce `ConfigDict(extra="forbid", frozen=True)` on telemetry models. |

---

## When to use it
- When building cloud-native observability for Kubernetes infrastructure and microservice architectures.
- When tracking real-time performance indicators and operational metrics for LLM inference servers and AI agent runtimes.
- When you require a proven, lightweight time-series database and alerting framework without mandatory cloud dependencies.

---

## When not to use it
- When you require a long-term analytical store for logs or distributed traces (use Loki or Tempo instead).
- When monitoring ephemeral, highly transient batch processes without a Pushgateway.

---

## Getting started

Install the Prometheus Python client alongside Pydantic v2 and FastMCP:

```bash
pip install prometheus_client pydantic>=2.0 fastmcp>=3.1.0 requests
```

Validate configuration files using `promtool`:

```bash
promtool check config prometheus.yml
```

---

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

---

## API examples

### FastMCP 3.1 Metrics Query Server with Pydantic v2 Validation
This example implements a FastMCP 3.1 server that queries Prometheus for system health and model throughput, validating inputs and outputs using strict **Pydantic v2** schemas (`extra="forbid"`, `frozen=True`).

```python
import time
import requests
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Prometheus-Telemetry-Gateway", version="3.1.0")

class PromQLQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prometheus_url: str = Field(default="http://localhost:9090", description="Prometheus base URL")
    query: str = Field(..., min_length=2, max_length=1000, description="PromQL expression string")
    timeout_sec: float = Field(default=10.0, ge=1.0, le=60.0)

    @field_validator("prometheus_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("prometheus_url must start with http:// or https://")
        return v.rstrip("/")

class MetricSample(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    metric: Dict[str, str]
    value: float
    timestamp: float

class PromQLQueryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    result_type: str
    samples: List[MetricSample]
    total_samples: int
    query_latency_ms: float

@mcp.tool()
async def query_prometheus_instant(
    query: str,
    prometheus_url: str = "http://localhost:9090",
    timeout_sec: float = 10.0
) -> str:
    """Executes an instant PromQL query against Prometheus and returns validated metrics."""
    req = PromQLQueryRequest(
        prometheus_url=prometheus_url,
        query=query,
        timeout_sec=timeout_sec
    )

    start_time = time.time()
    endpoint = f"{req.prometheus_url}/api/v1/query"
    params = {"query": req.query}

    try:
        res = requests.get(endpoint, params=params, timeout=req.timeout_sec)
        latency_ms = (time.time() - start_time) * 1000.0

        if res.status_code == 200:
            raw_data = res.json()
            data_body = raw_data.get("data", {})
            result_list = data_body.get("result", [])

            parsed_samples = []
            for item in result_list:
                metric_labels = item.get("metric", {})
                val_pair = item.get("value", [0, "0"])
                parsed_samples.append(
                    MetricSample(
                        metric=metric_labels,
                        timestamp=float(val_pair[0]),
                        value=float(val_pair[1])
                    )
                )

            resp = PromQLQueryResponse(
                status="success",
                result_type=data_body.get("resultType", "vector"),
                samples=parsed_samples,
                total_samples=len(parsed_samples),
                query_latency_ms=latency_ms
            )
            return resp.model_dump_json(indent=2)
        else:
            return f"Prometheus Query Failed: HTTP {res.status_code} - {res.text}"
    except Exception as e:
        return f"Prometheus Exception: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

### Python Metrics Exporter with Pydantic v2 Telemetry Validation
The following Python script exposes custom AI inference and FastMCP 3.1 agent metrics using the official Prometheus Python client, validated via strict **Pydantic v2** models before recording metric observations.

```python
import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, start_http_server
from pydantic import BaseModel, Field, field_validator, ConfigDict

# ---------------------------------------------------------------------------
# Pydantic v2 Telemetry Schema
# ---------------------------------------------------------------------------
class AgentTelemetryEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

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

---

## Operational Best Practices

### High-Cardinality Management & TSDB Tuning
1. **Control Label Cardinality**: Avoid placing dynamic user IDs, raw prompt texts, or unconstrained timestamp values in metric label dimensions. High cardinality leads to excessive TSDB index size and memory pressure.
2. **Scrape Interval vs Retention**: Standardize scrape intervals to 15 seconds for production LLM runtimes (`vLLM` / `FastMCP`). Set local retention (`--storage.tsdb.retention.time=15d`) and stream long-term metrics to Grafana Mimir or Thanos using `remote_write`.
3. **Recording Rules**: Pre-compute expensive PromQL rate calculations (e.g., `job:agent_error_rate:5m = sum(rate(agent_requests_total{status="error"}[5m])) / sum(rate(agent_requests_total[5m]))`) using Prometheus recording rules to keep Grafana dashboard load sub-second.

---

## Related tools / concepts
- **[Grafana Cloud](grafana-cloud.md)**: Directly query Prometheus metrics alongside Loki logs and Tempo traces in unified dashboards.
- **[OpenTelemetry Collector](opentelemetry-collector.md)**: Export OTel metric pipelines seamlessly into Prometheus scrapers or remote write receivers.
- **[Logfire](logfire.md)**: Operational Python tracing platform with native Prometheus metric bridges.

---

## Sources / references
- [Prometheus Official Documentation](https://prometheus.io/docs/introduction/overview/)
- [CNCF Prometheus Project Page](https://www.cncf.io/projects/prometheus/)
- [Prometheus Python Client GitHub Repository](https://github.com/prometheus/client_python)
- [Prometheus Query Language Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
