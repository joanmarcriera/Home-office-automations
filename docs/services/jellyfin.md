# Jellyfin

Jellyfin is the volunteer-built media solution that puts you in control of your media.

## Description
Stream to any device from your own server, with no strings attached. No fees, no tracking, no central server.

## Links
- [Official Website](https://jellyfin.org/)

## Alternatives
- [Plex](https://www.plex.tv/) (Non-OSS)
- [Emby](https://emby.media/) (Non-OSS)

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

## Backlog
- Setup hardware acceleration for transcoding.
- Integrate with Gelli (Android music client).


## Contribution Metadata
- Confidence: medium
- Last reviewed: 2026-02-26

## Sources / References
- [Official Website](https://jellyfin.org/)
- [Plex](https://www.plex.tv/) (Non-OSS)
- [Emby](https://emby.media/) (Non-OSS)
- [Jellyfin Docker Documentation](https://jellyfin.org/docs/general/installation/container)
- [Jellyfin API Documentation](https://api.jellyfin.org/)
