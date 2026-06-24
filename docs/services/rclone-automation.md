# Rclone Automation

## What it is
Rclone is a command-line program to manage files on cloud storage. This service focuses on automated backups and syncs between local ZFS pools and remote cloud providers (S3, B2, Drive). It is a "Swiss Army knife" for cloud storage, supporting over 40 different providers.

## What problem it solves
It provides a robust, scriptable way to handle complex cloud storage operations, including automated off-site backups, synchronization between different cloud providers, and mounting remote storage as a local filesystem. It ensures data integrity through checksum verification and preserves critical metadata like timestamps.

## Where it fits in the stack
**Category**: Service / Infrastructure / Backup. Rclone is an essential utility for data portability and disaster recovery in a home-office or homelab environment. In 2026, it serves as the primary **Agentic Data Orchestrator** for remote storage.

## Typical use cases
- Automated off-site backups to cloud providers.
- Synchronizing data between different cloud storages.
- Mounting cloud storage as a local filesystem.
- Orchestrating multi-cloud data movement via MCP 3.0 tool calls.

## Strengths
- **Massive Connectivity**: Supports 70+ cloud storage providers as of 2026, including S3, B2, Drive, and decentralized options like [Storj](storj.md).
- **Data Integrity**: Built-in support for MD5/SHA1 checksums and timestamp preservation.
- **Bi-directional Sync**: The `bisync` command provides robust two-way synchronization between remotes.
- **Efficient Transfers**: Supports multi-threaded uploads and server-side moves to minimize bandwidth usage.
- **Agentic Integration**: Native MCP 3.0 server integration allows agents like Claude 4.8 Opus to manage files across providers.

## Limitations
- **Command-line focused**: While a GUI exists (`rclone rcd --rc-web-gui`), it remains a CLI-first tool.
- **Complexity**: The sheer number of flags and provider-specific configurations can be overwhelming for new users.

## When to use it
- For robust, automated cloud sync tasks.
- When you need a "Swiss Army knife" for cloud storage.
- To bridge local storage (like TrueNAS ZFS pools) with remote cloud targets.
- For agent-driven data migration and archival.

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
# Sync with progress and checksum verification
rclone sync /path/to/local remote:backup -P --checksum
```

### Bi-directional Sync (Two-way)
```bash
# Synchronize two remotes bi-directionally
rclone bisync remote1:path remote2:path --resync
```

### Mount a remote as a filesystem
```bash
# Mount remote for media apps (with caching)
rclone mount remote:path /path/to/mountpoint \
  --vfs-cache-mode full \
  --vfs-cache-max-age 24h \
  &
```

### Bandwidth Throttling
To limit bandwidth during business hours (e.g., 08:00 to 18:00), use the `--bwlimit` flag or a schedule in your script:

```bash
# Limit to 500k during the day, 10M at night
rclone sync /local/path remote:path --bwlimit "08:00,512k 18:00,10M"
```

### Healthcheck Notifications
Use a generic webhook pattern to notify a healthcheck service (like Healthchecks.io) upon successful completion:

```bash
#!/bin/bash
rclone sync /data storj:backup -v
if [ $? -eq 0 ]; then
  curl -m 10 --retry 5 https://hc-ping.com/<uuid>
else
  curl -m 10 --retry 5 https://hc-ping.com/<uuid>/fail
fi
```

## API examples

Rclone has an internal RC (Remote Control) API.

### List files via RC (curl)
```bash
curl -u user:pass localhost:5572/operations/list -d '{"fs": "remote:", "remote": "path"}'
```

### MCP 3.0 Tool Execution
Autonomous agents can invoke rclone via MCP to move data:

```bash
mcp-invoke rclone --cmd "sync" --args "/local/docs storj:backups"
```

## Backlog
- [x] Perform quarterly technical freshness audit (2026-06-19).
- [x] Implement bandwidth throttling during business hours.
- [x] Set up healthcheck notifications for failed syncs.
- [ ] Perform quarterly technical freshness audit.

## Related tools / concepts
- [Duplicati](https://www.duplicati.com/)
- [Kopia](https://kopia.io/)
- [BorgBackup](borg.md)
- [Storj](storj.md) — A primary decentralized target for Rclone backups.
- [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html)
- [AWS S3](https://aws.amazon.com/s3/)
- [TrueNAS SCALE](../architecture/infrastructure.md)
- [ZFS](https://openzfs.org/)
- [Nextcloud](nextcloud.md) — For synchronizing user data to the cloud.
- [Paperless-ngx](paperless-ngx.md) — For off-site archival of digitized documents.
- [Immich](immich.md) — For backing up large photo libraries.
- [Gitea](gitea.md) — For mirroring git repositories to object storage.
- [Docker](../tools/infrastructure/docker.md)
- [Model Context Protocol](../tools/automation_orchestration/mcp.md)

## Sources / References
- [Rclone Official Website](https://rclone.org/)
- [Rclone Documentation](https://rclone.org/docs/)
- [Rclone Bisync Guide](https://rclone.org/bisync/)
- [MCP Rclone Server](https://github.com/rclone/rclone-mcp)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
