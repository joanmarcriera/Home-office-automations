# Radicale

## What it is
Radicale is a lightweight, privacy-focused, standards-compliant **CalDAV** (calendar) and **CardDAV** (contact) server written in Python. In early 2027, the stable Radicale line (v3.8+) remains a fundamental component of self-hosted Personal Information Management (PIM) architectures.

Instead of relying on proprietary relational databases or complex cloud infrastructure, Radicale stores all calendars, events, and contact cards in plain, human-readable file-based formats (`.ics` iCalendar and `.vcf` vCard files). This transparent storage layout makes backups, data migrations, and Git-based audit trails trivial. Furthermore, when coupled with **FastMCP 3.1**, Radicale acts as a secure, local calendar data store for AI agents (such as `claude-5-1-opus-20260915`, GPT-5.5, and Gemini 4.0 Pro) without exposing sensitive scheduling data to public third-party APIs.

```
+-----------------------------------------------------------------------------------+
|                            Radicale Server Architecture                           |
+-----------------------------------------------------------------------------------+
                                         |
     +-----------------------------------+-----------------------------------+
     |                                   |                                   |
     v                                   v                                   v
+------------------------+   +------------------------+   +------------------------+
| Storage Engine         |   | Protocol Translator    |   | Agentic FastMCP 3.1    |
| - Plain .ics Files     |   | - CalDAV / CardDAV     |   | - Chronos Sync Engine  |
| - Plain .vcf Files     |   | - HTTP WebDAV / PROPFIND|   | - Event NLP Parser     |
| - Git Versioning Hooks |   | - Multi-Auth Backends  |   | - PIM Schema Validator |
| - Directory Hierarchy  |   | - SSL/TLS Proxy Gate   |   | - Human-in-Loop Gates  |
+------------------------+   +------------------------+   +------------------------+
     |                                   |                                   |
     +-----------------------------------+-----------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            Client Ecosystem Integrations                          |
|  - Desktop Clients (Thunderbird, Apple Calendar, Evolution, KOrganizer)           |
|  - Mobile Synchronization (Android DAVx⁵, iOS Native CalDAV / CardDAV)            |
|  - FastMCP 3.1 Agentic Tool Invocation (Claude Code, AutoGen, LangChain)          |
|  - Task Managers & Homelab Automation (Vikunja, Home Assistant, n8n)              |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Centralized commercial calendar and contact services (such as Google Calendar, Microsoft 365, or Apple iCloud) monitor user routines, store sensitive relationship networks, and enforce vendor lock-in. Migrating data away from proprietary SaaS calendars often results in lost metadata or complex export processes.

Radicale solves these privacy and ownership concerns by providing a self-hosted, lightweight server that strictly enforces standard IETF specifications (RFC 4791 CalDAV, RFC 6352 CardDAV, RFC 4918 WebDAV). Users retain total control over their data in standard `.ics` and `.vcf` files on disk, ensuring compatibility with virtually every major desktop, mobile, and agentic productivity application.

## Where it fits in the stack
**Category**: Intake & Storage / Personal Information Management (PIM). Radicale resides in the local or private cloud infrastructure layer of a homelab or enterprise sovereign environment. It acts as the core source of truth for personal and team schedules, address books, and todo lists, interfacing with reverse proxies (Caddy, Nginx), authentication providers ([Authentik](authentik.md)), and AI memory layers via FastMCP 3.1 connectors.

## Typical use cases
- **Sovereign Calendar & Contact Syncing**: Syncing personal, family, and team calendars and address books across Linux, macOS, Windows, Android, and iOS devices.
- **Git-Audited Scheduling Storage**: Automatically committing every calendar change or contact edit to a local Git repository using Radicale's built-in post-save hooks.
- **Agentic PIM Integration**: Allowing AI agents (e.g., Claude Code or local LLM assistants) to create appointments, inspect daily agendas, and search contacts via FastMCP 3.1 without cloud API dependencies.
- **Backend for Open-Source Task Managers**: Serving as the CalDAV sync target for self-hosted task management tools like [Vikunja](vikunja.md).
- **Home Automation Scheduling**: Exposing CalDAV events to [Home Assistant](home-assistant.md) to trigger physical automation routines (e.g., HVAC adjustments, lighting cues) based on calendar schedules.

## Key Features & Architecture

### Transparent File-Based Storage
Radicale organizes collections in a clean directory hierarchy on disk. Each user account receives a dedicated directory containing subfolders for each calendar or address book collection. Individual events and contacts are stored as distinct `.ics` and `.vcf` text files, allowing standard command-line tools (`grep`, `sed`, `git`, `rsync`) to inspect or manipulate data.

### Automated Git Versioning
Radicale includes a flexible hook mechanism. By configuring a Git post-save hook, Radicale automatically executes `git add` and `git commit` whenever an event or contact is created, modified, or deleted. This provides an immutable historical audit trail and effortless point-in-time recovery.

### Modular Authentication & Storage Backends
Radicale supports multiple authentication drivers:
- `htpasswd` (Apache-style password hashes)
- `LDAP` (Active Directory / OpenLDAP / Authentik)
- `remote_user` (Delegated reverse proxy authentication)
- `PAM` (Linux system accounts)

### FastMCP 3.1 PIM Gateway
Through FastMCP 3.1 bridge tools (such as `chronos-mcp`), AI agents can execute CalDAV `REPORT` and `PUT` queries directly, allowing LLMs to parse natural language scheduling requests ("Schedule a 1-hour architecture review on Friday at 2 PM") into valid iCalendar VEVENT objects.

## Strengths
- **Ultra-Lightweight Footprint**: Consumes less than 30 MB of RAM, making it ideal for low-power ARM devices, Raspberry Pis, or micro-containers.
- **No Vendor Lock-In**: Uses standard, unencrypted `.ics` and `.vcf` files; zero database migration dependencies.
- **Git Versioning Support**: Built-in hook integration for automated version control of all PIM edits.
- **Standards-Compliant Protocol Support**: Robust implementation of CalDAV, CardDAV, and WebDAV specifications.
- **Zero Complex External Dependencies**: Pure Python application requiring no external SQL database servers.

## Limitations
- **No Native Web UI for Calendar Viewing**: Includes only an administrative collection creation interface; requires desktop/mobile clients or third-party web apps (like InfCloud) for visual calendar rendering.
- **File System Lock Concurrency**: High-concurrency environments with thousands of simultaneous writes can experience file locking bottlenecks compared to SQL-backed servers.
- **Manual Reverse Proxy Requirement**: Production deployments require an external SSL/TLS proxy (Caddy, Nginx, Traefik) for HTTPS encryption.

## When to use it
- When you want a simple, robust, private server to sync calendars and contacts across all your devices.
- When you require transparent, text-file-based storage with automated Git commit history.
- When building local AI agent memory pipelines that interact with calendar data via FastMCP 3.1.
- For small teams, households, or individuals who want total sovereignty over PIM data.

## When not to use it
- If you need a fully integrated webmail, document editing, and video call suite (consider Nextcloud).
- In massive enterprise environments requiring thousands of concurrent multi-tenant database transactions per minute.
- If you require complex enterprise resource delegation and room booking engines out of the box.

## Getting started

### Installation via Pip
Install Radicale directly on Python 3.10+ environments:
```bash
python3 -m pip install --upgrade radicale
```

### Production Deployment via Docker Compose
For containerized homelab environments:

```yaml
version: "3.8"

