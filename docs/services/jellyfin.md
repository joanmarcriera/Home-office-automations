# Jellyfin

Jellyfin is a free, open-source media server software that organizes, manages, and streams digital media collections (movies, TV series, music, photos, and live TV) across self-hosted homelabs and AI-augmented environments in early January 2027.

## What it is
Jellyfin is an open-source media management and streaming server designed as a completely free, privacy-first alternative to commercial platforms like Plex and Emby. Operating with zero subscription paywalls and no centralized user tracking, Jellyfin natively supports hardware-accelerated transcoding (Intel QuickSync, NVENC, AMF), multi-user access control, and integration with [FastMCP 3.1](../tools/automation_orchestration/mcp.md) servers for multimodal library enrichment using models like **Claude 5.1**, **GPT-5.5 / 5.6**, and **Gemini 4.0 Pro**.

## System Architecture

The diagram below details the architecture of a self-hosted Jellyfin media streaming server, showing hardware GPU transcoding paths, FastMCP 3.1 AI enrichment workflows, and client streaming clients.

```
+-----------------------------------------------------------------------------------+
|                              Media Acquisition & Ingress                          |
|  +--------------------+   +---------------------+   +--------------------------+  |
|  | Prowlarr Indexer   |   | qBittorrent Engine  |   | Family Home Recordings   |  |
|  +---------+----------+   +----------+----------+   +------------+-------------+  |
+------------|-------------------------|---------------------------|----------------+
             | File Download Complete  | Disk Storage              | Local Upload
+------------v-------------------------v---------------------------v----------------+
|                         Jellyfin Core Server Architecture                         |
|  +-----------------------------------------------------------------------------+  |
|  | SQLite / PostgreSQL Database & Media Metadata Engine                        |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|  +-------------------------------------v---------------------------------------+  |
|  | GPU Hardware-Accelerated Transcoder Core                                    |  |
|  | - Intel QuickSync (VAAPI) / NVIDIA NVENC / AMD AMF Passthrough              |  |
|  | - On-the-fly H.264 / HEVC / AV1 to HLS / DASH Transcoding Stream Engine       |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|  +-------------------------------------v---------------------------------------+  |
|  | FastMCP 3.1 Agentic Enrichment Gateway                                      |  |
|  | - Multimodal Vision Analysis (Gemma 3 / Gemini 4.0 Pro)                      |  |
|  | - Automated Chapter Marking, Tagging, & Transcript Subtitle Generation      |  |
|  +-----------------------------------------------------------------------------+  |
+----------------------------------------|------------------------------------------+
                                         | HLS / WebSockets / REST API
+----------------------------------------v------------------------------------------+
|                                Client Playback Network                            |
|  +---------------------+   +----------------------+   +------------------------+  |
|  | Smart TV App (Roku) |   | Mobile (iOS/Android) |   | Web Browser Player     |  |
|  +---------------------+   +----------------------+   +------------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It eliminates subscription fees, central telemetry harvesting, and restrictive licensing associated with commercial media streaming solutions. Jellyfin gives users total sovereignty over personal media libraries and metadata, while providing standardized API endpoints that allow AI agents to automatically organize, generate captions, tag home videos, and categorize raw media without relying on proprietary cloud services.

## Where it fits in the stack
**Category**: Services / Media Management & Streaming. Jellyfin acts as the central media distribution engine within a homelab, interfacing with the "Arr" automation suite ([Prowlarr](prowlarr.md)), reverse proxies (Traefik, Nginx, Caddy), identity providers ([Authentik](authentik.md)), and agentic AI toolkits.

## Comparison Matrix: Self-Hosted Media Servers

| Feature | Jellyfin | Plex Media Server | Emby Server |
| :--- | :--- | :--- | :--- |
| **Licensing** | 100% Free / Open Source (GPL-3.0) | Proprietary / Freemium (Plex Pass) | Proprietary / Freemium (Emby Premiere) |
| **Hardware Transcoding** | Free (Intel QSV, NVENC, VAAPI) | Requires Paid Plex Pass | Requires Paid Emby Premiere |
| **Central Telemetry** | None (100% Offline Capable) | High (Mandatory Cloud Auth) | Moderate |
| **Remote Access** | Native Reverse Proxy / Tailscale | Turnkey Cloud Relay | Turnkey Cloud Relay / Direct |
| **Agentic AI Tools** | Native via FastMCP 3.1 & REST API | Limited Webhooks | REST API |
| **Client Ecosystem** | Broad (Android TV, Apple TV, Web) | Extensive (Nearly All Devices) | Extensive |

## Typical use cases
- **Privacy-First Streaming Server**: Streaming high-bitrate 4K HDR video and lossless audio (FLAC) across smart TVs, mobile clients, and web browsers.
- **AI-Enriched Home Video Libraries**: Utilizing FastMCP 3.1 tools to analyze unorganized family videos with multimodal vision models (**Gemma 3**, **Gemini 4.0 Pro**) to automatically generate descriptive chapters and metadata tags.
- **Automated Media Indexing**: Integrating with [n8n](n8n.md) and Prowlarr to automatically process, transcode, and catalog new media downloads.
- **Live TV & DVR Recording**: Interfacing with HDHomeRun tuners to record and stream live digital television.
- **Multi-Tenant Homelab Access**: Providing secure, authenticated media playback to family members via [Tailscale](tailscale.md) or Authentik SSO.

## Strengths
- **100% Free & Open Source**: All core features—including hardware acceleration and client apps—are completely free (FOSS, GPL-3.0).
- **Zero Telemetry & Tracking**: No centralized authentication servers or user data logging; total privacy control.
- **High-Performance Transcoding**: Hardware-accelerated video conversion supporting QuickSync, NVENC, and Vaapi.
- **Native FastMCP 3.1 Integration**: Broad API exposure enabling AI agents to search, manage, and curate libraries via standardized tool definitions.
- **Extensive Client Ecosystem**: Native client apps across Android TV, iOS, Roku, web, and desktop environments.

## Limitations
- **No Remote Relay Cloud**: Remote access requires explicit network configuration (e.g., Tailscale or reverse proxy) rather than a turnkey cloud relay.
- **Smart TV App Parity**: Older smart TV platforms may lag behind commercial alternatives in UI polish.
- **Resource Demand During Transcoding**: High-concurrent 4K transcoding requires dedicated GPU hardware or QuickSync CPU support.

## When to use it
- When requiring a completely self-hosted media server with zero telemetry, zero paywalls, and total metadata ownership.
- When integrating media catalogs with autonomous agent pipelines via FastMCP 3.1 for automated metadata classification.
- When streaming high-bitrate video across local homelab networks with custom GPU transcoding hardware.

## When not to use it
- If you desire a commercial, zero-configuration cloud relay for remote streaming without managing network ingress.
- If your hardware cannot support local transcoding or lacks adequate storage for self-hosted media.

## Getting started

### Docker Compose Baseline
Deploy Jellyfin with hardware acceleration pass-through (Intel QuickSync example):

```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: jellyfin
    user: 1000:1000
    network_mode: host
    restart: unless-stopped
    devices:
      - /dev/dri:/dev/dri # Pass through Intel QuickSync GPU devices
    volumes:
      - ./config:/config
      - ./cache:/cache
      - /path/to/media:/media:ro
