# Tailscale

Tailscale is a zero-config VPN that makes your devices accessible from anywhere in the world.

## Description
It builds a secure WireGuard-based mesh network between your devices, even behind firewalls and NATs.

## When to use it
- When you need a secure, zero-config VPN to connect devices across different networks and firewalls.
- For accessing home lab services or remote servers without exposing them to the public internet.
- To establish a secure mesh network for team collaboration or CI/CD pipelines.
- For giving automation agents private access to internal services without publishing those services on the open internet.

## When not to use it
- If your environment requires a strictly hardware-based VPN solution with no third-party coordination server (though you can use [Headscale](https://github.com/juanfont/headscale) as an open-source alternative).
- For extremely high-throughput site-to-site links where dedicated leased lines or high-end hardware routers are more appropriate.

## Getting started

### Installation
On most Linux distributions, you can install Tailscale with a single command:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

After installation, authenticate the device:

```bash
sudo tailscale up
```

### Hello World
1. Install Tailscale on two different devices (e.g., your laptop and your phone).
2. Run `tailscale status` on your laptop to see your phone listed with its Tailscale IP.
3. Ping your phone using its Tailscale IP: `tailscale ping <phone-ip>`.
4. You have now established a secure connection between your devices!

## CLI examples

The `tailscale` command is used to manage the local node and view network status.

```bash
# Check the status of your tailnet and connected peers
tailscale status

# Get the Tailscale IP address of the current machine
tailscale ip -4

# Check network connectivity and find the nearest DERP relay
tailscale netcheck
```

## Home-office access patterns

Use Tailscale as a private access layer, then keep each service's own authentication enabled:

| Pattern | Use when | Notes |
| :--- | :--- | :--- |
| Device mesh | Laptops, phones, and servers need direct private access | Best default for personal devices and admin endpoints |
| Subnet router | A whole LAN segment needs to be reachable through one node | Limit advertised routes to the smallest required subnet |
| Exit node | A device needs trusted egress through home or office | Treat exit nodes as privileged network infrastructure |
| MagicDNS | Humans need stable names for private services | Pair with clear service names and avoid embedding raw IPs in docs |

For automation, prefer service-specific tokens plus Tailscale network reachability. Tailscale proves the caller is on the private network; the application still decides what that caller can do.

## Operational guardrails

- Keep admin services off public DNS unless there is a separate reason to expose them.
- Use ACLs or groups to separate family devices, lab servers, and automation runners.
- Review `tailscale status` and the admin console before assuming an old device is still trusted.
- Document which nodes advertise routes or run as exit nodes, because those nodes have higher blast radius.

## API examples

Tailscale provides a REST API (v2) for tailnet administration. You can use OAuth clients to generate access tokens.

```bash
# Generate an access token using OAuth credentials
curl -d "client_id=YOUR_CLIENT_ID" -d "client_secret=YOUR_CLIENT_SECRET" \
  "https://api.tailscale.com/api/v2/oauth/token"

# List all devices in your tailnet
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://api.tailscale.com/api/v2/tailnet/example.com/devices"
```

## Links
- [Official Website](https://tailscale.com/)

## Related tools / concepts
- [Headscale](headscale.md) (Open-source control server)
- [Cloudflare Mesh](cloudflare-mesh.md) (Alternative mesh networking)
- [Docker](../tools/infrastructure/docker.md) (Common deployment method)
- [n8n](n8n.md) (For automation workflows)
- [Home Assistant](home-assistant.md) (For IoT device networking)

## Backlog
- Setup Tailscale Exit Node on TrueNAS SCALE.
- Configure MagicDNS for easy service access.
- Add an ACL example for separating family devices from automation runners.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-07

## Sources / References
- https://tailscale.com/
- https://www.zerotier.com/
- https://www.netmaker.io/
- https://tailscale.com/docs/install/linux
- https://tailscale.com/docs/reference/tailscale-cli
- https://tailscale.com/docs/reference/tailscale-api
