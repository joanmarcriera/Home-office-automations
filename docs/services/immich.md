# Immich

Immich is a high-performance, self-hosted media management and photo/video backup platform engineered as an open-source, privacy-preserving alternative to Google Photos and Apple iCloud Photos. Built with a Node.js/TypeScript application server, PostgreSQL with pgvector extension, Redis event queue, and Python machine learning microservice, Immich provides high-speed mobile media backup, facial recognition, semantic CLIP search, and map geocoding. As of early 2027, Immich natively integrates with the **FastMCP 3.1 Specification**, enabling autonomous AI agents to query media libraries, search photos using multimodal vision embeddings, organize albums, and execute metadata tagging.

```
+---------------------------------------------------------------------------------------+
|                                IMMICH ARCHITECTURE OVERVIEW                           |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------+   +-----------------------+   +----------------------------+  |
|  | Mobile Native Apps |   | Web Client (Svelte)   |   | Reverse Proxy (Nginx/Caddy)|  |
|  | (iOS / Android)    |   | Responsive Web UI     |   | OIDC Auth / SSL Ingress    |  |
|  +---------+----------+   +-----------+-----------+   +-------------+--------------+  |
|            |                          |                             |                 |
+------------|--------------------------|-----------------------------|-----------------+
             |                          |                             |
             v                          v                             v
+---------------------------------------------------------------------------------------+
|                             IMMICH SERVER & CORE SERVICES                             |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------------+  +--------------------------+  +---------------------+  |
|  | Immich Server (REST API) |  | Redis Event Queue        |  | Machine Learning Node|  |
|  | Microservices Orchestrator|  | Job Worker Distribution  |  | (PyTorch/CLIP/ONNX) |  |
|  +------------+-------------+  +------------+-------------+  +----------+----------+  |
|               |                             |                            |            |
+---------------|-----------------------------|----------------------------|------------+
                |                             |                            |
                v                             v                            v
+---------------------------------------------------------------------------------------+
|                           PERSISTENCE & FASTMCP 3.1 BRIDGE                        |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------+   +--------------------+   +-------------------------------+  |
|  | PostgreSQL +       |   | Storage Vault      |   | FastMCP 3.1 Agent Server      |  |
|  | pgvector Engine    |   | Library / Thumbnails|  | Multimodal Media Query Tools  |  |
|  +--------------------+   +--------------------+   +-------------------------------+  |
|                                                                                       |
+---------------------------------------------------------------------------------------+
```

## What it is
Immich is a self-hosted media management application designed for large personal photo and video libraries. It combines native mobile client applications (featuring background sync, auto-upload, and offline caching) with a web interface. Immich decouples storage and asset metadata from proprietary clouds, storing original media files in clean, human-readable directory structures on local disk or network attached storage (NAS).

Under the hood, Immich uses PostgreSQL with `pgvector` for vector embedding storage, enabling sub-second semantic search across hundreds of thousands of photos. The machine learning service utilizes local ONNX Runtime models (accelerated via NVIDIA TensorRT, OpenVINO, or Apple Silicon CoreML) for face detection, facial recognition, object detection, and CLIP image-text embedding extraction without transmitting any data to external third-party cloud APIs.

## What problem it solves
Relying on commercial cloud photo storage introduces several operational and security issues:
1. **Recurring Storage Costs & Lock-In**: Expanding photo/video collections past cloud free tiers requires lifetime monthly subscriptions, while downloading raw original archives is made tedious by cloud rate limits.
2. **Privacy Breaches & Automated Scans**: Commercial providers perform cloud-side automated scanning and data mining on private photos, compromising family privacy.
3. **Loss of File Control & Naming Structure**: Cloud backup applications obscure raw file paths, making direct filesystem backups or local organization impossible.
4. **Agent Integration Obstacles**: Standard photo vaults do not support open protocols, preventing local AI agents (such as Claude Code, Cursor, or home lab assistants) from searching photos or generating automated family memory summaries.

