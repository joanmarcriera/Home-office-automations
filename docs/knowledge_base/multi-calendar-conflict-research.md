# Multi-Calendar Conflict Detection Research

## What it is
Research and technical methodology for identifying and resolving scheduling conflicts across multiple disparate calendar systems (e.g., Google Calendar, CalDAV, iCloud). In 2026, this research underpins the "Proactive AI Scheduling" pattern, where agents manage availability across professional and personal boundaries.

## What problem it solves
Prevents double-booking and optimizes time allocation in multi-user or multi-account environments. It automates the complex task of aggregating availability data while preserving privacy and handling time-zone/recurrence edge cases.

## Where it fits in the stack
**Knowledge Base / Pattern**. It informs the logic used in orchestration tools like [n8n](../services/n8n.md) and provides the architectural blueprint for custom [MCP servers](../tools/frameworks/microsoft-agent-framework.md) specialized in time management.

## Typical use cases
- **Household Coordination**: Harmonizing calendars between family members to find common free time.
- **Deep Work Protection**: Automatically blocking focus time on a work calendar based on personal commitments.
- **Agentic Appointment Booking**: Enabling AI agents to schedule meetings by checking multiple providers' real-time availability.
- **Event-Driven Rescheduling**: Triggering re-optimization when a high-priority event creates a conflict.

## Strengths
- **Privacy-Preserving**: Can utilize "Free/Busy" status without requiring full event details (titles, descriptions).
- **Interoperability**: Bridges the gap between cloud providers (Google/O365) and self-hosted CalDAV solutions (Nextcloud/Radicale).
- **Holistic View**: Provides a single "source of truth" for availability without needing to merge data into one physical calendar.
- **Automation Ready**: High-quality JSON outputs from Free/Busy APIs are easily consumed by LLM agents.

## Limitations
- **API Latency**: Fetching data from multiple providers can introduce delays in real-time agentic responses.
- **Recurrence Complexity**: Handling varied "recurring event" logic across different standards (iCal vs. GCal) remains technically challenging.
- **Write-Back Complexity**: Identifying a conflict is easier than automatically resolving it in a way that satisfies all stakeholders.

## When to use it
- When you manage more than two independent calendar accounts.
- When an AI agent needs to act as a personal scheduler or executive assistant.
- When you want to automate "energy-aware" scheduling based on diverse life commitments.

## When not to use it
- For simple, single-account scheduling where native "Find a Time" features are sufficient.
- When users have low trust in providing an agent with broad (even read-only) calendar access.

## Getting started

### Key Concepts
1.  **Aggregation**: Collecting events from all sources into a unified timeline.
2.  **Normalization**: Converting all events to UTC and expanding recurrences.
3.  **Conflict Matrix**: Calculating overlapping busy intervals.

### Recommended Tooling
- **Chronos MCP**: For CalDAV integration.
- **Google Calendar API**: For cloud-native integration.
- **n8n Calendar Nodes**: For visual orchestration.

## CLI examples

### Querying Google Free/Busy (via gcloud/curl)
```bash
# Example of querying the freebusy endpoint for two calendars
curl -X POST "https://www.googleapis.com/calendar/v3/freeBusy" \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json" \
     -d '{
           "timeMin": "2026-06-20T00:00:00Z",
           "timeMax": "2026-06-21T00:00:00Z",
           "items": [{"id": "work@company.com"}, {"id": "home@gmail.com"}]
         }'
```

## API examples

### Conflict Detection Logic (Python)
```python
def find_conflicts(calendar_a_busy, calendar_b_busy):
    conflicts = []
    for interval_a in calendar_a_busy:
        for interval_b in calendar_b_busy:
            # Simple overlap check
            if interval_a['start'] < interval_b['end'] and interval_b['start'] < interval_a['end']:
                conflicts.append({
                    'start': max(interval_a['start'], interval_b['start']),
                    'end': min(interval_a['end'], interval_b['end'])
                })
    return conflicts
```

## Related tools / concepts
- [Google Calendar](../tools/calendar_tasks/google_calendar.md)
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md)
- [n8n](../services/n8n.md)
- [Motion](../tools/calendar_tasks/motion.md) (AI-driven scheduling)
- [Reclaim AI](../tools/calendar_tasks/reclaim-ai.md) (Automated focus blocks)
- [Radicale Automation](../services/radicale-automation.md) (Self-hosted CalDAV)
- [Home Assistant](../services/home-assistant.md) (Calendar-triggered automations)
- [Jules Agent](../tools/ai_knowledge/jules.md) (Agentic orchestration)

## Sources / references
- [Google Calendar Free/Busy API Documentation](https://developers.google.com/calendar/api/v3/reference/freebusy/query)
- [CalDAV (RFC 4791) Specification](https://datatracker.ietf.org/doc/html/rfc4791)
- [Cronofy: The State of AI Scheduling 2026](https://docs.cronofy.com/developers/api/events/free-busy/)
- [Awesome Time Tracking: AI Scheduling Patterns](https://github.com/ever-works/awesome-time-tracking)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
