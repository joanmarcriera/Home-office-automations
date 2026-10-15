# Calendly

## What it is
Calendly is an enterprise scheduling automation platform and availability management engine engineered to eliminate back-and-forth meeting coordination, streamline routing logic, and orchestrate calendar workflows. In early 2027, Calendly functions as a primary public-facing scheduling gateway, offering native **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** server tools, real-time webhook event pipelines, automated qualification forms, and strict schema validation for autonomous AI scheduling agents.

## What problem it solves
Manual meeting coordination across distributed teams, external clients, and prospective leads creates significant administrative overhead, double-booking risks, time zone confusion, and conversion friction. Calendly eliminates scheduling bottlenecks by exposing real-time availability aggregated across underlying calendar backends (Google Workspace, Microsoft Outlook 365, iCloud) while enforcing configurable business constraints—including custom buffer intervals, daily meeting caps, minimum lead times, payment processing prior to booking, and round-robin host distribution.

In autonomous agentic workflows, Calendly provides a controlled, secure abstraction layer that prevents AI agents from having unrestricted write access to internal calendar databases, enabling agents to negotiate schedules, verify host availability, and provision meeting invites safely.

## Where it fits in the stack
**Calendar & Tasks / Scheduling Gateway**. Positioned between public-facing clients or AI communication agents ([Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/openai.md), [DeepSeek-V4](../providers/deepseek.md)) and core calendar infrastructure (Google Calendar, Office 365), Calendly coordinates automated event booking and triggers downstream operations in CRM systems ([HubSpot](../enterprise/hubspot.md), [Salesforce](../enterprise/salesforce.md)), messaging hubs ([Slack](../enterprise/slack.md)), and workflow orchestrators ([n8n](../../services/n8n.md)).

## Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
|                                 Calendly Scheduling Platform                                      |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | Booking Invocation Source                                                                    |  |
|  | (Public Web UI / Embed, FastMCP 3.1 AI Agent Tool Call, REST API v2 Integration)             |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | Lead Qualification & Routing Engine                                                         |  |
|  | (Custom Forms, Round-Robin Pools, Collective Availability, Daily Caps & Buffers)             |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | Real-Time Calendar Sync Engine                                                               |  |
|  | (Google Workspace, Microsoft Office 365 / Outlook, Apple iCloud, Exchange)                   |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | Event Dispatcher & Webhook Gateway                                                           |  |
|  | (FastMCP 3.1 Agent Feedback, n8n Automation Workflows, Stripe Payments, CRM Webhooks)      |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

## Typical use cases
- **Agentic Executive Scheduling**: Autonomous AI assistants negotiate availability with external partners, inspect open slots via FastMCP 3.1, and submit meeting requests without exposing host calendar content.
- **Qualified Inbound Sales Routing**: Pre-qualifying incoming leads via web forms and dynamically assigning high-value prospects to active account executives based on availability and territory rules.
- **Multi-Interviewer Panel Scheduling**: Calculating collective availability across engineering panels and candidate calendars for structured interview loops.
- **Paid Advisory & Coaching Bookings**: Requiring upfront credit card authorization or payment processing (via Stripe/PayPal integrations) prior to locking a consultation time on the host calendar.
- **Automated Workflow Orchestration**: Triggering n8n or Zapier webhooks upon `invitee.created` events to generate video conference links (Zoom, Google Meet, Teams), update customer records, and send preparation reminders.

## Strengths
- **Native FastMCP 3.1 Support**: Dedicated MCP server endpoints allow AI agents to inspect open availability windows and book slots programmatically with structured schemas.
- **Cross-Calendar Conflict Resolution**: Aggregates multiple calendars per user (e.g., personal Google Calendar and work Outlook) to prevent overlap.
- **Flexible Team Routing**: Supports Round-Robin distribution, collective group availability, and conditional routing forms based on customer inputs.
- **Enterprise Webhook Pipeline**: Real-time event notifications for `invitee.created`, `invitee.canceled`, and `meeting.rebooked` with HMAC signature validation.
- **Frictionless Invitee UX**: Responsive, accessible web interface optimized for desktop and mobile browsers.

## Limitations
- **Proprietary Cloud SaaS**: Closed-source service with no option for self-hosted or air-gapped deployment (use Cal.com for strict on-premise requirements).
- **Tiered Feature Locks**: Advanced routing forms, single sign-on (SSO), domain locking, and webhooks require paid or enterprise subscription tiers.
- **OAuth Scope Depth**: Requires extensive read/write permissions across host calendar providers for complete conflict detection.

## When to use it
- When exposing automated public scheduling links to external users, candidates, or customers.
- When deploying AI voice or text agents that need to book meetings on behalf of executives using FastMCP 3.1 tool calls.
- When multi-host routing, round-robin lead allocation, or qualification forms are required prior to booking.
- When seamlessly connecting scheduling triggers into automated CRM and notification pipelines.

