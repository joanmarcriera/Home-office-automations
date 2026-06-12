# CalDAV

## What it is
CalDAV (Calendaring Extensions to WebDAV) is an internet standard allowing a client to access scheduling information on a remote server. It extends the WebDAV (Web Distributed Authoring and Versioning) protocol and uses the iCalendar format for data exchange. As of June 2026, it remains the backbone of privacy-first, self-hosted scheduling ecosystems.

## What problem it solves
It provides an open, standardized protocol for calendar synchronization, enabling interoperability between different calendar clients (e.g., Apple Calendar, Thunderbird, Android apps) and servers (e.g., [Nextcloud](../../services/nextcloud.md), [Radicale](../../services/radicale.md), [Google Calendar](../calendar_tasks/google_calendar.md)) without vendor lock-in. It allows users to own their scheduling data while maintaining cross-device availability.

## Where it fits in the stack
**Infrastructure / Protocol**. It serves as the underlying "language" for calendar synchronization between self-hosted services and client applications.

## Typical use cases
- **Multi-Device Sync**: Keeping your personal schedule in sync across phone, laptop, and tablet.
- **Shared Calendars**: Coordinating schedules within a family or team using a self-hosted server.
- **Automation Triggers**: Using [n8n](../../services/n8n.md) or custom scripts to watch a CalDAV calendar and trigger actions.
- **Task Management**: Many CalDAV servers also support VTODO (tasks), allowing for synchronized todo lists via the same protocol.

## Strengths
- **Sovereignty**: Complete control over your private schedule when self-hosted.
- **Interoperability**: Works with nearly every major calendar application.
- **Open Standard**: Not dependent on the survival or pricing changes of a single company.
- **Simplicity**: Based on HTTP and XML, making it relatively easy to debug with standard web tools.

## Limitations
- **Discovery Complexity**: Finding the correct URL for a specific calendar can be frustrating (varies by server).
- **Sync Conflict Resolution**: Can be less robust than proprietary protocols (like Exchange/ActiveSync) in complex multi-user scenarios.
- **Authentication**: Modern OAuth2 flows can be difficult to implement for some legacy CalDAV clients.

## When to use it
- When building a self-hosted "sovereign" personal cloud.
- When you need to integrate calendar data into custom automation workflows.
- When you want to avoid proprietary "walled garden" calendar services.

## When not to use it
- If your entire organization is already on Google Workspace or Microsoft 365 and you don't need external integration.
- If you need advanced "room booking" or complex enterprise resource scheduling features.

## Getting started

### Self-Hosting a CalDAV Server
The easiest way to get started with a dedicated CalDAV server is [Radicale](../../services/radicale.md) or [Nextcloud](../../services/nextcloud.md).

```bash
# Simple Radicale docker run
docker run -d --name radicale \
    -p 5232:5232 \
    -v ~/radicale/data:/data \
    tomsquest/docker-radicale:latest
```

### Client Setup
1. **iOS/macOS**: Native support under "Add Account" -> "Other" -> "CalDAV Account".
2. **Android**: Requires a sync adapter like **DAVx⁵**.
3. **Thunderbird**: Native support via the "Calendar" tab.

## CLI examples

### Protocol Interaction (Curl)
You can interact with a CalDAV server directly using `curl` to perform a PROPFIND request to discover calendars.

```bash
curl -u 'user:password' -X PROPFIND \
  -H "Depth: 1" \
  -H "Content-Type: application/xml; charset=utf-8" \
  -d '<?xml version="1.0" encoding="utf-8" ?>
      <D:propfind xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
        <D:prop>
          <D:displayname />
          <C:calendar-description />
        </D:prop>
      </D:propfind>' \
  https://caldav.example.com/remote.php/dav/calendars/user/
```

### Radicale Maintenance
Use the `radicale` CLI to manage a self-hosted instance:
```bash
# Check the version of the installed Radicale package
python3 -m radicale --version
```

### Storage Verification
Verify the integrity of local collections:
```bash
python3 -m radicale --verify-storage
```

## API examples

### Python Integration (`caldav` library)
Programmatic access to calendars is common for automation scripts.

```python
import caldav
from datetime import datetime

# Connect to the server
client = caldav.DAVClient(
    url="https://caldav.example.com/remote.php/dav/",
    username="user",
    password="password"
)

principal = client.principal()
calendars = principal.calendars()

if calendars:
    calendar = calendars[0]
    # Fetch events for today
    events = calendar.date_search(
        start=datetime(2026, 6, 12),
        end=datetime(2026, 6, 13)
    )

    for event in events:
        print(f"Found event: {event.vobject_instance.vevent.summary.value}")
```

### Chronos MCP Configuration
Expose your CalDAV server to AI agents using [Chronos MCP](../automation_orchestration/chronos-mcp.md).

```json
{
  "mcpServers": {
    "chronos": {
      "command": "uvx",
      "args": ["-y", "chronos-mcp"],
      "env": {
        "CALDAV_URL": "https://caldav.example.com/remote.php/dav/",
        "CALDAV_USERNAME": "user",
        "CALDAV_PASSWORD": "password"
      }
    }
  }
}
```

## Related tools / concepts
- [Radicale](../../services/radicale.md): A popular suite that includes a robust CalDAV server.
- [Nextcloud](../../services/nextcloud.md): A full-featured private cloud with CalDAV support.
- [Vikunja](../../services/vikunja.md): A task manager that can sync via CalDAV.
- [Google Calendar](../calendar_tasks/google_calendar.md): A cloud provider that supports CalDAV access.
- [n8n](../../services/n8n.md): Can be used to automate CalDAV interactions.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md): Model Context Protocol server for CalDAV.
- [Home Assistant](../../services/home-assistant.md): Uses CalDAV for scheduling automation.
- [Authentik](../../services/authentik.md): Can provide SSO for CalDAV servers.

## Sources / references
- [RFC 4791: CalDAV Specification](https://tools.ietf.org/html/rfc4791)
- [Radicale Documentation](https://radicale.org/v3.html)
- [Python CalDAV Library GitHub](https://github.com/python-caldav/caldav)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
