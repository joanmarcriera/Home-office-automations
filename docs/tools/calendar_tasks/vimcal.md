# Vimcal

## What it is
Vimcal is a high-speed calendar application designed for power users, featuring keyboard shortcuts, time zone coordination, and scheduling links. It aims to be the "fastest calendar in the world" through a command-palette-driven interface. As of early 2027, it includes an enhanced AI Scheduling Assistant and multi-provider synchronization across Google Calendar and Microsoft Outlook. It is a proprietary SaaS product with a paid subscription model.

## What problem it solves
Reduces the time spent on manual scheduling and coordination by streamlining event creation and availability sharing. It eliminates the friction of navigating traditional, mouse-heavy calendar interfaces, especially for users managing global teams across multiple time zones.

## Where it fits in the stack
**Category**: Calendar & Tasks / Productivity Interface. Serves as a high-speed frontend for power users managing schedules across [Google Calendar](google_calendar.md) and [Outlook](outlook.md).

## Typical use cases
- **Fast Event Creation**: Use natural language parsing to book meetings in seconds.
- **Global Coordination**: Manage meetings across multiple time zones with a specialized horizontal overlay view.
- **Availability Snippets**: Quickly share free slots with collaborators without sending link friction.
- **Executive Scheduling**: Use the "AI Scheduling Assistant" to find mutual openings for large internal or client teams.
- **Agentic Scheduling**: Bridge Vimcal with AI assistants like **Claude 5.1**, **GPT-5.5**, and **Llama 4** using provider MCP servers compliant with the **FastMCP 3.1** protocol.

## Strengths
- **Keyboard-first navigation**: Inspired by Vim, allowing for extremely fast interaction.
- **Exceptional Time Zone Management**: Real-time conversion and visualization for global teams.
- **Natural Language Processing (NLP)**: High-accuracy event parsing for title, date, location, and attendees.
- **Distraction-Free UI**: Minimalist design focused on speed and cognitive efficiency.

## Limitations
- **Proprietary SaaS**: Closed-source model requiring a paid subscription for full capabilities.
- **No Direct Public REST API**: Direct developer integration relies on the underlying calendar providers (Google Calendar API or Microsoft Graph API).
- **Limited Native Task Management**: Focuses on scheduling rather than heavy task tracking (better paired with [Todoist](todoist.md) or [Reclaim.ai](reclaim.md)).

## When to use it
- If you spend a significant portion of your day in your calendar and want to minimize UI friction.
- If you frequently coordinate meetings across global time zones.
- If you prefer a keyboard-driven workflow for administrative scheduling tasks.

## When not to use it
- If you need a free or self-hosted calendar solution (consider [Vikunja](../../services/vikunja.md)).
- If you require direct REST API endpoints rather than provider-based API access.

## Getting started

### Installation
Vimcal is available as a desktop (macOS/Windows) and web application. Download the client from [Vimcal.com](https://www.vimcal.com/).

### Basic Setup
1. Sign up and connect your primary [Google Calendar](google_calendar.md) or [Outlook](outlook.md).
2. Use the command palette (`Cmd+K` on Mac, `Ctrl+K` on Windows) to execute commands.
3. **Natural Language Example**: Type "Coffee with Max at 10am tomorrow at Starbucks" and press Enter. The NLP parser automatically populates all fields.

## CLI examples

### Raycast / Alfred Integration
While Vimcal does not have an official CLI, power users leverage launcher extensions:
```bash
# Raycast command example using SOTA tools
raycast "Create Vimcal Event" --title "Review Q1 Roadmap" --time "2pm"
```

### Application Shortcuts
- `F`: Toggle "Free Slots" availability mode.
- `S`: Share availability snippets to clipboard.
- `A`: Open the AI Scheduling Assistant.

## API examples

### Underlying Provider Automation (Google Calendar)
Since Vimcal operates over provider backends, automation is performed via Google Calendar API or Microsoft Graph API. To programmatically validate and insert meetings securely under early 2027 architectures, a Python implementation using **Pydantic v2** is shown below:

```python
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# Define Pydantic v2 Schema for Vimcal-compatible Google Calendar Event
class EventDateTime(BaseModel):
    dateTime: datetime = Field(..., description="ISO 8601 formatted start/end time")
    timeZone: str = Field(default="UTC", description="Timezone identifier")

class EventAttendee(BaseModel):
    email: EmailStr
    optional: bool = False

class VimcalEventPayload(BaseModel):
    summary: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start: EventDateTime
    end: EventDateTime
    attendees: Optional[List[EventAttendee]] = Field(default_factory=list)

# Validate payload using Pydantic v2
raw_data = {
    "summary": "Vimcal Sync with Claude 5.1",
    "description": "Discussing FastMCP 3.1 workflows and task scheduling.",
    "start": {
        "dateTime": "2027-01-15T10:00:00Z",
        "timeZone": "UTC"
    },
    "end": {
        "dateTime": "2027-01-15T11:00:00Z",
        "timeZone": "UTC"
    },
    "attendees": [
        {"email": "alex@example.com", "optional": False}
    ]
}

try:
    validated_event = VimcalEventPayload.model_validate(raw_data)
    print(f"Validated payload successfully: {validated_event.summary}")
    # Now construct and insert event using the Google Calendar API
    # service.events().insert(calendarId='primary', body=validated_event.model_dump()).execute()
except Exception as e:
    print(f"Validation failed: {e}")
```

### MCP Integration
Use the [Google Calendar MCP Server](../automation_orchestration/mcp.md) or Microsoft Graph MCP server to allow agents like **Claude 5.1** or **GPT-5.5** to interact with Vimcal data via FastMCP 3.1:
```bash
npx @modelcontextprotocol/server-google-calendar
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription-based)
- **Self-hostable**: No

## Related tools / concepts
- [Notion Calendar](notion-calendar.md) — High-speed, integrated calendar from Notion.
- [Reclaim.ai](reclaim.md) — AI-driven scheduling for teams.
- [Todoist](todoist.md) — Task management integration partner.
- [Google Calendar](google_calendar.md) — Underlying data provider backend.
- [Outlook](outlook.md) — Enterprise data provider backend.
- [Model Context Protocol](../automation_orchestration/mcp.md) — FastMCP 3.1 framework.

## Sources / references
- [Vimcal Official Website](https://www.vimcal.com/)
- [Vimcal Documentation](https://docs.vimcal.com/)
- [Vimcal Keyboard Shortcuts Guide](https://www.vimcal.com/shortcuts)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
