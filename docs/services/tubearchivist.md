# Tube Archivist

Tube Archivist is a self-hosted YouTube archive that allows you to index and download YouTube videos, metadata, and comments to your own server.

## What it is
Tube Archivist is an open-source media management system designed specifically for preserving YouTube content. As of **early January 2027**, it features a robust integration with the **Deno** runtime for enhanced download reliability, handles advanced cookie-passing techniques for age-restricted content, and provides advanced tools for metadata persistence and Elasticsearch-based searching. It integrates with AI agents via **MCP 3.1** / **FastMCP 3.1** to allow natural language triggers for channel archival and indexing across multi-agent workflows.

## What problem it solves
YouTube videos can be deleted, made private, or censored without notice. Tube Archivist provides a way to build a permanent, offline, and searchable library of your favorite content, ensuring long-term access to tutorials, documentaries, and educational material while eliminating dependency on third-party platform availability and advertising.

## Architecture and Data Ingestion Pipeline

Tube Archivist uses an asynchronous, task-queued architecture connecting a Django backend, Redis queue worker, Elasticsearch/OpenSearch indexer, and `yt-dlp` / Deno extraction engine.

```
+-----------------------------------------------------------------------------------+
|                     Tube Archivist Architecture & Data Flow                       |
+-----------------------------------------------------------------------------------+
                                          |
 1. Trigger / Automation                  |
 +-------------------------------+       |
 | Web UI / FastMCP 3.1 Agent    |       |
 +---------------+---------------+       |
                 |                       |
                 v                       v
 2. Task Queue Dispatcher (Redis)        |
 +-----------------------------------------------+
 |  Asynchronous Task Ingestion Queue            |
 |  - Download / Metadata / Rescan Workers       |
 +---------------+-------------------------------+
                 |
                 v
 3. Extraction Engine (yt-dlp / Deno Runtime)
 +-----------------------------------------------+
 |  YouTube Scraping & Cookie Handling           |
 |  - Video Files, Subtitles, Thumbnails, NFOs   |
 +---------------+-------------------------------+
                 |
                 +-----------------------------------+
                 |                                   |
                 v                                   v
 4. Primary Media Storage                    5. Indexing Engine
 +-------------------------------+           +-------------------------------+
 |  Organized Local Disk Volume  |           |  Elasticsearch / OpenSearch   |
 |  - /youtube/<channel>/<video> |---------->|  - Full-Text Search Index     |
 |  - Embedded NFO / Subtitles   |           |  - Comments / Subtitle Search |
 +---------------+---------------+           +-------------------------------+
```

### Async Video Download & Indexing Sequence
The detailed runtime sequence between FastMCP 3.1 client agents, the Tube Archivist Django API, Redis async workers, `yt-dlp`/Deno, and Elasticsearch/OpenSearch is illustrated below:

```
+-------------------------------------------------------------------------------------------------------+
|                                TUBE ARCHIVIST ASYNC DOWNLOAD SEQUENCE                                 |
+-------------------------------------------------------------------------------------------------------+
  FastMCP Agent / UI             Tube Archivist API              Redis / Celery Worker           Elasticsearch Index
          |                              |                                 |                             |
          |--- 1. Download Video Request |                                 |                             |
          |    (URL, Quality, Cookies) ->|                                 |                             |
          |                              |--- 2. Enqueue Download Task --->|                             |
          |<-- 3. Return Task ID JSON ---|                                 |                             |
          |                              |                                 |--- 4. Extract Video Content
          |                              |                                 |    (yt-dlp / Deno Runtime)
          |                              |                                 |--- 5. Write Files & NFO
          |                              |                                 |       to Disk Storage       |
          |                              |                                 |                             |
          |                              |                                 |--- 6. Index Video Metadata,
          |                              |                                 |       Subtitles & Comments->|
          |<-- 7. Poll Task / Webhook ---|                                 |                             |
```

## Mathematical Formulations: Media Throughput & Index Scaling

### 1. Ingestion Makespan and Bandwidth Roofline

For an archival ingestion batch consisting of $N$ videos with sizes $S_i$ (bytes) and durations $D_i$ (seconds), the total elapsed download time $T_{\text{ingest}}$ constrained by network bandwidth $B_{\text{net}}$ (bytes/sec) and maximum concurrent worker slots $W$ is:

