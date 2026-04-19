# Headscale

Headscale is a self-hosted, open-source implementation of the Tailscale coordination server.

## What it is
It allows you to run your own Tailscale-compatible coordination server, providing full control over your mesh network's coordination layer without relying on Tailscale's SaaS offering.

## What problem it solves
It enables users to use the Tailscale client and protocol while maintaining 100% data sovereignty over their network topology and device metadata. It also removes limits on the number of devices typically found in free SaaS tiers.

## Where it fits in the stack
**Infrastructure / Networking**. It serves as the central "hub" or coordination point for a self-hosted Tailscale mesh network.

## Typical use cases
- Creating a secure, private mesh network for homelab services.
- Connecting remote devices and servers without a third-party SaaS provider.
- Implementing OIDC-based authentication for a private VPN.

## Strengths
- **Data Sovereignty**: You own the coordination server and all the data it manages.
- **Tailscale Compatibility**: Works with official Tailscale clients.
- **Open Source**: Full transparency and ability to customize.
- **OIDC Support**: Integrates with identity providers like Authentik.

## Limitations
- **Complexity**: Requires more manual configuration than Tailscale's SaaS.
- **Feature Lag**: Some advanced Tailscale features (like specific Tailnet Lock mechanisms) may arrive later in Headscale.

## When to use it
- When you want the ease of use of Tailscale but require a fully self-hosted solution.
- For privacy-conscious environments that cannot use external coordination servers.

## When not to use it
- If you prefer a "set it and forget it" experience and don't mind the third-party coordination.
- If you require advanced enterprise features provided exclusively by Tailscale's commercial tiers.

## Getting started

### Deployment
Headscale is typically deployed as a Docker container:

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

## API examples
Headscale provides a gRPC API and a REST API (via a proxy if needed). Most management is done via the CLI or integrated dashboards.

### OIDC Integration (Authentik)
To integrate with Authentik:
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
- [Tailscale](tailscale.md)
- [WireGuard](https://www.wireguard.com/)
- [Authentik](authentik.md)

## Sources / references
- [Headscale GitHub](https://github.com/juanfont/headscale)
- [Authentik Headscale Integration](https://integrations.goauthentik.io/networking/headscale/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
