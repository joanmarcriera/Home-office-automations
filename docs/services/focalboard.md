# Focalboard Service Documentation

## Service Overview
Focalboard is an open-source, self-hosted alternative to Trello, Notion, and Asana.

## Purpose / Business Value
Facilitates project management and task tracking for home lab projects and household organization.

## Why Self-Hosted
Ensures data privacy and keeps project boards accessible locally without cloud dependence.

## Data Location
`/mnt/<pool>/applications/focalboard/`

## Backup Strategy
- Database backups to `/mnt/<pool>/backups/focalboard/`.
- Dataset snapshots.

## Network Exposure
- **LAN**: Port 8000.
- **Tailscale**: Remote access for task management on the go.

## Authentication Method
Username/Password authentication.

## Dependencies
- PostgreSQL (recommended for production).

## Resource Usage Notes
Lightweight for single-user or small team usage.

## Security Considerations
Isolate the database. Use a reverse proxy for HTTPS.

## Maintenance Tasks
- Database maintenance.
- Periodic cleanup of archived boards.

## Upgrade Procedure
Pull the latest docker image and redeploy.
