# Jackett

## What it is
Jackett is an indexer proxy for the media-management ecosystem. It translates queries from apps into tracker-site-specific http queries, parses the HTML response, and then sends results back to the requesting software. In early January 2027, it supports modern trackers while providing a FastMCP 3.1 bridge for autonomous media discovery by frontier models like **Claude 5.1**, **Claude 5.6**, **GPT-5.5**, **GPT-5.6**, **Gemini 4.0 Pro/Ultra**, and **Llama 4**.

## What problem it solves
Tracker sites often have different search forms, authentication requirements (cookies, 2FA), and result formats. Jackett centralizes those differences behind a local API so media managers (Sonarr, Radarr, etc.) do not need custom logic for every tracker. It also provides a unified interface for manual searches across multiple providers.

## Where it fits in the stack
**Category**: Service / Media / Automation. It sits in the **media automation** layer between tracker websites and "Arr" applications. In a modern AI-agentic stack, it serves as a robust retrieval tool for agents using **Claude 5.1** or **GPT-5.5** to identify and fetch media assets via the **Model Context Protocol (MCP 3.1)**.

## Typical use cases
- Adding a tracker once in Jackett and reusing the generated Torznab URL across multiple applications.
- Testing tracker authentication and categories in a dedicated UI before production use.
- Running alongside **FlareSolverr** to handle Cloudflare challenges on specific trackers.
- Providing a search interface for AI agents (Claude 5.1, GPT-5.5) to discover media for private archival.
- Implementing an MCP 3.1 server for natural language media discovery and ingestion.

## Strengths
- **Broad tracker support**: Support for hundreds of public and private trackers.
- **Standards compliance**: Exposes feeds in the widely adopted Torznab/Newznab format.
- **Diagnostic UI**: Built-in testing tools to isolate credential or connectivity issues.
- **Stability**: Mature project with a consistent release cycle and strong community backing.
- **Agentic Bridge**: Early 2027 features improved FastMCP 3.1 integration for seamless agent orchestration.

## Limitations
- **Tracker fragility**: Changes to a tracker's HTML or bot protection can break individual indexers.
- **Privacy**: Requires careful network isolation; misconfiguration can leak search history.
- **Redundancy**: For new "Arr" stacks, [Prowlarr](prowlarr.md) is often preferred for its native sync capabilities.

## When to use it
- When integrating trackers that are not yet supported by Prowlarr.
- To maintain a standardized Torznab interface for legacy media tools.
- When you need a dedicated diagnostic interface for troubleshooting tracker-specific failures.

## When not to use it
- In new, all-"Arr" stack deployments (evaluate [Prowlarr](prowlarr.md) first).
- If you require a managed service; Jackett is strictly self-hosted for privacy and security.
- For public-facing services; Jackett should always be kept on a private network.

## Getting started

### Docker Compose quick start

```yaml
services:
  jackett:
    image: lscr.io/linuxserver/jackett:latest
    container_name: jackett
    environment:
      PUID: "1000"
      PGID: "1000"
      TZ: "Etc/UTC"
    volumes:
      - ./jackett-config:/config
      - ./downloads:/downloads
    ports:
      - "9117:9117"
    restart: unless-stopped
```

Open `http://localhost:9117`, copy the API key, add an indexer, and run **Test** to confirm connectivity.

## CLI examples

```bash
# Follow Jackett logs while testing an indexer
docker logs -f jackett

# Confirm the web UI is reachable via curl
curl -I http://localhost:9117

# Back up Jackett configuration before an upgrade
tar -czf jackett-config-backup-$(date +%F).tgz ./jackett-config
```

## API examples
Jackett's API allows for programmatic search and indexer management. The following Python script utilizes Pydantic v2 to validate search results.

```python
import requests
import xml.etree.ElementTree as ET
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

# Define Pydantic v2 schemas for validating Jackett results
class TorrentResult(BaseModel):
    title: str = Field(..., description="The name of the torrent release")
    link: HttpUrl = Field(..., description="The download URL or magnet link")
    size_bytes: int = Field(..., alias="size", description="The size of the payload in bytes")

    # Handle coercion of strings to integers in Pydantic v2
    @classmethod
    def from_xml_item(cls, item: ET.Element) -> "TorrentResult":
        title_text = item.find("title").text or ""
        link_text = item.find("link").text or ""

        # Extract torznab size attribute if present
        size_val = 0
        size_attr = item.find("{http://torznab.com/schemas/2015/feed}attr[@name='size']")
        if size_attr is not None:
            size_val = int(size_attr.get("value") or 0)

        return cls(title=title_text, link=link_text, size=size_val)

class SearchResponse(BaseModel):
    query: str
    results: List[TorrentResult]

def agent_media_search(api_key: str, query: str, base_url: str = "http://localhost:9117") -> SearchResponse:
    url = f"{base_url}/api/v2.0/indexers/all/results/torznab/api"
    params = {
        "apikey": api_key,
        "t": "search",
        "q": query
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    torrent_results = []

    for item in root.findall(".//item"):
        try:
            parsed_result = TorrentResult.from_xml_item(item)
            torrent_results.append(parsed_result)
        except Exception as e:
            # Skip invalid entries gracefully
            print(f"Skipping invalid result due to: {e}")

    return SearchResponse(query=query, results=torrent_results)

# Example execution
if __name__ == "__main__":
    api_key = "YOUR_JACKETT_API_KEY"
    search_data = agent_media_search(api_key, "debian 12.5")
    for r in search_data.results:
        print(f"Found: {r.title} ({r.size_bytes / 1024**2:.2f} MB)")
```

## Related tools / concepts
- [Prowlarr](prowlarr.md) — Recommended modern alternative for indexer management.
- [qbittorrent](qbittorrent.md) — BitTorrent client for media downloads.
- [Jellyfin](jellyfin.md) — Open-source media server for streaming.
- [n8n](n8n.md) — For automating media intake and notification workflows.
- [Tailscale](tailscale.md) — Secure remote access to your Jackett instance.
- [Immich](immich.md) — For managing personal media alongside automated content.
- [Homebox](homebox.md) — Inventory management for physical media collections.

## Sources / references
- [Jackett Github Project Repository](https://github.com/Jackett/Jackett)
- [LinuxServer Jackett Docker Image Docs](https://docs.linuxserver.io/images/docker-jackett/)
- [Prowlarr vs Jackett Comparison Guide](https://prowlarr.com/docs/faq/#prowlarr-vs-jackett)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
