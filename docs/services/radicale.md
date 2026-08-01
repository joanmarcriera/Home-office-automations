# Radicale

Radicale is a small but powerful CalDAV (calendar) and CardDAV (contact) server. It is written in Python and is designed to be lightweight, standards-compliant, and easy to set up.

## What it is
Radicale is an open-source CalDAV and CardDAV server that allows you to host your own calendars and contacts. In late October / November 2026, the stable version is **v3.8.x**, which continues to focus on a simple, file-based storage format (iCalendar and vCard), making backups and data ownership straightforward. It is a cornerstone of privacy-first personal information management.

## What problem it solves
It provides a private, self-hosted alternative to cloud-based synchronization services (like Google Calendar or iCloud). By using standard protocols, it allows for seamless syncing across a wide variety of devices and applications while keeping the user in full control of their scheduling and contact data, eliminating third-party tracking.

## Where it fits in the stack
Radicale serves as the **Intake & Storage layer** for personal information management (PIM) within a home-office or homelab ecosystem. It is often integrated with **Claude 5.1**, **GPT-5.5**, **Gemini 4.0**, **Llama 4**, or **Gemma 3** via the **MCP 3.1 Task Protocol** or FastMCP to allow AI agents to manage appointments and contacts using natural language and standardized execution patterns.

## Typical use cases
- Syncing personal and family calendars across desktops (Thunderbird) and mobile devices (Android/iOS via DAVx⁵).
- Hosting a private address book that is accessible from multiple devices.
- Serving as a backend for task management tools that support the CalDAV protocol.
- Providing an automated audit trail for scheduling changes via Git-based versioning.
- Exposing scheduling data to agentic workflows for automated meeting preparation.

## Strengths
- **Lightweight**: Minimal resource footprint, suitable for Raspberry Pi or low-power containers.
- **Simple Storage**: Uses standard `.ics` and `.vcf` files on disk, ensuring no vendor lock-in.
- **Extensible**: Supports multiple authentication backends (htpasswd, LDAP, remote user).
- **Standards-Compliant**: High compatibility with various CalDAV/CardDAV clients.
- **Git Integration**: Native support for versioning collections via git hooks.

## Limitations
- **No Built-in Web Client**: Lacks a full-featured web interface for managing events (primarily an admin UI).
- **Single-Server Focus**: Not intended for large-scale enterprise deployments with thousands of users.
- **Manual Hardening**: Requires a reverse proxy (like Nginx or Caddy) for proper SSL/TLS and advanced security.

## When to use it
- When you want a simple, privacy-focused solution for syncing calendars and contacts.
- If you value owning your data in a transparent, file-based format.
- For small teams or families needing a shared scheduling backend.
- When integrating calendar data into local AI agent memory via MCP.

## When not to use it
- If you require integrated email, document collaboration, or a native web calendar (consider Nextcloud).
- In environments requiring complex resource booking or advanced delegation features.
- If you prefer a database-backed storage for high-concurrency write operations.

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

### Git-based Versioning
Radicale can automatically version your collections using Git. Initialize a git repo in your collections directory and add the following to your `config.ini`:
```ini
[hook]
after_save = git add . && git commit -m "Radicale change"
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
Radicale follows the standard CalDAV/CardDAV (HTTP-based) protocol. Below is a Python API validator utilizing Pydantic v2 to structure calendars parsed from Radicale.

```python
import requests
import xml.etree.ElementTree as ET
from pydantic import BaseModel, Field
from typing import List, Optional

# Define Radicale parsed collection schema in Pydantic v2
class CalendarCollection(BaseModel):
    displayname: str = Field(..., description="The user-friendly name of the Radicale collection")
    href: str = Field(..., description="The relative URI path of the collection")
    owner: str = Field(..., description="The owner/user associated with the calendar path")

class CalendarListResponse(BaseModel):
    collections: List[CalendarCollection]

def list_radicale_calendars(username: str, password: str, base_url: str = "http://localhost:5232") -> CalendarListResponse:
    url = f"{base_url}/{username}/"
    headers = {"Depth": "1"}

    # PROPFIND is the standard WebDAV/CalDAV method used to list resources
    response = requests.request(
        "PROPFIND",
        url,
        auth=(username, password),
        headers=headers
    )
    response.raise_for_status()

    # Parse CalDAV XML namespace response
    root = ET.fromstring(response.content)
    namespaces = {
        'D': 'DAV:',
        'C': 'urn:ietf:params:xml:ns:caldav'
    }

    collections = []
    # Find all D:response elements representing collections
    for resp in root.findall('D:response', namespaces):
        href = resp.find('D:href', namespaces)
        href_text = href.text if href is not None else ""

        # Skip the parent collection root path
        if href_text == f"/{username}/" or not href_text:
            continue

        propstat = resp.find('.//D:prop', namespaces)
        displayname = "Unnamed Collection"
        if propstat is not None:
            disp_el = propstat.find('D:displayname', namespaces)
            if disp_el is not None and disp_el.text:
                displayname = disp_el.text

        try:
            col = CalendarCollection(
                displayname=displayname,
                href=href_text,
                owner=username
            )
            collections.append(col)
        except Exception as e:
            print(f"Skipping invalid calendar path: {e}")

    return CalendarListResponse(collections=collections)

# Example usage
if __name__ == "__main__":
    calendars = list_radicale_calendars("admin", "your_password")
    for cal in calendars.collections:
        print(f"Validated Calendar: {cal.displayname} -> Path: {cal.href}")
```

## Related tools / concepts
- Vikunja — Task management that can sync with Radicale.
- [Authentik](authentik.md) — For unified SSO and OIDC authentication.
- [Tailscale](tailscale.md) — Secure remote access to your Radicale instance.
- [Home Assistant](home-assistant.md) — For integrating calendars into home automation.
- [n8n](n8n.md) — For automating scheduling workflows (e.g., meeting reminders).
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) — To expose CalDAV data to AI agents.
- [Local LLMs Guide](../tools/ai_knowledge/local_llms.md) — Reference for Gemma 3 and other models.

## Sources / References
- [Official Radicale Project Website](https://radicale.org/)
- [Radicale Source Code Repository](https://github.com/Kozea/Radicale)
- [Radicale Documentation v3](https://radicale.org/v3.html)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2026-11-08
- Confidence: high
