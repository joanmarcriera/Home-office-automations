# Google Calendar

## What it is
Google Calendar is a time-management and scheduling calendar service developed by Google. It allows users to create and edit events, set reminders, and share calendars with others.

## What problem it solves
Provides a centralized, cloud-based calendar for scheduling events, coordinating with others, and managing time across devices.

## Where it fits in the stack
**Orchestration**. Used as an external calendar service that can be integrated with n8n and other automation tools.

## Typical use cases
- Managing personal and shared schedules
- Setting event reminders and notifications
- Integrating calendar events with automation workflows via the API

## Strengths
- Widely adopted with strong cross-platform support
- Rich API for programmatic access and automation
- Seamless integration with the Google ecosystem

## Limitations
- Cloud-hosted by Google; raises privacy concerns for sensitive scheduling data
- Depends on Google account and connectivity
- Limited customization compared to self-hosted calendar solutions

## When to use it
- When you need a widely compatible calendar with strong API support
- When collaborating with others who already use Google services

## When not to use it
- When privacy is a priority and self-hosting is preferred (use [Nextcloud Calendar](../../services/nextcloud.md) instead)
- When you need full control over your calendar data and infrastructure

## API and Automation Patterns
Google Calendar is often used as a central hub for agentic time-management. Common patterns include:
- **Event Conflict Resolution**: Using an agent to check for overlaps across multiple Google and Outlook calendars.
- **Smart Reminders**: Triggering IoT devices (via Home Assistant) based on upcoming calendar events.
- **Automatic Time Blocking**: Syncing tasks from logseq or Obsidian into dedicated calendar blocks.

## Advanced API Usage (v3)
The Google Calendar API allows for complex queries beyond simple event creation. For example, listing upcoming events with a specific query:
```python
# List the next 10 events from the primary calendar
events_result = service.events().list(
    calendarId='primary',
    timeMin=now,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime',
    q='Project Alpha'
).execute()
events = events_result.get('items', [])
```

## Getting started

Google Calendar is most effectively integrated into homelab automation via the Google Calendar API or n8n nodes.

### 1. Python SDK Example
Requires `google-api-python-client` and OAuth credentials.

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_event(summary, start_time, end_time):
    # Load credentials (simplified)
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'UTC'},
        'end': {'dateTime': end_time, 'timeZone': 'UTC'},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

# Example usage
create_event('Family Dinner', '2026-05-20T18:00:00Z', '2026-05-20T20:00:00Z')
```

### 2. n8n Integration
The **Google Calendar** node in n8n supports:
- **Trigger**: "Event Created", "Event Updated", or "Event Started".
- **Action**: "Create", "Update", "Delete", or "List" events.
- **Pattern**: Use a "Google Calendar Trigger" node linked to a "Telegram" node for real-time notification of family schedule changes.

## Related tools / concepts
- [Nextcloud Calendar](../../services/nextcloud.md)
- [Proton Calendar](proton_calendar.md)
- [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md)
- [n8n](../../services/n8n.md)
- [Home Assistant](../../services/home-assistant.md)
- [Logseq](../development_ops/logseq.md)
- [Obsidian](../development_ops/obsidian.md)
- [Fantastical](./fantastical.md)
- [Chronos MCP](../automation_orchestration/chronos-mcp.md)

## Sources / references
- [Official Website](https://calendar.google.com/)
- [API Documentation](https://developers.google.com/calendar)
- [n8n Google Calendar Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlecalendar/)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
