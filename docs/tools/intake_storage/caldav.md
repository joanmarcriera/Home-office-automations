# CalDAV

## What it is
CalDAV (Calendaring Extensions to WebDAV) is an open internet standard (RFC 4791) that enables client applications to discover, access, and manage scheduling information on remote servers. Extending the WebDAV (Web Distributed Authoring and Versioning) protocol and utilizing the iCalendar (RFC 5545) payload format, CalDAV provides a robust framework for multi-user calendar synchronization, free/busy status queries, access control lists (ACLs), and task (VTODO) management.

As of early January 2027, CalDAV serves as a fundamental scheduling protocol in sovereign, self-hosted AI stacks. It seamlessly connects autonomous agents executing Model Context Protocol (MCP) tool calls—specifically via **FastMCP 3.1 Task Protocol**—with self-hosted calendars like Nextcloud, Radicale, and Baïkal, enabling local AI models (such as DeepSeek-V4, Qwen 3.6, Llama 4, Claude 5.6, and GPT-5.6) to inspect temporal constraints, draft scheduling proposals, and synchronize reminders without relying on proprietary third-party cloud APIs.

## What problem it solves
- **Vendor Lock-in & Data Silos**: Proprietary calendar solutions (e.g., Google Calendar, Microsoft Exchange, Apple iCloud) enforce proprietary APIs, data silos, and vendor-driven privacy terms. CalDAV enforces an open standard, ensuring complete data ownership and multi-vendor client compatibility.
- **Agentic Temporal Context**: AI agents require structured, deterministic access to user schedules and todo lists. CalDAV exposes uniform XML HTTP methods (`PROPFIND`, `REPORT`, `MKCALENDAR`) and standard iCalendar MIME types (`text/calendar`), allowing agents to query events and task states cleanly without brittle web scraping or platform-specific SDK overhead.
- **Cross-Platform Interoperability**: CalDAV unifies scheduling across diverse operating systems and clients—including macOS Calendar, Thunderbird, iOS, Android (via DAVx⁵), and CLI tools—enabling seamless updates from both human inputs and autonomous workflows.
- **Privacy & Sovereignty**: In home-lab and enterprise deployments, scheduling data often contains highly sensitive information (medical appointments, private meetings, family routines). CalDAV allows home-lab operators to host end-to-end encrypted or private network calendars behind local identity providers like Authentik.

## Where it fits in the stack
**Infrastructure & Protocol Layer**. CalDAV operates directly on top of HTTP/1.1 and HTTP/2, utilizing WebDAV XML extensions for directory listing and property retrieval. It sits beneath calendar client applications, automation engines (e.g., n8n, Home Assistant), and FastMCP 3.1 scheduling gateways.

```
+-----------------------------------------------------------------------------------+
|                            User Interfaces & AI Agents                            |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  | Native Mobile/Desktop|   | FastMCP 3.1 Task Agent|   |  n8n / Home Assistant  |  |
|  | (iOS / DAVx5 / OS X|   | (Claude 5.6 / Qwen)   |   |   Automation Workflows |  |
|  +---------+----------+   +-----------+-----------+   +-----------+------------+  |
+------------|--------------------------|---------------------------|---------------+
             |                          |                           |
             +--------------------------+---------------------------+
                                        |
                                        v HTTP/HTTPS (CalDAV Protocol: RFC 4791)
                                        |  - PROPFIND (Discovery)
                                        |  - REPORT (Time-range queries)
                                        |  - PUT/DELETE (Event CRUD)
+---------------------------------------v-------------------------------------------+
|                          CalDAV Server Infrastructure                             |
|  +-----------------------------------------------------------------------------+  |
|  |                         WebDAV / CalDAV Engine                              |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | Authentication & Access   |  | iCalendar Parser & Indexer             |  |  |
|  |   | (OAuth2 / Authentik / Digest)  | (VEVENT, VTODO, VFREEBUSY Validation)  |  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|  +-----------------------------------------------------------------------------+  |
|  |                       Storage Layer (SQLite / ZFS / PostgreSQL)             |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   |  Radicale / Nextcloud DAV / Baïkal VEVENT Storage (.ics files)      |   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **FastMCP 3.1 Agentic Scheduling**: Autonomous AI assistants running via FastMCP 3.1 inspect CalDAV endpoints using `REPORT` queries to identify open time slots and insert structured `VEVENT` entries with automated reminder alarms (`VALARM`).
- **Sovereign Multi-Device Sync**: Synchronizing private calendars and task lists across personal devices using self-hosted servers such as Radicale or Nextcloud behind Caddy or Traefik reverse proxies.
- **Home Automation Integration**: Home Assistant queries CalDAV event states to trigger physical automations (e.g., adjusting climate controls prior to "Work From Home" calendar blocks or disabling notifications during "Deep Work" events).
- **Document-Driven Event Creation**: Workflows in n8n parse inbound invoices or medical appointment PDFs processed by Paperless-ngx, extract date/time metadata using open LLMs, and push formatted iCal records directly to a CalDAV server.
- **Task Synchronization (VTODO)**: Managing unified task queues across apps like Vikunja, Thunderbird, and OpenWebUI using CalDAV VTODO extensions.

## Architecture & Communication Protocols

CalDAV relies on specific HTTP request methods and XML payload formats to handle discovery, event queries, and concurrency management:

### Protocol Execution Flow

```
Client / FastMCP Agent                         CalDAV Server (Nextcloud / Radicale)
          |                                                   |
          |  1. PROPFIND /principal-search/ (Discover URL)    |
          |-------------------------------------------------->|
          |  2. 207 Multi-Status (XML with Calendar URLs)     |
          |<--------------------------------------------------|
          |                                                   |
          |  3. REPORT /calendar/ (time-range filter query)   |
          |-------------------------------------------------->|
          |  4. 207 Multi-Status (returns matching .ics VEVENTs)|
          |<--------------------------------------------------|
          |                                                   |
          |  5. PUT /calendar/event-12345.ics (Create/Update) |
          |     If-Match: "etag-v1"                           |
          |-------------------------------------------------->|
          |  6. 201 Created or 204 No Content (ETag: "etag-v2")|
          |<--------------------------------------------------|
