# Rclone Automation

## What it is
Rclone is a command-line program to manage files on cloud storage. This service focuses on automated backups and syncs between ZFS pools and remote cloud providers (S3, B2, Drive). In late October / November 2026, it serves as the primary **Agentic Data Orchestrator**, leveraging the [MCP 3.1 / FastMCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md) for automated data migration and disaster recovery.

## What problem it solves
It provides a robust, scriptable way to handle complex cloud storage operations, including automated off-site backups, synchronization between different cloud providers, and mounting remote storage as a local filesystem. It ensures data integrity through checksum verification and preserves critical metadata like timestamps. It eliminates manual file management by allowing agents to move data between 70+ providers using standardized tool calls.

## Where it fits in the stack
**Category**: Service / Infrastructure / Backup. Rclone is an essential utility for data portability and disaster recovery in a home-office or homelab environment. It bridges the gap between local storage (like TrueNAS SCALE) and the multi-cloud ecosystem, acting as the storage transport layer for the entire agentic stack.

## Typical use cases
- **Automated Off-site Backups**: Syncing ZFS snapshots or local folders to encrypted S3/B2 buckets.
- **Cloud-to-Cloud Migration**: Moving data between providers (e.g., Google Drive to Storj) without local downloading.
- **VFS Mounts**: Mounting cloud storage as a local filesystem for media servers or document indexing.
- **Agent-Driven Archival**: Using [Claude 5.1](../tools/providers/anthropic.md) to identify and archive old project files to cold storage via FastMCP 3.1.

## Strengths
- **Massive Connectivity**: Supports 70+ cloud storage providers as of late 2026, including S3, B2, Drive, and [Storj](storj.md).
- **Data Integrity**: Built-in support for MD5/SHA1 checksums and robust timestamp preservation.
- **Agentic Integration**: Native [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md) server integration allows for zero-touch data orchestration.
- **Efficiency**: Supports multi-threaded transfers and server-side operations to minimize bandwidth and latency.
- **Versatile Syncing**: The `bisync` command provides reliable two-way synchronization between remotes.

## Limitations
- **CLI-First**: While a web GUI exists (`rclone rcd --rc-web-gui`), advanced configuration and automation require command-line expertise.
- **Configuration Complexity**: The vast number of flags and provider-specific nuances can be daunting for beginners.
- **API Rate Limits**: Success is often limited by the target provider's API quotas rather than Rclone's performance.

## When to use it
- For robust, automated cloud sync and backup tasks.
- When you need a "Swiss Army knife" to bridge local ZFS pools with remote cloud targets.
- For agent-driven data migration, archival, and multi-cloud orchestration.
- To mount remote storage for use in containerized applications.

## When not to use it
- For simple, one-time drag-and-drop file transfers (use a web UI).
- If you are uncomfortable with command-line tools and require a full-featured graphical backup suite.

## Getting started

### Installation
```bash
curl https://rclone.org/install.sh | sudo bash
```

### Configuration
```bash
rclone config
```

### Automated Backup Script
```bash
#!/bin/bash
# Sync local docs to Storj with progress and checksums
rclone sync /mnt/data/docs storj:backups -P --checksum --bwlimit "08:00,512k 18:00,10M"

# Notify healthcheck on success
if [ $? -eq 0 ]; then
  curl -m 10 --retry 5 https://hc-ping.com/<uuid>
fi
```

## CLI examples

### Sync with Throttling
```bash
# Limit to 500k during business hours, 10M at night
rclone sync /local/path remote:path --bwlimit "08:00,512k 18:00,10M"
```

### Bi-directional Sync
```bash
# Synchronize two remotes bi-directionally with resync
rclone bisync remote1:path remote2:path --resync
```

### VFS Mount
```bash
# Mount remote for media apps with full caching
rclone mount remote:path /mnt/cloud \
  --vfs-cache-mode full \
  --vfs-cache-max-age 24h \
  &
```

## API examples

### Remote Control (RC) API
```bash
# List files on a remote via curl
curl -u user:pass localhost:5572/operations/list -d '{"fs": "remote:", "remote": "path"}'
```

### Python (Trigger Sync via RC API with Pydantic v2 Validation)
The following script utilizes **Pydantic v2** to construct, validate, and dispatch sync requests to Rclone's RC API daemon, enabling autonomous agents (Claude 5.1, GPT-5.5, Gemini 4.0) to safely orchestrate backups.

```python
import requests
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class RcloneSyncPayload(BaseModel):
    srcFs: str = Field(..., description="Source filesystem / remote path")
    dstFs: str = Field(..., description="Destination filesystem / remote path")
    createEmptySrcDirs: bool = Field(default=True, description="Create empty source directories on destination")
    checkers: int = Field(default=8, description="Number of checkers to run in parallel")
    transfers: int = Field(default=4, description="Number of parallel file transfers")

class RcloneSyncResponse(BaseModel):
    status: Optional[str] = Field(None, description="Job status")
    jobId: Optional[int] = Field(None, description="Spawned job ID if run asynchronously")

def trigger_rclone_sync(rc_url: str, auth: tuple, payload: RcloneSyncPayload) -> RcloneSyncResponse:
    url = f"{rc_url}/sync/sync"

    # Send request with validated Pydantic model dump
    response = requests.post(url, json=payload.model_dump())
    response.raise_for_status()

    raw_response = response.json()
    return RcloneSyncResponse(**raw_response)

# Example usage:
# sync_payload = RcloneSyncPayload(srcFs="/mnt/data/docs", dstFs="storj:backups")
# try:
#     result = trigger_rclone_sync("http://localhost:5572", ("user", "pass"), sync_payload)
#     print(f"Sync initiated. Job ID: {result.jobId}")
# except Exception as e:
#     print(f"Backup failed to trigger: {e}")
```

### MCP 3.1 / FastMCP 3.1 Tool Invocation
Autonomous agents can invoke rclone tasks via the [MCP 3.1 / FastMCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md):

```bash
mcp-invoke rclone --cmd "sync" --args "/local/docs storj:backups"
```

### Healthcheck Integration
```bash
# Trigger a fail signal to a monitoring service
curl -m 10 --retry 5 https://hc-ping.com/<uuid>/fail
```

## Related tools / concepts
- [Storj](storj.md) — A primary decentralized target for Rclone backups.
- [BorgBackup](borg.md) — For deduplicated, encrypted local-to-local backups.
- [Nextcloud](nextcloud.md) — For synchronizing user-facing data.
- [Paperless-ngx](paperless-ngx.md) — For off-site archival of digitized documents.
- [Immich](immich.md) — For backing up photo and video libraries.
- [Gitea](gitea.md) — For mirroring git repositories to object storage.
- [Docker](../tools/infrastructure/docker.md) — For containerized Rclone deployments.
- [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md) — For agentic storage orchestration.
- [TrueNAS SCALE](../architecture/infrastructure.md) — The underlying storage OS for many Rclone tasks.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — For generating Rclone configuration scripts.
- [Claude 5.1](../tools/ai_knowledge/claude.md) — For advanced file diagnostics and reasoning.

## Sources / References
- [Rclone Official Website](https://rclone.org/)
- [Rclone Documentation](https://rclone.org/docs/)
- [Rclone Bisync Guide](https://rclone.org/bisync/)
- [MCP Rclone Server](https://github.com/rclone/rclone-mcp)

## Contribution Metadata
- Last reviewed: 2026-11-12
- Confidence: high
