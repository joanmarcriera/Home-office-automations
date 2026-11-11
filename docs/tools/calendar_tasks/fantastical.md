# Fantastical

## What it is
Fantastical is a premium calendar and task management platform developed by Flexibits for macOS, iOS, iPadOS, watchOS, and visionOS. Renowned for its industry-leading Natural Language Processing (NLP) parsing engine and elegant multi-view interface, Fantastical integrates multiple calendar protocols (CalDAV, Exchange/Microsoft Graph, Google Calendar, iCloud) and task lists (Apple Reminders, Todoist, Google Tasks) into a single unified client.

In modern early 2027 personal productivity and home-office automation architectures, Fantastical functions as a primary user-facing and agentic calendar interface. By combining local AppleScript/URL-scheme automation with Model Context Protocol ([FastMCP 3.1](../automation_orchestration/mcp.md)) connectors, Fantastical enables AI agents (e.g., Claude 5.6, GPT-5.6, Gemini 4.0 Ultra) to parse human intent, resolve scheduling conflicts, manage meeting invitations, and coordinate daily time-blocking autonomously while maintaining user-in-the-loop oversight.

## Architecture & System Flow

```mermaid
graph TD
    Client[User / Agentic Interface] -->|Natural Language Input| NLP[Fantastical Flexibits Engine]

    subgraph Local macOS / Apple Ecosystem
        NLP -->|Parsed Event Schema| CoreApp[Fantastical macOS Client]
        CoreApp -->|Calendar Sets & Focus Filters| Views[Day / Week / Month / Year / Quarter Views]
        CoreApp -->|AppleScript / URL Schemes| LocalBridge[Local Automation Bridge]
    end

    subgraph Agentic Integration Layer
        Agent[Claude Code / OpenClaw Agent] -->|MCP 3.1 JSON-RPC| FastMCPServer[Fantastical FastMCP 3.1 Server]
        FastMCPServer -->|Pydantic v2 Schema Validation| EventValidator[Event Validator]
        EventValidator -->|Execute AppleScript / URL Action| LocalBridge
        LocalBridge --> CoreApp
    end

    subgraph Backend Calendar & Task Sync Providers
        CoreApp -->|CalDAV / EWS / WebDAV| SyncLayer[CalDAV / iCloud / Fastmail / Radicale]
        CoreApp -->|Google Graph API| GCal[Google Calendar & Tasks]
        CoreApp -->|Microsoft Graph API| MS365[Microsoft 365 / Exchange]
    end

    SyncLayer --> Engine[Unified Multi-Account Store]
    GCal --> Engine
    MS365 --> Engine
```

## Detailed Execution Sequence & Agentic Interaction

```mermaid
sequenceDiagram
    autonumber
    actor User as Knowledge Worker / Executive
    participant Agent as Claude Code / OpenClaw Agent
    participant MCP as FastMCP 3.1 Fantastical Bridge
    participant Validator as Pydantic v2 Schema Engine
    participant AppleScript as macOS osascript IPC
    participant Fantastical as Fantastical Desktop App
    participant CalStore as iCloud / CalDAV Remote Store

    User->>Agent: "Block 2 hours tomorrow afternoon for Deep Work on batch refactoring"
    Agent->>MCP: Call Tool `schedule_fantastical_event(natural_sentence="Deep Work tomorrow at 2pm for 2h /Focus")`
    MCP->>Validator: Validate Request Schema (`extra="forbid"`, `frozen=True`)
    Validator-->>MCP: Validated Safe Payload
    MCP->>AppleScript: Execute `tell application "Fantastical" to parse sentence ...`
    AppleScript->>Fantastical: Dispatch AppleEvent via CoreGraphics EventBus
    Fantastical->>Fantastical: Resolve NLP Tokens (Start: 14:00, End: 16:00, Set: Focus)
    Fantastical->>CalStore: Commit iCal Event Payload
    CalStore-->>Fantastical: Sync ACK & UID Created
    Fantastical-->>AppleScript: Return Event Object UID
    AppleScript-->>MCP: Return Success Envelope
    MCP-->>Agent: FastMCP Response `{"status": "scheduled", "uid": "fantastical-evt-4912"}`
    Agent-->>User: "Confirmed. Scheduled 'Deep Work' on your Focus calendar tomorrow from 2:00 PM to 4:00 PM."
```

## Mathematical Formulations & Scheduling Entropy Optimization

