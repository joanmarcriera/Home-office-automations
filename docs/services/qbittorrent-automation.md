# qBittorrent Automation

## What it is
qBittorrent Automation encompasses the workflows, scripts, and integrations used to manage the lifecycle of torrent downloads autonomously. In June 2026, it leverages the **v5.2** Web API and Model Context Protocol (MCP 3.0) to allow AI agents like Claude 4.8 Opus to orchestrate content acquisition, categorization, and library maintenance.

## What problem it solves
Manual torrent management is time-consuming and prone to organizational chaos. qBittorrent Automation solves the "acquisition overhead" by automatically ingesting content from RSS feeds, categorizing downloads based on content type, renaming files for media servers, and enforcing seeding rules to maintain private tracker ratios without human intervention.

## Where it fits in the stack
**Category**: Service / Media / Automation. It sits at the **intake orchestration layer**, bridging content discovery (via [SearXNG](searXNG.md) or RSS) with media consumption ([Plex](plex.md), [Jellyfin](jellyfin.md)).

## Typical use cases
- **Agentic Content Retrieval**: Asking an AI agent to "Find and download the latest Debian ISO," which it executes via the qBittorrent API.
- **Automated Library Maintenance**: Using [n8n](n8n.md) to move completed downloads to specific folders and trigger a media library scan.
- **Ratio Management**: Automatically pausing or deleting torrents once they reach a predefined seeding ratio or time limit.
- **Real-Time Notifications**: Sending alerts to [Element](element.md) or [Synapse](synapse.md) when a high-priority download completes.
- **Dynamic Bandwidth Scaling**: Automatically adjusting download speeds based on home network occupancy or [Speedtest](speedtest.md) results.

## Strengths
- **Native MCP 3.0 Support**: Allows autonomous agents to securely query and manipulate the download queue.
- **Comprehensive Web API**: Provides granular control over every aspect of the client, from peer management to transfer settings.
- **Event-Driven Triggers**: Native support for running external programs on torrent completion.
- **Category-Level Logic**: v5.2+ allows for different automation rules (seeding, pathing) based on assigned categories.
- **Extensive Tooling**: Large ecosystem of Python wrappers (`qbittorrent-api`) and automation nodes (n8n, Node-RED).

## Limitations
- **Security Complexity**: Exposing the Web API for automation requires robust authentication (e.g., via [Authentik](authentik.md)).
- **Configuration Overhead**: Setting up complex "If-This-Then-That" workflows can require significant initial effort.
- **Path Mapping**: Ensuring Docker container paths align across multiple services (qBittorrent, n8n, Plex) is a common point of friction.

## When to use it
- When you want a "set-and-forget" media and data acquisition pipeline.
- To manage complex seeding requirements for multiple private trackers simultaneously.
- When integrating content acquisition into a larger AI-driven homelab orchestration.
- To maintain a highly organized media library without manual file moving.

## When not to use it
- If you only download occasional files manually and don't mind manual organization.
- In environments where the security of the Web API cannot be guaranteed.

## Licensing and cost
- **Licensing**: Open Source (GPL-2.0 for qBittorrent; scripts/wrappers vary).
- **Cost**: Free.
- **Self-hostable**: Yes, typically run alongside [qBittorrent](qbittorrent.md) in a Docker environment.

## Getting started

### Prerequisites
1. A running [qBittorrent](qbittorrent.md) instance with Web UI enabled.
2. An automation engine like [n8n](n8n.md) or a Python environment.

### Hello World (n8n Webhook)
1. In qBittorrent, go to **Options > Downloads > Run external program on torrent completion**.
2. Set the command to trigger an n8n webhook:
   `curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"%N\", \"hash\": \"%I\"}" http://n8n:5678/webhook/torrent-done`
3. In n8n, create a workflow that sends a notification when this webhook is called.

## CLI examples
Automate qBittorrent via `curl` and the Web API.

```bash
# Login and save session SID
curl -i -d "username=admin&password=your_password" http://localhost:8080/api/v2/auth/login

# Add a torrent with a specific category
curl -b "SID=YOUR_SID" -F "urls=magnet:?xt=urn:btih:..." -F "category=ISO" http://localhost:8080/api/v2/torrents/add

# Pause all torrents in the 'Movies' category
curl -b "SID=YOUR_SID" -X POST "http://localhost:8080/api/v2/torrents/pause?category=Movies"
```

## API examples
Use the `qbittorrent-api` Python library for advanced automation.

### Python: Automated Cleanup Script
```python
import qbittorrentapi

qbt_client = qbittorrentapi.Client(host='localhost', port=8080, username='admin', password='password')

# Delete torrents that have finished seeding (Ratio > 2.0)
for torrent in qbt_client.torrents_info(status_filter='completed'):
    if torrent.ratio > 2.0:
        print(f"Cleaning up: {torrent.name}")
        torrent.delete(delete_files=False) # Keep files, remove from client
```

## Related tools / concepts
- [qBittorrent](qbittorrent.md) — The core download engine.
- [n8n](n8n.md) — The primary workflow engine for qBittorrent automation.
- [SearXNG](searXNG.md) — For programmatically finding content.
- [Plex](plex.md) — Media consumption platform.
- [Jellyfin](jellyfin.md) — Open-source media server.
- [Authentik](authentik.md) — Securing the Web API.
- [Tailscale](tailscale.md) — Secure remote access to the API.
- [Speedtest](speedtest.md) — Providing metrics for bandwidth automation.
- [Element](element.md) — Notification endpoint.
- [Synapse](synapse.md) — Matrix-based notification backbone.
- [Paperless-ngx](paperless-ngx.md) — Automated ingestion of downloaded documents.
- [Claude](../tools/ai_knowledge/claude.md) — Agent used for orchestrating acquisition.

## Sources / References
- [qBittorrent WebUI API](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1))
- [qbittorrent-api Python Library](https://github.com/rmartin16/qbittorrent-api)
- [Arrr Suite (Sonarr/Radarr)](https://wiki.servarr.com/)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
