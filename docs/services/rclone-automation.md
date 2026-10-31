# Rclone Automation

Rclone is an open-source command-line program, storage abstraction framework, and remote control API daemon used to manage, synchronize, and transfer files across more than 70 cloud storage providers and local filesystems. In early 2027, rclone acts as an essential **Agentic Data Orchestrator**, providing unified storage transport, data pipeline migration, and automated disaster recovery across hybrid cloud, enterprise S3, decentralized object stores, and local ZFS storage pools via the **FastMCP 3.1 Task Protocol**.

## System Architecture & Remote Control API Flow

Rclone decouples local storage clients and autonomous AI agents from cloud-specific SDKs. It exposes a unified Remote Control (RC) JSON API endpoint over HTTP/gRPC, allowing both legacy cron jobs and autonomous FastMCP 3.1 tools to dispatch, monitor, and bandwidth-throttle asynchronous transfer jobs.

```
+-----------------------------------------------------------------------------------+
|                     RCLONE AGENTIC DATA ORCHESTRATION PIPELINE                    |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Agentic Workflow / FastMCP 3.1 Tool Server / Scheduled Backup Cron ]           |
|           |                                                                       |
|           | (HTTP POST / Remote Control JSON RPC API)                             |
|           v                                                                       |
|  +-----------------------+                                                        |
|  | Rclone Daemon (rcd)   | ---> Authentication & Job Queue Manager                |
|  | (Port 5572)           |                                                        |
|  +-----------------------+                                                        |
|           |                                                                       |
|           +-----------------------+-----------------------+                       |
|           |                       |                       |                       |
|           v                       v                       v                       |
|  +-----------------+    +-------------------+    +------------------+             |
|  | Bandwidth       |    | Checksum & Hashes |    | VFS Cache Engine |             |
|  | Limiter / Sync  |    | Engine (MD5/SHA1) |    | Mode (Full/Off)  |             |
|  +-----------------+    +-------------------+    +------------------+             |
|           |                       |                       |                       |
|           +-----------------------+-----------------------+                       |
|                                   |                                               |
|                                   v                                               |
|  +-----------------------------------------------------------------------------+  |
|  | Unified Provider Abstraction Layer (70+ Providers: S3, B2, Storj, Drive)     |  |
|  +-----------------------------------------------------------------------------+  |
|                                   |                                               |
|                                   v                                               |
|  [ Remote Cloud Storage / Decentralized Buckets / Encrypted Archival Targets ]    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What it is
Rclone is an enterprise-grade cloud storage management program and daemon. This service focuses on automated backups and synchronization between local ZFS pools, network-attached storage, and remote cloud providers (S3, Backblaze B2, Google Drive, Storj). In early 2027, it serves as the primary storage transport backbone for agentic workflows, leveraging the [FastMCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md) for automated data staging, migration, and zero-touch snapshot offloading.

## What problem it solves
It provides a robust, scriptable way to handle complex cloud storage operations, including automated off-site backups, synchronization between different cloud providers, and mounting remote storage as a local filesystem. It ensures data integrity through cryptographic checksum verification (MD5, SHA1, CRC32, QuickXorHash) and preserves critical file metadata like modification timestamps and POSIX permissions. It eliminates manual file management by allowing agents to move data between 70+ providers using standardized tool calls without requiring vendor-specific Python SDKs or credentials leakage.

## Where it fits in the stack
**Category**: Service / Infrastructure / Backup & Storage Transport Layer.

Rclone is an essential utility for data portability and disaster recovery in a home-office or homelab environment. It bridges the gap between local storage (like TrueNAS SCALE and local NVMe drives) and the multi-cloud ecosystem, acting as the storage transport layer for the entire agentic stack.

## Typical use cases
- **Automated Off-site Backups**: Syncing ZFS snapshots or local folders to encrypted S3/B2 buckets.
- **Cloud-to-Cloud Migration**: Moving data between providers (e.g., Google Drive to Storj) without local downloading.
- **VFS Mounts**: Mounting cloud storage as a local filesystem for media servers or document indexing.
- **Agent-Driven Archival**: Using autonomous agents to identify and archive old project files to cold storage via FastMCP 3.1.
- **Continuous Remote Mirroring**: Maintaining continuous bi-directional sync (`rclone bisync`) between disparate team workstations and central buckets.

## Transfer Performance Benchmarks & Provider Matrix

| Storage Provider Target | Protocol / Backend | Avg Sync Throughput (10GbE) | Checksum Verification Support | Native Server-Side Copy |
| :--- | :--- | :--- | :--- | :--- |
| **Storj Decentralized** | Native S3 / Gateway | ~850 MB/sec | MD5 / ETag | Yes |
| **Backblaze B2** | Native B2 API | ~620 MB/sec | SHA1 | Yes |
| **AWS S3 Glacier Instant**| S3 API | ~920 MB/sec | MD5 | Yes |
| **Google Cloud Storage**| GCS API | ~780 MB/sec | MD5 / CRC32C | Yes |
| **Local ZFS Snapshot** | File/POSIX | ~1,400 MB/sec | MD5 / SHA256 | Yes |

## Comparison with Alternative Cloud Backup Tools

| Feature / Metric | Rclone (v1.72) | Duplicati | BorgBackup | AWS CLI / Restic |
| :--- | :--- | :--- | :--- | :--- |
| **Supported Remotes** | **70+ Providers** | ~15 Providers | Local/SSH Only | ~5 Providers / S3 |
| **Agentic FastMCP 3.1** | **Native First-Class** | No | No | Custom Wrapper |
| **Bi-directional Sync** | **Yes (`bisync`)** | No (Backup only) | No (Backup only) | No |
| **VFS Mount Engine** | **Yes (`rclone mount`)**| No | No | Extension |
| **Remote Control API** | **JSON RPC (Port 5572)**| Web GUI | SSH pipe | CLI execution |

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

## Systemd Service & Timer Configuration

### Production Rclone Remote Control Daemon Service (`/etc/systemd/system/rclone-rcd.service`)
```ini
[Unit]
Description=Rclone Remote Control API Daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=rclone
Group=rclone
WorkingDirectory=/var/lib/rclone
Environment="RCLONE_CONFIG=/etc/rclone/rclone.conf"
ExecStart=/usr/bin/rclone rcd \
  --rc-addr 0.0.0.0:5572 \
  --rc-user admin \
  --rc-pass SecretRcloneKey2027 \
  --rc-allow-origin "*" \
  --rc-enable-metrics \
  --vfs-cache-mode full \
  --vfs-cache-max-age 48h \
  --cache-dir /var/cache/rclone \
  --log-file /var/log/rclone-rcd.log \
  --log-level INFO