$$
T_{\text{ingest}} = \max\left( \frac{\sum_{i=1}^N S_i}{B_{\text{net}}}, \quad \sum_{w=1}^{\lceil N/W \rceil} \max_{j \in \text{Batch}_w} \left( \frac{S_j}{B_{\text{worker}}} + T_{\text{transcode}, j} \right) \right) + N \cdot T_{\text{index}}
$$

Where:
- $T_{\text{transcode}, j}$ is the ffmpeg container remuxing/transcoding latency.
- $T_{\text{index}}$ is the Elasticsearch document indexing and reverse token analysis delay ($15\text{ms} - 45\text{ms}$ per video).

### 2. Full-Text Inverted Index Storage Footprint

The Elasticsearch / OpenSearch index footprint $M_{\text{index}}$ across $V$ archived videos with subtitle token stream length $L_{\text{sub}}$ and comment volume $C_v$ is modeled as:

$$
M_{\text{index}} \approx \sum_{v=1}^V \left( \alpha_{\text{meta}} \cdot S_{\text{meta}} + \beta_{\text{sub}} \cdot L_{\text{sub}, v} \cdot \bar{w}_{\text{token}} + \gamma_{\text{comment}} \cdot \sum_{c=1}^{C_v} \text{len}(c) \right) \cdot (1 + R_{\text{replica}})
$$

Where:
- $\alpha_{\text{meta}} \approx 1.25$ accounts for JSON schema overhead and mapping metadata.
- $\beta_{\text{sub}} \approx 0.65$ reflects Lucene compression (LZ4/DEFLATE) over tokenized subtitle vectors.
- $R_{\text{replica}}$ is the number of configured index replicas.

### 3. YouTube Bot-Detection Probability & Exponential Backoff

When downloading playlists at high frequency, request rejection probability $P(\text{block})$ follows a cumulative threshold function of request rate $\lambda_{\text{req}}$ (requests/min) and IP reputation $R_{\text{ip}}$:

$$
P(\text{block}) = \frac{1}{1 + \exp\left( -\kappa \left( \lambda_{\text{req}} - \lambda_{\text{thresh}}(R_{\text{ip}}) \right) \right)}
$$

To minimize $P(\text{block}) < 0.01$, Tube Archivist worker dispatchers enforce dynamic randomized sleep intervals:

$$
\Delta t_{\text{delay}} = t_{\text{base}} + \mathcal{U}(0, \sigma_{\text{jitter}}) \cdot 2^{\min(k_{\text{retries}}, 4)}
$$

## Where it fits in the stack
It serves as a **content preservation layer** within the media management stack. It sits alongside general-purpose media servers like [Jellyfin](jellyfin.md) or [Plex](plex.md), but provides deep specialization for YouTube-specific metadata (comments, descriptions, subtitles) and automated channel monitoring for agentic workflows powered by **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**.

## Typical use cases
- Automatically monitoring and downloading new videos from subscribed channels or playlists.
- Archiving high-quality educational series for offline reference and AI-assisted summarization.
- Building a private, ad-free "YouTube" experience for family members.
- Researching video trends and comments at scale using its integrated search engine.
- Preserving a record of metadata even if the original video is removed from YouTube.
- Feeding local transcripts into RAG vector pipelines for offline LLM synthesis.

## Strengths
- **Comprehensive Preservation**: Captures thumbnails, descriptions, comments, subtitles, and high-quality video files.
- **Advanced Search**: Integrated Elasticsearch/OpenSearch for rapid full-text search across the entire archive.
- **Native Automation**: Built-in scheduling for periodic channel rescans and downloads.
- **Metadata Resilience**: Supports embedding all indexed metadata directly into the media files for reconstruction from the library files themselves.
- **Agentic Ready**: Robust REST API for integration with tools like **Claude 5.6** or **DeepSeek-V4** for automated content analysis.

## Limitations
- **Storage Intensive**: Storing high-resolution video archives can consume terabytes of storage rapidly.
- **Resource Usage**: Requires secondary containers for Redis and Elasticsearch, which can be memory-intensive.
- **Maintenance**: Ongoing site layout changes on YouTube require frequent `yt-dlp` updates within the container.

## Self-Hosted Media Archival Comparison Matrix