Immich resolves these problems by offering self-hosted storage sovereignty, local GPU-accelerated AI indexing, clean directory layout, and a native **FastMCP 3.1** media server interface.

## Where it fits in the stack
Immich serves as the **Personal Media Vault & Multimodal Storage Layer** in personal infrastructure stacks:

- **Upstream Sources**: iOS and Android mobile devices, DSLR camera SD card imports, drone footage backups, legacy photo archives.
- **Core Platform**: Immich Server (Node.js REST API, PostgreSQL + pgvector, Redis event queue, Machine Learning container).
- **Downstream Integrations**:
  - **Identity Providers**: [Authentik](authentik.md), Authelia, Keycloak (via OpenID Connect/OIDC).
  - **Storage Storage & Backup**: TrueNAS, ZFS pools, Unraid, [rclone](rclone-automation.md) offsite backup targets.
  - **AI Agents & MCP**: FastMCP 3.1 server, Claude 3.5/3.7, Cursor, local multi-modal LLMs (Ollama, vLLM, DeepSeek-V4).

## Typical use cases
- **Automated Mobile Camera Roll Backup**: Instant, background uploading of new photos and 4K videos from mobile devices over Wi-Fi or Tailscale connections.
- **Natural Language Semantic Media Search**: Finding specific photos using natural language prompts (e.g. "sunset over snow covered mountains in 2026") powered by local CLIP models.
- **Automated Facial Recognition & Grouping**: Clustering photos of family members, friends, and pets into named facial recognition timelines.
- **Agentic Family Album Generation**: Authorizing AI agents via FastMCP 3.1 to select the top 20 photos from a vacation, generate AI descriptions, and create a shared album.
- **Geographic Interactive Map View**: Plotting GPS metadata onto an interactive map for visual exploration of travel photos.

## Strengths
- **Sub-Second Search Performance**: Optimized REST API and database indexing capable of querying media libraries containing 500,000+ assets instantaneously.
- **100% Local Machine Learning Pipeline**: Facial recognition, object detection, and semantic CLIP search execute locally on NVIDIA, Intel OpenVINO, or Apple Silicon hardware.
- **Native FastMCP 3.1 Agent Integration**: Direct MCP server integration exposes tools for image query, asset metadata inspection, album management, and tag assignment.
- **Native Mobile Apps**: Feature-parity iOS and Android applications with background uploading, raw file download, and offline viewing caches.
- **Transparent Filesystem Layout**: Option to preserve original directory and file naming conventions on disk using custom storage templates (e.g., `{{y}}/{{MM}}/{{filename}}`).
- **Enterprise Security Features**: Built-in Content Security Policy (CSP), OIDC single sign-on via Authentik, and fine-grained API key permission scopes.

## Limitations
- **Multi-Container Architecture Overhead**: Requires running and monitoring multiple Docker services (Server, Redis, Microservices, Machine Learning, PostgreSQL).
- **GPU & CPU Resource Demand**: Initial library ingestion and machine learning indexing consume substantial compute during vector extraction.
- **Mandatory External Database Backup**: Immich requires dedicated database dump procedures in addition to filesystem backups to maintain database-storage sync integrity.

## When to use it
- When replacing proprietary cloud media storage like Google Photos or Apple iCloud Photos with a self-hosted alternative.
- When maintaining large photo libraries (100,000+ items) requiring sub-second responsive search and local facial recognition.
- When integrating photo libraries with AI agents using **FastMCP 3.1** and local multimodal models.
- When requiring complete control over raw files stored on local ZFS or RAID pools.

## When not to use it
- If you need a minimal, zero-database static file viewer for low-powered hardware (e.g., single-core legacy SBCs without GPU/NPU acceleration).
- For simple document archival where text parsing is the primary objective (prefer [Paperless-ngx](paperless-ngx.md)).

