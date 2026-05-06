# qBittorrent

## What it is
qBittorrent is a cross-platform, open-source BitTorrent client written in C++. It provides a familiar user interface similar to µTorrent but is entirely free of advertisements and bloatware.

## What problem it solves
It provides a reliable and efficient way to download and share files via the BitTorrent protocol. It centralizes torrent management through a powerful web interface, allowing for headless operation on servers or NAS devices.

## Where it fits in the stack
**Category**: Services / Content Acquisition. It is typically part of the "Automation" and "Data Intake" layer of a homelab media stack.

## Typical use cases
- Downloading Linux ISOs and other large open-source datasets.
- Managing torrents remotely via a web browser.
- Automating downloads using tools like [n8n](n8n.md) or the "Arr" suite.
- Hosting a private seeding box for community-shared content.

## Strengths
- **No Ads**: Completely free and open-source with no bundled software.
- **Web UI**: Excellent, feature-rich web interface that mirrors the desktop application.
- **Search Engine**: Integrated search engine for finding torrents across multiple sites.
- **Resource Efficient**: Low CPU and memory footprint compared to many other clients.

## Limitations
- **Security**: Requires careful configuration (VPN/Proxy) for private operation.
- **UI Design**: The interface is functional but may feel dated to some users.

## When to use it
- When you need a reliable, lightweight BitTorrent client with a web interface.
- When you want to manage torrents remotely via a browser or API.
- When you require features like RSS feed support, a download scheduler, and sequential downloading.

## When not to use it
- When you need a client for a protocol other than BitTorrent.
- When you prefer a client with a more modern, single-page application UI (though qBittorrent's UI is very functional).

## Getting started

### Docker
The recommended way to run qBittorrent is using the LinuxServer.io image:

```bash
docker run -d \
  --name=qbittorrent \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -e WEBUI_PORT=8080 \
  -p 8080:8080 \
  -p 6881:6881 \
  -p 6881:6881/udp \
  -v /path/to/appdata/config:/config \
  -v /path/to/downloads:/downloads \
  --restart unless-stopped \
  lscr.io/linuxserver/qbittorrent:latest
```

Access the web interface at `http://localhost:8080`. The default credentials (if not printed to the log) are often `admin` / `adminadmin`.

### Hello World
1. Run the Docker command to start qBittorrent.
2. Navigate to `http://localhost:8080` and log in.
3. Go to **Tools > Options > BitTorrent** and enable "Add torrents in Paused state" for safety.
4. Click the **Add Torrent Link** button and paste a legal magnet link (e.g., a Linux ISO) to see the client in action.

## CLI examples
The `qbittorrent-nox` binary can be managed via the Docker container.

```bash
# View container logs to find the temporary WebUI password
docker logs qbittorrent

# Check the version of qBittorrent running in the container
docker exec qbittorrent qbittorrent-nox --version

# Pause all active torrents
docker exec qbittorrent qbittorrent-nox --pause-all
```

## API examples
The Web UI API (v2) allows for remote torrent management.

### Python Example
Using the `qbittorrent-api` library is recommended for Python.

```python
from qbittorrentapi import Client

conn_info = dict(host='localhost', port=8080, username='admin', password='your_password')
qbt_client = Client(**conn_info)

# List all torrents
for torrent in qbt_client.torrents_info():
    print(f"Torrent: {torrent.name}, Progress: {torrent.progress*100:.2f}%")
```

### Curl Example
First, authenticate to get a session cookie:

```bash
# Login and save the session cookie
curl -i --header "Referer: http://localhost:8080" \
     --data "username=admin&password=your_password" \
     "http://localhost:8080/api/v2/auth/login"

# List all torrents (requires SID cookie from previous response)
curl "http://localhost:8080/api/v2/torrents/info" \
     --cookie "SID=<your_session_id>"
```

## Related tools / concepts
- [n8n](n8n.md) (For automation)
- [Docker](../tools/infrastructure/docker.md)
- [SearXNG](searXNG.md) (For finding content)
- [Plex](plex.md) (For media consumption)
- [TrueNAS](../../architecture/infrastructure.md) (Storage backend)

## Licensing and cost
- **Open Source**: Yes (GPL-2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Sources / References
- [Official Website](https://www.qbittorrent.org/)
- [Transmission](https://transmissionbt.com/)
- [Deluge](https://deluge-torrent.org/)

## Backlog
- Setup WireGuard VPN killswitch for the qBittorrent container.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-05
