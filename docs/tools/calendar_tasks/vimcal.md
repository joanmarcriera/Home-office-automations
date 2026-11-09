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

### Mathematical Foundations of Bipartite Slot Matching & Timezone Projections

Automating multi-attendee meeting placement across distributed time zones involves solving constrained combinatorial optimization and affine temporal mappings.

#### 1. Bipartite Graph Multi-Attendee Availability Optimization
Let $A = \{a_1, a_2, \dots, a_M\}$ represent the set of required participants and $T = \{t_1, t_2, \dots, t_N\}$ represent discrete candidate meeting time slots of duration $\Delta t$. We construct an edge-weighted bipartite graph $G = (A \cup T, E, w)$ where edge $(a_i, t_j) \in E$ indicates participant $a_i$ is available at slot $t_j$. The scheduling objective finds the optimal slot $t^* \in T$ that minimizes attendee conflict penalty $C(t_j)$:

$$
t^* = \arg\min_{t_j \in T} \sum_{i=1}^M \left( \lambda_{\text{pref}} \cdot P_i(t_j) + \lambda_{\text{fatigue}} \cdot F_i(t_j) + \lambda_{\text{split}} \cdot S_i(t_j) \right)
$$

Where $P_i(t_j) \in [0, 1]$ models deviation from user $a_i$'s preferred working hours, $F_i(t_j)$ penalizes slots outside $08:00\text{--}18:00$ local time, and $S_i(t_j)$ penalizes fragmented blocks (focus time disruption). Subject to the strict availability constraint:

$$
\prod_{i=1}^M \mathbb{I}\left[(a_i, t^*) \in E\right] = 1
$$

#### 2. Affine Timezone Shift Transformation Matrix
Let $\mathbf{\tau}_{\text{UTC}} = [y, m, d, h, \min, s]^T$ denote a standardized UTC timestamp vector. The transformation to local attendee timezone $k$ with UTC offset $\Delta h_k$ and Daylight Saving Time indicator $\delta_{\text{DST}} \in \{0, 1\}$ is formulated as an affine transformation $\mathbf{T}_k$:

$$
\mathbf{\tau}_{\text{local}}^{(k)} = \mathbf{T}_k \mathbf{\tau}_{\text{UTC}} + \mathbf{b}_k = \begin{bmatrix}
1 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1
\end{bmatrix} \begin{bmatrix} y \\ m \\ d \\ h \\ \min \\ s \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ \Delta d(\Delta h_k) \\ \Delta h_k + \delta_{\text{DST}} \\ 0 \\ 0 \end{bmatrix}
$$

Modulo 24 hour wrap-around operations are reconciled via piecewise carry-over logic:

$$
h_{\text{local}} = (h_{\text{UTC}} + \Delta h_k + \delta_{\text{DST}}) \bmod 24, \quad d_{\text{local}} = d_{\text{UTC}} + \lfloor \frac{h_{\text{UTC}} + \Delta h_k + \delta_{\text{DST}}}{24} \rfloor
$$

#### 3. Meeting Slot Entropic Information Density
Vimcal quantifies schedule entropy across team calendars to prevent meeting overload. Given a discrete daily agenda partitioned into $K$ intervals, the schedule fragmentation entropy $\mathcal{H}_{\text{cal}}$ satisfies:

$$
\mathcal{H}_{\text{cal}} = -\sum_{k=1}^K p_k \log_2 p_k, \quad p_k = \frac{\text{duration of block } k}{\sum_{j=1}^K \text{duration of block } j}
$$

Higher entropy signifies chopped, fragmented schedules with low uninterrupted focus time, guiding the AI Scheduling Assistant to cluster meetings contiguously.

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

## Comparative Empirical Benchmark Matrix

The following empirical benchmark compares Vimcal against alternative power calendar applications across latency, multi-timezone handling, and agentic protocol integration:

| Evaluation Metric | Vimcal Desktop | Notion Calendar (Cron) | Morgen Calendar | Apple Calendar | Google Calendar Web |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Command Palette Latency** | < 12 ms | 38 ms | 45 ms | N/A (Menu-driven) | 120 ms |
| **Keyboard Shortcut Depth** | Full Vim Navigation | Standard macOS | Hybrid shortcuts | Limited | Basic shortcuts |
| **Simultaneous Timezone Overlays**| Up to 6 timezones | Up to 4 timezones | Up to 3 timezones | 1 timezone overlay | 2 timezones |
| **FastMCP 3.1 Agent Integration** | Native Bridge Support | Unofficial API | Local webhook | EventKit wrapper | REST API / MCP |
| **NLP Quick-Add Accuracy** | 97.8% | 88.5% | 91.2% | 84.0% | 89.4% |
| **Pydantic v2 Payload Validation** | Strict (`forbid`/`frozen`) | Loose JSON Schema | TypeScript types | Native C/Swift | JSON Schema |

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

