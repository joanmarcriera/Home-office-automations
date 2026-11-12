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

## Mathematical Formulations & Media Ingestion Dynamics

The operational performance, storage capacity planning, and indexing scalability of Tube Archivist are determined by three core analytical dynamics: media transcode bitrate allocation, Elasticsearch BM25 full-text subtitle indexing complexity, and async queue delay rooflines.

### 1. Storage Capacity Planning & Transcoding Bitrate
Let $D$ denote the duration of the video in seconds, $R_{\text{res}}$ denote the target resolution format (e.g. 1080p60, 4K120), and $\mathcal{B}_{\text{video}}, \mathcal{B}_{\text{audio}}$ denote the respective average bitrates in kilobits per second (kbps). The raw media storage consumption $S_{\text{media}}$ in bytes is governed by:

$$
S_{\text{media}} = \frac{(\mathcal{B}_{\text{video}} + \mathcal{B}_{\text{audio}}) \cdot D}{8 \times 1024} + S_{\text{metadata}} + S_{\text{subs}}
$$

For multi-channel bulk subscription archiving, the aggregate monthly storage expansion $\Delta S_{\text{monthly}}$ across $K$ subscribed channels with average publishing frequency $f_k$ (videos/month) is modeled as:

$$
\Delta S_{\text{monthly}} = \sum_{k=1}^K f_k \cdot \mathbb{E}[S_{\text{media}, k}]
$$

For high-bitrate AV1 or VP9 video streams (e.g., $18.5\,\text{Mbps}$ for 4K60), a channel releasing 12 videos/month averaging 35 minutes consumes approximately $58.2\,\text{GB/month}$. Incorporating local Whisper ASR re-transcription adds vector embedding storage overhead $S_{\text{embed}} = N_{\text{chunks}} \cdot d \cdot 4\,\text{bytes}$.

### 2. Elasticsearch BM25 Subtitle & Comment Full-Text Relevance
Tube Archivist ingests video transcriptions (.vtt/.srt) and user comments into Elasticsearch indices configured with the Okapi BM25 scoring model. Given a search query $Q = \{q_1, q_2, \dots, q_n\}$ and subtitle document $D_{\text{sub}}$:

$$
\text{Score}_{\text{BM25}}(D_{\text{sub}}, Q) = \sum_{i=1}^n \text{IDF}(q_i) \cdot \frac{f(q_i, D_{\text{sub}}) \cdot (k_1 + 1)}{f(q_i, D_{\text{sub}}) + k_1 \cdot \left(1 - b + b \cdot \frac{|D_{\text{sub}}|}{\text{avgdl}}\right)}
$$

Where $k_1 = 1.2$, $b = 0.75$, $|D_{\text{sub}}|$ is the token length of the transcribed video segments, and $\text{IDF}(q_i) = \ln\left( \frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1 \right)$. This allows sub-second cross-video dialogue search across archives exceeding 50,000 indexed episodes.

### 3. Task Queue Wait-Time Roofline ($M/M/c$ Queuing Model)
When automated channel monitor cronjobs fire simultaneously, video download ingestion tasks are queued in Redis. Modeling the worker pool with $c$ concurrent download threads, Poisson arrival rate $\lambda_{\text{tasks}}$, and exponential service completion rate $\mu_{\text{download}}$:

$$
\rho = \frac{\lambda_{\text{tasks}}}{c \cdot \mu_{\text{download}}} < 1
$$

The expected waiting time in the download queue $W_q$ before an extraction worker claims the task is modeled as:

$$
W_q = \frac{P_0 \cdot \left( \frac{\lambda}{\mu} \right)^c \cdot \rho}{c! \cdot (1 - \rho)^2 \cdot \lambda}
$$

Where $P_0$ is the probability that all workers are idle:

$$
P_0 = \left[ \sum_{k=0}^{c-1} \frac{1}{k!} \left( \frac{\lambda}{\mu} \right)^k + \frac{1}{c!} \left( \frac{\lambda}{\mu} \right)^c \frac{1}{1 - \rho} \right]^{-1}
$$

When network bandwidth or YouTube rate limits reduce $\mu_{\text{download}}$ such that $\rho \to 1.0$, $W_q$ exhibits exponential queuing blowup, mandating concurrency backoff and token bucket pacing.

## Where it fits in the stack
It serves as a **content preservation layer** within the media management stack. It sits alongside general-purpose media servers like [Jellyfin](jellyfin.md) or [Plex](plex.md), but provides deep specialization for YouTube-specific metadata (comments, descriptions, subtitles) and automated channel monitoring for agentic workflows powered by **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**.

## Typical use cases
- Automatically monitoring and downloading new videos from subscribed channels or playlists.
- Archiving high-quality educational series for offline reference and AI-assisted summarization.
- Building a private, ad-free "YouTube" experience for family members.
- Researching video trends and comments at scale using its integrated search engine.
- Preserving a record of metadata even if the original video is removed from YouTube.

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