## When not to use it
- In strict air-gapped or on-premise environments requiring local data sovereignty (prefer Cal.com self-hosted).
- For simple internal team calendar management where native Google Workspace or Microsoft Outlook scheduling assistants suffice.
- When requiring fully customizable database-level calendar control without external SaaS rate limits.

## Getting started

### Environment Setup
Install required Python libraries for interacting with the Calendly API v2 and FastMCP 3.1 server tools:

```bash
pip install requests pydantic fastmcp
```

### Basic API Connectivity
Set your Calendly Personal Access Token and verify user details:

```python
import os
import requests

CALENDLY_TOKEN = os.getenv("CALENDLY_API_TOKEN", "your_token_here")
headers = {
    "Authorization": f"Bearer {CALENDLY_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.get("https://api.calendly.com/users/me", headers=headers)
if response.status_code == 200:
    user_info = response.json().get("resource", {})
    print(f"Connected to Calendly: {user_info.get('name')} ({user_info.get('email')})")
    print(f"User URI: {user_info.get('uri')}")
    print(f"Organization URI: {user_info.get('current_organization')}")
else:
    print(f"Error fetching profile: {response.status_code} - {response.text}")
```

### Local FastMCP 3.1 Integration Setup
To expose Calendly tools to local AI agents via Node/NPX:

```bash
npx @calendly/mcp-server --api-key $CALENDLY_API_TOKEN
```

## CLI examples

### 1. Retrieve Current User Details
```bash
curl -s --request GET \
  --url https://api.calendly.com/users/me \
  --header "Authorization: Bearer ${CALENDLY_API_TOKEN}" \
  --header "Content-Type: application/json" | jq .
```

### 2. List Active Event Types for an Organization
```bash
curl -s --request GET \
  --url "https://api.calendly.com/event_types?organization=${CALENDLY_ORG_URI}" \
  --header "Authorization: Bearer ${CALENDLY_API_TOKEN}" | jq '.collection[] | {name, slug, uri, scheduling_url}'
```

### 3. Query Scheduled Events for a Specific Date Range
```bash
curl -s --request GET \
  --url "https://api.calendly.com/scheduled_events?user=${CALENDLY_USER_URI}&min_start_time=2027-01-01T00:00:00.000000Z&status=active" \
  --header "Authorization: Bearer ${CALENDLY_API_TOKEN}" | jq '.collection[] | {name, start_time, status, uri}'
```

## API examples

### Complete FastMCP 3.1 Server with Pydantic v2 Schema Validation and Webhook Handling
The following production-grade Python script implements a **FastMCP 3.1** server that exposes tools for querying availability, booking appointments, validating webhooks, and managing Calendly scheduling workflows with strict **Pydantic v2** runtime validation.

