# Multi-Calendar Conflict Detection Research

## What it is
Multi-calendar conflict detection is the process of identifying overlapping events and availability gaps across disparate calendar systems (Google Calendar, Outlook, CalDAV). As of **early January 2027**, this has evolved from simple "busy" checks into **Agentic Calendar Orchestration**, where frontier models like Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, and Gemma 3 use the **MCP 3.1 Task Protocol** and **FastMCP 3.1** to automatically negotiate schedules across multiple personal and professional accounts with standardized execution, and resolve overlapping scheduling slots on behalf of users.

## What problem it solves
It prevents double-booking and "calendar sprawl" by providing a unified, unified view of availability. It solves the fragmentation problem in multi-user environments (e.g., family scheduling) and multi-role contexts (e.g., freelancer juggling multiple client calendars), automating the labor-intensive task of manual cross-referencing.

## Where it fits in the stack
**Category**: Knowledge Base / Pattern. It informs the logic layer of automation platforms like [n8n](../services/n8n.md) and [Home Assistant](../services/home-assistant.md). It serves as the primary data ingestion strategy for AI scheduling agents and "Focus Time" optimizers.

## Typical use cases
- **Multi-Account Coordination**: Automatically blocking "Personal" time on a work calendar when a family event is added.
- **Family Syncing**: Identifying the best 2-hour window for a 4-person family dinner across different providers.
- **Agentic Day Planning**: A "Daily Copilot" analyzing multiple calendars to proactively suggest rescheduling lower-priority tasks.
- **Focus Protection**: Automatically declining meeting invites that conflict with pre-existing deep work blocks.

## Strengths
- **Privacy-Preserving**: Leverages "Free/Busy" visibility levels to check availability without exposing sensitive event details.
- **Cross-Platform**: Bridges the gap between enterprise (Outlook/Google Workspace) and local-first (CalDAV/Nextcloud) ecosystems.
- **Real-Time Responsiveness**: Modern agentic flows can resolve conflicts within seconds of a new invite being received.
- **Context-Aware**: Can distinguish between "hard" conflicts (unmovable meetings) and "soft" conflicts (flexible personal tasks).

## Limitations
- **API Rate Limits**: Aggressive polling of multiple calendar APIs can lead to temporary blocks.
- **Sync Latency**: Changes made in one calendar may take several minutes to propagate through the orchestration layer.
- **Complex Recurring Logic**: Handling complex recurrence rules (e.g., "third Thursday of the month") across different implementations remains challenging.
- **Authorization Complexity**: Managing OAuth tokens and CalDAV credentials for multiple users requires robust secret management.

## When to use it
- When you manage more than two independent calendar accounts.
- When building an autonomous agent that needs to schedule its own tasks or meetings.
- When coordinating schedules across a group where participants use different calendar providers.

## When not to use it
- For single-account users where native "check availability" features are sufficient.
- In environments where calendar data is highly sensitive and cannot be exposed to an orchestration agent.
- For extremely simple "one-off" events that don't justify the setup of an orchestration layer.

## Getting started

### Local Orchestration with Python
The fastest way to start is using an orchestration library like `icalendar` or a framework-specific node in n8n.

1. **Install dependencies**:
   ```bash
   pip install icalendar requests google-api-python-client
   ```
2. **Setup Chronos MCP**:
   Follow the [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) guide to connect your CalDAV accounts.

### Dockerized Aggregator
Deploy a self-hosted aggregator like [Radicale](../services/radicale.md) to serve as a central proxy for multiple upstream calendars.

```yaml
# docker-compose.yml snippet
services:
  radicale:
    image: tomsoul/radicale
    container_name: radicale
    ports:
      - "5232:5232"
    volumes:
      - ./data:/data
```

## CLI examples

### Querying Google Calendar Availability
Using the `gcalcli` tool to check for conflicts:
```bash
# Search for events in a specific time range across all calendars
gcalcli agenda "2026-11-20 09:00" "2026-11-20 17:00"
```

### CalDAV Conflict Check via Curl
Querying a CalDAV server for busy periods:
```bash
curl -X REPORT -u 'user:pass' -H "Content-Type: text/xml" \
     --data '<c:free-busy-query xmlns:c="urn:ietf:params:xml:ns:caldav">
               <c:time-range start="20261120T000000Z" end="20261121T000000Z"/>
             </c:free-busy-query>' \
     https://calendar.example.com/dav/calendars/user/
```

