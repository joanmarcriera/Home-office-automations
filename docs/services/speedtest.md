# Speedtest

Internet connection speed testing tools and automation.

## Description
This service covers the use of Speedtest.net CLI and related tools to monitor and log internet performance over time.

## Where it fits in the stack
**Category**: Service / Infrastructure / Monitoring

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

## When not to use it
- On metered or low-bandwidth connections where testing might consume too much quota.

## Getting started

### Installation (Official Ookla CLI)
```bash
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest
```

## CLI examples

### Run a test
```bash
speedtest
```

### Run a test and output as JSON
```bash
speedtest --format=json
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

## Related tools / concepts
- [InfluxDB](../services/influxdb.md) (for storing speed history)
- [Grafana](../services/grafana.md) (for visualizing results)

## Sources / References
- [Speedtest CLI Official](https://www.speedtest.net/apps/cli)
- [Python speedtest-cli (Community)](https://github.com/sivel/speedtest-cli)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
