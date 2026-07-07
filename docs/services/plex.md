# Plex

Plex is a global streaming media service and a media player platform that organizes your video, music, and photos from your personal libraries and streams them to all your devices.

## What it is
Plex is a proprietary media server application that provides a centralized, Netflix-like interface for your personal media collection. As of **July 2026**, it continues to be the industry leader for home media streaming, offering advanced features like hardware-accelerated transcoding, robust remote access, and the highly-regarded **Plexamp** music player. In mid-2026, Plex introduced enhanced support for **MCP 3.0** via the **Plex Agentic Bridge**, allowing AI agents to query library state and initiate playback across the network.

## What problem it solves
It centralizes fragmented media collections (movies, TV shows, music, photos) and ensures they are playable on any device, anywhere in the world. It automatically fetches posters, metadata, and subtitles, handles on-the-fly video transcoding for low-bandwidth connections, and provides secure sharing capabilities for friends and family, eliminating the complexity of manual file management and format conversion.

## Where it fits in the stack
Plex serves as the **Media Consumption and Streaming hub** in a homelab ecosystem. It typically sits at the top of the media stack, consuming content processed and archived by tools like [Jackett](jackett.md), [qbittorrent](qbittorrent.md), and [Tube Archivist](tubearchivist.md).

## Typical use cases
- Streaming high-definition movies and TV shows to smart TVs, consoles, and mobile devices.
- Hosting a private, high-fidelity music library with the **Plexamp** application.
- Sharing curated media libraries with remote family members.
- Automatically organizing local media files with professional-grade metadata and trailers.
- Using **Plex Meta Manager (PMM)** to automate collection management and dynamic overlays.

## Strengths
- **Polished User Experience**: Best-in-class UI/UX across a wide range of platforms.
- **Hardware Acceleration**: Exceptional support for GPU-accelerated transcoding (NVENC, Intel QuickSync).
- **Device Ecosystem**: Available on almost every smart device, including specialized clients for audio and VR.
- **Ease of Use**: Simplified remote access setup (Plex Relay) and automated metadata matching.
- **Agent Integration**: Native support for **MCP 3.0 Task Protocol** for natural language media selection.

## Limitations
- **Proprietary**: The core server and many advanced features (Plex Pass) are closed-source.
- **Centralized Authentication**: Requires a connection to `plex.tv` for initial setup and most login scenarios.
- **Pricing**: Features like hardware transcoding and offline downloads require a **Plex Pass** subscription (priced at **$749.99 USD** for Lifetime as of July 2026).
- **Privacy**: Higher telemetry and data collection compared to fully open-source alternatives like Jellyfin.

## When to use it
- When you want the most polished and user-friendly interface for managing your media.
- For seamless remote access to your media library without complex VPN or proxy configuration.
- If you value high-quality mobile apps and native smart TV support.
- When sharing your library with non-technical users who expect a "Netflix-like" experience.

## When not to use it
- If you strictly require 100% open-source software (consider [Jellyfin](jellyfin.md)).
- In environments with no internet access (Plex can be configured for offline use, but it is not its primary design).
- If you want to avoid centralized account dependencies and telemetry.

## Getting started

### Docker installation
The recommended way to host Plex is via Docker. You will need a [Plex Claim Token](https://www.plex.tv/claim/) to associate the server with your account.

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
  linuxserver/plex:latest
```

Access the web interface at `http://localhost:32400/web`.

### Hello World
1. Start the container and sign in at `http://localhost:32400/web`.
2. Follow the setup wizard to name your server.
3. Click **Add Library**, choose **Movies**, and point it to `/data/movies`.
4. Add a video file to the directory and watch Plex automatically fetch the metadata.

## CLI examples
In a Docker environment, library management can be handled via the `Plex Media Scanner`:

```bash
# List all configured library sections and their IDs
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --list

# Manually trigger a scan for a specific library (e.g., section ID 1)
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --scan --section 1

# Refresh metadata for all items in a library to pick up new posters or trailers
docker exec -it plex "/usr/lib/plexmediaserver/Plex Media Scanner" --refresh --section 1
```

## API examples
The Plex API (REST on port 32400) allows for advanced automation.

### Python (Get Library Sections)
```python
from plexapi.server import PlexServer

baseurl = 'http://localhost:32400'
token = 'YOUR_PLEX_TOKEN'
plex = PlexServer(baseurl, token)

for section in plex.library.sections():
    print(f"Library Name: {section.title}, Items: {section.totalSize}")
```

### Curl (Check Server Identity)
```bash
curl -X GET "http://localhost:32400/identity"
```

## Related tools / concepts
- [Jellyfin](jellyfin.md) — The primary open-source alternative to Plex.
- [Plex Automation](plex-automation.md) — Scripts and workflows for enhancing your Plex experience.
- [Tube Archivist](tubearchivist.md) — For preserving YouTube content before streaming on Plex.
- [qbittorrent](qbittorrent.md) — For acquiring high-quality media files.
- [n8n](n8n.md) — For automating media ingestion notifications.
- [Tailscale](tailscale.md) — For secure, private remote access without using Plex Relay.
- [Immich](immich.md) — High-performance photo management alternative.
- [Gemma 3](../knowledge_base/models/gemma-3.md) — AI model used for natural language media selection via **MCP 3.0**.
- [Plex Meta Manager](https://metamanager.wiki/) — Advanced metadata and collection automation.

## Sources / References
- [Official Plex Website](https://www.plex.tv/)
- [Plex Media Server Documentation](https://support.plex.tv/articles/)
- [LinuxServer Plex Docker Image](https://docs.linuxserver.io/images/docker-plex/)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-21
