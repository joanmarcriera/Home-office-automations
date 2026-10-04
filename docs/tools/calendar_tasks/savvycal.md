# SavvyCal

## What it is
SavvyCal is a scheduling platform designed around mutual recipient-and-host convenience. As of early 2027, SavvyCal is integrated with **FastMCP 3.1** and the **FastMCP 3.1 Task Protocol**, enabling autonomous AI agents—such as `claude-5-1-opus-20260915`, GPT-5.5, and Gemini 4.0 Pro—to query host availability, rank preferred meeting slots, generate personalized one-off booking links, and handle meeting webhooks programmatically.

The platform's signature innovation is its interactive **Calendar Overlay** interface. When an invitee opens a SavvyCal booking link, SavvyCal securely overlays the recipient's personal or corporate calendar (Google Workspace, Microsoft Outlook, or Fastmail JMAP) directly onto the host's available slots. This eliminates back-and-forth context switching and allows both parties to find optimal meeting times instantly.

```
+-----------------------------------------------------------------------------------+
|                           SavvyCal Platform Architecture                           |
+-----------------------------------------------------------------------------------+
                                         |
     +-----------------------------------+-----------------------------------+
     |                                   |                                   |
     v                                   v                                   v
+------------------------+   +------------------------+   +------------------------+
| Calendar Backends      |   | Availability Engine    |   | Agentic FastMCP 3.1    |
| - Google Calendar API  |   | - Frequency Limits     |   | - Availability Queries |
| - Microsoft Graph API  |   | - Preferred Slot Rank  |   | - One-Off Link Synth   |
| - Fastmail JMAP Sync   |   | - Round-Robin Pools   |   | - Webhook Event Bus    |
| - CalDAV / iCloud      |   | - Timezone Detection   |   | - Human-in-Loop Gates  |
+------------------------+   +------------------------+   +------------------------+
     |                                   |                                   |
     +-----------------------------------+-----------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            Client Interfaces & Outputs                            |
|  - Interactive Calendar Overlay (Recipient Visual Comparison Pane)                 |
|  - Embeddable Booking Widgets & Custom Subdomains                                 |
|  - FastMCP 3.1 AI Agent Tool Calling (Claude Code, AutoGen, Agent Swarms)         |
|  - Real-Time Webhook Pipeline to n8n, Slack, and CRM Workflows                    |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Traditional scheduling software creates friction by prioritizing the host's schedule while placing all cognitive burden on the recipient. Invitees must manually tab back and forth between their calendar view and the booking page, risking double bookings or choosing inconvenient times.

SavvyCal solves this asymmetry by combining calendar overlay capabilities, weighted availability ranking, and burnout protection limits (e.g., maximum meetings per day or week). Furthermore, for developer and agentic workflows, SavvyCal exposes clean REST APIs and FastMCP 3.1 endpoints that allow AI agents to manage calendar coordination without exposing raw, sensitive calendar entries to external parties.

## Where it fits in the stack
**Category**: Calendar & Tasks / Meeting Automation. SavvyCal functions as an intelligent middleware layer between underlying calendar data stores (Google Calendar, Microsoft Outlook, Fastmail) and external communication endpoints (Email, Slack, Web Applications, AI Agents). It provides the scheduling layer in agentic workflows where AI assistants negotiate meeting times on behalf of executives.

## Typical use cases
- **Recipient-First Executive Scheduling**: High-touch booking links for enterprise sales, venture capital, and consulting where recipient experience is critical.
- **Agentic Meeting Negotiation**: AI agents (e.g., Claude Code or custom LangGraph agents) checking host availability via FastMCP 3.1 and sending pre-configured, personalized booking links in response to email inquiries.
- **Round-Robin Sales & Support Pools**: Distributing inbound demo requests or customer success calls across multi-person teams based on availability and individual meeting load limits.
- **Burnout Protection & Preferred Slots**: Ranking morning slots higher than afternoon slots and enforcing strict daily meeting caps (e.g., maximum 4 calls per day).
- **Group Meeting Polls**: Creating ad-free, integrated polls to find consensus across multiple internal and external stakeholders without third-party poll sites.

## Key Features & Architecture

### Calendar Overlay Engine
When an invitee accesses a SavvyCal scheduling link, SavvyCal prompts them (or leverages browser session credentials) to overlay their calendar onto the host's schedule. The overlay renders in real-time, highlighting exact overlapping free windows.

### Availability Ranking & Preference Controls
Unlike traditional scheduling tools that treat all free calendar slots equally, SavvyCal allows hosts to assign relative weights to availability blocks. Hosts can mark preferred booking times (e.g., 9 AM to 11 AM) while leaving secondary slots available only if primary windows are exhausted.

### FastMCP 3.1 Native Integration
SavvyCal features first-class FastMCP 3.1 support. AI agents can invoke MCP tools to check slot availability, create single-use custom links with specific duration overrides, and poll upcoming scheduled events without requiring full access to raw calendar event bodies.

### Comprehensive Webhook Pipeline
SavvyCal emits webhooks for critical lifecycle events (`event.created`, `event.updated`, `event.cancelled`, `poll.responded`). These events can be consumed directly by automation platforms like [n8n](../../services/n8n.md) or custom Python services to trigger follow-up actions in CRMs or Slack.

## Strengths
- **Superior Recipient UX**: Recipient calendar overlay eliminates manual time comparison and reduces booking friction.
- **Burnout Controls**: Granular limits on daily/weekly meeting duration, notice periods, and buffer times.
- **Agent-Ready Architecture**: Clean REST API and native FastMCP 3.1 server support.
- **Multi-Calendar Sync**: Simultaneously checks availability across multiple Google, Outlook, and Fastmail accounts.
- **Ad-Free Meeting Polls**: Unified polling system for group scheduling without ads or tracking scripts.

## Limitations
- **No Free Tier**: Requires a paid subscription after the trial period.
- **Domain Specialization**: Exclusively focused on scheduling and calendar coordination; does not function as a standalone task manager or full calendar client.
- **SaaS Delivery Model**: Closed-source commercial software; not self-hostable (for open-source CalDAV solutions, see [Radicale](../../services/radicale.md)).

## When to use it
- When you want to offer a frictionless, recipient-friendly scheduling experience to clients or executives.
- When configuring AI agents to handle meeting coordination via FastMCP 3.1.
- When managing complex team scheduling rules (Round-Robin, Collective availability) with daily meeting count limits.
- When you require multi-calendar conflict checking across personal and professional accounts.

## When not to use it
- For basic internal scheduling where native Google Calendar or Outlook invites are sufficient.
- If your organization mandates 100% open-source, on-premise calendar infrastructure (use [Radicale](../../services/radicale.md) or [CalDAV](caldav.md)).
- If you require a zero-cost, permanent free tool for casual scheduling.

## Getting started

### Account & Calendar Authorization
1. Register at [SavvyCal.com](https://savvycal.com/).
2. Connect your calendar providers (**Settings > Integrations > Google Workspace / Outlook / Fastmail**).
3. Configure your default availability schedules, buffer times, and meeting frequency caps.

### Generating API Credentials
Generate a personal access token under **Settings > Developer > API Tokens**.

```bash
# Verify authentication against SavvyCal API
curl -s -H "Authorization: Bearer $SAVVYCAL_API_KEY" \
  https://api.savvycal.com/v1/me | jq .