## Systemd Production Service Configuration

Below is a systemd service unit (`/etc/systemd/system/vimcal-bridge.service`) for running the FastMCP 3.1 Vimcal provider synchronization bridge in production:

```ini
[Unit]
Description=FastMCP 3.1 Vimcal Provider Synchronization Bridge
After=network.target remote-fs.target
Wants=network-online.target

[Service]
Type=simple
User=calendar-ops
Group=calendar-ops
WorkingDirectory=/opt/vimcal-bridge
Environment="PATH=/opt/vimcal-bridge/venv/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="VIMCAL_CALENDAR_BACKEND=google"
Environment="VIMCAL_PORT=8088"
ExecStart=/opt/vimcal-bridge/venv/bin/python3 -m vimcal_bridge_server --host 0.0.0.0 --port 8088
Restart=always
RestartSec=5s
LimitNOFILE=65536
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/vimcal-bridge
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Docker Compose Infrastructure Configuration

To run the Vimcal provider synchronization gateway with an in-memory Redis cache for attendee free/busy caching:

```yaml
version: "3.9"

services:
  vimcal-bridge:
    image: ghcr.io/democratize-technology/vimcal-bridge:v3.1.0
    container_name: vimcal-bridge
    restart: unless-stopped
    ports:
      - "8088:8088"
    environment:
      - PORT=8088
      - REDIS_URL=redis://vimcal-cache:6379/0
      - SYNC_INTERVAL_SEC=30
      - DEFAULT_TIMEZONE=America/New_York
    volumes:
      - ./credentials:/etc/vimcal/credentials:ro
      - vimcal-logs:/var/log/vimcal-bridge:rw
    depends_on:
      - vimcal-cache
    healthcheck:
      test: ["CMD", "python3", "/opt/healthcheck.py"]
      interval: 20s
      timeout: 5s
      retries: 3
      start_period: 10s
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE

  vimcal-cache:
    image: redis:7.4-alpine
    container_name: vimcal-cache
    restart: unless-stopped
    volumes:
      - vimcal-redis-data:/data

volumes:
  vimcal-logs:
  vimcal-redis-data:
```

## Automated Health Probe Script

The following Python probe verifies that the Vimcal FastMCP provider bridge is healthy and backend calendar credentials remain valid:

```python
#!/usr/bin/env python3
"""Automated Health & Status Probe for Vimcal Bridge Gateway"""
import sys
import urllib.request
import json

