# Jellyfin Service Documentation

## Service Overview
Jellyfin is a Free Software Media System that lets you control managing and streaming your media.

## Purpose / Business Value
Provides a centralized media server for movies, TV shows, and music, accessible across various devices in the home.

## Why Self-Hosted
Eliminates subscription fees and ensures media privacy. No tracking or telemetry compared to proprietary alternatives.

## Data Location
- **Config/Metadata**: `/mnt/<pool>/applications/jellyfin/`
- **Media Library**: `/mnt/<pool>/media/`

## Backup Strategy
- Config directory backed up via ZFS snapshots.
- Media library backed up to external storage/cloud.

## Network Exposure
- **LAN**: Port 8096.
- **Reverse Proxy**: Exposed via subdomain (e.g., jellyfin.home.arpa) for remote streaming.

## Authentication Method
Built-in user management with LDAP/SSO options.

## Dependencies
- Hardware acceleration (QuickSync/NVENC) for transcoding.

## Resource Usage Notes
High during transcoding; requires significant CPU/GPU resources and RAM.

## Security Considerations
Use TLS for remote access. Regularly update to patch vulnerabilities.

## Maintenance Tasks
- Library scanning and metadata cleanup.
- Monitoring cache and log sizes.

## Upgrade Procedure
Update container image to the latest stable release.
