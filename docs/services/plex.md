# Plex

Plex is a global streaming media service and a media player platform.

## Description
It organizes your video, music, and photos from your personal libraries and streams them to all your devices. While it is not fully open-source, it is a highly popular and feature-rich media server solution.

## Links
- [Official Website](https://www.plex.tv/)

## Alternatives
- [Jellyfin](jellyfin.md)
- [Emby](https://emby.media/)

## When to use it
- When you want a highly polished, user-friendly interface for your personal media collection.
- If you need easy remote access (Plex Pass often simplifies this with Relay).
- For a "set it and forget it" experience for non-technical family members.

## When not to use it
- If you strictly require open-source software (Plex is proprietary).
- When you want a solution that doesn't require a central account (Plex.tv).
- If you want full control over every aspect of the metadata and scanning without any external telemetry.

## Getting started

### Docker installation
The most common way to host Plex is via Docker. Replace placeholders with your actual paths and a [Plex Claim Token](https://www.plex.tv/claim/).

```bash
docker run -d \
  --name plex \
  --network=host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ="Etc/UTC" \
  -e PLEX_CLAIM="claim-xxxxxxxxxxxxxx" \
  -v /path/to/plex/config:/config \
  -v /path/to/media/tvshows:/data/tvshows \
  -v /path/to/media/movies:/data/movies \
  --restart unless-stopped \
  linuxserver/plex
```

## CLI examples

Plex provides the `Plex Media Scanner` for command-line library management. On Linux/Docker, you can execute it within the container:

```bash
# List all libraries (sections)
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --list

# Scan a specific library (replace <id> with the section number)
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --scan --section <id>

# Refresh metadata for a specific library
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --refresh --section <id>
```

## API examples

Plex exposes a REST API on port 32400. You need a `X-Plex-Token` for authentication.

### Python Example
```python
import requests

# Replace with your actual server IP and token
base_url = "http://localhost:32400"
headers = {"X-Plex-Token": "YOUR_PLEX_TOKEN"}

# Get all library sections
response = requests.get(f"{base_url}/library/sections", headers=headers)
print(response.text)
```

### Curl Example
```bash
# Get all library sections in XML format
curl -X GET "http://localhost:32400/library/sections?X-Plex-Token=YOUR_PLEX_TOKEN"

# Get server identity and version
curl -X GET "http://localhost:32400/identity"
```

## Related tools / concepts
- [Jellyfin](jellyfin.md)
- [Nextcloud](nextcloud.md)
- [n8n](n8n.md)

## Backlog
- Configure Plex Meta Manager for automated collection management.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://www.plex.tv/
- https://emby.media/
- https://support.plex.tv/articles/201242707-plex-media-scanner-via-command-line/
- https://docs.linuxserver.io/images/docker-plex/