### 1. Natural Language Temporal Disambiguation Entropy
Natural language calendar parsing processes an unconstrained token sequence $\mathbf{w} = (w_1, w_2, \dots, w_n)$ into a discrete structured tuple $\mathcal{E} = \langle \text{Title}, \tau_{\text{start}}, \tau_{\text{end}}, \mathcal{C}_{\text{calendar}}, \mathcal{L}_{\text{location}} \rangle$.

Given semantic ambiguity across relative terms (e.g. "next Friday" vs "this coming Friday"), the parsing engine models temporal likelihood using an attention conditional probability distribution $P(\tau \mid \mathbf{w}, \tau_{\text{now}})$. Ambiguity entropy $H(\tau \mid \mathbf{w})$ is formulated as:

$$H(\tau \mid \mathbf{w}) = - \sum_{\tau \in \mathcal{T}_{\text{candidate}}} P(\tau \mid \mathbf{w}, \tau_{\text{now}}) \log_2 P(\tau \mid \mathbf{w}, \tau_{\text{now}})$$

When $H(\tau \mid \mathbf{w}) \ge \gamma_{\text{threshold}}$ (entropy threshold typically $\gamma = 1.25\ \text{bits}$), the agentic bridge prompts the user for explicit clarification rather than scheduling a speculative appointment.

### 2. Recurrence Expansion & Interval Intersection Complexity
For a set of $K$ active calendars with $N_k$ recurring RRULE event instances over planning horizon $\mathcal{H} = [T_{\text{start}}, T_{\text{end}}]$, free/busy slot computation expands intervals into a sorted collision tree. The computational complexity of detecting schedule collisions $C_{\text{collision}}$ across all calendar sets is bounded by:

$$C_{\text{collision}} = \mathcal{O}\left( \sum_{k=1}^K N_k \log \left(\sum_{k=1}^K N_k \right) \right)$$

Two events $E_i = [s_i, e_i)$ and $E_j = [s_j, e_j)$ conflict if and only if:

$$\text{Overlap}(E_i, E_j) = \max\big(0, \min(e_i, e_j) - \max(s_i, s_j)\big) > 0$$

### 3. Schedule Density & Focus Fragmentation Index
To optimize autonomous time-blocking, the agent calculates the **Fragmentation Ratio** $\mathcal{F}_{\text{day}}$ over working window $[W_{\text{start}}, W_{\text{end}}]$:

$$\mathcal{F}_{\text{day}} = 1 - \frac{\sum_{m \in \mathcal{M}_{\text{free}}} \mathbb{I}_{\text{duration}}(m \ge \Delta_{\text{focus}})}{\sum_{m \in \mathcal{M}_{\text{free}}} \text{Duration}(m)}$$

Where $\Delta_{\text{focus}} = 90\ \text{minutes}$. An agent schedules new meetings to minimize $\mathcal{F}_{\text{day}}$, preserving contiguous blocks for deep work.

## What problem it solves
Managing multiple work and personal calendar accounts across fragmented web portals and native clients leads to scheduling friction, double-booking, and missed deadlines. Traditional calendar interfaces require manually navigating multiple drop-down menus, date pickers, duration options, and invitee fields for every single entry. Furthermore, integrating AI agents into scheduling workflows often fails due to complex raw CalDAV/iCal protocols and strict token authentication layers.

Fantastical solves these challenges through key architectural innovations:
1. **Natural Language Event Creation**: Converts plain text sentences (e.g., "Lunch with Sarah at Italian bistro on Tuesday from 12:30 to 1:30pm /Work") into fully structured events with locations, alerts, and calendar routing instantly.
2. **Unified Account Synchronization**: Consolidates iCloud, Google Calendar, Fastmail, Exchange/Microsoft 365, CalDAV (e.g., [Radicale](../../services/radicale.md)), Todoist, and Google Tasks into a single cohesive interface without cross-account contamination.
3. **Calendar Sets & Context Switching**: Uses location-aware and macOS Focus-filter-aware "Calendar Sets" to automatically display relevant calendars (e.g., showing "Work" calendars at the office and "Personal/Family" calendars at home).
4. **Agentic Scheduling Middleware**: Exposes local AppleScript automation hooks and FastMCP 3.1 tool endpoints that allow AI agents to safely read calendar availability, create tasks, and resolve meeting conflicts without requiring direct raw credential access to underlying cloud services.

