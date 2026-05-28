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

## 2026 State of the Industry: The Shift to Proactive Agents

As of May 2026, calendar management has shifted from manual conflict detection to **Proactive AI Scheduling Agents**. These agents don't just find free slots; they actively protect "Focus Time" and adapt to changing circumstances in real-time.

### Key 2026 Patterns
- **Adaptive Rescheduling**: Agents monitor actual vs. planned progress and automatically reschedule tasks when priorities shift or meetings run over.
- **Energy-Aware Scheduling**: Tasks are scheduled based on individual productivity patterns and chronotypes (e.g., complex tasks in the morning, admin in the afternoon).
- **Cross-Platform Coordination**: Seamlessly integrating work and personal calendars to ensure holistic availability without exposing private details.
- **Document-Driven Inputs**: Agents can analyze syllabi, project plans, or requirement documents to automatically generate time-blocked schedules.

## Strengths
- **Privacy-First**: Using Free/Busy APIs allows checking availability without exposing event details (titles, descriptions).
- **Interoperability**: Can combine data from Google Calendar and self-hosted CalDAV servers.
- **Proactive Management**: Modern agents can resolve conflicts before they appear on the user's radar.

## Limitations
- **Latency**: Multiple API calls are required to fetch data from different providers.
- **Complexity**: Timezone handling and recurring event expansion must be managed correctly by the logic layer.
- **Privacy Trust**: Requires significant access to personal data for energy-aware optimization.

## When to use it
- When scheduling requires coordination between two or more independent calendar accounts.
- When an AI agent needs to suggest non-conflicting time slots.
- When you want to automate the balancing of deep work and collaborative tasks.

## When not to use it
- For simple, single-account scheduling where a native "Check Availability" feature already exists.
- In low-trust environments where providing broad calendar access to an agent is not permissible.

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

### Chronos MCP (CalDAV)
[Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) supports multi-account management for CalDAV servers (Nextcloud, Fastmail, etc.). It can be used to query multiple calendars simultaneously and aggregate their events for conflict analysis.

## Best Practices for AI Scheduling (2026)
1.  **Define Hard Constraints**: Explicitly state "non-negotiables" (e.g., "no meetings before 9 AM") to guide agentic decisions.
2.  **Feedback Loops**: Rate scheduled blocks to help the AI learn your preferences over time.
3.  **Built-in Buffer Time**: Configure agents to automatically insert 10-15 minute buffers between transitions.
4.  **Syllabus Integration**: Use agents to parse educational or project timelines to pre-populate study/work blocks.

## Related tools / concepts
- [Google Calendar](../tools/calendar_tasks/google_calendar.md)
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md)
- [n8n](../services/n8n.md)
- [Motion](../tools/calendar_tasks/motion.md) (AI day planning)
- [Reclaim AI](../tools/calendar_tasks/reclaim-ai.md) (Smart focus blocks)

## Sources / references
- [Google Calendar Free/Busy API Documentation](https://developers.google.com/calendar/api/v3/reference/freebusy/query)
- [Cronofy Free/Busy API Notes](https://docs.cronofy.com/developers/api/events/free-busy/)
- [Awesome Time Tracking: AI Scheduling Agents 2026](https://github.com/ever-works/awesome-time-tracking/blob/develop/details/ai-scheduling-agents-2026.md)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
