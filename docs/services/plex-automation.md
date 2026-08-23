# Plex Automation

Workflows and scripts for managing Plex media libraries, metadata, and user activity.

## What it is
Plex Automation involves using the Plex Media Server API, the Plex Media Scanner CLI, and third-party tools to automate library updates, metadata refinement, transcode optimization, and real-time user notification flows. As of **January 2027**, this ecosystem has fully integrated with **Model Context Protocol (FastMCP 3.1)** and the **MCP 3.1 Task Protocol**, enabling autonomous AI agents powered by Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, and Gemma 3 to perform natural-language-driven library curation, playlist generation, and system administration with standardized tool schemas and robust Pydantic v2 execution models.

## What problem it solves
It completely eliminates the administrative overhead of manual library management. It ensures that new media is scanned and matched immediately upon arrival, metadata (such as custom covers, background art, and collection structures) remains pristine, and users receive automated notifications when their requested content is ready. Furthermore, it prevents performance degradation by automatically terminating stale or paused transcoded streams to conserve CPU/GPU compute blocks, and enables natural language conversational control over home media servers.

## Where it fits in the stack
**Category**: Services / Media Automation. It serves as the "Maintenance, Notification & Orchestration" layer for the [Plex](plex.md) media server, acting as the intelligent bridge between raw file storage layers (such as ZFS or NFS mounts) and the user-facing client application interfaces.

## Typical use cases
- **Intelligent Library Syncing**: Proactively triggering library scans for specific paths the instant the storage watcher daemon detects a complete file transfer.
- **Dynamic Collection Management**: Utilizing tools like **Plex Meta Manager (PMM)** to sync collections dynamically from Trakt, IMDb, or Letterboxd lists.
- **Real-Time Notification Workflows**: Leveraging Tautulli webhooks to dispatch custom Discord, Telegram, or Matrix messages when content is added or when playback is initiated.
- **Agentic Curation**: Using Gemini 4.0 Pro or Claude 5.6 to detect misidentified items, fetch high-resolution fan-art, or group anime seasons utilizing complex regex mapping.
- **Session Optimizer**: Monitoring active transcodes and killing paused sessions after 15 minutes of inactivity to optimize hardware usage.

## Strengths
- **Exhaustive REST API**: Virtually every action possible in the Plex Web interface is exposed and controllable via standard API endpoints.
- **Robust Python SDK**: The `plexapi` wrapper is highly mature and simplifies complex server-management workflows.
- **Extensive Ecosystem**: Backed by massive community-driven tools such as Tautulli, Plex Meta Manager, and the Arr suite.
- **FastMCP 3.1 Compatibility**: FastMCP-enabled gateways allow frontier models to query and update media states natively.

## Limitations
- **Token Security**: Relies on a persistent `X-Plex-Token`, which requires secure handling and lacks fine-grained scoping.
- **High Resource Requirements**: Heavy metadata processing (e.g., custom overlays or intros detection) can consume substantial memory and CPU.
- **Proprietary Core**: The underlying Plex server API remains closed-source, leading to occasional unannounced structural changes.

## When to use it
- When managing a medium-to-large scale server with multiple active users.
- To maintain professional-grade metadata consistency (e.g., standardized posters, language tracks, and collection hierarchies).
- When integrating media server status with custom homelab dashboards or multi-agent orchestration stacks.

## When not to use it
- If your server is purely personal and hosts a small, static library.
- If you have strict "air-gapped" security concerns that prohibit external API calls for metadata fetching.
- If you prefer complete manual control and do not mind occasionally misidentified media.

## Getting started

### Prerequisites
- A running [Plex](plex.md) instance with an active port binding (default `32400`).
- Your [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/).

### Hello World (Python)
Install the `plexapi` SDK:
```bash
pip install plexapi
```

Connect and query library sections:
```python
from plexapi.server import PlexServer

baseurl = 'http://localhost:32400'
token = 'YOUR_PLEX_TOKEN'
plex = PlexServer(baseurl, token)

for section in plex.library.sections():
    print(f"Section: {section.title} ({section.type})")
```

## CLI examples

Automation scripts often leverage the `Plex Media Scanner` CLI located inside the server container:

```bash
# Scan a specific library section (replace <id> with the section ID)
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --scan --section <id>

# Perform a deep refresh of metadata on a section
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --refresh --section <id>

# Output all configured libraries and their unique identifiers
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --list
```

## API examples

### Pydantic v2 Configurations & Session Validation
For reliable agentic execution, we use **Pydantic v2** to parse, validate, and verify our Plex configuration payloads and incoming webhook alerts.

```python
from pydantic import BaseModel, HttpUrl, Field, SecretStr
from typing import Optional
from datetime import datetime

class PlexServerConfig(BaseModel):
    """Configuration model for validating Plex Server connections."""
    base_url: HttpUrl = Field(..., description="The base HTTP/HTTPS URL of the Plex Server")
    token: SecretStr = Field(..., description="The secure X-Plex-Token required for authentication")
    library_id: int = Field(..., ge=1, description="The unique section ID of the target library")
    sync_interval_seconds: int = Field(default=300, ge=30, description="Scanning loop cycle time")

class PlexSessionAlert(BaseModel):
    """Pydantic model representing a parsed web alert from Tautulli or Plex."""
    event_type: str = Field(..., pattern="^(play|pause|stop|library_add)$")
    user: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    rating_key: str = Field(..., description="Unique Plex identifier for the media item")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Example usage of model validation
config_data = {
    "base_url": "http://192.168.1.100:32400",
    "token": "PLX12345XYZ",
    "library_id": 2
}
validated_config = PlexServerConfig(**config_data)
print(f"Validated connection to: {validated_config.base_url}")
```

### Auto-Delete Watched Content (Python)
```python
# Script to safely delete watched episodes from a temporary library section
from plexapi.server import PlexServer

plex = PlexServer('http://localhost:32400', 'YOUR_PLEX_TOKEN')
trash_library = plex.library.section('Temporary TV')

for episode in trash_library.search(viewed=True):
    print(f"Deleting watched temporary episode: {episode.title}")
    episode.delete()
```

## Related tools / concepts
- [Plex](plex.md) — The core self-hosted media server.
- [Jellyfin](jellyfin.md) — The leading open-source alternative.
- [n8n](../services/n8n.md) — Advanced workflow engine often utilized to map Plex alerts to social channels.
- [qbittorrent-automation](qbittorrent-automation.md) — Automating file downloads prior to Plex scanning.
- [Home Assistant](../services/home-assistant.md) — Syncing smart lights with Plex playback states.
- [Changedetection.io](../services/changedetection.md) — Monitoring upstream tracker releases.
- [Nextcloud](../services/nextcloud.md) — Secure storage sync for media assets and server databases.
- [Tube Archivist](../services/tubearchivist.md) — Self-hosted YouTube preservation hub.
- [Tautulli](https://tautulli.com/) — Premium monitoring and notification utility.
- [Plex Meta Manager](https://metamanager.wiki/) — Powerhouse metadata, overlays, and collection orchestrator.

## Sources / references
- [Official Plex API Documentation (Community Maintained)](https://github.com/Arcanemagus/plex-api/wiki)
- [Python-PlexAPI Documentation](https://python-plexapi.readthedocs.io/en/latest/introduction.html)
- [Plex Webhooks Reference](https://support.plex.tv/articles/115002267687-webhooks/)
- [Model Context Protocol Specification 3.1](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
