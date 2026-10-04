# Audiobookshelf

Audiobookshelf is a self-hosted, open-source media server specifically designed for managing, organizing, and streaming audiobooks, podcasts, and long-form spoken-word content.

## What it is
Audiobookshelf is a specialized media streaming platform optimized for spoken-word audio structures. Unlike general-purpose music and video servers such as [Plex](plex.md) or [Jellyfin](jellyfin.md), Audiobookshelf prioritizes single-file and multi-file book layouts, chapter markers, author and narrator metadata, bookmark synchronization, and precise listening position retention across multiple clients and users.

As of 2027, Audiobookshelf features native **FastMCP 3.1** and **Model Context Protocol (MCP)** integration. This enables AI agent runtimes (such as **Claude 5.1**, **GPT-5.5**, **Gemma 3**, and **Qwen 3.8**) to query library catalog metadata, inspect chapter structures, manage playlists, trigger automated transcriptions via local [Whisper](whisper.md) pipelines, and sync bookmarks programmatically.

## What problem it solves
Managing spoken-word audio in general music or video media players presents severe usability hurdles:
- **Position Loss & Lack of Cross-Device Sync**: Music players frequently lose track of hours-long playback positions when switching between desktop and mobile devices.
- **Poor Metadata Organization**: Music tags (album, artist, track number) fail to accommodate author, narrator, series order, publisher, and unabridged status.
- **Inadequate Chapter Support**: Long single-file audiobooks or multi-part MP3/M4B releases require robust embedded metadata parsing and silence-detection chapter generators.
- **Missing Podcast Management**: Audiobookshelf unifies personal DRM-free audiobook libraries with auto-downloading private podcast feeds in a single web and mobile interface.

Audiobookshelf solves these challenges by implementing dedicated data schemas for books and podcasts, multi-user progress tracking, and open REST and MCP interfaces.

## System Architecture

```
                                  Audiobookshelf Ecosystem & MCP Architecture

  +-----------------------+        +-----------------------------------+        +-----------------------------------+
  | Web UI & Mobile Apps  | ---->  | Audiobookshelf Core Server        | ---->  | Audio Storage & Libraries         |
  | - iOS / Android Apps  |        | - Node.js Express REST Engine     |        | - /audiobooks                     |
  | - CarPlay / Auto      |        | - SQLite Metadata Database        |        | - /podcasts                       |
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
                                                     ^                                            ^
                                                     |                                            |
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
  | AI Agents & LLMs      | ---->  | FastMCP 3.1 Audiobookshelf Bridge | ---->  | Whisper Transcription Service     |
  | - Claude 5.1 / GPT-5.5|        | - JSON-RPC / SSE MCP Protocol     |        | - Local Speech-to-Text Pipeline   |
  | - Natural Querying    |        | - Pydantic v2 Validated API Calls |        | - Chapter & Semantic Search       |
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
```

## Where it fits in the stack
Within a self-hosted homelab or enterprise knowledge architecture, Audiobookshelf functions as the **Spoken Word & Audio Knowledge Server**:
1. **Media Layer**: Sits alongside [Navidrome](navidrome.md) (music) and [Jellyfin](jellyfin.md) (video) as the specialized hub for narrative audio.
2. **Knowledge Base Ingestion**: Connects with [Knowledge Management](../knowledge_base/README.md) patterns and [n8n](n8n.md) workflows to ingest speech-to-text transcripts into vector databases (e.g., [Qdrant](../tools/infrastructure/qdrant.md)).
3. **Agentic Tooling Integration**: Serves as an MCP resource provider, allowing conversational agents to inspect reading histories and recommend books based on user preferences.

## Typical use cases
- **Personal DRM-Free Library Streaming**: Hosting, organizing, and streaming personal M4B, MP3, FLAC, and AAC audiobook collections.
- **Cross-Device Listening**: Seamlessly resuming playback across web browsers, Android, iOS, Android Auto, and Apple CarPlay.
- **Private Podcast Aggregation**: Subscribing to public or authenticated podcast RSS feeds with automatic background episode downloads.
- **Automated AI Summarization & Search**: Using local [Whisper](whisper.md) instances to generate timestamps, chapter transcripts, and searchable text for long-form lectures and podcasts.
- **Multi-User Family Sharing**: Providing individual accounts with custom permissions, listening stats, and isolated progress state for household members.

