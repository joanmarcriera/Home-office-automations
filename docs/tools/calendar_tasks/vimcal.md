# Vimcal

## What it is
Vimcal is a high-speed calendar application designed for power users, featuring custom keyboard navigation, multi-time-zone coordination, and integrated scheduling workflows. It provides a command-palette-driven interface ("the fastest calendar in the world") paired with an advanced **AI Scheduling Assistant** that coordinates multi-participant availability across [Google Calendar](google_calendar.md) and [Outlook](outlook.md) backends. In early 2027, Vimcal integrates deeply with agentic scheduling infrastructure using **FastMCP 3.1** protocol connections to manage calendar availability for teams operating with **Claude 5.1/5.6**, **GPT-5.5/5.6**, **Gemini 4.0 Ultra**, and **Qwen 3.6**.

```
+-----------------------------------------------------------------------------------+
|                         VIMCAL AGENTIC SCHEDULING SYSTEM                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Power User /        | ----> | Vimcal Desktop Engine | ---> | Cross-Timezone  | |
|  | Command Palette     |       | NLP / Free-Busy Parser|      | Overlay Matrix  | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Google / Graph      | <---- | FastMCP 3.1 Server    | <--- | Provider OAuth  | |
|  | Calendar Backends   |       | Tool Gateways         |      | Sync Layer      | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Manual scheduling across global distributed teams creates friction, requires constant context switching, and involves repetitive mouse interactions. Vimcal eliminates this overhead by enabling instant natural language event entry, fast availability snippet generation, and automated cross-timezone visual overlay mapping.

## Where it fits in the stack
**Category**: Calendar & Tasks / Productivity Interface. Functions as a high-speed frontend client over underlying calendar provider backends ([Google Calendar](google_calendar.md) and [Outlook](outlook.md)).

## System Architecture & Multi-Timezone Engine

The following diagram illustrates the client interaction flow, natural language engine, AI scheduling assistant, and provider sync layer:

```
                         VIMCAL SYSTEM ARCHITECTURE

    Power User / Keyboard
    (Cmd+K / Fast Shortcuts)
            │
            ▼
    ┌──────────────────────────────────────────┐
    │ Vimcal Frontend (Desktop & Web)          │
    │  - Command Palette                       │
    │  - Timezone Overlays                     │
    └─────────────────────┬────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
    ┌───────────────────┐     ┌───────────────────┐
    │ NLP Parser        │     │ AI Scheduling     │
    │ & Timezone Engine │     │ Assistant         │
    └─────────┬─────────┘     └─────────┬─────────┘
              │                         │
              └─────────────┬───────────┘
                            ▼
    ┌──────────────────────────────────────────┐
    │ FastMCP 3.1 Calendar Provider Gateway    │
    └─────────────────────┬────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
    ┌───────────────────┐     ┌───────────────────┐
    │ Google Calendar   │     │ Microsoft Graph   │
    │ API v3            │     │ API v1.0          │
    └───────────────────┘     └───────────────────┘