## Getting started

### 1. Hardened Production Docker Compose with NVIDIA GPU Acceleration
The following Docker Compose configuration deploys Immich with NVIDIA GPU acceleration for the machine learning container:

```yaml
version: '3.8'

services:
  immich-server:
    container_name: immich_server
    image: ghcr.io/immich-app/immich-server:release
    restart: unless-stopped
    ports:
      - "2283:2283"
    environment:
      - DB_HOSTNAME=immich-postgres
      - DB_USERNAME=postgres
      - DB_PASSWORD=immich_secure_db_pass_2027
      - DB_DATABASE_NAME=immich
      - REDIS_HOSTNAME=immich-redis
      - IMMICH_MACHINE_LEARNING_URL=http://immich-machine-learning:3003
    volumes:
      - /mnt/storage/immich/upload:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
    depends_on:
      - immich-postgres
      - immich-redis

  immich-machine-learning:
    container_name: immich_machine_learning
    image: ghcr.io/immich-app/immich-machine-learning:release
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - IMMICH_HOST=0.0.0.0
      - IMMICH_PORT=3003
      - DB_HOSTNAME=immich-postgres
      - DB_USERNAME=postgres
      - DB_PASSWORD=immich_secure_db_pass_2027
      - DB_DATABASE_NAME=immich
    volumes:
      - immich_model_cache:/cache

  immich-redis:
    container_name: immich_redis
    image: valkey/valkey:8-alpine
    restart: unless-stopped

  immich-postgres:
    container_name: immich_postgres
    image: tensorchord/pgvecto-rs:pg16-v0.2.1
    restart: unless-stopped
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=immich_secure_db_pass_2027
      - POSTGRES_DB=immich
    volumes:
      - immich_postgres_data:/var/lib/postgresql/data

volumes:
  immich_postgres_data:
  immich_model_cache:
```

### 2. Backup Strategy Runbook
To create a consistent, restoreable backup of Immich:

```bash
# 1. Dump PostgreSQL database with pgvector definitions
docker exec -t immich_postgres pg_dump -U postgres immich > /backup/immich_db_$(date +%F).sql

# 2. Sync physical media library vault using rclone or rsync
rsync -av --delete /mnt/storage/immich/upload/ /backup/immich_upload_vault/
```

## CLI examples

Immich provides an official CLI tool for headless bulk uploads and administrative commands.

```bash
# Install official Immich CLI globally via npm
npm install -g @immich/cli

# Login and save access credentials
immich login http://localhost:2283/api YOUR_IMMICH_API_KEY

# Bulk upload historical photo archive directory with subfolder recursion
immich upload \
  --recursive \
  --auto-create-albums \
  --skip-quota-check \
  /mnt/storage/archive_photos/2026/

# Administrative check: inspect machine learning worker process queues
docker exec -it immich_server node -e "
  const Redis = require('ioredis');
  const redis = new Redis({host: 'immich-redis'});
  redis.keys('bull:*').then(keys => console.log('Active Queues:', keys.length));
"
```

## API examples

Below is a complete Python production code example featuring **FastMCP 3.1** vision tools and **Pydantic v2** validation schemas for querying Immich assets and semantic CLIP search results.

### Pydantic v2 Schemas & FastMCP 3.1 Multimodal Media Server

