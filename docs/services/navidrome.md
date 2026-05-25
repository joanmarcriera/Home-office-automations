# Navidrome

## What it is
Navidrome is a modern self-hosted music server and streamer. It indexes a local music library, serves it through a responsive web UI, and exposes a Subsonic-compatible API for mobile and desktop music clients. It is a high-performance music server that allows you to listen to your music collection from any device. It is lightweight enough for small home servers but still supports multi-user libraries, transcoding through `ffmpeg`, playlists, album art, and external clients.

## What problem it solves
It turns a folder of owned audio files into a private streaming service. That avoids relying on commercial music subscriptions for personal collections, lets a household keep music available on the LAN/VPN, and gives automation scripts a stable API for library checks.

## Where it fits in the stack
Navidrome belongs in the **media services** layer alongside Jellyfin and Audiobookshelf. In a home-office setup, it is usually deployed behind a reverse proxy, backed up with the rest of `/data`, and pointed at read-only music storage.

## Typical use cases
- Stream a FLAC/MP3 library to browsers, phones, and Subsonic-compatible clients.
- Maintain family accounts with separate favorites, playlists, and playback state.
- Keep a low-resource music service separate from a heavier video server.
- Expose a music library over Tailscale or a private VPN without publishing file shares.

## Strengths
- **Small operational footprint**: Simple single-binary or single-container deployment.
- **Client compatibility**: Works with many Subsonic-compatible apps.
- **Read-only media mounts**: Easy to keep the app from modifying source music files.
- **Good homelab fit**: Configuration can be managed through a TOML file or environment variables.

## Limitations
- **Music-focused**: It is not a full video/photo media platform.
- **Metadata-dependent**: Poor tags lead to poor browsing results.
- **Transcoding dependency**: `ffmpeg` must be available for some formats and clients.

## When to use it
- When you have a large collection of owned music files and want to stream them like Spotify.
- For a lightweight music server that runs on modest hardware (e.g., Raspberry Pi).
- When you want to use third-party mobile apps like Ample, DSub, or Play:Sub.
- To maintain privacy by keeping your listening habits and music files on your own hardware.

## When not to use it
Do not use Navidrome as a general media server for video, live TV, or photo libraries; use Jellyfin or Plex for those workloads. If you need audiobook-specific progress handling, chapter metadata, and podcast-style feeds, prefer Audiobookshelf.

## Getting started

### Docker Compose quick start
Create a data directory and point the music mount at an existing local music folder:

```bash
mkdir -p ./navidrome-data ./music
cat > docker-compose.yml <<'YAML'
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
YAML
docker compose up -d
```

Open `http://localhost:4533`, create the first admin user, and trigger or wait for the initial library scan.

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
Navidrome supports the Subsonic API. A basic ping request verifies that API authentication and the server endpoint are working:

```bash
: "${NAVIDROME_USER:?set NAVIDROME_USER to a Navidrome user}"
: "${NAVIDROME_PASSWORD:?set NAVIDROME_PASSWORD to that user's password}"
curl "http://localhost:4533/rest/ping.view?u=$NAVIDROME_USER&p=$NAVIDROME_PASSWORD&v=1.16.1&c=home-office&f=json"
```

Python health check using token authentication:

```python
import hashlib
import secrets
import urllib.parse
import os
import urllib.request

base_url = os.environ.get("NAVIDROME_URL", "http://localhost:4533")
username = os.environ["NAVIDROME_USER"]
password = os.environ["NAVIDROME_PASSWORD"]
salt = secrets.token_hex(6)
token = hashlib.md5(f"{password}{salt}".encode()).hexdigest()
query = urllib.parse.urlencode({
    "u": username,
    "t": token,
    "s": salt,
    "v": "1.16.1",
    "c": "home-office-check",
    "f": "json",
})
with urllib.request.urlopen(f"{base_url}/rest/ping.view?{query}", timeout=10) as response:
    print(response.read().decode())
```

### Advanced: Automated Playlist Management (Python)
This script demonstrates how to search for tracks by a specific genre and create/update a playlist. This pattern is useful for local agents that curate music based on external triggers (e.g., weather or time of day).

```python
import requests
import hashlib
import secrets

# Configuration
BASE_URL = "http://localhost:4533/rest"
USER = "admin"
PASS = "password"
CLIENT_ID = "playlist-bot"

def get_auth_params():
    salt = secrets.token_hex(6)
    token = hashlib.md5(f"{PASS}{salt}".encode()).hexdigest()
    return {"u": USER, "t": token, "s": salt, "v": "1.16.1", "c": CLIENT_ID, "f": "json"}

def search_tracks(query):
    params = get_auth_params()
    params["query"] = query
    res = requests.get(f"{BASE_URL}/search3.view", params=params)
    return res.json().get("subsonic-response", {}).get("searchResult3", {}).get("song", [])

def update_playlist(playlist_name, song_ids):
    params = get_auth_params()
    # 1. Get playlist ID
    res = requests.get(f"{BASE_URL}/getPlaylists.view", params=params)
    playlists = res.json().get("subsonic-response", {}).get("playlists", {}).get("playlist", [])
    playlist = next((p for p in playlists if p["name"] == playlist_name), None)

    if not playlist:
        # Create if not exists
        params["name"] = playlist_name
        params["songId"] = song_ids
        requests.get(f"{BASE_URL}/createPlaylist.view", params=params)
    else:
        # Update existing
        pid = playlist["id"]
        params["playlistId"] = pid
        params["songIdToAdd"] = song_ids
        requests.get(f"{BASE_URL}/updatePlaylist.view", params=params)

# Example: Create a "Jazz Morning" playlist from recent additions
songs = search_tracks("genre:Jazz")
ids = [s["id"] for s in songs[:10]]
if ids:
    update_playlist("Jazz Morning", ids)
    print(f"Updated 'Jazz Morning' with {len(ids)} tracks.")
```

## Troubleshooting
- If the UI starts but no albums appear, verify Linux permissions with `ls -n ./music` and make the Compose `user` match the folder owner.
- If remote clients cannot connect, confirm port `4533` is reachable through the firewall, VPN, or reverse proxy.
- If some files do not play, install or expose `ffmpeg` and check whether the client requires transcoding for that format.
- If playlists are missing, create the admin user first, then touch `.m3u` files or trigger a rescan.

## Links
- [Official Website](https://www.navidrome.org/)
- [GitHub Repository](https://github.com/navidrome/navidrome)
- [Installation Docs](https://www.navidrome.org/docs/installation/)
- [Getting Started Docs](https://www.navidrome.org/docs/getting-started/)

## Related tools / concepts
- [Audiobookshelf](audiobookshelf.md) — For specialized audiobook and podcast management.
- [Airsonic](https://airsonic.github.io/)
- [Jellyfin](jellyfin.md)
- [Plex](plex.md)
- [Beets](https://beets.io/)
- [Lidarr](https://lidarr.audio/)
- [MusicBrainz](https://musicbrainz.org/)
- [Subsonic API](http://www.subsonic.org/pages/api.jsp)

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Sources / References
- https://www.navidrome.org/
- https://www.navidrome.org/docs/installation/
- https://www.navidrome.org/docs/getting-started/
- https://github.com/navidrome/navidrome
- https://airsonic.github.io/

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15
