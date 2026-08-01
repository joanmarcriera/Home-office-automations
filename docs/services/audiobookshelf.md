# Audiobookshelf

Audiobookshelf is a self-hosted audiobook and podcast server.

## What it is
Audiobookshelf is a specialized media server designed specifically for the unique needs of spoken-word audio. Unlike general media servers like [Plex](plex.md) or [Jellyfin](jellyfin.md), it prioritizes chapter management, narrator metadata, and progress tracking for long-form audio. As of late October / November 2026, it supports automated narration analysis and semantic indexing via **MCP 3.1 / FastMCP**, allowing agents like **Gemma 3**, **Qwen 3.6**, and **Claude 5.1** to query library content and generate summaries.

## What problem it solves
It solves the poor experience of managing audiobooks in music-centric applications. It handles multi-file books, detects chapters automatically from metadata or file structures, and provides a dedicated mobile interface for offline listening without losing your place.

## Where it fits in the stack
In a homelab, Audiobookshelf serves as the **Spoken Word Media Hub**. It sits alongside tools like [Plex](plex.md) (video) and [Navidrome](navidrome.md) (music) to provide a complete self-hosted media ecosystem. It can be integrated with [Agentic Workflows](../knowledge_base/patterns/agentic-workflows.md) via its **MCP 3.1** server to automate metadata cleanup and transcript generation.

## Typical use cases
- **Personal Audiobook Library**: Hosting and streaming owned DRM-free audiobook collections.
- **Private Podcast Aggregator**: Downloading and serving podcast feeds for private consumption.
- **Bedtime Stories**: Setting up a child-friendly interface for audio stories with controlled access.
- **AI-Enhanced Transcripts**: Using local [Whisper](whisper.md) instances to generate searchable transcripts for podcasts and books.
- **Semantic Library Search**: Querying your collection via [Claude 5.1](../tools/providers/anthropic.md) to find "books about stoicism narrated by a British voice."

## Strengths
- **Native Mobile Apps**: Excellent Android and iOS apps with full offline support and CarPlay/Android Auto integration.
- **Robust Metadata**: Fetches data from Audible, Open Library, Google Books, and specialized narrator databases.
- **Multi-User Support**: Separate progress tracking for every family member with automatic token refresh.
- **MCP 3.1 / FastMCP Support**: Native integration for autonomous agent library management, playlist creation, and structured querying.
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
The recommended way to run Audiobookshelf (v2.16.0+, late October / November 2026) for persistent configuration and easy updates:

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
Audiobookshelf provides a REST API and an **MCP 3.1** server for management and streaming:

```bash
# Get all libraries (requires Bearer Token)
curl -X GET "http://localhost:1337/api/libraries" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

### Python API with Pydantic Validation
Here is a Python example utilizing **Pydantic v2** to model, parse, and validate audiobook metadata payloads retrieved from the Audiobookshelf REST API or via MCP tool definitions:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class AudiobookMetadataModel(BaseModel):
    """
    Pydantic v2 model representing Audiobook shelf library item metadata
    synchronized or updated via API/MCP.
    """
    id: str = Field(..., description="Unique audiobook library item ID")
    title: str = Field(..., min_length=1, description="Title of the book")
    author: str = Field(..., description="Author of the book")
    narrator: Optional[str] = Field(None, description="Narrator(s) of the audiobook")
    duration: float = Field(..., description="Total play duration in seconds")
    genres: List[str] = Field(default_factory=list, description="Associated genres")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Listening progress ratio (0.0 to 1.0)")

# Example API payload validation
raw_data = {
    "id": "book_09876",
    "title": "Meditations",
    "author": "Marcus Aurelius",
    "narrator": "Richard Armitage",
    "duration": 18230.5,
    "genres": ["Philosophy", "Stoicism", "Classics"],
    "progress": 0.45
}

audiobook = AudiobookMetadataModel.model_validate(raw_data)
print(f"Validated Audiobook: '{audiobook.title}' by {audiobook.author} (Narrator: {audiobook.narrator})")
print(f"Progress: {audiobook.progress * 100:.1f}% complete ({audiobook.duration * audiobook.progress:.1f}s listened)")
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
- [Claude 5.1](../tools/providers/anthropic.md) — Frontier model for high-fidelity narration summaries.

## Sources / references
- [Audiobookshelf Official Site](https://www.audiobookshelf.org/)
- [GitHub Repository](https://github.com/advplyr/audiobookshelf)
- [Audiobookshelf MCP Server GitHub](https://github.com/advplyr/mcp-server-audiobookshelf)

## Contribution Metadata
- Last reviewed: 2026-11-06
- Confidence: high