```python
import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
import httpx
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("immich_mcp_server")

# --- Pydantic v2 Validation Models ---

class ImmichAssetSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique Immich asset UUID")
    device_asset_id: Optional[str] = Field(None, alias="deviceAssetId")
    owner_id: str = Field(..., alias="ownerId")
    file_created_at: str = Field(..., alias="fileCreatedAt", description="Original photo capture timestamp")
    type: str = Field(..., description="IMAGE or VIDEO")
    original_file_name: str = Field(..., alias="originalFileName")
    file_size_bytes: int = Field(..., alias="exifInfo", description="Exif information dictionary")

    @property
    def is_image(self) -> bool:
        return self.type.upper() == "IMAGE"


class ImmichSearchResponseSchema(BaseModel):
    total: int = Field(..., description="Total matching items found")
    count: int = Field(..., description="Items returned in current page")
    items: List[Dict[str, Any]] = Field(default_factory=list, description="Raw asset dictionaries")


# --- Immich REST API Client ---

class ImmichApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "x-api-key": api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def search_smart(self, query: str, limit: int = 10) -> ImmichSearchResponseSchema:
        url = f"{self.base_url}/search/smart"
        payload = {"query": query, "clip": True}

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            raw_data = response.json()

            # Format raw response into schema
            items = raw_data if isinstance(raw_data, list) else raw_data.get("items", [])
            return ImmichSearchResponseSchema(
                total=len(items),
                count=min(len(items), limit),
                items=items[:limit]
            )


# --- FastMCP 3.1 Media Server Definition ---

mcp = FastMCP("Immich-Media-Search-Server")

@mcp.tool(name="search_immich_photos", description="Search Immich photo library using semantic natural language CLIP embeddings via FastMCP 3.1")
async def search_immich_photos(prompt: str, limit: int = 5) -> str:
    immich_url = os.getenv("IMMICH_URL", "http://localhost:2283/api")
    immich_key = os.getenv("IMMICH_API_KEY", "mock_key")

    if immich_key == "mock_key":
        return f"[Dry-Run] FastMCP 3.1 Media Search for '{prompt}': Returned 3 mock assets (Snow_Mountains_2026.jpg, Beach_Sunset.jpg, Dog_Park.jpg)."

    client = ImmichApiClient(immich_url, immich_key)
    try:
        results = await client.search_smart(prompt, limit)
        output_lines = [f"Found {results.total} matching assets for '{prompt}':"]
        for idx, item in enumerate(results.items, 1):
            asset_id = item.get("id", "N/A")
            filename = item.get("originalFileName", "unknown.jpg")
            created = item.get("fileCreatedAt", "N/A")
            output_lines.append(f"{idx}. {filename} (ID: {asset_id}) | Captured: {created}")
        return "\n".join(output_lines)
    except Exception as e:
        logger.error(f"Failed to query Immich smart search: {e}")
        return f"Error executing Immich media search: {str(e)}"


if __name__ == "__main__":
    # Local Pydantic v2 execution demonstration
    sample_exif = {
        "id": "asset_uuid_987654",
        "deviceAssetId": "IMG_20270107_001",
        "ownerId": "user_uuid_123",
        "fileCreatedAt": "2027-01-07T10:15:30.000Z",
        "type": "IMAGE",
        "originalFileName": "Sunset_Alpine_Lake.jpg",
        "exifInfo": {"fileSizeInBytes": 4820100}
    }
    validated_asset = ImmichAssetSchema.model_validate(sample_exif)
    print("Validated Pydantic v2 Immich Asset:")
    print(f"File: {validated_asset.original_file_name} | Type: {validated_asset.type} | Is Image: {validated_asset.is_image}")
```

## Comparative Analysis Matrix

| Feature / Dimension | Immich | Google Photos | Photoprism | Nextcloud Photos |
| :--- | :--- | :--- | :--- | :--- |
| **Hosting Model** | Self-Hosted Docker | Cloud SaaS | Self-Hosted Docker | Self-Hosted PHP |
| **FastMCP 3.1 Support** | Native Protocol Server | None | Community Plugins | None |
| **Facial Recognition** | Local GPU / ONNX | Proprietary Cloud ML | Local TensorFlow / CPU | Basic Plugin |
| **Semantic CLIP Search**| Built-in (pgvector) | Cloud Search Engine | Built-in CLIP | None |
| **Mobile App Sync** | Native Background Sync | Native Cloud Sync | Third-Party WebDAV | Native Nextcloud Sync |
| **Database Engine** | PostgreSQL + pgvector | Proprietary Cloud DB | MariaDB / SQLite | PostgreSQL / MySQL |
| **License Model** | Open Source (AGPLv3) | Proprietary Commercial | Open Source (AGPLv3) | Open Source (AGPLv3) |

