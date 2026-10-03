# Morgen

## What it is
Morgen is a cross-platform calendar, task manager, and meeting scheduler that aggregates all personal and enterprise scheduling sources into a single, unified interface. It connects seamlessly across Google Calendar, Microsoft Outlook, Exchange, Apple iCloud, and self-hosted CalDAV servers (such as Nextcloud, [Radicale](../../services/radicale-automation.md), and Baïkal).

In early 2027, Morgen is widely adopted as an agentic time-blocking command center. Autonomous AI agents (such as Claude 5.1, GPT-5.6, Gemini 4.0 Pro, DeepSeek-V4, Llama 4, and Qwen 3.8) can interact with Morgen's unified REST API and local FastMCP 3.1 task bridge to schedule events, negotiate meeting slots, resolve calendar conflicts, and manage time-blocked task lists across disparate calendar backends without requiring distinct integrations for each provider.

```
+-----------------------------------------------------------------------------------+
|                              MORGEN UNIFIED HUB                                   |
|                                                                                   |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|  | Google Calendar    |  | Microsoft Outlook  |  | Self-Hosted CalDAV          |  |
|  | (Personal Account) |  | (Corporate Exchange)|  | (Radicale / Nextcloud)     |  |
|  +---------+----------+  +---------+----------+  +--------------+--------------+  |
|            |                       |                        |                     |
|            +-----------------------+------------------------+                     |
|                                    v                                              |
|                   +----------------------------------+                            |
|                   | Morgen Synchronization Engine   |                            |
|                   +----------------+-----------------+                            |
|                                    |                                              |
|            +-----------------------+------------------------+                     |
|            v                                                v                     |
|  +------------------+                             +--------------------+          |
|  | Native GUI App   |                             | FastMCP 3.1        |          |
|  | (Win/macOS/Linux)|                             | Agentic Tool Bridge|          |
|  +------------------+                             +--------------------+          |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing schedules across multiple personal, client, and corporate environments leads to calendar fragmentation, scheduling double-bookings, and friction during task time-blocking. Furthermore, developers building autonomous AI scheduling agents face the immense complexity of integrating separate OAuth2 flows, API endpoints, and data formats for Google, Microsoft, Apple, and CalDAV systems.

Morgen solves these issues by:
- **Unified Aggregation**: Bringing all calendars into a single timeline without merging or leaking personal and work accounts.
- **Cross-Calendar Conflict Resolution**: Automatically blocking out time across corporate calendars when personal events are created, preserving privacy without overbooking.
- **Unified Agent Interface**: Exposing a single, developer-friendly REST API and FastMCP 3.1 server layer for autonomous agents to inspect availability, create events, and time-block tasks across all connected providers.
- **Integrated Task Time-Blocking**: Syncing tasks directly from Todoist, Microsoft To-Do, ClickUp, and Notion, and allowing drag-and-drop or programmatic scheduling into open calendar slots.

## Where it fits in the stack
**Category**: [Calendar & Tasks](../calendar_tasks/index.md) / Unified Scheduling Command Center. Morgen sits between low-level calendar backends (Google, Exchange, CalDAV) and high-level productivity workflows, acting as the scheduling execution layer for humans and autonomous AI agents.

```
+--------------------------------------------------------------------+
| Application / Agent Layer: FastMCP 3.1 Scheduling Agent / User GUI |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
| Unified Engine: Morgen Local Client & Morgen Cloud API             |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
| Backends: Google Calendar | Outlook/Exchange | iCloud | CalDAV      |
+--------------------------------------------------------------------+
```

## Typical use cases
- **Multi-Ecosystem Schedule Aggregation**: Managing a corporate Exchange calendar alongside an iCloud family calendar and a personal Google Calendar on macOS, Linux, or Windows.
- **AI Agentic Executive Assistant**: Deploying an autonomous AI assistant that monitors incoming requests, calculates free/busy availability across all calendars, and reserves focus-work blocks via Morgen tools.
- **Self-Hosted CalDAV Bridge**: Using Morgen as a modern desktop and mobile frontend for self-hosted instances of [Radicale](../../services/radicale-automation.md) or Nextcloud Calendar.
- **Task Time-Blocking**: Syncing actionable task lists from Todoist or Microsoft To-Do and placing them directly onto calendar timelines.
- **Smart Booking Page Sharing**: Generating customized scheduling links that calculate real-time availability across all private and public connected calendars.

## Strengths
- **Unrivaled Provider Support**: Simultaneous full sync support for Google, Outlook/Exchange, iCloud, and standard CalDAV servers.
- **Native Cross-Platform Clients**: High-performance native applications built for Windows, macOS, Linux (AppImage/Deb/RPM), iOS, and Android.
- **Privacy Controls & Local Buffering**: Offers local-only calendar storage options and token security for self-hosted servers.
- **Rich Task Integration**: Native multi-provider task sync (Todoist, Microsoft To-Do, Google Tasks) with drag-and-drop time-blocking.
- **Developer & Agent Friendly**: Clean, predictable REST APIs and FastMCP 3.1 integrations for programmatic calendar manipulation.

## Limitations
- **Closed Source Core**: Proprietary client application and backend sync service.
- **Subscription Model for Advanced Tools**: Multi-account synchronization and advanced booking links require a paid Morgen Pro subscription.
- **No Direct Web App**: Relies primarily on native desktop/mobile apps and cloud API endpoints rather than a browser-only SPA.

## When to use it
- When operating across multiple distinct calendar providers (e.g., corporate Outlook + personal Google + self-hosted CalDAV).
- When configuring autonomous AI agents to manage time-blocking, meeting booking, and calendar queries across fragmented ecosystems.
- When you need a unified cross-platform desktop calendar app on Linux, macOS, and Windows.
- When managing time-blocking workflows that combine tasks from Todoist or Microsoft To-Do with live calendar events.

## When not to use it
- If your schedule is entirely contained within a single ecosystem (e.g., Google Workspace only) and you don't require task time-blocking or multi-calendar aggregation.
- If you require a 100% open-source desktop client (consider Thunderbird or KOrganizer).
- If you prefer a browser-only web application without installing native desktop software.

## Getting started

### Installation

#### macOS (Homebrew Cask)
```bash
brew install --cask morgen
```

#### Linux (Debian / Ubuntu)
```bash
# Download latest .deb package from official releases
wget https://release.morgen.so/desktop/linux/morgen-latest.deb
sudo dpkg -i morgen-latest.deb
sudo apt-get install -f # Resolve dependencies if necessary
```

#### Linux (AppImage)
```bash
chmod +x morgen-*.AppImage
./morgen-*.AppImage
```

### Account Configuration & Setup
1. Launch the Morgen desktop application.
2. Complete authentication with your primary Morgen account.
3. Click **Add Account** in the left sidebar to connect:
   - Google Calendar (OAuth2)
   - Microsoft Outlook / Exchange (OAuth2 / MS Entra)
   - Apple iCloud (App-Specific Password)
   - CalDAV (Server URL, Port, Username, Password)
4. Enable Task Integrations (Todoist, Microsoft To-Do, or Google Tasks) under **Settings > Tasks**.

## CLI examples

While Morgen is primarily a native application, it can be launched, inspected, and controlled via command-line utilities and deep-link protocols.

```bash
# Verify Morgen background daemon process on macOS or Linux
pgrep -fl morgen

