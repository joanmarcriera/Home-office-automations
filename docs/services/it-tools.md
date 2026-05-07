# IT-Tools

## What it is

IT-Tools is a comprehensive, open-source collection of web-based utilities designed for developers. It features a wide array of tools including formatters (JSON, SQL, XML), generators (UUID, Password, QR Code), and various converters. The application is built to be extremely fast and runs entirely in the browser after the initial load.

## What problem it solves

Developers often need small utilities for daily tasks but using public SaaS websites for these can pose privacy risks (pasting sensitive JSON or SQL) or be inconvenient due to ads and tracking. IT-Tools provides a unified, self-hostable suite of these utilities that ensures data stays within the local network.

## Where it fits in the stack

**Category**: Service / Developer Utility. It belongs in the **self-hosted productivity utilities** layer, typically hosted alongside code repositories and CI/CD tools.

## Typical use cases
- Formatting and minifying code snippets (JSON, CSS, SQL).
- Generating secure passwords and unique identifiers (UUID, ULID).
- Converting between different data formats (YAML to JSON, Base64, etc.).
- Inspecting and debugging network/web data (JWT parser, HTTP status codes).

## Strengths
- **Huge Variety**: Over 50+ tools in a single interface.
- **Client-Side Processing**: Most tools perform logic in the browser, ensuring speed and privacy.
- **Modern UI**: Clean, searchable, and responsive design.
- **Lightweight**: Minimal backend requirements; primarily serves static assets.

## Limitations
- **Browser-Only**: Not designed for automated CLI-based data processing.
- **State Management**: Generally doesn't persist data across sessions; each tool is a "stateless" utility.

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

## Related tools / concepts
- [Omni Tools](omni-tools.md) — similar collection of web-based utilities
- [Gitea](gitea.md) — self-hosted Git service to pair with developer tools
- [Linkwarden](linkwarden.md) — for saving useful snippets and documentation
- [Changedetection.io](changedetection.md) — for monitoring documentation or API changes
- [DevToys](https://devtoys.app/) — desktop-based alternative for developer utilities

## Backlog
- Host locally on TrueNAS for offline developer support.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://it-tools.tech/
- https://github.com/CorentinTh/it-tools
- https://devtoys.app/