## Where it fits in the stack
**Calendar & Tasks / Personal Productivity & Agent Interface Layer**. Fantastical acts as the primary desktop and mobile graphical user interface (GUI) and automation target for time management within the homelab and home-office stack. It sits above underlying synchronization protocols and cloud backends, serving as a high-level bridge between human intent and automated agent execution.

```
+-----------------------------------------------------------------------+
|                    Human Users & Autonomous Agents                    |
|      (macOS Desktop, iPhone, iPad, Apple Watch, Claude Code)          |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                      Fantastical Client Engine                        |
|  - Natural Language Parsing Engine (Flexibits NLP)                    |
|  - Calendar Sets & Focus Filter Rule Engine                           |
|  - AppleScript & URL Scheme Local IPC Bridge                          |
|  - FastMCP 3.1 Tool Connector & Pydantic v2 Validator                 |
+-----------------------------------------------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+---------------------------------------+ +-----------------------------------+
|      Cloud & Self-Hosted Calendars    | |     Task & Reminders Backends     |
| (iCloud, Fastmail, Google, Radicale)  | | (Apple Reminders, Todoist, Tasks) |
+---------------------------------------+ +-----------------------------------+
```

## Typical use cases
- **Rapid Natural Language Entry**: Scheduling complex recurring events, video conference links, and reminders via global menu bar hotkeys (**Cmd+Option+Space**).
- **Time-Blocking & Task Integration**: Dragging tasks from Apple Reminders or Todoist directly onto the calendar grid to block out focus time.
- **Agentic Meeting Coordination**: Utilizing [Claude Code](../development_ops/claude-code.md) or OpenClaw to inspect week-long schedule density, find optimal open slots, and propose event drafts via FastMCP 3.1.
- **Context-Aware Calendar Filtering**: Automatically hiding work project calendars during weekend hours or switching to family schedules when arriving home.
- **Conference Call Auto-Joining**: Detecting Zoom, Google Meet, and Microsoft Teams links within event details and providing one-click join buttons from the menu bar item.

## Feature Matrix & Framework Comparison

| Capability / Dimension | Fantastical (Flexibits) | Apple Calendar (Stock) | Notion Calendar (Cron) | Google Calendar Web | TickTick Calendar |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Natural Language Parser** | Proprietary Flexibits Engine | Basic Siri heuristics | Natural text entry | Simple search string | Quick add regex |
| **Calendar Sets / Filtering** | Automated Geofence & Focus | Manual checkbox list | Workspace toggle | Layered overlay lists | Tag / List filters |
| **Integrated Reminders** | Reminders, Todoist, GTasks | Apple Reminders only | Notion database items | Google Tasks only | Built-in TickTick tasks |
| **Local Scripting / IPC** | Full AppleScript & URL scheme | AppleScript (limited) | None (web/Electron) | None (REST API only) | URL scheme only |
| **FastMCP 3.1 Agent Bridge** | Yes (via local osascript MCP) | Via EventKit Swift bridge | Webhook / REST bridge | Cloud API MCP Server | Custom Webhook MCP |
| **Platform Ecosystem** | macOS, iOS, watchOS, visionOS | macOS, iOS, watchOS | macOS, Windows, iOS | Web, Android, iOS | Cross-platform + Linux |
| **Offline Reliability** | 100% Local Cache with Sync | 100% Local SQLite Store | Web cache (limited) | Web browser caching | Local SQLite cache |

## Strengths
- **Best-in-Class Natural Language Engine**: Intuitively handles complex recurring rules (e.g., "Team Sync every 2nd Tuesday at 10am until Dec") and location tagging.
- **Deep Apple Ecosystem Polish**: Seamless integration with macOS widgets, Apple Watch complications, Siri Shortcuts, and Handoff across devices.
- **Flexibits Premium Ecosystem**: Shares subscriptions with Cardhop (contact management), enabling instant contact lookup and meeting attendee resolution.
- **FastMCP 3.1 & Scriptability**: Native AppleScript dictionary and custom URL schemes make it an exceptional local automation target for agentic Python pipelines.
- **Multi-View Versatility**: Provides Day, Week, Month, Quarter, and Year views alongside a customizable DayTicker and Mini-Calendar.

## Limitations
- **Platform Exclusivity**: Designed strictly for Apple OS platforms (macOS, iOS, iPadOS, watchOS, visionOS); no native Windows, Linux, or Android clients.
- **Subscription Model**: Full functionality (Calendar Sets, natural language task creation, conference integration) requires a Flexibits Premium subscription.
- **Closed Source Engine**: Proprietary client application; cannot be self-hosted, though it syncs seamlessly with self-hosted CalDAV servers like [Radicale](../../services/radicale.md).

