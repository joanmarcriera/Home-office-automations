# Homebox Service Documentation

## Service Overview
Homebox is the inventory and organization system built for the home user.

## Purpose / Business Value
Organizes physical assets in the home lab and household, including warranties and location tracking.

## Why Self-Hosted
To keep a private record of personal belongings.

## Data Location
`/mnt/<pool>/applications/homebox/`

## Backup Strategy
- SQLite database backups.
- Dataset snapshots.

## Network Exposure
- **LAN**: Port 7745.
- **Tailscale**: Remote access for inventory management.

## Authentication Method
Built-in user management.

## Dependencies
- Go-based standalone binary or Docker.

## Resource Usage Notes
Extremely lightweight.

## Security Considerations
Ensure secure login credentials.

## Maintenance Tasks
- Regular backups of the SQLite database.

## Upgrade Procedure
Pull the latest docker image and restart.
