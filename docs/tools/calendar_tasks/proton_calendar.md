# Proton Calendar

## What it is
Proton Calendar is a privacy-focused, end-to-end encrypted (E2EE) calendar service developed by Proton. As of late November/December 2026, it is a key component of the privacy-first productivity suite, offering a secure alternative to mainstream providers for users of frontier models like Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.6 who prioritize data sovereignty and secure agentic scheduling.

## What problem it solves
It provides a secure and private way to manage schedules and events without exposing sensitive metadata to service providers or third-party advertisers. By using client-side encryption, it ensures that event titles, locations, and participants remain confidential even if the service provider's infrastructure is compromised. It solves the privacy gap in digital life management.

## Where it fits in the stack
**Orchestration / Personal Information Management (PIM)**. It serves as the secure scheduling layer for individuals and teams who have migrated away from surveillance-based ecosystems like Google Workspace or Microsoft 365.

## Typical use cases
- **Confidential Business Scheduling**: Managing sensitive meetings, legal appointments, or medical schedules.
- **Secure Event Invitations**: Sending and receiving encrypted invitations within the Proton ecosystem.
- **Privacy-First Homelab Integration**: Using iCal secret links to display schedules in [Home Assistant](../../services/home-assistant.md) without exposing the full calendar.
- **Cross-Platform Sync**: Maintaining a synchronized, encrypted schedule across web, Android, iOS, and desktop.
- **Agentic Scheduling**: Interfacing with [Chronos MCP](../automation_orchestration/chronos-mcp.md) or **FastMCP 3.1** servers for automated, private calendar management.

## Strengths
- **End-to-End Encryption (E2EE)**: All major event fields (title, description, location) are encrypted before leaving the device.
- **Zero-Access Architecture**: Proton cannot access your calendar data; they only store the encrypted blobs.
- **Open Source Clients**: The web and mobile applications are open source and subject to independent security audits.
- **Standardized Import/Export**: Robust support for the `.ics` (iCalendar) format for migration.
- **Enhanced Sync (2026)**: Improved real-time sync across devices using the latest Proton Bridge protocols and secure desktop bridge services.

## Limitations
- **Automation Complexity**: The E2EE nature makes it difficult for third-party automation tools (like [n8n](../../services/n8n.md) or Zapier) to interact with the data directly without user-side decryption.
- **No Native CalDAV**: Lacks native, server-side CalDAV support for legacy desktop applications (though Proton Bridge provides proxy capabilities).
- **Read-Only External Sync**: Integration with external tools often relies on "Secret Links" which are read-only.

## When to use it
- When privacy and data security are the primary requirements for your schedule.
- If you are already integrated into the Proton ecosystem (Mail, Drive, VPN).
- For managing highly sensitive appointments where even metadata leaks are a concern.

## When not to use it
- If you require high-frequency, bidirectional automation with third-party tools that don't support E2EE.
- If your workflow depends on native CalDAV access for older desktop calendar clients (see [CalDAV](../intake_storage/caldav.md)).
- When collaborative features (like complex resource booking) found in enterprise Google/Microsoft suites are required.

## Getting started