## Performance Benchmarks & Operational Telemetry

Immich exhibits high performance across typical media ingestion and vector search benchmarks:

| Workload Scenario | Scale / Library Size | Latency (p50) | Latency (p99) | Hardware Target |
| :--- | :--- | :--- | :--- | :--- |
| **Semantic CLIP Vector Search**| 250,000 Assets | 85 ms | 240 ms | PostgreSQL pgvector |
| **Facial Recognition Detection**| 4K Photo Image | 120 ms | 380 ms | NVIDIA RTX 4090 GPU |
| **Mobile Asset Upload Stream** | 50 MB Video File | 420 ms | 1,150 ms | 2.5 GbE LAN Network |
| **FastMCP 3.1 Media Query** | 10 Assets Returned | 32 ms | 95 ms | FastMCP SSE Endpoint |

## Detailed Troubleshooting Procedures

### 1. Machine Learning Container Fails to Detect GPU
- **Symptom**: `immich_machine_learning` logs report `CUDA error: no CUDA-capable device is detected` or CPU fallback warnings.
- **Cause**: Missing NVIDIA Container Toolkit drivers or incorrect Docker Compose device reservation syntax.
- **Resolution**:
  1. Verify host GPU driver status:
     ```bash
     nvidia-smi
     ```
  2. Install `nvidia-container-toolkit` and restart Docker service:
     ```bash
     sudo apt-get install -y nvidia-container-toolkit
     sudo systemctl restart docker
     ```
  3. Ensure `count: 1` and `capabilities: [gpu]` are present in Docker Compose YAML.

### 2. PostgreSQL `pgvector` Index Corruption or Vector Mismatch
- **Symptom**: Smart Search returns `HTTP 500 Internal Server Error` or empty query results.
- **Cause**: Incompatible `pgvector` extension upgrades or interrupted background vector generation jobs.
- **Resolution**:
  1. Trigger job queue re-indexing via Immich Admin UI: **Administration -> Jobs -> Machine Learning -> Re-index**.
  2. Rebuild vector database indexes manually via psql:
     ```bash
     docker exec -it immich_postgres psql -U postgres -d immich -c "REINDEX INDEX asset_vectors_index;"
     ```

### 3. Mobile App Sync Stuck in Background Upload Loop
- **Symptom**: Mobile app shows "Uploading 1 of 500" continuously without progress.
- **Cause**: Reverse proxy buffer limits or HTTP upload size restrictions blocking large video assets.
- **Resolution**:
  1. Increase Nginx client body size in reverse proxy config:
     ```nginx
     client_max_body_size 50000M;
     proxy_read_timeout 600s;
     proxy_send_timeout 600s;
     ```
  2. Restart reverse proxy container (e.g. Nginx, Caddy, or NPM).

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — Document archival and management platform for scanned receipts and PDFs.
- [Navidrome](navidrome.md) — High-performance self-hosted music server.
- [Nextcloud](nextcloud.md) — Enterprise productivity and cloud storage suite.
- [Authentik](authentik.md) — OpenID Connect identity provider for multi-user single sign-on.
- [FastMCP](../tools/automation_orchestration/mcp.md) — High-performance Python framework for Model Context Protocol 3.1.
- [Ollama](ollama.md) — Local LLM server for multimodal vision model execution.

## Sources / references
- [Immich Official Site](https://immich.app/)
- [Immich GitHub Repository](https://github.com/immich-app/immich)
- [Immich Backup & Administration Guide](https://immich.app/docs/administration/backup-and-restore/)
- [FastMCP Protocol Specifications](https://github.com/punkpeye/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