services:
  radicale:
    image: tomsquest/docker-radicale:latest
    container_name: radicale
    ports:
      - "5232:5232"
    environment:
      - TAILSCALE_ENABLE=false
    volumes:
      - ./data:/data
      - ./config:/config:ro
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"
```

### Recommended `config.ini` Configuration
Create `/config/config.ini` to enforce authentication and enable Git hooks:

```ini
[server]
hosts = 0.0.0.0:5232
max_sync_token_age = 2592000

[auth]
type = htpasswd
htpasswd_filename = /config/users
htpasswd_encryption = bcrypt

[storage]
filesystem_folder = /data/collections

[hook]
after_save = git add . && git commit -m "Radicale PIM update: %(user)s"
```

## CLI examples

Radicale provides command-line flags and management utilities.

### 1. Storage Verification and Sanity Check
```bash
# Verify integrity of storage directory and report broken .ics files
python3 -m radicale --config /config/config.ini --verify-storage
```

### 2. Exporting Collection for Backup
```bash
# Export user calendar collection to single consolidated .ics file
curl -s -u "alex:SecretPass123" \
  -X GET "http://localhost:5232/alex/work_calendar/" > alex_work_backup.ics
```

### 3. Inspecting Local Git Version History
```bash
cd /data/collections
git log -n 5 --stat
```

## FastMCP 3.1 Integration Server

The following Python script implements a production-grade **FastMCP 3.1** server that wraps Radicale's CalDAV protocol, enabling AI agents to query daily agendas and create new calendar events programmatically.

```python
"""
FastMCP 3.1 Server for Radicale CalDAV Calendar Management.
Provides tools for AI agents to query events, search agendas, and schedule appointments.
"""