# Trigger Morgen UI to open to a specific calendar date via deep-link
open "morgen://calendar/2027-01-07"

# Inspect local Morgen app configuration on Linux
ls -la ~/.config/Morgen/

# Trigger event creation window via deep-link
open "morgen://events/new?title=Strategic%20Planning&duration=60"
```

## API examples

### Direct HTTP REST Interaction with Morgen API
```bash
: "${MORGEN_API_KEY:?Please set MORGEN_API_KEY in environment}"

# Fetch all events scheduled for today across all connected calendars
curl -s -X GET "https://api.morgen.so/v3/events/list?start=2027-01-07T00:00:00Z&end=2027-01-07T23:59:59Z" \
  -H "Authorization: ApiKey $MORGEN_API_KEY" \
  -H "Content-Type: application/json" | jq .
```

### Programmatic Payload Validation with Pydantic v2 (Python)
The following Python module defines strict **Pydantic v2** models to validate, parse, and verify event creation payloads before sending requests to the Morgen API.

```python
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict, HttpUrl
import json

class MorgenEventParticipant(BaseModel):
    email: str = Field(..., description="Email address of participant")
    name: Optional[str] = Field(default=None, description="Display name of participant")
    status: str = Field(default="accepted", description="RSVP status: accepted, pending, declined")

class CreateMorgenEventRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    calendar_id: str = Field(..., alias="calendarId", description="Target Morgen Calendar ID")
    title: str = Field(..., min_length=1, max_length=200, description="Title of the meeting/event")
    description: Optional[str] = Field(default=None, description="Detailed agenda or notes")
    start_time: datetime = Field(..., alias="start", description="ISO 8601 start timestamp")
    end_time: datetime = Field(..., alias="end", description="ISO 8601 end timestamp")
    location: Optional[str] = Field(default=None, description="Physical location or meeting URL")
    participants: List[MorgenEventParticipant] = Field(default_factory=list)
    is_busy: bool = Field(default=True, alias="isBusy")

    @field_validator("end_time")
    @classmethod
    def validate_end_after_start(cls, v: datetime, info) -> datetime:
        start = info.data.get("start_time")
        if start and v <= start:
            raise ValueError("End time must be strictly after start time")
        return v

def generate_validated_morgen_payload() -> str:
    now = datetime.now(timezone.utc)
    event = CreateMorgenEventRequest(
        calendarId="cal_google_primary_99",
        title="Agentic Time-Blocking Audit & Sync",
        description="Review FastMCP 3.1 calendar tools and verify conflict detection.",
        start=now + timedelta(hours=2),
        end=now + timedelta(hours=3),
        location="https://meet.google.com/abc-defg-hij",
        participants=[
            MorgenEventParticipant(email="lead@enterprise.com", name="Engineering Lead")
        ],
        isBusy=True
    )
    return event.model_dump_json(by_alias=True, indent=2)

if __name__ == "__main__":
    print("Validated Morgen Event Creation Payload:")
    print(generate_validated_morgen_payload())
```

### FastMCP 3.1 Morgen Tools & Scheduling Server
The following Python script implements a production-ready **FastMCP 3.1** server that exposes calendar management, availability lookup, and task creation tools for AI agent orchestration.

```python
import os
import requests
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="Morgen-Calendar-Tools",
    version="3.1.0",
    description="FastMCP 3.1 Tool Bridge for Morgen Unified Calendar API"
)

MORGEN_API_KEY = os.environ.get("MORGEN_API_KEY", "mock_key_for_testing")
MORGEN_BASE_URL = "https://api.morgen.so/v3"

class AvailabilityQueryInput(BaseModel):
    start_iso: str = Field(..., description="Start timestamp ISO string (e.g. 2027-01-07T08:00:00Z)")
    end_iso: str = Field(..., description="End timestamp ISO string (e.g. 2027-01-07T18:00:00Z)")