## API examples

### Pydantic v2 Calendar Conflict Validation
Using **Pydantic v2** to model, parse, and validate calendar events, time ranges, and flexibility properties before triggering schedule negotiation:

```python
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import List

class CalendarEvent(BaseModel):
    """Pydantic model representing a single calendar event block."""
    event_id: str = Field(..., description="Unique event identifier")
    summary: str = Field(..., description="Brief description of the event")
    start_time: datetime = Field(..., description="Event start date/time")
    end_time: datetime = Field(..., description="Event end date/time")
    is_flexible: bool = Field(default=False, description="Whether event can be shifted if a conflict arises")

    @model_validator(mode="after")
    def validate_time_range(self) -> 'CalendarEvent':
        """Ensure end_time is chronologically after start_time."""
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be strictly after start_time")
        return self

class ConflictDetectionRequest(BaseModel):
    """Pydantic request payload validation model for cross-calendar conflict scans."""
    primary_events: List[CalendarEvent]
    secondary_events: List[CalendarEvent]

# Sample validation execution
event_data = {
    "event_id": "evt-109283",
    "summary": "AI Alignment Sync",
    "start_time": "2026-11-20T10:00:00Z",
    "end_time": "2026-11-20T11:00:00Z",
    "is_flexible": True
}
validated_event = CalendarEvent(**event_data)
print(f"Validated '{validated_event.summary}' event successfully (Flexible={validated_event.is_flexible}).")
```

### Agentic Conflict Detection (MCP 3.1 Task Protocol)
In November 2026, agents use the MCP 3.1 Task Protocol to query calendars and execute scheduling tasks. This example demonstrates how an agent might use a "Calendar Tool" to detect conflicts.

```python
import mcp_client

async def detect_calendar_conflicts(agent, start_time, end_time):
    # Agent calls the 'list_busy_times' tool via MCP 3.1 Task Protocol
    busy_blocks = await agent.call_tool(
        "chronos-mcp",
        "list_busy_times",
        {"start": start_time, "end": end_time}
    )

    # Process blocks to find overlaps
    conflicts = find_overlaps(busy_blocks)
    return conflicts

# Example logic for overlap detection
def find_overlaps(blocks):
    sorted_blocks = sorted(blocks, key=lambda x: x['start'])
    # ... standard interval overlap logic ...
    return overlaps
```

### Google Calendar Free/Busy API
```python
# Querying multiple calendars for Free/Busy status
body = {
  "timeMin": "2026-11-20T00:00:00Z",
  "timeMax": "2026-11-21T00:00:00Z",
  "items": [{"id": "work@company.com"}, {"id": "personal@gmail.com"}]
}
result = service.freebusy().query(body=body).execute()
```

## Related tools / concepts
- [Google Calendar](../tools/calendar_tasks/google_calendar.md) — Primary cloud provider.
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) — Agentic CalDAV orchestration.
- [n8n](../services/n8n.md) — Workflow automation for cross-calendar syncing.
- [Motion](../tools/calendar_tasks/motion.md) — AI-driven day planning and conflict resolution.
- [Reclaim](../tools/calendar_tasks/reclaim.md) — Automated focus time and habit scheduling.
- [Radicale](../services/radicale.md) — Self-hosted CalDAV server for local aggregation.
- [Nextcloud](../services/nextcloud.md) — Comprehensive suite with built-in multi-calendar support.
- [Home Assistant](../services/home-assistant.md) — Using calendar triggers for home automation.
- [Claude](../tools/ai_knowledge/claude.md) — Frontier model used for schedule negotiation.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Local model for privacy-preserving negotiation.

## Sources / references
- [Google Calendar Free/Busy API Documentation](https://developers.google.com/calendar/api/v3/reference/freebusy/query)
- [RFC 4791: CalDAV Scheduling Extensions](https://datatracker.ietf.org/doc/html/rfc4791)
- [MCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/spec/3.1/task-protocol)
- [Awesome Time Tracking: AI Scheduling Agents 2026](https://github.com/ever-works/awesome-time-tracking/blob/develop/details/ai-scheduling-agents-2026.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