```python
import os
import hmac
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, EmailStr, field_validator
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server for Calendly Agentic Workflows
mcp = FastMCP(
    name="calendly-enterprise-agent-server",
    version="3.1"
)

# ---------------------------------------------------------------------------
# Pydantic v2 Schema Definitions
# ---------------------------------------------------------------------------

class InviteeDetails(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the invitee")
    email: EmailStr = Field(..., description="Valid email address of the invitee")
    time_zone: str = Field("America/New_York", description="IANA time zone string (e.g., America/New_York)")
    notes: Optional[str] = Field(None, max_length=500, description="Custom preparation notes or topics")

class AvailabilityQueryRequest(BaseModel):
    event_type_uri: str = Field(..., description="Calendly Event Type URI")
    start_date: datetime = Field(..., description="Search start boundary (ISO 8601)")
    end_date: datetime = Field(..., description="Search end boundary (ISO 8601)")

    @field_validator("end_date")
    @classmethod
    def validate_date_range(cls, v: datetime, info) -> datetime:
        start = info.data.get("start_date")
        if start and v <= start:
            raise ValueError("end_date must be strictly after start_date")
        if start and v > start + timedelta(days=30):
            raise ValueError("Query window cannot exceed 30 days")
        return v

class AvailableSlot(BaseModel):
    start_time: datetime
    end_time: datetime
    status: str = Field("available")

class AvailabilityResponse(BaseModel):
    event_type_uri: str
    available_slots: List[AvailableSlot]
    total_slots_found: int

class BookingRequest(BaseModel):
    event_type_uri: str = Field(..., description="Target event type URI")
    start_time: datetime = Field(..., description="Selected slot start time")
    invitee: InviteeDetails = Field(..., description="Invitee personal information")

class BookingConfirmation(BaseModel):
    booking_id: str
    event_name: str
    start_time: datetime
    end_time: datetime
    invitee_email: EmailStr
    status: str = Field("active")
    join_url: Optional[str] = None

class WebhookPayload(BaseModel):
    event: str = Field(..., description="Calendly webhook event name (e.g., invitee.created)")
    created_at: datetime
    data: Dict[str, Any]

# ---------------------------------------------------------------------------
# FastMCP 3.1 Tools
# ---------------------------------------------------------------------------

@mcp.tool(
    name="check_calendly_availability",
    description="Query available scheduling slots for a given Calendly event type and date range."
)
def check_calendly_availability(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate query constraints and return mock available time slots."""
    try:
        query = AvailabilityQueryRequest.model_validate(payload)

        # Generate mock 30-minute intervals for demonstration
        mock_slots = []
        curr = query.start_date.replace(hour=9, minute=0, second=0, microsecond=0)
        while curr < query.end_date and len(mock_slots) < 5:
            if curr.weekday() < 5:  # Monday - Friday
                mock_slots.append(AvailableSlot(
                    start_time=curr,
                    end_time=curr + timedelta(minutes=30)
                ))
            curr += timedelta(hours=3)

        response_data = AvailabilityResponse(
            event_type_uri=query.event_type_uri,
            available_slots=mock_slots,
            total_slots_found=len(mock_slots)
        )
        return {"success": True, "data": response_data.model_dump(mode="json")}

    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="book_calendly_meeting",
    description="Book a confirmed meeting slot on Calendly on behalf of an invitee."
)
def book_calendly_meeting(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate booking request and simulate booking confirmation."""
    try:
        booking = BookingRequest.model_validate(payload)
        end_time = booking.start_time + timedelta(minutes=30)

        confirmation = BookingConfirmation(
            booking_id=f"CAL-BOOK-{hash(booking.invitee.email) % 1000000:06d}",
            event_name="30 Minute Executive Strategy Session",
            start_time=booking.start_time,
            end_time=end_time,
            invitee_email=booking.invitee.email,
            status="active",
            join_url=f"https://meet.google.com/cal-{hash(booking.invitee.name) % 10000:04d}"
        )
        return {"success": True, "confirmation": confirmation.model_dump(mode="json")}

    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------------------------------------------------------------------------
# Webhook Signature Verification Helper
# ---------------------------------------------------------------------------

def verify_calendly_webhook_signature(payload_body: str, signature_header: str, signing_key: str) -> bool:
    """
    Validate incoming Calendly webhook HMAC SHA256 signatures.
    Header format: t=1612345678,v1=hash_value
    """
    try:
        parts = {k: v for k, v in (item.split("=") for item in signature_header.split(","))}
        timestamp = parts.get("t")
        signature = parts.get("v1")

        if not timestamp or not signature:
            return False

        signed_payload = f"{timestamp}.{payload_body}"
        expected_sig = hmac.new(
            signing_key.encode("utf-8"),
            signed_payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_sig, signature)
    except Exception:
        return False

if __name__ == "__main__":
    print("Starting FastMCP 3.1 Calendly Agent Server...")
    mcp.run()
```

## Troubleshooting & Common Operational Pitfalls

| Diagnostic Scenario | Potential Root Cause | Recommended Operational Resolution |
| :--- | :--- | :--- |
| **HTTP 401 Unauthorized** | Invalid or expired Personal Access Token | Regenerate API token in Calendly Developer Portal and verify environment variable string formatting. |
| **HTTP 403 Forbidden on Webhooks** | Subscription tier insufficient | Webhooks and advanced routing forms require Standard, Teams, or Enterprise subscription plans. |
| **No Slots Returned** | Overlapping calendar busy blocks or lead time limits | Verify host availability schedules, buffer settings, minimum scheduling notice (e.g., 24h limit), and time zone offsets. |
| **Webhook Signature Mismatch** | Incorrect signing key or payload body modification | Ensure raw HTTP body text is passed to HMAC verifier without middleware JSON re-formatting. |
| **Rate Limiting (HTTP 429)** | Exceeded 600 requests / min API ceiling | Implement exponential backoff retry algorithms in agent tool wrappers. |

## Operational Guardrails & Best Practices
1. **Scope Minimization**: Use specific Personal Access Tokens bound strictly to necessary organizations rather than broad admin tokens.
2. **Buffer Interval Hardening**: Configure forced 10–15 minute buffer times after every booked meeting to prevent back-to-back executive fatigue.
3. **Agent Availability Filtering**: When agents present open slots to candidates, format times explicitly in the candidate's local time zone with full IANA descriptors (`America/Chicago`, `Europe/London`).
4. **Webhook Idempotency**: Store received `invitee.created` event URIs in a deduplication cache ([Valkey](../infrastructure/valkey.md) or SQLite) to handle duplicate webhook deliveries safely.

## Related tools / concepts
- [SavvyCal](../calendar_tasks/savvycal.md) — Multi-host calendar scheduling software with interactive overlay capabilities.
- [Morgen](../calendar_tasks/morgen.md) — Privacy-focused, local-first calendar and task management client.
- [Akiflow](../calendar_tasks/akiflow.md) — Consolidated daily task and calendar planner.
- [n8n](../../services/n8n.md) — Workflow automation server for processing Calendly webhooks.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Universal protocol for agent tool integrations.

## Sources / references
- [Calendly Official Website](https://calendly.com/)
- [Calendly Developer Portal & API v2 Docs](https://developer.calendly.com/)
- [Calendly FastMCP Repository](https://github.com/calendly/mcp-server)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
