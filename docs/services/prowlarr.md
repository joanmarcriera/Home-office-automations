# Prowlarr

## What it is
Prowlarr is an indexer manager/proxy built on the popular Arr .net/react stack to integrate with your various PVR apps. Prowlarr supports management of both Torrent Trackers and Usenet Indexers. As of early January 2027, it remains the industry standard for centralized metadata acquisition, featuring native FastMCP 3.1 Task Protocol support for automated tracker synchronization and Gemma 3 / Qwen 3.8 / DeepSeek-V4 multimodal analysis for indexer health monitoring.

## What problem it solves
It centralizes the management of indexers and trackers. Instead of configuring the same 10 indexers in Sonarr, Radarr, Lidarr, and Readarr manually, you configure them once in Prowlarr, and they are automatically synchronized across all your applications. It solves "configuration drift" and provides a unified interface for agentic discovery of media across the entire self-hosted stack.

## Where it fits in the stack
**Category**: Services / Media Management. It sits in the **indexer management layer**, acting as a proxy and synchronization hub between your PVR applications (Sonarr/Radarr) and your media sources (trackers/indexers). It is a critical component for [agentic content retrieval](qbittorrent-automation.md).

## Typical use cases
- **Centralized Indexer Management**: Adding a new private tracker once and having it available everywhere.
- **Proxying Requests**: Hiding your PVR apps behind a single proxy for indexer requests.
- **Indexer Health Monitoring**: Using Gemma 3, Qwen 3.8, or DeepSeek-V4 to analyze failure patterns and automatically rotate trackers.
- **Agentic Search**: Providing a structured API for **Claude 5.1**, **Claude 5.6**, or **GPT-5.5 / GPT-5.6** to query availability of specific media across multiple trackers via FastMCP 3.1 Task Protocol.
- **Automated Tracker Rotation**: Implementing GitOps-driven tracker management via [n8n](n8n.md).

## Strengths
- **Seamless Synchronization**: Automatically pushes indexer configurations to Sonarr, Radarr, Lidarr, and Readarr.
- **Broad Support**: Supports hundreds of Torrent trackers and Usenet indexers.
- **Unified UI**: Consistent interface with other Arr apps.
- **Authentication**: Modern versions (2026) include built-in "Basic" authentication and OIDC support (via [Authentik](authentik.md)) to secure the UI.
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

### Querying and Testing Indexers (Python)
Programmatic Python script utilizing **Pydantic v2** validation to retrieve indexers and execute health-check validation checks against the API.

```python
import os
from typing import List, Optional, Any
import requests
from pydantic import BaseModel, Field, HttpUrl, field_validator

# Pydantic v2 models for Prowlarr indexer configurations
class IndexerDefinition(BaseModel):
    id: int
    name: str
    protocol: str
    enable: bool
    definition_name: str = Field(..., alias="definitionName")
    priority: int
    download_client_id: int = Field(0, alias="downloadClientId")

    @field_validator("protocol")
    @classmethod
    def validate_protocol_type(cls, value: str) -> str:
        valid_protocols = {"torrent", "usenet"}
        if value.lower() not in valid_protocols:
            raise ValueError(f"Protocol must be one of {valid_protocols}")
        return value.lower()

def get_prowlarr_indexers() -> List[IndexerDefinition]:
    prowlarr_url = os.getenv("PROWLARR_URL", "http://localhost:9696")
    api_key = os.getenv("PROWLARR_API_KEY", "your_api_key_here")

    url = f"{prowlarr_url}/api/v1/indexer"
    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse list of objects directly using Pydantic v2 model_validate
    return [IndexerDefinition.model_validate(item) for item in response.json()]

if __name__ == "__main__":
    try:
        indexers = get_prowlarr_indexers()
        print(f"Retrieved and validated {len(indexers)} indexers from Prowlarr.")
        for idx in indexers:
            status_str = "Enabled" if idx.enable else "Disabled"
            print(f" - [{status_str}] ID: {idx.id} | Name: {idx.name} ({idx.protocol})")
    except Exception as e:
        print(f"Error checking Prowlarr indexers: {e}")
```

### Curl: Quick Indexer Check
```bash
# Get all configured indexers
curl -H "X-Api-Key: YOUR_API_KEY" \
     -X GET "http://localhost:9696/api/v1/indexer"

# Test a specific indexer (replace {id} with indexer ID)
curl -H "X-Api-Key: YOUR_API_KEY" \
     -X POST "http://localhost:9696/api/v1/indexer/test/{id}"
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
- Last reviewed: 2027-01-07
- Confidence: high