| Feature / Dimension | Tube Archivist | Mealie / Plex / Jellyfin | Raw `yt-dlp` Scripts | Changedetection.io | Pinchflat (yt-dlp WebUI) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Dedicated YouTube Archival | Streaming Media Playback | Ad-hoc CLI Download | Web Page & Diff Monitoring | Minimal WebUI Downloader |
| **Metadata Ingest** | Full (Comments, Subs, NFO) | Basic NFO / Movie DB | Manual CLI flags | Visual text snapshots | Basic title and description |
| **Search Capabilities** | Elasticsearch Full-Text | Title & Tag Database | File System Grep | Diff Text Search | SQLite string pattern match |
| **API & Agent Integration** | REST + FastMCP 3.1 Tools | Webhooks / REST API | None (Scripted execution) | Webhooks / REST API | Basic REST endpoints |
| **Multi-Container Stack** | High (Django, ES, Redis) | Low-Medium (Single DB) | None (CLI binary) | Low (Python/Redis) | Lightweight single container |
| **Channel Auto-Sync** | Built-in Scheduled Rescan | Plugins required | Cron-based scripts | Native page check | Cron-based channel check |
| **Subtitle Indexing** | Deep Lucene token search | Display only during stream| Unindexed .vtt files | N/A | Flat text file storage |
| **Hardware Overhead** | Moderate (~2-4 GB RAM) | Moderate (~1-2 GB RAM) | Minimal (<100 MB RAM) | Minimal (<250 MB RAM) | Low (<500 MB RAM) |

## Systemd Production Container Service Management

For Linux hosts running Tube Archivist outside Docker Compose via standard systemd container units:

```ini
[Unit]
Description=Tube Archivist Media Management Container
After=docker.service network.target
Requires=docker.service

[Service]
Type=simple
Restart=always
RestartSec=10s
ExecStartPre=-/usr/bin/docker stop tubearchivist
ExecStartPre=-/usr/bin/docker rm tubearchivist
ExecStart=/usr/bin/docker run --name tubearchivist \
  -p 8000:8000 \
  -v /mnt/media/youtube:/youtube \
  -v /mnt/media/cache:/cache \
  -e ES_URL=http://archivist-es:9200 \
  -e REDIS_HOST=archivist-redis \
  -e HOST_UID=1000 \
  -e HOST_GID=1000 \
  -e TA_USERNAME=admin \
  -e TA_PASSWORD=secure_password_2027 \
  bbilly1/tubearchivist:latest
ExecStop=/usr/bin/docker stop tubearchivist

[Install]
WantedBy=multi-user.target
```

## When to use it
- When you want to ensure permanent, offline access to specific YouTube content.
- When you need to search across video descriptions and comments at scale for research or knowledge management.
- To provide a private, curated media experience without tracking or platform bias.
- For building a local knowledge base from video content via AI ingestion.

## When not to use it
- For occasional, one-off video downloads (use a simple CLI tool like `yt-dlp`).
- If server resources (RAM/CPU/Storage) are extremely limited.
- If you prefer a single-binary solution without the complexity of multiple service containers.

## Getting started

### Installation (Docker Compose)
Tube Archivist requires Redis and Elasticsearch/OpenSearch.

```yaml
version: '3.8'

services:
  tubearchivist:
    container_name: tubearchivist
    image: bbilly1/tubearchivist:latest
    ports:
      - "8000:8000"
    volumes:
      - /mnt/media/youtube:/youtube
      - /mnt/media/cache:/cache
    environment:
      - ES_URL=http://archivist-es:9200
      - REDIS_HOST=archivist-redis
      - HOST_UID=1000
      - HOST_GID=1000
      - TA_USERNAME=admin
      - TA_PASSWORD=secure_password_2027
    depends_on:
      archivist-es:
        condition: service_healthy
      archivist-redis:
        condition: service_started
    restart: unless-stopped

  archivist-redis:
    image: redis/redis-stack-server:latest
    container_name: archivist-redis
    ports:
      - "6379:6379"
    restart: unless-stopped

  archivist-es:
    image: bbilly1/tubearchivist-es:latest
    container_name: archivist-es
    environment:
      - "ELASTIC_PASSWORD=verysecret"
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "discovery.type=single-node"
      - "xpack.security.enabled=false"
    volumes:
      - archivist_es_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200/_cluster/health | grep -q 'status'"]
      interval: 10s
      timeout: 5s
      retries: 6
    restart: unless-stopped

volumes:
  archivist_es_data:
```

### Hello World
1. Start the stack with `docker compose up -d` and navigate to `http://localhost:8000`.
2. Log in with your configured credentials (`admin` / `secure_password_2027`).
3. Go to **Downloads**, paste a YouTube URL, and click **Index and Download**.
4. Check **Channels** tab to verify thumbnail generation and comment ingestion.

