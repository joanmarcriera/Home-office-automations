# Prowlarr

## What it is
Prowlarr is an indexer manager/proxy built on the popular Arr .net/react stack to integrate with your various PVR apps. Prowlarr supports management of both Torrent Trackers and Usenet Indexers.

## What problem it solves
It centralizes the management of indexers and trackers. Instead of configuring the same 10 indexers in Sonarr, Radarr, Lidarr, and Readarr manually, you configure them once in Prowlarr, and they are automatically synchronized across all your applications.

## Where it fits in the stack
**Category**: Services / Media Management. It sits in the **indexer management layer**, acting as a proxy and synchronization hub between your PVR applications (Sonarr/Radarr) and your media sources (trackers/indexers).

## Typical use cases
- **Centralized Indexer Management**: Adding a new private tracker once and having it available everywhere.
- **Proxying Requests**: Hiding your PVR apps behind a single proxy for indexer requests.
- **Indexer Health Monitoring**: Tracking which indexers are down or failing across your entire stack.

## Strengths
- **Seamless Synchronization**: Automatically pushes indexer configurations to Sonarr, Radarr, Lidarr, and Readarr.
- **Broad Support**: Supports hundreds of Torrent trackers and Usenet indexers.
- **Unified UI**: Consistent interface with other Arr apps.
- **Proxy Support**: Can proxy all indexer requests through a VPN or specific network interface.

## Limitations
- **Arr Ecosystem Focus**: Optimized for the Arr suite; may be less useful if you only use standalone downloaders or alternative PVRs.
- **Resource Usage**: Like other Arr apps, it has a non-trivial RAM footprint compared to lightweight alternatives like Jackett.

## When to use it
- When you use multiple "Arr" applications (Sonarr, Radarr, etc.) and want to centralize indexer management.
- To replace [Jackett](jackett.md) for a more modern, synchronized experience.
- When you want automatic health monitoring and per-app indexer assignment.

## When not to use it
- If you only use a single PVR application and don't mind manual configuration.
- On extremely resource-constrained devices where [Jackett](jackett.md) might be preferred for its slightly lower overhead.

## Getting started

### Docker Compose
```yaml
services:
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
    volumes:
      - /path/to/prowlarr/config:/config
    ports:
      - 9696:9696
    restart: unless-stopped
```

### Hello World
1. Access the UI at `http://localhost:9696`.
2. Go to **Settings > Apps** and add your Sonarr/Radarr instances using their API keys.
3. Go to **Indexers** and add your first tracker or indexer.
4. Watch as the indexer is automatically added to your connected PVR apps!

## CLI examples
Prowlarr is primarily managed via Web UI or API, but you can check logs or restart via Docker:

```bash
# View logs
docker logs -f prowlarr

# Restart service
docker restart prowlarr
```

## API examples
Prowlarr uses a REST API similar to other Arr apps.

```bash
# Get all configured indexers
curl -H "X-Api-Key: YOUR_API_KEY" \
     -X GET "http://localhost:9696/api/v1/indexer"
```

## Related tools / concepts
- [Jackett](jackett.md) — The predecessor and primary alternative.
- [Sonarr](https://sonarr.tv/) — Smart TV show downloader.
- [Radarr](https://radarr.video/) — Movie downloader.
- [Lidarr](https://lidarr.audio/) — Music downloader.
- [Readarr](https://readarr.com/) — Book downloader.
- [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) — Proxy server to bypass Cloudflare protection on some trackers.

## Backlog

## Sources / References
- [Official Website](https://prowlarr.com/)
- [GitHub Repository](https://github.com/Prowlarr/Prowlarr)
- [Wiki Documentation](https://wiki.servarr.com/prowlarr)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
