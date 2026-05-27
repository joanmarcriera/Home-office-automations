# qBittorrent Automation

Automated workflows for managing torrent downloads, post-processing, and library maintenance.

## What it is
qBittorrent Automation involves using the qBittorrent Web UI API, external scripts, and automation platforms like n8n to manage the lifecycle of downloads.

## What problem it solves
It automates the tedious parts of media acquisition: starting downloads from RSS feeds, categorizing files based on content, renaming files for media centers (like Plex or Jellyfin), and managing disk space by automatically removing old torrents.

## Where it fits in the stack
**Category**: Services / Media Automation. It sits between content discovery (RSS/Indexers) and media consumption (Plex).

## Typical use cases
- **RSS Auto-DL**: Automatically downloading new episodes of TV shows via RSS.
- **Categorization & Sorting**: Moving completed downloads to specific folders based on their "Category" tag.
- **Notifications**: Using [n8n](n8n.md) to send a Telegram or Element notification when a large download completes.
- **Bandwidth Scheduling**: Automatically pausing or slowing down downloads during business hours.
- **Seed Management**: Automating the cleanup of completed downloads based on share ratios or seeding time.

## Strengths
- **Robust Web API**: Excellent documentation and coverage for almost all client features.
- **Python Libraries**: Multiple well-maintained wrappers (e.g., `qbittorrent-api`).
- **Low Overhead**: Automation scripts can run as lightweight cron jobs or n8n nodes.
- **Category-Level Limits**: As of v5.2 (May 2026), seeding limits can be enforced at the category level, allowing for automated rule sets (e.g., "Public" torrents stop at 2.0 ratio, while "Private" ones seed indefinitely).

## Limitations
- **Security**: The Web UI API must be secured behind a strong password or VPN.
- **Complexity**: Setting up complex "If This Then That" logic (e.g., cross-seeding) can require significant scripting.

## When to use it
- When you want a "set it and forget it" media stack.
- To manage a large number of torrents across multiple categories.
- When integrating your download client with other homelab services.

## When not to use it
- If you only download occasional files manually.
- If you don't have enough storage to handle automated "fire and forget" downloads.

## Getting started

### Prerequisites
- A running [qBittorrent](qbittorrent.md) instance.
- Web UI enabled in **Tools > Options > Web UI**.

### Basic Python Setup
Install the `qbittorrent-api` library:

```bash
pip install qbittorrent-api
```

### Hello World (Python)
```python
import qbittorrentapi

# Connect to the client
qbt_client = qbittorrentapi.Client(
    host='localhost',
    port=8080,
    username='admin',
    password='your_password'
)

# List all downloading torrents
for torrent in qbt_client.torrents_info(status_filter='downloading'):
    print(f"{torrent.name} - {torrent.progress * 100:.2f}%")
```

## CLI examples

Automation often uses `curl` to interact with the Web UI API directly.

```bash
# Login and get a SID cookie (needed for subsequent requests)
curl -i -d "username=admin&password=your_password" http://localhost:8080/api/v2/auth/login

# Add a torrent via Magnet link
curl -b "SID=YOUR_SID" -d "urls=magnet:?xt=urn:btih:..." http://localhost:8080/api/v2/torrents/add

# Pause all active torrents
curl -b "SID=YOUR_SID" -X POST http://localhost:8080/api/v2/torrents/pause?hashes=all
```

## API examples

### n8n Integration (Webhook)
You can configure qBittorrent to trigger an n8n webhook when a download finishes. In qBittorrent, go to **Options > Downloads > Run external program on torrent completion**:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"%N\", \"size\": \"%Z\", \"path\": \"%R\"}" http://n8n-server:5678/webhook/torrent-finished
```

### Advanced Filtering (Python)
```python
# Remove torrents that have been seeding for more than 7 days
for torrent in qbt_client.torrents_info(status_filter='seeding'):
    if torrent.seeding_time > (7 * 24 * 3600):
        print(f"Removing old seed: {torrent.name}")
        torrent.delete(delete_files=True)

# Automate Category-Level Limits (v5.2 Feature)
# Set a 2.0 ratio limit for the "Linux-ISOs" category
qbt_client.torrents_set_share_limits(
    category='Linux-ISOs',
    ratio_limit=2.0,
    seeding_time_limit=-1 # No time limit
)
```

## Related tools / concepts
- [qBittorrent](qbittorrent.md) — The core client.
- [Jellyfin](jellyfin.md) — Open-source media server for consuming automated downloads.
- [Plex](plex.md) — Alternative media consumer.
- [n8n](n8n.md) — Workflow engine for complex "If-This-Then-That" scenarios.
- [Rclone Automation](rclone-automation.md) — For moving files to cloud storage after download.
- [SearXNG](searXNG.md) — Can be used to programmatically find torrent links.
- [Authentik](authentik.md) — For managing secure access to the qBittorrent Web UI.
- [Tailscale](tailscale.md) — For secure remote access to automation triggers.
- [Arrr Suite (Sonarr/Radarr)](https://wiki.servarr.com/) — Dedicated media automation stacks.

## Sources / References
- [qBittorrent Web UI API Documentation](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1))
- [qbittorrent-api Python Wrapper](https://github.com/rmartin16/qbittorrent-api)

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-27
