# Radicale

Radicale is a small but powerful CalDAV (calendar) and CardDAV (contact) server. It is written in Python and is designed to be lightweight, standards-compliant, and easy to set up.

## What it is
Radicale is an open-source CalDAV and CardDAV server that allows you to host your own calendars and contacts. As of **July 2026**, the stable version is **v3.7.x**, which continues to focus on a simple, file-based storage format (iCalendar and vCard), making backups and data ownership straightforward.

## What problem it solves
It provides a private, self-hosted alternative to cloud-based synchronization services (like Google Calendar or iCloud). By using standard protocols, it allows for seamless syncing across a wide variety of devices and applications while keeping the user in full control of their scheduling and contact data, ensuring privacy in an AI-driven world.

## Where it fits in the stack
Radicale serves as the **Intake & Storage layer** for personal information management (PIM) within a home-office or homelab ecosystem. It is often integrated with **Gemma 3** or **Claude 4.8** via the **Chronos MCP** to allow AI agents to manage appointments and contacts using natural language.

## Typical use cases
- Syncing personal and family calendars across desktops (Thunderbird) and mobile devices (Android/iOS via DAVx⁵).
- Hosting a private address book that is accessible from multiple devices.
- Serving as a backend for task management tools that support the CalDAV protocol.
- Providing an automated audit trail for scheduling changes via Git-based versioning.
- Enabling agentic scheduling via **MCP 3.0 Task Protocol** integrations.

## Strengths
- **Lightweight**: Minimal resource footprint, suitable for Raspberry Pi or low-power containers.
- **Simple Storage**: Uses standard `.ics` and `.vcf` files on disk, ensuring no vendor lock-in.
- **Extensible**: Supports multiple authentication backends (htpasswd, LDAP, remote user).
- **Standards-Compliant**: High compatibility with various CalDAV/CardDAV clients.
- **Git Integration**: Built-in support for versioning changes via git hooks.

## Limitations
- **No Built-in Web Client**: Lacks a full-featured web interface for managing events (primarily an admin UI).
- **Single-Server Focus**: Not intended for large-scale enterprise deployments with thousands of users.
- **Manual Hardening**: Requires a reverse proxy (like Nginx or Caddy) for proper SSL/TLS and advanced security.

## When to use it
- When you want a simple, privacy-focused solution for syncing calendars and contacts.
- If you value owning your data in a transparent, file-based format.
- For small teams or families needing a shared scheduling backend.
- When integrating calendar data with local AI agents using [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md).

## When not to use it
- If you require integrated email, document collaboration, or a native web calendar (consider [Nextcloud](nextcloud.md)).
- In environments requiring complex resource booking or advanced delegation features.

## Getting started

### Installation
Install Radicale using `pip`:
```bash
python3 -m pip install --upgrade radicale
```

### Docker Compose
For containerized deployments (standard for TrueNAS SCALE or Docker-based homelabs):

```yaml
services:
  radicale:
    image: tomsquest/docker-radicale:latest
    container_name: radicale
    ports:
      - "5232:5232"
    volumes:
      - ./data:/data
      - ./config:/config:ro
    restart: unless-stopped
    user: "1000:1000"
```

### Hello World
1. Access the admin UI at `http://localhost:5232`.
2. Create a new collection and select **Calendar**.
3. Name it "Work" and click **Create**.
4. Use the provided URL in your calendar client (e.g., Thunderbird) with your configured credentials.

## CLI examples
The `radicale` module provides utilities for maintenance and integrity checks:

```bash
# Verify the integrity of the local collections storage
python3 -m radicale --verify-storage

# Check the installed version and active configuration paths
python3 -m radicale --version --debug

# Export a specific collection to a single .ics file for backup
python3 -m radicale --export /path/to/collection > personal_backup.ics
```

## API examples
Radicale follows the standard CalDAV/CardDAV (HTTP-based) protocol.

### Python (Discovering Collections)
```python
import requests

url = "http://localhost:5232/admin/"
response = requests.request(
    "PROPFIND",
    url,
    auth=("admin", "your_password"),
    headers={"Depth": "1"}
)
print(response.text)
```

### Curl (Deleting an Event)
```bash
curl -u admin:password -X DELETE "http://localhost:5232/admin/calendar/event-uuid.ics"
```

## Related tools / concepts
- [Nextcloud](nextcloud.md) — Comprehensive alternative with built-in web calendar.
- [Vikunja](vikunja.md) — Task management that can sync with Radicale.
- [Authentik](authentik.md) — For unified SSO and OIDC authentication.
- [Tailscale](tailscale.md) — Secure remote access to your Radicale instance.
- [Home Assistant](home-assistant.md) — For integrating calendars into home automation.
- [n8n](n8n.md) — For automating scheduling workflows.
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) — To expose CalDAV data to AI agents.
- [DAVx⁵](https://www.davx5.com/) — The industry-standard Android synchronization client.
- [Paperless-ngx](paperless-ngx.md) — For document archiving.

## Sources / References
- [Official Website](https://radicale.org/)
- [GitHub Repository](https://github.com/Kozea/Radicale)
- [Radicale Documentation (v3)](https://radicale.org/v3.html)
- [Git-based Versioning Guide](https://radicale.org/v3.html#git-based-versioning)
- [TrueNAS SCALE Deployment](https://www.truenas.com/docs/scale/apps/custom-app-deployment/)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-21
