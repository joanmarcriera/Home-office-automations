# qBittorrent

qBittorrent is an open-source BitTorrent client.

## Description
It aims to be an open-source alternative to µTorrent. It is fast, stable, and provides a feature-rich web interface.

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

## CLI examples

You can manage the qBittorrent container using standard Docker commands:

```bash
# View container logs to find the temporary WebUI password
docker logs qbittorrent

# Restart the qBittorrent service
docker restart qbittorrent

# Check the version of qBittorrent running in the container
docker exec qbittorrent qbittorrent-nox --version
```

## API examples

qBittorrent provides a Web UI API. First, authenticate to get a session cookie:

```bash
# Login and save the session cookie
curl -i --header "Referer: http://localhost:8080" \
     --data "username=admin&password=your_password" \
     "http://localhost:8080/api/v2/auth/login"
```

Once authenticated, use the cookie (SID) for subsequent requests:

```bash
# List all torrents (requires SID cookie)
curl "http://localhost:8080/api/v2/torrents/info" \
     --cookie "SID=<your_session_id>"
```

## Links
- [Official Website](https://www.qbittorrent.org/)

## Alternatives
- [Transmission](https://transmissionbt.com/)
- [Deluge](https://deluge-torrent.org/)

## Backlog
- Setup WireGuard VPN killswitch for the qBittorrent container.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://www.qbittorrent.org/
- https://transmissionbt.com/
- https://deluge-torrent.org/
