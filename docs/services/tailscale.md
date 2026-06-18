# Tailscale

## What it is
Tailscale is a zero-config VPN that builds a secure, WireGuard-based mesh network (a "tailnet") between your devices, even behind complex firewalls and NATs. In June 2026, version **1.82** has introduced "Identity-Aware Tool Routing," allowing autonomous agents to securely traverse the tailnet using short-lived, verifiable credentials.

## What problem it solves
Managing secure remote access typically requires complex firewall rules, port forwarding, and static VPN keys. Tailscale eliminates this complexity, providing a private network overlay where devices can communicate as if they were on the same local LAN. It solves the "secure connectivity" problem for distributed homelabs, allowing cloud-hosted agents and remote devices to securely access internal services without public exposure.

## Where it fits in the stack
**Category**: Service / Infrastructure / Networking. Tailscale acts as the **secure connectivity layer**, providing the private mesh backbone that links all homelab services, agents, and user endpoints.

## Typical use cases
- **Secure Remote Management**: Accessing [Home Assistant](home-assistant.md) or [Paperless-ngx](paperless-ngx.md) from a mobile device while traveling.
- **Cross-Cloud Mesh**: Connecting a local server to a remote VPS (e.g., for [Storj](storj.md) nodes or [n8n](n8n.md) runners).
- **Agentic Tool Access**: Allowing a cloud-hosted Claude 4.8 Opus instance to securely call local APIs via a Tailscale tunnel.
- **Zero-Trust SSH**: Securely SSHing into homelab servers without managing traditional SSH keys via **Tailscale SSH**.
- **Exit Node Routing**: Routing all device traffic through a trusted home network when using untrusted public Wi-Fi.

## Strengths
- **Zero Configuration**: No manual port forwarding or key management required.
- **Identity-Based Security**: Access is tied to single sign-on (SSO) identities (e.g., via [Authentik](authentik.md)).
- **MagicDNS**: Provides stable, easy-to-remember hostnames for every device in the tailnet.
- **P2P Connectivity**: Establishes direct, encrypted tunnels between devices whenever possible, minimizing latency.
- **Tailscale Funnel**: Allows for selective, secure exposure of local services to the public internet without traditional port forwarding.

## Limitations
- **Coordination Dependency**: Relies on Tailscale's central coordination server for key exchange (unless using the open-source [Headscale](headscale.md) alternative).
- **Client Installation**: Requires the Tailscale client software to be installed on every participating device.
- **Throughput overhead**: While minimal, the user-space WireGuard implementation can have a slight performance impact compared to kernel-space alternatives on very high-speed links.

## When to use it
- When you need a secure, hassle-free VPN to connect devices across different locations and networks.
- For providing secure, private access to homelab services for family members or AI agents.
- To eliminate the need for public port forwarding and reduce the attack surface of your home network.
- When you require stable DNS names for private services across multiple sites.

## When not to use it
- If your environment prohibits the use of third-party coordination servers (consider [Headscale](headscale.md)).
- In strictly air-gapped environments with no internet access for coordination.

## Licensing and cost
- **Licensing**: Client is Open Source (BSD-3-Clause). Coordination server is proprietary (Headscale is the open-source alternative).
- **Cost**: Free tier available for personal use (up to 100 devices and 3 users as of 2026). Paid plans for enterprise features.
- **Self-hostable**: Only the client and the [Headscale](headscale.md) coordination server.

## Getting started

### Installation
Install Tailscale on Linux with a single command:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

After installation, authenticate the device:

```bash
sudo tailscale up
```

### Hello World
1. Install Tailscale on your laptop and your smartphone.
2. Log in using the same account on both.
3. Run `tailscale status` on your laptop to see your phone's Tailscale IP.
4. Ping your phone: `tailscale ping <phone-hostname>`.
5. You now have a secure, private tunnel between your devices!

## CLI examples
The `tailscale` command is the primary interface for managing the local node.

```bash
# Check the status of the tailnet
tailscale status

# Get the Tailscale IP of the current machine
tailscale ip -4

# Advertise the current machine as an exit node
sudo tailscale up --advertise-exit-node

# Check connectivity and DERP relay status
tailscale netcheck

# GA 2026: Verify SSH access for a peer
tailscale ssh --check <peer-hostname>
```

## API examples
Tailscale provides a REST API (v2) for programmatic tailnet administration.

### Python: Listing Devices via API
```python
import requests

API_KEY = "YOUR_TAILSCALE_API_KEY"
TAILNET = "your-tailnet.ts.net"

def list_devices():
    url = f"https://api.tailscale.com/api/v2/tailnet/{TAILNET}/devices"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Example usage
devices = list_devices()
for device in devices.get('devices', []):
    print(f"Device: {device['hostname']}, IP: {device['addresses'][0]}")
```

## Related tools / concepts
- [Headscale](headscale.md) — The open-source coordination server alternative.
- [Authentik](authentik.md) — For managing SSO and identity within Tailscale.
- [Home Assistant](home-assistant.md) — Frequently accessed remotely via Tailscale.
- [Paperless-ngx](paperless-ngx.md) — Secure document access over the tailnet.
- [n8n](n8n.md) — For automating tailnet administration via the Tailscale API.
- [Ollama](ollama.md) — For providing private AI services across the tailnet.
- [Nextcloud](nextcloud.md) — For private file sharing within the mesh.
- [Storj](storj.md) — For backing up tailnet-connected servers.
- [Cloudflare Mesh](cloudflare-mesh.md) — A competing zero-trust networking solution.
- [WireGuard](https://www.wireguard.com/) — The underlying protocol for Tailscale.
- [Subnet Routers](https://tailscale.com/kb/1019/subnets/) — For accessing non-Tailscale devices on a local network.

## Sources / References
- [Official Website](https://tailscale.com/)
- [Tailscale Documentation](https://tailscale.com/docs/)
- [Tailscale API Reference](https://tailscale.com/api/)
- [Headscale GitHub](https://github.com/juanfont/headscale)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
