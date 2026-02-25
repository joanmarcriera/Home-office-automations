# Diskover Service Documentation

## Service Overview
Diskover is an open-source file indexer and disk space analyzer.

## Purpose / Business Value
Helps manage large amounts of data on TrueNAS pools by providing a visual representation of disk usage and helping identify duplicates or large files.

## Why Self-Hosted
Provides local analysis of private datasets without sending file metadata to the cloud.

## Data Location
`/mnt/<pool>/applications/diskover/`

## Backup Strategy
- Config folder ZFS snapshots.
- (Database can be rebuilt by re-indexing).

## Network Exposure
- **LAN**: Port 80 (via web server).
- **Tailscale**: Private access for storage monitoring.

## Authentication Method
Basic auth via web server or built-in if available.

## Dependencies
- Elasticsearch (for storing file indices).
- Redis.

## Resource Usage Notes
Can be high during indexing (CPU/RAM). Elasticsearch requires significant RAM.

## Security Considerations
Do not expose publicly as it reveals file structure of the server.

## Maintenance Tasks
- Regular re-indexing of ZFS pools.
- Monitoring Elasticsearch health.

## Upgrade Procedure
Update container image and potentially the Elasticsearch version.
