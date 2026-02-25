# Nextcloud Service Documentation

## Service Overview
Nextcloud is a suite of client-server software for creating and using file hosting services.

## Purpose / Business Value
Provides a self-hosted alternative to cloud storage (Dropbox/Google Drive), ensuring data privacy and control. Integrates files, calendars, contacts, and communication.

## Why Self-Hosted
To maintain absolute ownership of personal data and avoid third-party cloud vulnerabilities and costs.

## Data Location
`/mnt/<pool>/applications/nextcloud/`

## Backup Strategy
- Daily database dumps.
- ZFS snapshots of the data dataset.
- Periodic offsite sync via rclone.

## Network Exposure
- **LAN**: Port 80/443.
- **Reverse Proxy**: Exposed via HTTPS for remote access.
- **Tailscale**: Preferred for admin access.

## Authentication Method
Built-in user management with support for 2FA and LDAP/OIDC.

## Dependencies
- PHP, MariaDB/PostgreSQL, Redis.

## Resource Usage Notes
Can be heavy on PHP/Database; requires sufficient RAM for caching.

## Security Considerations
Enable 2FA. Regularly check for security updates in the Nextcloud admin panel.

## Maintenance Tasks
- Monitoring data directory growth.
- Database optimization.

## Upgrade Procedure
Use the built-in web updater or update the Docker image. Always backup the database first.
