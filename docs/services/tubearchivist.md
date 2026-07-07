# Tube Archivist

Tube Archivist is a self-hosted YouTube archive that allows you to index and download YouTube videos, metadata, and comments to your own server.

## What it is
Tube Archivist is an open-source media management system designed specifically for preserving YouTube content. As of **July 2026**, it features a robust integration with the **Deno** runtime for enhanced download reliability and provides advanced tools for metadata persistence and elasticsearch-based searching. It is a critical tool for digital sovereignty in the era of platform-driven content volatility.

## What problem it solves
YouTube videos can be deleted, made private, or censored without notice. Tube Archivist provides a way to build a permanent, offline, and searchable library of your favorite content, ensuring long-term access to tutorials, documentaries, and educational material while eliminating dependency on third-party platform availability and advertising.

## Where it fits in the stack
It serves as a **content preservation layer** within the media management stack. It sits alongside general-purpose media servers like [Jellyfin](jellyfin.md) or [Plex](plex.md), but provides deep specialization for YouTube-specific metadata (comments, descriptions, subtitles) and automated channel monitoring for agentic workflows.

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
- **Agentic Ready**: Robust API for integration with tools like **Gemma 3** for content analysis.

## Limitations
- **Storage Intensive**: Storing high-resolution video archives can consume terabytes of storage rapidly.
- **Resource Usage**: Requires secondary containers for Redis and Elasticsearch, which can be memory-intensive.
- **Maintenance**: Ongoing site layout changes on YouTube require frequent `yt-dlp` updates within the container.

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
services:
  tubearchivist:
    container_name: tubearchivist
    image: bbilly1/tubearchivist:latest
    ports:
      - 8000:8000
    volumes:
      - /path/to/media:/youtube
      - /path/to/cache:/cache
    environment:
      - ES_URL=http://archivist-es:9200
      - REDIS_HOST=archivist-redis
      - HOST_UID=1000
      - HOST_GID=1000
      - TA_USERNAME=admin
      - TA_PASSWORD=password
    depends_on:
      - archivist-es
      - archivist-redis

  archivist-redis:
    image: redis/redis-stack-server:latest

  archivist-es:
    image: bbilly1/tubearchivist-es:latest
    environment:
      - "ELASTIC_PASSWORD=verysecret"
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "discovery.type=single-node"
    volumes:
      - /path/to/es:/usr/share/elasticsearch/data
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
The REST API allows for integration with AI agents (e.g., **Gemma 3** or **Claude 4.8**).

### Python (List Archived Videos)
```python
import requests

TA_URL = "http://localhost:8000/api"
HEADERS = {"Authorization": "Token YOUR_API_TOKEN"}

response = requests.get(f"{TA_URL}/video/", headers=HEADERS)
for video in response.json()['results']:
    print(f"Archived: {video['title']} by {video['channel_name']}")
```

### Curl (Trigger a Download)
```bash
curl -X POST -H "Authorization: Token <your_api_token>" \
     -d "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
     "http://localhost:8000/api/download/"
```

## Related tools / concepts
- [Plex](plex.md) — For streaming your YouTube archive to smart TVs and mobile devices.
- [Jellyfin](jellyfin.md) — The recommended open-source alternative for media streaming.
- [Audiobookshelf](audiobookshelf.md) — For managing audio-only YouTube archives or podcasts.
- [Changedetection.io](changedetection.md) — To monitor YouTube channels for visual or metadata changes.
- [n8n](n8n.md) — For advanced automation (e.g., notifying you in Element when a video is archived).
- [SearXNG](searXNG.md) — For private searching before adding videos to the archive.
- [Home Assistant](home-assistant.md) — For dashboard integration and download notifications.
- [Tailscale](tailscale.md) — For secure remote access to your video library.
- [Gemma 3](../knowledge_base/models/gemma-3.md) — For automated content analysis and metadata enrichment.
- [PO Token Management](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp) — For mitigating 403 errors during download.

## Sources / References
- [Official Website](https://www.tubearchivist.com/)
- [Tube Archivist Documentation](https://docs.tubearchivist.com/)
- [GitHub Repository](https://github.com/tubearchivist/tubearchivist)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-21
