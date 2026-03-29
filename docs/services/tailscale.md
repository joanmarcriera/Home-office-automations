# Tailscale

Tailscale is a zero-config VPN that makes your devices accessible from anywhere in the world.

## Description
It builds a secure WireGuard-based mesh network between your devices, even behind firewalls and NATs.

## Links
- [Official Website](https://tailscale.com/)

## Alternatives
- [ZeroTier](https://www.zerotier.com/)
- [Netmaker](https://www.netmaker.io/)

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

### Hello-world example
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

# Bring down the Tailscale connection
sudo tailscale down

# Check network connectivity and find the nearest DERP relay
tailscale netcheck
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

# Get details for a specific device by ID
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://api.tailscale.com/api/v2/device/123456789"
```

## Backlog
- Setup Tailscale Exit Node on TrueNAS SCALE.
- Configure MagicDNS for easy service access.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://tailscale.com/
- https://www.zerotier.com/
- https://www.netmaker.io/
- https://tailscale.com/docs/install/linux
- https://tailscale.com/docs/reference/tailscale-cli
- https://tailscale.com/docs/reference/tailscale-api