```

### Initial Configuration
1. Deploy the Docker Compose stack.
2. Open your web browser and navigate to `http://localhost:8096`.
3. Complete the Setup Wizard to configure the initial administrator account.
4. Add your media libraries by linking the `/media` mount directories.

## CLI examples

```bash
# Check installed Jellyfin version inside container
docker exec -it jellyfin /jellyfin/jellyfin --version

# Tail recent container logs for troubleshooting
docker logs --tail 100 -f jellyfin

# Trigger a background library scan via command line
docker exec -it jellyfin /jellyfin/jellyfin-scanner -scan
```

## Production Systemd Service Unit

For bare-metal or virtual machine Linux deployments without Docker containers, create `/etc/systemd/system/jellyfin.service`:

```ini
[Unit]
Description=Jellyfin Media Server Daemon
After=network-online.target mount.target
Wants=network-online.target

[Service]
Type=simple
User=jellyfin
Group=jellyfin
WorkingDirectory=/usr/lib/jellyfin
ExecStart=/usr/bin/jellyfin \
    --datadir /var/lib/jellyfin \
    --cachedir /var/cache/jellyfin \
    --configdir /etc/jellyfin \
    --logdir /var/log/jellyfin
Restart=always
RestartSec=10s
LimitNOFILE=65536

# Hardware access & security hardening
SupplementaryGroups=video render
ProtectSystem=full
ProtectHome=read-only
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## API examples

### Python: AI-Assisted Metadata Enrichment with Pydantic v2
Updating Jellyfin movie metadata using validated AI-generated summaries:

```python
import requests
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class JellyfinMetadataUpdate(BaseModel):
    overview: str = Field(..., description="AI-generated summary from multimodal model analysis", min_length=10)
    genres: List[str] = Field(..., min_length=1, description="List of assigned genre tags")
    tagline: Optional[str] = Field(None, description="Generated movie tagline")
    locked_fields: List[str] = Field(default=["Overview", "Genres"], description="Lock fields from scraper overwrites")

