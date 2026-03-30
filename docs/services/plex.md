# Plex

Plex is a global streaming media service and a media player platform that organizes your video, music, and photos from your personal libraries and streams them to all your devices.

## Description
While it is not fully open-source, Plex is one of the most popular and feature-rich media server solutions. It consists of the Plex Media Server, which hosts your content, and various Plex apps that allow you to play that content on smart TVs, mobile devices, and web browsers.

## When to use it
- When you want a polished, user-friendly interface for managing and streaming your personal media collection.
- To access your media library remotely from anywhere in the world.
- When you want to share your media library with friends or family members.
- If you value features like automatic metadata fetching, transcode support, and cross-platform compatibility.

## When not to use it
- If you strictly require 100% open-source software (consider [Jellyfin](jellyfin.md)).
- If you don't want to rely on a central authentication server (Plex requires an account on plex.tv for most features).
- In environments with no internet access (Plex can be configured for offline use, but it is not its primary design).

## Links
- [Official Website](https://www.plex.tv/)
- [Plex Media Server Downloads](https://www.plex.tv/media-server-downloads/)
- [Plex Support Articles](https://support.plex.tv/articles/)

## Alternatives
- [Jellyfin](jellyfin.md) (Fully open-source)
- [Emby](https://emby.media/) (Proprietary, but often seen as a middle ground)
- [Kodi](https://kodi.tv/) (Local playback focused)

## Getting started

### Docker installation
The most common way to host Plex is via Docker. You will need a [Plex Claim Token](https://www.plex.tv/claim/) to associate the server with your account.

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

Access the web interface at `http://localhost:32400/web`.

### Hello World
1. Start the Plex Docker container.
2. Open `http://localhost:32400/web` in your browser and sign in.
3. Follow the setup wizard to name your server.
4. Click **Add Library**, choose **Movies**, and point it to the `/data/movies` directory.
5. Add a single movie file to that directory and watch Plex automatically fetch the poster and metadata.

## CLI examples

Plex provides the `Plex Media Scanner` for command-line library management. In a Docker environment, you execute it within the container.

```bash
# List all configured library sections
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --list

# Scan a specific library section to find new files (replace <id> with the section number)
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --scan --section <id>

# Update metadata for all items in a specific library
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --refresh --section <id>
```

## API examples

Plex exposes a REST API on port 32400. You need a `X-Plex-Token` for most requests.

### Get Server Identity and Version
```bash
curl -X GET "http://localhost:32400/identity"
```

### List All Libraries (Sections)
```bash
curl -X GET "http://localhost:32400/library/sections?X-Plex-Token=YOUR_PLEX_TOKEN"
```

### Python Example (using plexapi)
The `plexapi` library is the recommended way to interact with Plex via Python.

```python
from plexapi.server import PlexServer

baseurl = 'http://localhost:32400'
token = 'YOUR_PLEX_TOKEN'
plex = PlexServer(baseurl, token)

for section in plex.library.sections():
    print(f"Library: {section.title}, Type: {section.type}")
```

## Backlog
- Configure Plex Meta Manager for automated collection management.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-02

## Sources / References
- https://www.plex.tv/
- https://emby.media/
- https://support.plex.tv/articles/201242707-plex-media-scanner-via-command-line/
- https://docs.linuxserver.io/images/docker-plex/