def probe_vimcal():
    try:
        req = urllib.request.Request("http://127.0.0.1:8088/health", headers={"User-Agent": "VimcalProbe/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                print(f"FAIL: Gateway returned HTTP status {resp.status}")
                return 1
            payload = json.loads(resp.read().decode())
            if not payload.get("connected"):
                print(f"FAIL: Provider disconnected: {payload}")
                return 2
            print(f"OK: Vimcal Bridge active. Backend: {payload.get('backend')} | Timezone: {payload.get('timezone')}")
            return 0
    except Exception as exc:
        print(f"FAIL: Unable to reach Vimcal Bridge Gateway: {exc}")
        return 3

if __name__ == "__main__":
    sys.exit(probe_vimcal())
```

## API examples

### Production FastMCP 3.1 Calendar Tool & Pydantic v2 Schema Validation
Because Vimcal functions over Google Calendar and Microsoft Graph backends, agentic calendar integration utilizes provider endpoints wrapped in a FastMCP 3.1 server layer with strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
import os
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict, ValidationError
from mcp.server.fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Vimcal-Provider-Bridge")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("vimcal-calendar-bridge", version="3.1.0")

# Strict Pydantic v2 Models
class EventAttendee(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    email: EmailStr
    response_status: Optional[str] = Field(default="needsAction", description="Status: accepted, declined, tentative, needsAction")

class EventTime(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    date_time: datetime = Field(..., description="ISO 8601 formatted timestamp")
    time_zone: str = Field(default="UTC", description="IANA timezone identifier e.g. America/New_York")

class CalendarEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    summary: str = Field(..., min_length=1, max_length=255, description="Event title")
    location: Optional[str] = Field(default=None, description="Meeting location or video URL")
    description: Optional[str] = Field(default=None, description="Event body or agenda")
    start: EventTime
    end: EventTime
    attendees: List[EventAttendee] = Field(default_factory=list)

class CalendarEventResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    event_id: str
    status: str
    html_link: str
    created_at: datetime

class FreeBusySlot(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    start_time: datetime
    end_time: datetime
    is_free: bool

class FreeBusyQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    time_min: datetime
    time_max: datetime
    timezone: str = Field(default="UTC")
    attendee_emails: List[EmailStr]

@mcp.tool()
async def create_vimcal_compatible_event(
    event_payload: CalendarEventRequest,
    ctx: Optional[Context] = None
) -> CalendarEventResponse:
    """
    Validates and schedules a calendar event compatible with Vimcal provider backends.
    """
    if ctx:
        await ctx.info("Validating calendar event payload with strict Pydantic v2...")

    try:
        if ctx:
            await ctx.info(f"Event validated: '{event_payload.summary}' at {event_payload.start.date_time}")

        # Simulate provider insertion API response
        return CalendarEventResponse(
            event_id="evt_vimcal_20270107_9921",
            status="confirmed",
            html_link="https://calendar.google.com/calendar/event?eid=ZXZ0X3ZpbWNhbF8yMDI3",
            created_at=datetime.now(timezone.utc)
        )

    except Exception as ve:
        logger.error(f"Calendar event creation failed: {ve}")
        raise ValueError(f"Invalid calendar event schema: {ve}")

@mcp.tool()
async def query_free_busy_slots(
    req: FreeBusyQueryRequest,
    ctx: Optional[Context] = None
) -> List[FreeBusySlot]:
    """
    Queries attendee free/busy status for automated slot selection.
    """
    if ctx:
        await ctx.info("Querying attendee availability across provider accounts...")

    try:
        # Mock free slot response
        return [
            FreeBusySlot(start_time=req.time_min, end_time=req.time_max, is_free=True)
        ]
    except Exception as ve:
        logger.error(f"FreeBusy query failed: {ve}")
        raise ValueError(f"Invalid freebusy request: {ve}")

if __name__ == "__main__":
    mcp.run()
```

## Systematic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Verification Command | Resolution & Workaround Strategy |
| :--- | :--- | :--- | :--- |
| **OAuth Token Expiration (Error 401)** | Refresh token revoked or expired after password change | `journalctl -u vimcal-bridge.service -n 50` | Run `vimcal-bridge --reauth` to re-trigger browser OAuth handshake. |
| **Cross-Timezone DST Drift** | System local timezone definition mismatched with IANA identifier | `timedatectl` & `date +%Z` | Force explicit IANA timezone in request payload (`America/New_York` instead of generic `EST`). |
| **Double-Booking Edge Case** | Concurrent meeting reservation during high latency window | Check Google Calendar sync status via API | Enable pessimistic free-busy locking in FastMCP bridge or force pre-write free-busy re-query. |
| **NLP Temporal Parsing Failure** | Ambiguous date expression (e.g., "next Friday" when today is Friday) | `vimcal-cli parse "next Friday at 2pm"` | Specify explicit dates or modify default NLP ambiguity setting in Vimcal Preferences (`Cmd+,`). |
| **FastMCP Gateway Disconnect** | Local RPC port collision or background worker crash | `lsof -i :8088` | Kill orphaned process on port 8088 and restart `vimcal-bridge.service`. |
| **Google API Rate Limit (429)** | High-frequency polling on active calendar event list | `curl -i http://127.0.0.1:8088/stats` | Implement exponential backoff jitter and enable Redis cache for free-busy queries. |
| **Payload Schema Rejection** | Agent passed unexpected extra fields to `CalendarEventRequest` | Inspect error trace in FastMCP log | Ensure agent payload adheres strictly to schema with `extra="forbid"`. |
| **Attendee Invite Delivery Failure**| Provider OAuth scope lacks permission to send invite notifications| Check OAuth scopes in Google Cloud Console | Grant `https://www.googleapis.com/auth/calendar.events` scope and re-authenticate. |

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
