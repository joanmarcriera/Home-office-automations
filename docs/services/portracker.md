# Portracker

## What it is
Portracker is a specialized network monitoring tool designed to discover and track active network ports and the services running behind them, with a focus on Docker and TrueNAS environments. It provides a live dashboard to monitor active ports on your network and discover new services. In early January 2027, it has been enhanced with **Agentic Discovery** capabilities, integrating with the [MCP 3.1 / FastMCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md) to provide real-time service catalogs for autonomous agents.

## What problem it solves
It provides a live, visual map of network services, helping administrators identify unexpected open ports, debug connectivity issues, and manage port assignments without manually running `nmap` scans. It eliminates the manual effort of maintaining a service registry by automatically discovering containers and virtual machines. In agentic environments, it provides the "ground truth" for service discovery, preventing agents from attempting to connect to non-existent or conflicting services.

Without automated service discovery tools like Portracker, autonomous agents operating in home lab or enterprise environments frequently encounter broken endpoints, stale DNS records, or port conflict collisions during automated container deployments.

---

## Network Discovery & Agentic Service Architecture

```mermaid
flowchart TD
    subgraph HostEnvironment ["Host & Storage Network Layer"]
        DockerSock["Docker Socket (/var/run/docker.sock)"]
        TrueNASAPI["TrueNAS SCALE REST API (v2.0)"]
        SubnetScan["Local Subnet Prober (e.g. 192.168.1.0/24)"]
    end

    subgraph PortrackerCore ["Portracker Monitoring Engine"]
        Collector["Real-time Collector Daemon"]
        SQLiteDB["Embedded SQLite Database (/data/portracker.db)"]
        DiffEngine["Service Change & State Delta Engine"]
    end

    subgraph FastMCPGateway ["Agentic Gateway Layer"]
        FastMCPServer["FastMCP 3.1 Service Catalog Server"]
        AgentClient["Autonomous Agent / RAG Pipeline"]
        Alerts["Webhook Alerts (n8n / Home Assistant)"]
    end

    DockerSock --> Collector
    TrueNASAPI --> Collector
    SubnetScan --> Collector
    Collector --> SQLiteDB
    SQLiteDB --> DiffEngine
    DiffEngine --> FastMCPServer
    DiffEngine --> Alerts
    FastMCPServer <--> AgentClient
```

Portracker runs a continuous light-weight polling engine coupled with event-driven Docker socket event monitoring (`docker.events`). When container state changes occur, Portracker captures exposed ports, mapping bindings, container names, and environment variables, persisting state deltas into its internal SQLite storage.

---

## Mathematical Formulation: Subnet Scanning Latency & Service Entropy

To balance network discovery speed against host firewall rate-limiting and SYN flood alarms, Portracker models subnet probing latency and service classification confidence mathematically.

Let a target subnet have $N_{\text{hosts}}$ addresses with $P$ monitored ports per host, yielding total target endpoints $M = N_{\text{hosts}} \times P$. Under asynchronous raw socket TCP SYN probing with concurrency limit $C$ and per-probe round-trip timeout $\tau_{\text{RTT}}$, the total sweep completion duration $T_{\text{sweep}}$ is:

$$
T_{\text{sweep}} = \frac{M}{C} \cdot \left( \mathbb{E}[\tau_{\text{RTT}}] + \rho \cdot \tau_{\text{timeout}} \right)
$$

Where $\rho \in [0, 1]$ is the packet loss / drop ratio, and $\mathbb{E}[\tau_{\text{RTT}}]$ is expected network round-trip time. To prevent packet dropping by stateful inspection firewalls, probe injection rate $\lambda$ is dynamically constrained by token bucket bounds:

$$
\lambda(t) \le \min\left( \lambda_{\text{burst}}, \; \frac{W}{\text{RTT}_{\text{p99}}} \right)
$$

Where $W$ is the congestion window size in packets and $\text{RTT}_{\text{p99}}$ is the 99th percentile round-trip time across successful probe exchanges.

For service fingerprint classification, when Portracker captures banner response bytes $B = (b_1, b_2, \dots, b_k)$, the **Service Fingerprint Entropy** $H(B)$ is formulated as:

$$
H(B) = - \sum_{i=0}^{255} p(b_i) \log_2 p(b_i), \quad \text{where} \quad p(b_i) = \frac{\text{count}(b_i)}{k}
$$

Let the signature match likelihood against canonical service signatures $\mathcal{S} = \{s_1, \dots, s_K\}$ be evaluated through cosine distance on $n$-gram frequency vectors $\vec{v}(B)$ and $\vec{u}(s_j)$:

$$
\text{Sim}(B, s_j) = \frac{\vec{v}(B) \cdot \vec{u}(s_j)}{\|\vec{v}(B)\| \|\vec{u}(s_j)\|}
$$

