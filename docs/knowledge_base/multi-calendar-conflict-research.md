# Multi-Calendar Conflict Detection Research

Research into techniques and tools for identifying scheduling conflicts across multiple calendars (Google Calendar and CalDAV).

## What it is
A set of methods to aggregate availability data from multiple sources (e.g., family members' calendars) and calculate overlapping "busy" periods to find suitable meeting or event times.

## What problem it solves
Prevents double-booking and simplifies scheduling in a multi-user or multi-account environment by automating the check for availability across disparate calendar systems.

## Where it fits in the stack
**Knowledge Base / Pattern**. It informs the logic used in automation tools like [n8n](../services/n8n.md) to orchestrate calendar events.

## Typical use cases
- Husband and wife coordinating family events.
- Scheduling personal tasks without conflicting with work meetings.
- Automated appointment booking agents checking multiple providers.

## Strengths
- **Privacy-First**: Using Free/Busy APIs allows checking availability without exposing event details (titles, descriptions).
- **Interoperability**: Can combine data from Google Calendar and self-hosted CalDAV servers.

## Limitations
- **Latency**: Multiple API calls are required to fetch data from different providers.
- **Complexity**: Timezone handling and recurring event expansion must be managed correctly by the logic layer.

## When to use it
- When scheduling requires coordination between two or more independent calendar accounts.
- When an AI agent needs to suggest non-conflicting time slots.

## When not to use it
- For simple, single-account scheduling where a native "Check Availability" feature already exists.

## Implementation Details

### Google Calendar Free/Busy API
The Google Calendar API provides a `freebusy.query` method that returns blocks of busy time for one or more calendars.

**Example Request (Python):**
```python
body = {
  "timeMin": "2026-05-01T00:00:00Z",
  "timeMax": "2026-05-02T00:00:00Z",
  "items": [{"id": "user1@gmail.com"}, {"id": "user2@gmail.com"}]
}
eventsResult = service.freebusy().query(body=body).execute()
```
The response contains a dictionary of calendars, each with a list of `busy` periods (start and end times).

### Chronos MCP (CalDAV)
[Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) supports multi-account management for CalDAV servers (Nextcloud, Fastmail, etc.). It can be used to query multiple calendars simultaneously and aggregate their events for conflict analysis.

## Related tools / concepts
- [Google Calendar](../tools/calendar_tasks/google_calendar.md)
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md)
- [n8n](../services/n8n.md)

## Sources / references
- [Google Calendar Free/Busy API Documentation](https://developers.google.com/calendar/api/v3/reference/freebusy/query)
- [Cronofy Free/Busy API Notes](https://docs.cronofy.com/developers/api/events/free-busy/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