```

### Key HTTP Methods in CalDAV
1. **`PROPFIND`**: Fetches properties of resources (e.g., `displayname`, `calendar-home-set`, `supported-calendar-component-set`). Used during initial discovery.
2. **`REPORT`**: Executes targeted queries against calendar collections. The most common report is `calendar-query`, which filters events based on `time-range` parameters.
3. **`MKCALENDAR`**: Creates a new calendar collection under a specific WebDAV collection.
4. **`PUT`**: Uploads or updates an iCalendar object (`.ics` file) containing `VEVENT` or `VTODO` blocks. Concurrency control is strictly handled via HTTP `If-Match` / `If-None-Match` headers with ETags.
5. **`DELETE`**: Removes an event or calendar resource from the server.

## Strengths
- **Strict Data Sovereignty**: Self-hosted CalDAV deployments store scheduling data locally on user hardware (ZFS/NVMe storage), mitigating cloud compliance, telemetry, and security risks.
- **Protocol Maturity & Stability**: Standardized via IETF RFC 4791 and RFC 5545, guaranteeing long-term client stability without sudden API breaking changes or vendor deprecations.
- **Granular Concurrency & Locking**: Leverages HTTP ETag headers and WebDAV locking mechanisms to prevent overwriting conflicting updates from multiple devices or agents.
- **Integrated Task Management**: Supports `VTODO` components alongside `VEVENT` entries, allowing unified calendar and task sync within a single storage engine.
- **Native AI Agent Compatibility**: Highly structured iCalendar payloads are easily parsed and validated using Pydantic v2 schemas in FastMCP 3.1 tool implementations.

## Limitations
- **Complex URL Discovery**: CalDAV endpoints differ significantly between implementations (e.g., Nextcloud: `/remote.php/dav/calendars/user/name/`, Radicale: `/user/calendar.ics/`). Agents must implement multi-step WebDAV `PROPFIND` discovery routines.
- **Timezone Resolution Overhead**: iCalendar data uses VTIMEZONE blocks or Olson timezone IDs (e.g., `America/New_York`). Improperly handling UTC offsets or Daylight Saving Time transitions can lead to subtle scheduling errors.
- **Sync Overhead at Scale**: Large calendar stores containing thousands of historical events can experience high resource loads during full sync operations unless strict `time-range` `REPORT` queries are enforced.

## When to use it
- When operating a sovereign, private home-lab setup using [Nextcloud](../../services/nextcloud.md) or [Radicale](../../services/radicale.md).
- When integrating autonomous AI scheduling tools via [FastMCP 3.1](../automation_orchestration/mcp.md) that require standards-compliant calendar CRUD capabilities.
- When orchestrating cross-application task and event synchronization across [n8n](../../services/n8n.md), [Home Assistant](../../services/home-assistant.md), and desktop/mobile devices.

## When not to use it
- If your environment relies purely on proprietary Google Workspace or Microsoft 365 services where native REST APIs (Google Calendar API or Graph API) are enforced.
- When building lightweight, ephemeral event queues that do not require standard client display or calendar UI representation.

## Getting started

Deployment of a lightweight, high-performance CalDAV server using **Radicale**:

```bash
# Deploy Radicale CalDAV server via Docker
docker run -d \
  --name radicale \
  -p 5232:5232 \
  -v /opt/radicale/data:/data \
  -v /opt/radicale/config:/config:ro \
  --restart unless-stopped \
  tomsun/radicale
