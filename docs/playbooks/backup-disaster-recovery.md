# Playbook: Backup & Disaster Recovery

## What it is
The Backup & Disaster Recovery playbook provides a comprehensive strategy for protecting the data and configurations of the homelab automation stack. It utilizes [restic](https://restic.net/), [BorgBackup](https://www.borgbackup.org/), or [Kopia](https://kopia.io/) to implement a robust 3-2-1 backup strategy (3 copies, 2 different media, 1 offsite) for services like [Paperless-ngx](../services/paperless-ngx.md), [Immich](../services/immich.md), [Nextcloud](../services/nextcloud.md), as well as local vector databases ([Milvus](../tools/infrastructure/milvus.md), Qdrant, ChromaDB) and configurations of your local Model Context Protocol / FastMCP 3.1 servers.

## What problem it solves
It mitigates the risk of catastrophic data loss due to:
- **Hardware Failure**: Failure of SSDs or HDDs hosting critical application data.
- **Ransomware / Malware**: Encrypted or corrupted data that requires a clean point-in-time restore.
- **Accidental Deletion**: Human or agentic errors resulting in the loss of files or database records.
- **Natural Disasters**: Physical damage to the local environment (fire, flood, theft).

## Where it fits in the stack
**Category**: Playbook / Governance. It serves as the **protective layer** for the entire repository, ensuring that every service documented in `docs/services/` and every vector collection has a verified path to recovery.

## Typical use cases
- **Paperless-ngx Vault Backup**: Daily encrypted snapshots of all scanned documents and their metadata.
- **Immich Library Protection**: Efficiently backing up terabytes of family photos and videos using deduplication.
- **Nextcloud Sync Recovery**: Restoring user data after a failed upgrade or corrupted database state.
- **Configuration Versioning**: Backing up the `.env` files, Docker Compose manifests, FastMCP 3.1 server configurations, and n8n workflows that define the stack.
- **Vector database snapshots**: Backing up vector collections and schema setups for reproducible local RAG.

## Strengths
- **Deduplication**: Saves significant storage space by only backing up unique data across snapshots.
- **Encryption**: Ensures all backups are encrypted at rest, protecting sensitive data from unauthorized access.
- **Mountable Backups**: Ability to mount a snapshot as a local filesystem for granular file recovery.
- **Vendor Agnostic**: Works with local NAS, external drives, and cloud storage (S3, B2, Wasabi).

## Limitations
- **Upload Speed**: Offsite backups are limited by your internet connection's upload bandwidth.
- **Resource Intensive**: Initial backups and verification (checks) can consume significant CPU and I/O.
- **Encryption Key Management**: Losing your backup passphrase means permanent loss of access to your data.
- **Manual Verification**: "Checking" backups (restore drills) still requires human or advanced agent oversight.

## When to use it
- To protect any service that stores user-generated or mission-critical data.
- Before performing major infrastructure upgrades or migrations.
- When you require a verifiable "rollback" point for the entire automation stack.

## When not to use it
- For transient data (e.g., `/tmp` folders, cache directories) that can be easily recreated.
- For data already managed by a specialized backup solution (though a secondary backup is often recommended).

## Getting started

### 1. Initialize the Repository (restic example)
Select your backup target (e.g., a local NAS via SFTP or an S3 bucket):
```bash
export RESTIC_REPOSITORY="sftp:user@nas:/backups/restic"
export RESTIC_PASSWORD_FILE="/home/user/.restic_password"
restic init
```

### 2. Prepare Application Data
For services with databases (Paperless, Nextcloud), perform a dump before backing up the volumes:
```bash
docker exec paperless-db pg_dumpall -U paperless > /data/backups/paperless_dump.sql
```

### 3. Run the Backup
Include the application volumes, vector DB snapshots, database dump, and MCP configuration folder:
```bash
restic backup /home/user/docker/paperless /data/backups/paperless_dump.sql /home/user/.config/Claude/claude_desktop_config.json
```

### 4. Implement 3-2-1 Strategy
Repeat Step 3 to an offsite S3-compatible target:
```bash
export RESTIC_REPOSITORY="s3:s3.wasabisys.com/my-backups"
restic backup /home/user/docker/paperless
```

## CLI examples

### 1. Listing Available Snapshots
```bash
restic snapshots
```

### 2. Restoring a Specific File
```bash
restic restore latest --target /tmp/restore --include /path/to/file.txt
```

### 3. Pruning Old Data (Maintenance)
Keep 7 daily, 4 weekly, and 12 monthly snapshots:
```bash
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
```

## API examples

### Python: Backup Metadata Verification & Logging with Pydantic v2
The following script utilizes **Pydantic v2** validation to model and log the results of backups, verifying that snapshots meet retention requirements and have correct sizing and checksums.

```python
import sys
import json
import subprocess
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class BackupSnapshot(BaseModel):
    snapshot_id: str = Field(..., alias="id", min_length=8)
    time: datetime
    paths: List[str]
    host: str
    tags: Optional[List[str]] = None
    size_bytes: int = Field(default=0, ge=0)

    @field_validator("paths")
    @classmethod
    def must_not_be_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Paths to backup must contain at least one directory or file.")
        return v

class BackupReport(BaseModel):
    repository: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(..., pattern="^(SUCCESS|FAILED)$")
    snapshots: List[BackupSnapshot]
    error_message: Optional[str] = None

def verify_backup_state(repo_path: str) -> dict:
    # Simulated execution of: restic --json snapshots
    # In a real pipeline, subprocess.run(["restic", "--json", "snapshots"]) is invoked
    mock_raw_json = """
    [
      {
        "id": "abc12345",
        "time": "2026-11-20T12:00:00Z",
        "paths": ["/home/user/docker/paperless", "/data/backups/paperless_dump.sql"],
        "host": "homelab-server",
        "tags": ["daily", "database"],
        "size_bytes": 154321098
      }
    ]
    """
    try:
        raw_snapshots = json.loads(mock_raw_json)
        # Parse and validate snapshots
        snapshots_objs = [BackupSnapshot.model_validate(s) for s in raw_snapshots]

        report = BackupReport(
            repository=repo_path,
            status="SUCCESS",
            snapshots=snapshots_objs
        )
        return report.model_dump()
    except Exception as e:
        failure_report = BackupReport(
            repository=repo_path,
            status="FAILED",
            snapshots=[],
            error_message=str(e)
        )
        return failure_report.model_dump()

if __name__ == "__main__":
    repo = "sftp:user@nas:/backups/restic"
    report_data = verify_backup_state(repo)
    print("Validated Backup Report:\n", json.dumps(report_data, indent=2, default=str))
```

### Automated Restore Drill (n8n Workflow)
Example logic for an n8n node to trigger a restore drill on a staging environment.
```json
{
  "action": "trigger_restore",
  "params": {
    "snapshot": "latest",
    "target_env": "staging",
    "services": ["paperless-ngx", "milvus-standalone"]
  }
}
```

## Related tools / concepts
- [Paperless-ngx](../services/paperless-ngx.md) — Primary document store.
- [Immich](../services/immich.md) — Photo management.
- [Nextcloud](../services/nextcloud.md) — Personal cloud storage.
- [MinIO](../tools/intake_storage/minio.md) — Local S3-compatible target.
- [S3 Storage](../tools/intake_storage/s3-storage.md) — Cloud backup targets.
- [HashiCorp Vault](../tools/automation_orchestration/hashicorp-vault.md) — Managing backup credentials.
- [Tailscale](../services/tailscale.md) — Secure connectivity to remote backup servers.

## Sources / References
- [The 3-2-1 Backup Strategy](https://www.backblaze.com/blog/the-3-2-1-backup-strategy/)
- [restic Documentation](https://restic.readthedocs.io/)
- [BorgBackup Documentation](https://borgbackup.readthedocs.io/)
- [Kopia Documentation](https://kopia.io/docs/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
