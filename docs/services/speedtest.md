# Speedtest

## What it is
Speedtest encompasses the software binaries, self-hosted services, and automated network telemetry workflows used to measure, log, and analyze internet connection performance (download/upload bandwidth, latency, jitter, and packet loss). As of **early January 2027**, it primarily utilizes the official **Ookla Speedtest CLI** and self-hosted persistent dashboards like **Speedtest Tracker**, fully integrated with AI agents via **MCP 3.1** / **FastMCP 3.1** for proactive network diagnostics, dynamic bandwidth allocation, and SLA compliance monitoring.

By combining low-overhead network probes with structured JSON outputs and FastMCP 3.1 task protocol bindings, Speedtest allows frontier models like **Claude 5.1/5.6**, **GPT-5.5/5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Qwen 3.6 VL** to autonomously evaluate local gateway performance, detect ISP throttling, and adjust dependent network workloads.

```
+-----------------------------------------------------------------------------------+
|                                 AGENT / MONITORED SERVICE                         |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  |  Claude 5.6 / GPT-5.6   |     |  Home Assistant /     |     |  n8n / Plex /   |  |
|  |  Diagnostic Agents    |     |  Grafana Dashboards   |     |  qBittorrent    |  |
|  +-----------+-----------+     +-----------+-----------+     +--------+--------+  |
|              |                             |                          |           |
+--------------|-----------------------------|--------------------------|-----------+
               |                             |                          |
               v                             v                          v
+-----------------------------------------------------------------------------------+
|                        FASTMCP 3.1 SPEEDTEST SERVER BRIDGE                        |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  | Task Correlation ID   |     | Speedtest Tracker     |     | Pydantic v2     |  |
|  | Protocol Engine       |     | REST Ingestion API    |     | Schema Guard    |  |
|  +-----------+-----------+     +-----------+-----------+     +--------+--------+  |
+--------------|-----------------------------|--------------------------|-----------+
               |                             |                          |
               v                             v                          v
+-----------------------------------------------------------------------------------+
|                           LOCAL NETWORK GATEWAY & PROBES                          |
|                                                                                   |
|  +------------------+   +------------------+   +------------------+   +---------+ |
|  | Ookla Speedtest  |   | Speedtest Tracker|   | InfluxDB / Loki  |   | Global  | |
|  | Official CLI     |   | Docker Container |   | Telemetry Store  |   | Ookla   | |
|  | Binary           |   | (Laravel/Vue)    |   |                  |   | Servers | |
|  +------------------+   +------------------+   +------------------+   +---------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Intermittent internet performance degradation and micro-outages are notoriously difficult to diagnose without structured, historical baseline telemetry. Speedtest solves the "network visibility" problem by providing periodic, objective measurements of WAN performance directly from the local gateway environment.

It enables homelab operators, enterprise sysadmins, and autonomous AI agents to:
1. Verify whether an ISP is delivering advertised download/upload bandwidth speeds.
2. Identify peak-hour network congestion or protocol-specific traffic throttling.
3. Generate immutable, timestamped audit logs for ISP service credit requests.
4. Programmatically throttle bandwidth-heavy background tasks (e.g., torrent seeding or remote backups) when available WAN capacity drops below critical thresholds.

## Where it fits in the stack
**Category**: Service / Infrastructure / Monitoring. It acts as an **external network probe**, providing ground-truth performance telemetry required to optimize other services like [Plex](plex.md), [n8n](n8n.md), and autonomous AI agents that depend on high-speed internet connectivity.

In the homelab and enterprise infrastructure stack:
1. **Agent Diagnostic Layer**: FastMCP 3.1 tool server, Claude Code, Home Assistant agents.
2. **Dashboard & Visualization Layer**: Speedtest Tracker, Grafana Loki, Grafana Cloud.
3. **Probe Execution Layer**: Ookla Speedtest CLI binary (`speedtest`).
4. **Target Endpoint**: Ookla Global Speedtest Edge Server Network.

## Typical use cases
- **Proactive ISP Monitoring**: Running scheduled hourly background tests to build long-term bandwidth trend graphs and identify latency degradation.
- **Agentic Infrastructure Troubleshooting**: An AI agent (e.g., **Claude 5.6** or **DeepSeek-V4**) detects slow n8n workflow execution or API timeouts and triggers a Speedtest tool call to isolate WAN bottlenecks.
- **Dynamic Quality of Service (QoS)**: Automatically adjusting [qBittorrent](qbittorrent.md) download/upload speed caps based on current available bandwidth measured during peak hours.
- **SLA Violation Auditing**: Automatically logging speed drops below guaranteed contractual levels and compiling monthly PDF audit reports for ISP billing disputes.
- **Pre-Flight VoIP / Streaming Verification**: Verifying ping jitter and packet loss before initializing high-priority video conferencing or live media streaming pipelines.

## Strengths
- **Industry Standard Accuracy**: Ookla's globally distributed multi-gigabit edge server network ensures accurate, comparable throughput measurements.
- **Machine-Readable JSON Output**: The official CLI supports structured `--format=json` output, making it straightforward to parse via Python scripts and FastMCP 3.1 tools.
- **Low Host Overhead**: The compiled C++ official CLI binary is lightweight and runs efficiently inside unprivileged Docker containers or cron jobs.
- **Self-Hosted Historical Dashboards**: Tools like Speedtest Tracker provide intuitive web GUIs, threshold notifications, and REST API access.
- **Rich Telemetry Data**: Measures download/upload bandwidth, idle latency, loaded latency (bufferbloat), jitter, and packet loss percentage.

## Limitations
- **WAN Bandwidth Consumption**: Running frequent tests (e.g., every 15 minutes) on high-speed gigabit lines consumes hundreds of gigabytes of data monthly, which can exhaust metered connections (Starlink, 5G home internet).
- **Local Network Interference**: Concurrent high-volume local network traffic (e.g., 4K video streams or game downloads) will artificially depress test results.
- **Server Selection Variability**: Results can fluctuate depending on the geographical distance, routing path, and current load of the automatically selected Ookla target server.
- **Proprietary CLI License**: The compiled official Ookla binary is proprietary software requiring automated license acceptance flags (`--accept-license`).

## When to use it
- When you need objective, historical data on your internet gateway's performance trends.
- To troubleshoot suspected ISP bandwidth throttling or routing issues.
- When building autonomous AI agents that need to adapt workflow execution based on active network capacity.
- To verify the performance of remote VPN tunnels ([Tailscale](tailscale.md) or WireGuard) or homelab edge routers.

## When not to use it
- On highly metered or capped connections (mobile data, satellite links) where data transfer costs are prohibitive.
- During high-priority, zero-latency activities (online gaming tournaments or live broadcasting) where test traffic would introduce latency spikes.
- In strict open-source-only environments where proprietary binaries are explicitly barred.

## Getting started

### Installation: Official Ookla CLI
Install the official Ookla binary on Linux host systems:

```bash
# Ubuntu/Debian official repository setup
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest

# Verify installation and version
speedtest --version
```

### Self-Hosted Dashboard Setup (Speedtest Tracker)
Deploy Speedtest Tracker with Docker Compose for persistent historical logging and web visualization:

```yaml
version: '3.8'

services:
  speedtest-tracker:
    container_name: speedtest-tracker
    image: alexjustesen/speedtest-tracker:latest
    ports:
      - "8080:80"
      - "8443:443"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - SPEEDTEST_SCHEDULE=0 * * * *  # Executed top of every hour
      - SPEEDTEST_SERVERS=           # Optional comma-separated server IDs
      - DISPLAY_TIMEZONE=America/New_York
    volumes:
      - ./config:/config
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3
```

## CLI examples

```bash
# 1. Run an interactive speedtest with default automatic server selection
speedtest

# 2. List nearby Ookla test servers with their explicit IDs and geographical distance
speedtest --servers

# 3. Execute a test against a specific target server ID
speedtest --server-id=12345

# 4. Generate structured JSON output for script parsing (auto-accepting licenses)
speedtest --format=json --accept-license --accept-gdpr

# 5. Measure latency under load (Bufferbloat analysis)
speedtest --format=json-pretty --accept-license
```

## API examples

### Production FastMCP 3.1 Server with Pydantic v2 Validation
This Python implementation demonstrates a production-grade FastMCP 3.1 tool server that runs the Ookla Speedtest CLI, validates JSON outputs against strict Pydantic v2 schemas, and returns actionable metrics with FastMCP 3.1 task correlation:

```python
import json
import subprocess
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 server
mcp = FastMCP("network-diagnostics-server")