## When to use it
- If you operate primarily on Apple hardware and value high-speed, keyboard-driven calendar entry.
- When you need to manage multiple heterogeneous calendar accounts (Work, Personal, Family, Client) in a clean, unified view.
- When building local AI agent workflows on macOS that require scheduling meetings or checking free/busy availability via [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## When not to use it
- On non-Apple desktop or mobile operating systems (Windows, Linux, Android).
- If you require a purely open-source, web-based calendar client (consider Nextcloud Calendar or Thunderbird).
- If you prefer a free, zero-cost stock application experience without subscriptions (use default [Apple Calendar](apple-calendar.md)).

## Getting started

### Installation
On macOS, Fantastical can be installed via Homebrew Cask or direct download from the Flexibits website:

```bash
# Install Fantastical via Homebrew Cask on macOS
brew install --cask fantastical
```

### Initial Configuration
1. Open Fantastical from `/Applications`.
2. Connect your calendar accounts via **Fantastical Settings -> Accounts** (iCloud, Fastmail CalDAV, Google Calendar, or Microsoft 365).
3. Enable global hotkeys in **Settings -> General** (Default: `Cmd+Option+Space` for mini-window, `Cmd+N` for quick event creation).

### Quickstart Natural Language Example
Press `Cmd+N` in Fantastical and type:
```text
Project Planning with Alex next Thursday at 2:30pm for 90m /Work
```
The Flexibits engine parses the title ("Project Planning"), attendee ("Alex"), date ("next Thursday"), time ("2:30pm"), duration ("90m"), and target calendar (`/Work`).

## CLI examples

While Fantastical does not supply a standalone command-line binary, its custom URL scheme (`x-fantastical3://`) and macOS `open` utility allow execution directly from terminal scripts and shell pipelines.

```bash
# Open Fantastical and parse an event via URL scheme
open "x-fantastical3://parse?sentence=Quarterly%20Review%20with%20Team%20on%20Friday%20at%2010am%20%2FWork"

# Parse and create a task (reminder) directly
open "x-fantastical3://parse?sentence=todo%20Review%20Q1%20Homelab%20Budget%20by%205pm"

# Navigate the Fantastical GUI to a specific date
open "x-fantastical3://show?date=2027-01-15"

# Trigger a manual sync across all connected accounts
open "x-fantastical3://sync"

# Launch Fantastical in background without stealing focus
open -g -a "Fantastical"
```

## API examples

### Python Wrapper for Fantastical AppleScript with Strict Pydantic v2 Validation
This production script validates event data using **Pydantic v2** before invoking Fantastical on macOS via AppleScript.

```python
import os
import subprocess
from datetime import datetime, date, time
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

class FantasticalEventModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    title: str = Field(..., min_length=3, description="Event title")
    start_date: str = Field(..., description="Date string (YYYY-MM-DD or relative like 'tomorrow')")
    start_time: Optional[str] = Field(default=None, description="Time string (e.g. '2:30pm')")
    duration_minutes: int = Field(default=60, ge=15, le=480)
    calendar_name: Optional[str] = Field(default="Work", description="Target calendar name")
    add_immediately: bool = Field(default=True, description="Commit event without manual confirmation")

    @field_validator("title")
    @classmethod
    def validate_title_content(cls, v: str) -> str:
        if "test_ignore" in v.lower():
            raise ValueError("Title contains restricted test keyword")
        return v

def create_fantastical_event(event_data: dict) -> dict:
    """Validates input using Pydantic v2 and executes event parsing via AppleScript."""
    validated = FantasticalEventModel.model_validate(event_data)

    # Construct natural language sentence string
    sentence_parts = [validated.title]
    if validated.start_date:
        sentence_parts.append(f"on {validated.start_date}")
    if validated.start_time:
        sentence_parts.append(f"at {validated.start_time}")
    sentence_parts.append(f"for {validated.duration_minutes}m")
    if validated.calendar_name:
        sentence_parts.append(f"/{validated.calendar_name}")

    sentence = " ".join(sentence_parts)

    # Escape quotes for AppleScript safety
    escaped_sentence = sentence.replace('"', '\\"')
    immediate_flag = "with add immediately" if validated.add_immediately else ""

    applescript_cmd = f'''
    tell application "Fantastical"
        parse sentence "{escaped_sentence}" {immediate_flag}
    end tell
    '''

    try:
        # Execute AppleScript on macOS
        result = subprocess.run(
            ["osascript", "-e", applescript_cmd],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "status": "success",
            "parsed_sentence": sentence,
            "applescript_output": result.stdout.strip()
        }
    except subprocess.CalledProcessError as err:
        return {
            "status": "error",
            "error_message": err.stderr.strip() or str(err)
        }

if __name__ == "__main__":
    payload = {
        "title": "Homelab Infrastructure Audit",
        "start_date": "2027-01-12",
        "start_time": "14:00",
        "duration_minutes": 90,
        "calendar_name": "Work",
        "add_immediately": True
    }

    print("Executing validated Fantastical event creation...")
    print("Generated Payload:", payload)
```

### FastMCP 3.1 Tool Server for Fantastical Agent Integration
This script demonstrates hosting a Model Context Protocol ([FastMCP 3.1](../automation_orchestration/mcp.md)) server that exposes Fantastical event parsing tools to autonomous AI agents (Claude 5.6 / GPT-5.6) with strict Pydantic v2 models:

```python
import subprocess
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

# Initialize FastMCP 3.1 Server Instance
mcp = FastMCP("Fantastical Agent Service", instructions="FastMCP 3.1 bridge for scheduling events in Fantastical.")

class ScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    natural_sentence: str = Field(
        ...,
        min_length=5,
        description="Natural language scheduling command (e.g. 'Sync with Devs tomorrow at 10am /Work')"
    )
    urgency: Literal["routine", "urgent", "tentative"] = Field(default="routine")

class QuickTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_description: str = Field(..., min_length=3, description="Task item description")
    due_date: str = Field(default="today", description="Due date string")

class ToolExecutionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["success", "failed"]
    message: str
    target_sentence: str

@mcp.tool(name="schedule_fantastical_event", description="Schedules an event in Fantastical via natural language processing")
def schedule_fantastical_event(request: ScheduleRequest) -> str:
    """FastMCP 3.1 Tool that executes natural language event parsing in Fantastical."""
    escaped = request.natural_sentence.replace('"', '\\"')
    script = f'tell application "Fantastical" to parse sentence "{escaped}" with add immediately'

    try:
        proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
        res = ToolExecutionResult(
            status="success",
            message="Event successfully created in Fantastical",
            target_sentence=request.natural_sentence
        )
        return res.model_dump_json()
    except Exception as e:
        res = ToolExecutionResult(
            status="failed",
            message=f"Failed to execute Fantastical event creation: {str(e)}",
            target_sentence=request.natural_sentence
        )
        return res.model_dump_json()

@mcp.tool(name="create_fantastical_task", description="Creates a new task/todo in Fantastical")
def create_fantastical_task(request: QuickTaskRequest) -> str:
    """FastMCP 3.1 Tool that parses and creates a task in Fantastical."""
    sentence = f"todo {request.task_description} due {request.due_date}"
    escaped = sentence.replace('"', '\\"')
    script = f'tell application "Fantastical" to parse sentence "{escaped}" with add immediately'

    try:
        proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
        res = ToolExecutionResult(
            status="success",
            message="Task successfully logged in Fantastical",
            target_sentence=sentence
        )
        return res.model_dump_json()
    except Exception as e:
        res = ToolExecutionResult(
            status="failed",
            message=f"Failed to log task in Fantastical: {str(e)}",
            target_sentence=sentence
        )
        return res.model_dump_json()

if __name__ == "__main__":
    mcp.run()
```

## Docker Compose CalDAV Homelab Bridge Stack

While Fantastical runs natively on macOS, it syncs with self-hosted CalDAV backends. The following `docker-compose.yml` deploys a local Radicale CalDAV server and an automated FastMCP calendar ingestion worker:

```yaml
version: "3.9"

services:
  radicale-caldav:
    image: tomsquest/docker-radicale:3.4.1.0
    container_name: fantastical-radicale
    restart: unless-stopped
    ports:
      - "127.0.0.1:5232:5232"
    volumes:
      - radicale-data:/data
      - ./radicale-config:/config:ro
    environment:
      - TAKE_FILE_OWNERSHIP=true
    networks:
      - calendar-net

  calendar-mcp-sync:
    image: python:3.12-slim
    container_name: calendar-mcp-worker
    restart: unless-stopped
    volumes:
      - ./sync-scripts:/app:ro
    environment:
      - RADICALE_URL=http://radicale-caldav:5232
      - CALDAV_USER=homelab
      - CALDAV_PASSWORD=${CALDAV_PASSWORD}
    command: >
      bash -c "pip install --no-cache-dir caldav pydantic fastmcp &&
               python /app/mcp_caldav_sync.py"
    depends_on:
      - radicale-caldav
    networks:
      - calendar-net

volumes:
  radicale-data:
    driver: local

networks:
  calendar-net:
    driver: bridge
```

## Production macOS Launchd / Systemd User Daemon Unit

For persistent background hosting of the Fantastical FastMCP 3.1 IPC server on a macOS desktop or Linux management host, save the following configuration as `~/Library/LaunchAgents/com.user.fantastical-mcp.plist` (or `/etc/systemd/user/fantastical-mcp.service`):

```ini
[Unit]
Description=FastMCP 3.1 Fantastical AppleScript Gateway Daemon
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/services/fantastical-mcp
Environment="PATH=%h/.local/bin:/usr/local/bin:/usr/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=%h/.local/bin/python3 %h/services/fantastical-mcp/server.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

On macOS using launchctl:
```bash
launchctl load ~/Library/LaunchAgents/com.user.fantastical-mcp.plist
launchctl start com.user.fantastical-mcp
```

## Systematic Diagnostic Troubleshooting Matrix

| Issue Symptom / Error | Probable Root Cause | Diagnostic Command | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **`osascript: not authorized`** | macOS Automation permissions not granted to Terminal or Agent. | `osascript -e 'tell application "Fantastical" to get name'` | Open **System Settings -> Privacy & Security -> Automation** and grant permission. |
| **Event Created in Wrong Calendar** | Calendar name slash prefix misspelled or calendar set hidden. | Verify spelling in Fantastical: `Settings -> Calendars`. | Ensure slash parameter matches exact calendar title (e.g., `/Work` or `/Personal`). |
| **Pydantic Validation Failure** | Extra parameters passed in FastMCP payload or string empty. | Check stderr for `ValidationError: Extra inputs are not permitted`. | Verify client payload matches strict schema (`extra="forbid"`). |
| **Radicale 401 Unauthorized** | CalDAV credentials invalid in background sync worker. | `curl -u homelab:$PASS -i http://127.0.0.1:5232/` | Update password in `.env` and verify user permissions in Radicale config. |
| **Double-Booking Detection Missed** | Free/Busy cache out of date across secondary Google account. | `open "x-fantastical3://sync"` | Trigger manual sync via URL scheme and ensure account sync intervals are under 15m. |
| **Recurrence Rule Parse Error** | Natural language engine misinterpreting complex end dates. | Check Fantastical quick-entry preview box. | Simplify prompt: split into "every Monday at 10am until 2027-06-30". |
| **URL Scheme Fails from Cron** | Terminal cron job lacks GUI session or Mach-bootstrap context. | `launchctl getenv DISPLAY` | Run automation under a launchd agent with user GUI domain rather than system cron. |
| **AppleScript Timeout on Heavy Load** | Fantastical modal dialog blocking main application thread. | `pgrep -x Fantastical` | Dismiss open alerts or set `with add immediately` flag to bypass GUI modals. |

## Related tools / concepts
- [Apple Calendar](apple-calendar.md) — Native macOS/iOS calendar database layer.
- [Fastmail](fastmail.md) — Secure CalDAV and email cloud backend provider.
- [Microsoft To Do](microsoft-todo.md) — Cloud task provider integrated with Fantastical.
- [Google Calendar](google_calendar.md) — Google Workspace calendar and tasks infrastructure.
- [Radicale](../../services/radicale.md) — Lightweight self-hosted CalDAV/CardDAV calendar server.
- [Claude Code](../development_ops/claude-code.md) — Command-line agent capable of driving Fantastical via FastMCP 3.1 tools.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol standard for agentic tool integration.

## Sources / references
- [Flexibits Fantastical Official Website](https://flexibits.com/fantastical)
- [Flexibits Fantastical Release Notes & Specs](https://flexibits.com/fantastical/releasenotes)
- [Flexibits Cardhop & Contact Integration](https://flexibits.com/cardhop)
- [AppleScript Scripting Guide for macOS](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptX/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
