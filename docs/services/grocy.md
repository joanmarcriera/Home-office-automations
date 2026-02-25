# Grocy Service Documentation

## Service Overview
Grocy is a self-hosted web-based groceries & household management solution.

## Purpose / Business Value
Helps track household inventory (pantry, fridge), plan meals, and manage chores to reduce waste and improve efficiency.

## Why Self-Hosted
To keep personal consumption and lifestyle data private.

## Data Location
`/mnt/<pool>/applications/grocy/`

## Backup Strategy
- Database backups and attachment snapshots.

## Network Exposure
- **LAN**: Port 80.
- **Home Assistant**: Often accessed via Home Assistant Ingress.

## Authentication Method
Built-in user management.

## Dependencies
- PHP, SQLite (default).

## Resource Usage Notes
Lightweight.

## Security Considerations
Keep updated. Isolate within the LAN.

## Maintenance Tasks
- Regular data cleanup and barcode maintenance.

## Upgrade Procedure
Update the docker image.
