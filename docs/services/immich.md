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

### Machine Learning Node
Immich uses a dedicated service for AI tasks. By default, it runs on the CPU, but can be configured for NVIDIA GPUs or OpenVINO.

```yaml
# Partial docker-compose.yml for the ML node
services:
  immich-machine-learning:
    container_name: immich_machine_learning
    image: ghcr.io/immich-app/immich-machine-learning:release
    volumes:
      - model-cache:/cache
    restart: unless-stopped
```

### Local AI Models
Immich supports various models for:
- **CLIP**: Enables semantic search (searching by description).
- **Facial Recognition**: Automatically detects and groups faces.

## Backup and retention workflow

Treat Immich as the media application layer, not the only preservation layer:

1. Back up the upload/library storage and the PostgreSQL database together.
2. Keep a second copy outside the Immich host, such as NAS snapshots, object storage, or offline disk rotation.
3. Test restore by bringing up a temporary stack and confirming albums, people, and search indexes rebuild correctly.
4. For phone uploads, keep the mobile app's delete-after-upload behavior conservative until the independent backup has run.
5. Document retention rules for screenshots, duplicates, shared albums, and original camera files separately.

For home-office automation, the useful split is: Immich for browsing and AI search, file-level backup for disaster recovery, and [Paperless-ngx](paperless-ngx.md) or [Homebox](homebox.md) for receipts, warranties, and inventory evidence that should not live only in a photo timeline.

## Related tools / concepts
- [Photoprism](https://www.photoprism.app/) (Alternative)
- [Nextcloud Photos](nextcloud.md) (Alternative)

## Backlog
- Configure machine learning node for advanced image classification.
- Add a tested backup/restore runbook for the Immich database and upload library.

## Sources / References
- [Official Website](https://immich.app/)
- [GitHub Repository](https://github.com/immich-app/immich)
- [Immich Backup and Restore Documentation](https://immich.app/docs/administration/backup-and-restore/)
- [Photoprism Official Website](https://www.photoprism.app/)

## Contribution Metadata
- Last reviewed: 2026-05-07
- Confidence: high
