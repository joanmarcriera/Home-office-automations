# Habitica Service Documentation

## Service Overview
Habitica is an open-source habit-building and productivity app that treats your real life like a game.

## Purpose / Business Value
Gamifies personal and household tasks, increasing engagement and productivity for family members.

## Why Self-Hosted
Maintains control over personal habit data and ensures availability within the home lab environment.

## Data Location
`/mnt/<pool>/applications/habitica/`

## Backup Strategy
- Daily MongoDB backups stored in `/mnt/<pool>/backups/habitica/`.
- ZFS snapshots of the application dataset.

## Network Exposure
- **LAN**: Port 3000.
- **Tailscale**: Access via private mesh network.

## Authentication Method
Local account management.

## Dependencies
- MongoDB.

## Resource Usage Notes
Moderate; requires dedicated RAM for MongoDB and the Node.js application.

## Security Considerations
Ensure MongoDB is not accessible from the LAN. Use a reverse proxy for TLS if exposed.

## Maintenance Tasks
- MongoDB optimization.
- Regular updates to keep up with the upstream project.

## Upgrade Procedure
Update docker-compose image tags and restart services.
