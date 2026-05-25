# Headscale

Headscale is a self-hosted, open-source implementation of the Tailscale coordination server.

## What it is
It allows you to run your own Tailscale-compatible coordination server, providing full control over your mesh network's coordination layer without relying on Tailscale's SaaS offering.

## What problem it solves
It enables users to use the Tailscale client and protocol while maintaining 100% data sovereignty over their network topology and device metadata. It also removes limits on the number of devices typically found in free SaaS tiers.

## Where it fits in the stack
**Infrastructure / Networking**. It serves as the central "hub" or coordination point for a self-hosted Tailscale mesh network. It is often a core component of a [self-hosted infrastructure](../architecture/infrastructure.md) stack.

## Typical use cases
- Creating a secure, private mesh network for homelab services.
- Connecting remote devices and [Docker](../tools/infrastructure/docker.md) containers across different networks.
- Implementing OIDC-based authentication for a private VPN using [Authentik](authentik.md).
- Establishing secure communication for a [K3s cluster](../playbooks/k3s-cluster-setup.md).

## Key Features
- **Zero-Config VPN**: Leverages the Tailscale protocol for seamless connectivity.
- **NAT Traversal**: Built-in STUN/DERP support to punch through restrictive firewalls.
- **Access Control Lists (ACLs)**: Define granular permissions for device-to-device communication.
- **Multiple User Support**: Isolated namespaces for different users or projects.
- **Node Expiry**: Automatically expire node authorizations for improved security.

## Strengths
- **Data Sovereignty**: You own the coordination server and all the data it manages.
- **Tailscale Compatibility**: Works with official Tailscale clients.
- **Open Source**: Full transparency and ability to customize.
- **OIDC Support**: Integrates with identity providers like [Authentik](authentik.md).

## Limitations
- **Complexity**: Requires more manual configuration than Tailscale's SaaS.
- **Feature Lag**: Some advanced Tailscale features (like specific Tailnet Lock mechanisms) may arrive later in Headscale.
- **High Availability**: Setting up HA for Headscale is more involved than using the managed service.

## When to use it
- When you want the ease of use of Tailscale but require a fully self-hosted solution.
- For privacy-conscious environments that cannot use external coordination servers.

## When not to use it
- If you prefer a "set it and forget it" experience and don't mind the third-party coordination.
- If you require advanced enterprise features provided exclusively by Tailscale's commercial tiers.

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

# List all registered nodes
headscale nodes list

# Register a new node using a pre-auth key
headscale preauthkeys create -u myuser
```

## Advanced Configuration (ACLs)
Headscale uses HuJSON (JSON with comments) to define network policies.

```json
{
  "groups": {
    "group:admin": ["user1"],
    "group:dev":   ["user2", "user3"]
  },
  "hosts": {
    "server": "100.64.0.1"
  },
  "acls": [
    {
      "action": "accept",
      "src":    ["group:admin"],
      "dst":    ["*:*"]
    },
    {
      "action": "accept",
      "src":    ["group:dev"],
      "dst":    ["server:22", "server:80"]
    }
  ]
}
```

## API examples
Headscale provides a gRPC API and a REST API. You can interact with it via `curl` if you have a valid API key.

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

## Maintenance & Troubleshooting
- **Database Backup**: If using SQLite, ensure you backup `headscale.db` regularly.
- **DERP Servers**: If nodes struggle to connect, consider deploying a local DERP server to assist with NAT traversal.
- **Logs**: Check container logs for authentication failures or OIDC mismatch errors.

## Related tools / concepts
- [Tailscale](tailscale.md)
- [Docker](../tools/infrastructure/docker.md)
- [Authentik](authentik.md)
- [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md)
- [Infrastructure Overview](../architecture/infrastructure.md)
- [n8n Automation](n8n.md)
- [Home Assistant Integration](home-assistant.md)

## Sources / references
- [Headscale GitHub](https://github.com/juanfont/headscale)
- [Authentik Headscale Integration](https://integrations.goauthentik.io/networking/headscale/)
- [Tailscale ACL Documentation](https://tailscale.com/kb/1018/acls/)

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Contribution Metadata
- Last reviewed: 2026-05-24
- Confidence: high
