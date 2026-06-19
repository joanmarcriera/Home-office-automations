# Portracker

## What it is
Portracker is a specialized network monitoring tool designed to discover and track active network ports and the services running behind them, with a focus on Docker and TrueNAS environments. It provides a dashboard to monitor active ports on your network and discover new services. It integrates well with TrueNAS and Docker to display native apps, virtual machines, and containers.

## What problem it solves
It provides a live, visual map of network services, helping administrators identify unexpected open ports, debug connectivity issues, and manage port assignments without manually running `nmap` scans. In a June 2026 context, it serves as a critical observability layer for "Agentic Infrastructure" where autonomous agents may spin up or scale services dynamically.

## Where it fits in the stack
It is a **Network Observability Tool**, typically deployed at the edge of a home lab network to monitor the Docker host or the local subnet. It sits alongside [Home Assistant](home-assistant.md) in the management plane.

## Typical use cases
- Monitoring a Docker host for new or exposed services.
- Mapping port assignments to prevent conflicts during service deployment.
- Auditing the local network for unintended open ports on IoT devices.
- Observability for agentic workflows (e.g., [n8n](n8n.md) or [OpenClaw](../development_ops/openclaw.md) auto-deployments).

## Strengths
- **Real-time Discovery**: Near-instant discovery of service changes and port mappings.
- **Platform Collectors**: Specialized collectors for [Docker](../tools/infrastructure/docker.md) and [TrueNAS](../../architecture/infrastructure.md).
- **Multi-node Monitoring**: Support for Peer-to-Peer monitoring and hierarchical server grouping.
- **Lightweight**: Single binary with an embedded SQLite database, no external dependencies.
- **Internal Visibility**: Distinguishes between internal container ports and published host ports.

## Limitations
- **Scope**: Focused on port mapping rather than deep traffic analysis or security intrusion detection.
- **Resource Intensity**: Continuous monitoring of host processes requires elevated privileges (`SYS_PTRACE`).
- **Read-only TrueNAS VMs**: VMs discovered via the TrueNAS API are read-only; full monitoring requires a local agent.

## When to use it
- When you want to monitor open ports on your network in real-time.
- To discover new services running in Docker containers or on TrueNAS.
- To avoid port conflicts by having a clear map of assigned ports.

## When not to use it
- For deep packet inspection or security auditing (use specialized tools like Suricata or Snort).
- If you only need a one-time port scan (use `nmap`).

## Getting started

### Docker Compose
The recommended way to deploy Portracker is via [Docker](../tools/infrastructure/docker.md) Compose. Enable `ENABLE_AUTH` for secure access.

```yaml
services:
  portracker:
    image: mostafawahied/portracker:latest
    container_name: portracker
    restart: unless-stopped
    pid: "host"
    cap_add:
      - SYS_PTRACE
      - SYS_ADMIN
    security_opt:
      - apparmor:unconfined
    ports:
      - "4999:4999"
    environment:
      - ENABLE_AUTH=true
      - SESSION_SECRET=change-this-to-a-random-string
      # Optional: TrueNAS API for enhanced discovery
      - TRUENAS_API_KEY=your_api_key
      - TRUENAS_URL=https://your-truenas-ip/api/v2.0
    volumes:
      - ./portracker-data:/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Hello World
1. Start Portracker: `docker compose up -d`.
2. Open `http://localhost:4999` in your browser.
3. If authentication is enabled, follow the setup wizard to create your admin account.
4. Observe how Portracker automatically discovers running Docker containers and their mapped ports.
5. Launch a new container (e.g., `docker run -d -p 8080:80 nginx`) and watch it appear in the dashboard within seconds.

## CLI examples
Manage the Portracker container and its environment:

```bash
# View real-time application logs
docker logs -f portracker

# Inspect the container environment variables
docker inspect portracker --format='{{range .Config.Env}}{{println .}}{{end}}'

# Reset the internal SQLite database (DANGER: deletes all data)
docker exec -it portracker rm /data/portracker.db
```

## API examples
Portracker provides internal API endpoints for health and status monitoring.

### Health Check
```bash
curl -X GET "http://localhost:4999/api/v1/health"
```

### Peer-to-Peer Status
In multi-node setups, you can query the status of a specific peer:

```bash
curl -X GET "http://localhost:4999/api/v1/status" \
     -H "x-api-key: YOUR_PEER_API_KEY"
```

### Alerting & Webhooks
Portracker can be configured to send alerts to external webhooks (e.g., Discord, Slack, or n8n) when unexpected port changes are detected.

**Simple Python Webhook Listener:**
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_alert():
    data = request.json
    print(f"Alert Received: {data['event_type']}")
    print(f"Message: {data['message']}")
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)
```

## Peer-to-Peer Monitoring
Portracker supports a decentralized monitoring model where multiple instances can be linked together.

- **Add Peers**: Link secondary Portracker instances to a primary "manager" dashboard.
- **Hierarchical Grouping**: Organize servers in a parent-child structure (e.g., nesting VM instances under their physical host).
- **Consolidated View**: View all your servers, containers, and VMs from a single dashboard without a central server.

## Related tools / concepts
- [Home Assistant](home-assistant.md) — For centralized homelab management.
- [Tailscale](tailscale.md) — For secure access to the Portracker dashboard.
- [Gitea](gitea.md) — For managing the infrastructure-as-code monitored by Portracker.
- [Syncthing](syncthing.md) — For syncing Portracker SQLite backups.
- [Storj](storj.md) — For offsite archival of network audit logs.
- [n8n](n8n.md) — For automated alerting based on port changes.
- [Authentik](authentik.md) — For managing SSO access to the dashboard.
- [Docker](../tools/infrastructure/docker.md)
- [TrueNAS](../../architecture/infrastructure.md)
- [Rclone Automation](rclone-automation.md) — For backing up Portracker data to cloud storage.
- [Kiwix](kiwix.md) — For offline access to network documentation.
- [Nextcloud](nextcloud.md) — For storing historical network maps.

## Sources / references
- [GitHub Repository](https://github.com/mostafa-wahied/portracker)
- [Nmap Project](https://nmap.org/)
- [Netdata](https://www.netdata.cloud/)
- [Uptime Kuma](https://uptime.kuma.pet/)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
