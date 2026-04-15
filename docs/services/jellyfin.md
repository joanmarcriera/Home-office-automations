# Jellyfin

Jellyfin is the volunteer-built media solution that puts you in control of your media.

## Description
Stream to any device from your own server, with no strings attached. No fees, no tracking, no central server.

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

### Python Example
```python
import requests

# Replace with your actual server IP and token
base_url = "http://localhost:8096"
headers = {"X-Emby-Token": "YOUR_ACCESS_TOKEN"}

# Get public server information
response = requests.get(f"{base_url}/System/Info/Public", headers=headers)
print(response.json())
```

### Curl Example
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
- [Plex](plex.md)
- [Nextcloud](nextcloud.md)
- [Navidrome](navidrome.md)

## Links
- [Official Website](https://jellyfin.org/)

## Alternatives
- [Plex](https://www.plex.tv/) (Non-OSS)
- [Emby](https://emby.media/) (Non-OSS)

## Backlog
- Setup hardware acceleration for transcoding.
- Integrate with Gelli (Android music client).


## Contribution Metadata
- Confidence: medium
- Last reviewed: 2026-03-02

## Sources / References
- [Official Website](https://jellyfin.org/)
- [Plex](https://www.plex.tv/) (Non-OSS)
- [Emby](https://emby.media/) (Non-OSS)
- [Jellyfin Docker Documentation](https://jellyfin.org/docs/general/installation/container)
- [Jellyfin API Documentation](https://api.jellyfin.org/)
