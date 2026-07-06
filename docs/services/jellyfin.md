# Jellyfin

## What it is
Jellyfin is a free and open-source media server software that allows you to organize, manage, and stream your digital media (movies, TV shows, music, and photos). Originating as a fork of Emby, it has evolved by July 2026 into a premier open-standard platform for private media distribution. It fully embraces **FastMCP 3.0** for high-performance tool hosting and uses **Gemma 3** multimodal reasoning for automated library enrichment.

## What problem it solves
Commercial media services often involve subscription fees, tracking, and limited control over personal metadata. Jellyfin provides a completely free, private alternative that ensures full ownership of media collections. It eliminates the "pay-to-transcode" model and solves the "AI discovery" problem by allowing local models to index and describe media without cloud exposure.

## Where it fits in the stack
**Category**: Service / Media Management. It sits in the **media distribution and consumption** layer. It acts as the primary interface for large libraries, integrating with the "Arr" suite ([Prowlarr](prowlarr.md)) and providing a standardized endpoint for **Gemma 3** vision agents to analyze and categorize content.

## Typical use cases
- **Personal Netflix**: Hosting a private collection of movies and TV shows for streaming to smart TVs.
- **Agentic Library Curation**: Using **Gemma 3** multimodal capabilities to automatically generate descriptions and tags for unorganized home videos.
- **Home Music Server**: Streaming high-fidelity audio (FLAC) via native apps.
- **Live TV & DVR**: Integrating with tuners to watch and record live television.
- **Automated Genre Classification**: Utilizing GPT-5.5 or **Gemma 3** via **FastMCP 3.0** to perform semantic classification of large libraries.

## Strengths
- **Truly Open Source**: No "premium" features hidden behind a paywall (unlike Plex or Emby).
- **Privacy Focused**: No central tracking; all data stays on your local infrastructure.
- **Hardware Acceleration**: High-performance transcoding using Intel QuickSync, NVENC, and AMF.
- **Modern Client Ecosystem**: The **Jellyfin Desktop** app (v12.x) provides native HDR and 4K playback.
- **MCP 3.0 Native**: Exposes library data as standardized tools for AI agents.

## Limitations
- **Client App Availability**: Some older smart TV platforms may have less polished apps than commercial competitors.
- **Setup Complexity**: Requires manual configuration for remote access (e.g., [Tailscale](tailscale.md) or a reverse proxy).
- **No Cloud-Link**: Does not offer a proprietary relay service for remote streaming.

## When to use it
- When you want a completely open-source, self-hosted media server with no tracking.
- For users who value privacy and want full control over their metadata.
- To stream media collections to various devices with efficient hardware transcoding.
- When integrating media libraries into an agentic workflow using **FastMCP 3.0**.

## When not to use it
- If you require a turn-key solution with zero configuration for remote access.
- If you depend on a specific proprietary smart TV app that is not yet supported.
- If you prefer a managed, cloud-hosted media solution.

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

### Hello World
1. Start the Jellyfin container using the command above.
2. Open your web browser and navigate to `http://localhost:8096`.
3. Follow the Setup Wizard to create your first user.
4. Add your first library by selecting the folder mounted to `/media`.
5. Your media will begin to appear in the dashboard!

## CLI examples
Jellyfin administrative tasks can be performed via `docker exec`.

```bash
# Check the version of Jellyfin running in the container
docker exec -it jellyfin /jellyfin/jellyfin --version

# View recent logs for troubleshooting
docker logs --tail 100 jellyfin

# Force a scan of all libraries
docker exec -it jellyfin /jellyfin/jellyfin-scanner -scan
```

## API examples
Jellyfin provides a REST API. You'll need an `X-Emby-Token` for most requests.

### Python: Library Metadata Enrichment
```python
import requests

# Example: Updating a movie's description using a Gemma 3 summary
url = "http://localhost:8096/Items/{ItemId}"
headers = {"X-Emby-Token": "YOUR_ACCESS_TOKEN"}
data = {
    "Overview": "Generated summary from Gemma 3 vision analysis...",
    "LockedFields": ["Overview"]
}

response = requests.post(url, headers=headers, json=data)
```

### FastMCP 3.0 Tool Definition (TypeScript)
Exposing Jellyfin search to agents.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("jellyfin-manager");

mcp.addTool({
  name: "search_media",
  description: "Search for media items in Jellyfin",
  parameters: { searchTerm: { type: "string" } },
  execute: async ({ searchTerm }) => {
    const res = await fetch(`http://jellyfin:8096/Items?searchTerm=${searchTerm}`, {
      headers: { "X-Emby-Token": process.env.JELLYFIN_TOKEN }
    });
    return res.json();
  }
});

mcp.serve();
```

## Related tools / concepts
- [Plex](plex.md) — Proprietary media server alternative.
- [Navidrome](navidrome.md) — Lightweight music-focused streaming server.
- [Audiobookshelf](audiobookshelf.md) — Audiobook and podcast management.
- [Tube Archivist](tubearchivist.md) — YouTube archival and serving.
- [Tailscale](tailscale.md) — Secure remote access without port forwarding.
- [Authentik](authentik.md) — For centralized identity and access management.
- [n8n](n8n.md) — For advanced media automation workflows.
- [Home Assistant](home-assistant.md) — For integrating media playback into home automation.
- [Prowlarr](prowlarr.md) — For managing media indexers and trackers.
- [Immich](immich.md) — Self-hosted photo and video backup solution.

## Sources / references
- [Official Website](https://jellyfin.org/)
- [Jellyfin Docker Documentation](https://jellyfin.org/docs/general/installation/container)
- [Jellyfin API Documentation](https://api.jellyfin.org/)
- [Jellyfin v12.0 Project Roadmap](https://jellyfin.org/posts/roadmap-2026/)
- [GitHub — jellyfin/jellyfin](https://github.com/jellyfin/jellyfin)

## Contribution Metadata
- Last reviewed: 2026-07-06
- Confidence: high
