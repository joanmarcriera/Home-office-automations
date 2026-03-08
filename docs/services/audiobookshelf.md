# Audiobookshelf

Audiobookshelf is a self-hosted audiobook and podcast server.

## Description
It allows you to organize and stream your audiobook and podcast collection. It features multi-user support, progress syncing across devices, and a robust web interface along with mobile apps.

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

## API examples
Audiobookshelf provides a REST API for management and streaming:

```bash
# Get all libraries
curl -X GET "http://localhost:1337/api/libraries" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

## Links
- [Official Website](https://www.audiobookshelf.org/)
- [GitHub Repository](https://github.com/advplyr/audiobookshelf)

## Alternatives
- [Plex (with Prologue)](https://www.plex.tv/)
- [Jellyfin](jellyfin.md)

## Backlog
- Integrate with Kavita for ebook/manga support.
- Explore AI-based transcription for hosted podcasts.

## Sources / References
- https://www.audiobookshelf.org/
- https://github.com/advplyr/audiobookshelf
- https://www.plex.tv/
- [Official Website](https://www.audiobookshelf.org/)
- [GitHub Repository](https://github.com/advplyr/audiobookshelf)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-08
