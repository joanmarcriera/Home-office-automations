# Tailscale

## What it is
Tailscale is a zero-config VPN that creates a secure mesh network between your devices, regardless of where they are located.

## What problem it solves
It allows you to access your homelab services securely from anywhere without having to deal with port forwarding or complex firewall rules.

## Where it fits in the pipeline
**Sync / Connect**

## Typical use cases (in this homelab / family automation context)
- **Remote Access**: Accessing Paperless-ngx or Home Assistant securely while on vacation.
- **Secure File Sync**: Allowing Syncthing to sync devices across different networks (e.g., home and office).
- **SSH Access**: Securely managing homelab servers from a mobile device.

## Integration points
- **Nextcloud / Paperless-ngx**: Provides the secure transport layer for accessing these services remotely.
- **Syncthing**: Enables peer-to-peer sync between devices that are not on the same local network.

## Licensing and cost
- **Open Source**: The client is partially open source; the coordination server is proprietary (though a self-hosted alternative, Headscale, exists).
- **Cost**: Freemium
- **Free tier**: Yes (Personal plan includes up to 100 devices and 3 users).
- **Self-hostable**: No (Coordination server is SaaS), but Headscale is a self-hostable alternative.

## Strengths
- Incredibly easy setup (it "just works").
- High performance based on the WireGuard protocol.
- Secure by default with end-to-end encryption.

## Limitations
- Central coordination server is proprietary.
- Some features require a paid subscription for larger teams.

## Alternatives / Related tools
- **ZeroTier**
- **WireGuard** (Manual setup)
- **Headscale** (Self-hosted alternative for the control server)

## Links
- [Official Website](https://tailscale.com/)
- [GitHub](https://github.com/tailscale/tailscale)
