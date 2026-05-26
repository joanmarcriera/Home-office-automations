# Audiobookshelf

Audiobookshelf is a self-hosted audiobook and podcast server.

## What it is
Audiobookshelf is a specialized media server designed specifically for the unique needs of spoken-word audio. Unlike general media servers like Plex or Jellyfin, it prioritizes chapter management, narrator metadata, and progress tracking for long-form audio.

## What problem it solves
It solves the poor experience of managing audiobooks in music-centric applications. It handles multi-file books, detects chapters automatically from metadata or file structures, and provides a dedicated mobile interface for offline listening without losing your place in a 40-hour narration.

## Where it fits in the stack
In a homelab, Audiobookshelf serves as the **Spoken Word Media Hub**. It sits alongside tools like Plex (video) and Navidrome (music) to provide a complete self-hosted media ecosystem. It can be integrated with automation tools to ingest new downloads or notify users of new podcast episodes.

## Typical use cases
- **Personal Audiobook Library**: Hosting and streaming owned DRM-free audiobook collections.
- **Private Podcast Aggregator**: Downloading and serving podcast feeds for private consumption.
- **Bedtime Stories**: Setting up a child-friendly interface for audio stories with controlled access.

## Strengths
- **Native Mobile Apps**: Excellent Android and iOS apps with offline support. New 2026 clients like "Still" offer polished, minimalist interfaces.
- **Robust Metadata**: Fetches data from Audible, Open Library, and Google Books.
- **Multi-User Support**: Separate progress tracking for every family member with automatic token refresh (v2.26.0+).
- **Universal Search**: Improved search results include episodes for podcast libraries and better ebook indexing.

## Limitations
- **Narrow Focus**: Not suitable for music or video collections.
- **Beta Software**: Some features and the iOS app are still in active development.
- **Metadata Quality**: Highly dependent on the quality of external sources for older or obscure titles.

## When to use it
- When you want a dedicated, high-quality experience for audiobooks that Plex or Jellyfin might not fully support (e.g., proper chapter support, narrator metadata).
- When you want to host your own private podcast feeds.
- When you need offline listening with a dedicated mobile application.

## When not to use it
- When you only have a few audiobooks and already use Plex or Jellyfin for everything else.
- When you strictly use commercial services like Audible and don't own your audio files.

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
Management is mostly web-based, but you can interact with the container:

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
# Get all libraries
curl -X GET "http://localhost:1337/api/libraries" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

## Related tools / concepts
- [Jellyfin](jellyfin.md)
- [Plex](plex.md)
- [Navidrome](navidrome.md)
- [n8n](n8n.md)
- [Whisper](whisper.md)

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

The resulting JSON transcript can be indexed in a local [Vector DB](../knowledge_base/vector-db-comparison.md) for semantic search across your entire spoken-word history.

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-26

## Sources / References
- [Audiobookshelf Official Site](https://www.audiobookshelf.org/)
- [GitHub Repository](https://github.com/advplyr/audiobookshelf)
- [v2.26.0 Release Notes](https://github.com/advplyr/audiobookshelf/releases)
