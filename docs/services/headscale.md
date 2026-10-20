# Headscale

Headscale is a self-hosted, open-source implementation of the Tailscale coordination server. As of early January 2027, **v0.26.0+** stands as the recommended production baseline, introducing enhanced **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** support for automated agentic network orchestration, Tailscale protocol 1.80+ compatibility, and integration with multimodal agent clusters (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**) for intelligent traffic shaping, zero-trust ACL updates, and automated security auditing.

## What it is
Headscale allows you to run your own Tailscale-compatible coordination server, providing 100% control over your mesh network's control plane, IP address allocations, and node ACL policies without relying on Tailscale's SaaS infrastructure.

## What problem it solves
It enables organizations and homelab operators to use standard Tailscale client software while maintaining absolute data sovereignty over network topologies, device keys, and traffic routing. It eliminates artificial node/user limits present in free SaaS tiers and ensures complete network isolation without third-party telemetry exposure.

## Where it fits in the stack
**Category**: Infrastructure / Networking. It serves as the central coordination hub for a self-hosted overlay mesh network. It forms the core zero-trust networking layer in [self-hosted infrastructure](../architecture/infrastructure.md), allowing autonomous agents and services to communicate securely across heterogeneous cloud environments and local hardware.

```
+-----------------------------------------------------------------------------------+
|                        HEADSCALE MESH COORDINATION TOPOLOGY                       |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   |                   HEADSCALE COORDINATION SERVER (v0.26+)                  |   |
|   |   - Control Plane & SQLite / PostgreSQL DB                                |   |
|   |   - FastMCP 3.1 Node & ACL Orchestration Gateway                          |   |
|   |   - OIDC Identity Mapping Engine (Authentik / Kanidm)                     |   |
|   +-------------------------------------+-------------------------------------+   |
+-----------------------------------------|-----------------------------------------+
                                          |
                      (WireGuard Control Plane Handshake)
                                          |
      +-----------------------------------+-----------------------------------+
      |                                   |                                   |
      v                                   v                                   v
+-----------+                       +-----------+                       +-----------+
| Edge Node | <===================> | Cloud VM  | <===================> | AI Agent  |
| (Homelab) |  (Encrypted WireGuard | (VPS)     |  (Encrypted WireGuard | Cluster   |
+-----------+   P2P Mesh Tunnels)   +-----------+   P2P Mesh Tunnels)   +-----------+
```

### Protocol & Key Exchange Sequence

```
Client Node (Tailscale)               Headscale Server              DERP Relay Node
    |                                        |                             |
    |---- 1. Register / Auth (OIDC Key) ---->|                             |
    |<--- 2. Assign WireGuard Mesh IP -------|                             |
    |     & Peer Node Public Keys            |                             |
    |                                        |                             |
    |---- 3. P2P Direct Connection Probe --------------------------------->| (If NAT Traversal Fails)
    |<=== 4. Direct Encrypted WireGuard Tunnel (P2P Mesh) ================>|
```

## Typical use cases
- **Zero-Trust Agentic Mesh**: Creating an encrypted, private mesh network for cross-cloud AI agent clusters and local microservices.
- **Cross-Cloud Node Interconnect**: Safely linking remote edge devices, bare-metal servers, and [Docker](../tools/infrastructure/docker.md) containers across disparate networks.
- **Unified OIDC Identity Mapping**: Integrating OIDC/OAuth 2.0 authentication for VPN access using [Authentik](authentik.md).
- **Kubernetes Cluster Interconnect**: Establishing secure Pod-to-Pod or Node-to-Node transport for a multi-region [K3s cluster](../playbooks/k3s-cluster-setup.md).
- **Private API Transport**: Providing AI agents (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**) with secure access to non-public internal APIs without exposing ports to the internet.
- **Automated GitOps ACL Orchestration**: Automating network firewall and routing rule updates via FastMCP 3.1 agentic workflows.

## Feature & Architecture Comparison Matrix

