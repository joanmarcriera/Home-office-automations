# Rclone Automation

Automated scripts and configurations for Rclone on TrueNAS SCALE.

## Description
Rclone is a command-line program to manage files on cloud storage. This service focuses on automated backups and syncs between local ZFS pools and remote cloud providers (S3, B2, Drive).

## Where it fits in the stack
**Category**: Service / Infrastructure / Backup

## Typical use cases
- Automated off-site backups to cloud providers.
- Synchronizing data between different cloud storages.
- Mounting cloud storage as a local filesystem.

## Strengths
- Supports 40+ cloud storage providers.
- Highly efficient and battle-tested CLI.
- Preserves timestamps and supports checksum verification.

## Limitations
- Command-line only (GUI is experimental).
- Requires careful configuration of API keys and secrets.

## When to use it
- For robust, automated cloud sync tasks.
- When you need a "Swiss Army knife" for cloud storage.

## When not to use it
- For simple drag-and-drop file transfers (use a web UI or dedicated sync client).
- If you are uncomfortable with the command line.

## Getting started

### Installation
```bash
curl https://rclone.org/install.sh | sudo bash
```

### Configuration
```bash
rclone config
```

## CLI examples

### Sync local folder to remote
```bash
rclone sync /path/to/local remote:backup -P
```

### Mount a remote as a filesystem
```bash
rclone mount remote:path /path/to/mountpoint &
```

## API examples

Rclone has an internal RC (Remote Control) API.

### List files via RC (curl)
```bash
curl -u user:pass localhost:5572/operations/list -d '{"fs": "remote:", "remote": "path"}'
```

## Related tools / concepts
- [Duplicati](https://www.duplicati.com/)
- [Kopia](https://kopia.io/)
- [BorgBackup](../services/borg.md)

## Backlog
- Implement bandwidth throttling during business hours.
- Set up healthcheck notifications for failed syncs.

## Sources / References
- [Rclone Official Website](https://rclone.org/)
- [Rclone Documentation](https://rclone.org/docs/)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