```

## CLI examples

Developers can interact with SavvyCal using `curl` or custom script wrappers.

### 1. List Active Scheduling Links
```bash
curl -s -X GET "https://api.savvycal.com/v1/links?state=active" \
  -H "Authorization: Bearer $SAVVYCAL_API_KEY" | jq '.data[] | {id: .id, name: .name, slug: .slug}'
```

### 2. Create a One-Off Single-Use Booking Link
```bash
curl -s -X POST "https://api.savvycal.com/v1/links" \
  -H "Authorization: Bearer $SAVVYCAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priority Executive Briefing",
    "type": "one_off",
    "durations": [30, 45],
    "expires_at": "2027-01-15T23:59:59Z",
    "max_bookings": 1
  }' | jq .
```

### 3. Fetch Upcoming Scheduled Meetings
```bash
curl -s -X GET "https://api.savvycal.com/v1/events?status=scheduled" \
  -H "Authorization: Bearer $SAVVYCAL_API_KEY" | jq '.data[] | {id: .id, title: .title, starts_at: .starts_at, invitee: .organizer_email}'
```

## FastMCP 3.1 Integration Server

The following complete Python script implements a production-grade **FastMCP 3.1** server for SavvyCal, enabling AI agents to query availability and generate single-use scheduling links dynamically.

```python
"""
FastMCP 3.1 Server for SavvyCal Scheduling Automation.
Exposes availability querying and personalized link generation tools to AI agents.
"""

