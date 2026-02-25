# Storj Node Service Documentation

## Service Overview
A Storj storage node contributes disk space to the Storj decentralized cloud storage network.

## Purpose / Business Value
Monetizes excess storage space on TrueNAS pools to offset homelab costs.

## Why Self-Hosted
Utilizes existing hardware and storage capacity to generate passive income.

## Data Location
- **Identity**: `/mnt/<pool>/applications/storj/identity/`
- **Data**: `/mnt/<pool>/applications/storj/data/`

## Backup Strategy
- **Identity**: MUST be backed up (redundant copies).
- **Data**: Generally not backed up (network handles redundancy).

## Network Exposure
- **External**: Port 28967 (TCP/UDP) must be forwarded for network participation.

## Authentication Method
Identity certificate signed by the Storj network.

## Dependencies
- Reliable internet connection with low latency.
- Sufficient disk space.

## Resource Usage Notes
Lightweight CPU/RAM; steady disk I/O and network bandwidth.

## Security Considerations
Isolate the node in a DMZ or dedicated VLAN if possible.

## Maintenance Tasks
- Monitoring node reputation and earnings.
- Ensuring uptime (critical for reputation).

## Upgrade Procedure
Auto-update is built-in for most Storj docker configurations.
