# Jellyfin

## What it is

Jellyfin is a free and open-source media server software that allows you to organize, manage, and stream your digital media (movies, TV shows, music, and photos) to various devices. It is a volunteer-built project that originated as a fork of Emby.

## What problem it solves

Commercial media services often come with subscription fees, tracking, and limited control over your own metadata. Jellyfin provides a completely free, private alternative that lets you host your own media collection on your own hardware, ensuring you have full ownership and control over how your media is consumed and shared.

## Where it fits in the stack

**Category**: Service / Media Management. It sits in the **media distribution and consumption** layer, serving as the front-end interface for users to access large libraries of video and audio stored on local disks or NAS devices.

## Typical use cases

- **Personal Netflix**: Hosting a private collection of movies and TV shows for streaming to smart TVs and mobile devices.
- **Home Music Server**: Streaming high-fidelity music collections (FLAC, MP3) throughout the home.
- **Live TV & DVR**: Integrating with tuners to watch and record live television.
- **Photo Archival**: Organizing and viewing family photo and video archives.

## Strengths

- **Truly Open Source**: No "premium" features hidden behind a paywall (unlike Plex or Emby).
- **Privacy Focused**: No central tracking or phone-home requirements; all data stays on your server.
- **Hardware Acceleration**: Supports a wide range of hardware transcoding options (Intel QuickSync, NVENC, AMF).
- **Customizable**: Extensive support for themes, plugins, and custom CSS for the web interface.

## Limitations

- **Client App Availability**: While improving, native apps for some older smart TV platforms may be less polished or unavailable compared to Plex.
- **Setup Complexity**: Requires more manual configuration for remote access (e.g., setting up a reverse proxy) compared to commercial alternatives.
- **No Cloud-Link**: Does not offer a simplified cloud-based relay for remote streaming without manual port forwarding or VPN.

## When to use it

- When you want a completely open-source, self-hosted media server with no tracking or subscription fees.
- For users who value privacy and want full control over their media collection and metadata.
- To stream your own collection of movies, TV shows, and music to various devices.

## When not to use it

- If you require out-of-the-box support for a very wide range of proprietary smart TV platforms (Plex often has better native app availability).
- If you prefer a managed, cloud-hosted solution with minimal server maintenance.

## Getting started

### Docker installation
The most common way to run Jellyfin is via Docker. Replace placeholders with your actual paths.

```bash
docker run -d \
 --name jellyfin \
 --user 1000:1000 \
 --net=host \
 --volume /path/to/config:/config \
 --volume /path/to/cache:/cache \
 --mount type=bind,source=/path/to/media,target=/media \
 --restart=unless-stopped \
 jellyfin/jellyfin
```

Jellyfin will be available at `http://localhost:8096`.

### Hardware Acceleration (Transcoding)

To enable hardware acceleration, you must pass the host's GPU devices into the container and select the correct driver in the Jellyfin Dashboard (Playback > Transcoding).

#### NVIDIA (NVENC)
Requires the `nvidia-container-toolkit` on the host.

```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

#### Intel QuickSync (QSV) / VA-API
Requires mounting the render group devices.

```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin
    devices:
      - /dev/dri/renderD128:/dev/dri/renderD128
      - /dev/dri/card0:/dev/dri/card0
```

### Hello World
1. Start the Jellyfin container using the Docker command above.
2. Open your web browser and navigate to `http://localhost:8096`.
3. Follow the Setup Wizard to create your first user and set your preferred language.
4. Add your first library by selecting the folder you mounted to `/media`.
5. Your media will begin to appear in the dashboard!

## CLI examples

While Jellyfin is primarily managed through its web interface, you can perform some administrative tasks via `docker exec`.

```bash
# Check the version of Jellyfin running in the container
docker exec -it jellyfin /jellyfin/jellyfin --version

# View the last 50 lines of the Jellyfin log
docker logs --tail 50 jellyfin

# Restart the Jellyfin container
docker restart jellyfin
```

## API examples

Jellyfin provides a comprehensive REST API. You'll need an `X-Emby-Token` for most requests, which you can generate by authenticating.

```bash
# Get information about the server
curl -X GET "http://localhost:8096/System/Info/Public"

# List all users on the server (requires an admin token)
curl -H "X-Emby-Token: YOUR_ACCESS_TOKEN" \
     -X GET "http://localhost:8096/Users"

# Get a user's library views (replace {userId} with the actual ID)
curl -H "X-Emby-Token: YOUR_ACCESS_TOKEN" \
     -X GET "http://localhost:8096/Users/{userId}/Views"
```

## Related tools / concepts

- [Plex](plex.md) — the primary proprietary alternative to Jellyfin
- [Navidrome](navidrome.md) — a lightweight, music-focused streaming alternative
- [Audiobookshelf](audiobookshelf.md) — for specialized audiobook and podcast management
- [Tube Archivist](tubearchivist.md) — for archiving and serving YouTube content within a home theater setup
- [Tailscale](tailscale.md) — for secure remote access to your Jellyfin server without port forwarding
- [Radarr/Sonarr](https://servarr.com/) — for automating the collection management that Jellyfin serves

### Gelli (Android Music)
[Gelli](https://github.com/dkanada/gelli) is a native Android music player for Jellyfin. It provides a more music-centric interface compared to the main Jellyfin app, supporting offline downloads and Android Auto.

1. **Install Gelli**: Download the APK from the [GitHub releases](https://github.com/dkanada/gelli/releases) or F-Droid.
2. **Connect**: Enter your Jellyfin server URL and login credentials.
3. **Usage**: Browse your music library, create playlists, and download tracks for offline listening.

## Sources / References

- [Official Website](https://jellyfin.org/)
- [Jellyfin Docker Documentation](https://jellyfin.org/docs/general/installation/container)
- [Jellyfin API Documentation](https://api.jellyfin.org/)
- [Plex](https://www.plex.tv/)
- [Emby](https://emby.media/)

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Contribution Metadata

- Last reviewed: 2026-06-25
- Confidence: high
