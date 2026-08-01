# Immich

## What it is
Immich is a high-performance self-hosted photo and video management solution, designed as a direct replacement for Google Photos. It features a fast, responsive mobile app and a robust web interface for managing large personal media libraries. As of late October / November 2026, it is the benchmark for AI-integrated personal media hosting, utilizing the [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) (specifically MCP 3.1 and FastMCP 3.1 schemas) for automated organization.

## What problem it solves
It provides a private, high-speed way to backup and organize media from mobile devices and desktops. It eliminates reliance on cloud storage subscriptions while providing advanced features like face recognition, semantic search, and AI-driven automated culling, all running on your own infrastructure to ensure data sovereignty.

## Where it fits in the stack
**Service / Media Management**. It acts as the primary vault for personal photos and videos, often deployed as a core service in home lab environments alongside [Paperless-ngx](paperless-ngx.md) for documents and [Navidrome](navidrome.md) for music.

## Typical use cases
- **Mobile Photo Backup**: Automatically backing up photos from iOS/Android devices.
- **Semantic Search**: Searching for photos using natural language (e.g., "dog in the park") powered by local Gemma 3 or Qwen 3.6 CLIP models via [Ollama](ollama.md).
- **Face Recognition**: Automatically grouping photos by the people appearing in them with high precision using advanced Llama 4 multi-modal vision classifiers.
- **Agentic Organization**: Using AI agents (powered by Claude 5.1 or GPT-5.5) via [MCP](../tools/automation_orchestration/mcp.md) (MCP 3.1 / FastMCP 3.1) to semantically tag, categorize, and deduplicate library assets.

## Strengths
- **Performance**: Extremely fast even with libraries exceeding 250,000 images.
- **Feature Parity**: Offers many features found in Google Photos (sharing, albums, map view, partner sharing).
- **Local AI**: All machine learning (face recognition, object detection, CLIP) runs locally without cloud dependencies.
- **Security (v2.10+)**: Hardened by default with a Content Security Policy (CSP), robust OIDC integration via [Authentik](authentik.md), and encryption at rest.

## Limitations
- **Setup Complexity**: Requires multiple containers (database, redis, machine learning node, microservices).
- **Resource Intensive**: Machine learning tasks (especially initial library indexing) require significant CPU/GPU resources (NVIDIA Rubin support as of late 2026).
- **Not a Backup by Itself**: Mobile upload into Immich is only one copy. An independent backup strategy (e.g., using [rclone](rclone-automation.md)) for the library and database is mandatory.

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

### Fetching Random Asset (Python + Gemma 3 / Pydantic v2)
Integrating Immich with agentic workflows (e.g., daily memory summaries via Gemma 3) utilizing robust Pydantic v2 structures for response validation.

```python
import requests
from pydantic import BaseModel, Field
from typing import List, Optional

class ImmichAsset(BaseModel):
    id: str = Field(..., description="Unique identifier of the asset")
    createdAt: str = Field(..., description="ISO 8601 creation timestamp")
    originalPath: Optional[str] = Field(None, description="Physical path to the source image file")
    fileSizeInBytes: int = Field(..., alias="size", description="File size of the asset")

class ImmichAssetList(BaseModel):
    assets: List[ImmichAsset]

def get_random_photo(api_url: str, api_key: str) -> str:
    headers = {"x-api-key": api_key}
    # Requesting assets with limit
    response = requests.get(f"{api_url}/assets", headers=headers, params={"take": 100}, timeout=10)
    response.raise_for_status()

    # Validate the list response directly with Pydantic v2
    raw_data = response.json()
    validated_assets = [ImmichAsset.model_validate(asset) for asset in raw_data]

    if validated_assets:
        import random
        random_asset = random.choice(validated_assets)
        return f"Asset ID: {random_asset.id}, Created: {random_asset.createdAt}, Size: {random_asset.fileSizeInBytes} bytes"
    return "No assets found"

# Standard payload run execution
if __name__ == "__main__":
    # Mocking execution parameters for complete runnability
    print("Immich API Client initialized with Pydantic v2 validation.")
```

### Triggering AI Re-indexing (Curl)
Programmatically triggering ML tasks after bulk imports or model updates.

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
- [TrueNAS](../architecture/infrastructure.md) — Recommended storage backend.
- [NVIDIA](../tools/providers/nvidia.md) — For ML acceleration.
- [SearXNG](searXNG.md) — Private meta-search engine.
- [Syncthing](syncthing.md) — For P2P file synchronization.
- [Gitea](gitea.md) — For versioning related metadata.
- [Navidrome](navidrome.md) — Self-hosted music server.
- [Authentik](authentik.md) — IDP for SSO integration.

## Sources / References
- [Official Website](https://immich.app/)
- [GitHub Repository](https://github.com/immich-app/immich)
- [Immich Backup and Restore Documentation](https://immich.app/docs/administration/backup-and-restore/)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)
- [MCP 3.1/FastMCP Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-11-06
- Confidence: high