| Dimension | Headscale (Self-Hosted) | Tailscale SaaS | WireGuard (Standalone) | Nebula / Innernet |
| :--- | :--- | :--- | :--- | :--- |
| **Control Plane** | Self-Hosted Go Binary | Cloud Managed SaaS | None (Manual Keys) | Self-Hosted Lighthouse |
| **Data Sovereignty** | 100% On-Premises | Third-Party Telemetry | 100% On-Premises | 100% On-Premises |
| **Client Software** | Standard Tailscale Clients | Standard Tailscale Clients | Native WireGuard Tools | Dedicated Client Binaries |
| **Agentic Auth (FastMCP 3.1)**| Native gRPC / REST API Tools | Limited Admin API Keys | Scripted SSH / Key swaps | Custom Lighthouse API |
| **Node Limits** | Unlimited | Tiered Quotas | Unlimited | Unlimited |

## Strengths
- **100% Data Sovereignty**: Complete ownership of the coordination server, node keys, and routing metadata.
- **Full Tailscale Client Compatibility**: Compatible with official Tailscale clients across Linux, macOS, Windows, iOS, and Android.
- **Native FastMCP 3.1 Support**: Allows AI agents to query network topology, register nodes, and apply ACL policies via structured tool calls.
- **OIDC Integration**: Seamless single sign-on mapping via [Authentik](authentik.md), Keycloak, or Okta.
- **Uncapped Scale**: No artificial quotas on device registrations or user counts.
- **Lightweight Architecture**: Single binary backend written in Go, optimized for low overhead.

## Limitations
- **Operational Complexity**: Requires manual maintenance of public DNS, TLS certificates, and database backups compared to managed SaaS.
- **Feature Parity Lag**: Advanced proprietary Tailscale SaaS features (such as specialized enterprise Tailnet Lock variants) may lag in Headscale releases.
- **High Availability Overhead**: Multi-region database replication for HA deployment requires advanced PostgreSQL setup.
- **CLI-Centric Administration**: While third-party web UIs exist (e.g., Headscale-UI, Headplane), core administration relies primarily on the CLI or gRPC/REST APIs.

## When to use it
- When you require Tailscale's WireGuard mesh networking but demand total data sovereignty over the coordination server.
- For air-gapped or privacy-restricted environments subject to strict compliance standards.
- When managing multi-node infrastructures that exceed free SaaS account quotas.
- As the networking backbone for autonomous multi-agent systems requiring private inter-service RPC.

## When not to use it
- If you prefer a zero-maintenance, fully managed SaaS solution and accept third-party control-plane coordination.
- If your team relies exclusively on enterprise features offered solely in commercial SaaS tiers.
- When lacking resources to host and maintain a publicly reachable HTTPS server.

## Getting started

### Docker Compose
Deploying Headscale via Docker Compose for early 2027 stack environments:

```yaml
services:
  headscale:
    image: headscale/headscale:latest
    container_name: headscale
    volumes:
      - ./config:/etc/headscale
      - ./data:/var/lib/headscale
    ports:
      - "8080:8080"
      - "9090:9090"
    command: headscale serve
    restart: unless-stopped
```

### Basic Configuration
Create a `config.yaml` in your local `./config` volume directory. Ensure the `server_url` matches your public FQDN (e.g., `https://headscale.example.com`).

## CLI examples
Manage users, nodes, pre-authentication keys, and ACL policies using the `headscale` CLI:

```bash
# Create a new user namespace
docker exec headscale headscale users create homelab-user

# List all registered mesh nodes with detailed status
docker exec headscale headscale nodes list -o wide

# Generate a reusable pre-authentication key valid for 24 hours
docker exec headscale headscale preauthkeys create -u homelab-user --reusable --expiration 24h

# Move a node to a different user space
docker exec headscale headscale nodes move --identifier 5 --user new-user

# Revoke/Expire a node session manually
docker exec headscale headscale nodes expire --identifier 12
```

## FastMCP 3.1 Node & Pre-Auth Key Management Server

