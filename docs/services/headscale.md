# Headscale

Headscale is a self-hosted, open-source implementation of the Tailscale coordination server. As of early January 2027, **v0.26.0+** stands as the recommended production baseline, introducing enhanced **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** support for automated agentic network orchestration, Tailscale protocol 1.80+ compatibility, and integration with multimodal agent clusters (**Claude 5.1**, **GPT-5.5/5.6**, **Gemini 4.0 Pro**, **DeepSeek-V4**) for intelligent traffic shaping, zero-trust ACL updates, and automated security auditing.

## What it is
Headscale allows you to run your own Tailscale-compatible coordination server, providing 100% control over your mesh network's control plane, IP address allocations, and node ACL policies without relying on Tailscale's SaaS infrastructure.

## What problem it solves
It enables organizations and homelab operators to use standard Tailscale client software while maintaining absolute data sovereignty over network topologies, device keys, and traffic routing. It eliminates artificial node/user limits present in free SaaS tiers and ensures complete network isolation without third-party telemetry exposure.

## Where it fits in the stack
**Category**: Infrastructure / Networking. It serves as the central coordination hub for a self-hosted overlay mesh network. It forms the core zero-trust networking layer in [self-hosted infrastructure](../architecture/infrastructure.md), allowing autonomous agents and services to communicate securely across heterogeneous cloud environments and local hardware.

## Typical use cases
- **Zero-Trust Agentic Mesh**: Creating an encrypted, private mesh network for cross-cloud AI agent clusters and local microservices.
- **Cross-Cloud Node Interconnect**: Safely linking remote edge devices, bare-metal servers, and [Docker](../tools/infrastructure/docker.md) containers across disparate networks.
- **Unified OIDC Identity Mapping**: Integrating OIDC/OAuth 2.0 authentication for VPN access using [Authentik](authentik.md).
- **Kubernetes Cluster Interconnect**: Establishing secure Pod-to-Pod or Node-to-Node transport for a multi-region [K3s cluster](../playbooks/k3s-cluster-setup.md).
- **Private API Transport**: Providing AI agents (**Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**) with secure access to non-public internal APIs without exposing ports to the internet.
- **Automated GitOps ACL Orchestration**: Automating network firewall and routing rule updates via FastMCP 3.1 agentic workflows.

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
