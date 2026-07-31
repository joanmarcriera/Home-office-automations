# Jellyfin

## What it is
Jellyfin is a free and open-source media server software that allows you to organize, manage, and stream your digital media (movies, TV shows, music, and photos). Originating as a fork of Emby, it has evolved by November 2026 into a premier open-standard platform for private media distribution. It fully embraces **FastMCP 3.1** for high-performance tool hosting and uses **Gemini 4.0** and **Gemma 3** multimodal reasoning for automated library enrichment and content understanding.

## What problem it solves
Commercial media services often involve subscription fees, telemetry tracking, and limited control over personal metadata. Jellyfin provides a completely free, private alternative that ensures full ownership of media collections. It eliminates the "pay-to-transcode" model and solves the "AI-driven discovery and enrichment" challenge by allowing local models to index, tag, and describe media without cloud exposure.

## Where it fits in the stack
**Category**: Service / Media Management. It sits in the **media distribution and consumption** layer. It acts as the primary interface for large libraries, integrating with the "Arr" suite ([Prowlarr](prowlarr.md)) and providing a standardized endpoint for **Gemini 4.0** and **Gemma 3** vision agents to analyze, index, and categorize raw content.

## Typical use cases
- **Personal Netflix**: Hosting a private collection of movies and TV shows for streaming to smart TVs and mobile clients.
- **Agentic Library Curation**: Using **Gemini 4.0** and **Gemma 3** multimodal capabilities to automatically generate high-quality descriptions and genre tags for unorganized home videos.
- **Home Music Server**: Streaming high-fidelity audio (FLAC) via native clients.
- **Live TV & DVR**: Integrating with hardware tuners to watch and record live television.
- **Automated Genre Classification**: Utilizing GPT-5.5 or **Gemma 3** via **FastMCP 3.1** to perform semantic classification of large libraries.

## Strengths
- **Truly Open Source**: No premium features hidden behind a paywall (unlike Plex or Emby).
- **Privacy Focused**: No central tracking or telemetries; all user data remains on local infrastructure.
- **Hardware Acceleration**: Highly efficient transcoding using Intel QuickSync, NVENC, and AMF.
- **Modern Client Ecosystem**: The **Jellyfin Desktop** and mobile clients provide native HDR and 4K playback.
- **FastMCP 3.1 Native**: Exposes library data as standardized tools for AI agents under the Model Context Protocol.

## Limitations
- **Client App Availability**: Some older smart TV platforms may have less polished apps than commercial competitors.
- **Setup Complexity**: Requires manual configuration for remote access (e.g., [Tailscale](tailscale.md) or a reverse proxy).
- **No Cloud-Link**: Does not offer a proprietary relay service for remote streaming, requiring own networking setup.

## When to use it
- When you want a completely open-source, self-hosted media server with no telemetry tracking.
- For users who value privacy and want full control over their metadata database.
- To stream media collections to various devices with efficient hardware transcoding.
- When integrating media libraries into an agentic workflow using **FastMCP 3.1**.

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

### Python: Library Metadata Enrichment with Pydantic v2
This script uses **Pydantic v2** to validate metadata updates before writing them back to the Jellyfin API, incorporating summaries from a **Gemini 4.0** or **Gemma 3** vision analysis pipeline.

```python
import requests
from pydantic import BaseModel, Field, conlist
from typing import Optional

# Define the metadata schema using Pydantic v2
class JellyfinMovieMetadata(BaseModel):
    overview: str = Field(..., description="Generated summary from Gemini 4.0 vision analysis", min_length=10)
    genres: conlist(str, min_length=1) = Field(..., description="List of categorized genres")
    tagline: Optional[str] = Field(None, description="Catchy tagline for the movie")
    locked_fields: list[str] = Field(default=["Overview", "Genres"], description="Lock fields to prevent scraper overwrites")

# Example: Updating a movie's description
def update_jellyfin_metadata(item_id: str, token: str, metadata_payload: dict):
    # Validate payload using Pydantic v2
    validated = JellyfinMovieMetadata(**metadata_payload)

    url = f"http://localhost:8096/Items/{item_id}"
    headers = {
        "X-Emby-Token": token,
        "Content-Type": "application/json"
    }

    data = {
        "Overview": validated.overview,
        "Genres": validated.genres,
        "Tagline": validated.tagline,
        "LockedFields": validated.locked_fields
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print("Metadata updated and validated successfully!")

# Usage example (Dummy parameters)
# update_jellyfin_metadata("item_123", "dummy_token", {
#     "overview": "An interactive, visual demo of homelab services automated via agents.",
#     "genres": ["Homelab", "Automation"],
#     "tagline": "The future of automation is here."
# })
```

### FastMCP 3.1 Tool Definition (TypeScript)
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
- [Jellyfin Project Roadmap](https://jellyfin.org/posts/roadmap-2026/)
- [GitHub — jellyfin/jellyfin](https://github.com/jellyfin/jellyfin)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
