# qBittorrent

## What it is
qBittorrent is a premier, open-source BitTorrent client designed for cross-platform reliability and performance. Written in C++ using the Qt toolkit, it provides a feature-rich, advertisement-free alternative to proprietary clients. In early January 2027, version **5.x** has solidified its position as the industry standard for self-hosted torrenting, featuring advanced asynchronous piece calculation, frontier model (Claude 5.1, Claude 5.6, GPT-5.5, GPT-5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, Gemma 3, Qwen 3.8) analysis for download health, and native Model Context Protocol (FastMCP 3.1) support.

## What problem it solves
Managing file transfers via the BitTorrent protocol can be resource-intensive and organizationally complex. qBittorrent solves this by providing a lightweight, headless-capable engine with a powerful Web UI. It allows users to manage massive torrent libraries, automate downloads via RSS, and securely access their transfer queue remotely without compromising on features or privacy.

## Where it fits in the stack
**Category**: Service / Content Acquisition. It serves as the **primary data intake engine** for large-scale file transfers, typically integrated with media servers and automation frameworks in a homelab environment.

## Typical use cases
- **Headless Server Operations**: Running as a Docker container on a NAS or VPS for 24/7 seeding and downloading.
- **Automated ISO Acquisition**: Using RSS feeds to automatically mirror open-source software distributions.
- **Agentic File Transfers**: Allowing AI agents (e.g., Claude 5.1, Claude 5.6, GPT-5.5, GPT-5.6) to manage the download queue via the Web API and FastMCP 3.1 Task Protocol.
- **Remote Library Management**: Accessing and controlling torrents from any device via the integrated Web UI.
- **High-Performance Seeding**: Leveraging the libtorrent-rasterbar backend for efficient multi-gigabit seeding.

## Strengths
- **No Bloatware**: Completely free and open-source with no bundled ads or tracking.
- **Powerful Web UI**: A near-perfect replica of the desktop interface accessible via any browser.
- **Integrated Search Engine**: Allows finding torrents directly within the client across multiple indexers.
- **Advanced Organizational Tools**: Support for categories, tags, and sub-categories for managing thousands of torrents.
- **Native FastMCP 3.1 Integration**: Direct "Tool Calling" support for AI agents to securely query and manipulate torrents using modern JSON schemas.
- **Open Source Licensing**: Licensed under GPL-2.0, ensuring it remains free and community-driven.

## Limitations
- **Security Dependency**: Requires careful network configuration (VPN, Killswitch, Proxy) for privacy-conscious users.
- **UI Aesthetic**: While highly functional, the interface follows a traditional desktop metaphor which may feel dated to some.
- **Resource Usage**: Large libraries with tens of thousands of active torrents can still be memory-intensive, despite recent optimizations.

## When to use it
- When you need a reliable, high-performance BitTorrent client for a server or desktop environment.
- To eliminate advertisements and proprietary bloat from your torrenting workflow.
- For managing a headless download box that is accessible via a web browser or API.
- When building automated content pipelines that require a robust, documented Web API.

## When not to use it
- If your primary need is for protocols other than BitTorrent (e.g., USENET, IPFS).
- In environments where a very minimal, single-purpose client (like Transmission) is preferred over a feature-rich one.

## Getting started

### Docker Compose (Standard stack with Gluetun VPN)
The recommended way to run qBittorrent is with a VPN sidecar like Gluetun to ensure privacy:

```yaml
services:
  gluetun:
    image: qmcgaw/gluetun
    container_name: gluetun
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    environment:
      - VPN_SERVICE_PROVIDER=your_provider
      - VPN_TYPE=wireguard
      - WIREGUARD_PRIVATE_KEY=your_key
      - WIREGUARD_ADDRESSES=10.0.0.2/32
    ports:
      - 8080:8080 # qBittorrent Web UI
      - 6881:6881
      - 6881:6881/udp

  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    network_mode: "container:gluetun"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      - WEBUI_PORT=8080
    volumes:
      - ./config:/config
      - ./downloads:/downloads
    restart: unless-stopped
```