class SpeedtestRequest(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 task protocol correlation ID")
    server_id: Optional[int] = Field(default=None, description="Optional specific Ookla server ID to target")
    timeout_seconds: int = Field(default=120, ge=30, le=300)

class OoklaPingMetrics(BaseModel):
    jitter: float = Field(..., description="Jitter in milliseconds")
    latency: float = Field(..., description="Idle ping latency in milliseconds")
    low: Optional[float] = Field(default=None)
    high: Optional[float] = Field(default=None)

class OoklaBandwidthMetrics(BaseModel):
    bandwidth: int = Field(..., description="Raw bandwidth in bytes per second")
    bytes: int = Field(..., description="Total bytes transferred during test")
    elapsed: int = Field(..., description="Elapsed duration in milliseconds")

    @property
    def megabits_per_second(self) -> float:
        # Convert bytes/sec to Megabits/sec (1 byte = 8 bits)
        return round((self.bandwidth * 8) / 1_000_000.0, 2)

class SpeedtestResultSchema(BaseModel):
    type: str = Field(..., description="Result type identifier")
    timestamp: str = Field(..., description="ISO 8601 execution timestamp")
    ping: OoklaPingMetrics = Field(..., description="Ping latency metrics")
    download: OoklaBandwidthMetrics = Field(..., description="Download throughput metrics")
    upload: OoklaBandwidthMetrics = Field(..., description="Upload throughput metrics")
    isp: str = Field(..., description="Detected ISP organization name")
    external_ip: str = Field(..., alias="externalIp", description="Public WAN IP address")

class StructuredNetworkReport(BaseModel):
    task_id: str
    isp: str
    public_ip: str
    download_mbps: float
    upload_mbps: float
    ping_ms: float
    jitter_ms: float
    status: str

@mcp.tool()
async def run_network_diagnostic(request_payload: Dict[str, Any]) -> str:
    """Executes local network speedtest and returns validated health metrics."""
    try:
        req = SpeedtestRequest.model_validate(request_payload)
    except ValidationError as e:
        return f"Task Rejected - Schema Violation: {e.errors()}"

    cmd = ["speedtest", "--format=json", "--accept-license", "--accept-gdpr"]
    if req.server_id is not None:
        cmd.append(f"--server-id={req.server_id}")

    try:
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=req.timeout_seconds
        )

        if process.returncode != 0:
            return f"Task {req.task_id} Failed - Speedtest CLI Error:\n{process.stderr}"

        raw_data = json.loads(process.stdout)
        validated = SpeedtestResultSchema.model_validate(raw_data)

        report = StructuredNetworkReport(
            task_id=req.task_id,
            isp=validated.isp,
            public_ip=validated.external_ip,
            download_mbps=validated.download.megabits_per_second,
            upload_mbps=validated.upload.megabits_per_second,
            ping_ms=validated.ping.latency,
            jitter_ms=validated.ping.jitter,
            status="OPTIMAL" if validated.download.megabits_per_second > 100.0 else "DEGRADED"
        )

        return report.model_dump_json(indent=2)

    except subprocess.TimeoutExpired:
        return f"Task {req.task_id} Failed: Diagnostic timed out after {req.timeout_seconds} seconds."
    except Exception as err:
        return f"Task {req.task_id} Error: {str(err)}"

if __name__ == "__main__":
    mcp.run()
