# Immich

## What it is
Immich is a high-performance self-hosted photo and video management solution, designed as a direct replacement for Google Photos.

## What problem it solves
It provides a private, high-speed way to backup and organize media from mobile devices and desktops. It eliminates reliance on cloud storage subscriptions while providing advanced features like face recognition and semantic search.

## Where it fits in the stack
**Service / Media Management**. It acts as the primary vault for personal photos and videos.

## Typical use cases
- **Mobile Photo Backup**: Automatically backing up photos from iOS/Android devices.
- **Semantic Search**: Searching for photos using natural language (e.g., "dog in the park") powered by local CLIP models.
- **Face Recognition**: Automatically grouping photos by the people appearing in them.

## Strengths
- **Performance**: Extremely fast even with tens of thousands of images.
- **Feature Parity**: Offers many features found in Google Photos (sharing, albums, map view).
- **Local AI**: All machine learning (face recognition, object detection, CLIP) runs locally.
- **Active Development**: Rapidly evolving with frequent updates and new features.

## Limitations
- **Setup Complexity**: Requires multiple containers (database, redis, machine learning node).
- **Resource Intensive**: Machine learning tasks (especially initial library indexing) require significant CPU/GPU.
- **Not a Backup by Itself**: Mobile upload into Immich is only one copy. Keep an independent backup of the library and database.

## When to use it
- If you want a self-hosted alternative to Google Photos or iCloud Photos.
- When privacy and ownership of your personal media are priorities.
- If you have a large media library and need a fast, responsive interface.

## When not to use it
- If you prefer a simple file-based gallery without background processing.
- For extremely low-powered hardware that cannot handle the machine learning requirements.

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0 License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Hardware Acceleration (ML Node)
Immich uses a dedicated service for AI tasks (face recognition, CLIP, etc.). For high-performance library indexing, configure NVIDIA GPU or OpenVINO.

#### NVIDIA GPU (Docker)
```yaml
services:
  immich-machine-learning:
    container_name: immich_machine_learning
    image: ghcr.io/immich-app/immich-machine-learning:release
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - model-cache:/cache
    restart: unless-stopped
```

#### OpenVINO (Intel CPU/iGPU)
Set `IMMICH_MACHINE_LEARNING_URL` to point to a machine-learning container using the OpenVINO image:
`image: ghcr.io/immich-app/immich-machine-learning:release-openvino`

## Backup & Restore Runbook

### Backup Strategy
To ensure a consistent backup, you must back up both the **PostgreSQL database** and the **Upload Library**.

1.  **Database Dump**:
    ```bash
    # Run inside the database container
    docker exec -t immich_postgres pg_dumpall -c -U postgres > immich_backup.sql
    ```
2.  **Filesystem Backup**:
    Sync the `UPLOAD_LOCATION` to your backup target (e.g., using `rclone` or `rsync`).
    ```bash
    rsync -avz /path/to/immich/library/ /backup/immich/library/
    ```

### Restore Procedure
1.  Bring up a fresh Immich stack with the same version as your backup.
2.  Stop the `immich_server` container: `docker stop immich_server`.
3.  Restore the database:
    ```bash
    cat immich_backup.sql | docker exec -i immich_postgres psql -U postgres
    ```
4.  Restore the files to the `UPLOAD_LOCATION`.
5.  Restart the stack: `docker compose up -d`.

## Related tools / concepts
- [Photoprism](https://www.photoprism.app/) (Alternative)
- [Nextcloud Photos](nextcloud.md) (Alternative)
- [Paperless-ngx](paperless-ngx.md) (For document archival)
- [Homebox](homebox.md) (For physical asset inventory)
- [TrueNAS SCALE](../architecture/infrastructure.md) (Recommended storage backend)
- [NVIDIA](../tools/providers/nvidia.md) (For ML acceleration)
- [OpenVINO](https://www.intel.com/content/www/us/en/developer/tools/openvino-toolkit/overview.html) (Intel AI optimization)

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Sources / References
- [Official Website](https://immich.app/)
- [GitHub Repository](https://github.com/immich-app/immich)
- [Immich Backup and Restore Documentation](https://immich.app/docs/administration/backup-and-restore/)
- [Photoprism Official Website](https://www.photoprism.app/)

## Contribution Metadata
- Last reviewed: 2026-05-07
- Confidence: high
