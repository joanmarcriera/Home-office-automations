# IT-Tools

## What it is
A comprehensive suite of web-based developer utilities including formatters, generators, and converters. It is designed to run entirely in the client's browser.

## What problem it solves
It centralizes dozens of common developer tasks (like JWT decoding, UUID generation, and JSON formatting) into a single, searchable interface, eliminating the need to visit multiple, potentially untrusted utility websites.

## Where it fits in the stack
It is a **Client-Side Utility Service**, typically self-hosted via Docker for privacy and offline availability.

## Typical use cases
- Formatting messy JSON or SQL queries for readability.
- Generating secure passwords or mock data (UUIDs, Lorem Ipsum).
- Converting between different data representations (Base64, Hex, YAML).

## Strengths
- **Privacy**: Most operations happen locally in the browser.
- **Searchable**: Fast fuzzy search for all tools.
- **Self-Hostable**: Easy deployment via a single Docker image.

## Limitations
- **Browser-Bound**: Not suitable for CLI-based automation or bulk processing of massive files.
- **Client Performance**: Very large files may lag the browser interface.

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

### TrueNAS Deployment
To host IT-Tools on TrueNAS (SCALE or CORE with Docker/Jails):
1. **Create a Dataset**: Create a dataset for configuration (though IT-Tools is largely stateless).
2. **Custom App (SCALE)**: Use the "Custom App" wizard.
   - **Image**: `corentinth/it-tools:latest`
   - **Port Forwarding**: Map a host port (e.g., 30080) to container port 80.
3. **Networking**: Ensure the web UI is accessible over your local network for offline use.

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
- [Omni Tools](omni-tools.md)
- [SearXNG](searXNG.md)
- [Gitea](gitea.md)
- [Authentik](authentik.md)
- [Nextcloud](nextcloud.md)
- [Paperless-ngx](paperless-ngx.md) — For managing the documents generated or formatted by these tools.
- [Immich](immich.md) — For managing media assets.
- [Home Assistant](home-assistant.md) — For dashboard integration.

## Backlog
- [x] Host locally on TrueNAS for offline developer support.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15

## Sources / References
- https://it-tools.tech/
- https://github.com/CorentinTh/it-tools
- https://devtoys.app/
