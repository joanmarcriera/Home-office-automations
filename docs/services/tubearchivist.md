# Tube Archivist

## What it is
Tube Archivist is a self-hosted YouTube archive that allows you to index and download YouTube videos, metadata, and comments to your own server.

## What problem it solves
YouTube videos can be deleted, made private, or censored at any time. Tube Archivist provides a way to build a permanent, offline, and searchable library of your favorite YouTube content, ensuring you always have access to the information and entertainment you value.

## Where it fits in the stack
**Category**: Services / Media Management. It serves as a **content preservation layer**, sitting alongside tools like Plex or Jellyfin but specialized for YouTube content and metadata.

## Typical use cases
- Archiving educational channels or tutorials for offline reference.
- Saving high-quality versions of favorite music videos or documentaries.
- Building a private "YouTube" experience without ads or tracking.
- Keeping a record of comments and metadata for research purposes.

## Strengths
- **Comprehensive Metadata**: Downloads thumbnails, descriptions, comments, and subtitles.
- **Powerful Search**: Features an integrated Elasticsearch-based search engine for finding content within your archive.
- **Automation**: Can be configured to automatically monitor and download new videos from specific channels or playlists.
- **Self-Hosted**: Full control over your data and hardware.

## Limitations
- **Storage Intensive**: High-quality video archives can consume terabytes of storage quickly.
- **Resource Usage**: Requires a secondary Redis and Elasticsearch/OpenSearch container, which can be memory-intensive.
- **Maintenance**: Upstream changes to YouTube's API or site layout may occasionally break the downloaders (requiring `yt-dlp` updates).

## When to use it
- When you want to ensure permanent access to specific YouTube content.
- When you want to watch YouTube content without an internet connection.
- When you need to search across video descriptions and comments at scale.

## When not to use it
- If you only need to download an occasional video (use a simple CLI tool like `yt-dlp`).
- If you have very limited server resources (RAM/CPU/Storage).
- If you prefer a lightweight, single-binary solution without the complexity of multiple containers.

## Getting started

### Installation (Docker Compose)
Tube Archivist requires a few companion services (Redis and Elasticsearch).

```yaml
services:
  tubearchivist:
    container_name: tubearchivist
    restart: always
    image: bbilly1/tubearchivist
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
    image: redis/redis-stack-server
    restart: always

  archivist-es:
    image: bbilly1/tubearchivist-es
    restart: always
    environment:
      - "ELASTIC_PASSWORD=verysecret"
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "xpack.security.enabled=true"
      - "discovery.type=single-node"
      - "path.repo=/usr/share/elasticsearch/data/snapshot"
    volumes:
      - /path/to/es:/usr/share/elasticsearch/data
```

### Hello World
1. Start the Docker Compose stack.
2. Navigate to `http://localhost:8000`.
3. Log in with the credentials defined in your environment variables.
4. Go to **Downloads**, paste a YouTube URL, and click **Index and Download**.

## CLI examples

Tube Archivist is primarily managed via the web UI, but you can interact with the container for maintenance.

```bash
# Force an immediate rescan of the media directory
docker exec tubearchivist python manage.py rescan

# Manually update yt-dlp within the container
docker exec tubearchivist pip install -U yt-dlp

# Check the status of the background task worker
docker exec tubearchivist python manage.py check_worker
```

## API examples

### Python (Get all videos)
Tube Archivist provides a REST API. You can find your API key in the web UI settings.

```python
import requests

TA_URL = "http://localhost:8000/api"
HEADERS = {"Authorization": "Token YOUR_API_TOKEN"}

response = requests.get(f"{TA_URL}/video/", headers=HEADERS)
videos = response.json()

for video in videos['results']:
    print(f"Title: {video['title']}, Channel: {video['channel_name']}")
```

### Curl (Trigger a download)
```bash
curl -X POST -H "Authorization: Token <your_api_token>" \
     -d "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
     "http://localhost:8000/api/download/"
```

## Related tools / concepts
- [Plex](plex.md) — for streaming your archived content to TV/Mobile
- [Jellyfin](jellyfin.md) — an open-source alternative to Plex
- [Audiobookshelf](audiobookshelf.md) — for managing YouTube podcasts or audio-only archives
- [Changedetection.io](changedetection.md) — to monitor YouTube channels for changes
- [SearXNG](searXNG.md) — to search for YouTube content privately before archiving
- [n8n](n8n.md) — for advanced automation of video ingestion

## Backlog
- Configure automated downloads for subscribed channels.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://www.tubearchivist.com/
- https://docs.tubearchivist.com/
- https://github.com/tubearchivist/tubearchivist
- https://github.com/yt-dlp/yt-dlp
