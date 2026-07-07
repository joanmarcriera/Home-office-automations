# Headscale

Headscale is a self-hosted, open-source implementation of the Tailscale coordination server. As of July 2026, **v0.25.0** is the recommended baseline, introducing enhanced OIDC token rotation, a streamlined gRPC API for node management, and native support for the [Model Context Protocol (MCP 3.0)](../tools/automation_orchestration/mcp.md) Task Protocol. It serves as the backbone for private, agent-accessible mesh networks.

## What it is
It allows you to run your own Tailscale-compatible coordination server, providing full control over your mesh network's coordination layer without relying on Tailscale's SaaS offering. It is increasingly used in agentic GitOps workflows to manage secure communication between distributed [Gemma 3](../tools/ai_knowledge/local_llms.md) instances.

## What problem it solves
It enables users to use the Tailscale client and protocol while maintaining 100% data sovereignty over their network topology and device metadata. It also removes limits on the number of devices typically found in free SaaS tiers and allows for complete network isolation without third-party visibility.

## Where it fits in the stack
**Infrastructure / Networking**. It serves as the central "hub" or coordination point for a self-hosted Tailscale mesh network. It is a core component of a [self-hosted infrastructure](../architecture/infrastructure.md) stack, enabling secure communication between agents and local services.

## Typical use cases
- Creating a secure, private mesh network for homelab services.
- Connecting remote devices and [Docker](../tools/infrastructure/docker.md) containers across different networks.
- Implementing OIDC-based authentication for a private VPN using [Authentik](authentik.md).
- Establishing secure communication for a [K3s cluster](../playbooks/k3s-cluster-setup.md).
- Providing agents (Gemma 3, Claude 4.8 Opus, GPT-5.5) with secure access to internal APIs without public exposure via the [MCP 3.0](../tools/automation_orchestration/mcp.md) Task Protocol.

## Strengths
- **Data Sovereignty**: You own the coordination server and all the data it manages.
- **Tailscale Compatibility**: Works with official Tailscale clients and the latest [Tailscale](tailscale.md) protocol updates.
- **Open Source**: Full transparency and ability to customize.
- **OIDC Support**: Robust integration with identity providers like [Authentik](authentik.md).
- **Agent Friendly**: Native MCP 3.0 support allows for automated node and ACL management.

## Limitations
- **Complexity**: Requires more manual configuration than Tailscale's SaaS.
- **Feature Lag**: Some advanced Tailscale features (like specific Tailnet Lock mechanisms) may arrive later in Headscale.
- **High Availability**: Setting up HA for Headscale is more involved than using the managed service.
- **CLI Focus**: While third-party UIs exist, the primary management interface is the CLI or the gRPC API.

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
Headscale provides a gRPC API and a REST API. You can interact with it via `curl` if you have a valid API key.

### Node Management via API
```bash
# Get all nodes via the REST API
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://headscale.example.com/api/v1/node"
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
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — For agentic network orchestration.

## Sources / references
- [Headscale GitHub](https://github.com/juanfont/headscale)
- [Authentik Headscale Integration](https://integrations.goauthentik.io/networking/headscale/)
- [Tailscale ACL Documentation](https://tailscale.com/kb/1018/acls/)
- [Headscale v0.25.0 Release Notes (July 2026)](https://github.com/juanfont/headscale/releases)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
