# IT-Tools

IT-Tools is a collection of handy online tools for developers.

## Description
It provides a wide variety of web-based tools, including formatters (JSON, SQL, XML), generators (UUID, Password, QR Code), and converters. It is designed to be fast and runs entirely in the browser.

## When to use it
- When you need quick access to common developer utilities (formatters, generators, converters) without leaving the browser.
- For a lightweight, self-hostable set of tools that doesn't require complex installation.

## When not to use it
- For complex data processing that requires a specialized CLI or heavy-duty offline tool.
- When dealing with extremely large datasets that may crash a browser-based tool.

## Getting started

### Docker
The easiest way to run IT-Tools locally is via Docker:

```bash
docker run -d --name it-tools --restart unless-stopped -p 8080:80 corentinth/it-tools:latest
```

### Usage
1. Open `http://localhost:8080` in your web browser.
2. Select a tool from the sidebar or search for one using the search bar (e.g., "JSON Formatter").
3. Paste your data into the input field and see the results instantly.

## CLI examples
Since IT-Tools runs in the browser, CLI interactions are primarily for managing the container:

```bash
# View container logs
docker logs it-tools

# Restart the IT-Tools container
docker restart it-tools

# Check the version by inspecting the image
docker inspect --format='{{index .Config.Labels "org.opencontainers.image.version"}}' corentinth/it-tools:latest
```

## Links
- [Official Website](https://it-tools.tech/)
- [GitHub Repository](https://github.com/CorentinTh/it-tools)

## Alternatives
- [Omni Tools](omni-tools.md)
- [DevToys](https://devtoys.app/) (Desktop)

## Backlog
- Host locally on TrueNAS for offline developer support.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://it-tools.tech/
- https://github.com/CorentinTh/it-tools
- https://devtoys.app/
