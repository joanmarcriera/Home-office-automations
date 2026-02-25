# rclone Automation Jobs Service Documentation

## Service Overview
rclone is a command-line program to manage files on cloud storage. Automation jobs use rclone to sync or copy files between TrueNAS datasets and cloud providers.

## Purpose / Business Value
Ensures offsite backups and data synchronization between local and cloud environments.

## Why Self-Hosted
Provides a flexible, scriptable way to manage cloud data without using proprietary client software.

## Data Location
- **Config**: `/mnt/<pool>/applications/rclone/rclone.conf`
- **Logs**: `/mnt/<pool>/applications/rclone/logs/`

## Backup Strategy
- The `rclone.conf` file is critical and must be backed up securely (contains API tokens).

## Network Exposure
- **LAN**: N/A (usually runs as a CLI tool or cron job).
- **External**: Outbound connections to cloud providers.

## Authentication Method
Cloud-specific OAuth or API keys stored in `rclone.conf`.

## Dependencies
- Connectivity to cloud providers (e.g., Backblaze B2, Google Drive).

## Resource Usage Notes
Lightweight CPU/RAM; bandwidth usage can be high during sync tasks.

## Security Considerations
Encrypt the `rclone.conf` file using rclone's built-in encryption.

## Maintenance Tasks
- Monitoring job logs for errors.
- Renewing API tokens if necessary.

## Upgrade Procedure
Update the rclone binary or docker image.
