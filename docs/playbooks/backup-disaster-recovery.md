# Playbook: Backup & Disaster Recovery

## What it is
The Backup & Disaster Recovery playbook provides a comprehensive strategy for protecting the data and configurations of the homelab automation stack. It utilizes [restic](https://restic.net/), [BorgBackup](https://www.borgbackup.org/), or [Kopia](https://kopia.io/) to implement a robust 3-2-1 backup strategy (3 copies, 2 different media, 1 offsite) for services like [Paperless-ngx](../services/paperless-ngx.md), [Immich](../services/immich.md), and [Nextcloud](../services/nextcloud.md).

## What problem it solves
It mitigates the risk of catastrophic data loss due to:
- **Hardware Failure**: Failure of SSDs or HDDs hosting critical application data.
- **Ransomware / Malware**: Encrypted or corrupted data that requires a clean point-in-time restore.
- **Accidental Deletion**: Human or agentic errors resulting in the loss of files or database records.
- **Natural Disasters**: Physical damage to the local environment (fire, flood, theft).

## Where it fits in the stack
**Category**: Playbook / Governance. It serves as the **protective layer** for the entire repository, ensuring that every service documented in `docs/services/` has a verified path to recovery.

## Typical use cases
- **Paperless-ngx Vault Backup**: Daily encrypted snapshots of all scanned documents and their metadata.
- **Immich Library Protection**: Efficiently backing up terabytes of family photos and videos using deduplication.
- **Nextcloud Sync Recovery**: Restoring user data after a failed upgrade or corrupted database state.
- **Configuration Versioning**: Backing up the `.env` files, Docker Compose manifests, and n8n workflows that define the stack.

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
Include the application volumes and the database dump:
```bash
restic backup /home/user/docker/paperless /data/backups/paperless_dump.sql
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

### Python: Monitoring Backup Success via Healthchecks.io
Integrate backup scripts with a monitoring service to detect failures.
```python
import requests
import subprocess

def run_backup():
    try:
        # Run restic backup
        subprocess.run(["restic", "backup", "/data"], check=True)
        # Signal success to monitoring
        requests.get("https://hc-ping.com/your-uuid-here")
    except subprocess.CalledProcessError:
        # Signal failure
        requests.get("https://hc-ping.com/your-uuid-here/fail")

run_backup()
```

### Automated Restore Drill (n8n Workflow)
Example logic for an n8n node to trigger a restore drill on a staging environment.
```json
{
  "action": "trigger_restore",
  "params": {
    "snapshot": "latest",
    "target_env": "staging",
    "services": ["paperless-ngx"]
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
- Last reviewed: 2026-07-21
- Confidence: high
