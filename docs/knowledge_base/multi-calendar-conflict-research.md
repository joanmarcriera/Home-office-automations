# Multi-Calendar Conflict Detection Research

Research into techniques and tools for identifying scheduling conflicts across multiple calendars (Google Calendar and CalDAV).

## What it is
A set of methods to aggregate availability data from multiple sources (e.g., family members' calendars) and calculate overlapping "busy" periods to find suitable meeting or event times. In June 2026, this has evolved into "Agentic Calendar Orchestration," where autonomous agents manage these conflicts using the Model Context Protocol (MCP 3.0).

## What problem it solves
Prevents double-booking and simplifies scheduling in a multi-user or multi-account environment by automating the check for availability across disparate calendar systems. It solves the "fragmented availability" problem where one's true schedule is spread across work (Outlook), personal (Google), and family (Nextcloud) platforms.

## Where it fits in the stack
**Knowledge Base / Pattern**. It informs the logic used in automation tools like [n8n](../services/n8n.md) to orchestrate calendar events. It sits in the **Interaction Layer** of the [Home-Office Architecture](../architecture/README.md).

## Typical use cases
- **Household Coordination**: Husband and wife coordinating family events without sharing private event details.
- **Context-Aware Scheduling**: Scheduling personal tasks (e.g., gym) only during blocks that don't conflict with work meetings.
- **Automated Appointment Agents**: Booking agents checking multiple service provider calendars to find the first available slot.
- **Focus Time Protection**: Automatically blocking out time for deep work based on project deadlines and meeting density.

## Strengths
- **Privacy-First**: Using Free/Busy APIs allows checking availability without exposing event titles or descriptions.
- **Interoperability**: Combines data from Google Calendar, iCloud, and self-hosted CalDAV (Nextcloud) servers.
- **Proactive Management**: Modern agents can resolve conflicts before they appear on the user's radar using predictive scheduling.
- **MCP 3.0 Integration**: Standardized tool-use for calendars via MCP servers.

## Limitations
- **API Latency**: Querying multiple providers sequentially can be slow; requires parallel execution patterns.
- **Complexity**: Timezone handling, recurring event expansion, and "tentative" status management require robust logic.
- **Token Expiry**: Maintaining authenticated sessions across multiple OAuth2 providers (Google, Microsoft) adds maintenance overhead.

## When to use it
- When scheduling requires coordination between two or more independent calendar accounts.
- When an AI agent needs to suggest non-conflicting time slots for a task.
- When you want to automate the balancing of deep work and collaborative tasks across multiple platforms.

## When not to use it
- For simple, single-account scheduling where a native "Check Availability" feature already exists.
- In low-trust environments where providing broad calendar access to an agent is not permissible.
- For extremely time-sensitive scheduling where API latency of several seconds is unacceptable.

## Getting started

### Local Deployment of Google Calendar MCP
The fastest way to enable agentic conflict detection is to run the Google Calendar MCP server.

```bash
# Using npx to start the MCP server
npx -y @modelcontextprotocol/server-google-calendar
```

### Nextcloud (CalDAV) Integration
For self-hosted environments, use the Chronos MCP server to bridge CalDAV calendars to your agent.

1. Ensure your [Nextcloud](../services/nextcloud.md) instance is accessible.
2. Configure [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) with your CalDAV credentials.
3. Use the `get_events` tool to pull data from multiple calendars for a specific time range.

## CLI examples

### Querying Free/Busy via cURL (Google)
```bash
curl -X POST "https://www.googleapis.com/calendar/v3/freeBusy/query?key=YOUR_API_KEY" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "timeMin": "2026-06-20T00:00:00Z",
       "timeMax": "2026-06-21T00:00:00Z",
       "items": [{"id": "primary"}, {"id": "family123@group.calendar.google.com"}]
     }'
```

### Listing Calendars via MCP CLI
```bash
# List available calendars for the current authenticated user
mcp-cli call google-calendar list_calendars
```

## API examples

### Python: Multi-Source Conflict Checker
```python
import asyncio
from datetime import datetime, timedelta

async def check_conflicts(start_time, end_time):
    # Pseudocode for agentic orchestration
    google_busy = await call_mcp_tool("google-calendar", "get_free_busy", {
        "timeMin": start_time, "timeMax": end_time, "items": [{"id": "primary"}]
    })

    caldav_busy = await call_mcp_tool("chronos-mcp", "get_events", {
        "calendar": "personal", "start": start_time, "end": end_time
    })

    # Merge and find gaps
    conflicts = merge_busy_periods(google_busy, caldav_busy)
    return find_free_slots(start_time, end_time, conflicts)

# Run the check for the next 24 hours
asyncio.run(check_conflicts(datetime.now(), datetime.now() + timedelta(days=1)))
```

## Related tools / concepts
- [Google Calendar](../tools/calendar_tasks/google_calendar.md) - Primary public calendar provider.
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) - CalDAV bridge for agents.
- [n8n](../services/n8n.md) - Visual automation for calendar syncing.
- [Motion](../tools/calendar_tasks/motion.md) - AI-driven schedule optimization.
- [Reclaim AI](../tools/calendar_tasks/reclaim-ai.md) - Smart time-blocking.
- [Nextcloud](../services/nextcloud.md) - Self-hosted calendar and contact management.
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md) - The reasoning layer for scheduling.
- [Tool Calling and MCP](./patterns/tool-calling-and-mcp.md) - How agents interact with calendars.
- [Proton Calendar](../tools/calendar_tasks/proton_calendar.md) - Privacy-focused encrypted calendar.
- [Apple Calendar](../tools/calendar_tasks/apple-calendar.md) - Native ecosystem integration.

## Sources / references
- [Google Calendar Free/Busy API Documentation](https://developers.google.com/calendar/api/v3/reference/freebusy/query)
- [Model Context Protocol: Google Calendar Server](https://github.com/modelcontextprotocol/servers/tree/main/src/google-calendar)
- [Cronofy Free/Busy API Notes](https://docs.cronofy.com/developers/api/events/free-busy/)
- [Awesome Time Tracking: AI Scheduling Agents 2026](https://github.com/ever-works/awesome-time-tracking/blob/develop/details/ai-scheduling-agents-2026.md)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
