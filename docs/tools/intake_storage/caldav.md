# CalDAV

## What it is
CalDAV (Calendaring Extensions to WebDAV) is an internet standard allowing a client to access scheduling information on a remote server. It extends the WebDAV (Web Distributed Authoring and Versioning) protocol and uses the iCalendar format for data exchange. As of early January 2027, it remains the primary open standard for cross-vendor calendar synchronization in sovereign AI stacks, supporting FastMCP 3.1 Task Protocol integrations.

## What problem it solves
It provides an open, standardized protocol for calendar synchronization, enabling interoperability between different calendar clients (e.g., Apple Calendar, Thunderbird, Android apps) and servers (e.g., Nextcloud, Radicale, Baïkal, Google Calendar) without vendor lock-in. It allows users to own their scheduling data while maintaining cross-device availability.

## Where it fits in the stack
**Infrastructure / Protocol**. It serves as the underlying "language" for calendar synchronization between self-hosted services and client applications.

## Typical use cases
- **Multi-Device Sync**: Keeping your personal schedule in sync across phone, laptop, and tablet.
- **Shared Calendars**: Coordinating schedules within a family or team using a self-hosted server.
- **Automation Triggers**: Using [n8n](../../services/n8n.md) or custom scripts to watch a CalDAV calendar and trigger actions.
- **Task Management**: Many CalDAV servers also support VTODO (tasks), allowing for synchronized todo lists via the same protocol.
- **Agentic Scheduling**: Giving AI agents the ability to read and write to your schedule via standardized [MCP 3.1](../automation_orchestration/mcp.md) (FastMCP 3.1) servers.

## Strengths
- **Sovereignty**: Complete control over your private schedule when self-hosted.
- **Interoperability**: Works with nearly every major calendar application.
- **Open Standard**: Not dependent on the survival or pricing changes of a single company.
- **Simplicity**: Based on HTTP and XML, making it relatively easy to debug with standard web tools.
- **Task Support**: Native support for task synchronization (VTODO) alongside events.

## Limitations
- **Discovery Complexity**: Finding the correct URL for a specific calendar can be frustrating (varies by server).
- **Sync Conflict Resolution**: Can be less robust than proprietary protocols (like Exchange/ActiveSync) in complex multi-user scenarios.
- **Authentication**: Modern OAuth2 flows can be difficult to implement for some legacy CalDAV clients.

## When to use it
- When building a self-hosted "sovereign" personal cloud using [Nextcloud](../../services/nextcloud.md) or [Radicale](../../services/radicale.md).
- When you need to integrate calendar data into custom automation workflows.
- When you want to avoid proprietary "walled garden" calendar services like [Google Calendar](../calendar_tasks/google_calendar.md).

## When not to use it
- If your entire organization is already on Google Workspace or Microsoft 365 and you don't need external integration.
- If you need advanced "room booking" or complex enterprise resource scheduling features not well-supported by basic CalDAV.

## Getting started

The most common way to start with CalDAV is to deploy a dedicated server like **Radicale**.

```bash
# Deploy Radicale using Docker
docker run -d --name radicale \
    -p 5232:5232 \
    -v ~/radicale/data:/data \
    tomsun/radicale
```

Once running, you can connect clients by pointing them to `http://localhost:5232/user/calendar.ics/`.

## CLI examples

### 1. Discovery via Curl
Use `PROPFIND` to discover the display name and description of calendars.

```bash
curl -u 'user:password' -X PROPFIND \
  -H "Depth: 1" \
  -H "Content-Type: application/xml; charset=utf-8" \
  -d '<?xml version="1.0" encoding="utf-8" ?>
      <D:propfind xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
        <D:prop><D:displayname /><C:calendar-description /></D:prop>
      </D:propfind>' \
  https://caldav.example.com/remote.php/dav/calendars/user/
```

### 2. Verify Storage (Radicale)
Check the internal storage consistency of a Radicale server.

```bash
docker exec -it radicale radicale --verify-storage
```

### 3. Fetching iCal Data
Retrieve the raw iCalendar data for a specific calendar.

```bash
curl -u 'user:password' https://caldav.example.com/remote.php/dav/calendars/user/personal.ics
```

## API examples

### Python Integration with Strict Pydantic v2 Validation
To integrate CalDAV with AI agents using frontier models (e.g., **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, or **Qwen 3.6 VL**), schedules must be parsed and validated programmatically to avoid syntax injection and data corruption.

```python
import caldav
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, ValidationError

class CalendarEventSchema(BaseModel):
    uid: str = Field(..., description="Unique event identifier")
    summary: str = Field(..., min_length=1, max_length=1000, description="Brief title of the event")
    start_time: datetime = Field(..., alias="start", description="UTC start time")
    end_time: datetime = Field(..., alias="end", description="UTC end time")
    description: Optional[str] = Field(None, description="Detailed description of event context")
    location: Optional[str] = Field(None, description="Event physical location or virtual URL")

def parse_and_validate_caldav_event(raw_event: Any) -> CalendarEventSchema:
    """
    Parses a raw CalDAV VEVENT and validates it against the Pydantic v2 schema.
    """
    vevent = raw_event.vobject_instance.vevent
    try:
        event_data = {
            "uid": vevent.uid.value,
            "summary": vevent.summary.value,
            "start": vevent.dtstart.value,
            "end": vevent.dtend.value,
            "description": getattr(vevent, "description", None) and vevent.description.value,
            "location": getattr(vevent, "location", None) and vevent.location.value,
        }
        # Strict parsing and validation via model_validate
        return CalendarEventSchema.model_validate(event_data)
    except (AttributeError, ValidationError) as e:
        print(f"Failed to validate CalDAV object: {e}")
        raise

# Example connection loop
def fetch_verified_schedule(cal_url: str, user: str, sec: str) -> List[CalendarEventSchema]:
    client = caldav.DAVClient(url=cal_url, username=user, password=sec)
    principal = client.principal()
    calendars = principal.calendars()

    verified_events = []
    if calendars:
        calendar = calendars[0]
        # Query window
        events = calendar.date_search(start=datetime(2026, 12, 22), end=datetime(2026, 12, 23))
        for item in events:
            try:
                verified_events.append(parse_and_validate_caldav_event(item))
            except (ValidationError, AttributeError):
                continue
    return verified_events
```

## Related tools / concepts
- [Nextcloud](../../services/nextcloud.md): Suite that includes a robust CalDAV server.
- [Vikunja](../../services/vikunja.md): Task manager that can sync via CalDAV.
- [Google Calendar](../calendar_tasks/google_calendar.md): Cloud provider supporting CalDAV access.
- [n8n](../../services/n8n.md) or custom scripts to watch a CalDAV calendar and trigger actions.
- [Paperless-ngx](../../services/paperless-ngx.md): Trigger calendar events from documents.
- [Home Assistant](../../services/home-assistant.md): Scheduling automation.
- [Authentik](../../services/authentik.md): SSO for CalDAV servers.
- [Radicale](../../services/radicale.md): Lightweight CalDAV/CardDAV server.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Standard for tool use including scheduling.

## Sources / references
- [RFC 4791: CalDAV Specification](https://tools.ietf.org/html/rfc4791)
- [CalDAV.org](http://caldav.org/)
- [Radicale Documentation](https://radicale.org/v3.html)
- [FastMCP 3.1 Task Protocol for Calendaring](https://modelcontextprotocol.io/3.1/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
