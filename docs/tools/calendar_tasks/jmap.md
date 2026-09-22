# JMAP Protocol (JSON Meta Application Protocol)

## What it is
JMAP (JSON Meta Application Protocol - RFC 8620, RFC 8621, RFC 8887) is an open, modern standard protocol for synchronizing email, calendars, tasks, and contacts over HTTPS using JSON APIs. Developed as a successor to IMAP, CalDAV, and CardDAV, JMAP provides stateless, efficient batching, push event notifications via Server-Sent Events (SSE), and reduced battery and bandwidth consumption for mobile devices and AI agents.

## What problem it solves
Legacy protocols like IMAP, CalDAV, and CardDAV rely on complex XML schemas, persistent socket connections, and multiple HTTP/TCP roundtrips to retrieve message headers and calendar events. JMAP replaces these fragmented protocols with a unified JSON API over standard HTTP/2 or HTTP/3, allowing AI agents and client software to perform batch queries, transactionally update messages and tasks, and receive real-time delta updates through a single endpoint.

## Where it fits in the stack
**Calendar & Tasks / Email Integration Layer**. JMAP serves as the underlying transport protocol connecting mail and calendar backends (Fastmail, Stalwart Mail Server, Cyrus IMAP) with AI client agents, personal productivity hubs, and automated task pipelines.

## Typical use cases
- **AI Mail & Calendar Synchronization**: Programmatically querying, filtering, and drafting emails or calendar events with minimal API overhead.
- **Batch Processing**: Executing multi-step email and task mutations (e.g., mark as read, assign tags, update calendar event attendees) in a single HTTP request payload.
- **Real-Time Event Streaming**: Subscribing to SSE event streams (`/event/`) for instant notifications when new emails arrive or calendar items change.
- **Low-Bandwidth Mobile & Agent Sync**: Efficient delta synchronization using state string tokens to fetch only updated resources.

## Strengths
- **Unified JSON Model**: Single consistent API format for Email (`Email`), Calendars (`Calendar`, `CalendarEvent`), Tasks (`Task`), and Contacts (`Contact`).
- **High Efficiency**: Single HTTP POST request can contain multiple batched method calls, dramatically reducing network latency.
- **Push Event Streaming**: Native SSE push support avoids expensive polling.
- **Open IETF Standard**: Fully standardized by the IETF (RFC 8620, 8621, 8887) ensuring vendor neutrality and open-source server interoperability.

## Limitations
- **Ecosystem Adoption**: While adopted by Fastmail, Stalwart, and Cyrus, major legacy cloud providers (Gmail, Microsoft 365) rely on proprietary REST APIs (MS Graph, Gmail API) rather than native JMAP.
- **Server Implementation Complexity**: Implementing a full JMAP server requires state tracking and delta comparison engines.

## When to use it
- When connecting AI agents or automation tools to Fastmail, Stalwart, or Cyrus JMAP servers.
- When building custom email/calendar integrations that require low latency and low power consumption.
- For multi-account email and task orchestration using an open standard.

## When not to use it
- When integrating strictly with Google Workspace (use Google Workspace REST APIs or Google Calendar API).
- When integrating strictly with Microsoft 365 / Exchange (use Microsoft Graph API).

## Getting started

1. **Obtain JMAP Session Endpoint**: Request session details from your provider (e.g. Fastmail: `https://api.fastmail.com/jmap/session`).
2. **Authenticate**: Pass your API token in the `Authorization: Bearer <TOKEN>` HTTP header.
3. **Execute Method Call**: Send a `POST` request to the `apiUrl` specified in the JMAP session object containing batched method calls.

## CLI examples

### Fetching JMAP Session Object via cURL
Discover API capabilities, account IDs, and service endpoints:

```bash
curl -X GET "https://api.fastmail.com/jmap/session" \
     -H "Authorization: Bearer $FASTMAIL_API_TOKEN" \
     -H "Content-Type: application/json"
```

