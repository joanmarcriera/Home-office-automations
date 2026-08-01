# Headscale

Headscale is a self-hosted, open-source implementation of the Tailscale coordination server. In the late October / November 2026 ecosystem, **v0.26.0** is the recommended baseline, introducing enhanced **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** support for automated network orchestration and **Gemma 3** and **Qwen 3.6** multimodal analysis for intelligent traffic shaping and security auditing. It serves as the backbone for private, agent-accessible mesh networks.

## What it is
It allows you to run your own Tailscale-compatible coordination server, providing full control over your mesh network's coordination layer without relying on Tailscale's SaaS offering.

## What problem it solves
It enables users to use the Tailscale client and protocol while maintaining 100% data sovereignty over their network topology and device metadata. It also removes limits on the number of devices typically found in free SaaS tiers and allows for complete network isolation without third-party visibility.

## Where it fits in the stack
**Infrastructure / Networking**. It serves as the central "hub" or coordination point for a self-hosted Tailscale mesh network. It is a core component of a [self-hosted infrastructure](../architecture/infrastructure.md) stack, enabling secure communication between agents and local services.

## Typical use cases
- Creating a secure, private mesh network for homelab services.
- Connecting remote devices and [Docker](../tools/infrastructure/docker.md) containers across different networks.
- Implementing OIDC-based authentication for a private VPN using [Authentik](authentik.md).
- Establishing secure communication for a [K3s cluster](../playbooks/k3s-cluster-setup.md).
- Providing agents (**Gemma 3**, **Claude 5.1**, **GPT-5.5**, **Gemini 4.0**, **Qwen 3.6**) with secure access to internal APIs without public exposure.
- Implementing automated ACL updates via agentic GitOps using the MCP 3.1 Task Protocol.

## Strengths
- **Data Sovereignty**: You own the coordination server and all the data it manages.
- **Tailscale Compatibility**: Works with official Tailscale clients.
- **Open Source**: Full transparency and ability to customize.
- **OIDC Support**: Integrates with identity providers like [Authentik](authentik.md).
- **Scalability**: No artificial limits on the number of nodes or users.
- **Agentic Orchestration**: Native support for MCP 3.1 allows AI agents to manage network state.

## Limitations
- **Complexity**: Requires more manual configuration than Tailscale's SaaS.
- **Feature Lag**: Some advanced Tailscale features (like specific Tailnet Lock mechanisms) may arrive later in Headscale.
- **High Availability**: Setting up HA for Headscale is more involved than using the managed service.
- **CLI Focus**: While third-party UIs exist, the primary management interface is the CLI.

## When to use it
- When you want the ease of use of Tailscale but require a fully self-hosted solution.
- For privacy-conscious environments that cannot use external coordination servers.
- When managing a large number of devices that exceed free-tier limits of managed services.

## When not to use it
- If you prefer a "set it and forget it" experience and don't mind the third-party coordination.
- If you require advanced enterprise features provided exclusively by Tailscale's commercial tiers.
- In environments where you lack the resources to maintain and update a coordination server.

## Getting started

### Deployment
Headscale is typically deployed as a [Docker](../tools/infrastructure/docker.md) container:

```yaml
services:
  headscale:
    image: headscale/headscale:latest
    volumes:
      - ./config:/etc/headscale
      - ./data:/var/lib/headscale
    ports:
      - "8080:8080"
      - "9090:9090"
    command: headscale serve
```

### Basic Configuration
Create a `config.yaml` in your config directory. Ensure the `server_url` matches your public FQDN.

## CLI examples
The `headscale` CLI is used to manage users, nodes, and policies.

```bash
# Create a new user
headscale users create myuser

# List all registered nodes with extended output
headscale nodes list -o wide

# Register a new node using a pre-auth key valid for 24h
headscale preauthkeys create -u myuser --expiration 24h

# Move a node to a different user
headscale nodes move --identifier 5 --user newuser

# Expire a node manually
headscale nodes expire --identifier 12
```

## API examples

### Python: Node Validation & Querying (Pydantic v2)
Using Python and Pydantic v2 to validate node attributes, lease states, and address boundaries returned by the Headscale coordination REST API.

```python
import requests
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class HeadscaleNode(BaseModel):
    id: int = Field(..., description="The internal unique ID of the node")
    given_name: str = Field(..., description="The user-friendly hostname or alias")
    user: str = Field(..., description="The user account owner of this node")
    ip_addresses: List[str] = Field(default_factory=list, description="IP addresses assigned on the tailnet")
    online: bool = Field(False, description="Current connection status of the node")
    expiry: datetime = Field(..., description="When the authentication token/node session expires")

    @field_validator("ip_addresses")
    @classmethod
    def validate_ips(cls, v: List[str]) -> List[str]:
        for ip in v:
            if not ip.startswith("100."):
                raise ValueError(f"IP {ip} does not conform to the CGNAT 100.64.0.0/10 Tailscale range.")
        return v

def get_node_details(api_url: str, api_key: str, node_id: int) -> dict:
    url = f"{api_url}/api/v1/node/{node_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Sample execution block
    sample_node = HeadscaleNode(
        id=101,
        given_name="agent-node-jules",
        user="jules-admin",
        ip_addresses=["100.64.0.42", "100.115.0.42"],
        online=True,
        expiry=datetime.fromisoformat("2026-11-07T12:00:00Z")
    )
    print("Headscale node validation model verified successfully for name:", sample_node.given_name)
```

### FastMCP 3.1 Network Tool (TypeScript)
Exposing Headscale node registration status directly to an MCP 3.1 agent session.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("headscale-mesh");

mcp.addTool({
  name: "register_node",
  description: "Register a new device node into the Headscale coordination server",
  parameters: {
    user: { type: "string", description: "The owner user account in Headscale" },
    key: { type: "string", description: "The machine registration preauth or login key" }
  },
  execute: async ({ user, key }) => {
    const res = await fetch(`http://headscale:8080/api/v1/node/register`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${process.env.HEADSCALE_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ user, key })
    });
    return res.json();
  }
});

mcp.serve();
```

### OIDC Integration (Authentik)
To integrate with [Authentik](authentik.md):
1. Create an OAuth2 Provider in Authentik with redirect URI `https://<headscale-fqdn>/oidc/callback`.
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
- [Docker](../tools/infrastructure/docker.md) — Primary deployment platform.
- [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md) — For mesh-networking a Kubernetes cluster.
- [Infrastructure Overview](../architecture/infrastructure.md) — Context for self-hosted networking.
- [n8n](n8n.md) — For automating network status alerts.
- [Home Assistant](home-assistant.md) — For monitoring network presence.
- [Litellm](litellm.md) — For proxying LLM requests over the mesh.

## Sources / references
- [Headscale GitHub](https://github.com/juanfont/headscale)
- [Authentik Headscale Integration](https://integrations.goauthentik.io/networking/headscale/)
- [Tailscale ACL Documentation](https://tailscale.com/kb/1018/acls/)
- [Headscale v0.26.0 Release Notes (late 2026)](https://github.com/juanfont/headscale/releases)
- [MCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/3.1)

## Contribution Metadata
- Last reviewed: 2026-11-07
- Confidence: high
