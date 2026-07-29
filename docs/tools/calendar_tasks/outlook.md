# Microsoft Outlook Calendar

## What it is
The enterprise-standard calendar application for Microsoft 365. As of late 2026, it is deeply integrated with **Microsoft Work IQ**, a shared intelligence layer that exposes mail, calendar, and meeting data to AI agents via the Model Context Protocol (MCP 3.1).

## What problem it solves
Provides professional-grade scheduling, meeting management, and resource booking integrated with email and corporate directories. It handles complex enterprise needs like delegated access, cross-tenant availability, and automated meeting transcription/summarization via Copilot.

## Where it fits in the stack
**Category**: Calendar & Tasks / Personal Information Management

## Typical use cases
- **Enterprise scheduling**: Manage complex team calendars and physical resource (room) bookings.
- **AI-assisted coordination**: Use **Work IQ** to allow agents like **Claude 5.1** or **GPT-5.5** to schedule meetings based on organizational context.
- **Hybrid work management**: Automatically coordinate in-person vs. remote attendance.
- **Meeting lifecycle**: From scheduling to automated action item extraction using Microsoft 365 Copilot.

## Strengths
- Deep integration with Microsoft 365, Teams, and the wider Graph ecosystem.
- Robust enterprise security, compliance, and centralized IT governance.
- **Work IQ Native**: First-party MCP 3.1 servers allow agents to "reason" over calendar data securely.

## Limitations
- Can be complex to configure for personal/independent use cases outside Microsoft 365.
- API access (Microsoft Graph) requires Entra ID app registration and OAuth complexity.

## When to use it
- In corporate environments or home offices already standardized on Microsoft 365.
- When you require deep integration with Outlook email and Teams meetings.
- If you need a secure, compliant way for AI agents to interact with your schedule.

## When not to use it
- For simple personal use cases where [Google Calendar](google_calendar.md) or [Proton Calendar](proton_calendar.md) suffice.
- If you prefer a local-first, privacy-focused, or fully open-source solution.

## Getting started
### CLI for Microsoft 365
The official CLI now includes an **MCP server mode**.
1. Install the CLI:
   ```bash
   npm install -g @pnp/cli-microsoft365
   ```
2. Log in to your account:
   ```bash
   m365 login
   ```
3. **Hello-world example**: List your upcoming events:
   ```bash
   m365 outlook event list
   ```

## CLI examples
The CLI is the primary tool for administrators and power users.

### Run as an MCP 3.1 Server
You can start the CLI in MCP mode to give your AI assistant immediate access:
```bash
m365 mcp start
```

### Advanced Calendar Management
```bash
# Find available rooms for a specific time
m365 outlook room list --placeName "Conference Room"

# Create a meeting with a Teams link
m365 outlook event add --subject "Architecture Review" --start "2026-11-15T10:00:00" --end "2026-11-15T11:00:00" --isOnlineMeeting true
```

## API examples
The **Microsoft Graph API** is the underlying engine for all Outlook integrations.

### Create and Validate an Event (Python)
Programmatic event creation should be validated using **Pydantic v2** prior to making requests to the Microsoft Graph API under late-2026 guidelines.

```python
import requests
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Define Pydantic v2 Schema for Outlook/Graph Calendar Event
class DateTimeTimeZone(BaseModel):
    dateTime: datetime = Field(..., description="ISO 8601 formatted datetime")
    timeZone: str = Field(default="UTC", description="Standardized timezone string")

class EmailAddress(BaseModel):
    name: str
    address: EmailStr

class Attendee(BaseModel):
    emailAddress: EmailAddress
    type: str = Field(default="required")

class OutlookEventPayload(BaseModel):
    subject: str = Field(..., min_length=1, max_length=150)
    body_content: Optional[str] = Field(default=None, alias="bodyPreview")
    start: DateTimeTimeZone
    end: DateTimeTimeZone
    attendees: List[Attendee] = Field(default_factory=list)

# Validate payload
raw_event = {
    "subject": "Microsoft 365 Graph Sync with Claude 5.1",
    "bodyPreview": "Validating Outlook Calendar models under MCP 3.1.",
    "start": {
        "dateTime": "2026-11-20T14:00:00Z",
        "timeZone": "UTC"
    },
    "end": {
        "dateTime": "2026-11-20T15:00:00Z",
        "timeZone": "UTC"
    },
    "attendees": [
        {
            "emailAddress": {
                "name": "Jane Doe",
                "address": "[email protected]"
            },
            "type": "required"
        }
    ]
}

try:
    validated_event = OutlookEventPayload.model_validate(raw_event)
    print(f"Validated Outlook event successfully: '{validated_event.subject}'")

    # POST to Microsoft Graph API
    API_TOKEN = "YOUR_ACCESS_TOKEN"
    API_URL = "https://graph.microsoft.com/v1.0/me/events"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    # response = requests.post(API_URL, headers=headers, json=validated_event.model_dump(by_alias=True))
except Exception as e:
    print(f"Validation failed: {e}")
```

## Model Context Protocol (MCP 3.1) Integration
Microsoft provides official **Work IQ MCP servers** for enterprise tenants.

**Available Tools (via Work IQ):**
- `mcp_outlook_list_events`: Fetch schedule for a given range.
- `mcp_outlook_create_event`: Schedule new meetings with intelligent conflict resolution.
- `mcp_outlook_find_meeting_times`: Identify the best time for multiple attendees.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Microsoft 365), Free (Outlook.com)
- **Self-hostable**: No (Cloud), Yes (Exchange Server - Legacy)

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Microsoft Graph](../providers/microsoft-graph.md)
- [Microsoft Work IQ](../automation_orchestration/mcp.md)
- [Microsoft To Do](microsoft-todo.md)
- [Reclaim](reclaim.md) — Excellent for AI-driven Outlook scheduling.
- [Chronos MCP](../automation_orchestration/mcp.md)
- [n8n](../../services/n8n.md)

## Sources / references
- [Microsoft Outlook](https://outlook.live.com/)
- [Microsoft Graph API](https://developer.microsoft.com/en-us/graph)
- [Work IQ MCP Overview (Microsoft Learn)](https://learn.microsoft.com/en-us/microsoft-agent-365/tooling-servers-overview)
- [CLI for Microsoft 365](https://pnp.github.io/cli-microsoft365/)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
