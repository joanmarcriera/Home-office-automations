# Speedtest

## What it is
Speedtest is a collection of internet connection speed testing tools and automation scripts. It primarily uses the official Speedtest.net (Ookla) CLI to measure network performance, including download speed, upload speed, latency, and jitter.

## What problem it solves
It allows for automated, periodic monitoring of internet performance, providing data-driven evidence of ISP service levels. It helps identify intermittent bandwidth issues, verify performance after network changes, and log historical speed data for long-term analysis.

## Where it fits in the stack
**Category**: Service / Infrastructure / Monitoring. It acts as an external probe to verify the primary internet gateway's performance.

## Typical use cases
- Monitoring ISP performance for SLA compliance.
- Logging speed drops during specific hours.
- Triggering alerts when bandwidth falls below a threshold.

## Strengths
- Industry-standard measurement.
- High-quality CLI tool available for multiple platforms.
- Supports JSON output for easy parsing.

## Limitations
- Consumes significant data during tests.
- Results can be affected by local network activity.

## When to use it
- To verify your internet connection speed programmatically.
- To build a history of network performance.
- When troubleshooting suspected ISP bandwidth throttling.

## When not to use it
- On metered or low-bandwidth connections where testing might consume too much quota.
- During critical low-latency tasks (like gaming or video calls) as it saturates the connection.

## Getting started

### Installation (Official Ookla CLI)
```bash
# Ubuntu/Debian
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest
```

### Speedtest Tracker (Self-Hosted Dashboard)
For a persistent dashboard and automated testing, it is recommended to use [Speedtest Tracker](https://github.com/alexjustesen/speedtest-tracker).

```yaml
services:
  speedtest-tracker:
    container_name: speedtest-tracker
    image: alexjustesen/speedtest-tracker:latest
    restart: unless-stopped
    ports:
      - 8080:80
      - 443:443
    environment:
      - PUID=1000
      - PGID=1000
      - SPEEDTEST_SCHEDULE=0 * * * * # Every hour
    volumes:
      - ./config:/config
```

## CLI examples

### Run a test
```bash
# Basic test with automatic server selection
speedtest

# Run test using a specific server ID
speedtest --server-id=1234
```

### Advanced Formatting
```bash
# Output as JSON for programmatic parsing
speedtest --format=json

# Output as CSV for spreadsheet import
speedtest --format=csv
```

## API examples

### Parsing results (Python)
```python
import subprocess
import json

def run_speedtest():
    result = subprocess.run(['speedtest', '--format=json'], capture_output=True, text=True)
    data = json.loads(result.stdout)

    download = data['download']['bandwidth'] / 125000  # Convert to Mbps
    upload = data['upload']['bandwidth'] / 125000      # Convert to Mbps

    print(f"Download: {download:.2f} Mbps")
    print(f"Upload: {upload:.2f} Mbps")

run_speedtest()
```

### Dashboard Visualization
To visualize speedtest results over time:
1. **Data Collection**: Use a script to run `speedtest --format=json` and send the output to InfluxDB.
2. **Setup InfluxDB**:
```bash
# Example curl to write to InfluxDB
curl -i -XPOST 'http://localhost:8086/write?db=speedtest' --data-binary "download,host=server value=$DOWNLOAD_SPEED"
```
3. **Grafana Dashboard**: Connect Grafana to InfluxDB and create a "Time Series" panel using the following query:
   - `SELECT "value" FROM "download" WHERE $timeFilter`
4. **Automation**: Schedule the script via cron to run every hour.

## Related tools / concepts
- [InfluxDB](influxdb.md)
- [Grafana](grafana.md)
- [Prometheus](https://prometheus.io/)
- [Uptime Kuma](https://uptime.kuma.pet/)
- [Netdata](https://www.netdata.cloud/)
- [Home Assistant](home-assistant.md)
- [n8n](n8n.md)
- [Rclone Automation](rclone-automation.md) — For ensuring backups don't saturate the connection during speedtests.
- [Authentik](authentik.md) — For securing the dashboard or Grafana instance.
- [Portracker](portracker.md) — To monitor ports used by Speedtest Tracker.
- [Docker](../tools/infrastructure/docker.md)

## Backlog
- [x] Perform quarterly technical freshness audit (2026-05-27).
- [x] Create a dashboard for visualizing speedtest results over time.

## Sources / References
- [Speedtest CLI Official](https://www.speedtest.net/apps/cli)
- [Python speedtest-cli (Community)](https://github.com/sivel/speedtest-cli)
- [Speedtest Tracker GitHub](https://github.com/alexjustesen/speedtest-tracker)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-27
