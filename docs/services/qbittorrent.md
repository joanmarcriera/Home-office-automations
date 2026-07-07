# qBittorrent

## What it is
qBittorrent is a premier, open-source BitTorrent client designed for cross-platform reliability and performance. Written in C++ using the Qt toolkit, it provides a feature-rich, advertisement-free alternative to proprietary clients. As of **July 2026**, version **5.2.0** has solidified its position as the industry standard for self-hosted torrenting, featuring advanced asynchronous piece calculation and native [Model Context Protocol (MCP 3.0)](../tools/automation_orchestration/mcp.md) support. It is licensed under **GPL-2.0** and is entirely free.

## What problem it solves
Managing file transfers via the BitTorrent protocol can be resource-intensive and organizationally complex. qBittorrent solves this by providing a lightweight, headless-capable engine with a powerful Web UI. It allows users to manage massive torrent libraries, automate downloads via RSS, and securely access their transfer queue remotely without compromising on features or privacy.

## Where it fits in the stack
**Category**: Service / Content Acquisition. It serves as the **primary data intake engine** for large-scale file transfers, typically integrated with media servers like [Plex](plex.md) and automation frameworks like [n8n](n8n.md) in a homelab environment.

## Typical use cases
- **Headless Server Operations**: Running as a [Docker](../tools/infrastructure/docker.md) container on a NAS or VPS for 24/7 seeding and downloading.
- **Automated ISO Acquisition**: Using RSS feeds to automatically mirror open-source software distributions.
- **Agentic File Transfers**: Allowing AI agents (e.g., [Gemma 3](../tools/ai_knowledge/local_llms.md), Claude 4.8 Opus) to manage the download queue via the Web API and [MCP 3.0](../tools/automation_orchestration/mcp.md).
- **Remote Library Management**: Accessing and controlling torrents from any device via the integrated Web UI or secure [Tailscale](tailscale.md) connection.
- **High-Performance Seeding**: Leveraging the libtorrent-rasterbar backend for efficient multi-gigabit seeding.

## Strengths
- **No Bloatware**: Completely free and open-source with no bundled ads or tracking.
- **Powerful Web UI**: A near-perfect replica of the desktop interface accessible via any browser.
- **Integrated Search Engine**: Allows finding torrents directly within the client across multiple indexers like [Jackett](jackett.md).
- **Advanced Organizational Tools**: Support for categories, tags, and sub-categories for managing thousands of torrents.
- **Native MCP 3.0 Integration**: Direct "Tool Calling" support for AI agents to securely query and manipulate torrents.

## Limitations
- **Security Dependency**: Requires careful network configuration (VPN, Killswitch, Proxy) for privacy-conscious users using tools like [Gluetun](https://github.com/qdm12/gluetun).
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
The Web API (v2) is the primary method for external interaction.

### Python: Listing Active Torrents
```python
import requests

# Step 1: Login
session = requests.Session()
login_url = "http://localhost:8080/api/v2/auth/login"
session.post(login_url, data={'username': 'admin', 'password': 'password'})

# Step 2: Query Info
info_url = "http://localhost:8080/api/v2/torrents/info"
response = session.get(info_url)
torrents = response.json()

for t in torrents:
    print(f"Torrent: {t['name']}, Progress: {t['progress']*100:.2f}%")
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
- [Ollama](ollama.md) — For running agents that manage qBittorrent downloads.
- [Jackett](jackett.md) — Indexer proxy for multi-tracker search.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Primary agent used for orchestrating acquisition.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — For agentic qBittorrent orchestration.

## Sources / references
- [Official Website](https://www.qbittorrent.org/)
- [qBittorrent GitHub](https://github.com/qbittorrent/qBittorrent)
- [Web API Documentation](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1))
- [qBittorrent v5.2.0 Release Notes](https://github.com/qbittorrent/qBittorrent/releases)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
