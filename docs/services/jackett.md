# Jackett

## What it is
Jackett is an indexer proxy for the media-management ecosystem. It translates queries from apps (CouchPotato, SickRage, Sonarr, Radarr, etc) into tracker-site-specific http queries, parses the HTML response, and then sends results back to the requesting software. It normalizes search, category, and download results from many torrent trackers into Torznab/Newznab-style feeds that tools such as Sonarr, Radarr, Lidarr, and Readarr can consume.

## What problem it solves
Tracker sites often have different search forms, authentication requirements, categories, and result formats. Jackett centralizes those differences behind a local API so media managers do not need custom logic for every tracker.

## Where it fits in the stack
Jackett sits in the **media automation** layer between tracker websites and Arr applications. In a home-office/homelab environment, it should be kept on a private network, protected by its API key, and treated as an integration adapter rather than a public-facing service.

## Typical use cases
- Add a tracker once in Jackett, then reuse the generated Torznab URL in Sonarr or Radarr.
- Test tracker authentication and categories before wiring them into multiple media apps.
- Isolate tracker-specific breakage to one service instead of every downstream application.
- Run alongside FlareSolverr when a tracker requires browser-like challenge handling.

## Strengths
- **Broad tracker support**: Many public and private trackers are supported through a common interface.
- **Arr-compatible**: Exposes URLs and API keys that Sonarr/Radarr-style tools understand.
- **Good diagnostic UI**: Per-indexer tests make broken credentials or categories easier to isolate.
- **Container-friendly**: The LinuxServer image is a common deployment path.

## Limitations
- **Tracker fragility**: HTML changes or anti-bot protections can break individual indexers.
- **Operational sensitivity**: Misconfigured public exposure can leak search behavior and API keys.
- **Overlap with Prowlarr**: New Arr-stack deployments often prefer Prowlarr for tighter management integration.

## When to use it
- When you need to integrate multiple torrent trackers into your automated media stack.
- To provide a standardized Torznab interface for legacy trackers.
- When you want to troubleshoot tracker issues in a dedicated interface before they reach your media managers.

## When not to use it
Do not expose Jackett directly to the public internet or use it for non-compliant access to copyrighted material. For a new all-Arr deployment that needs centralized app/indexer sync, evaluate [Prowlarr](https://github.com/Prowlarr/Prowlarr) first.

## Getting started

### Docker Compose quick start

```bash
mkdir -p ./jackett-config ./downloads
cat > docker-compose.yml <<'YAML'
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
YAML
docker compose up -d
```

Open `http://localhost:9117`, copy the API key from the Jackett UI, add an indexer, run **Test**, and then paste the generated Torznab feed URL into Sonarr/Radarr.

### Native Linux service option
For systems where Docker is not available, Jackett publishes release tarballs and a systemd installer script from the GitHub releases page. Prefer Docker unless a host-level install is required by the platform.

## CLI examples

```bash
# Follow Jackett logs while testing an indexer
docker logs -f jackett

# Confirm the web UI is reachable
curl -I http://localhost:9117

# Back up Jackett configuration before changing indexers
tar -czf jackett-config-backup.tgz jackett-config
```

## API examples
Jackett's API key is shown in the web UI. Export the key and an indexer ID from your instance before running the examples:

```bash
: "${JACKETT_API_KEY:?set JACKETT_API_KEY from the Jackett UI}"
: "${JACKETT_INDEXER_ID:?set JACKETT_INDEXER_ID from a configured Jackett indexer}"

# List configured indexers through the local API
curl "http://localhost:9117/api/v2.0/indexers?apikey=$JACKETT_API_KEY"

# Query one Torznab indexer for a Linux ISO-style test search
curl "http://localhost:9117/api/v2.0/indexers/$JACKETT_INDEXER_ID/results/torznab/api?apikey=$JACKETT_API_KEY&t=search&q=ubuntu"
```

Minimal Python reachability check:

```python
import os
import urllib.request

api_key = os.environ["JACKETT_API_KEY"]
url = f"http://localhost:9117/api/v2.0/indexers?apikey={api_key}"
with urllib.request.urlopen(url, timeout=10) as response:
    print(response.status)
    print(response.read().decode()[:500])
```

### Advanced: Automated Media Intake (Python)
This pattern demonstrates how to query multiple Jackett indexers for a specific term and filter results by health (seeds) and size. This is a foundational pattern for custom intake agents.

```python
import requests
import xml.etree.ElementTree as ET

# Configuration
JACKETT_URL = "http://localhost:9117"
API_KEY = "YOUR_JACKETT_API_KEY"

def search_jackett(query, category=2000): # 2000 is usually Movies
    # Query 'all' indexers via the Torznab interface
    url = f"{JACKETT_URL}/api/v2.0/indexers/all/results/torznab/api"
    params = {
        "apikey": API_KEY,
        "t": "search",
        "q": query,
        "cat": category
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    # Parse Torznab XML response
    root = ET.fromstring(response.content)
    results = []

    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text

        # Extract Torznab-specific attributes (size, seeders)
        size = 0
        seeders = 0
        for attr in item.findall("{http://torznab.com/schemas/2015/feed}attr"):
            name = attr.get("name")
            if name == "size":
                size = int(attr.get("value"))
            elif name == "seeders":
                seeders = int(attr.get("value"))

        results.append({
            "title": title,
            "link": link,
            "size_gb": round(size / (1024**3), 2),
            "seeders": seeders
        })

    return results

# Example: Find a specific Linux ISO with at least 10 seeders
matches = search_jackett("ubuntu 24.04")
healthy_matches = [m for m in matches if m["seeders"] > 10]

for m in healthy_matches:
    print(f"Found: {m['title']} ({m['size_gb']} GB, {m['seeders']} seeds)")
```

## Troubleshooting
- If an indexer test fails, re-check credentials, required cookies, two-factor/session settings, and whether the tracker changed its login flow.
- If downstream Arr apps return no results, confirm that categories selected in Jackett match the media type requested by the app.
- If Cloudflare or other browser challenges appear, test whether FlareSolverr is supported for that tracker and keep it private as well.
- If you see frequent breakage in an all-Arr stack, compare migration effort to Prowlarr.

## Links
- [GitHub Repository](https://github.com/Jackett/Jackett)
- [LinuxServer Jackett image](https://docs.linuxserver.io/images/docker-jackett/)

## Related tools / concepts
- [Prowlarr](prowlarr.md)
- [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr)
- [qbittorrent](qbittorrent.md)
- [radarr](https://radarr.video/)
- [sonarr](https://sonarr.tv/)
- [lidarr](https://lidarr.audio/)
- [readarr](https://readarr.com/)
- [jellyfin](jellyfin.md)
- [Homebox](homebox.md)

## Backlog
- [x] Migrate to Prowlarr for better integration with the "Arr" stack.

## Sources / References
- https://github.com/Jackett/Jackett
- https://docs.linuxserver.io/images/docker-jackett/
- https://github.com/Prowlarr/Prowlarr
- https://github.com/FlareSolverr/FlareSolverr

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15