```

### Basic Radicale Configuration (`config`)
```ini
[server]
hosts = 0.0.0.0:5232

[auth]
type = htpasswd
htpasswd_filename = /config/users
htpasswd_encryption = md5

[storage]
type = filesystem
filesystem_folder = /data/collections
```

Once deployed, connect clients or agent servers to `http://localhost:5232/user/calendar_name/`.

## CLI examples

### 1. Principal & Calendar Discovery via Curl
Use WebDAV `PROPFIND` to discover the calendar home set for an authenticated user:

```bash
curl -u 'username:password' -X PROPFIND \
  -H "Depth: 1" \
  -H "Content-Type: application/xml; charset=utf-8" \
  -d '<?xml version="1.0" encoding="utf-8" ?>
      <D:propfind xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
        <D:prop>
          <D:displayname />
          <C:calendar-description />
          <C:supported-calendar-component-set />
        </D:prop>
      </D:propfind>' \
  https://caldav.example.com/remote.php/dav/calendars/username/
```

### 2. Time-Range REPORT Query
Query events occurring within a specific UTC window:

```bash
curl -u 'username:password' -X REPORT \
  -H "Depth: 1" \
  -H "Content-Type: application/xml; charset=utf-8" \
  -d '<?xml version="1.0" encoding="utf-8" ?>
      <C:calendar-query xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
        <D:prop>
          <D:getetag />
          <C:calendar-data />
        </D:prop>
        <C:filter>
          <C:comp-filter name="VCALENDAR">
            <C:comp-filter name="VEVENT">
              <C:time-range start="20270101T000000Z" end="20270131T235959Z"/>
            </C:comp-filter>
          </C:comp-filter>
        </C:filter>
      </C:calendar-query>' \
  https://caldav.example.com/remote.php/dav/calendars/username/personal/
```

### 3. Inserting a New Event via PUT with Concurrency Guard
Insert a new `VEVENT` with strict HTTP headers:

```bash
curl -u 'username:password' -X PUT \
  -H "Content-Type: text/calendar; charset=utf-8" \
  -H "If-None-Match: *" \
  -d $'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Sovereign AI//FastMCP CalDAV//EN\r\nBEGIN:VEVENT\r\nUID:event-20270107T120000-001@riera.co.uk\r\nDTSTAMP:20270107T080000Z\r\nDTSTART:20270108T140000Z\r\nDTEND:20270108T150000Z\r\nSUMMARY:Agent Maintenance Window\r\nDESCRIPTION:Automated FastMCP 3.1 schedule optimization run.\r\nLOCATION:Home Lab Server Room\r\nEND:VEVENT\r\nEND:VCALENDAR' \
  https://caldav.example.com/remote.php/dav/calendars/username/personal/event-20270107T120000-001.ics
```

## API examples

### Production-Grade FastMCP 3.1 CalDAV Tool Server

This server provides an agent interface for querying and creating CalDAV calendar events using Pydantic v2 schemas and python `caldav` integration:

```python
import os
from datetime import datetime
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError, field_validator
import caldav

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Sovereign-CalDAV-Gateway")

# Environment Credentials
CALDAV_URL = os.getenv("CALDAV_URL", "http://localhost:5232/")
CALDAV_USER = os.getenv("CALDAV_USER", "admin")
CALDAV_PASS = os.getenv("CALDAV_PASS", "secret_pass")

# --- Pydantic v2 Validation Schemas ---

class CalendarEventQuery(BaseModel):
    calendar_name: str = Field(default="personal", description="Target CalDAV calendar display name")
    start_time: datetime = Field(..., description="Query start range in ISO 8601 format (UTC)")
    end_time: datetime = Field(..., description="Query end range in ISO 8601 format (UTC)")

    @field_validator("end_time")
    def validate_time_window(cls, v: datetime, info):
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("end_time must be strictly greater than start_time")
        return v

class CreateEventInput(BaseModel):
    calendar_name: str = Field(default="personal", description="Target calendar collection")
    summary: str = Field(..., min_length=1, max_length=500, description="Title of the calendar event")
    start_time: datetime = Field(..., description="Event start time in ISO 8601 UTC")
    end_time: datetime = Field(..., description="Event end time in ISO 8601 UTC")
    description: Optional[str] = Field(None, description="Detailed event summary or agent notes")
    location: Optional[str] = Field(None, description="Physical address or meeting URL")

class CalendarEventResponse(BaseModel):
    uid: str = Field(..., description="Unique iCalendar UID")
    etag: Optional[str] = Field(None, description="HTTP ETag header for concurrency locking")
    summary: str = Field(..., description="Event title")
    start_time: datetime = Field(..., description="Event start")
    end_time: datetime = Field(..., description="Event end")
    description: Optional[str] = None
    location: Optional[str] = None

# --- Helper Utilities ---

def get_caldav_client() -> caldav.DAVClient:
    return caldav.DAVClient(
        url=CALDAV_URL,
        username=CALDAV_USER,
        password=CALDAV_PASS
    )

# --- FastMCP 3.1 Tool Definitions ---

@mcp.tool(
    name="caldav_query_events",
    description="Queries events from a CalDAV calendar within a specified UTC time range."
)
def query_events(payload: CalendarEventQuery) -> List[CalendarEventResponse]:
    """Retrieves and validates events from CalDAV store within a given window."""
    client = get_caldav_client()
    principal = client.principal()
    calendars = principal.calendars()

    target_cal = None
    for cal in calendars:
        if payload.calendar_name.lower() in str(cal.name).lower():
            target_cal = cal
            break

    if not target_cal:
        if calendars:
            target_cal = calendars[0]
        else:
            raise RuntimeError("No CalDAV calendars accessible for this account.")

    raw_events = target_cal.date_search(
        start=payload.start_time,
        end=payload.end_time,
        expand=True
    )

    results: List[CalendarEventResponse] = []
    for item in raw_events:
        try:
            vevent = item.vobject_instance.vevent
            event_obj = CalendarEventResponse(
                uid=str(vevent.uid.value),
                etag=str(item.etag) if hasattr(item, "etag") else None,
                summary=str(vevent.summary.value),
                start_time=vevent.dtstart.value if isinstance(vevent.dtstart.value, datetime) else datetime.combine(vevent.dtstart.value, datetime.min.time()),
                end_time=vevent.dtend.value if isinstance(vevent.dtend.value, datetime) else datetime.combine(vevent.dtend.value, datetime.min.time()),
                description=str(vevent.description.value) if hasattr(vevent, "description") else None,
                location=str(vevent.location.value) if hasattr(vevent, "location") else None
            )
            results.append(event_obj)
        except (AttributeError, ValidationError) as err:
            continue

    return results

@mcp.tool(
    name="caldav_create_event",
    description="Creates a new iCalendar event on a designated CalDAV server collection."
)
def create_event(payload: CreateEventInput) -> CalendarEventResponse:
    """Validates input payload and creates a VEVENT record on the CalDAV server."""
    client = get_caldav_client()
    principal = client.principal()
    calendars = principal.calendars()

    if not calendars:
        raise RuntimeError("No accessible CalDAV calendars found.")

    calendar = calendars[0]

    new_event = calendar.save_event(
        dtstart=payload.start_time,
        dtend=payload.end_time,
        summary=payload.summary,
        description=payload.description or "",
        location=payload.location or ""
    )

    vevent = new_event.vobject_instance.vevent
    return CalendarEventResponse(
        uid=str(vevent.uid.value),
        etag=str(new_event.etag) if hasattr(new_event, "etag") else None,
        summary=str(vevent.summary.value),
        start_time=payload.start_time,
        end_time=payload.end_time,
        description=payload.description,
        location=payload.location
    )

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Nextcloud](../../services/nextcloud.md): Comprehensive self-hosted productivity suite featuring integrated CalDAV server support.
- [Radicale](../../services/radicale.md): Lightweight, filesystem-backed CalDAV and CardDAV server.
- [Vikunja](../../services/vikunja.md): Sovereign task management framework with CalDAV VTODO synchronization.
- [Chronos / Calendar Mapping Rules](../../reference-implementations/calendar/mapping-rules.md): Reference standards for AI event extraction and transformation.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Standard protocol for agent tool execution and context integration.
- [Home Assistant](../../services/home-assistant.md): IoT automation hub using CalDAV calendar triggers for state management.
- [Paperless-ngx](../../services/paperless-ngx.md): Document archiving platform integrated with AI extraction pipelines to auto-generate CalDAV events.

## Sources / references
- [RFC 4791: Calendaring Extensions to WebDAV (CalDAV)](https://datatracker.ietf.org/doc/html/rfc4791)
- [RFC 5545: Internet Calendaring and Scheduling Core Object Specification (iCalendar)](https://datatracker.ietf.org/doc/html/rfc5545)
- [CalDAV Developer Guide & Specifications](http://caldav.org/)
- [Radicale CalDAV Server Documentation](https://radicale.org/v3.html)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/3.1/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
