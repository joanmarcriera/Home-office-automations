# Linkwarden Service Documentation

## Service Overview
Linkwarden is a self-hosted, open-source collaborative bookmark manager to archive web pages.

## Purpose / Business Value
Provides a centralized repository for web resources, ensuring that bookmarks are archived and accessible even if the original source goes offline. Facilitates research and knowledge sharing within the home lab environment.

## Why Self-Hosted
Ensures privacy of bookmarked content and full control over archived data without reliance on third-party cloud services.

## Data Location
`/mnt/<pool>/applications/linkwarden/`

## Backup Strategy
- Weekly ZFS snapshots of the application dataset.
- Database exports stored in `/mnt/<pool>/backups/linkwarden/`.
- Offsite replication via rclone.

## Network Exposure
- **LAN**: Accessible on port 3000.
- **Reverse Proxy**: Exposed via Traefik/Nginx with TLS for secure remote access.
- **Tailscale**: Recommended for remote access without WAN exposure.

## Authentication Method
Built-in user authentication with support for multiple users and roles.

## Dependencies
- PostgreSQL database.
- Redis (optional, for caching).

## Resource Usage Notes
Lightweight; typically requires < 500MB RAM.

## Security Considerations
Keep the instance updated. Ensure database is not exposed to the network. Use strong passwords.

## Maintenance Tasks
- Regular database vacuuming.
- Monitoring disk usage for archived pages.

## Upgrade Procedure
Pull the latest docker image and restart the container. Review release notes for database migrations.
