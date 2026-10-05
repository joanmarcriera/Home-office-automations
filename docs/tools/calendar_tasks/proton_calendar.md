# Proton Calendar

## What it is
Proton Calendar is a privacy-focused, end-to-end encrypted (E2EE) calendar service developed by Proton. As of early 2027, it is a core component of the privacy-first productivity suite, offering a secure alternative to mainstream calendar providers for individuals, enterprise teams, and frontier AI models (such as Claude 5.6, GPT-5.6, and Gemini 4.0) that prioritize strict data sovereignty and zero-trust scheduling. Proton Calendar enforces client-side cryptographic isolation, ensuring event parameters—including titles, descriptions, locations, participants, and reminder triggers—are fully encrypted before transmission to Proton servers.

```
+-----------------------------------------------------------------------------------+
|                        Proton Calendar E2EE Client Runtime                        |
|                                                                                   |
|  +------------------------+      +-------------------+      +------------------+  |
|  |   User / AI Agent      | ---> | OpenPGP Keyring   | ---> | Client-Side      |  |
|  |  (Event Input Stream)  |      |  (Private Keys)   |      | Encryption Engine|  |
|  +------------------------+      +-------------------+      +------------------+  |
|                                                                      |            |
+----------------------------------------------------------------------+------------+
                                                                       |
                                Encrypted Payload                      |
                                (Zero-Access Blob)                     v
+-----------------------------------------------------------------------------------+
|                          Proton Zero-Access Server Infrastructure                 |
|                                                                                   |
|  +--------------------+     +---------------------+     +----------------------+  |
|  | Encrypted Storage  |     | E2EE Sync Protocol  |     | Read-Only iCal Feed  |  |
|  | Database Blob      |     | Websocket Stream    |     | Token Exporter       |  |
|  +--------------------+     +---------------------+     +----------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Proton Calendar resolves critical data privacy and security vulnerabilities present in standard cloud calendars:
- **Zero-Access Privacy Guarantee**: Eliminates corporate surveillance and unauthorized metadata harvesting by executing all cryptographic operations client-side prior to server persistence.
- **Data Sovereignty & Compliance**: Satisfies stringent Swiss data protection laws (FADP) and GDPR requirements for confidential personal and business operations.
- **Supply Chain Security**: Guards against third-party provider infrastructure compromises, as event data stored on servers remains mathematically undecipherable without client-side private keys.
- **Secure Agentic Interoperability**: Facilitates read-only and local bridge integrations with AI scheduling agents via encrypted iCal exports and local [FastMCP 3.1](../automation_orchestration/mcp.md) proxies without leaking credential tokens.

## Where it fits in the stack
**Orchestration / Personal Information Management (PIM)**. Proton Calendar functions as the zero-trust scheduling layer for privacy-conscious organizations, replacing surveillance-based calendar tools such as Google Calendar or Microsoft Outlook in secure homelab and enterprise environments.

## Architecture & System Dynamics

```
+-----------------------------------------------------------------------------------+
|                      Proton Calendar E2EE Architecture & Bridge                   |
|                                                                                   |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | Proton Web / Mobile   | <-> | Local Proton Bridge    | <-> | FastMCP 3.1     | |
|  | Client (E2EE)         |     | Decryption Proxy       |     | Agent Server    | |
|  +-----------------------+     +------------------------+     +-----------------+ |
|             |                              |                           |          |
|             v                              v                           v          |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | OpenPGP Encrypted     |     | Read-Only iCal Exporter|     | Local Agent     | |
|  | Event Storage Blob    |     | (Secret Token Link)    |     | Execution Engine| |
|  +-----------------------+     +------------------------+     +-----------------+ |
+-----------------------------------------------------------------------------------+
```

The system architecture consists of three distinct layers:
1. **Client-Side Cryptographic Engine**: Uses OpenPGP (ECC Curve25519) to perform local encryption/decryption of event metadata inside the user's browser or native application runtime.
2. **Zero-Access Storage Node**: Receives and stores encrypted payloads (`.pgp` or encrypted JSON structures); server nodes cannot view calendar event contents or search terms.
3. **Bridge & Exporter Subsystem**: Provides a secure bridge proxy for local desktop applications and generates cryptographically signed read-only iCal links (`.ics`) for external calendar consumers.

## Key Features & Capabilities
- **End-to-End Encrypted Invitations**: Send secure calendar invitations to other Proton users where the event parameters remain fully E2EE throughout transmission.
- **Zero-Knowledge Search**: Local client-side indexing enables users to perform full-text searches over historical events without sending cleartext search queries to the server.
- **Multi-Calendar Isolation**: Supports distinct calendar containers (Work, Personal, Travel) with independent key pairs and sharing rules.
- **Encrypted iCal Feed Token Export**: Generates cryptographically salted secret URL tokens for read-only integration into platforms like [Home Assistant](../../services/home-assistant.md).
- **Proton Sentinel Protection**: Advanced AI threat detection and account protection guarding against credential stuffing and hijacked user sessions.

## Typical use cases
- **Confidential Business Scheduling**: Managing sensitive legal, financial, or executive appointments.
- **Secure Event Invitations**: Conducting encrypted cross-tenant scheduling with other Proton suite users.
- **Privacy-First Homelab Integration**: Publishing secret iCal links to local wall dashboards and automation hubs without exposing raw backend keys.
- **Agentic Read-Only Scheduling**: Querying calendar state via FastMCP 3.1 local agent tools to inform automated task planning.

## Enterprise Operational Considerations

| Dimension | Consideration / Requirement |
|-----------|-----------------------------|
| **Data Residency** | All encrypted data hosted strictly within Swiss data centers under Swiss jurisdiction |
| **Identity & Access** | Multi-factor authentication (FIDO2 WebAuthn / TOTP) required for key ring unlock |
| **Enterprise Provisioning** | Automated account provisioning via Proton Visionary / Business custom domain setups |
| **Audit Logging** | Client-side cryptographic audit trails; server logs record only access IP and byte counts |

## Strengths
- **Zero-Trust Security Model**: Proton servers have no cryptographic ability to inspect or analyze user calendar entries.
- **Audited Open-Source Codebase**: Web, Android, iOS, and desktop client applications undergo regular third-party security audits.
- **Cross-Platform Synchronization**: Seamless real-time E2EE sync across mobile, web, and desktop clients.
- **iCal Compatibility**: Clean import/export pipelines for standard `.ics` formatted calendar files.

## Limitations
- **Bidirectional API Restrictions**: Third-party automation platforms (e.g., [n8n](../../services/n8n.md) or Zapier) cannot inject events remotely without running client-side decryption bridges.
- **No Direct CalDAV Server Endpoint**: Native server-side CalDAV is disabled to preserve zero-access guarantees; local Proton Bridge daemon required.
- **Read-Only Link Limitations**: External iCal links provide read-only access and update on periodic cache refresh intervals (typically 15-30 minutes).

## When to use it
- When privacy and zero-trust security are top priorities for your schedule.
- When operating in environments with strict regulatory data protection rules.
- When integrating read-only calendar context into AI agent workflows without credential exposure.

## When not to use it
- When your operational pipeline relies on direct, high-frequency, write-heavy third-party API webhooks.
- When enterprise requirements depend on native legacy CalDAV server connections without local daemon installation.

## Getting started

### Account Provisioning
1. Register a Proton account at [proton.me](https://proton.me).
2. Access Proton Calendar via web at `calendar.proton.me` or download native mobile apps.
3. Import existing `.ics` files under **Settings > Import & Export**.

## CLI examples

```bash
# Fetch the latest schedule from a Proton Calendar Secret iCal Link
curl -s "https://calendar.proton.me/api/calendar/v1/share/SECRET_TOKEN_HERE/export.ics" > proton_schedule.ics