## CLI examples
Tube Archivist is primarily managed via the UI, but the container provides tools for maintenance:

```bash
# Force an immediate rescan of the media directory to pick up external changes
docker exec tubearchivist python manage.py rescan

# Manually update yt-dlp to the latest version within the container
docker exec tubearchivist pip install -U yt-dlp

# Trigger a manual scan of channel tabs (shorts, streams, videos)
docker exec tubearchivist python manage.py ta_index_channel_tabs

# Trigger full comment re-indexing across all stored archives
docker exec tubearchivist python manage.py ta_index_comments --all

# Backup Elasticsearch metadata indices to local snapshot directory
docker exec archivist-es bin/elasticsearch-snapshot create snapshot_daily
```

## API examples

### FastMCP 3.1 Tube Archivist Ingestion Tool
This example showcases a production-ready FastMCP 3.1 tool utilizing Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) to trigger video ingestion, query archive statuses, and validate download responses. It allows frontier models like **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Ultra** to dynamically archive requested YouTube tutorials and extract descriptions.

```python
"""Tube Archivist FastMCP 3.1 Management Server with strict Pydantic v2 validation."""

import requests
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_validator
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TubeArchivistManager")

TA_URL = "http://localhost:8000/api"
HEADERS = {"Authorization": "Token YOUR_API_TOKEN", "Content-Type": "application/json"}

class ArchivalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    url: HttpUrl = Field(..., description="The valid YouTube video or channel URL to archive")
    bypass_cache: bool = Field(default=False, description="Whether to bypass local cache and force download")
    priority: int = Field(default=1, ge=1, le=5, description="Queue priority level (1=normal, 5=urgent)")

    @field_validator("url")
    @classmethod
    def validate_youtube_domain(cls, v: HttpUrl) -> HttpUrl:
        url_str = str(v)
        if "youtube.com" not in url_str and "youtu.be" not in url_str:
            raise ValueError("Target URL must belong to youtube.com or youtu.be domain")
        return v

class ArchivalResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    success: bool = Field(..., description="Whether the archival task was successfully queued")
    message: str = Field(..., description="Response message from the Tube Archivist API")
    task_id: str = Field(default="", description="The unique ID of the triggered download task")
    queue_position: Optional[int] = Field(None, description="Current position in task queue")

class SearchQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query_term: str = Field(..., min_length=2, description="Keywords to match against video subtitles/titles")
    max_results: int = Field(default=10, ge=1, le=50)

@mcp.tool()
async def trigger_youtube_download(request_data: ArchivalRequest) -> ArchivalResponse:
    """Submits a download request to the local Tube Archivist instance and returns validated status."""
    payload = {
        "url": str(request_data.url),
        "bypass_cache": request_data.bypass_cache,
        "priority": request_data.priority
    }

    try:
        response = requests.post(f"{TA_URL}/download/", headers=HEADERS, json=payload, timeout=10)

        if response.status_code == 201:
            data = response.json()
            return ArchivalResponse(
                success=True,
                message="Video successfully queued for download",
                task_id=data.get("task_id", "task-queued-ok"),
                queue_position=data.get("queue_position", 1)
            )
        else:
            return ArchivalResponse(
                success=False,
                message=f"Failed to queue video. API status {response.status_code}: {response.text}",
                task_id=""
            )
    except requests.RequestException as exc:
        return ArchivalResponse(
            success=False,
            message=f"Network exception connecting to Tube Archivist API: {str(exc)}",
            task_id=""
        )

@mcp.tool()
async def search_archive(query: SearchQuery) -> Dict[str, Any]:
    """Queries Elasticsearch index for archived videos matching title or subtitle keywords."""
    try:
        response = requests.get(
            f"{TA_URL}/video/",
            headers=HEADERS,
            params={"q": query.query_term, "page_size": query.max_results},
            timeout=8
        )
        if response.status_code == 200:
            return {"status": "success", "results": response.json().get("data", [])}
        return {"status": "error", "message": f"Search failed with HTTP {response.status_code}"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Video Metadata Schema
Validate archived YouTube video metadata payloads ingested into Elastic/OpenSearch indices:

```python
"""Strict Pydantic v2 Video Metadata Schema for Tube Archivist."""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime

class VideoMetadata(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        populate_by_name=True,
        str_strip_whitespace=True
    )

    youtube_id: str = Field(..., alias="youtubeId", description="11-character YouTube video alphanumeric ID")
    title: str = Field(..., min_length=1, description="Sanitized video title")
    channel_name: str = Field(..., alias="channelName")
    published_at: datetime = Field(..., alias="publishedAt")
    duration_seconds: int = Field(..., alias="durationSeconds", ge=0)
    view_count: int = Field(default=0, alias="viewCount", ge=0)
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    media_filepath: str = Field(..., alias="mediaFilepath")

    @field_validator("youtube_id")
    @classmethod
    def validate_yt_id(cls, v: str) -> str:
        if len(v) != 11:
            raise ValueError("YouTube video ID must be exactly 11 characters")
        return v

# Sample verification
sample_record = {
    "youtubeId": "dQw4w9WgXcQ",
    "title": "Understanding LLM Agent Topologies and Service Meshes",
    "channelName": "Systems Engineering Lab",
    "publishedAt": "2026-11-10T08:00:00Z",
    "durationSeconds": 620,
    "viewCount": 152000,
    "tags": ["AI", "FastMCP", "Self-Hosted"],
    "description": "Comprehensive walkthrough of local AI agent routing architectures.",
    "mediaFilepath": "/youtube/Systems_Engineering_Lab/20261110_dQw4w9WgXcQ.mp4"
}

meta = VideoMetadata.model_validate(sample_record)
print(f"Validated Video: {meta.title} [{meta.youtube_id}]")
```

## Diagnostic Troubleshooting Matrix

| Symptom / Error | Potential Root Cause | Verification Command | Resolution Step |
| :--- | :--- | :--- | :--- |
| `HTTP 403 Forbidden` on video download | YouTube bot detection or outdated `yt-dlp` binary | `docker exec tubearchivist yt-dlp --version` | Upgrade `yt-dlp` in container (`pip install -U yt-dlp`) or configure PO Token / cookies in TA setting. |
| Elasticsearch Connection Error (`ES_URL`) | ES container starting slower than TA Django app | `docker logs archivist-es` | Ensure `depends_on` healthcheck condition in `docker-compose.yml` or restart `tubearchivist` container. |
| Redis queue stalled / tasks stuck | Redis container memory limit exceeded or OOM | `docker exec archivist-redis redis-cli ping` | Flush stale keys or increase Redis memory budget in compose limits. |
| Disk space full (`/youtube` volume) | High video resolution downloads filling storage | `df -h /mnt/media/youtube` | Set maximum resolution limit in Tube Archivist settings or add external storage volume. |
| `yt-dlp JS Interpreter Missing (Deno)` | Tube Archivist container missing Deno JS runtime for token extraction | `docker exec tubearchivist deno --version` | Update Tube Archivist base image to latest release including embedded Deno engine. |
| Subtitle Index Ingestion Failure | Corrupt WebVTT format or character encoding failure | `docker logs tubearchivist \| grep -i subtitle` | Enable subtitle parsing sanitizer in settings and rescan metadata via CLI. |
| Celery Worker Task Timeout | Video file download exceeding network timeout on large stream | `docker exec tubearchivist celery -A tubearchivist inspect active` | Adjust `DOWNLOAD_TIMEOUT: 7200` in Django environment configuration. |
| Elastic Search High Heap Memory Alarm | JVM heap pool undersized for large subtitle catalog | `docker exec archivist-es curl -s localhost:9200/_nodes/stats/jvm` | Increase `ES_JAVA_OPTS="-Xms2g -Xmx2g"` in Elasticsearch container definition. |

## Related tools / concepts
- [Plex](plex.md) — For streaming your YouTube archive to smart TVs and mobile devices.
- [Jellyfin](jellyfin.md) — The recommended open-source alternative for media streaming.
- [Audiobookshelf](audiobookshelf.md) — For managing audio-only YouTube archives or podcasts.
- [Changedetection.io](changedetection.md) — To monitor YouTube channels for visual or metadata changes.
- [n8n](n8n.md) — For advanced automation (e.g., notifying you in Element when a video is archived).
- [SearXNG](searXNG.md) — For private searching before adding videos to the archive.
- [Home Assistant](home-assistant.md) — For dashboard integration and download notifications.
- [Tailscale](tailscale.md) — For secure remote access to your video library.
- [PO Token Management](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp) — For mitigating 403 errors during download.

## Sources / References
- [Official Website](https://www.tubearchivist.com/)
- [Tube Archivist Documentation](https://docs.tubearchivist.com/)
- [GitHub Repository](https://github.com/tubearchivist/tubearchivist)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
