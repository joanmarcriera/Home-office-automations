# Tailscale Service Documentation

## Service Overview
Tailscale is a zero-config VPN that creates a secure mesh network between your devices.

## Purpose / Business Value
Provides secure, encrypted remote access to the home lab without the need for port forwarding. Essential for managing services on the go and ensuring private communication between nodes.

## Why Self-Hosted
While the coordination server is cloud-based, the nodes run locally on TrueNAS and other devices, ensuring end-to-end encrypted peer-to-peer connections.

## Data Location
- **Config**: /mnt/<pool>/applications/tailscale/ (if running in Docker)
- **TrueNAS Native**: Managed by TrueNAS SCALE system.

## Backup Strategy
- Auth keys and node configuration stored in the Tailscale admin console.
- Local configuration backups.

## Network Exposure
- **LAN**: N/A (Mesh network).
- **WAN**: Outbound only; no inbound ports required.

## Authentication Method
Identity-based (SSO/Google/Microsoft/etc.).

## Dependencies
- Connectivity to Tailscale coordination server.

## Resource Usage Notes
Extremely lightweight.

## Security Considerations
Use strong MFA for the identity provider. Regularly review authorized devices in the admin console.

## Maintenance Tasks
- Updating the Tailscale client on all nodes.
- Renewing node keys.

## Upgrade Procedure
Update via TrueNAS SCALE app interface or update Docker image.
