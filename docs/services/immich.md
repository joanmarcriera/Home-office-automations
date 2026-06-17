# Immich

## What it is
Immich is a high-performance self-hosted photo and video management solution, designed as a direct replacement for Google Photos. It features a fast, responsive mobile app and a robust web interface for managing large personal media libraries.

## What problem it solves
It provides a private, high-speed way to backup and organize media from mobile devices and desktops. It eliminates reliance on cloud storage subscriptions while providing advanced features like face recognition and semantic search, all running on your own infrastructure to ensure data sovereignty.

## Where it fits in the stack
**Service / Media Management**. It acts as the primary vault for personal photos and videos, often deployed as a core service in home lab environments.

## Typical use cases
- **Mobile Photo Backup**: Automatically backing up photos from iOS/Android devices.
- **Semantic Search**: Searching for photos using natural language (e.g., "dog in the park") powered by local CLIP models.
- **Face Recognition**: Automatically grouping photos by the people appearing in them.
- **2026 Features**: 'Free Up Space' mobile cleanup, web-based database management, and HLS video streaming (Roadmap May 2026).
- **Agentic Organization**: Using Claude 4.8 Opus via MCP to semantically tag and categorize library assets.

## Strengths
- **Performance**: Extremely fast even with libraries exceeding 100,000 images.
- **Feature Parity**: Offers many features found in Google Photos (sharing, albums, map view, partner sharing).
- **Local AI**: All machine learning (face recognition, object detection, CLIP) runs locally without cloud dependencies.
- **Security (v2.7.0)**: Hardened by default with a Content Security Policy (CSP) and robust OIDC integration.

## Limitations
- **Setup Complexity**: Requires multiple containers (database, redis, machine learning node, microservices).
- **Resource Intensive**: Machine learning tasks (especially initial library indexing) require significant CPU/GPU resources.
- **Not a Backup by Itself**: Mobile upload into Immich is only one copy. An independent backup strategy for the library and database is mandatory.

## When to use it
- If you want a privacy-first, self-hosted alternative to Google Photos or iCloud Photos.
- When you have a large media library and need a fast, responsive interface.
- If you have the hardware resources (ideally with GPU acceleration) to run local AI models.

## When not to use it
- If you prefer a simple, low-resource file-based gallery without background processing.
- For extremely low-powered hardware (e.g., older Raspberry Pis) that cannot handle the machine learning overhead.

## Getting started

### Hardware Acceleration (ML Node)
Immich uses a dedicated service for AI tasks. For high-performance library indexing, configure NVIDIA GPU or OpenVINO.

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

### Backup & Restore Runbook
To ensure a consistent backup, you must back up both the **PostgreSQL database** and the **Upload Library**.

1.  **Database Dump**:
    ```bash
    docker exec -t immich_postgres pg_dumpall -c -U postgres > immich_backup.sql
    ```
2.  **Filesystem Backup**:
    ```bash
    rsync -avz /path/to/immich/library/ /backup/immich/library/
    ```

## CLI examples

### Immich CLI (Asset Upload)
The official Immich CLI allows for bulk uploading existing libraries from a terminal.

```bash
# Login to your instance
immich login http://immich.local/api YOUR_API_KEY

# Upload a directory recursively
immich upload --recursive /path/to/old/photos/
```

### Administrative Maintenance
Using `docker exec` for internal service health checks.

```bash
# Check machine learning node logs for CLIP processing errors
docker logs immich_machine_learning --tail 50

# Force a vacuum on the postgres database to reclaim space
docker exec -it immich_postgres vacuumdb -U postgres --all --full
```

## API examples

### Fetching Random Asset (Python)
Integrating Immich with agentic workflows (e.g., daily memory summaries via GPT-5.5).

```python
import requests
import random

API_URL = "http://immich.local/api"
API_KEY = "YOUR_API_KEY"
headers = {"x-api-key": API_KEY}

def get_random_photo():
    # Get all assets (limited for performance)
    response = requests.get(f"{API_URL}/assets", headers=headers, params={"take": 100})
    assets = response.json()
    if assets:
        random_asset = random.choice(assets)
        return f"Asset ID: {random_asset['id']}, Created: {random_asset['createdAt']}"
    return "No assets found"

print(get_random_photo())
```

### Triggering AI Re-indexing (Curl)
Programmatically triggering ML tasks after bulk imports.

```bash
curl -X POST "http://immich.local/api/jobs/machine-learning/trigger" \
     -H "x-api-key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"force": true}'
```

## Related tools / concepts
- [Nextcloud Photos](nextcloud.md) — Slower but integrated storage alternative.
- [Paperless-ngx](paperless-ngx.md) — For document archival alongside media.
- [Homebox](homebox.md) — For physical asset inventory management.
- [TrueNAS SCALE](../architecture/infrastructure.md) — Recommended storage backend.
- [NVIDIA](../tools/providers/nvidia.md) — For ML acceleration.
- [SearXNG](searXNG.md) — Private meta-search engine.
- [Syncthing](syncthing.md) — For P2P file synchronization.
- [Gitea](gitea.md) — For versioning related metadata.

## Sources / References
- [Official Website](https://immich.app/)
- [GitHub Repository](https://github.com/immich-app/immich)
- [Immich Backup and Restore Documentation](https://immich.app/docs/administration/backup-and-restore/)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
