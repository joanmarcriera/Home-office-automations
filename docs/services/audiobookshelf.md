# Audiobookshelf

Audiobookshelf is a self-hosted audiobook and podcast server.

## What it is
Audiobookshelf is a specialized media server designed specifically for the unique needs of spoken-word audio. Unlike general media servers like [Plex](plex.md) or [Jellyfin](jellyfin.md), it prioritizes chapter management, narrator metadata, and progress tracking for long-form audio. As of June 2026, it supports automated narration analysis using **Claude 4.8 Opus** to generate rich summaries and chapter markers.

## What problem it solves
It solves the poor experience of managing audiobooks in music-centric applications. It handles multi-file books, detects chapters automatically from metadata or file structures, and provides a dedicated mobile interface for offline listening without losing your place in a 40-hour narration.

## Where it fits in the stack
In a homelab, Audiobookshelf serves as the **Spoken Word Media Hub**. It sits alongside tools like [Plex](plex.md) (video) and [Navidrome](navidrome.md) (music) to provide a complete self-hosted media ecosystem. It can be integrated with automation tools like [n8n](n8n.md) to ingest new downloads or notify users of new podcast episodes.

## Typical use cases
- **Personal Audiobook Library**: Hosting and streaming owned DRM-free audiobook collections.
- **Private Podcast Aggregator**: Downloading and serving podcast feeds for private consumption.
- **Bedtime Stories**: Setting up a child-friendly interface for audio stories with controlled access.
- **AI-Enhanced Transcripts**: Using local [Whisper](whisper.md) instances to generate searchable transcripts for podcasts and books.

## Strengths
- **Native Mobile Apps**: Excellent Android and iOS apps with full offline support.
- **Robust Metadata**: Fetches data from Audible, Open Library, and Google Books.
- **Multi-User Support**: Separate progress tracking for every family member with automatic token refresh.
- **Ebook Support**: Basic reader functionality for ebooks, making it a versatile digital library hub.
- **Chapter Discovery**: Automatically detects chapters even in single-file audiobooks using silence detection and metadata.

## Limitations
- **Narrow Focus**: Not suitable for general music collections (use [Navidrome](navidrome.md)) or video.
- **Metadata Quality**: Highly dependent on the quality of external sources for older or obscure titles.
- **Transcoding Overhead**: High-quality transcoding for mobile devices can be CPU-intensive on older hardware.

## When to use it
- When you want a dedicated, high-quality experience for audiobooks that general media servers do not provide.
- When you want to host your own private podcast feeds and manage their storage.
- When you need reliable offline listening with dedicated mobile applications for commuting or travel.

## When not to use it
- When you only have a few audiobooks and already use [Jellyfin](jellyfin.md) for everything else.
- When you strictly use commercial services like Audible and do not own your audio files.
- For high-fidelity music streaming, where [Navidrome](navidrome.md) is the superior choice.

## Getting started

### Docker Compose
The recommended way to run Audiobookshelf for persistent configuration and easy updates:

```yaml
services:
  audiobookshelf:
    container_name: audiobookshelf
    image: ghcr.io/advplyr/audiobookshelf:latest
    ports:
      - 1337:80
    volumes:
      - /path/to/audiobooks:/audiobooks
      - /path/to/podcasts:/podcasts
      - /path/to/config:/config
      - /path/to/metadata:/metadata
    restart: unless-stopped
```

Access the web interface at `http://localhost:1337`.

## CLI examples
Management is mostly web-based, but you can interact with the container for maintenance:

```bash
# View server logs
docker logs audiobookshelf

# List files in the audiobooks directory
docker exec audiobookshelf ls /audiobooks

# Restart the service
docker restart audiobookshelf
```

## API examples
Audiobookshelf provides a REST API for management and streaming:

```bash
# Get all libraries (requires Bearer Token)
curl -X GET "http://localhost:1337/api/libraries" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

## Related tools / concepts
- [Jellyfin](jellyfin.md) — Open-source media server for video and photos.
- [Plex](plex.md) — Popular media server alternative.
- [Navidrome](navidrome.md) — Dedicated server for music streaming.
- [n8n](n8n.md) — For automating media ingestion and notifications.
- [Whisper](whisper.md) — For local AI transcription of audio files.
- [Authentik](authentik.md) — For managing multi-user SSO access.
- [Nextcloud](nextcloud.md) — For file storage and cloud-based library backups.

## Advanced Integrations

### Kavita (Ebooks & Manga)
While Audiobookshelf specializes in audio, it can be paired with [Kavita](https://www.kavitareader.com/) for a complete digital library.

1.  **Shared Storage**: Point both services to the same root media directory.
2.  **OPDS Feed**: Use Audiobookshelf's OPDS feed to browse your collection in external readers that support the standard.
3.  **Authentication**: Pair both services with [Authentik](authentik.md) for unified access.

### AI Podcast Transcription
Enrich your podcast library with full-text search by integrating [Whisper](whisper.md) for local transcription.

```bash
# Example: Using faster-whisper-server (Speaches) to transcribe a podcast episode
curl http://speaches:8000/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F file="@/podcasts/my_episode.mp3" \
  -F model="base"
```

The resulting JSON transcript can be indexed in a local vector database for semantic search across your entire spoken-word history.

## Sources / references
- [Audiobookshelf Official Site](https://www.audiobookshelf.org/)
- [GitHub Repository](https://github.com/advplyr/audiobookshelf)
- [Audiobookshelf API Documentation](https://api.audiobookshelf.org/)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
