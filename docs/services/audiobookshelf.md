# Audiobookshelf

Audiobookshelf is a self-hosted audiobook and podcast server.

## What it is
Audiobookshelf is a specialized media server designed specifically for the unique needs of spoken-word audio. Unlike general media servers like [Plex](plex.md) or [Jellyfin](jellyfin.md), it prioritizes chapter management, narrator metadata, and progress tracking for long-form audio. As of July 2026, it supports automated narration analysis and semantic indexing via **MCP 3.0**, allowing agents like **Gemma 3** and **Claude 4.8** to query library content and generate summaries.

## What problem it solves
It solves the poor experience of managing audiobooks in music-centric applications. It handles multi-file books, detects chapters automatically from metadata or file structures, and provides a dedicated mobile interface for offline listening without losing your place.

## Where it fits in the stack
In a homelab, Audiobookshelf serves as the **Spoken Word Media Hub**. It sits alongside tools like [Plex](plex.md) (video) and [Navidrome](navidrome.md) (music) to provide a complete self-hosted media ecosystem. It can be integrated with [Agentic Workflows](../knowledge_base/patterns/agentic-workflows.md) via its **MCP 3.0** server to automate metadata cleanup and transcript generation.

## Typical use cases
- **Personal Audiobook Library**: Hosting and streaming owned DRM-free audiobook collections.
- **Private Podcast Aggregator**: Downloading and serving podcast feeds for private consumption.
- **Bedtime Stories**: Setting up a child-friendly interface for audio stories with controlled access.
- **AI-Enhanced Transcripts**: Using local [Whisper](whisper.md) instances to generate searchable transcripts for podcasts and books.
- **Semantic Library Search**: Querying your collection via [Claude 4.8](../tools/providers/anthropic.md) to find "books about stoicism narrated by a British voice."

## Strengths
- **Native Mobile Apps**: Excellent Android and iOS apps with full offline support and CarPlay/Android Auto integration.
- **Robust Metadata**: Fetches data from Audible, Open Library, Google Books, and specialized narrator databases.
- **Multi-User Support**: Separate progress tracking for every family member with automatic token refresh.
- **MCP 3.0 Support**: Native integration for autonomous agent library management and querying.
- **Chapter Discovery**: Automatically detects chapters even in single-file audiobooks using silence detection and metadata.

## Limitations
- **Narrow Focus**: Not suitable for general music collections (use [Navidrome](navidrome.md)) or video.
- **Metadata Quality**: Highly dependent on the quality of external sources for older or obscure titles.
- **Transcoding Overhead**: High-quality transcoding for mobile devices can be CPU-intensive on older hardware.

## When to use it
- When you want a dedicated, high-quality experience for audiobooks that general media servers do not provide.
- When you want to host your own private podcast feeds and manage their storage.
- When you need reliable offline listening with dedicated mobile applications for commuting or travel.
- To integrate your spoken-word library into [Knowledge Management](../knowledge_base/README.md) patterns.

## When not to use it
- When you only have a few audiobooks and already use [Jellyfin](jellyfin.md) for everything else.
- When you strictly use commercial services like Audible and do not own your audio files.
- For high-fidelity music streaming, where [Navidrome](navidrome.md) is the superior choice.

## Getting started

### Docker Compose
The recommended way to run Audiobookshelf (v2.15.0+, July 2026) for persistent configuration and easy updates:

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
    environment:
      - AUDIOBOOKSHELF_UID=1000
      - AUDIOBOOKSHELF_GID=1000
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
Audiobookshelf provides a REST API and an **MCP 3.0** server for management and streaming:

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
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Standard for agentic library orchestration.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — For running Gemma 3 for library analysis.
- [Claude 4.8](../tools/providers/anthropic.md) — Frontier model for high-fidelity narration summaries.

## Sources / references
- [Audiobookshelf Official Site](https://www.audiobookshelf.org/)
- [GitHub Repository](https://github.com/advplyr/audiobookshelf)
- [Audiobookshelf MCP Server GitHub](https://github.com/advplyr/mcp-server-audiobookshelf)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