| Feature / Dimension | Tube Archivist | Mealie / Plex / Jellyfin | Raw `yt-dlp` Scripts | Changedetection.io | Metube |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Dedicated YouTube Archival | Streaming Media Playback | Ad-hoc CLI Download | Web Page & Diff Monitoring | Simple yt-dlp Web UI |
| **Metadata Ingest** | Full (Comments, Subs, NFO) | Basic NFO / Movie DB | Manual CLI flags | Visual text snapshots | Audio/Video title only |
| **Search Capabilities** | Elasticsearch Full-Text | Title & Tag Database | File System Grep | Diff Text Search | None (Flat file list) |
| **API & Agent Integration** | REST + FastMCP 3.1 Tools | Webhooks / REST API | None (Scripted execution) | Webhooks / REST API | Simple REST API |
| **Multi-Container Stack** | High (Django, ES, Redis) | Low-Medium (Single DB) | None (CLI binary) | Low (Python/Redis) | Standalone Container |
| **Channel Auto-Sync** | Built-in Scheduled Rescan | Plugins required | Cron-based scripts | Native page check | None |
| **Storage Deduplication** | Channel & Video ID Index | File hash scan | Manual overwrite flags| Text snapshot storage | Filename check only |

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
ExecStartPre=/usr/bin/docker pull bbilly1/tubearchivist:latest
ExecStart=/usr/bin/docker run --rm --name tubearchivist \
  -p 8000:8000 \
  -v /mnt/media/youtube:/youtube \
  -v /mnt/media/cache:/cache \
  -e ES_URL=http://archivist-es:9200 \
  -e REDIS_HOST=archivist-redis \
  -e HOST_UID=1000 \
  -e HOST_GID=1000 \
  bbilly1/tubearchivist:latest
ExecStop=/usr/bin/docker stop tubearchivist

[Install]
WantedBy=multi-user.target
```

### Tube Archivist Background Worker Daemon (`tubearchivist-worker.service`)
In decoupled bare-metal deployments where background Celery workers run directly on dedicated GPU/host nodes:

```ini
[Unit]
Description=Tube Archivist Background Task Worker Daemon
After=network.target redis.service elasticsearch.service
Wants=redis.service elasticsearch.service

[Service]
Type=simple
User=tubearchivist
Group=tubearchivist
WorkingDirectory=/opt/tubearchivist
ExecStart=/opt/tubearchivist/venv/bin/celery -A tubearchivist worker -l INFO -c 4
Restart=always
RestartSec=5s
Environment="REDIS_HOST=127.0.0.1"
Environment="ES_URL=http://127.0.0.1:9200"
Environment="PYTHONUNBUFFERED=1"
LimitNOFILE=65536

# Hardening
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true

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
      - TA_PASSWORD=archivist_secure_password
      - TA_HOST=http://localhost:8000
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
    volumes:
      - archivist_redis_data:/data
    restart: unless-stopped

  archivist-es:
    image: bbilly1/tubearchivist-es:latest
    container_name: archivist-es
    environment:
      - "ELASTIC_PASSWORD=verysecret"
      - "ES_JAVA_OPTS=-Xms1024m -Xmx1024m"
      - "discovery.type=single-node"
      - "xpack.security.enabled=true"
    volumes:
      - archivist_es_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200 | grep -q 'You Know, for Search'"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  archivist_redis_data:
  archivist_es_data:
```

### Hello World
1. Start the stack and navigate to `http://localhost:8000`.
2. Log in with your configured credentials.
3. Go to **Downloads**, paste a YouTube URL, and click **Index and Download**.

## CLI examples
Tube Archivist is primarily managed via the UI, but the container provides tools for maintenance:

```bash
# Force an immediate rescan of the media directory to pick up external changes
docker exec tubearchivist python manage.py rescan

# Manually update yt-dlp to the latest version within the container
docker exec tubearchivist pip install -U yt-dlp

# Trigger a manual scan of channel tabs (shorts, streams, videos)
docker exec tubearchivist python manage.py ta_index_channel_tabs
```

## API examples

### FastMCP 3.1 Tube Archivist Ingestion Tool
This example showcases a production-ready FastMCP 3.1 tool utilizing strict **Pydantic v2** schemas (`extra="forbid"`, `frozen=True`) to trigger video ingestion and validate download responses. It allows frontier models like **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Ultra** to dynamically archive requested YouTube tutorials and extract descriptions.