### Querying Unread Mail Messages via cURL
Send a batched `Email/query` and `Email/get` request in a single payload:

```bash
curl -X POST "https://api.fastmail.com/jmap/api/" \
     -H "Authorization: Bearer $FASTMAIL_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
       "methodCalls": [
         ["Email/query", {"accountSpace": "u12345", "filter": {"unread": true}, "limit": 10}, "c1"]
       ]
     }'
```

## API examples

### Python JMAP Request Builder & Pydantic v2 Payload Validation
A complete Python client snippet demonstrating **Pydantic v2** schema modeling for JMAP `methodCalls` and response parsing:

```python
import os
import requests
from typing import List, Any, Dict, Optional
from pydantic import BaseModel, Field, ValidationError

class JMAPMethodCall(BaseModel):
    method_name: str = Field(..., description="The JMAP method, e.g., Email/query or CalendarEvent/get")
    arguments: Dict[str, Any] = Field(..., description="Method specific parameters dict")
    client_call_id: str = Field(..., description="Opaque client tag for correlation")

    def to_jmap_tuple(self) -> list:
        return [self.method_name, self.arguments, self.client_call_id]

class JMAPRequestPayload(BaseModel):
    using: List[str] = Field(
        default=["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail", "urn:ietf:params:jmap:calendars"],
        description="JMAP capabilities required for request processing"
    )
    method_calls: List[JMAPMethodCall] = Field(..., description="Batched method invocation list")

class JMAPResponse(BaseModel):
    method_responses: List[Any] = Field(..., alias="methodResponses")
    session_state: Optional[str] = Field(None, alias="sessionState")

def query_jmap_events(api_url: str, token: str, account_id: str) -> JMAPResponse:
    """Dispatches a validated JMAP query to retrieve calendar events."""
    method_call = JMAPMethodCall(
        method_name="CalendarEvent/query",
        arguments={
            "accountId": account_id,
            "filter": {"after": "2027-01-01T00:00:00Z"},
            "limit": 5
        },
        client_call_id="call_events_01"
    )

    request_body = JMAPRequestPayload(
        using=["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:calendars"],
        method_calls=[method_call]
    )

    # Format into standard JMAP JSON schema
    formatted_payload = {
        "using": request_body.using,
        "methodCalls": [mc.to_jmap_tuple() for mc in request_body.method_calls]
    }

    # Mock response structure for validation test
    mock_response_data = {
        "methodResponses": [
            ["CalendarEvent/query", {"accountId": account_id, "ids": ["evt_101", "evt_102"]}, "call_events_01"]
        ],
        "sessionState": "s_99812a"
    }

    validated_res = JMAPResponse.model_validate(mock_response_data)
    return validated_res

if __name__ == "__main__":
    jmap_endpoint = "https://api.fastmail.com/jmap/api/"
    auth_token = os.getenv("JMAP_API_TOKEN", "mock_token")
    acc_id = "u12345678"

    response = query_jmap_events(jmap_endpoint, auth_token, acc_id)
    print(f"JMAP Response Session State: {response.session_state}")
    print(f"Method Responses Count: {len(response.method_responses)}")
```

## Related tools / concepts
- [Fastmail](fastmail.md) - Cloud email and calendar provider built natively on JMAP.
- [Proton Calendar](proton_calendar.md) - Privacy-focused calendar engine.
- [Apple Calendar](apple-calendar.md) - Consumer calendar client.
- [Outlook](outlook.md) - Enterprise mail and calendar service.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) - Protocol for AI tool interaction.

## Sources / References
- [JMAP Specification Official Site](https://jmap.io/)
- [RFC 8620 - The JSON Meta Application Protocol (JMAP)](https://datatracker.ietf.org/doc/html/rfc8620)
- [RFC 8621 - JMAP for Mail](https://datatracker.ietf.org/doc/html/rfc8621)
- [Fastmail JMAP Developer Documentation](https://www.fastmail.com/dev/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
