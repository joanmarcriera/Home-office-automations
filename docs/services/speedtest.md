# Speedtest

## What it is
Speedtest encompasses the tools and automated workflows used to measure and log internet connection performance (download/upload bandwidth, latency, and jitter). In **July 2026**, it primarily utilizes the official **Ookla Speedtest CLI** and self-hosted dashboards like **Speedtest Tracker**, integrated with AI agents via **MCP 3.0** for proactive network troubleshooting and service-level monitoring.

## What problem it solves
Intermittent internet performance issues are difficult to diagnose without historical data. Speedtest solves the "network visibility" problem by providing periodic, objective measurements of ISP performance. It helps users verify if they are receiving the advertised speeds, identify peak-hour throttling, and provide evidence for technical support requests using an immutable audit trail of performance logs.

## Where it fits in the stack
**Category**: Service / Infrastructure / Monitoring. It acts as an **external network probe**, providing the ground-truth performance data required to optimize other services like [Plex](plex.md), [n8n](n8n.md), and autonomous agents that rely on stable, high-bandwidth connectivity for large-scale data ingestion.

## Typical use cases
- **Proactive ISP Monitoring**: Running hourly tests to track long-term bandwidth trends and latency spikes.
- **Agentic Troubleshooting**: An AI agent (e.g., **Gemma 3**) detects slow n8n execution and triggers a Speedtest to rule out network bottlenecks.
- **Dynamic QoS Optimization**: Automatically adjusting [qBittorrent](qbittorrent.md) download limits based on current available bandwidth.
- **SLA Verification**: Logging and reporting speed drops to an ISP for potential service credits.
- **Gaming/VoIP Readiness**: Verifying jitter and ping before starting high-priority low-latency tasks.

## Strengths
- **Industry Standard**: Ookla's global server network ensures reliable and comparable measurement.
- **Machine-Readable Output**: The CLI supports JSON and CSV for seamless integration with automation scripts and AI tools.
- **Low Overhead**: The official CLI is a lightweight binary that can be easily scheduled via cron or Docker.
- **Persistent Dashboards**: Tools like Speedtest Tracker provide beautiful, historical visualizations of network health.
- **Open Licensing**: The monitoring stack (Speedtest Tracker, InfluxDB, Grafana) is fully self-hostable and free for personal use.

## Limitations
- **Data Consumption**: Frequent testing on metered connections (like Starlink or mobile data) can consume significant monthly quota.
- **Local Interference**: Concurrent high-bandwidth activities on the local network (e.g., 4K streaming) will skew test results.
- **Server Variability**: Results can vary slightly depending on the proximity and load of the selected test server.
- **Proprietary CLI**: The underlying official CLI binary is proprietary and requires EULA acceptance.

## When to use it
- When you need objective, historical data on your internet connection's performance.
- To troubleshoot suspected bandwidth throttling or routing issues with your ISP.
- When building automation that needs to adapt to varying network conditions.
- To verify the health of your primary internet gateway in a homelab environment.

## When not to use it
- On extremely low-bandwidth or highly metered connections where data usage is a concern.
- During critical activities that require full bandwidth (e.g., large backups or video production).
- In environments where proprietary binaries are strictly prohibited.

## Getting started

### Installation: Official Ookla CLI
```bash
# Ubuntu/Debian
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest
```

### Self-Hosted Monitoring (Speedtest Tracker)
Deploy the tracker via Docker Compose for persistent logging:

```yaml
services:
  speedtest-tracker:
    container_name: speedtest-tracker
    image: alexjustesen/speedtest-tracker:latest
    ports:
      - 8080:80
    environment:
      - SPEEDTEST_SCHEDULE=0 * * * * # Every hour
    volumes:
      - ./config:/config
```

## CLI examples
The `speedtest` command provides granular control over the testing process.

```bash
# Run a basic test with automatic server selection
speedtest

# List nearby servers and their IDs
speedtest --servers

# Run a test against a specific server
speedtest --server-id=1234

# Output results in JSON format for scripts
speedtest --format=json
```

## API examples
Integrate Speedtest results into Python scripts for automation.

### Python: Agentic Bandwidth Check
```python
import subprocess
import json

def get_network_health():
    cmd = ["speedtest", "--format=json", "--accept-license", "--accept-gdpr"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)

    # Convert to Mbps
    down = data['download']['bandwidth'] / 125000
    up = data['upload']['bandwidth'] / 125000

    return {"download_mbps": down, "upload_mbps": up, "ping_ms": data['ping']['latency']}

# Agent uses this to decide if it should start a large data transfer
health = get_network_health()
print(f"Current Download Speed: {health['download_mbps']:.2f} Mbps")
```

## Related tools / concepts
- [InfluxDB](influxdb.md) — For storing historical speed data.
- [Grafana](grafana.md) — For visualizing network performance trends.
- [n8n](n8n.md) — For triggering alerts based on speed thresholds.
- [qBittorrent](qbittorrent.md) — Its speed can be dynamically throttled based on results.
- [Plex](plex.md) — Monitoring remote streaming capability.
- [Tailscale](tailscale.md) — Measuring performance of private mesh tunnels.
- [Home Assistant](home-assistant.md) — For displaying speedtest metrics on a home dashboard.
- [Authentik](authentik.md) — Securing the Speedtest Tracker dashboard.
- [Uptime Kuma](https://uptime.kuma.pet/) — For complementary connectivity monitoring.
- [Ollama](ollama.md) — For running agents that analyze network logs.
- [Gemma 3](../knowledge_base/models/gemma-3.md) — AI model used for proactive network troubleshooting.

## Sources / References
- [Speedtest.net Official CLI](https://www.speedtest.net/apps/cli)
- [Speedtest Tracker GitHub](https://github.com/alexjustesen/speedtest-tracker)
- [Ookla Knowledge Base](https://help.speedtest.net/hc/en-us)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-21