### Account Setup
Create a Proton account at [proton.me](https://proton.me). Proton Calendar is included in the free tier, with expanded features available for paid plans.

### Data Migration
1. Export your existing calendar from [Google Calendar](google_calendar.md) or Outlook as an `.ics` file.
2. In Proton Calendar, navigate to **Settings** > **Import**.
3. Upload the `.ics` file to populate your new calendar.

## CLI examples

### Fetching a Secret iCal Link
While there is no official CLI for direct event manipulation, you can use `curl` to fetch your calendar's secret link for read-only automation:

```bash
# Fetch the latest schedule from a Proton Secret Link
curl -s "https://calendar.proton.me/api/calendar/v1/share/SECRET_TOKEN/export.ics" > schedule.ics

# Count the number of upcoming events in the next month (simple grep)
grep "BEGIN:VEVENT" schedule.ics | wc -l
```

### Validating an Exported ICS
Use `icalendar` (Python-based CLI tool) to inspect the structure of an exported Proton calendar:

```bash
# Install tool
pip install icalendar pydantic

# Inspect events
icalendar view schedule.ics
```

## API examples

### Parsing and Validating Proton iCal Feeds (Python with Pydantic v2)
Since direct API access is restricted by E2EE, most developers interact with Proton Calendar via the read-only iCal feed. This example retrieves an encrypted or shared iCal feed, parses its events, and validates them with strict **Pydantic v2** schemas to ensure structural integrity before processing by AI agents.

```python
import requests
from icalendar import Calendar
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional, List
from datetime import datetime

class ProtonEventSchema(BaseModel):
    uid: str = Field(..., description="Unique event identifier")
    summary: str = Field(..., min_length=1, description="Event title or subject")
    description: Optional[str] = Field(None, description="Event description details")
    dtstart: datetime = Field(..., description="Event start date and time")
    dtend: datetime = Field(..., description="Event end date and time")

    @field_validator('dtend')
    @classmethod
    def validate_end_after_start(cls, dtend: datetime, info) -> datetime:
        dtstart = info.data.get('dtstart')
        if dtstart and dtend < dtstart:
            raise ValueError("Event end time cannot be before event start time")
        return dtend

# Secret shared URL from Proton Calendar settings
SECRET_URL = "https://calendar.proton.me/api/calendar/v1/share/TOKEN/export.ics"

def get_and_validate_proton_events() -> List[ProtonEventSchema]:
    # For simulation, we use mock iCal content
    sample_ics = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:evt-2026-abc123
SUMMARY:Secure Agentic Architecture Review
DESCRIPTION:Reviewing FastMCP 3.1 implementations with Llama 4 and Claude 5.1
DTSTART:2026-12-25T14:00:00Z
DTEND:2026-12-25T15:00:00Z
END:VEVENT
END:VCALENDAR"""

    # In a live environment, fetch the real feed:
    # response = requests.get(SECRET_URL)
    # cal = Calendar.from_ical(response.content)

    cal = Calendar.from_ical(sample_ics)
    events_list = []

    for component in cal.walk():
        if component.name == "VEVENT":
            try:
                # Build raw payload dictionary
                raw_payload = {
                    "uid": str(component.get('uid')),
                    "summary": str(component.get('summary')),
                    "description": str(component.get('description')) if component.get('description') else None,
                    "dtstart": component.get('dtstart').dt,
                    "dtend": component.get('dtend').dt
                }
                # Strictly validate with Pydantic v2
                validated = ProtonEventSchema.model_validate(raw_payload)
                events_list.append(validated)
            except ValidationError as e:
                print(f"Skipping invalid event {component.get('uid')}:", e.json())
            except Exception as ex:
                print(f"Parsing error: {ex}")

    return events_list

if __name__ == "__main__":
    for event in get_and_validate_proton_events():
        print(f"Successfully Validated: {event.summary} ({event.dtstart} -> {event.dtend})")
```

## Related tools / concepts
- [Google Calendar](google_calendar.md) — The primary alternative being replaced.
- [Nextcloud Calendar](../../services/nextcloud.md) — Self-hosted E2EE-capable alternative.
- [CalDAV](../intake_storage/caldav.md) — The protocol standard for calendar sync.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) — MCP server for managing calendars.
- [Home Assistant](../../services/home-assistant.md) — Often consumes Proton iCal feeds for dashboard display.
- [n8n](../../services/n8n.md) — Workflow automation that can trigger from iCal feeds.
- [Proton Mail](../enterprise/proton-mail.md) — Tightly integrated secure email service.

## Sources / references
- [Proton Calendar Official Website](https://proton.me/calendar)
- [Proton Calendar Security Model](https://proton.me/blog/proton-calendar-security-model)
- [How to use Proton Calendar](https://proton.me/support/proton-calendar-basics)
- [Proton Bridge Documentation](https://proton.me/mail/bridge)

## Contribution Metadata
- Last reviewed: 2026-12-21
- Confidence: high
