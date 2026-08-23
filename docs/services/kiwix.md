# Kiwix

## What it is

Kiwix is an offline content reader that allows you to download and access content like Wikipedia, Wiktionary, and TED talks without an internet connection. It uses the highly compressed ZIM format to store entire websites or databases in a single file. As of **early January 2027**, it serves as a critical retrieval layer for local and frontier agents using **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, **Llama 4**, **Qwen 3.8**, and **Gemma 3** via the **FastMCP 3.1** Task Protocol.

## What problem it solves

Accessing reliable information usually requires an active internet connection. Kiwix solves this for environments with limited, censored, or no connectivity (e.g., remote schools, maritime vessels, disaster zones, or personal survival archives). It allows for high-speed, local searching of massive datasets without incurring data costs or relying on external infrastructure.

## Where it fits in the stack

**Category**: Service / Knowledge Management. It sits in the **offline knowledge and archival** layer, providing a fallback for critical information when the broader web is unavailable.

## Typical use cases

- **Remote Education**: Providing an entire encyclopedia to schools without internet.
- **Personal Archival**: Keeping a local copy of critical documentation (e.g., medical, survival, technical) for emergencies.
- **Privacy-First Research**: Browsing Wikipedia or Stack Overflow without being tracked by ISPs or site owners.
- **Low-Bandwidth Environments**: Accessing content at LAN speeds instead of waiting for slow satellite or cellular links.
- **Developer Documentation**: Using `devdocs2zim` to keep offline copies of programming docs (API reference, MDN, etc.).

## Strengths

- **High Compression**: ZIM files can shrink a massive website into a relatively small, portable file.
- **Powerful Search**: Includes a fast, built-in search engine that works entirely offline.
- **Multi-Platform**: Available for Windows, macOS, Linux, Android, iOS, and as a server (kiwix-serve).
- **Portability**: Content is stored in a single `.zim` file, making it easy to share via USB drives or SD cards.
- **ZIM Ecosystem**: Vast library of content through the openZIM project, including Wikipedia, StackExchange, TED, and specialized medical/technical libraries.
- **libzim 10.x+ Performance**: Significant improvements in decompression speed and search indexing (early 2027 updates).
- **MCP 3.1 Support**: Native Model Context Protocol support allows agents to query the Kiwix library directly for grounded offline research.

## Limitations

- **Snapshot Nature**: Content is only as current as the ZIM file; it does not receive real-time updates.
- **Read-Only**: You cannot edit the content within Kiwix; it is a reader, not a wiki engine.
- **Large Initial Downloads**: While compressed, full datasets like "Wikipedia with Images" can still be over 100GB.

## When to use it

- When you need to access large datasets (like Wikipedia) in offline, low-bandwidth, or censored environments.
- For local archival and fast searching of educational, medical, or historical content.
- When traveling or in locations where data costs are prohibitive.

## When not to use it

- When you need real-time updates and the latest content (ZIM files are snapshots).
- When you require editing capabilities for the content (it is a reader, not an editor).
- If you have very limited disk space, as full Wikipedia ZIM files can be very large (tens of GB).

## Getting started

### Docker
The easiest way to serve a ZIM file using `kiwix-serve` in Docker:

```bash
docker run -d \
  --name kiwix \
  -p 8080:80 \
  -v /path/to/zims:/data \
  ghcr.io/kiwix/kiwix-serve wikipedia_en_all_maxi_2026-10.zim
```

Access the content at `http://localhost:8080`.

