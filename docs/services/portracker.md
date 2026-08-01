# Portracker

## What it is
Portracker is a specialized network monitoring tool designed to discover and track active network ports and the services running behind them, with a focus on Docker and TrueNAS environments. It provides a live dashboard to monitor active ports on your network and discover new services. In late October / November 2026, it has been enhanced with **Agentic Discovery** capabilities, integrating with the [MCP 3.1 / FastMCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md) to provide real-time service catalogs for autonomous agents.

## What problem it solves
It provides a live, visual map of network services, helping administrators identify unexpected open ports, debug connectivity issues, and manage port assignments without manually running `nmap` scans. It eliminates the manual effort of maintaining a service registry by automatically discovering containers and virtual machines. In agentic environments, it provides the "ground truth" for service discovery, preventing agents from attempting to connect to non-existent or conflicting services.

## Where it fits in the stack
It is a **Network Observability Tool**, typically deployed at the edge of a home lab network to monitor the Docker host or the local subnet. It serves as the primary **Discovery Provider** for agentic infrastructure monitoring, feeding high-fidelity service data into RAG pipelines and automation frameworks like [n8n](n8n.md).

## Typical use cases
- **Docker Host Monitoring**: Real-time tracking of new or exposed container services.
- **Conflict Prevention**: Mapping port assignments to prevent overlapping ports during service deployment.
- **Network Auditing**: Identifying unintended open ports on IoT devices or development machines.
- **Agentic Service Discovery**: Providing a real-time service catalog for autonomous agents via [FastMCP 3.1](../tools/automation_orchestration/mcp.md).

## Strengths
- **Real-time Discovery**: Near-instant discovery of service changes and port mappings.
- **Platform Collectors**: Specialized collectors for [Docker](../tools/infrastructure/docker.md) and [TrueNAS](../architecture/infrastructure.md).
- **Lightweight & Portable**: Single binary with an embedded SQLite database, no external dependencies.
- **Peer-to-Peer Monitoring**: Supports decentralized monitoring where multiple instances can be linked without a central server.
- **Agentic Ingestion**: High-fidelity data export for AI-driven infrastructure management.

## Limitations
- **Scope**: Focused on port mapping rather than deep traffic analysis (use Suricata for IDS).
- **Privilege Requirements**: Continuous monitoring of host processes requires elevated privileges (`SYS_PTRACE`).
- **Read-only TrueNAS VMs**: VMs discovered via the TrueNAS API are read-only; full monitoring requires a local agent.

## When to use it
- When you want to monitor open ports on your network in real-time.
- To discover new services running in Docker containers or on TrueNAS SCALE.
- To avoid port conflicts in a complex homelab environment.
- As a foundation for autonomous agent service discovery and inventory management.

## When not to use it
- For deep packet inspection (DPI) or security intrusion detection.
- If you only need a one-time port scan (use `nmap`).

## Getting started

### Docker Compose
Deploy Portracker via [Docker](../tools/infrastructure/docker.md) Compose. Enable `ENABLE_AUTH` for secure access.

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
      - TRUENAS_API_KEY=your_api_key
      - TRUENAS_URL=https://your-truenas-ip/api/v2.0
    volumes:
      - ./portracker-data:/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Hello World
1. Start Portracker: `docker compose up -d`.
2. Open `http://localhost:4999` and follow the setup wizard.
3. Launch a new container (e.g., `docker run -d -p 8080:80 nginx`) and watch it appear in the dashboard within seconds.

## CLI examples
```bash
# View real-time application logs
docker logs -f portracker

# Inspect the container environment variables
docker inspect portracker --format='{{range .Config.Env}}{{println .}}{{end}}'

# Reset the internal SQLite database (DANGER: deletes all data)
docker exec -it portracker rm /data/portracker.db
```

## API examples

### Health Check
```bash
curl -X GET "http://localhost:4999/api/v1/health"
```

### Peer Status Query
```bash
curl -X GET "http://localhost:4999/api/v1/status" \
     -H "x-api-key: YOUR_PEER_API_KEY"
```

### Python (Query Active Ports with Pydantic v2 Validation)
The following script queries Portracker's Active Ports API and uses **Pydantic v2** to parse and validate the network services topology, serving as safe inputs for frontier reasoning models like Claude 5.1, GPT-5.5, or Gemini 4.0.

```python
import requests
from pydantic import BaseModel, Field
from typing import Optional, List

class PortServiceItem(BaseModel):
    port: int = Field(..., description="The network port number")
    protocol: str = Field(..., description="Network protocol (tcp, udp)")
    service_name: str = Field(..., description="Discovered service name")
    container_name: Optional[str] = Field(None, description="Docker container name if applicable")

class PortrackerApiResponse(BaseModel):
    active_ports: List[PortServiceItem] = Field(default_factory=list)

def get_active_ports(base_url: str, access_token: str) -> PortrackerApiResponse:
    url = f"{base_url}/api/v1/ports"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    raw_data = response.json()
    return PortrackerApiResponse(**raw_data)

# Example usage:
# try:
#     ports_response = get_active_ports("http://localhost:4999", "YOUR_ACCESS_TOKEN")
#     for item in ports_response.active_ports:
#         print(f"Port: {item.port} | Protocol: {item.protocol} | Service: {item.service_name}")
# except Exception as e:
#     print(f"Failed to query ports: {e}")
```

### Webhook Alerting
Portracker can send POST requests to a webhook when changes are detected:

```python
# Simple Python listener for Portracker alerts
from flask import Flask, request
app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def handle_alert():
    print(f"Alert: {request.json['message']}")
    return "OK", 200
```

## Related tools / concepts
- [Home Assistant](home-assistant.md) — For visualizing network status in a dashboard.
- [Tailscale](tailscale.md) — For secure access to the Portracker dashboard.
- [Authentik](authentik.md) — For managing SSO access.
- [n8n](n8n.md) — For automating responses to new port discoveries.
- [Docker](../tools/infrastructure/docker.md) — Primary target for monitoring.
- [TrueNAS](../architecture/infrastructure.md) — Enhanced discovery target.
- [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md) — For agentic service discovery.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — For analyzing network topology.
- [Uptime Kuma](https://uptime.kuma.pet/) — For availability monitoring.

## Sources / References
- [Portracker GitHub](https://github.com/mostafa-wahied/portracker)
- [Nmap Official Site](https://nmap.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2026-11-12
- Confidence: high