### Hello World
1. Access the Web UI at `http://localhost:8080`.
2. Change the default credentials in **Tools > Options > Web UI**.
3. Go to **Tools > Options > BitTorrent** and check "Add torrents in Paused state" for better control.
4. Paste a magnet link to a legal torrent (e.g., an Ubuntu ISO) to verify the engine is working.

## CLI examples
Interact with the qBittorrent container for maintenance or debugging.

```bash
# Check the version of qBittorrent-nox running in the container
docker exec qbittorrent qbittorrent-nox --version

# View recent logs to find the temporary WebUI password
docker logs qbittorrent | grep password

# Manually pause all active torrents
docker exec qbittorrent qbittorrent-nox --pause-all
```

## API examples
The Web API (v2) is the primary method for external interaction. The following Python code uses Pydantic v2 to validate active torrent information.

```python
import requests
from pydantic import BaseModel, Field, field_validator
from typing import List

# Define the model schema for validating active torrents using Pydantic v2
class TorrentInfo(BaseModel):
    name: str = Field(..., description="The name of the torrent")
    progress: float = Field(..., description="The download progress as a fraction of 1 (0.0 to 1.0)")
    status: str = Field(..., description="The current status (downloading, seeding, paused, etc.)")
    num_seeds: int = Field(..., alias="num_seeds", description="The number of connected seeds")

    @field_validator('progress')
    @classmethod
    def validate_progress(cls, val: float) -> float:
        if not (0.0 <= val <= 1.0):
            raise ValueError("Progress must be between 0.0 and 1.0")
        return val

class TorrentListResponse(BaseModel):
    torrents: List[TorrentInfo]

def fetch_active_torrents(api_url: str) -> TorrentListResponse:
    # Step 1: Login session
    session = requests.Session()
    login_url = f"{api_url}/api/v2/auth/login"
    session.post(login_url, data={'username': 'admin', 'password': 'password'})

    # Step 2: Query Torrent Info
    info_url = f"{api_url}/api/v2/torrents/info"
    response = session.get(info_url)
    raw_data = response.json()

    parsed_torrents = []
    for item in raw_data:
        try:
            torrent = TorrentInfo(
                name=item.get("name"),
                progress=item.get("progress"),
                status=item.get("state"),
                num_seeds=item.get("num_seeds", 0)
            )
            parsed_torrents.append(torrent)
        except Exception as e:
            print(f"Skipping malformed entry: {e}")

    return TorrentListResponse(torrents=parsed_torrents)

# Example usage
if __name__ == "__main__":
    url_base = "http://localhost:8080"
    data = fetch_active_torrents(url_base)
    for t in data.torrents:
        print(f"Validated Torrent: {t.name} ({t.progress * 100:.1f}%) Status: {t.status}")
```

## Related tools / concepts
- [qBittorrent Automation](qbittorrent-automation.md) — For advanced API workflows and n8n integrations.
- [n8n](n8n.md) — For orchestrating downloads with other services.
- [Plex](plex.md) — For consuming media downloaded via qBittorrent.
- [Jellyfin](jellyfin.md) — Open-source media server alternative.
- [Authentik](authentik.md) — For securing remote access to the Web UI.
- [Tailscale](tailscale.md) — For secure remote access to the dashboard.
- [SearXNG](searXNG.md) — A privacy-focused search engine for finding torrents.
- [Paperless-ngx](paperless-ngx.md) — For managing documents acquired via Bittorrent.
- [Local LLMs Guide](../tools/ai_knowledge/local_llms.md) — Reference for Gemma 3 and other models.
- [Gluetun](https://github.com/qdm12/gluetun) — VPN sidecar for secure torrenting.

## Sources / references
- [qBittorrent Official Project Site](https://www.qbittorrent.org/)
- [qBittorrent Source Code Repository](https://github.com/qbittorrent/qBittorrent)
- [Web API Development Reference](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1))
- [Model Context Protocol Specification](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