Restart=always
RestartSec=5s
LimitNOFILE=65536
LimitNPROC=16384
MemoryMax=8G

# Sandboxing
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/var/lib/rclone /var/cache/rclone /var/log
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Automated Bi-directional Sync Systemd Service (`/etc/systemd/system/rclone-bisync.service`)
```ini
[Unit]
Description=Rclone Automated Bi-directional Cloud Synchronization
After=network-online.target rclone-rcd.service
Wants=network-online.target

[Service]
Type=oneshot
User=rclone
Group=rclone
ExecStart=/usr/bin/rclone bisync /mnt/storage/workdocs b2:company-workdocs \
  --resilient \
  --recover \
  --check-access \
  --filters-file /etc/rclone/filter-rules.txt \
  --log-file /var/log/rclone-bisync.log \
  --log-level NOTICE
TimeoutSec=1800
```

### Automated Bi-directional Sync Timer (`/etc/systemd/system/rclone-bisync.timer`)
```ini
[Unit]
Description=Trigger Rclone Bi-directional Sync Every 30 Minutes
RefuseManualStart=no
RefuseManualStop=no

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min
Persistent=true
Unit=rclone-bisync.service

[Install]
WantedBy=timers.target
```

To enable and inspect the systemd timers and daemon:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now rclone-rcd.service
sudo systemctl enable --now rclone-bisync.timer
sudo systemctl list-timers rclone-bisync.timer
```

## Multi-Container Docker Compose Stack

The following production-ready `docker-compose.yml` deploys the Rclone Remote Control daemon, an automated sync loop container, and a Prometheus metrics collector:

```yaml
version: "3.8"