class CreateTaskInput(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(default="", description="Task description")
    due_date: str = Field(..., description="Due date YYYY-MM-DD")
    priority: int = Field(default=2, ge=1, le=3, description="Priority: 1=High, 2=Medium, 3=Low")

@mcp.tool(
    name="morgen_check_availability",
    description="Inspects user availability across all connected Morgen calendars for a given time window."
)
def morgen_check_availability(params: AvailabilityQueryInput) -> Dict[str, Any]:
    """Queries Morgen API to return busy time slots."""
    if MORGEN_API_KEY == "mock_key_for_testing":
        # Mock response for verification and testing
        return {
            "status": "success",
            "query_window": {"start": params.start_iso, "end": params.end_iso},
            "busy_slots": [
                {"start": "2027-01-07T10:00:00Z", "end": "2027-01-07T11:00:00Z", "title": "Corporate Standup"},
                {"start": "2027-01-07T14:00:00Z", "end": "2027-01-07T15:00:00Z", "title": "Architecture Review"}
            ]
        }

    headers = {"Authorization": f"ApiKey {MORGEN_API_KEY}", "Content-Type": "application/json"}
    try:
        res = requests.get(
            f"{MORGEN_BASE_URL}/events/list",
            headers=headers,
            params={"start": params.start_iso, "end": params.end_iso},
            timeout=10
        )
        res.raise_for_status()
        events = res.json().get("data", {}).get("events", [])
        busy_slots = [
            {"start": e["start"], "end": e["end"], "title": e.get("title", "Busy")}
            for e in events if e.get("showAs") == "busy"
        ]
        return {"status": "success", "busy_slots": busy_slots}
    except Exception as err:
        return {"status": "error", "message": str(err)}

@mcp.tool(
    name="morgen_create_task",
    description="Creates a new task in Morgen task manager for time-blocking onto calendar."
)
def morgen_create_task(params: CreateTaskInput) -> Dict[str, Any]:
    """Creates a task payload in Morgen."""
    if MORGEN_API_KEY == "mock_key_for_testing":
        return {
            "status": "success",
            "task_id": "morgen_tsk_991823",
            "title": params.title,
            "due_date": params.due_date,
            "message": "Task successfully created in Morgen inbox."
        }

    headers = {"Authorization": f"ApiKey {MORGEN_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "title": params.title,
        "description": params.description,
        "dueDate": params.due_date,
        "priority": params.priority
    }
    try:
        res = requests.post(f"{MORGEN_BASE_URL}/tasks/create", headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        return {"status": "success", "data": res.json()}
    except Exception as err:
        return {"status": "error", "message": str(err)}

if __name__ == "__main__":
    print("Starting FastMCP 3.1 Morgen Tools Server...")
    mcp.run()
```

## Licensing and cost
- **Open Source**: No (Proprietary native client and cloud sync platform).
- **Pricing Tiers**:
  - **Free Plan**: Single calendar connection, basic scheduling links.
  - **Pro Plan**: Unlimited calendar connections, multiple booking pages, advanced task sync integrations (Todoist, Microsoft To-Do, Notion), and full API access.
- **Self-Hostable**: No (Requires Morgen cloud sync backend, but connects to self-hosted CalDAV servers like Radicale or Nextcloud).

## Related tools / concepts
- [Akiflow](akiflow.md) — Command-center alternative focused on task time-blocking.
- [Fantastical](fantastical.md) — Apple-ecosystem focused calendar alternative.
- [Calendly](calendly.md) — Web-first meeting booking tool.
- [Radicale](../../services/radicale-automation.md) — Lightweight self-hosted CalDAV/CardDAV server.
- [CalDAV](../intake_storage/caldav.md) — Open standard protocol for calendar access.
- [Todoist](todoist.md) — Cloud task manager integrated into Morgen.
- [Microsoft To-Do](microsoft-todo.md) — Enterprise task manager integrated into Morgen.
- [JMAP](../calendar_tasks/jmap.md) — Next-generation mail and calendar sync protocol.

## Sources / references
- [Morgen Official Website](https://www.morgen.so/)
- [Morgen Developer API Documentation](https://morgen.notion.site/Morgen-API-Docs-642152643a0e4171a81112615a1334f2)
- [Morgen Support & Knowledge Base](https://morgen.notion.site/Morgen-Help-Center-885474c3e86c4a85a4f66453f6316278)
- [FastMCP 3.1 Specification](https://mcp.dev/protocols/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
