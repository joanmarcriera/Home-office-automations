# Google Calendar

## What it is
Google Calendar is a cloud-based time-management and scheduling service. It allows users to manage multiple calendars, share schedules with others, and integrate event data into third-party applications via its extensive REST API.

## What problem it solves
It provides a centralized, universally accessible source of truth for scheduling. It solves the fragmentation of time management by offering multi-device synchronization, automated reminders, and a robust platform for collaborative scheduling across organizations.

## Where it fits in the stack
**Orchestration / Productivity**. In the homelab stack, it often serves as a primary destination for events extracted from documents by AI agents or as a trigger for automation workflows in [n8n](../../services/n8n.md).

## Typical use cases
- **Automated Event Creation**: Extracting dates from scanned receipts (via [Paperless-ngx](../../services/paperless-ngx.md)) and adding them to the calendar.
- **Availability Monitoring**: Using "Free/Busy" polling to detect schedule conflicts before booking appointments.
- **Home Automation Triggers**: Triggering Home Assistant "Scenes" based on the start or end time of specific calendar events.

## Strengths
- **Ubiquity**: Integrated into almost every mobile and desktop OS.
- **API Maturity**: The Google Calendar API is well-documented and supported by nearly all automation platforms (n8n, Make, Zapier).
- **Collaboration**: Rich support for shared calendars, event invitations, and public holiday feeds.

## Limitations
- **Privacy**: Data is hosted by Google, which may be a concern for privacy-conscious users.
- **Connectivity**: Requires an internet connection for real-time synchronization.
- **Complexity**: Managing OAuth2 credentials for API access can be challenging for beginners.

## When to use it
- When you need a widely compatible calendar with strong API support.
- When collaborating with others who already use Google Workspace or personal Gmail accounts.
- As a backing store for [Chronos MCP](../automation_orchestration/chronos-mcp.md) or other agentic calendar tools.

## When not to use it
- When absolute data sovereignty is required (use [Nextcloud Calendar](../../services/nextcloud.md) or [Radicale](../../services/radicale.md) instead).
- For high-frequency "journaling" where local, low-latency storage is preferred.

## Getting Started: Python API Example

Using the `google-api-python-client` to create an event and check availability.

```python
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Scopes required for calendar management
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'path/to/credentials.json'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=creds)

# 1. Create an Event
event = {
  'summary': 'AI Sync Meeting',
  'location': 'Home Office',
  'start': {'dateTime': '2026-05-20T10:00:00Z'},
  'end': {'dateTime': '2026-05-20T11:00:00Z'},
}
event = service.events().insert(calendarId='primary', body=event).execute()
print(f"Event created: {event.get('htmlLink')}")

# 2. Check Free/Busy Status
body = {
  "timeMin": "2026-05-20T00:00:00Z",
  "timeMax": "2026-05-20T23:59:59Z",
  "items": [{"id": "primary"}]
}
res = service.freebusy().query(body=body).execute()
busy_slots = res['calendars']['primary']['busy']
print(f"Busy slots for today: {busy_slots}")
```

## n8n Integration Patterns

| Pattern | Nodes Used | Description |
| :--- | :--- | :--- |
| **Intake to Calendar** | `Paperless-ngx` -> `Ollama` -> `Google Calendar` | Extract date from PDF and create event. |
| **Conflict Notifier** | `Google Calendar` (Trigger) -> `Telegram` | Send an alert if a new event overlaps with a protected slot. |
| **Daily Briefing** | `Google Calendar` -> `n8n AI Agent` -> `Telegram` | Summarize today's schedule at 8:00 AM. |

## Related tools / concepts
- [Nextcloud Calendar](../../services/nextcloud.md)
- [Proton Calendar](proton_calendar.md)
- [Radicale](../../services/radicale.md)
- [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md)
- [Chronos MCP](../automation_orchestration/chronos-mcp.md)
- [n8n](../../services/n8n.md)
- [Make](../automation_orchestration/make.md)
- [Paperless-ngx](../../services/paperless-ngx.md)

## Sources / references
- [Official Website](https://calendar.google.com/)
- [Google Calendar API v3 Documentation](https://developers.google.com/calendar/api/v3/reference)
- [Python Quickstart - Google Calendar API](https://developers.google.com/calendar/api/quickstart/python)

## Contribution Metadata

- Last reviewed: 2026-05-15
- Confidence: high