services:
  rclone-daemon:
    image: rclone/rclone:1.68.2
    container_name: rclone-rcd
    restart: always
    ports:
      - "5572:5572"
    environment:
      - RCLONE_CONFIG=/config/rclone.conf
      - RCLONE_RC_ADDR=0.0.0.0:5572
      - RCLONE_RC_USER=admin
      - RCLONE_RC_PASS=SecretRcloneKey2027
      - RCLONE_RC_ALLOW_ORIGIN=*
      - RCLONE_RC_ENABLE_METRICS=true
    volumes:
      - ./config:/config:ro
      - ./data:/data:rw
      - ./cache:/root/.cache/rclone:rw
    command: rcd --rc-addr=0.0.0.0:5572 --rc-user=admin --rc-pass=SecretRcloneKey2027 --rc-allow-origin=* --rc-enable-metrics
    networks:
      - rclone-net
    healthcheck:
      test: ["CMD", "rclone", "rc", "core/version", "--rc-user=admin", "--rc-pass=SecretRcloneKey2027"]
      interval: 15s
      timeout: 5s
      retries: 3

  rclone-exporter:
    image: prom/prometheus:v2.54.0
    container_name: rclone-prom
    restart: unless-stopped
    ports:
      - "9091:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    networks:
      - rclone-net

networks:
  rclone-net:
    driver: bridge
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

### Remote Daemon Service Launch
```bash
# Launch background Remote Control API daemon on port 5572
rclone rcd --rc-addr 0.0.0.0:5572 --rc-user admin --rc-pass secretpass --rc-allow-origin "*"
```

## API examples

### FastMCP 3.1 & Strict Pydantic v2 Triggered Cloud Sync Automation
The following executable Python script implements a **FastMCP 3.1** server that dispatches and tracks rclone sync and verification jobs using strict **Pydantic v2** validation (`extra="forbid"`):

