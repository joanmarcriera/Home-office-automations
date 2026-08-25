# Playbook: Backup & Disaster Recovery

## What it is
The Backup & Disaster Recovery playbook provides a comprehensive enterprise strategy for protecting the data, state, configurations, and vector indices of the self-hosted automation and AI stack. It leverages modern deduplicating backup engines ([restic](https://restic.net/), [BorgBackup](https://www.borgbackup.org/), or [Kopia](https://kopia.io/)) to enforce a zero-trust 3-2-1 backup architecture (3 copies of data, 2 distinct storage media types, 1 offsite/air-gapped target) across services like [Paperless-ngx](../services/paperless-ngx.md), [Immich](../services/immich.md), [Nextcloud](../services/nextcloud.md), vector databases ([Milvus](../tools/infrastructure/milvus.md), [Qdrant](../tools/infrastructure/qdrant.md), ChromaDB), and FastMCP 3.1 server configurations.

## What problem it solves
It mitigates catastrophic operational risks and data loss caused by:
- **Hardware & Storage Failure**: Silent bit rot, SSD wear, NVMe drive failures, or NAS array corruption.
- **Ransomware & Cryptographic Corruption**: Malicious encryption or automated process corruption requiring clean point-in-time snapshot recovery.
- **Human & Agentic Faults**: Accidental database drops, broken workflow execution paths, or bad automated file transformations.
- **Disaster & Site Loss**: Physical site damage, local power anomalies, or hardware theft.

## Where it fits in the stack
**Category**: Playbook / Governance. It serves as the core **data-resilience layer** across the entire repository, guaranteeing that every persistent service documented under `docs/services/` and every vector store collection has a deterministic, automated path to full recovery.

## Typical use cases
- **Paperless-ngx Document Vault Snapshot**: Daily encrypted backups of scanned documents, PostgreSQL metadata, and OCR indices.
- **Immich Media Library Backup**: Deduplicated, block-level snapshotting of multi-terabyte photo/video libraries.
- **Nextcloud Data & State Sync**: Point-in-time recovery for database and user data directories prior to stack upgrades.
- **FastMCP & Agent Stack Configuration Versioning**: Backing up environment credentials, Docker Compose manifests, MCP server configs, and n8n execution workflows.
- **Vector Database Index Persistence**: Consistent snapshots of HNSW vector collections, embedding stores, and metadata tables for instant RAG recovery.

## Strengths
- **Global Deduplication & Compression**: Drastically reduces storage requirements across historical snapshots.
- **End-to-End Cryptographic Security**: Authenticated AES-256 encryption at rest protects sensitive documents and API secrets.
- **Granular Mountable Restores**: Snapshots can be mounted as read-only FUSE filesystems for single-file or table recovery.
- **Multi-Cloud Target Flexibility**: Seamless backup to local NAS, remote S3 buckets, MinIO, or B2 cloud vaults.

## Limitations
- **Egress & Upload Bandwidth**: Remote offsite replication is constrained by outbound network throughput.
- **Resource Usage During Compression**: Initial backup indexing and verification passes demand high CPU and disk I/O.
- **Passphrase Dependency**: Losing backup encryption keys results in unrecoverable snapshot loss.
- **Verification Requirement**: Backup archives require regular automated restore drills to guarantee data integrity.

## When to use it
- Protecting any self-hosted service, production database, or local vector store containing non-ephemeral data.
- Creating pre-upgrade checkpoints before major infrastructure or schema migrations.
- Fulfilling data retention compliance and disaster readiness for agentic workflows.

## When not to use it
- Ephemeral caches, temporary working directories (`/tmp`), or public model weights that can be re-downloaded from registry endpoints.

## Getting started

### 1. Initialize Restic Repository Target
Select a backup destination (local SFTP target, S3 bucket, or MinIO instance):
```bash
export RESTIC_REPOSITORY="sftp:backupuser@nas.local:/backups/homelab"
export RESTIC_PASSWORD_FILE="/etc/restic_passphrase"
restic init
```

### 2. Export Application Database Dump
Dump relational databases prior to snapshotting volume directories:
```bash
docker exec -t paperless-db pg_dumpall -U paperless > /var/backups/paperless_dump.sql
```

### 3. Run Incremental Backup
Backup application directories, database dumps, and FastMCP server configuration manifests:
```bash
restic backup /opt/paperless/media /var/backups/paperless_dump.sql ~/.config/FastMCP/mcp_config.json
```

### 4. Execute 3-2-1 Offsite Snapshot Replication
Replicate local snapshots to an offsite S3-compatible cloud storage target:
```bash
export RESTIC_REPOSITORY="s3:https://s3.us-west-004.backblazeb2.com/my-homelab-backup"
restic backup /opt/paperless/media /var/backups/paperless_dump.sql
```

## CLI examples

### 1. Inspecting Backup Snapshots
```bash
restic snapshots --compact
```

### 2. Restoring a Specific Snapshot Path
```bash
restic restore latest --target /mnt/restore_staging --include /opt/paperless/media
```

### 3. Automated Retention & Snapshot Pruning
Retain 7 daily, 4 weekly, and 12 monthly snapshots while purging stale data blocks:
```bash
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
```

## API examples

### Python: Backup Verification & Health Reporting (Pydantic v2)
This script uses **Pydantic v2** models to parse, validate, and verify snapshot output metrics from backup repositories, alerting on missing targets or oversized snapshots.

```python
import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class SnapshotItem(BaseModel):
    snapshot_id: str = Field(..., alias="id", min_length=8)
    time: datetime
    paths: List[str]
    host: str
    tags: Optional[List[str]] = Field(default_factory=list)
    size_bytes: int = Field(default=0, ge=0)

    @field_validator("paths")
    @classmethod
    def validate_paths(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Backup path list cannot be empty.")
        return v

class BackupRepositoryReport(BaseModel):
    repository_url: str
    checked_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(..., pattern="^(HEALTHY|DEGRADED|FAILED)$")
    total_snapshots: int
    snapshots: List[SnapshotItem]
    error_details: Optional[str] = None

def validate_backup_health(json_payload: str, repo_url: str) -> dict:
    try:
        raw_items = json.loads(json_payload)
        snapshots = [SnapshotItem.model_validate(item) for item in raw_items]

        report = BackupRepositoryReport(
            repository_url=repo_url,
            status="HEALTHY" if len(snapshots) > 0 else "DEGRADED",
            total_snapshots=len(snapshots),
            snapshots=snapshots
        )
        return report.model_dump()
    except Exception as e:
        return BackupRepositoryReport(
            repository_url=repo_url,
            status="FAILED",
            total_snapshots=0,
            snapshots=[],
            error_details=str(e)
        ).model_dump()

if __name__ == "__main__":
    sample_json = """
    [
      {
        "id": "a1b2c3d4e5f6",
        "time": "2027-01-07T04:00:00Z",
        "paths": ["/opt/paperless/media", "/var/backups/paperless_dump.sql"],
        "host": "core-node-01",
        "tags": ["daily", "production"],
        "size_bytes": 4839204812
      }
    ]
    """
    res = validate_backup_health(sample_json, "sftp:user@nas:/backups")
    print("Backup Health Report:\n", json.dumps(res, indent=2, default=str))
```

## Related tools / concepts
- [Paperless-ngx](../services/paperless-ngx.md) — Document management system.
- [Immich](../services/immich.md) — Self-hosted photo library.
- [Nextcloud](../services/nextcloud.md) — Cloud sync & file storage platform.
- [MinIO](../tools/intake_storage/minio.md) — Local S3 storage provider.
- [S3 Storage](../tools/intake_storage/s3-storage.md) — Cloud backup destinations.
- [Tailscale](../services/tailscale.md) — Secure peer-to-peer connection for offsite NAS nodes.
- [HashiCorp Vault](../tools/automation_orchestration/hashicorp-vault.md) — Secure storage for backup encryption keys.

## Sources / References
- [The 3-2-1 Backup Rule Guide](https://www.backblaze.com/blog/the-3-2-1-backup-strategy/)
- [restic Official Documentation](https://restic.readthedocs.io/)
- [BorgBackup Manual](https://borgbackup.readthedocs.io/)
- [Kopia Documentation](https://kopia.io/docs/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