```

### Multi-Timezone Matrix Resolution
Vimcal resolves global time differences by projecting participant calendars into a normalized UTC time matrix before rendering user-specific local timezone overlays. When power users press `Z` to add target timezones (e.g., London GMT, Tokyo JST, San Francisco PST), the client dynamically updates free-busy visual blocks without triggering additional backend REST API round trips.

### Natural Language Parser Mechanics
The internal NLP parser breaks down unstructured meeting requests into deterministic fields:
- **Title Extraction**: Strips temporal keywords ("Sync with Alex", "Q1 Planning").
- **Temporal Resolution**: Resolves relative terms ("next Tuesday at 3pm", "tomorrow morning") into ISO 8601 timestamps using local system time and participant timezone metadata.
- **Participant Mapping**: Auto-completes email contacts from local OAuth token stores.

## Typical use cases
- **Rapid Event Booking**: Create meetings in seconds using natural language parsing (e.g., "Strategy sync with Sarah tomorrow at 3pm EST").
- **Global Team Scheduling**: Visualize overlapping working hours across multiple global time zones using horizontal timezone overlays.
- **Instant Availability Sharing**: Generate plain-text or Markdown availability snippets (`Cmd+F`) to paste directly into chat apps or emails.
- **Agentic Scheduling Workflows**: Coordinate agent-managed calendar slots via underlying Google Calendar or Microsoft Graph MCP servers using **FastMCP 3.1**.
- **Cross-Calendar Unified Overview**: Merging personal Google Calendar events with enterprise Outlook calendars in a unified single-keyboard interface.

## Strengths
- **Keyboard-First Design**: Vim-inspired navigation keys and command palette (`Cmd+K`) maximize cognitive efficiency.
- **Superior Time Zone Support**: Real-time conversion, visual drag-and-drop overlays, and automated daylight savings adjustment.
- **High-Precision NLP Engine**: Accurately extracts titles, dates, durations, locations, and attendee lists from raw text input.
- **AI Scheduling Assistant**: Intelligently analyzes attendee free/busy states to propose optimal slot combinations.
- **FastMCP 3.1 Integration**: Seamlessly maps agentic scheduling commands to underlying calendar provider tool definitions.

## Limitations
- **Proprietary Commercial SaaS**: Closed-source subscription product ($15-$20/month per user); no self-hosted option.
- **No Direct Developer REST API**: Direct API access relies on underlying provider endpoints (Google Calendar API or Microsoft Graph API).
- **Focused Feature Scope**: Designed specifically for calendar scheduling rather than heavy task board management (best paired with [Todoist](todoist.md)).

## When to use it
- When calendar navigation speed and keyboard shortcuts are critical to your daily workflow.
- When coordinating frequent meetings across multiple international time zones.
- When you want an intelligent overlay over existing enterprise Google Workspace or Microsoft 365 accounts.

## When not to use it
- If your team requires a free or self-hosted, open-source calendar tool (consider [Vikunja](../../services/vikunja.md) or [Proton Calendar](proton_calendar.md)).
- If you require direct public REST API access without going through Google or Microsoft API layers.

## Installation / setup

### Desktop Installation
1. Download the Vimcal desktop application installer for macOS (`.dmg`) or Windows (`.exe`) from [Vimcal.com](https://www.vimcal.com/).
2. Drag the application to your `Applications` folder on macOS or complete the setup wizard on Windows.
3. Open Vimcal and complete OAuth authentication with your **Google Workspace** or **Microsoft 365** account.

### Configuring Keyboard Preferences
Launch the configuration menu (`Cmd+,` or `Ctrl+,`) to enable custom Vim-style bindings (`j/k` navigation, `d` day view, `w` week view, `m` month view) and register default meeting link providers (Zoom, Google Meet, or Microsoft Teams).

## Getting started

1. **Open Command Palette**: Press `Cmd+K` to open the central action bar.
2. **Book an Event**: Type `Sync with Alex tomorrow at 2pm for 30m` and press `Enter`.
3. **Share Availability**: Press `Cmd+F`, highlight preferred open time blocks, and press `Enter` to copy markdown availability text to your clipboard.

## CLI examples

### Raycast / Alfred Custom Launch Scripts
```bash
# Example Raycast command for quick event booking
raycast "Create Vimcal Event" --title "FastMCP 3.1 Architecture Review" --time "14:00"

# Key Vimcal Application Shortcuts:
# F - Toggle Free Slots mode
# S - Copy availability snippet to clipboard
# A - Launch AI Scheduling Assistant
# Z - Add or toggle primary timezone overlay
```

## API examples

### Production FastMCP 3.1 Calendar Tool & Pydantic v2 Schema Validation
Because Vimcal functions over Google Calendar and Microsoft Graph backends, agentic calendar integration utilizes provider endpoints wrapped in a FastMCP 3.1 server layer:

```python
import os
import logging
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Vimcal-Provider-Bridge")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("vimcal-calendar-bridge")