## Strengths
- **Purpose-Built UI/UX**: Interfaces tailored specifically for audiobooks, featuring speed control, sleep timers, volume boost, and chapter selection.
- **Rich Metadata Matching**: Automated metadata retrieval from Audible, Google Books, Open Library, iTunes, and Discogs.
- **Native FastMCP 3.1 Integration**: Direct support for agentic querying, tool invocation, and automated library maintenance via Model Context Protocol.
- **Offline Download & Sync**: Mobile applications allow full offline library sync with automatic background progress updates once reconnected.
- **Folder and Embedded Tag Parsing**: Capable of inferring series, authors, and chapters from folder hierarchies or ID3/M4B embedded tags.

## Limitations
- **Not Suited for Music**: Lacks music-centric features like album artist grouping, lyrics support, dynamic playlists by BPM, or last.fm scrobbling (use [Navidrome](navidrome.md)).
- **Transcoding CPU Overhead**: On-the-fly audio transcoding for low-bandwidth mobile connections can require significant CPU resources if hardware acceleration is unavailable.
- **E-Book Viewer Limitations**: While basic EPUB/PDF reading is supported, it is primarily an audio platform rather than a dedicated e-reader server like Calibre-Web.

## When to use it
- When you possess an owned collection of DRM-free audiobooks or lecture series and want a polished, sync-enabled streaming experience.
- When you want to combine audiobook streaming with custom, auto-downloaded podcast feeds.
- When building AI workflow pipelines that require querying audio transcripts, chapters, and listening habits via MCP 3.1.
- When requiring multi-user access with isolated listening statistics and progress boundaries.

## When not to use it
- When managing high-fidelity music collections (use [Navidrome](navidrome.md)).
- When seeking a video streaming or full-featured home theater solution (use [Jellyfin](jellyfin.md) or [Plex](plex.md)).
- When exclusively reading static EPUB or PDF e-books without audio components (use Calibre-Web or Kavita).

## Getting started

### Docker Compose Setup
Deploy Audiobookshelf using Docker Compose for simple persistence, configuration, and upgrades:

```yaml
version: "3.8"

services:
  audiobookshelf:
    container_name: audiobookshelf
    image: ghcr.io/advplyr/audiobookshelf:latest
    ports:
      - "1337:80"
    volumes:
      - /srv/audiobookshelf/audiobooks:/audiobooks
      - /srv/audiobookshelf/podcasts:/podcasts
      - /srv/audiobookshelf/config:/config
      - /srv/audiobookshelf/metadata:/metadata
    environment:
      - AUDIOBOOKSHELF_UID=1000
      - AUDIOBOOKSHELF_GID=1000
      - TZ=America/New_York
    restart: unless-stopped
```

After launching the service (`docker compose up -d`), navigate to `http://localhost:1337` to create the initial administrator account and register media root paths.

## CLI examples

### 1. Checking Container Logs and Health
Inspect server startup routines and library scanner execution:

```bash
# View real-time container logs
docker logs -f audiobookshelf

# Execute internal SQLite maintenance
docker exec -it audiobookshelf sqlite3 /config/abs.sqlite "PRAGMA integrity_check;"
```

### 2. Manual Trigger of Library Rescan via Curl
Trigger an automated library rescan via the REST API:

```bash
curl -X POST "http://localhost:1337/api/libraries/lib_audiobooks_01/scan" \
  -H "Authorization: Bearer <YOUR_ABS_API_TOKEN>" \
  -H "Content-Type: application/json"
```

### 3. Backup Server Configuration and Database
Create a compressed archive of server settings and user progress state:

```bash
docker exec audiobookshelf tar -czf /metadata/abs_backup_$(date +%Y%m%d).tar.gz /config /metadata
```

## API examples

### 1. FastMCP 3.1 Server Integration for Audiobookshelf
The following complete Python application uses **FastMCP 3.1** and **Pydantic v2** to create an MCP microservice that allows AI agents to inspect libraries, query items, and update listening positions:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
import requests
import os
from typing import List, Optional

mcp = FastMCP("Audiobookshelf-Agent-Bridge")

ABS_BASE_URL = os.getenv("ABS_BASE_URL", "http://localhost:1337")
ABS_API_TOKEN = os.getenv("ABS_API_TOKEN", "your_secret_bearer_token")

HEADERS = {
    "Authorization": f"Bearer {ABS_API_TOKEN}",
    "Content-Type": "application/json"
}

class ChapterSchema(BaseModel):
    id: int
    start: float
    end: float
    title: str

class LibraryItemSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Audiobookshelf unique item identifier")
    title: str = Field(..., description="Book title")
    author: Optional[str] = Field("Unknown", description="Author name")
    duration: float = Field(..., description="Total length in seconds")
    progress: float = Field(default=0.0, description="Listening completion ratio (0.0 to 1.0)")
    chapters: List[ChapterSchema] = Field(default_factory=list)

class UpdateProgressRequest(BaseModel):
    item_id: str = Field(..., description="Library item ID")
    current_time_seconds: float = Field(..., description="Current playback position in seconds")
    duration_seconds: float = Field(..., description="Total book duration in seconds")

@mcp.tool()
def search_audiobook_catalog(query: str) -> str:
    """Search the Audiobookshelf library catalog by title or author."""
    url = f"{ABS_BASE_URL}/api/libraries/lib_audiobooks_01/items?q={query}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return f"Error querying catalog: {resp.status_code} - {resp.text}"

    data = resp.json().get("results", [])
    parsed_items = []
    for raw in data:
        media = raw.get("media", {})
        metadata = media.get("metadata", {})
        parsed_items.append(
            LibraryItemSchema(
                id=raw.get("id"),
                title=metadata.get("title", "Untitled"),
                author=metadata.get("authorName", "Unknown"),
                duration=media.get("duration", 0.0),
                progress=raw.get("userProgress", {}).get("progress", 0.0),
                chapters=[
                    ChapterSchema(
                        id=c.get("id", 0),
                        start=c.get("start", 0.0),
                        end=c.get("end", 0.0),
                        title=c.get("title", f"Chapter {idx}")
                    ) for idx, c in enumerate(media.get("chapters", []))
                ]
            )
        )
    return f"Found {len(parsed_items)} items:\n" + "\n".join([i.model_dump_json() for i in parsed_items])

@mcp.tool()
def update_listening_progress(req: UpdateProgressRequest) -> str:
    """Update listening progress for a specific library item via FastMCP 3.1."""
    url = f"{ABS_BASE_URL}/api/me/progress/{req.item_id}"
    progress_ratio = req.current_time_seconds / req.duration_seconds if req.duration_seconds > 0 else 0.0
    payload = {
        "currentTime": req.current_time_seconds,
        "duration": req.duration_seconds,
        "progress": progress_ratio,
        "isFinished": progress_ratio >= 0.99
    }
    resp = requests.patch(url, headers=HEADERS, json=payload)
    if resp.status_code in (200, 204):
        return f"Successfully updated progress for {req.item_id} to {progress_ratio * 100:.1f}%"
    return f"Failed to update progress: {resp.status_code} - {resp.text}"

if __name__ == "__main__":
    mcp.run()
```

### 2. Audiobookshelf REST API Endpoint Reference

| HTTP Method | Endpoint Path | Description | Required Auth |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/libraries` | List all configured libraries (audiobooks & podcasts) | Bearer Token |
| `GET` | `/api/libraries/{id}/items` | Retrieve paginated catalog items for a specific library | Bearer Token |
| `GET` | `/api/items/{id}` | Get detailed metadata, chapters, and audio files for an item | Bearer Token |
| `PATCH` | `/api/me/progress/{id}` | Update listening progress, duration, and completion status | Bearer Token |
| `POST` | `/api/podcasts/feed` | Add a new podcast subscription feed URL | Bearer Token / Admin |

## Related tools / concepts
- [Navidrome](navidrome.md) — Dedicated Subsonic-compatible music streaming server.
- [Jellyfin](jellyfin.md) — Open-source video, TV, and general media platform.
- [Plex](plex.md) — Media server platform with broad client device support.
- [Whisper](whisper.md) — Automatic speech recognition for generating audiobook transcripts.
- [n8n](n8n.md) — Automation tool for webhook-driven ingestion and notification pipelines.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Agentic framework for exposing media tool APIs.
- [Authentik](authentik.md) — Identity provider for single sign-on (SSO) authentication.

## Sources / references
- [Audiobookshelf Official Documentation](https://www.audiobookshelf.org/docs)
- [Audiobookshelf GitHub Repository](https://github.com/advplyr/audiobookshelf)
- [Audiobookshelf MCP Server Repository](https://github.com/advplyr/mcp-server-audiobookshelf)
- [Audiobookshelf REST API OpenAPI Spec](https://api.audiobookshelf.org/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