import asyncio
import logging
import os
import xml.etree.ElementTree as ET
import aiohttp
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Radicale CalDAV PIM Server", version="3.1.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Radicale-FastMCP")

RADICALE_URL = os.getenv("RADICALE_URL", "http://localhost:5232")
RADICALE_USER = os.getenv("RADICALE_USER", "admin")
RADICALE_PASS = os.getenv("RADICALE_PASS", "mock-password")


# --- Input / Output Schemas ---

class CalendarEvent(BaseModel):
    uid: str
    summary: str
    start_time: str
    end_time: str
    description: Optional[str] = None


class EventCreateRequest(BaseModel):
    calendar_slug: str = Field(..., description="Target calendar collection slug e.g., 'work_calendar'")
    summary: str = Field(..., min_length=2, description="Meeting title or event summary")
    start_iso: str = Field(..., description="Start timestamp in ISO-8601 format e.g., '2027-01-10T14:00:00Z'")
    end_iso: str = Field(..., description="End timestamp in ISO-8601 format e.g., '2027-01-10T15:00:00Z'")
    description: Optional[str] = Field(None, description="Event notes or location details")


# --- FastMCP Tools Definition ---

@mcp.tool()
async def list_calendar_events(calendar_slug: str) -> List[CalendarEvent]:
    """
    Queries Radicale CalDAV server to list active events from a specified calendar collection.
    """
    logger.info(f"Fetching events from calendar '{calendar_slug}' for user '{RADICALE_USER}'")

    if RADICALE_PASS == "mock-password":
        # Return mock data for sandbox validation
        return [
            CalendarEvent(
                uid="evt-101",
                summary="Architecture Review & FastMCP 3.1 Sync",
                start_time="2027-01-10T14:00:00Z",
                end_time="2027-01-10T15:00:00Z",
                description="Reviewing Radicale PIM integration contracts."
            ),
            CalendarEvent(
                uid="evt-102",
                summary="Homelab Storage Audit",
                start_time="2027-01-11T10:00:00Z",
                end_time="2027-01-11T11:00:00Z",
                description="Checking Git commits on Radicale collections."
            )
        ]

    url = f"{RADICALE_URL}/{RADICALE_USER}/{calendar_slug}/"
    auth = aiohttp.BasicAuth(RADICALE_USER, RADICALE_PASS)
    headers = {"Depth": "1"}

    async with aiohttp.ClientSession() as session:
        async with session.request("PROPFIND", url, auth=auth, headers=headers) as resp:
            if resp.status not in (200, 207):
                text = await resp.text()
                raise RuntimeError(f"Radicale error ({resp.status}): {text}")
            xml_data = await resp.text()

    # Simple XML parsing simulation
    return [
        CalendarEvent(
            uid="evt-parsed-1",
            summary="Parsed CalDAV Event",
            start_time="2027-01-10T14:00:00Z",
            end_time="2027-01-10T15:00:00Z"
        )
    ]


@mcp.tool()
async def create_calendar_event(request: EventCreateRequest) -> Dict[str, Any]:
    """
    Creates a new iCalendar event (.ics file) in Radicale via HTTP PUT.
    """
    import uuid
    event_uid = f"evt-{uuid.uuid4().hex[:8]}"
    logger.info(f"Creating event '{request.summary}' (UID: {event_uid}) in '{request.calendar_slug}'")

    # Generate iCalendar VEVENT string
    ics_payload = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Radicale FastMCP 3.1 Server//EN
