# qBittorrent Service Documentation

## Service Overview
qBittorrent is an open-source BitTorrent client.

## Purpose / Business Value
Automates the downloading of Linux ISOs and other large datasets for the home lab.

## Why Self-Hosted
Provides full control over torrenting activity and allows for integration with automated media stacks.

## Data Location
- **Config**: `/mnt/<pool>/applications/qbittorrent/`
- **Downloads**: `/mnt/<pool>/downloads/`

## Backup Strategy
- Config directory ZFS snapshots.
- (Downloads are generally not backed up unless critical).

## Network Exposure
- **LAN**: Port 8080 (Web UI).
- **External**: BitTorrent ports forwarded (via VPN recommended).

## Authentication Method
Web UI login.

## Dependencies
- VPN container/connection (highly recommended for privacy).

## Resource Usage Notes
Moderate; depends on number of active torrents and disk I/O.

## Security Considerations
Always run behind a VPN with a kill switch. Secure the Web UI with a strong password.

## Maintenance Tasks
- Monitoring disk usage in the downloads dataset.
- Pruning completed torrents.

## Upgrade Procedure
Update container image.
