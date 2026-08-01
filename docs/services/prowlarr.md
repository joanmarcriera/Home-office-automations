# Prowlarr

## What it is
Prowlarr is an indexer manager/proxy built on the popular Arr .net/react stack to integrate with your various PVR apps. Prowlarr supports management of both Torrent Trackers and Usenet Indexers. In the late October / November 2026 ecosystem, it remains the industry standard for centralized metadata acquisition, featuring native **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** support for automated tracker synchronization and **Gemma 3** and **Qwen 3.6** multimodal analysis for indexer health monitoring.

## What problem it solves
It centralizes the management of indexers and trackers. Instead of configuring the same 10 indexers in Sonarr, Radarr, Lidarr, and Readarr manually, you configure them once in Prowlarr, and they are automatically synchronized across all your applications. It solves "configuration drift" and provides a unified interface for agentic discovery of media across the entire self-hosted stack.

## Where it fits in the stack
**Category**: Services / Media Management. It sits in the **indexer management layer**, acting as a proxy and synchronization hub between your PVR applications (Sonarr/Radarr) and your media sources (trackers/indexers). It is a critical component for [agentic content retrieval](qbittorrent-automation.md).

## Typical use cases
- **Centralized Indexer Management**: Adding a new private tracker once and having it available everywhere.
- **Proxying Requests**: Hiding your PVR apps behind a single proxy for indexer requests.
- **Indexer Health Monitoring**: Using **Gemma 3** or **Claude 5.1** to analyze failure patterns and automatically rotate trackers.
- **Agentic Search**: Providing a structured API for frontier models (**Claude 5.1**, **GPT-5.5**, **Gemini 4.0**, **Llama 4**, **Gemma 3**, **Qwen 3.6**) to query availability of specific media across multiple trackers via the MCP 3.1 Task Protocol.
- **Automated Tracker Rotation**: Implementing GitOps-driven tracker management via [n8n](n8n.md).

## Strengths
- **Seamless Synchronization**: Automatically pushes indexer configurations to Sonarr, Radarr, Lidarr, and Readarr.
- **Broad Support**: Supports hundreds of Torrent trackers and Usenet indexers.
- **Unified UI**: Consistent interface with other Arr apps.
- **Authentication**: Modern versions include built-in "Basic" authentication and OIDC support (via [Authentik](authentik.md)) to secure the UI.
- **MCP 3.1 Integration**: Native support for standardized task representations, allowing AI agents to orchestrate complex acquisition workflows.

## Limitations
- **Arr Ecosystem Focus**: Optimized for the Arr suite; may be less useful if you only use standalone downloaders or alternative PVRs.
- **Resource Usage**: Like other Arr apps, it has a non-trivial RAM footprint compared to lightweight alternatives like [Jackett](jackett.md).
- **Complexity**: For users with only one tracker, the overhead of managing Prowlarr may exceed the benefits.

## When to use it
- When you use multiple "Arr" applications (Sonarr, Radarr, etc.) and want to centralize indexer management.
- To replace [Jackett](jackett.md) for a more modern, synchronized experience.
- When you want automatic health monitoring and per-app indexer assignment.
- For managing access to private trackers across multiple geographically distributed downloaders using [Tailscale](tailscale.md).

## When not to use it
- If you only use a single PVR application and don't mind manual configuration.
- On extremely resource-constrained devices where [Jackett](jackett.md) might be preferred for its slightly lower overhead.

## Getting started

### Docker Compose
```yaml
services:
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
    volumes:
      - /path/to/prowlarr/config:/config
    ports:
      - 9696:9696
    restart: unless-stopped
```

### Hello World
1. Access the UI at `http://localhost:9696`.
2. Go to **Settings > Apps** and add your Sonarr/Radarr instances using their API keys.
3. Go to **Indexers** and add your first tracker or indexer.
4. Watch as the indexer is automatically added to your connected PVR apps!

## CLI examples
Prowlarr is primarily managed via Web UI or API, but you can check logs or restart via Docker:

```bash
# View logs
docker logs -f prowlarr

# Restart service
docker restart prowlarr

# Check the version of Prowlarr running
docker exec prowlarr /app/prowlarr/Prowlarr --version
```

## API examples

### Python: Indexer Validation (Pydantic v2)
Using Python and Pydantic v2 to validate and register Torrent/Usenet tracker configurations programmatically prior to synchronization.

```python
import requests
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class ProwlarrIndexer(BaseModel):
    name: str = Field(..., description="The user-friendly name of the indexer")
    protocol: str = Field("torrent", description="Protocol used by the indexer (e.g. torrent, usenet)")
    api_url: HttpUrl = Field(..., description="The actual target indexer API or URL endpoint")
    api_key: Optional[str] = Field(None, description="API credential key for indexer authentication")
    categories: List[int] = Field(default_factory=list, description="List of category IDs to synchronize")

def register_prowlarr_indexer(api_url: str, api_key: str, indexer: ProwlarrIndexer) -> dict:
    url = f"{api_url}/api/v1/indexer"
    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    # Pydantic v2 safely serializes the model to JSON-compatible dictionary
    payload = indexer.model_dump(mode="json")
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Sample execution block
    new_indexer = ProwlarrIndexer(
        name="SOTA Torrents Hub",
        protocol="torrent",
        api_url="https://api.sotahub-torrent.local",
        api_key="prowlarr_secret_key_2026",
        categories=[2000, 5000]
    )
    print("Prowlarr indexer config validated successfully for:", new_indexer.name)
```

### FastMCP 3.1 Indexer Tool (TypeScript)
Exposing Prowlarr's indexer health checking capability to an MCP 3.1 agent session.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("prowlarr-indexers");

mcp.addTool({
  name: "test_indexer",
  description: "Test if a specific Prowlarr indexer is currently reachable and responding",
  parameters: {
    indexerId: { type: "number", description: "The internal ID of the Prowlarr indexer" }
  },
  execute: async ({ indexerId }) => {
    const res = await fetch(`http://prowlarr:9696/api/v1/indexer/test/${indexerId}`, {
      method: "POST",
      headers: { "X-Api-Key": process.env.PROWLARR_API_KEY }
    });
    return res.json();
  }
});

mcp.serve();
```

## Related tools / concepts
- [Jackett](jackett.md) — The predecessor and primary alternative.
- [Jellyfin](jellyfin.md) — The frontend media server.
- [Plex](plex.md) — Alternative media server.
- [qbittorrent](qbittorrent.md) — Standard BitTorrent client.
- [qbittorrent-automation](qbittorrent-automation.md) — For agentic acquisition workflows.
- [n8n](n8n.md) — Workflow engine for media automation.
- [Tailscale](tailscale.md) — For secure remote access to the Prowlarr UI.
- [Authentik](authentik.md) — For SSO integration.
- [Paperless-ngx](paperless-ngx.md) — For automated document ingestion.
- [Local LLMs Guide](../tools/ai_knowledge/local_llms.md) — Reference for Gemma 3 and other models.

## Sources / references
- [Official Website](https://prowlarr.com/)
- [GitHub Repository](https://github.com/Prowlarr/Prowlarr)
- [Wiki Documentation](https://wiki.servarr.com/prowlarr)
- [Prowlarr Setup & Authentication Guide (2026)](https://www.rapidseedbox.com/blog/prowlarr-guide)

## Contribution Metadata
- Last reviewed: 2026-11-07
- Confidence: high