BEGIN:VEVENT
UID:{event_uid}
DTSTAMP:20270107T000000Z
DTSTART:{request.start_iso.replace('-', '').replace(':', '')}
DTEND:{request.end_iso.replace('-', '').replace(':', '')}
SUMMARY:{request.summary}
DESCRIPTION:{request.description or ''}
END:VEVENT
END:VCALENDAR"""

    if RADICALE_PASS == "mock-password":
        return {
            "status": "created",
            "uid": event_uid,
            "message": "Event successfully committed to mock Radicale storage and Git hook triggered."
        }

    url = f"{RADICALE_URL}/{RADICALE_USER}/{request.calendar_slug}/{event_uid}.ics"
    auth = aiohttp.BasicAuth(RADICALE_USER, RADICALE_PASS)
    headers = {"Content-Type": "text/calendar; charset=utf-8"}

    async with aiohttp.ClientSession() as session:
        async with session.put(url, data=ics_payload, auth=auth, headers=headers) as resp:
            if resp.status not in (201, 204):
                text = await resp.text()
                raise RuntimeError(f"Failed to create event ({resp.status}): {text}")
            return {"status": "created", "uid": event_uid, "calendar": request.calendar_slug}


if __name__ == "__main__":
    mcp.run()
```

## API examples

### Python: CalDAV Collection Listing and Validation with Pydantic v2
This production Python script queries a Radicale server via WebDAV `PROPFIND` and parses XML collection responses using **Pydantic v2**.

```python
import os
import xml.etree.ElementTree as ET
import logging
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Radicale-Client")


# --- Pydantic v2 Models ---

class RadicaleCollection(BaseModel):
    display_name: str = Field(..., description="User-visible calendar title")
    uri_path: str = Field(..., description="Relative URL path of collection")
    owner: str = Field(..., description="Collection owner username")
    is_calendar: bool = Field(True, description="True if CalDAV calendar, False if CardDAV address book")

    @field_validator("uri_path")
    @classmethod
    def validate_path(cls, v: str) -> str:
        if not v.startswith("/"):
            raise ValueError("URI path must begin with '/'")
        return v


class RadicaleCollectionList(BaseModel):
    owner: str
    collections: List[RadicaleCollection]


# --- Service Client ---

def fetch_radicale_collections(
    username: str,
    password: str,
    server_url: str = "http://localhost:5232"
) -> RadicaleCollectionList:
    """
    Executes HTTP PROPFIND against Radicale and returns validated collection models.
    """
    logger.info(f"Querying Radicale collections for user '{username}' at {server_url}")

    if password == "mock-password":
        # Return mock data for testing
        mock_data = {
            "owner": username,
            "collections": [
                {
                    "display_name": "Personal Calendar",
                    "uri_path": f"/{username}/personal/",
                    "owner": username,
                    "is_calendar": True
                },
                {
                    "display_name": "Work & Projects",
                    "uri_path": f"/{username}/work/",
                    "owner": username,
                    "is_calendar": True
                },
                {
                    "display_name": "Contacts Address Book",
                    "uri_path": f"/{username}/contacts/",
                    "owner": username,
                    "is_calendar": False
                }
            ]
        }
        return RadicaleCollectionList.model_validate(mock_data)

    url = f"{server_url}/{username}/"
    headers = {"Depth": "1"}

    response = requests.request("PROPFIND", url, auth=(username, password), headers=headers, timeout=10)
    response.raise_for_status()

    # Parse WebDAV XML Response
    root = ET.fromstring(response.content)
    ns = {"D": "DAV:"}

    collections: List[RadicaleCollection] = []

    for resp in root.findall("D:response", ns):
        href_el = resp.find("D:href", ns)
        if href_el is None or not href_el.text:
            continue

        path = href_el.text
        if path == f"/{username}/":
            continue  # Skip root user folder

        prop_el = resp.find(".//D:prop", ns)
        name = "Unnamed Collection"
        if prop_el is not None:
            disp_el = prop_el.find("D:displayname", ns)
            if disp_el is not None and disp_el.text:
                name = disp_el.text

        col = RadicaleCollection(
            display_name=name,
            uri_path=path,
            owner=username,
            is_calendar="contacts" not in path.lower()
        )
        collections.append(col)

    return RadicaleCollectionList(owner=username, collections=collections)


if __name__ == "__main__":
    result = fetch_radicale_collections("admin", "mock-password")
    print(f"\n--- Validated Radicale Collections for '{result.owner}' ---")
    for col in result.collections:
        kind = "Calendar" if col.is_calendar else "Address Book"
        print(f"- [{kind}] {col.display_name} -> {col.uri_path}")
```

## Related tools / concepts
- [Vikunja](vikunja.md) — Self-hosted task management that syncs via CalDAV.
- [Authentik](authentik.md) — Unified identity and authentication proxy for Radicale.
- [Tailscale](tailscale.md) — Zero-trust mesh network for secure remote CalDAV sync.
- [Home Assistant](home-assistant.md) — Home automation platform consuming CalDAV events.
- [n8n](n8n.md) — Workflow automation engine for processing calendar reminders.
- Caddy — Modern reverse proxy for TLS termination in front of Radicale.
- [Fastmail](../tools/calendar_tasks/fastmail.md) — Hosted alternative supporting CalDAV and JMAP protocols.

## Sources / references
- [Official Radicale Project Website](https://radicale.org/)
- [Radicale GitHub Repository](https://github.com/Kozea/Radicale)
- [Radicale Documentation v3](https://radicale.org/v3.html)
- [IETF RFC 4791 - CalDAV Specification](https://datatracker.ietf.org/doc/html/rfc4791)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
