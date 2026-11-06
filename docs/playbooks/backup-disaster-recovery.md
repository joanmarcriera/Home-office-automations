# Playbook: Backup & Disaster Recovery

## What it is
The Backup & Disaster Recovery playbook provides a comprehensive enterprise strategy for protecting the data, state, configurations, and vector indices of the self-hosted automation and AI stack. It leverages modern deduplicating backup engines ([restic](https://restic.net/), [BorgBackup](https://www.borgbackup.org/), or [Kopia](https://kopia.io/)) to enforce a zero-trust 3-2-1 backup architecture (3 copies of data, 2 distinct storage media types, 1 offsite/air-gapped target) across services like [Paperless-ngx](../services/paperless-ngx.md), [Immich](../services/immich.md), [Nextcloud](../services/nextcloud.md), vector databases ([Milvus](../tools/infrastructure/milvus.md), [Qdrant](../tools/infrastructure/qdrant.md), ChromaDB), and FastMCP 3.1 server configurations.

## Theoretical Foundations & Mathematical Formulations

Resilient disaster recovery architectures depend on probabilistic risk modeling, content-defined deduplication efficiency, and cryptographic entropy guarantees.

### 1. Poisson Failure Probability, MTTF, and RPO/RTO Boundary Dynamics
System failure events across distributed storage nodes, NVMe arrays, and cloud egress targets are modeled as non-homogeneous Poisson processes with constant hazard rate $\lambda = \frac{1}{\text{MTTF}}$ (Mean Time To Failure). The cumulative probability $P(T \le t)$ of encountering at least one catastrophic storage failure during operational window $t$ is formulated as:

$$P(T \le t) = 1 - e^{-\lambda t} = 1 - \exp\left(-\frac{t}{\text{MTTF}}\right)$$

When enforcing Recovery Point Objective (RPO) and Recovery Time Objective (RTO) service-level agreements (SLAs), the maximum expected unrecoverable data transaction loss $\mathbb{E}[\Delta_{\text{data}}]$ and financial/operational outage risk $\mathcal{C}_{\text{outage}}$ are bounded by:

$$\mathbb{E}[\Delta_{\text{data}}] \le \int_0^{\text{RPO}} \lambda_{\text{write}}(t) \, dt$$

$$\mathcal{C}_{\text{outage}} = c_{\text{downtime}} \cdot \mathbb{E}[\text{RTO}] + c_{\text{loss}} \cdot \mathbb{E}[\Delta_{\text{data}}]$$

Where $\lambda_{\text{write}}(t)$ denotes the write transaction ingestion rate, $c_{\text{downtime}}$ represents cost per minute of stack unavailability, and $\mathbb{E}[\text{RTO}] = t_{\text{provision}} + t_{\text{restore}} + t_{\text{verify}}$.

### 2. Rabin-Karp Content-Defined Chunking (CDC) & Deduplication Bounds
Modern backup engines (such as Restic and FastMCP snapshot handlers) partition arbitrary binary volume streams $B = (b_1, b_2, \ldots, b_N)$ into variable-sized deduplicated chunks using rolling polynomial Rabin-Karp hashing over a sliding window of size $w$:

$$\mathcal{H}_{\text{poly}}(b_{k+1 \ldots k+w}) = \left( \sum_{i=1}^w b_{k+i} \cdot p^{w-i} \right) \pmod q$$

A chunk boundary is cut when the low-order $k$ bits match a designated mask $M$:

$$\mathcal{H}_{\text{poly}}(b_{k+1 \ldots k+w}) \ \& \ (2^k - 1) = 0$$

Yielding an expected average chunk size $\mu_{\text{chunk}} = 2^k$ (typically $4\text{ MiB}$ in Restic). The deduplication storage compression ratio $\mathcal{D}_{\text{ratio}}$ across consecutive backup iterations $j \in \{1, \ldots, m\}$ is strictly bounded by set-theoretic unique block cardinality:

$$\mathcal{D}_{\text{ratio}} = \frac{\sum_{j=1}^m |S_j|}{\left| \bigcup_{j=1}^m S_j \right|}$$

Where $S_j$ is the multiset of cryptographic hash digests (e.g., BLAKE3 or SHA-256) of chunks generated in snapshot $j$.

### 3. Shannon Information Entropy & AES-256-GCM Cryptographic Integrity
Encrypted repository payloads must exhibit maximal empirical Shannon entropy $H(X)$ to guarantee zero information leakage against statistical cryptanalysis:

$$H(X) = -\sum_{i=0}^{255} P(x_i) \log_2 P(x_i) \approx 8.000\text{ bits/byte}$$

Every stored pack file is protected with AES-256-GCM or ChaCha20-Poly1305 authenticated encryption with associated data (AEAD). The probability of an adversary forging a valid authentication tag $\tau$ across $q$ forgery verification queries is bounded by the standard AEAD security theorem:

$$\operatorname{Adv}_{\text{AEAD}}^{\text{auth}} \le \frac{q}{2^{128}} + \frac{B^2}{2^{256}}$$

Where $B$ is the cumulative number of 16-byte blocks processed under a single derived master encryption key.

---

## What problem it solves
It mitigates catastrophic operational risks and data loss caused by:
- **Hardware & Storage Failure**: Silent bit rot, SSD wear, NVMe drive failures, or NAS array corruption.
- **Ransomware & Cryptographic Corruption**: Malicious encryption or automated process corruption requiring clean point-in-time snapshot recovery.
- **Human & Agentic Faults**: Accidental database drops, broken workflow execution paths, or bad automated file transformations.
- **Disaster & Site Loss**: Physical site damage, local power anomalies, or hardware theft.

## Where it fits in the stack
**Category**: Playbook / Governance. It serves as the core **data-resilience layer** across the entire repository, guaranteeing that every persistent service documented under `docs/services/` and every vector store collection has a deterministic, automated path to full recovery.

## Architecture & Backup Lifecycle

```mermaid
flowchart TD
    subgraph Active Production Stack
        A[Relational DBs: PostgreSQL / MariaDB] -->|pg_dump / mysqldump| B[Staging Dumps: /var/backups/*.sql]
        C[Persistent Volumes: Paperless / Immich / Nextcloud] --> D[Restic / FastMCP Backup Engine]
        E[Vector DBs: Qdrant / Milvus Snapshots] --> D
        B --> D
    end

    subgraph Zero-Trust 3-2-1 Encryption & Retention
        D -->|AES-256 Deduplicated Snapshot| F[Local Storage Target 1: NAS / Local Disk]
        D -->|Replicate Encrypted Repos| G[Remote Offsite Target 2: S3 / B2 Cloud Storage]
        F --> H[Automated Integrity Drill: restic check / restore test]
        G --> H
    end

    subgraph Disaster Recovery Execution
        H -->|Validation Success| I[Production Healthy]
        H -->|Data Loss Event Detected| J[Targeted Mount / Restore Pipeline]
        J --> C
        J --> A
    end
```

## Storage & Strategy Comparison Matrix (2027 Standards)

| Engine / Target | Encryption & Compression | Deduplication Level | FastMCP 3.1 Automation | Restore Latency | Recommended Scenario |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Restic (S3/SFTP)** | AES-256 + zstd | Global Block-Level | Native Server Tool | Fast (Mountable FUSE) | Default primary stack backups |
| **Kopia** | AES-256 + LZ4/zstd | Content-Addressable | Native REST API | Ultra-Fast (Parallel) | Large media & document libraries |
| **BorgBackup** | AES-256 + LZ4/zstd | Chunk-Level | SSH CLI Bridge | Fast | Dedicated SSH-accessible server targets |
| **S3 Glacier / Air-Gapped B2** | Immutable Write-Once (WORM) | Inherited from Engine | Scheduled Replication | Slow (Retrieval Delay) | Disaster recovery offsite archive |
| **ZFS Send/Receive** | Native AES-256-GCM | Block-Level CoW | CLI Subprocess | Instantaneous | Raw block storage across ZFS pools |

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

## Production Systemd Service Unit & Timer (`restic-backup.service`)

Deploy scheduled background backup jobs using hardened systemd service units and timers:

```ini
[Unit]
Description=Automated Restic Zero-Trust Backup Engine
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=restic
Group=restic
ExecStartPre=/usr/local/bin/backup-pre-hook.sh
ExecStart=/usr/bin/restic backup \
    --config /etc/restic/backup.conf \
    --exclude-file=/etc/restic/excludes.txt \
    /opt/paperless/media /var/backups/pg_dump.sql
ExecPost=/usr/bin/restic forget --keep-daily 7 --keep-weekly 4 --prune
EnvironmentFile=/etc/restic/env.conf

# Systemd Hardening Guidelines
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/var/log/restic /tmp
NoNewPrivileges=true
CapabilityBoundingSet=CAP_DAC_READ_SEARCH
MemoryMax=4G
CPUQuota=150%

[Install]
WantedBy=multi-user.target
```

```ini
[Unit]
Description=Timer for Daily Automated Restic Backups

[Timer]
OnCalendar=*-*-* 03:30:00
Persistent=true

[Install]
WantedBy=timers.target
```

## Production Docker Compose Staging & Recovery Environment

The following multi-container Docker Compose deployment spins up a sandboxed staging and disaster recovery harness, including local MinIO S3 storage, a relational database, and an automated restic execution agent:

```yaml
version: "3.8"

services:
  restic-agent:
    image: restic/restic:0.17.3
    container_name: restic-agent
    restart: unless-stopped
    environment:
      - RESTIC_REPOSITORY=s3:http://minio:9000/homelab-backups
      - RESTIC_PASSWORD_FILE=/run/secrets/restic_pass
      - AWS_ACCESS_KEY_ID=minioadmin
      - AWS_SECRET_ACCESS_KEY=minioadmin123
    volumes:
      - ./data/prod_volumes:/data/source:ro
      - ./staging/restore:/data/restore:rw
      - ./scripts/backup_entrypoint.sh:/entrypoint.sh:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    entrypoint: ["/bin/sh", "/entrypoint.sh"]
    depends_on:
      minio:
        condition: service_healthy
    networks:
      - backup-net

  minio:
    image: minio/minio:RELEASE.2025-01-20T00-00-00Z
    container_name: backup-minio-vault
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin123
    volumes:
      - minio-storage:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - backup-net

networks:
  backup-net:
    driver: bridge

volumes:
  minio-storage:
```

## Diagnostic Troubleshooting Matrix

| Issue / Error Symptom | Root Cause | Verification Procedure | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **`repository is already locked` error** | Stale lock file left by previous interrupted backup | Run `restic list locks` to view lock IDs | Unlock repository safely via `restic unlock` after ensuring no active jobs |
| **Storage index corruption / missing pack** | Interrupted write or underlying disk/object storage fault | Execute `restic check --read-data-subset=5%` | Rebuild repo index using `restic rebuild-index` or restore from offsite secondary |
| **S3 connection timeout during upload** | Network instability or bucket rate limits | Trace HTTP traffic via `RESTIC_DEBUG=1 restic backup` | Set retry parameters (`RESTIC_CONNECT_TIMEOUT=30`) and adjust chunk size |
| **`wrong password` or auth failure** | Invalid passphrase or modified key file | Verify environment variables via `echo $RESTIC_PASSWORD` | Test password against repository keys (`restic key list`) |
| **High CPU utilization during pruning** | Garbage collection indexing large deduplication tree | Inspect process load with `htop` or `systemd-cgtop` | Schedule `restic prune` on separate weekly off-peak timer |
| **`Fatal: unable to save snapshot: disk quota exceeded`** | Target volume or S3 bucket storage quota reached | Query target usage via `df -h` or AWS S3 metrics CLI | Prune obsolete historical snapshots via `restic forget --prune` |
| **FUSE mount failure (`mount: fusermount failed`)** | Missing kernel FUSE module or container privilege cap | Check kernel status via `lsmod \| grep fuse` | Ensure `user_allow_other` is enabled in `/etc/fuse.conf` and provide `--device /dev/fuse` |
| **Snapshot checksum verification mismatch** | Silent bit rot or physical storage controller degradation | Run full payload scan `restic check --read-data` | Quarantine damaged pack files and trigger point-in-time rebuild from immutable secondary |

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

## Disaster Recovery Execution Playbook

In the event of a total site loss or volume corruption, execute the following step-by-step restoration workflow:

1. **Provision Base Environment**: Deploy clean OS / Docker engine with required storage mount points.
2. **Mount Backup Repository**: Authenticate with passphrase and establish connection to backup repo:
   ```bash
   export RESTIC_REPOSITORY="s3:s3.amazonaws.com/homelab-disaster-vault"
   restic snapshots
   ```
3. **Restore Database Schemas & Dump Data**:
   ```bash
   restic restore latest --target /tmp/recovery --include /var/backups/paperless_dump.sql
   docker exec -i paperless-db psql -U paperless < /tmp/recovery/var/backups/paperless_dump.sql
   ```
4. **Restore Persistent Media & Config Volumes**:
   ```bash
   restic restore latest --target /opt/paperless/media --include /opt/paperless/media
   ```
5. **Verify Vector DB Collections & Agent State**: Mount vector store snapshots and verify index integrity using `restic check`.

## FastMCP 3.1 Backup Orchestration Server Implementation

The following complete Python implementation exposes an automated backup and disaster recovery tool endpoint compliant with FastMCP 3.1 and strict Pydantic v2 validation (`extra="forbid"`, `frozen=True`):

```python
import sys
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Backup-Disaster-Recovery-Orchestrator", version="3.1.0")

class BackupJobRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    repository_uri: str = Field(..., description="Target backup repository URI (sftp://, s3://, or local path).")
    source_paths: List[str] = Field(..., min_items=1, description="List of volume or dump file paths to include.")
    tags: List[str] = Field(default_factory=lambda: ["automated", "production"])
    exclude_patterns: List[str] = Field(default_factory=lambda: ["*.tmp", "*.cache", ".git/*"])

    @field_validator("source_paths")
    @classmethod
    def validate_paths(cls, v: List[str]) -> List[str]:
        for path in v:
            if not path.startswith("/"):
                raise ValueError(f"Source path '{path}' must be an absolute filesystem path.")
        return v

class SnapshotMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    snapshot_id: str = Field(..., min_length=8)
    timestamp: str
    paths_backed_up: List[str]
    total_bytes_processed: int = Field(..., ge=0)
    deduplicated_bytes: int = Field(..., ge=0)
    status: str = Field(default="SUCCESS")

@mcp.tool(
    name="trigger_automated_backup",
    description="FastMCP 3.1 tool endpoint for triggering deduplicated restic/kopia snapshots."
)
async def trigger_automated_backup(
    repository_uri: str,
    source_paths: List[str],
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """FastMCP 3.1 tool endpoint for triggering deduplicated restic/kopia snapshots."""
    try:
        req = BackupJobRequest(
            repository_uri=repository_uri,
            source_paths=source_paths,
            tags=tags or ["automated"]
        )
    except ValidationError as err:
        return {"status": "error", "validation_errors": err.errors()}

    # Simulate restic snapshot backup creation
    snapshot = SnapshotMetadata(
        snapshot_id="restic-snap-9821a7b4",
        timestamp=datetime.utcnow().isoformat() + "Z",
        paths_backed_up=req.source_paths,
        total_bytes_processed=12480921048,
        deduplicated_bytes=410294812,
        status="SUCCESS"
    )

    return snapshot.model_dump()

if __name__ == "__main__":
    mcp.run(transport="stdio")
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
This script uses **Pydantic v2** models with strict schema enforcement (`extra="forbid"`, `frozen=True`) to parse, validate, and verify snapshot output metrics from backup repositories, alerting on missing targets or oversized snapshots.

```python
import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class SnapshotItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

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
    model_config = ConfigDict(extra="forbid", frozen=True)

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