```python
import requests
import time
from typing import Dict, Any, Optional, Literal, List
from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TubeArchivistManager", instructions="FastMCP 3.1 service tool for managing Tube Archivist downloads and indexing.")

TA_URL = "http://localhost:8000/api"
HEADERS = {"Authorization": "Token YOUR_API_TOKEN"}

class ArchivalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    url: HttpUrl = Field(..., description="The valid YouTube video or channel URL to archive")
    bypass_cache: bool = Field(default=False, description="Whether to bypass local cache and force download")
    preferred_quality: Literal["best", "1080p", "720p", "audio_only"] = Field(default="1080p")
    download_subtitles: bool = Field(default=True, description="Extract and index video subtitle streams")

class ArchivalResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["queued", "cached", "rejected", "error"]
    message: str = Field(description="Response message from the Tube Archivist API")
    task_id: str = Field(default="", description="The unique ID of the triggered download task")
    queue_wait_ms: float = Field(default=0.0)

@mcp.tool(name="trigger_youtube_download", description="Submits a download request to local Tube Archivist instance with validation.")
def trigger_youtube_download(request: ArchivalRequest) -> str:
    """
    Submits a download request to the local Tube Archivist instance, validates input,
    and returns a Pydantic v2 validated status JSON payload.
    """
    start_time = time.time()
    payload = {
        "url": str(request.url),
        "bypass_cache": request.bypass_cache,
        "quality": request.preferred_quality,
        "extract_subs": request.download_subtitles
    }

    try:
        response = requests.post(f"{TA_URL}/download/", headers=HEADERS, json=payload, timeout=10)
        elapsed = (time.time() - start_time) * 1000.0

        if response.status_code == 201:
            data = response.json()
            result = ArchivalResponse(
                status="queued",
                message="Video successfully queued for download",
                task_id=str(data.get("task_id", "task-ta-001")),
                queue_wait_ms=round(elapsed, 2)
            )
        else:
            result = ArchivalResponse(
                status="rejected",
                message=f"API responded with status {response.status_code}: {response.text}",
                task_id="",
                queue_wait_ms=round(elapsed, 2)
            )
        return result.model_dump_json()
    except requests.RequestException as e:
        elapsed = (time.time() - start_time) * 1000.0
        return ArchivalResponse(
            status="error",
            message=f"Network exception when connecting to Tube Archivist API: {str(e)}",
            task_id="",
            queue_wait_ms=round(elapsed, 2)
        ).model_dump_json()

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Video Metadata Schema
Validate archived YouTube video metadata payloads ingested into Elastic/OpenSearch indices:

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime

class VideoMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True, str_strip_whitespace=True)

    youtube_id: str = Field(..., alias="youtubeId")
    title: str = Field(...)
    channel_name: str = Field(..., alias="channelName")
    published_at: datetime = Field(..., alias="publishedAt")
    duration_seconds: int = Field(..., alias="durationSeconds", ge=0)
    view_count: int = Field(default=0, alias="viewCount", ge=0)
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    subtitles_indexed: bool = Field(default=False)

    @field_validator("youtube_id")
    @classmethod
    def validate_yt_id(cls, v: str) -> str:
        if len(v) != 11:
            raise ValueError("YouTube video ID must be exactly 11 characters")
        return v

# Sample validation
raw_meta = {
    "youtubeId": "dQw4w9WgXcQ",
    "title": "Sample Educational Video",
    "channelName": "Tech Academy",
    "publishedAt": "2026-11-10T08:00:00Z",
    "durationSeconds": 620,
    "viewCount": 152000,
    "tags": ["AI", "Education", "Self-Hosted"],
    "description": "Comprehensive tutorial on building multi-agent architectures.",
    "subtitles_indexed": True
}

meta = VideoMetadata.model_validate(raw_meta)
print(f"Validated Video Metadata: {meta.title} by {meta.channel_name}")
```

## Diagnostic Troubleshooting Matrix

| Symptom / Error | Potential Root Cause | Verification Command | Resolution Step |
| :--- | :--- | :--- | :--- |
| `HTTP 403 Forbidden` on video download | YouTube bot detection or outdated `yt-dlp` binary | `docker exec tubearchivist yt-dlp --version` | Upgrade `yt-dlp` in container (`pip install -U yt-dlp`) or configure PO Token / cookies in TA setting. |
| Elasticsearch Connection Error (`ES_URL`) | ES container starting slower than TA Django app | `docker logs archivist-es` | Ensure `depends_on` healthcheck condition in `docker-compose.yml` or restart `tubearchivist` container. |
| Redis queue stalled / tasks stuck | Redis container memory limit exceeded or worker hang | `docker exec archivist-redis redis-cli ping` | Flush stale keys or increase Redis memory budget in compose limits. |
| Disk space full (`/youtube` volume) | High video resolution downloads filling storage | `df -h /mnt/media/youtube` | Set maximum resolution limit in Tube Archivist settings or add external storage volume. |
| Deno extraction engine failure | Missing Deno runtime executable or cookie read failure | `docker exec tubearchivist deno --version` | Verify Deno install inside image and ensure cookie file permissions match `HOST_UID`. |
| Subtitle indexing failure in Elasticsearch | Corrupt VTT formatting or ES heap memory exhaustion | `docker logs archivist-es \| grep -i oom` | Increase `ES_JAVA_OPTS` heap allocation from 512m to 2048m. |
| Channel rescan skipping new uploads | Channel RSS feed caching or rate limit throttle | `docker exec tubearchivist python manage.py rescan --force` | Force manual rescan CLI invocation and clear channel cache timestamp. |
| Pydantic schema validation error on MCP tool | Invalid YouTube URL structure or extra fields passed | Inspect FastMCP client logs | Ensure caller passes canonical YouTube link with `ConfigDict(extra="forbid", frozen=True)`. |

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