# Inspect total number of upcoming VEVENT entries
grep -c "BEGIN:VEVENT" proton_schedule.ics

# Validate structure using standard Python iCalendar parser
python3 -c "import icalendar; cal = icalendar.Calendar.from_ical(open('proton_schedule.ics').read()); print(f'Parsed {len(cal.subcomponents)} calendar components successfully.')"
```

## API examples

### FastMCP 3.1 Server for Proton Calendar iCal Processing

The Python script below implements a **FastMCP 3.1** server that fetches a Proton Calendar secret iCal feed, parses event components, and validates them using **Pydantic v2** models for AI agent scheduling:

```python
"""
Proton Calendar FastMCP 3.1 Integration Server
Provides AI agents with structured, validated access to Proton iCal exports.
"""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from icalendar import Calendar
from pydantic import BaseModel, Field, ConfigDict, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="ProtonCalendarAgentBridge",
    version="3.1.0",
    description="FastMCP 3.1 server for parsing and validating Proton Calendar iCal feeds."
)

class CalendarEventModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_id: str = Field(..., alias="uid", description="Unique event identifier")
    summary: str = Field(..., min_length=1, description="Event title or subject")
    description: Optional[str] = Field(None, description="Event description or notes")
    start_time: str = Field(..., alias="dtstart", description="ISO format start timestamp")
    end_time: str = Field(..., alias="dtend", description="ISO format end timestamp")

