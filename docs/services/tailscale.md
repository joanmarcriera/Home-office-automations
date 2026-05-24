# Tailscale

## What it is
Tailscale is a zero-config VPN that builds a secure WireGuard-based mesh network between your devices, even behind firewalls and NATs. It makes your devices accessible from anywhere in the world as if they were on the same local network.

## What problem it solves
It simplifies complex network configurations like port forwarding, VPN server management, and NAT traversal. It provides a secure way to access internal services (like Home Assistant, NAS, or dev environments) from outside the home or office without exposing them to the public internet.

## Where it fits in the stack
**Category**: Service / Infrastructure / Networking. Tailscale acts as the primary secure connectivity layer for remote access and inter-node communication across different locations.

## Typical use cases
- Accessing home lab services (TrueNAS, Paperless, etc.) from a mobile device while traveling.
- Connecting remote nodes (e.g., a VPS and a home server) into a single private network.
- Securely sharing internal services with family members or colleagues.
- Providing a private tunnel for automation agents to reach internal APIs.

## Strengths
- **Zero Configuration**: No need to manage complex VPN keys or firewall rules.
- **Secure**: Built on WireGuard, with automatic key rotation and encrypted tunnels.
- **Mesh Connectivity**: Devices connect directly to each other whenever possible, minimizing latency.
- **MagicDNS**: Provides stable, easy-to-remember hostnames for all devices.

## Limitations
- **Coordination Server**: Relies on a central coordination server (though data is encrypted and doesn't pass through it).
- **Client Software Required**: Every participating device must have the Tailscale client installed.

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

### TrueNAS SCALE: Exit Node Setup
To use your TrueNAS SCALE server as a Tailscale Exit Node (routing all your traffic through your home network while away):

1.  **Install the Tailscale App**: Navigate to **Apps > Discover Apps** and search for "Tailscale".
2.  **Authentication**: During installation, provide your Auth Key or follow the login URL in the logs.
3.  **Enable Routing**: In the Tailscale app configuration on TrueNAS, ensure "Userspace" is unchecked (if possible) and that the container has permissions for IP forwarding.
4.  **Advertise Exit Node**:
    - Exec into the Tailscale pod or use the extra args field:
    ```bash
    tailscale up --advertise-exit-node
    ```
5.  **Approve in Admin Console**:
    - Go to the [Tailscale Admin Console](https://login.tailscale.com/admin/machines).
    - Find your TrueNAS machine.
    - Click **Edit Route Settings** and check **Exit Node**.
6.  **Usage**: On your client device (phone/laptop), select your TrueNAS server as the "Exit Node" in the Tailscale menu.

### MagicDNS Configuration
MagicDNS allows you to access your devices using short, stable hostnames instead of IP addresses.

1.  **Enable MagicDNS**: In the [Tailscale Admin Console](https://login.tailscale.com/admin/dns), toggle **MagicDNS** to ON.
2.  **Nameservers**: Add global nameservers (e.g., Cloudflare `1.1.1.1` or Google `8.8.8.8`) to ensure public DNS resolution continues to work while connected.
3.  **Search Domains**: Configure search domains if you want to use custom suffixes for your tailnet devices.
4.  **Usage**: You can now reach your TrueNAS server at `http://truenas` or `http://truenas.your-tailnet.ts.net` instead of its private IP.

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

### Advanced ACLs (Tag-based Access Control)
Use ACLs to enforce least-privilege access across your tailnet. Prefer tags over individual user emails for automation and server nodes.

```json
{
  "groups": {
    "group:admin": ["alice@example.com"],
    "group:family": ["bob@example.com", "carol@example.com"]
  },
  "tags": {
    "tag:automation": ["alice@example.com"],
    "tag:server":     ["alice@example.com"]
  },
  "acls": [
    // Admins can access everything
    {"action": "accept", "src": ["group:admin"], "dst": ["*:*"]},

    // Family can only access the media server (Jellyfin/Plex)
    {"action": "accept", "src": ["group:family"], "dst": ["tag:server:8096", "tag:server:32400"]},

    // Automation runners can access specific internal APIs
    {"action": "accept", "src": ["tag:automation"], "dst": ["tag:server:5678", "tag:server:8080"]}
  ]
}
```

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
- [Headscale](headscale.md)
- [Cloudflare Mesh](cloudflare-mesh.md)
- [Docker](../tools/infrastructure/docker.md)
- [n8n](n8n.md)
- [Home Assistant](home-assistant.md)
- [TrueNAS SCALE](https://www.truenas.com/truenas-scale/)
- [Nextcloud](nextcloud.md)
- [WireGuard](https://www.wireguard.com/)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15

## Sources / References
- https://tailscale.com/
- https://www.zerotier.com/
- https://www.netmaker.io/
- https://tailscale.com/docs/install/linux
- https://tailscale.com/docs/reference/tailscale-cli
- https://tailscale.com/docs/reference/tailscale-api
