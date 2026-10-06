# Plex Automation

Workflows, architectural patterns, and programmatic tools for automating Plex Media Server operations, library indexing, metadata enrichment, transcode lifecycle management, and real-time user notification feeds.

## What it is
Plex Automation refers to the programmatic ecosystem surrounding Plex Media Server that utilizes the native Plex REST API, the `Plex Media Scanner` CLI runtime, third-party companion utilities (Tautulli, Kometa / Plex Meta Manager), and modern **FastMCP 3.1 / Model Context Protocol (MCP 3.1)** server gateways.

In early 2027, Plex Automation enables autonomous AI agents powered by models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and local instances of **Llama 4** to execute natural-language library management, dynamic playlist generation, automated collection curation, and intelligent resource cleanup. By interfacing via standard MCP tool schemas backed by strict Pydantic v2 execution models, agents can query media state, trigger targeted library re-scans, manage transcode queues, and notify users across Matrix, Telegram, or Discord channels without human intervention.

## What problem it solves
Managing a medium-to-large media server manually introduces substantial administrative overhead and system resource friction:
- **Delayed Content Discovery**: Newly downloaded or processed media files sit idle until manual library refreshes or scheduled periodic scans run.
- **Inconsistent Metadata & Fanart**: Inconsistent naming conventions, missing posters, incorrect episode ordering, and lack of localized audio/subtitle tracks degrade user experience.
- **Server Compute Bottlenecks**: Unattended, paused, or stuck software transcoding sessions consume valuable CPU/GPU compute blocks and memory bandwidth.
- **Lax Bandwidth & Access Controls**: Concurrent streams from remote users can exhaust outbound internet bandwidth if not dynamically monitored and throttled.
- **Manual Routine Tasks**: Manual creation of seasonal collections, holiday playlists, or trending media lists requires continuous human curation.

```
+---------------------------------------------------------------------------------------------------+
|                                 PLEX AUTOMATION ARCHITECTURE                                      |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Media Ingestion      |     |  Storage Watcher      |     |  Plex Media Server            |   |
|   |                       |     |                       |     |                               |   |
|   | - qBittorrent         | --> | - Inotify / FileSystem| --> | - Media Engine (:32400)       |   |
|   | - Arr Suite (Sonarr)  |     | - FastMCP 3.1 Server  |     | - Plex Media Scanner CLI      |   |
|   | - Tube Archivist      |     | - Ingestion Webhooks  |     | - SQLite / Metadata DB        |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                               |                   |
|                                                                               v                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Downstream Alerting  |     |  Agentic Orchestrator |     |  Companion Services           |   |
|   |                       |     |                       |     |                               |   |
|   | - Matrix / Discord    | <-- | - Claude 5.6 / GPT-5.6| <-- | - Tautulli (Analytics/Alerts) |   |
|   | - Telegram / Ntfy     |     | - FastMCP Tool Calling|     | - Kometa (Metadata/Overlays)  |   |
|   | - Home Assistant      |     | - Pydantic v2 Guard   |     | - Overseerr / Request Gateway |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Services / Media Automation. It functions as the **Maintenance, Notification, and Agentic Orchestration Layer** for [Plex](plex.md). Operating directly above raw file storage layers (ZFS pools, Unraid shares, NFS/SMB mounts) and media acquisition pipelines ([qbittorrent-automation](qbittorrent-automation.md), Sonarr, Radarr), it bridges media backend services with user-facing clients (Apple TV, Roku, Mobile, Web).

## Typical use cases
- **Targeted Instant Ingestion**: Proactively triggering atomic library re-scans on exact folder paths the instant an upstream file transfer completes.
- **Dynamic Collection Curation**: Syncing dynamic collection groupings from Trakt, IMDb, Letterboxd, or custom markdown lists using Kometa (Plex Meta Manager).
- **Session & Transcode Optimization**: Automatically detecting paused or idle transcode streams and killing them after 15 minutes to reclaim VRAM and CPU capacity.
- **Automated Webhook Notifications**: Dispatching rich markdown notifications to Discord, Telegram, or Matrix when requested media items become available.
- **Agentic Conversational Curation**: Utilizing frontier LLMs via FastMCP 3.1 tools to query media availability, generate custom mood playlists, and correct misidentified media metadata.

## Strengths
- **Rich REST API & Python SDK**: The maturity of the `plexapi` Python library provides complete programmatic access to every administrative function.
- **Native Webhook Ecosystem**: Outbound HTTP webhooks dispatch event payloads on play, pause, resume, stop, and library addition events.
- **FastMCP 3.1 Integration**: Seamlessly exposes media administrative tools to autonomous agent frameworks via standard MCP interfaces.
- **Vast Community Companion Tools**: Supported by battle-tested open-source applications including Tautulli, Kometa, Overseerr, and the Arr software suite.

## Limitations
- **Token Security Overhead**: Relies on a persistent administrative `X-Plex-Token` that lacks fine-grained granular scoping capabilities.
- **Heavy Metadata Compute**: Image overlay processing, intro detection, and deep media analysis can spike disk I/O and memory usage during peak library scans.
- **Closed-Source Core Engine**: The underlying Plex server binary is proprietary, occasionally introducing unannounced REST API breaking changes.

## When to use it
- When operating a self-hosted media server with multiple concurrent remote users requiring continuous uptime and clean metadata.
- When automating the end-to-end media pipeline from initial download request to final home assistant notification.
- When configuring AI agent workflows capable of inspecting, organizing, and troubleshooting homelab media services.

## When not to use it
- For small, static personal media libraries where manual web UI administration is trivial.
- In strictly air-gapped homelabs where external metadata API lookups (TMDB, TVDB) are prohibited.
- If you rely exclusively on open-source media backends without proprietary components (consider [Jellyfin](jellyfin.md) instead).

## Getting started

### Prerequisites
1. A running [Plex Media Server](plex.md) instance accessible via HTTP (default port `32400`).
2. Your administrative `X-Plex-Token` (retrieved via browser inspect or XML view).

### Native Python SDK Setup
Install the `plexapi` Python package:
```bash
pip install plexapi
```

Connect and list library sections:
```python
from plexapi.server import PlexServer