def update_jellyfin_item(item_id: str, api_token: str, payload: dict, base_url: str = "http://localhost:8096"):
    try:
        # Validate update payload with Pydantic v2
        validated = JellyfinMetadataUpdate.model_validate(payload)

        url = f"{base_url}/Items/{item_id}"
        headers = {
            "X-Emby-Token": api_token,
            "Content-Type": "application/json"
        }

        data = {
            "Overview": validated.overview,
            "Genres": validated.genres,
            "Tagline": validated.tagline,
            "LockedFields": validated.locked_fields
        }

        res = requests.post(url, headers=headers, json=data, timeout=10)
        res.raise_for_status()
        print(f"Successfully updated metadata for Jellyfin item {item_id}")
    except ValidationError as ve:
        print(f"Metadata validation error: {ve}")
    except requests.RequestException as re:
        print(f"Jellyfin API request error: {re}")

# Example invocation:
# update_jellyfin_item("item_abc_123", "your_jellyfin_api_token", {
#     "overview": "An in-depth documentary showcasing modern homelab automation and agent orchestration.",
#     "genres": ["Technology", "Documentary"],
#     "tagline": "Homelab automation at scale."
# })
```

### FastMCP 3.1 Media Server Tool Suite (Python)
Exposing Jellyfin media discovery and playback control as agentic tools using FastMCP 3.1:

```python
import os
import httpx
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("Jellyfin-Media-Server", version="3.1.0")

JELLYFIN_URL = os.getenv("JELLYFIN_URL", "http://localhost:8096")
JELLYFIN_TOKEN = os.getenv("JELLYFIN_TOKEN", "your_jellyfin_api_token")

class MediaItemQuery(BaseModel):
    search_term: str = Field(..., min_length=2, description="Media title or keyword")
    include_genres: bool = Field(True, description="Retrieve assigned genre tags")
    limit: int = Field(5, ge=1, le=20)

@mcp.tool()
async def search_jellyfin_library(query: MediaItemQuery) -> str:
    """Searches for movies, TV shows, and media items in Jellyfin library."""
    url = f"{JELLYFIN_URL}/Items"
    headers = {"X-Emby-Token": JELLYFIN_TOKEN}
    params = {
        "searchTerm": query.search_term,
        "Limit": query.limit,
        "Recursive": "true",
        "Fields": "Overview,Genres,ProductionYear" if query.include_genres else "Overview"
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, headers=headers, params=params, timeout=8.0)
            res.raise_for_status()
            items = res.json().get("Items", [])

            if not items:
                return f"No media items found matching '{query.search_term}'."

            formatted = []
            for item in items:
                name = item.get("Name", "Unknown")
                item_type = item.get("Type", "Unknown")
                year = item.get("ProductionYear", "N/A")
                genres = ", ".join(item.get("Genres", []))
                formatted.append(f"- {name} ({year}) [{item_type}] (Genres: {genres}) - ID: {item.get('Id')}")

            return "\n".join(formatted)
        except Exception as e:
            return f"Jellyfin search error: {str(e)}"

