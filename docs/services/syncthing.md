# Syncthing Service Documentation

## Service Overview
Syncthing is a continuous file synchronization program. It synchronizes files between two or more computers in real time.

## Purpose / Business Value
Provides a decentralized, private alternative to cloud sync services. Essential for syncing note vaults (Obsidian/Logseq) and backups between devices without a central server.

## Why Self-Hosted
To ensure data privacy and avoid reliance on third-party cloud providers for file synchronization.

## Data Location
- **Config**: /mnt/<pool>/applications/syncthing/
- **Sync Folders**: Various paths on ZFS pools.

## Backup Strategy
- Config directory ZFS snapshots.
- (Data is naturally redundant across synced devices).

## Network Exposure
- **LAN**: Port 8384 (Web UI).
- **Tailscale**: Secure access to the Web UI and sync protocol across networks.

## Authentication Method
Username/Password for Web UI.

## Dependencies
- Connectivity between nodes (local or via discovery relay).

## Resource Usage Notes
Lightweight; CPU usage spikes during initial indexing or large transfers.

## Security Considerations
Use strong passwords for the Web UI. Sync connections are already encrypted via TLS.

## Maintenance Tasks
- Monitoring sync conflicts.
- Updating to the latest stable version.

## Upgrade Procedure
Update the docker image or use the built-in auto-updater for standalone installs.
