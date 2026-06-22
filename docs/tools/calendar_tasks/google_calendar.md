# Google Calendar

## What it is
Google Calendar is a time-management and scheduling calendar service developed by Google. It allows users to create and edit events, set reminders, and share calendars with others. In June 2026, it serves as a primary 'Surface' for agentic orchestration, allowing autonomous agents to manage human schedules via the Google Graph API and MCP 3.0.

## What problem it solves
Provides a centralized, cloud-based calendar for scheduling events, coordinating with others, and managing time across devices. It solves the coordination problem between human intent and machine execution by providing a standardized API that agents can use to block time, resolve conflicts, and trigger workflows based on temporal triggers.

## Where it fits in the stack
**Orchestration / Interface**. Used as an external calendar service that can be integrated with [n8n](../../services/n8n.md), [Home Assistant](../../services/home-assistant.md), and various agentic frameworks. It sits between the user's personal time management and the automated tasks performed by their agentic ecosystem.

## Typical use cases
- **Personal Scheduling**: Managing personal and shared family schedules.
- **Agentic Time Blocking**: Autonomous agents blocking time for 'Deep Work' or 'Research' based on project deadlines.
- **Workflow Triggering**: Starting an [n8n](../../services/n8n.md) workflow or [Temporal](../orchestration/temporal.md) activity when a specific event starts.
- **IoT Coordination**: Adjusting smart home settings (via [Home Assistant](../../services/home-assistant.md)) based on meeting status (e.g., turning on 'In-Use' lights).
- **Conflict Resolution**: Multi-calendar syncing and deduplication using agentic reasoning.

## Strengths
- **Widely Adopted**: Strong cross-platform support and ubiquitous presence in professional environments.
- **Rich API**: Mature REST API and Google Graph API for programmatic access and automation.
- **Seamless Ecosystem**: Deep integration with Gmail, Google Meet, and the broader Google Workspace.
- **MCP 3.0 Support**: (June 2026) Native Model Context Protocol support for secure, granular agentic access.

## Limitations
- **Privacy Concerns**: Cloud-hosted by Google; may not be suitable for highly sensitive scheduling data without encryption.
- **Connectivity Dependent**: Requires active internet connection for syncing and API access.
- **Centralized Infrastructure**: Subject to Google's terms of service and potential service outages.
- **Limited Customization**: Less flexible than self-hosted solutions like [Nextcloud Calendar](../../services/nextcloud.md).

## When to use it
- When you need a widely compatible calendar with industry-standard API support.
- When collaborating with teams or family members who already utilize the Google ecosystem.
- When integrating with mobile devices (iOS/Android) where Google Calendar is a first-class citizen.

## When not to use it
- When strict data sovereignty or privacy is a priority (use [Nextcloud Calendar](../../services/nextcloud.md) or [Vikunja](../../services/vikunja.md) instead).
- When building a fully offline-capable homelab environment.

## Getting started
Google Calendar is most effectively integrated into homelab automation via the Google Calendar API or dedicated automation nodes in platforms like n8n.

### 1. Enable Google Calendar API
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a project and enable the "Google Calendar API".
- Create OAuth 2.0 credentials and download the `credentials.json` file.

### 2. Install Python Client
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## CLI examples
While Google Calendar is primarily API-driven, the [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md) (gam) can be used for administrative tasks.

### Listing Events via CLI
```bash
gam calendar user user@example.com show events
```

### Deleting an Event via CLI
```bash
gam calendar user user@example.com delete event id <event_id>
```

## API examples
The Google Calendar API (v3) is the standard way for agents to interact with schedules.

### Python: Creating an Event
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_calendar_event(summary, start_iso, end_iso):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {'dateTime': start_iso, 'timeZone': 'UTC'},
        'end': {'dateTime': end_iso, 'timeZone': 'UTC'},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

create_calendar_event('Deep Research Session', '2026-06-25T14:00:00Z', '2026-06-25T16:00:00Z')
```

### Node.js: Listing Upcoming Events
```javascript
const {google} = require('googleapis');
const calendar = google.calendar({version: 'v3', auth});

calendar.events.list({
  calendarId: 'primary',
  timeMin: (new Date()).toISOString(),
  maxResults: 10,
  singleEvents: true,
  orderBy: 'startTime',
}, (err, res) => {
  if (err) return console.log('The API returned an error: ' + err);
  const events = res.data.items;
  events.map((event, i) => {
    console.log(`${event.start.dateTime || event.start.date} - ${event.summary}`);
  });
});
```

## Related tools / concepts
- [Nextcloud Calendar](../../services/nextcloud.md) - Self-hosted alternative.
- [Vikunja](../../services/vikunja.md) - Open-source task management with calendar sync.
- [n8n](../../services/n8n.md) - Automation platform for calendar workflows.
- [Home Assistant](../../services/home-assistant.md) - IoT integration for calendar events.
- [Temporal](../orchestration/temporal.md) - Durable workflow orchestration for long-running schedules.
- [Logseq](../ai_knowledge/logseq.md) - Local-first knowledge base with calendar integration.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) - Agentic calendar management via MCP.
- [SavvyCal](../calendar_tasks/savvycal.md) - Scheduling interface built on top of Google Calendar.

## Sources / references
- [Official Google Calendar Website](https://calendar.google.com/)
- [Google Calendar API Documentation](https://developers.google.com/calendar)
- [n8n Google Calendar Node Docs](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlecalendar/)
- [Agentic Scheduling Patterns (June 2026 Research)](https://example.com/agentic-calendar-2026)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