@mcp.tool()
async def trigger_jellyfin_library_scan() -> Dict[str, Any]:
    """Triggers an asynchronous media library refresh scan across all Jellyfin mounts."""
    url = f"{JELLYFIN_URL}/Library/Refresh"
    headers = {"X-Emby-Token": JELLYFIN_TOKEN}

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, headers=headers, timeout=5.0)
            res.raise_for_status()
            return {"status": "SUCCESS", "message": "Jellyfin library refresh scan initiated."}
        except Exception as e:
            return {"status": "FAILED", "error": str(e)}

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & GPU Acceleration Tuning

1. **QuickSync GPU Permissions**: Ensure the host user running the Jellyfin container belongs to the `video` and `render` groups (typically GID 44 or 109 on Linux systems) to avoid permission denied errors when accessing `/dev/dri/renderD128`.
2. **Cache Directory Offloading**: Allocate high-speed NVMe storage for Jellyfin's `/cache` directory to prevent micro-stutters during dynamic trickplay thumbnail generation and active transcoding chunks.
3. **Automated Library Scanning Rate Limits**: Configure webhooks from intake tools (e.g., qBittorrent or Sonarr/Radarr) rather than setting periodic automated library scans every 15 minutes, preserving CPU/IOPS for playback.

## Troubleshooting & Diagnostic Matrix

| Symptom / Issue | Probable Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| Transcoding fails immediately (`Playback Error`) | Lacking read/write permissions on `/dev/dri/renderD128` or missing GPU drivers inside container. | Verify host group ownership (`ls -la /dev/dri`) and append `group_add: ["44", "109"]` in `docker-compose.yml`. |
| High CPU usage (>90%) during 4K streaming | Hardware acceleration disabled; falling back to software CPU encoding. | Navigate to **Dashboard > Playback > Transcoding** and select Intel QuickSync (QSV) or NVENC explicitly. |
| Subtitles out of sync or rendering as plain text | Client player does not support native ASS/SSA subtitle rendering, forcing full video burn-in. | Enable **Extract Subtitles** in Client Playback settings or convert ASS subtitles to SRT using automated scripts. |
| Remote clients cannot connect (`Connection Timed Out`) | Missing port forwarding or reverse proxy header configuration. | Ensure reverse proxy passes `Host`, `X-Real-IP`, and `X-Forwarded-For` HTTP headers and WebSocket upgrades (`Upgrade: $http_upgrade`). |
| Library scan misses newly added media files | Incorrect directory permission masks (`umask`) set by download client. | Set directory permissions to `755` and file permissions to `644` in downstream download tools (qBittorrent/Sabnzbd). |

## Related tools / concepts
- [Plex](plex.md) — Proprietary media server alternative.
- [Authentik](authentik.md) — SSO authentication provider securing Jellyfin access.
- [Tailscale](tailscale.md) — Encrypted mesh VPN for remote streaming access.
- [Prowlarr](prowlarr.md) — Indexer management for automated media pipelines.
- [n8n](n8n.md) — Workflow automation engine for Jellyfin webhooks.
- [FastMCP](../tools/automation_orchestration/mcp.md) — Model Context Protocol framework for agentic media tools.

## Sources / references
- [Jellyfin Official Website](https://jellyfin.org/)
- [Jellyfin Container Installation Docs](https://jellyfin.org/docs/general/installation/container)
- [Jellyfin API Reference](https://api.jellyfin.org/)
- [Jellyfin GitHub Repository](https://github.com/jellyfin/jellyfin)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
