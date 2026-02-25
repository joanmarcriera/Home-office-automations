# Vikunja Service Documentation

## Service Overview
Vikunja is an open-source, self-hosted to-do list application for organizing tasks and projects.

## Purpose / Business Value
Provides a centralized, private task management system for personal and family use.

## Why Self-Hosted
To keep personal tasks and schedules private and accessible within the local network.

## Data Location
`/mnt/<pool>/applications/vikunja/`

## Backup Strategy
- Database backups (MariaDB/PostgreSQL).
- ZFS snapshots of application data.

## Network Exposure
- **LAN**: Port 3456.
- **Reverse Proxy**: Exposed for remote task management.

## Authentication Method
Built-in user accounts with support for OpenID Connect.

## Dependencies
- Database (MySQL/PostgreSQL).

## Resource Usage Notes
Lightweight.

## Security Considerations
Secure the API endpoint. Use TLS via reverse proxy.

## Maintenance Tasks
- Regular database backups.

## Upgrade Procedure
Update the docker-compose image tags for both frontend and backend.
