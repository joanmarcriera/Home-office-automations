# Kiwix

Kiwix is an offline content reader that allows you to download and access content like Wikipedia, Wiktionary, and TED talks without an internet connection.

## Description
It uses the highly compressed ZIM format to store entire websites or databases in a single file. Kiwix is an essential tool for environments with limited or no internet access, such as schools in remote areas, prisons, or for personal archival.

## When to use it
- When you need to access large datasets (like Wikipedia) in offline, low-bandwidth, or censored environments.
- For local archival and fast searching of educational, medical, or historical content.
- When traveling or in locations where data costs are prohibitive.

## When not to use it
- When you need real-time updates and the latest content (ZIM files are snapshots).
- When you require editing capabilities for the content (it is a reader, not an editor).
- If you have very limited disk space, as full Wikipedia ZIM files can be very large (tens of GB).

## Links
- [Official Website](https://www.kiwix.org/)
- [Kiwix Get (Downloads)](https://get.kiwix.org/)
- [GitHub Repository (Kiwix Tools)](https://github.com/kiwix/kiwix-tools)

## Alternatives
- [Internet-in-a-Box](https://internet-in-a-box.org/)
- [Xowa](http://xowa.org/)
- [Aard 2](https://aard2.github.io/)

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

## Backlog
- Set up automated downloads for new ZIM files.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-02

## Sources / References
- https://www.kiwix.org/
- https://github.com/kiwix/kiwix-tools
- https://download.kiwix.org/zim/wikipedia/
- https://internet-in-a-box.org/
