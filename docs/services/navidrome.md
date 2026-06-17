# Navidrome

## What it is
Navidrome is a modern self-hosted music server and streamer. It indexes a local music library, serves it through a responsive web UI, and exposes a Subsonic-compatible API for mobile and desktop music clients. As of June 2026, it is the industry standard for lightweight, high-performance music streaming in personal homelabs.

## What problem it solves
It turns a folder of owned audio files into a private streaming service. This avoids reliance on commercial music subscriptions, ensures your personal collection remains available offline or over a private VPN (like [Tailscale](tailscale.md)), and provides automation scripts with a stable API for library management and scrobbling.

## Where it fits in the stack
Navidrome belongs in the **Media Services** layer alongside [Jellyfin](jellyfin.md) and [Audiobookshelf](audiobookshelf.md). In a home-office setup, it is typically deployed behind a reverse proxy, backed up to secure storage, and pointed at read-only music datasets to prevent accidental modification of source files.

## Typical use cases
- **Personal Spotify**: Streaming a FLAC/MP3 library to browsers, phones, and desktop clients.
- **Family Accounts**: Maintaining separate favorites, playlists, and playback states for multiple users.
- **Low-Resource Streaming**: Running a music service on modest hardware (like a Raspberry Pi) where heavier servers fail.
- **Remote Access**: Listening to your collection over [Tailscale](tailscale.md) without exposing file shares to the internet.

## Strengths
- **Small operational footprint**: Simple single-binary or single-container deployment with minimal RAM usage.
- **Broad Compatibility**: Works with dozens of Subsonic-compatible apps (Ample, DSub, Play:Sub).
- **Read-only media mounts**: Ensures your curated music library remains untouched by the application.
- **Native Transcoding**: Uses `ffmpeg` to serve high-quality audio to bandwidth-constrained mobile devices.
- **Plugin System (2026)**: Supports community add-ons like AudioMuse-AI for prompt-based playlist generation.

## Limitations
- **Music-focused**: It is not designed for video, photo, or live TV libraries (use [Jellyfin](jellyfin.md)).
- **Metadata-dependent**: Requires well-tagged files for a good browsing experience.
- **No Native Chapter Support**: For audiobooks and podcasts, [Audiobookshelf](audiobookshelf.md) is the preferred choice.

## When to use it
- When you have a large collection of owned music files and want a private, Spotify-like experience.
- For a lightweight music server that runs efficiently on modest hardware.
- When you want to use third-party mobile apps with a stable, well-documented API.
- To maintain privacy by keeping your listening habits and files on your own hardware.

## When not to use it
- For general media hosting (video/photos); use [Jellyfin](jellyfin.md) or [Plex](plex.md).
- If you require specific audiobook features like chapter-level navigation and narrator metadata; use [Audiobookshelf](audiobookshelf.md).
- If you strictly stream from commercial services and do not own physical or digital music files.

## Getting started

### Docker Compose
Create a data directory and point the music mount at your local music folder:

```yaml
services:
  navidrome:
    image: ghcr.io/navidrome/navidrome:latest
    container_name: navidrome
    user: "1000:1000"
    ports:
      - "4533:4533"
    restart: unless-stopped
    environment:
      ND_SCANSCHEDULE: "1h"
      ND_LOGLEVEL: "info"
      ND_SESSIONTIMEOUT: "24h"
    volumes:
      - ./navidrome-data:/data
      - ./music:/music:ro
```

Open `http://localhost:4533`, create the first admin user, and the initial library scan will begin.

### Minimal configuration file
For non-container installs, a minimal `navidrome.toml` can be:

```toml
MusicFolder = "/srv/media/music"
DataFolder = "/var/lib/navidrome"
Address = "0.0.0.0"
Port = 4533
ScanSchedule = "1h"
LogLevel = "info"
```

## CLI examples

```bash
# Follow startup and scan logs for the container
docker logs -f navidrome

# Confirm the web UI is listening on the default port
curl -I http://localhost:4533

# Check that the container can see mounted music files
docker exec navidrome find /music -maxdepth 2 -type f | head
```

## API examples
Navidrome supports the Subsonic API. A basic ping request verifies authentication:

```bash
curl "http://localhost:4533/rest/ping.view?u=USER&p=PASS&v=1.16.1&c=home-office&f=json"
```

### Automated Playlist Management (Python)
This pattern is useful for local agents that curate music based on external triggers (e.g., weather or time of day) via [n8n](n8n.md).

```python
import requests
import hashlib
import secrets

BASE_URL = "http://localhost:4533/rest"
USER = "admin"
PASS = "password"

def get_auth():
    salt = secrets.token_hex(6)
    token = hashlib.md5(f"{PASS}{salt}".encode()).hexdigest()
    return {"u": USER, "t": token, "s": salt, "v": "1.16.1", "c": "agent-bot", "f": "json"}

# Example: Search for Jazz tracks
params = get_auth()
params["query"] = "genre:Jazz"
res = requests.get(f"{BASE_URL}/search3.view", params=params)
songs = res.json().get("subsonic-response", {}).get("searchResult3", {}).get("song", [])
print(f"Found {len(songs)} Jazz tracks.")
```

## Troubleshooting
- If the UI starts but no albums appear, verify Linux permissions with `ls -n ./music` and make the Compose `user` match the folder owner.
- If remote clients cannot connect, confirm port `4533` is reachable through the firewall, VPN, or reverse proxy.
- If some files do not play, install or expose `ffmpeg` and check whether the client requires transcoding for that format.
- If playlists are missing, create the admin user first, then touch `.m3u` files or trigger a rescan.

## Related tools / concepts
- [Audiobookshelf](audiobookshelf.md) — For specialized audiobook and podcast management.
- [Jellyfin](jellyfin.md) — For video and photo media libraries.
- [Plex](plex.md) — Proprietary alternative for general media hosting.
- [Tailscale](tailscale.md) — For secure remote access to your music server.
- [n8n](n8n.md) — For automating library updates and scrobbling notifications.
- [Ollama](ollama.md) — For AI-powered sonic analysis and playlist generation via plugins.
- [Homebox](homebox.md) — For inventory management of physical media collections.
- [Authentik](authentik.md) — For managing multi-user access via OIDC.

## Sources / references
- [Official Website](https://www.navidrome.org/)
- [GitHub Repository](https://github.com/navidrome/navidrome)
- [Navidrome Documentation](https://www.navidrome.org/docs/)
- [Subsonic API Specification](http://www.subsonic.org/pages/api.jsp)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
