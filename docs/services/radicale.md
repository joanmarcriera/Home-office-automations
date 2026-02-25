# Radicale Service Documentation

## Service Overview
Radicale is a lightweight CalDAV (calendar) and CardDAV (contact) server.

## Purpose / Business Value
Provides a private, self-hosted alternative to Google Contacts and Calendar, allowing for simple sync across personal devices.

## Why Self-Hosted
To maintain data sovereignty over sensitive schedule and contact information.

## Data Location
`/mnt/<pool>/applications/radicale/`

## Backup Strategy
- Simple file-level backups of the storage directory.
- ZFS snapshots of the application dataset.

## Network Exposure
- **LAN**: Port 5232.
- **Reverse Proxy**: Exposed for remote sync on mobile devices.

## Authentication Method
Built-in basic authentication or external auth backends.

## Dependencies
- Python environment (if not running via Docker).

## Resource Usage Notes
Extremely lightweight.

## Security Considerations
Always use TLS (via reverse proxy) when accessing over WAN.

## Maintenance Tasks
- Monitoring log files for sync errors.

## Upgrade Procedure
Update the docker image or use `pip install --upgrade radicale`.