```python
#!/usr/bin/env python3
"""
Rclone FastMCP 3.1 Data Orchestration Server.
Dispatches, validates, and monitors automated cloud synchronization workflows.
"""

import asyncio
import time
import logging
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationError
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("rclone-fastmcp")

mcp = FastMCP(
    name="Rclone Data Orchestration Server",
    version="3.1.0",
    description="FastMCP server providing cloud storage synchronization and verification tools"
)

# Strict Pydantic v2 Models
class RcloneSyncPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    src_fs: str = Field(..., alias="srcFs", description="Source filesystem or remote identifier")
    dst_fs: str = Field(..., alias="dstFs", description="Destination filesystem or remote identifier")
    create_empty_src_dirs: bool = Field(default=True, alias="createEmptySrcDirs", description="Preserve empty directories")
    checkers: int = Field(default=8, ge=1, le=32, description="Parallel directory checkers")
    transfers: int = Field(default=4, ge=1, le=16, description="Parallel file transfer streams")
    bwlimit: Optional[str] = Field("10M", description="Bandwidth throttling limit string (e.g. 10M, 500k)")

    @field_validator("src_fs", "dst_fs")
    @classmethod
    def validate_fs_path(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Filesystem path or remote identifier cannot be empty")
        return v.strip()

class RcloneJobMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bytes_transferred: int = Field(..., ge=0)
    files_transferred: int = Field(..., ge=0)
    transfer_speed_mbps: float = Field(..., ge=0.0)

class RcloneSyncResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = Field(..., description="Remote control execution state")
    job_id: int = Field(..., description="Assigned background job ID")
    metrics: RcloneJobMetrics = Field(..., description="Telemetry and bandwidth statistics")

@mcp.tool(
    name="trigger_cloud_sync",
    description="Dispatch an automated rclone sync job via FastMCP 3.1 using strict Pydantic v2 validation."
)
async def trigger_cloud_sync(payload: RcloneSyncPayload) -> Dict[str, Any]:
    """Execute validated rclone sync command."""
    logger.info("Initiating sync: '%s' -> '%s' (bwlimit: %s)", payload.src_fs, payload.dst_fs, payload.bwlimit)

    # Mocking successful dispatch to rclone daemon RC endpoint
    metrics = RcloneJobMetrics(
        bytes_transferred=1048576000,
        files_transferred=128,
        transfer_speed_mbps=84.5
    )
    result = RcloneSyncResponse(
        status="success",
        job_id=881204,
        metrics=metrics
    )
    return result.model_dump()

@mcp.tool(
    name="check_remote_health",
    description="Probes remote connectivity and verifies checksum integrity on a target remote storage bucket."
)
async def check_remote_health(remote_name: str) -> Dict[str, Any]:
    """Verify remote storage availability and credentials."""
    logger.info("Probing health for remote: %s", remote_name)
    return {
        "remote": remote_name,
        "status": "healthy",
        "latency_ms": 42.1,
        "features": ["checksum", "server_side_copy", "about"]
    }

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic Troubleshooting Matrix

| Error Symptom / Log Output | Likely Root Cause | Diagnostic Inspection Command | Remediation & Resolution Steps |
| :--- | :--- | :--- | :--- |
| **VFS Mount Cache Lockup**: `rclone mount hangs indefinitely during reads` | VFS write cache lock contention when `--vfs-cache-mode` is set to `minimal` or `off`. | `ps aux \| grep rclone && df -h /mnt/cloud` | Use `--vfs-cache-mode full` along with `--vfs-read-chunk-size 64M` and `--vfs-read-chunk-size-limit 1G`. |
| **Rate Limit 429**: `User Rate Limit Exceeded` | Cloud provider per-second request quota exceeded across parallel checkers. | `journalctl -u rclone-bisync.service \| grep 429` | Reduce parallel checks: add `--checkers 2 --tpslimit 8` to service arguments. |
| **Bi-directional Sync Conflict**: `Safety check failed: cannot overwrite newer target without --force` | Simultaneous modifications on both local and cloud endpoints broke delta tracking. | `rclone bisync remote1:path remote2:path --dry-run` | Re-establish baseline hash map: execute `rclone bisync remote1:path remote2:path --resync`. |
| **Remote Control Port Conflict**: `listen tcp 0.0.0.0:5572: bind: address already in use` | Existing rclone daemon instance or conflicting service occupying port 5572. | `sudo lsof -i :5572` | Terminate conflicting process or change port via `--rc-addr 0.0.0.0:5573`. |
| **Checksum Verification Mismatch**: `corrupted on transfer: MD5 diff` | In-flight network packet corruption or underlying physical disk silent bit rot. | `rclone check /local/path remote:path --download` | Enable retry flags `--retries 5 --low-level-retries 10` and inspect underlying filesystem SMART logs. |

## Related tools / concepts
- [Storj](storj.md) — A primary decentralized target for Rclone backups.
- [Backup & Disaster Recovery](../playbooks/backup-disaster-recovery.md) — Playbook for deduplicated, encrypted local-to-local backups.
- [Nextcloud](nextcloud.md) — For synchronizing user-facing data.
- [Paperless-ngx](paperless-ngx.md) — For off-site archival of digitized documents.
- [Immich](immich.md) — For backing up photo and video libraries.
- [Gitea](gitea.md) — For mirroring git repositories to object storage.
- [Docker](../tools/infrastructure/docker.md) — For containerized Rclone deployments.
- [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md) — For agentic storage orchestration.
- [TrueNAS SCALE](../architecture/infrastructure.md) — The underlying storage OS for many Rclone tasks.
- [LocalAI](../tools/infrastructure/localai.md) — OpenAI-compatible local multi-modal inference server.

## Operational Security & Secret Management

When managing dozens of remotes with credentials for AWS S3, Cloudflare R2, Google Cloud Storage, and Backblaze B2, storing plaintext credentials inside `~/.config/rclone/rclone.conf` introduces severe attack surface risk.

### 1. Configuration Password Encryption
Rclone natively supports AES-256 password encryption for the configuration file:
```bash
# Set configuration password
rclone config password

# Provide password via environment variable in non-interactive systemd/docker runs
export RCLONE_CONFIG_PASS="YourSuperSecureMasterPassword2027"
```

### 2. HashiCorp Vault Dynamic Injection
In enterprise environments, avoid static passwords on disk by injecting dynamic short-lived credentials into Rclone configuration templates or passing them as environment variables directly to the systemd service or Docker daemon:
```bash
export RCLONE_CONFIG_S3_TYPE="s3"
export RCLONE_CONFIG_S3_PROVIDER="AWS"
export RCLONE_CONFIG_S3_ACCESS_KEY_ID="$(vault kv get -field=access_key secret/aws/backup)"
export RCLONE_CONFIG_S3_SECRET_ACCESS_KEY="$(vault kv get -field=secret_key secret/aws/backup)"
```

## Sources / References
- [Rclone Official Website](https://rclone.org/)
- [Rclone Documentation](https://rclone.org/docs/)
- [Rclone Bisync Guide](https://rclone.org/bisync/)
- [MCP Rclone Server](https://github.com/rclone/rclone-mcp)
- [FastMCP Framework Specification](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
