# Portracker

## What it is
Portracker is a specialized network monitoring tool designed to discover and track active network ports and the services running behind them, with a focus on Docker and TrueNAS environments. It provides a dashboard to monitor active ports on your network and discover new services. It integrates well with TrueNAS and Docker to display native apps, virtual machines, and containers.

## What problem it solves
It provides a live, visual map of network services, helping administrators identify unexpected open ports, debug connectivity issues, and manage port assignments without manually running `nmap` scans.

## Where it fits in the stack
It is a **Network Observability Tool**, typically deployed at the edge of a home lab network to monitor the Docker host or the local subnet.

## Typical use cases
- Monitoring a Docker host for new or exposed services.
- Mapping port assignments to prevent conflicts during service deployment.
- Auditing the local network for unintended open ports on IoT devices.

## Strengths
- **Real-time**: Near-instant discovery of service changes.
- **Visual**: Clean dashboard for quick assessment.
- **Docker-native**: Deep integration with the Docker socket for container metadata.

## Limitations
- **Scope**: Focused on port mapping rather than deep traffic analysis or security intrusion detection.
- **Resource Intensity**: Continuous monitoring of host processes requires elevated privileges (`SYS_PTRACE`).

## When to use it
- When you want to monitor open ports on your network in real-time.
- To discover new services running in Docker containers or on TrueNAS.
- To avoid port conflicts by having a clear map of assigned ports.

## When not to use it
- For deep packet inspection or security auditing (use specialized tools like Suricata or Snort).
- If you only need a one-time port scan (use `nmap`).

## Getting started

### Docker Compose
The recommended way to deploy Portracker is via Docker Compose. Enable `ENABLE_AUTH` for secure access.

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

## Links
- [GitHub Repository](https://github.com/mostafa-wahied/portracker)

## Related tools / concepts
- [Home Assistant](home-assistant.md)
- [Tailscale](tailscale.md)
- [Gitea](gitea.md)
- [Syncthing](syncthing.md)
- [Storj](storj.md)
- [Netdata](https://www.netdata.cloud/)
- [Uptime Kuma](https://uptime.kuma.pet/)
- [nmap](https://nmap.org/)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15

## Sources / References
- https://github.com/mostafa-wahied/portracker
- https://nmap.org/
- https://www.netdata.cloud/