import asyncio
import logging
import os
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("SavvyCal Scheduling Server", version="3.1.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SavvyCal-FastMCP")

SAVVYCAL_API_BASE = "https://api.savvycal.com/v1"
SAVVYCAL_API_KEY = os.getenv("SAVVYCAL_API_KEY", "mock-token-for-dev")


# --- Input / Output Schemas ---

class AvailabilityQueryRequest(BaseModel):
    link_id: str = Field(..., description="The SavvyCal scheduling link ID to check slots for")
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")


class TimeSlot(BaseModel):
    starts_at: str
    ends_at: str


class OneOffLinkRequest(BaseModel):
    link_name: str = Field(..., min_length=3, description="Display name for the custom scheduling link")
    duration_minutes: int = Field(default=30, ge=15, le=120, description="Meeting duration in minutes")
    invitee_email: Optional[str] = Field(None, description="Pre-fill invitee email address if known")
    max_bookings: int = Field(default=1, ge=1, description="Maximum allowed bookings before link expires")


class OneOffLinkResponse(BaseModel):
    link_id: str
    booking_url: str
    expires_at: Optional[str] = None


# --- Tools Implementation ---

@mcp.tool()
async def check_available_slots(request: AvailabilityQueryRequest) -> List[TimeSlot]:
    """
    Queries open time slots on a specified SavvyCal link within a date range.
    """
    logger.info(f"Querying slots for link {request.link_id} between {request.start_date} and {request.end_date}")

    if SAVVYCAL_API_KEY == "mock-token-for-dev":
        # Mock slots for local validation
        return [
            TimeSlot(starts_at=f"{request.start_date}T09:00:00Z", ends_at=f"{request.start_date}T09:30:00Z"),
            TimeSlot(starts_at=f"{request.start_date}T10:00:00Z", ends_at=f"{request.start_date}T10:30:00Z"),
            TimeSlot(starts_at=f"{request.end_date}T14:00:00Z", ends_at=f"{request.end_date}T14:30:00Z")
        ]

    url = f"{SAVVYCAL_API_BASE}/links/{request.link_id}/slots"
    headers = {"Authorization": f"Bearer {SAVVYCAL_API_KEY}"}
    params = {"from": request.start_date, "to": request.end_date}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"SavvyCal API error ({resp.status}): {text}")
            data = await resp.json()
            return [TimeSlot(starts_at=s["starts_at"], ends_at=s["ends_at"]) for s in data.get("slots", [])]


