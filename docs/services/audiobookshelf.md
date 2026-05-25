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
- **Native Mobile Apps**: Excellent Android and iOS (beta) apps with offline support.
- **Robust Metadata**: Fetches data from Audible, Open Library, and Google Books.
- **Multi-User Support**: Separate progress tracking for every family member.
- **Live Transcriptions**: Experimental support for transcribing podcasts.

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

### Docker
To run Audiobookshelf using Docker:

```bash
docker run -d \
  --name audiobookshelf \
  --publish 1337:80 \
  -v /path/to/audiobooks:/audiobooks \
  -v /path/to/podcasts:/podcasts \
  -v /path/to/config:/config \
  -v /path/to/metadata:/metadata \
  --restart unless-stopped \
  ghcr.io/advplyr/audiobookshelf:latest
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
- [ ] Perform quarterly technical freshness audit.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-13

## Sources / References
- [Audiobookshelf Official Site](https://www.audiobookshelf.org/)
- [GitHub Repository](https://github.com/advplyr/audiobookshelf)
- [Plex Official Site](https://www.plex.tv/)