```

## Solution Architecture & Monitoring Comparison

| Metric / Dimension | Speedtest Tracker | LibreSpeed (Self-Hosted) | iPerf3 (Internal Probe) | Prometheus Blackbox |
| :--- | :--- | :--- | :--- | :--- |
| **Measurement Target** | WAN Internet Speed | Local/WAN HTML5 Speed | Local LAN/WAN Throughput | HTTP/ICMP Endpoint Health |
| **Edge Network** | Ookla Global Edge | Self-Hosted Server | Custom iPerf Server | Target Endpoint |
| **FastMCP 3.1 Support**| Native Adapter Available | Custom Wrapper | Custom Wrapper | Grafana API Adapter |
| **Data Consumption** | High (Full WAN saturation)| Configurable | High | Minimal (Ping/Headers) |
| **Bufferbloat Test** | Native (Loaded Latency) | Limited | Manual Scripts | No |
| **UI & Dashboards** | Excellent (Vue/Laravel GUI)| Simple Web Page | None (CLI) | Grafana Dashboards |

## Performance & Bandwidth Consumption Benchmarks

The table below highlights typical data transfer volumes and execution times associated with Speedtest runs across common connection tiers:

| Gateway Connection Tier | Avg Test Duration | Data Used (Download) | Data Used (Upload) | Total Test Data Volume |
| :--- | :--- | :--- | :--- | :--- |
| **100 Mbps Fast Ethernet** | ~20 Seconds | ~150 MB | ~100 MB | ~250 MB |
| **500 Mbps Fiber** | ~22 Seconds | ~650 MB | ~450 MB | ~1.1 GB |
| **1 Gbps Symmetric Fiber** | ~25 Seconds | ~1.4 GB | ~1.1 GB | ~2.5 GB |
| **2.5 Gbps Multi-Gigabit**| ~28 Seconds | ~3.2 GB | ~2.8 GB | ~6.0 GB |

## Operational Runbooks & Troubleshooting

### Issue 1: Speedtest CLI Fails with License Error
- **Symptom**: FastMCP tool execution returns `To accept the license, run speedtest with --accept-license`.
- **Root Cause**: The official Ookla CLI binary requires explicit interactive or flag-based license acceptance.
- **Resolution**:
  1. Pass mandatory acceptance flags in subprocess invocation:
     ```bash
     speedtest --accept-license --accept-gdpr
     ```
  2. Or set environment variable: `export SPEEDTEST_ACCEPT_LICENSE=true`.

### Issue 2: Artificially Low Speed Measurements
- **Symptom**: 1 Gbps connection reports only 100 Mbps in automated tests.
- **Root Cause**: Network interface negotiation dropped to 100 Mbps (Fast Ethernet) due to a bad cable, or container CPU throttling limits execution.
- **Resolution**:
  1. Check host interface negotiation: `ethtool eth0 | grep Speed`.
  2. Ensure Docker container has sufficient CPU allocation (avoid strict `cpus: "0.5"` limits during multi-thread throughput tests).

### Issue 3: Speedtest Tracker API `500 Server Error`
- **Symptom**: Speedtest Tracker Web UI stops recording scheduled runs.
- **Root Cause**: SQLite database lock contention or disk full error on target host.
- **Resolution**:
  1. Inspect container logs: `docker logs speedtest-tracker --tail 100`.
  2. Restart application container: `docker compose restart speedtest-tracker`.

## Related tools / concepts
- [Grafana Cloud](../tools/process_understanding/grafana-cloud.md) — For visualizing network performance trends and telemetry.
- [Grafana Loki](../tools/process_understanding/grafana-loki.md) — For log management and bandwidth telemetry aggregation.
- [n8n](n8n.md) — For triggering alerts based on speed thresholds.
- [qBittorrent](qbittorrent.md) — Speed limits can be dynamically throttled based on results.
- [Plex](plex.md) — Monitoring remote streaming capability.
- [Tailscale](tailscale.md) — Measuring performance of private mesh tunnels.
- [Home Assistant](home-assistant.md) — Displaying speedtest metrics on a home dashboard.
- [Authentik](authentik.md) — Securing the Speedtest Tracker dashboard.
- [Ollama](ollama.md) — Running agents that analyze network logs.

## Sources / references
- [Speedtest.net Official CLI](https://www.speedtest.net/apps/cli)
- [Speedtest Tracker GitHub Repository](https://github.com/alexjustesen/speedtest-tracker)
- [Ookla CLI Documentation](https://www.speedtest.net/apps/cli)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
