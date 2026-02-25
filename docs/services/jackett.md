# Jackett Service Documentation

## Service Overview
Jackett works as a proxy server that translates queries from apps (Sonarr, Radarr, etc.) into tracker-specific http queries.

## Purpose / Business Value
Consolidates multiple torrent tracker searches into a single API, simplifying the media automation pipeline.

## Why Self-Hosted
Facilitates the automation of local media library management without manual searching.

## Data Location
`/mnt/<pool>/applications/jackett/`

## Backup Strategy
- Config folder ZFS snapshots.

## Network Exposure
- **LAN**: Port 9117.
- **Reverse Proxy**: (Not recommended to expose publicly).

## Authentication Method
Admin password for the web interface.

## Dependencies
- Connectivity to external torrent trackers.

## Resource Usage Notes
Very lightweight.

## Security Considerations
Keep private; no need for external exposure.

## Maintenance Tasks
- Updating indexer configurations.
- Monitoring logs for failed searches.

## Upgrade Procedure
Auto-update or pull the latest docker image.
