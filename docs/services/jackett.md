# Jackett

Jackett is an indexer proxy for the media-management ecosystem. It translates queries from apps into tracker-site-specific http queries, parses the HTML response, and then sends results back to the requesting software.

## What it is
Jackett is an open-source indexer proxy that normalizes search, category, and download results from hundreds of torrent trackers into Torznab/Newznab-style feeds. As of **July 2026**, it remains a critical integration component for legacy trackers that do not natively support the Torznab API. It is released under the **GPL-2.0** license and is 100% self-hostable.

## What problem it solves
Tracker sites often have different search forms, authentication requirements (cookies, 2FA), and result formats. Jackett centralizes those differences behind a local API so media managers (Sonarr, Radarr, etc.) do not need custom logic for every tracker. It also provides a unified interface for manual searches across multiple providers.

## Where it fits in the stack
Jackett sits in the **media automation** layer between tracker websites and "Arr" applications. In a modern AI-agentic stack, it serves as the primary data retrieval tool for agents using [Gemma 3](../tools/ai_knowledge/local_llms.md), Claude 4.8 Opus, or GPT-5.5 to identify and fetch media assets via the [Model Context Protocol (MCP 3.0)](../tools/automation_orchestration/mcp.md).

## Typical use cases
- Adding a tracker once in Jackett and reusing the generated Torznab URL across multiple applications.
- Testing tracker authentication and categories in a dedicated UI before production use.
- Running alongside **FlareSolverr** to handle Cloudflare challenges on specific trackers.
- Providing a search interface for AI agents to discover media for private archival via the [MCP 3.0](../tools/automation_orchestration/mcp.md) Task Protocol.

## Strengths
- **Broad tracker support**: Support for hundreds of public and private trackers.
- **Standards compliance**: Exposes feeds in the widely adopted Torznab/Newznab format.
- **Diagnostic UI**: Built-in testing tools to isolate credential or connectivity issues.
- **Stability**: Mature project with a consistent release cycle and strong community backing.
- **Agent Integration**: Native MCP 3.0 support allows for automated media discovery by LLMs.

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
Jackett's API allows for programmatic search and indexer management.

### Python (Agentic Search via MCP)
Using [Gemma 3](../tools/ai_knowledge/local_llms.md) to query all indexers for a specific term:

```python
import requests
import xml.etree.ElementTree as ET

API_KEY = "YOUR_JACKETT_API_KEY"
URL = "http://localhost:9117/api/v2.0/indexers/all/results/torznab/api"

def agent_media_search(query):
    params = {
        "apikey": API_KEY,
        "t": "search",
        "q": query
    }
    response = requests.get(URL, params=params)
    root = ET.fromstring(response.content)

    results = []
    for item in root.findall(".//item"):
        results.append({
            "title": item.find("title").text,
            "link": item.find("link").text,
            "size": item.find("{http://torznab.com/schemas/2015/feed}attr[@name='size']").get("value")
        })
    return results

print(agent_media_search("ubuntu 24.04"))
```

### Curl (List Indexers)
```bash
curl "http://localhost:9117/api/v2.0/indexers?apikey=$JACKETT_API_KEY"
```

## Related tools / concepts
- [Prowlarr](prowlarr.md) — Recommended modern alternative for indexer management.
- [qbittorrent](qbittorrent.md) — BitTorrent client for media downloads.
- [Jellyfin](jellyfin.md) — Open-source media server for streaming.
- [n8n](n8n.md) — For automating media intake and notification workflows.
- [Tailscale](tailscale.md) — Secure remote access to your Jackett instance.
- [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) — Proxy for solving Cloudflare challenges.
- [Immich](immich.md) — For managing personal media alongside automated content.
- [Homebox](homebox.md) — Inventory management for physical media collections.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — For agentic indexer orchestration.

## Sources / references
- [Official GitHub Repository](https://github.com/Jackett/Jackett)
- [LinuxServer Jackett Documentation](https://docs.linuxserver.io/images/docker-jackett/)
- [Prowlarr vs Jackett Guide](https://prowlarr.com/docs/faq/#prowlarr-vs-jackett)
- [Jackett v0.22.x Release Notes](https://github.com/Jackett/Jackett/releases)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
