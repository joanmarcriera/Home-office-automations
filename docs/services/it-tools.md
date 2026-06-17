# IT-Tools

A comprehensive suite of web-based developer utilities including formatters, generators, and converters, designed to run entirely in the client's browser.

## What it is
IT-Tools is an open-source, client-side utility suite for developers. As of **June 2026**, it features over 120 specialized tools, ranging from JWT debuggers and CRON parsers to advanced cryptographic utilities and data converters. It is designed to be lightweight, searchable, and privacy-first.

## What problem it solves
It centralizes dozens of common developer tasks into a single, searchable interface, eliminating the need to visit multiple, potentially untrusted utility websites. By running all operations locally in the browser, it ensures that sensitive data (like JSON payloads or private keys) never leaves the user's local network.

## Where it fits in the stack
IT-Tools is a **Client-Side Utility Service** in the self-hosted productivity layer. It is typically deployed as a static web application via Docker, serving as a reliable toolbox for local development and home-office operations.

## Typical use cases
- Formatting messy JSON, SQL, or XML for readability.
- Generating secure passwords, UUIDs, or mock data (Lorem Ipsum).
- Decoding JWTs or performing Base64/Hex/YAML conversions.
- Testing CRON expressions or calculating date differences.
- Inspecting and generating QR codes for local network configurations.

## Strengths
- **Privacy**: All processing happens locally in the browser.
- **Speed**: Instantaneous search and tool loading via a unified interface.
- **Self-Hostable**: Simple deployment with a single Docker image and zero external dependencies.
- **Offline Capable**: Works perfectly in air-gapped or low-connectivity environments once loaded.

## Limitations
- **Client-Side Performance**: Large files (e.g., >50MB JSON) can cause browser lag or memory exhaustion.
- **No Native Automation**: Designed for interactive use; lacks a CLI or API for batch processing.
- **Browser Compatibility**: Requires a modern web browser for advanced cryptographic and media operations.

## When to use it
- When you need quick, privacy-conscious access to developer utilities.
- For a lightweight, searchable set of tools that doesn't require complex installation.
- To provide a safe, internal alternative to public utility websites for a team or family.

## When not to use it
- For bulk data processing that requires a specialized CLI (e.g., `jq` for JSON).
- When dealing with extremely large datasets that exceed browser memory limits.
- If you require server-side persistence or collaborative features (use [Nextcloud](nextcloud.md) instead).

## Getting started

### Docker installation
The easiest way to run IT-Tools locally is via Docker:

```bash
docker run -d \
  --name it-tools \
  --restart unless-stopped \
  -p 8080:80 \
  corentinth/it-tools:latest
```

Open `http://localhost:8080` to access the toolbox.

### TrueNAS Deployment (SCALE)
1. **App Wizard**: Use the "Custom App" wizard.
2. **Image**: `corentinth/it-tools:latest`.
3. **Networking**: Map host port `30080` to container port `80`.
4. **Resources**: Assign minimal CPU/RAM (0.5 Cores / 512MB RAM is sufficient).

## CLI examples
Since IT-Tools is a static web app, CLI commands are primarily for lifecycle management:

```bash
# View container logs during initial load
docker logs it-tools

# Pull the latest tools and security updates
docker pull corentinth/it-tools:latest

# Check the version of the running container
docker inspect --format='{{index .Config.Labels "org.opencontainers.image.version"}}' it-tools
```

## API examples
IT-Tools is a front-end only application and does not expose a server-side API. For health monitoring in an automated stack (e.g., using **Claude 4.8 Opus** or **n8n**):

```bash
# Basic health check to ensure the web server is responsive
curl -fsS http://localhost:8080 >/dev/null && echo "IT-Tools is reachable"
```

For scripted transformations, use standard unix utilities instead:
```bash
# JSON formatting fallback
echo '{"it-tools":"active"}' | jq .
```

## Related tools / concepts
- [Omni Tools](omni-tools.md) — A similar browser-based utility suite with enhanced media tools.
- [SearXNG](searXNG.md) — Private search engine for developer documentation.
- [Gitea](gitea.md) — Self-hosted git service for managing the code you format.
- [Authentik](authentik.md) — For adding SSO and security to your utility suite.
- [Nextcloud](nextcloud.md) — For long-term file storage and collaboration.
- [Paperless-ngx](paperless-ngx.md) — For archiving the documents you generate or format.
- [Immich](immich.md) — For managing media assets.
- [Home Assistant](home-assistant.md) — For dashboard integration.

## Sources / References
- [Official Website](https://it-tools.tech/)
- [GitHub Repository](https://github.com/CorentinTh/it-tools)
- [Docker Hub - corentinth/it-tools](https://hub.docker.com/r/corentinth/it-tools)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).
- [ ] Implement [MCP 3.0] bridge to allow AI agents to invoke local transformation logic.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-18