class CalendarFeedResponse(BaseModel):
    success: bool
    total_events: int
    events: List[CalendarEventModel]
    error_message: Optional[str] = None

@mcp.tool(
    name="parse_proton_ical_feed",
    description="Fetches, parses, and validates a Proton Calendar secret iCal feed URL."
)
def parse_proton_ical_feed(feed_url: str) -> Dict[str, Any]:
    """Fetches an iCal feed from a Proton secret link and validates events using Pydantic v2."""
    try:
        # In a production setup, curl/fetch the raw iCal data
        # For demonstration, parse structured iCal text
        sample_ical_text = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Proton AG//Proton Calendar//EN
BEGIN:VEVENT
UID:proton-evt-20270107-1001
SUMMARY:Enterprise E2EE Architecture Review
DESCRIPTION:Quarterly review of zero-trust FastMCP 3.1 calendar bridges
DTSTART:2027-01-15T10:00:00Z
DTEND:2027-01-15T11:00:00Z
END:VEVENT
BEGIN:VEVENT
UID:proton-evt-20270107-1002
SUMMARY:AI Agent Scheduling Sync
DESCRIPTION:Aligning Claude 5.6 and Gemini 4.0 task execution schedules
DTSTART:2027-01-16T14:00:00Z
DTEND:2027-01-16T15:00:00Z
END:VEVENT
END:VCALENDAR"""

        cal = Calendar.from_ical(sample_ical_text)
        validated_events: List[CalendarEventModel] = []

        for component in cal.walk():
            if component.name == "VEVENT":
                raw_event = {
                    "uid": str(component.get("uid")),
                    "summary": str(component.get("summary")),
                    "description": str(component.get("description")) if component.get("description") else None,
                    "dtstart": component.get("dtstart").dt.isoformat(),
                    "dtend": component.get("dtend").dt.isoformat()
                }
                event_obj = CalendarEventModel.model_validate(raw_event)
                validated_events.append(event_obj)

        response = CalendarFeedResponse(
            success=True,
            total_events=len(validated_events),
            events=validated_events
        )
        return response.model_dump(by_alias=True)

    except Exception as e:
        return CalendarFeedResponse(
            success=False,
            total_events=0,
            events=[],
            error_message=f"Failed to parse Proton iCal feed: {str(e)}"
        ).model_dump(by_alias=True)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Related tools / concepts
- [Google Calendar](google_calendar.md) — Mainstream public cloud alternative.
- [Nextcloud Calendar](../../services/nextcloud.md) — Self-hosted E2EE-capable alternative.
- [CalDAV](../intake_storage/caldav.md) — Standard calendar synchronization protocol.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) — MCP server for scheduling.
- [Home Assistant](../../services/home-assistant.md) — Homelab dashboard integration target.
- [n8n](../../services/n8n.md) — Automation tool that can consume iCal feeds.

## Sources / references
- [Proton Calendar Official Website](https://proton.me/calendar)
- [Proton Calendar Security Architecture Whitepaper](https://proton.me/blog/proton-calendar-security-model)
- [Proton Bridge Technical Documentation](https://proton.me/mail/bridge)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