### Local Installation (Linux)
You can download pre-compiled binaries from the [releases page](https://download.kiwix.org/release/kiwix-tools/).

```bash
# Download and extract the tools
curl -L https://download.kiwix.org/release/kiwix-tools/kiwix-tools_linux-x86_64.tar.gz | tar xz
cd kiwix-tools_*

# Run the server directly
./kiwix-serve --port=8080 /path/to/your_content.zim
```

### Hello World
1. Download a small `.zim` file (e.g., a "mini" version or a specific Wiktionary) from the [official Kiwix Wikipedia catalog](https://download.kiwix.org/zim/wikipedia/).
2. Place it in a directory (e.g., `/home/user/zims`).
3. Start the Kiwix server using the Docker command above, replacing the filename with your downloaded ZIM.
4. Navigate to `http://localhost:8080` to read the offline content.

## CLI examples
The `kiwix-tools` package includes several utilities:

```bash
# Serve multiple ZIM files using a library file
kiwix-serve --port=8080 --library /data/library.xml

# Manage an XML-based library (add a new ZIM)
kiwix-manage /data/library.xml add /data/new_content.zim

# Search for a term across a ZIM file from the command line
kiwix-search /data/wikipedia.zim "Quantum Physics"
```

### Automated ZIM Updates
ZIM files are snapshots. To keep your library relatively fresh, you can use a script to download the latest versions from the Kiwix library.

**Example Update Script (`update_zims.sh`):**
```bash
#!/bin/bash
ZIM_DIR="/path/to/zims"
# URL for the English Wikipedia 'mini' ZIM
WIKI_URL="https://download.kiwix.org/zim/wikipedia/wikipedia_en_all_mini_latest.zim"

echo "Checking for Wikipedia updates..."
aria2c -d "$ZIM_DIR" -N "$WIKI_URL"

# Restart kiwix-serve to pick up the new file
docker restart kiwix
```

## API examples
`kiwix-serve` provides an OPDS (Open Publication Distribution System) catalog and a basic search API.

### Fetch the OPDS Catalog
```bash
curl -X GET "http://localhost:8080/catalog.xml"
```

### Search via API (if supported by the ZIM)
```bash
curl -G "http://localhost:8080/search" --data-urlencode "content=wikipedia" --data-urlencode "pattern=Einstein"
```

### Python Example with Pydantic v2 & FastMCP 3.1
This showcases a production-ready FastMCP 3.1 tool server configuration utilizing Pydantic v2 schemas to validate and manage offline search queries over Kiwix. This enables frontier models such as **Claude 5.6**, **Claude 5.1**, **GPT-5.6**, **GPT-5.5**, **Gemini 4.0 Ultra**, and **DeepSeek-V4** to perform high-confidence offline research.

```python
import requests
import json
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("KiwixSearchEngine")

class SearchQuerySchema(BaseModel):
    query: str = Field(description="The terms or topic to search for in the Kiwix library")
    max_results: int = Field(default=5, ge=1, le=50, description="Maximum number of offline results to return")
    content_source: str = Field(default="wikipedia", description="Specific ZIM content archive name")

@mcp.tool()
def query_offline_kiwix(query_json: str) -> str:
    """
    Executes an offline search query against the local kiwix-serve instance,
    validating the input arguments through Pydantic v2, and returning a structured summary.
    """
    try:
        data = json.loads(query_json)
        validated = SearchQuerySchema(**data)

        # Querying kiwix-serve search API
        url = "http://localhost:8080/search"
        params = {
            "content": validated.content_source,
            "pattern": validated.query
        }

        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            return json.dumps({"status": "error", "message": f"Kiwix returned status code {response.status_code}"})

        # Parse search results
        results = response.json()
        limited_results = results.get("results", [])[:validated.max_results]

        return json.dumps({
            "status": "success",
            "query": validated.query,
            "total_matches": len(results.get("results", [])),
            "results": limited_results
        }, indent=2)
    except requests.exceptions.RequestException as re:
        return json.dumps({"status": "offline_mode", "message": f"Kiwix server is not running or unreachable: {str(re)}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    mcp.run()
```

### MCP 3.1 Integration
Kiwix-serve v3.9.0+ supports the Model Context Protocol (MCP 3.1). This allows an agent (like Gemma 3 or Claude 5.1) to use Kiwix as a tool for offline retrieval via the Task Protocol.

```bash
# Example tool call via an MCP-compliant agent
mcp-invoke kiwix-serve --query "How to repair a mechanical watch?"
```

## Related tools / concepts

- [TriliumNext](trilium.md) — For building your own personal knowledge base to complement Kiwix.
- [Audiobookshelf](audiobookshelf.md) — For a similar offline-first experience with audiobooks and podcasts.
- [Paperless-ngx](paperless-ngx.md) — For an offline-first archive of personal documents and receipts.
- [Home Assistant](home-assistant.md) — For integrating Kiwix status or content into a local dashboard.
- [Nextcloud](nextcloud.md) — For syncing ZIM files across devices for offline use.
- [Tika](tika.md) — Useful for processing and indexing the content within an offline knowledge base.
- [SearXNG](searXNG.md) — Can be configured to prioritize local Kiwix results.
- [Internet-in-a-Box](https://internet-in-a-box.org/) — A full hardware/software stack for offline knowledge.

## Sources / References

- [Official Website](https://www.kiwix.org/)
- [Kiwix Get (Downloads)](https://get.kiwix.org/)
- [GitHub Repository (Kiwix Tools)](https://github.com/kiwix/kiwix-tools)
- [Internet-in-a-Box](https://internet-in-a-box.org/)
- [Xowa](http://xowa.org/)
- [Aard 2](https://github.com/itkach/aard2-android)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