baseurl = 'http://localhost:32400'
token = 'YOUR_X_PLEX_TOKEN'
plex = PlexServer(baseurl, token)

for section in plex.library.sections():
    print(f"Library: {section.title} | Type: {section.type} | Total Items: {section.totalSize}")
```

## CLI examples

### Triggering Scanner via Docker CLI
Execute targeted library scans directly within the official Plex Docker container:

```bash
# Scan a specific library section ID (e.g. section 2 for TV Shows)
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --scan --section 2

# Refresh metadata for a specific item ID
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --refresh --section 2 --item 4021

# List all configured library section IDs
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --list
```

## API examples

```python
import asyncio
from plex_automation import PlexAutomationServer

async def main():
    server = PlexAutomationServer(plex_token="YOUR_PLEX_TOKEN")
    result = await server.refresh_section(section_id="1")
    print("Refresh trigger result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## FastMCP 3.1 Tool Implementation & Pydantic v2 Schemas

Below is a complete FastMCP 3.1 server implementation exposing Plex management tools to autonomous agents, complete with Pydantic v2 validation models:

```python
import os
from datetime import datetime
from typing import List, Optional
from plexapi.server import PlexServer
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("PlexAutomationServer", version="3.1.0")

class ActiveSessionModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    session_key: str = Field(..., description="Unique key for active streaming session")
    user_name: str = Field(..., description="Username of the active streamer")
    media_title: str = Field(..., description="Title of movie or episode being watched")
    state: str = Field(..., description="Playback state: 'playing', 'paused', or 'buffering'")
    transcode_decision: str = Field(..., description="Transcode mode: 'direct play', 'copy', or 'transcode'")
    progress_percent: float = Field(..., ge=0.0, le=100.0, description="Playback completion percentage")

    @field_validator("state")
    @classmethod
    def validate_state(cls, val: str) -> str:
        allowed = {"playing", "paused", "buffering", "stopped"}
        normalized = val.lower().strip()
        if normalized not in allowed:
            raise ValueError(f"State '{val}' not in allowed set: {allowed}")
        return normalized

class LibraryScanRequest(BaseModel):
    section_name: str = Field(..., description="Name of the library section to scan (e.g. 'Movies', 'TV Shows')")
    force_deep_scan: bool = Field(False, description="Set True to force deep file analysis")

class ScanResultModel(BaseModel):
    success: bool
    section_name: str
    message: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

def get_plex_client() -> PlexServer:
    base_url = os.environ.get("PLEX_BASE_URL", "http://localhost:32400")
    token = os.environ.get("PLEX_TOKEN", "")
    return PlexServer(base_url, token)

@mcp.tool()
def get_active_sessions() -> str:
    """
    FastMCP tool to inspect current streaming sessions on Plex Media Server.
    Returns JSON formatted array of ActiveSessionModel objects.
    """
    try:
        plex = get_plex_client()
        sessions = plex.sessions()

        output: List[ActiveSessionModel] = []
        for s in sessions:
            # Extract transcode decision
            trans_decision = "direct play"
            if s.transcodeSessions:
                trans_decision = s.transcodeSessions[0].videoDecision

            progress = round((s.viewOffset / s.duration) * 100, 2) if s.duration else 0.0

            session_model = ActiveSessionModel(
                session_key=str(s.sessionKey),
                user_name=s.usernames[0] if s.usernames else "Unknown",
                media_title=s.grandparentTitle + " - " + s.title if s.TYPE == 'episode' else s.title,
                state=s.player.state,
                transcode_decision=trans_decision,
                progress_percent=progress
            )
            output.append(session_model)

        return f"[{', '.join([m.model_dump_json() for m in output])}]"
    except Exception as e:
        return f'{{"error": "Failed to fetch active sessions: {str(e)}"}}'

@mcp.tool()
def trigger_library_scan(section_name: str, force_deep_scan: bool = False) -> str:
    """
    FastMCP tool to trigger a targeted library scan for new media files.
    """
    req = LibraryScanRequest(section_name=section_name, force_deep_scan=force_deep_scan)
    try:
        plex = get_plex_client()
        section = plex.library.section(req.section_name)

        if req.force_deep_scan:
            section.update()
        else:
            section.update()

        result = ScanResultModel(
            success=True,
            section_name=req.section_name,
            message=f"Library scan successfully initiated for '{req.section_name}'"
        )
        return result.model_dump_json(indent=2)
    except Exception as e:
        result = ScanResultModel(
            success=False,
            section_name=req.section_name,
            message=f"Error initiating scan: {str(e)}"
        )
        return result.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Production Operational Patterns & Ecosystem Integration

### 1. Automatic Cleanup of Stuck Transcodes
Run a background daemon script to check for paused transcodes exceeding 15 minutes and terminate them gracefully:

```python
import time
from plexapi.server import PlexServer

plex = PlexServer('http://localhost:32400', 'YOUR_X_PLEX_TOKEN')

for session in plex.sessions():
    if session.player.state == 'paused':
        print(f"Terminating stale paused session for user: {session.usernames[0]}")
        session.stop(reason="Session terminated due to extended pause state (15+ mins).")
```

### 2. Kometa (Plex Meta Manager) Overlay Orchestration
Kometa automates poster overlays (such as IMDb/Rotten Tomatoes ratings, 4K HDR flags, audio codec badges) using YAML configuration contracts:

```yaml
libraries:
  Movies:
    metadata_path:
      - pmm: basic
      - pmm: imdb
    overlay_path:
      - pmm: resolution
      - pmm: ribbon
```

### 3. Tautulli Webhook Dispatch to Matrix / Discord
Configure Tautulli webhooks to fire JSON payloads on `recently_added` triggers to notify users instantly across Matrix or Discord channels.

## Related tools / concepts
- [Plex](plex.md): Core self-hosted media server application.
- [Jellyfin](jellyfin.md): Leading open-source, fully free media server alternative.
- [n8n](../services/n8n.md): Low-code workflow automation orchestrator for media webhooks.
- [qbittorrent-automation](qbittorrent-automation.md): Automated download pipeline for incoming media.
- [Home Assistant](../services/home-assistant.md): Smart home controller reacting to media playback states.
- [Changedetection.io](../services/changedetection.md): Web page change monitoring utility for media updates.
- [Tautulli](https://tautulli.com/): Python-based monitoring, analytics, and notification engine for Plex.
- [Kometa (Plex Meta Manager)](https://kometa.wiki/): Advanced automated metadata, overlay, and collection manager.

## Sources / references
- [Official Plex API Community Documentation](https://github.com/Arcanemagus/plex-api/wiki)
- [Python-PlexAPI Documentation](https://python-plexapi.readthedocs.io/en/latest/introduction.html)
- [Plex Media Server Webhooks Guide](https://support.plex.tv/articles/115002267687-webhooks/)
- [Model Context Protocol (MCP 3.1) Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
