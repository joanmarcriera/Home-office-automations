# Plex Automation

Workflows and scripts for managing Plex media libraries, metadata, and user activity.

## What it is
Plex Automation involves using the Plex Media Server API, the Plex Media Scanner CLI, and third-party tools to automate library updates, metadata refinement, and notifications. As of **June 2026**, this ecosystem has evolved to include native **Model Context Protocol (MCP 3.0)** support for agentic media management via Claude 4.8 Opus and GPT-5.5.

## What problem it solves
It eliminates manual library management. It ensures that new media is scanned and matched immediately, library metadata (like posters and collections) is kept clean and consistent, and users are notified when new content they are interested in becomes available. It also enables natural language discovery and orchestration through autonomous agents.

## Where it fits in the stack
**Category**: Services / Media Automation. It is the "Maintenance & Notification" layer for the [Plex](plex.md) media server, acting as the bridge between raw file storage and the user-facing streaming interface.

## Typical use cases
- Automatically refreshing library sections when a new file is detected via filesystem watcher.
- Using **Plex Meta Manager (PMM)** to create dynamic collections (e.g., "Top IMDB Movies").
- Sending a Discord/Telegram message whenever a new movie is added to the server (via Tautulli).
- Agentic maintenance: Using Claude 4.8 Opus to identify and fix metadata mismatches or low-quality posters across a 10,000+ item library.
- Automatically killing transcoding streams that have been paused for too long to save CPU.

## Strengths
- **Comprehensive API**: Almost every action in the Plex Web UI can be performed via the API.
- **Strong Ecosystem**: Tools like Tautulli and Plex Meta Manager provide advanced automation out of the box.
- **Python Integration**: The `plexapi` library is mature and provides high-level abstractions for complex tasks.
- **Agentic Ready**: Native MCP 3.0 servers allow for seamless integration with LLMs for conversational media control.

## Limitations
- **Token Management**: Requires a `X-Plex-Token`, which can be tricky to retrieve for some users.
- **Complexity**: Advanced metadata automation (like custom overlays on posters) can be difficult to set up initially.
- **Proprietary API**: While comprehensive, the API is not open-source, and breaking changes can occur without notice.

## When to use it
- When you have a large media library that is difficult to manage manually.
- To provide a "premium" streaming experience for family and friends with automated notifications and collections.
- When you want to integrate your media server with other homelab notification systems or AI agents.

## When not to use it
- If you have a small library and only use Plex occasionally.
- If you don't care about metadata consistency or posters.
- If you prefer a completely manual, "air-gapped" media management style.

## Getting started

### Prerequisites
- A running [Plex](plex.md) instance.
- Your [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/).

### Hello World (Python)
Install the `plexapi` library:
```bash
pip install plexapi
```

Connect and list all library sections:
```python
from plexapi.server import PlexServer

baseurl = 'http://localhost:32400'
token = 'YOUR_PLEX_TOKEN'
plex = PlexServer(baseurl, token)

for section in plex.library.sections():
    print(f"Section: {section.title} ({section.type})")
```

## CLI examples

Automation often involves the `Plex Media Scanner` inside the Docker container.

```bash
# Scan a specific library section to find new files (replace <id> with section ID)
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --scan --section <id>

# Refresh metadata for a specific section
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --refresh --section <id>

# List all sections and their IDs
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --list
```

## API examples

### n8n Integration (Webhook)
You can use n8n to react to Plex Webhooks (requires Plex Pass). In Plex, go to **Settings > Webhooks** and add your n8n webhook URL. n8n will receive JSON payloads for events like:
- `library.on.deck`: When a new item is added to "On Deck".
- `media.play`: When a user starts watching something.
- `media.scrobble`: When a user finishes watching something.

### Auto-Delete Watched Content (Python)
```python
# Simple script to delete episodes from a 'Trash' library once watched
trash_library = plex.library.section('Trash TV')
for episode in trash_library.search(viewed=True):
    print(f"Deleting watched episode: {episode.title}")
    episode.delete()
```

## Related tools / concepts
- [Plex](plex.md) — The core media server.
- [Jellyfin](jellyfin.md) — Open-source media server alternative.
- [n8n](n8n.md) — Workflow orchestration for media ingestion.
- [qbittorrent-automation](qbittorrent-automation.md) — Automating content acquisition.
- [Home Assistant](home-assistant.md) — For notifications and playback-based automations.
- [Changedetection.io](changedetection.md) — Monitoring trackers or metadata sources.
- [Nextcloud](nextcloud.md) — For off-server backups of configuration and metadata.
- [Tube Archivist](tubearchivist.md) — For preserving YouTube content.
- [Tautulli](https://tautulli.com/) — Monitoring and notification system.
- [Plex Meta Manager](https://metamanager.wiki/) — Advanced metadata automation.

## Sources / References
- [Official Plex API Documentation (Community Maintained)](https://github.com/Arcanemagus/plex-api/wiki)
- [Python-PlexAPI Documentation](https://python-plexapi.readthedocs.io/en/latest/introduction.html)
- [Plex Webhooks Overview](https://support.plex.tv/articles/115002267687-webhooks/)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