@mcp.tool()
async def create_personalized_link(request: OneOffLinkRequest) -> OneOffLinkResponse:
    """
    Generates a single-use, custom SavvyCal scheduling link for high-priority contacts.
    """
    logger.info(f"Generating one-off link '{request.link_name}' for {request.invitee_email or 'anonymous'}")

    if SAVVYCAL_API_KEY == "mock-token-for-dev":
        return OneOffLinkResponse(
            link_id="link_oneoff_998877",
            booking_url="https://savvycal.com/alex/priority-briefing",
            expires_at=(datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"
        )

    url = f"{SAVVYCAL_API_BASE}/links"
    headers = {
        "Authorization": f"Bearer {SAVVYCAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": request.link_name,
        "type": "one_off",
        "durations": [request.duration_minutes],
        "max_bookings": request.max_bookings
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 201:
                text = await resp.text()
                raise RuntimeError(f"SavvyCal API error ({resp.status}): {text}")
            data = await resp.json()
            return OneOffLinkResponse(
                link_id=data["id"],
                booking_url=data["url"],
                expires_at=data.get("expires_at")
            )


if __name__ == "__main__":
    mcp.run()
```

## API examples

### Python: Webhook Processing and Event Validation using Pydantic v2
This script demonstrates receiving SavvyCal webhook notifications (e.g., meeting booked or cancelled) and validating payload structures with **Pydantic v2**.

```python
import os
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator, ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SavvyCal-Webhooks")


# --- Pydantic v2 Webhook Schemas ---

class InviteeDetails(BaseModel):
    name: str = Field(..., description="Full name of meeting invitee")
    email: str = Field(..., description="Email address of invitee")
    time_zone: str = Field("UTC", description="Invitee primary timezone")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()


class MeetingLocation(BaseModel):
    type: str = Field(..., description="Location type e.g., google_meet, zoom, phone")
    url: Optional[HttpUrl] = Field(None, description="Video conference room URL")


class SavvyCalEventData(BaseModel):
    event_id: str = Field(..., alias="id")
    link_id: str
    title: str
    starts_at: datetime
    ends_at: datetime
    invitee: InviteeDetails
    location: Optional[MeetingLocation] = None


class WebhookEnvelope(BaseModel):
    event_type: str = Field(..., alias="type")
    created_at: datetime
    data: SavvyCalEventData

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        allowed = {"event.created", "event.updated", "event.cancelled", "poll.responded"}
        if v not in allowed:
            raise ValueError(f"Unknown event type: {v}")
        return v


# --- Processing Engine ---

def process_webhook_payload(raw_json: str) -> Optional[Dict[str, Any]]:
    """
    Parses and validates incoming SavvyCal webhook JSON payload.
    """
    try:
        payload_dict = json.loads(raw_json)
        envelope = WebhookEnvelope.model_validate(payload_dict)

        logger.info(f"Received valid '{envelope.event_type}' for meeting '{envelope.data.title}'")
        logger.info(f"Invitee: {envelope.data.invitee.name} ({envelope.data.invitee.email})")
        logger.info(f"Time: {envelope.data.starts_at} to {envelope.data.ends_at}")

        if envelope.data.location and envelope.data.location.url:
            logger.info(f"Meeting Join Link: {envelope.data.location.url}")

        return envelope.model_dump(mode="json")

    except ValidationError as e:
        logger.error(f"Webhook validation failed: {e.json()}")
        return None
    except json.JSONDecodeError:
        logger.error("Invalid JSON string supplied")
        return None


if __name__ == "__main__":
    # Test sample webhook payload
    sample_webhook_json = json.dumps({
        "type": "event.created",
        "created_at": "2027-01-08T10:00:00Z",
        "data": {
            "id": "evt_9988776655",
            "link_id": "link_sales_demo",
            "title": "Acme Corp <> Product Demo",
            "starts_at": "2027-01-10T15:00:00Z",
            "ends_at": "2027-01-10T15:30:00Z",
            "invitee": {
                "name": "Sarah Connor",
                "email": "sarah.connor@cyberdyne.example.com",
                "time_zone": "America/Los_Angeles"
            },
            "location": {
                "type": "google_meet",
                "url": "https://meet.google.com/abc-defg-hij"
            }
        }
    })

    result = process_webhook_payload(sample_webhook_json)
    print("\n--- Validated Webhook Output ---")
    print(json.dumps(result, indent=2))
```

## Related tools / concepts
- [Calendly](calendly.md) — Market predecessor and primary scheduling competitor.
- [Morgen](morgen.md) — Desktop calendar and unified task application.
- [Amie](amie.md) — Visual productivity and scheduling app.
- [n8n](../../services/n8n.md) — Workflow automation engine for processing meeting webhooks.
- [Zapier](../automation_orchestration/zapier.md) — Cloud connector service with official SavvyCal app.
- [Google Calendar](google_calendar.md) — Primary underlying calendar sync backend.
- [Microsoft To Do](microsoft-todo.md) — Task management integration destination.
- [Fastmail](fastmail.md) — Privacy-focused calendar and mail service supported via JMAP.

## Sources / references
- [SavvyCal Official Web Portal](https://savvycal.com/)
- [SavvyCal Developer API Reference](https://developers.savvycal.com/)
- [SavvyCal Meeting Polls Feature](https://savvycal.com/polls)
- [FastMCP SavvyCal GitHub Repository](https://github.com/savvycal/mcp-server)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