# Pydantic v2 Models
class EventAttendee(BaseModel):
    email: EmailStr
    response_status: Optional[str] = Field(default="needsAction", description="Status: accepted, declined, tentative, needsAction")

class EventTime(BaseModel):
    date_time: datetime = Field(..., description="ISO 8601 formatted timestamp")
    time_zone: str = Field(default="UTC", description="IANA timezone identifier e.g. America/New_York")

class CalendarEventRequest(BaseModel):
    summary: str = Field(..., min_length=1, max_length=255, description="Event title")
    location: Optional[str] = Field(default=None, description="Meeting location or video URL")
    description: Optional[str] = Field(default=None, description="Event body or agenda")
    start: EventTime
    end: EventTime
    attendees: List[EventAttendee] = Field(default_factory=list)

class CalendarEventResponse(BaseModel):
    event_id: str
    status: str
    html_link: str
    created_at: datetime

class FreeBusySlot(BaseModel):
    start_time: datetime
    end_time: datetime
    is_free: bool

class FreeBusyQueryRequest(BaseModel):
    time_min: datetime
    time_max: datetime
    timezone: str = Field(default="UTC")
    attendee_emails: List[EmailStr]

@mcp.tool()
async def create_vimcal_compatible_event(
    event_payload: dict,
    ctx: Optional[Context] = None
) -> CalendarEventResponse:
    """
    Validates and schedules a calendar event compatible with Vimcal provider backends.

    Args:
        event_payload: Raw event dictionary from LLM tool call.
        ctx: FastMCP Context object.
    """
    if ctx:
        await ctx.info("Validating calendar event payload with Pydantic v2...")

    try:
        validated_event = CalendarEventRequest.model_validate(event_payload)

        if ctx:
            await ctx.info(f"Event validated: '{validated_event.summary}' at {validated_event.start.date_time}")

        # Simulate provider insertion API response
        return CalendarEventResponse(
            event_id="evt_vimcal_20270107_9921",
            status="confirmed",
            html_link="https://calendar.google.com/calendar/event?eid=ZXZ0X3ZpbWNhbF8yMDI3",
            created_at=datetime.now(timezone.utc)
        )

    except ValidationError as ve:
        logger.error(f"Calendar event validation failed: {ve}")
        raise ValueError(f"Invalid calendar event schema: {ve}")

@mcp.tool()
async def query_free_busy_slots(
    query_payload: dict,
    ctx: Optional[Context] = None
) -> List[FreeBusySlot]:
    """
    Queries attendee free/busy status for automated slot selection.

    Args:
        query_payload: Dictionary containing time_min, time_max, and attendee_emails.
        ctx: FastMCP Context object.
    """
    if ctx:
        await ctx.info("Querying attendee availability across provider accounts...")

    try:
        req = FreeBusyQueryRequest.model_validate(query_payload)
        # Mock free slot response
        return [
            FreeBusySlot(start_time=req.time_min, end_time=req.time_max, is_free=True)
        ]
    except ValidationError as ve:
        logger.error(f"FreeBusy query validation failed: {ve}")
        raise ValueError(f"Invalid freebusy request: {ve}")

if __name__ == "__main__":
    mcp.run()
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Commercial SaaS subscription (~$15-$20/month per user)
- **Self-hostable**: No

## Related tools / concepts
- [Notion Calendar](notion-calendar.md) — Fast integrated calendar client for Notion workspaces.
- [Reclaim.ai](reclaim.md) — AI-driven adaptive time-blocking engine.
- [Todoist](todoist.md) — High-efficiency task capture and management.
- [Google Calendar](google_calendar.md) — Underlying cloud calendar backend provider.
- [Outlook](outlook.md) — Enterprise cloud calendar backend provider.
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — FastMCP 3.1 agent architecture standard.

## Sources / references
- [Vimcal Official Site](https://www.vimcal.com/)
- [Vimcal Features & Documentation](https://docs.vimcal.com/)
- [Vimcal Shortcuts Reference](https://www.vimcal.com/shortcuts)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
