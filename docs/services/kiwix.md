# Kiwix

Kiwix is an offline content reader.

## Description
It allows you to download and access content like Wikipedia, Wiktionary, and TED talks without an internet connection. It is highly useful for environments with limited or no internet access.

## When to use it
- When you need to access large datasets (like Wikipedia) in offline or low-bandwidth environments.
- For local archival and fast searching of educational or historical content.

## When not to use it
- When you need real-time updates and the latest content.
- When you require editing capabilities for the content.

## Getting started

### Docker
To serve a single `.zim` file using `kiwix-serve` in Docker:

```bash
docker run -d \
  -p 8080:80 \
  -v /path/to/zims:/data \
  ghcr.io/kiwix/kiwix-serve wikipedia_en_all_maxi_2024-01.zim
```

Access the content at `http://localhost:8080`.

### Hello World
1. Download a small `.zim` file (e.g., [Ray Charles Wiki](https://download.kiwix.org/zim/wikipedia/wikipedia_en_ray_charles_mini_2024-01.zim)).
2. Place it in `/path/to/zims`.
3. Start the container with that filename.
4. Navigate to `http://localhost:8080` to read the offline content.

## CLI examples
The `kiwix-manage` tool allows you to manage library XML files:

```bash
# Create a new library file
kiwix-manage /data/library.xml add /data/wikipedia.zim

# Remove a zim file from the library
kiwix-manage /data/library.xml remove wikipedia

# List all files in a ZIM archive
kiwix-search --list /data/wikipedia.zim
```

## API examples
Kiwix-serve provides an OPDS catalog and a basic API for library exploration:

```bash
# Fetch library information in OPDS format
curl -X GET "http://localhost:8080/catalog.xml"
```

## Links
- [Official Website](https://www.kiwix.org/)
- [GitHub Repository](https://github.com/kiwix/kiwix-tools)

## Alternatives
- [Internet-in-a-Box](https://internet-in-a-box.org/)

## Backlog
- Set up automated downloads for new ZIM files.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://www.kiwix.org/
- https://github.com/kiwix/kiwix-tools
- https://internet-in-a-box.org/