Below is a complete FastMCP 3.1 server implementation for programmatic Headscale node registration, pre-auth key minting, and Pydantic v2 payload validation.

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Server Tool for Headscale Control Plane Orchestration
"""

import os
import sys
import httpx
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("headscale-control-plane", version="1.4.0")

HEADSCALE_URL = os.getenv("HEADSCALE_URL", "https://headscale.example.com")
HEADSCALE_API_KEY = os.getenv("HEADSCALE_API_KEY", "default-secret-token")

class HeadscaleUser(BaseModel):
    id: str
    name: str
    created_at: Optional[str] = Field(None, alias="createdAt")

class HeadscaleNodeInfo(BaseModel):
    id: str
    name: str
    given_name: str = Field(..., alias="givenName")
    user: HeadscaleUser
    ip_addresses: List[str] = Field(..., alias="ipAddresses")
    online: bool
    last_seen: Optional[str] = Field(None, alias="lastSeen")

    @field_validator("ip_addresses")
    @classmethod
    def validate_ips(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Headscale node must be assigned at least one IP address")
        return v

class PreAuthKeyResponse(BaseModel):
    id: str
    key: str
    user: str
    reusable: bool
    expiration: str

@mcp.tool()
async def generate_agent_preauth_key(
    user_name: str,
    reusable: bool = False,
    expiration_hours: int = 24
) -> Dict[str, Any]:
    """
    Generates a new Headscale pre-authentication key for registering edge nodes or AI agents.
    """
    headers = {
        "Authorization": f"Bearer {HEADSCALE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "user": user_name,
        "reusable": reusable,
        "expiration": f"{expiration_hours}h",
        "ephemeral": False
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(f"{HEADSCALE_URL}/api/v1/preauthkey", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json().get("preAuthKey", {})

            validated_key = PreAuthKeyResponse(
                id=str(data.get("id", "0")),
                key=data.get("key", ""),
                user=data.get("user", user_name),
                reusable=data.get("reusable", reusable),
                expiration=str(data.get("expiration", ""))
            )
            return validated_key.model_dump()

        except Exception as exc:
            return {"error": f"Failed to generate pre-auth key: {str(exc)}"}

@mcp.tool()
async def list_registered_nodes() -> Dict[str, Any]:
    """
    Lists all nodes registered on the Headscale coordination mesh with active status.
    """
    headers = {"Authorization": f"Bearer {HEADSCALE_API_KEY}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(f"{HEADSCALE_URL}/api/v1/node", headers=headers)
            resp.raise_for_status()
            raw_nodes = resp.json().get("nodes", [])

            validated_nodes = [
                HeadscaleNodeInfo.model_validate(n).model_dump()
                for n in raw_nodes
            ]
            return {"nodes": validated_nodes, "total": len(validated_nodes)}

        except Exception as exc:
            return {"error": f"Failed to list Headscale nodes: {str(exc)}"}

if __name__ == "__main__":
    mcp.run()
```

## API examples

### Node and Pre-Auth Key Management (Python with Pydantic v2)
Programmatic Python script for querying registered Headscale nodes and requesting pre-authentication keys utilizing **Pydantic v2** validation.

```python
import os
from datetime import datetime
from typing import List, Optional
import requests
from pydantic import BaseModel, Field, field_validator

class NodeUser(BaseModel):
    id: str
    name: str
    created_at: datetime = Field(..., alias="createdAt")

class HeadscaleNode(BaseModel):
    id: str
    name: str
    given_name: str = Field(..., alias="givenName")
    user: NodeUser
    ip_addresses: List[str] = Field(..., alias="ipAddresses")
    online: bool
    last_seen: Optional[datetime] = Field(None, alias="lastSeen")

    @field_validator("ip_addresses")
    @classmethod
    def must_have_ips(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("Node must have at least one assigned IP address")
        return value

def get_headscale_nodes() -> List[HeadscaleNode]:
    headscale_url = os.getenv("HEADSCALE_URL", "https://headscale.example.com")
    api_key = os.getenv("HEADSCALE_API_KEY", "your_api_key_here")

    url = f"{headscale_url}/api/v1/node"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    # Parse list of nodes directly using Pydantic v2 model_validate
    data = response.json().get("nodes", [])
    return [HeadscaleNode.model_validate(node) for node in data]

if __name__ == "__main__":
    try:
        nodes = get_headscale_nodes()
        print(f"Retrieved and validated {len(nodes)} registered nodes.")
        for node in nodes:
            status = "ONLINE" if node.online else "OFFLINE"
            print(f" - [{status}] Name: {node.given_name} | User: {node.user.name} | IPs: {', '.join(node.ip_addresses)}")
    except Exception as e:
        print(f"Error querying Headscale API: {e}")
```

### OIDC Integration (Authentik)
To integrate with [Authentik](authentik.md):
1. Configure an OAuth2 Provider in Authentik with redirect URI `https://<headscale-fqdn>/oidc/callback`.
2. Update Headscale `config.yaml`:

```yaml
oidc:
  issuer: "https://<authentik-fqdn>/application/o/<application-slug>/"
  client_id: "<client-id>"
  client_secret: "<client-secret>"
  scope: ["openid", "profile", "email", "offline_access"]
```

## Production Systemd Service Unit (`headscale.service`)

For bare-metal and Linux VM hosting environments, run Headscale via systemd:

```ini
[Unit]
Description=Headscale Open-Source Tailscale Control Server
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
User=headscale
Group=headscale
WorkingDirectory=/var/lib/headscale
ExecStart=/usr/local/bin/headscale serve --config /etc/headscale/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
LimitNOFILE=65536
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/headscale /var/log/headscale

[Install]
WantedBy=multi-user.target
```

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Probable Cause | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **Nodes Stuck in Direct Connection Failure** | UDP NAT Traversal blocked or missing STUN/DERP relay | `tailscale status` / `tailscale netcheck` | Open UDP port 3478 or ensure DERP relay endpoints are reachable over HTTPS. |
| **OIDC Login Loop Callback Error** | Mismatched redirect URI in Authentik / Kanidm configuration | `journalctl -u headscale.service -f` | Verify `oidc.issuer` and client callback matching `https://headscale.domain.com/oidc/callback`. |
| **Node Key Expiration Disconnects** | Pre-auth key expired or node key explicitly revoked | `headscale nodes list` | Re-issue pre-auth key via FastMCP 3.1 tool or execute `tailscale up --login-server`. |
| **Database Lock contention (SQLite)** | High node re-auth concurrency locking SQLite file | `lsof /var/lib/headscale/db.sqlite` | Migrate database backend to PostgreSQL in `config.yaml` for production scale. |

## Operational Guardrails & Security

1. **gRPC / REST API Transport Encryption**: Expose Headscale endpoints exclusively behind an SSL-terminating reverse proxy (Nginx, Caddy, or Traefik) with TLS 1.3 enforced.
2. **Database Backup Cadence**: Automate SQLite database snapshots or PostgreSQL WAL archiving before executing Headscale binary upgrades.
3. **ACL Policy Validation**: Test HuJSON ACL policies locally before applying updates to prevent accidental administrative lockouts.

## Related tools / concepts
- [Tailscale](tailscale.md) — The commercial counterpart and protocol origin.
- [Authentik](authentik.md) — Identity provider for OIDC integration.
- [Docker](../tools/infrastructure/docker.md) — Primary container deployment platform.
- [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md) — For mesh-networking a Kubernetes cluster across environments.
- [Infrastructure Overview](../architecture/infrastructure.md) — Context for self-hosted zero-trust networking.
- [n8n](n8n.md) — For automating network change alerts.
- [Home Assistant](home-assistant.md) — For tracking physical device online presence.
- [Litellm](litellm.md) — For proxying LLM API requests across the secure mesh network.

## Sources / references
- [Headscale GitHub Repository](https://github.com/juanfont/headscale)
- [Authentik Headscale Integration Guide](https://integrations.goauthentik.io/networking/headscale/)
- [Tailscale ACL Documentation](https://tailscale.com/kb/1018/acls/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
