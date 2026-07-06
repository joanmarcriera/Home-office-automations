# Tailscale

## What it is
Tailscale is a zero-config VPN that builds a secure, WireGuard-based mesh network (a "tailnet") between your devices. In July 2026, it has introduced **Identity-Aware Tool Routing**, allowing autonomous agents to securely traverse the tailnet using short-lived, verifiable credentials. It provides the secure backbone for distributed homelabs, enabling cloud-hosted agents to interact with local services as if they were on the same network.

## What problem it solves
Managing secure remote access traditionally involves complex firewall rules, manual port forwarding, and static VPN keys. Tailscale eliminates this complexity, providing a private network overlay that works across complex firewalls and NATs. It solves the "secure connectivity" problem for distributed environments, allowing **Gemma 3** agents and remote users to securely access services like [Home Assistant](home-assistant.md) without public exposure.

## Where it fits in the stack
**Category**: Service / Infrastructure / Networking. Tailscale acts as the **secure connectivity layer**, providing the private mesh backbone that links all homelab services, agents, and user endpoints. It integrates with **FastMCP 3.0** for secure, low-latency tool discovery across distributed nodes.

## Typical use cases
- **Secure Remote Management**: Accessing [Paperless-ngx](paperless-ngx.md) or [Nextcloud](nextcloud.md) from any device while traveling.
- **Cross-Cloud Mesh**: Connecting local servers to remote VPS instances for [Storj](storj.md) nodes or [n8n](n8n.md) runners.
- **Agentic Tool Access**: Allowing a cloud-hosted Claude 4.8 instance to securely call local APIs via a Tailscale tunnel.
- **Zero-Trust SSH**: Securely accessing homelab servers without traditional SSH keys via **Tailscale SSH**.
- **Exit Node Routing**: Routing traffic through a trusted home network when using untrusted public Wi-Fi.

## Strengths
- **Zero Configuration**: No manual port forwarding or key management required.
- **Identity-Based Security**: Access is tied to single sign-on (SSO) identities via [Authentik](authentik.md).
- **MagicDNS**: Provides stable, easy-to-remember hostnames for every device in the tailnet.
- **P2P Connectivity**: Establishes direct, encrypted tunnels between devices whenever possible.
- **Tailscale Funnel**: Selective, secure exposure of local services to the public internet without traditional port forwarding.

## Limitations
- **Coordination Dependency**: Relies on Tailscale's central coordination server (unless using [Headscale](headscale.md)).
- **Client Installation**: Requires the Tailscale client software on every participating device.
- **Throughput overhead**: Minimal, but user-space WireGuard can have a slight performance impact on high-speed links.

## When to use it
- When you need a secure, hassle-free VPN to connect devices across different locations and networks.
- For providing private access to homelab services for family members or **Gemma 3** agents.
- To eliminate public port forwarding and reduce the attack surface of your network.
- When you require stable DNS names for private services across multiple sites.

## When not to use it
- If your environment strictly prohibits third-party coordination servers (consider [Headscale](headscale.md)).
- In air-gapped environments with no internet access for coordination.

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

### FastMCP 3.0 Secure Tool Routing
Exposing a local service to a tailnet-connected agent.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("tailscale-tool-router");

mcp.addTool({
  name: "get_node_status",
  description: "Get status of a specific tailnet node",
  parameters: { hostname: { type: "string" } },
  execute: async ({ hostname }) => {
    // Logic to query Tailscale API or local CLI
    return { status: "online", tailscaleIP: "100.x.y.z" };
  }
});

mcp.serve();
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
- [MCP 3.0](../tools/automation_orchestration/mcp.md) — Protocol for agentic tool discovery over Tailscale.
- [FastMCP 3.0](../tools/automation_orchestration/mcp.md) — High-performance tool hosting for distributed agents.

## Sources / References
- [Official Website](https://tailscale.com/)
- [Tailscale Documentation](https://tailscale.com/docs/)
- [Tailscale API Reference](https://tailscale.com/api/)
- [Headscale GitHub](https://github.com/juanfont/headscale)

## Contribution Metadata
- Last reviewed: 2026-07-06
- Confidence: high