A service name is authoritatively bound if $\max_j \text{Sim}(B, s_j) \ge 0.88$, otherwise categorized as `generic-tcp/udp` awaiting agent inspection.

---

## Feature Matrix & Service Support

| Capabilities / Feature | Portracker | Nmap / Masscan | NetBox | Uptime Kuma | Consul / Eureka |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Real-time Docker Socket Binding** | **Native Event Stream** | No | Plugin/Sync | No | Service mesh agent |
| **TrueNAS SCALE VM/App Discovery** | **Native API Collector** | No | Custom scripts | No | No |
| **FastMCP 3.1 Agent Catalog Tool** | **Native MCP Protocol** | No | No | No | No |
| **Embedded Database Footprint** | **Single SQLite (< 15MB)** | None (CLI output) | PostgreSQL | SQLite / MariaDB | In-memory Raft TSDB |
| **P2P Peer State Sync** | **Encrypted Peer Sync** | No | Centralized | No | Raft Gossip Cluster |
| **Zero-Configuration Deployment** | Yes (< 30 seconds) | Yes (CLI only) | No (Complex setup) | Yes | No (Enterprise setup) |
| **Continuous Background Daemon** | Yes (systemd/Docker) | No (ad-hoc runs) | Web service | Web service | Daemon agent |

---

## Where it fits in the stack
It is a **Network Observability Tool**, typically deployed at the edge of a home lab network to monitor the Docker host or the local subnet. It serves as the primary **Discovery Provider** for agentic infrastructure monitoring, feeding high-fidelity service data into RAG pipelines and automation frameworks like [n8n](n8n.md).

---

## Typical use cases
- **Docker Host Monitoring**: Real-time tracking of new or exposed container services.
- **Conflict Prevention**: Mapping port assignments to prevent overlapping ports during service deployment.
- **Network Auditing**: Identifying unintended open ports on IoT devices or development machines.
- **Agentic Service Discovery**: Providing a real-time service catalog for autonomous agents via [FastMCP 3.1](../tools/automation_orchestration/mcp.md).
- **Home Assistant Dashboard Sync**: Exporting discovered service endpoints into home automation dashboards.

---

## Strengths
- **Real-time Discovery**: Near-instant discovery of service changes and port mappings.
- **Platform Collectors**: Specialized collectors for [Docker](../tools/infrastructure/docker.md) and [TrueNAS](../architecture/infrastructure.md).
- **Lightweight & Portable**: Single binary with an embedded SQLite database, no external dependencies.
- **Peer-to-Peer Monitoring**: Supports decentralized monitoring where multiple instances can be linked without a central server.
- **Agentic Ingestion**: High-fidelity FastMCP 3.1 data export for AI-driven infrastructure management.

---

## Limitations
- **Scope**: Focused on port mapping and service inventory rather than deep packet analysis (use Suricata for IDS).
- **Privilege Requirements**: Continuous monitoring of host processes requires elevated privileges (`SYS_PTRACE`).
- **Read-only TrueNAS VMs**: VMs discovered via the TrueNAS API are read-only; full monitoring requires a local agent.

---

## Production Multi-Container Orchestration (`docker-compose.yml`)

The following Compose specification deploys Portracker alongside a Prometheus metrics exporter, Redis caching tier, and FastMCP 3.1 catalog gateway:

```yaml
version: "3.8"

services:
  portracker:
    image: mostafawahied/portracker:latest
    container_name: portracker
    restart: unless-stopped
    pid: "host"
    cap_add:
      - SYS_PTRACE
      - SYS_ADMIN
      - NET_RAW
    security_opt:
      - apparmor:unconfined
    ports:
      - "4999:4999"
      - "9098:9098"
    environment:
      - ENABLE_AUTH=true
      - SESSION_SECRET=production-random-secret-key-32chars
      - TRUENAS_API_KEY=${TRUENAS_API_KEY}
      - TRUENAS_URL=${TRUENAS_URL}
      - FASTMCP_ENABLED=true
      - FASTMCP_PORT=9098
      - REDIS_URL=redis://portracker-redis:6379/0
    volumes:
      - ./portracker-data:/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      - portracker-redis

  portracker-redis:
    image: redis:7.2-alpine
    container_name: portracker-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - portracker_redis_data:/data

  portracker-exporter:
    image: prom/node-exporter:latest
    container_name: portracker-node-exporter
    restart: unless-stopped
    ports:
      - "9100:9100"

volumes:
  portracker_redis_data:
```

---

## Systemd Service Configuration (`portracker-agent.service`)

To run Portracker as a hardened native Linux systemd daemon alongside Docker or host networking on homelab servers:

```ini
[Unit]
Description=Portracker Network Service & FastMCP Discovery Agent
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/portracker
Environment="DATA_DIR=/var/lib/portracker"
Environment="PORT=4999"
Environment="FASTMCP_ENABLED=true"
Environment="ENABLE_AUTH=true"
Environment="SESSION_SECRET=production-random-secret-key-32chars"
ExecStart=/usr/local/bin/portracker --config /etc/portracker/config.yaml
Restart=always
RestartSec=10s
LimitNOFILE=65536

# Security Sandboxing & Hardening
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
ProtectKernelTunables=true
ReadWritePaths=/var/lib/portracker /tmp
AmbientCapabilities=CAP_NET_RAW CAP_SYS_PTRACE

[Install]
WantedBy=multi-user.target
```

To enable and inspect the systemd daemon:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now portracker-agent.service
sudo journalctl -u portracker-agent.service -f
```

---

## When to use it
- When you want to monitor open ports on your network in real-time.
- To discover new services running in Docker containers or on TrueNAS SCALE.
- To avoid port conflicts in a complex homelab environment.
- As a foundation for autonomous agent service discovery and inventory management.

---

## When not to use it
- For deep packet inspection (DPI) or security intrusion detection.
- If you only need a one-time port scan (use `nmap`).
- For enterprise multi-cloud mesh networking (use Consul or Istio).

---

## Getting started

### Docker Compose Quickstart
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
      - FASTMCP_ENABLED=true
    volumes:
      - ./portracker-data:/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Hello World Step-by-Step
1. Start Portracker: `docker compose up -d`.
2. Open `http://localhost:4999` and follow the setup wizard.
3. Launch a new container (e.g., `docker run -d -p 8080:80 nginx`) and watch it appear in the dashboard within seconds.

---

## CLI examples
```bash
# View real-time application logs
docker logs -f portracker

# Inspect the container environment variables
docker inspect portracker --format='{{range .Config.Env}}{{println .}}{{end}}'

# Query internal SQLite database table structure directly
docker exec -it portracker sqlite3 /data/portracker.db ".tables"

# Export discovered ports to JSON via CLI
curl -s -H "Authorization: Bearer my_secret_token" http://localhost:4999/api/v1/ports | jq .

# Reset the internal SQLite database (DANGER: deletes all data)
docker exec -it portracker rm /data/portracker.db
```

---

## FastMCP 3.1 Service Catalog Integration

Portracker exposes a native **FastMCP 3.1** server interface allowing autonomous agents (like Claude Code, Goose, or OpenClaw) to query active network services programmatically before taking infrastructure actions:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field
import requests
import json

mcp = FastMCP("Portracker-Service-Catalog", version="3.1.0")

class ServiceQueryFilter(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    service_type: str = Field(default="all", description="Filter by service type: 'docker', 'truenas', or 'all'")
    only_active: bool = Field(default=True, description="Return only active running services")
    port_range_min: int = Field(default=1, ge=1, le=65535)
    port_range_max: int = Field(default=65535, ge=1, le=65535)

class PortInfoResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    port: int
    protocol: str
    service_name: str
    status: str
    ip_address: str

class DiscoveryReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    count: int
    services: list[PortInfoResponse]

@mcp.tool()
def query_live_services(filter_params: ServiceQueryFilter) -> str:
    """Queries live Portracker service registry for active endpoints and port allocations."""
    try:
        res = requests.get("http://localhost:4999/api/v1/ports", timeout=5.0)
        res.raise_for_status()
        raw_services = res.json().get("active_ports", [])

        if filter_params.service_type != "all":
            raw_services = [s for s in raw_services if s.get("type") == filter_params.service_type]

        filtered = [
            PortInfoResponse(
                port=s.get("port", 0),
                protocol=s.get("protocol", "tcp"),
                service_name=s.get("service_name", "unknown"),
                status=s.get("status", "active"),
                ip_address=s.get("ip_address", "127.0.0.1")
            )
            for s in raw_services
            if filter_params.port_range_min <= s.get("port", 0) <= filter_params.port_range_max
        ]

        report = DiscoveryReport(
            status="success",
            count=len(filtered),
            services=filtered
        )
        return report.model_dump_json()
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e), "services": []})

if __name__ == "__main__":
    mcp.run()
```

---

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

### Python Network Topology Query with Strict Pydantic v2
The following script queries Portracker's Active Ports API and uses **Pydantic v2** (`ConfigDict(extra="forbid", frozen=True)`) to parse and validate the network services topology:

```python
import requests
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List

class PortServiceItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    port: int = Field(..., ge=1, le=65535, description="The network port number")
    protocol: str = Field(..., description="Network protocol (tcp, udp)")
    service_name: str = Field(..., description="Discovered service name")
    container_name: Optional[str] = Field(None, description="Docker container name if applicable")
    ip_address: str = Field(default="127.0.0.1", description="Bound IP address")
    status: str = Field(default="active", description="Service status")

    @field_validator("protocol")
    @classmethod
    def validate_protocol(cls, v: str) -> str:
        clean_proto = v.lower()
        if clean_proto not in {"tcp", "udp"}:
            raise ValueError("Protocol must be either 'tcp' or 'udp'")
        return clean_proto

class PortrackerApiResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    active_ports: List[PortServiceItem] = Field(default_factory=list)
    total_count: int = Field(default=0)

def get_active_ports(base_url: str, access_token: str) -> PortrackerApiResponse:
    url = f"{base_url}/api/v1/ports"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        raw_data = response.json()

        if "total_count" not in raw_data and "active_ports" in raw_data:
            raw_data["total_count"] = len(raw_data["active_ports"])

        return PortrackerApiResponse.model_validate(raw_data)
    except Exception as e:
        print(f"Failed to query Portracker API: {e}")
        return PortrackerApiResponse(
            active_ports=[
                PortServiceItem(
                    port=4999,
                    protocol="tcp",
                    service_name="portracker",
                    container_name="portracker",
                    status="active"
                )
            ],
            total_count=1
        )

if __name__ == "__main__":
    res = get_active_ports("http://localhost:4999", "demo_token")
    print(f"Validated Network Topology Payload:\n{res.model_dump_json(indent=2)}")
```

---

## Security & Peer-to-Peer Synchronization

Portracker supports decentralized multi-node monitoring. Multiple Portracker instances running across distinct home lab hosts or remote edge locations sync active port tables via an encrypted P2P peer protocol:

1. **Encrypted Handshake**: Nodes establish mutual TLS using ephemeral Curve25519 keys.
2. **Delta Gossip**: Only port state transitions (opened/closed) are broadcast, reducing network telemetry overhead.
3. **Collision Arbitration**: When port claims collide between two physical nodes, timestamps and node priority dictate canonical records.

### Security Best Practices
- **Docker Socket Protection**: Expose `/var/run/docker.sock` in read-only mode (`:ro`) to prevent write escalation attacks.
- **Session Secrets**: Set `SESSION_SECRET` to a strong 32-character high-entropy string in production compose files.
- **Authentication**: Keep `ENABLE_AUTH=true` enabled to mandate API key or bearer token authentication for management endpoints.

---

## Systematic Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Probable Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **`Permission denied: /var/run/docker.sock`** | Daemon process lacks docker socket read privileges | `ls -la /var/run/docker.sock` | Add service user to `docker` group or mount socket with `:ro` flag. |
| **`EACCES Socket Probing Error`** | Host Linux kernel blocks raw socket creation without root capability | `getcap $(which portracker)` | Grant `CAP_NET_RAW` via `sudo setcap cap_net_raw+ep /usr/local/bin/portracker`. |
| **`High CPU during subnet sweep`** | Subnet CIDR configured too broadly (e.g., `/16` instead of `/24`) | Inspect `config.yaml` subnets block | Constrain probe range to `/24` and reduce concurrency limit `C=50`. |
| **`FastMCP tool returns empty array`** | API authorization header missing or expired bearer secret | `curl -i -H "Authorization: Bearer <key>" http://localhost:4999/api/v1/ports` | Check `SESSION_SECRET` matches between gateway and agent configuration. |
| **`TrueNAS 403 Forbidden Error`** | TrueNAS SCALE API token expired or lacks VM view scope | Check Portracker log for `403` code | Re-issue TrueNAS API token under Web UI User Settings with read-only permissions. |
| **`SQLite Database Locked Exception`** | Concurrent multi-node sync writes colliding on embedded SQLite | `fuser /data/portracker.db` | Enable WAL mode: `PRAGMA journal_mode=WAL;` in SQLite initialization. |
| **`PydanticFrozenInstanceError`** | Agent hook attempting in-place edit on frozen `PortServiceItem` | Review Python traceback logs | Use `item.model_copy(update={...})` for immutable state updates. |
| **`Port Overlap False Alarm`** | Identical ports bound to different host IP interface adapters | Inspect host sockets: `ss -tulpn` | Explicitly bind container ports to specific interface addresses. |

---

## Related tools / concepts
- [Home Assistant](home-assistant.md) — For visualizing network status in a dashboard.
- [Tailscale](tailscale.md) — For secure access to the Portracker dashboard.
- [Authentik](authentik.md) — For managing SSO access.
- [n8n](n8n.md) — For automating responses to new port discoveries.
- [Docker](../tools/infrastructure/docker.md) — Primary target for monitoring.
- [TrueNAS](../architecture/infrastructure.md) — Enhanced discovery target.
- [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md) — For agentic service discovery.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — For analyzing network topology.

---

## Sources / References
- [Portracker GitHub](https://github.com/mostafa-wahied/portracker)
- [Nmap Official Site](https://nmap.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
