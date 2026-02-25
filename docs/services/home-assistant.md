# Home Assistant Service Documentation

## Service Overview
Home Assistant is the central control system for smart home devices, focusing on local control and privacy.

## Purpose / Business Value
Provides a unified interface and automation engine for all household smart devices (lights, climate, security).

## Why Self-Hosted
Local control ensures smart home functionality even without internet access and protects user privacy.

## Data Location
`/mnt/<pool>/applications/home-assistant/`

## Backup Strategy
- Built-in "Google Drive Backup" add-on or local ZFS snapshots.
- Full system backups before major version upgrades.

## Network Exposure
- **LAN**: Port 8123.
- **Reverse Proxy**: Exposed via Nabu Casa or private reverse proxy for remote access.

## Authentication Method
Built-in user management with 2FA support.

## Dependencies
- Connectivity to smart devices (Zigbee, Z-Wave, Wi-Fi).

## Resource Usage Notes
Lightweight but benefits from SSD storage for the database (recorder).

## Security Considerations
Enable 2FA. Isolate smart home devices in a separate VLAN if possible.

## Maintenance Tasks
- Monitoring device battery levels.
- Updating integrations and add-ons.

## Upgrade Procedure
Update via the Supervisor or by pulling the latest Docker image.
