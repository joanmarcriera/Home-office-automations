# Kiwix

## What it is

Kiwix is an offline content reader that allows you to download and access content like Wikipedia, Wiktionary, and TED talks without an internet connection. It uses the highly compressed ZIM format to store entire websites or databases in a single file.

## What problem it solves

Accessing reliable information usually requires an active internet connection. Kiwix solves this for environments with limited, censored, or no connectivity (e.g., remote schools, maritime vessels, disaster zones, or personal survival archives). It allows for high-speed, local searching of massive datasets without incurring data costs or relying on external infrastructure.

## Where it fits in the stack

**Category**: Service / Knowledge Management. It sits in the **offline knowledge and archival** layer, providing a fallback for critical information when the broader web is unavailable.

## Typical use cases

- **Remote Education**: Providing an entire encyclopedia to schools without internet.
- **Personal Archival**: Keeping a local copy of critical documentation (e.g., medical, survival, technical) for emergencies.
- **Privacy-First Research**: Browsing Wikipedia or Stack Overflow without being tracked by ISPs or site owners.
- **Low-Bandwidth Environments**: Accessing content at LAN speeds instead of waiting for slow satellite or cellular links.

## Strengths

- **High Compression**: ZIM files can shrink a massive website into a relatively small, portable file.
- **Powerful Search**: Includes a fast, built-in search engine that works entirely offline.
- **Multi-Platform**: Available for Windows, macOS, Linux, Android, iOS, and as a server (kiwix-serve).
- **Portability**: Content is stored in a single `.zim` file, making it easy to share via USB drives or SD cards.

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
  ghcr.io/kiwix/kiwix-serve wikipedia_en_all_maxi_2024-01.zim
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

### Python Example
```python
import requests

# Fetch the library information in XML format
response = requests.get("http://localhost:8080/catalog.xml")
if response.status_code == 200:
    print("Kiwix Library Catalog:")
    print(response.text[:500] + "...")
```

## Related tools / concepts

- [Trilium Notes](trilium.md) — for building your own personal knowledge base to complement Kiwix
- [Audiobookshelf](audiobookshelf.md) — for a similar offline-first experience with audiobooks and podcasts
- [Paperless-ngx](paperless-ngx.md) — for an offline-first archive of personal documents and receipts
- [Home Assistant](home-assistant.md) — for integrating Kiwix status or content into a local dashboard
- [Nextcloud](nextcloud.md) — for syncing ZIM files across devices for offline use
- [Internet-in-a-Box](https://internet-in-a-box.org/) — a full hardware/software stack for offline knowledge

## Sources / References

- [Official Website](https://www.kiwix.org/)
- [Kiwix Get (Downloads)](https://get.kiwix.org/)
- [GitHub Repository (Kiwix Tools)](https://github.com/kiwix/kiwix-tools)
- [Internet-in-a-Box](https://internet-in-a-box.org/)
- [Xowa](http://xowa.org/)
- [Aard 2](https://github.com/itkach/aard2-android)

## Contribution Metadata

- Last reviewed: 2026-06-25
- Confidence: high
