# JMAP Protocol (JSON Meta Application Protocol)

## What it is
JMAP (JSON Meta Application Protocol - standardized under **RFC 8620**, **RFC 8621**, **RFC 8887**, and **RFC 9007**) is an open, modern internet protocol designed for synchronizing email, calendars, tasks, contacts, and user state over HTTPS using structured JSON APIs. Developed as a successor to legacy internet protocols like IMAP, CalDAV, and CardDAV, JMAP delivers stateless operation, batching, push event notifications via Server-Sent Events (SSE), and reduced battery and bandwidth consumption for mobile applications and autonomous AI agents. As of early 2027, JMAP is heavily integrated into modern AI agent task engines and productivity providers (Fastmail, Stalwart Mail Server, Cyrus IMAP), providing a standardized transport protocol for **FastMCP 3.1** calendar, mail, and task orchestration workflows.

## What problem it solves
Legacy protocols like IMAP, CalDAV, and CardDAV rely on complex XML schemas (iCalendar/iTIP, vCard), persistent TCP socket connections (e.g. IMAP IDLE), and multi-step HTTP/TCP roundtrips to retrieve message headers, free/busy status, or calendar entries. These legacy mechanisms create high latency, drain mobile battery power, and require complex custom XML parsing libraries in agent runtimes. JMAP replaces these fragmented protocols with a unified JSON-over-HTTP/2-or-HTTP/3 API. This enables AI agents and productivity client software to execute batched, transactional mutations, query mailbox and event deltas via concise state strings, and receive real-time push events through a single unified endpoint.

## Where it fits in the stack
**Calendar, Tasks & Email / Open Protocol Integration Layer**. JMAP sits as the underlying communication protocol connecting backend mail/calendar servers (Fastmail, Stalwart, Cyrus IMAP) with AI agent orchestrators, personal productivity dashboards, and automated email/task pipelines.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AI Agent / Client Application                         │
│               (FastMCP 3.1 Server / Autonomous Sync Engine)                │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Single HTTP/2 POST (JSON Batched Requests)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                            JMAP Core Transport                              │
│                (Session Object Discovery & State String Sync)               │
└──────────────┬──────────────────────────────────────────────┬───────────────┘
               │                                              │
               │ Synchronous Batch Methods                    │ Push Event Stream (SSE)
┌──────────────▼──────────────┐                ┌──────────────▼───────────────┐
│ JMAP Mail / Calendar Data   │                │   JMAP Event Notification    │
│ (Email, Calendar, Task)     │                │   (/event/ SSE Channel)      │
└──────────────┬──────────────┘                └──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────────────────────┐
│                           JMAP Server Storage Engine                        │
│                   (Fastmail, Stalwart Mail Server, Cyrus)                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **AI Agent Calendar & Task Management**: Programmatically querying, filtering, drafting, and scheduling calendar events (`CalendarEvent`) or task items (`Task`) with minimal API overhead.
- **Batched Mail Processing**: Executing multi-step email mutations (e.g., query unread emails, apply tags, move to archive, and generate draft response) inside a single batched HTTP POST request.
- **Real-Time Event Streaming via SSE**: Subscribing to JMAP Server-Sent Event channels (`/event/`) to instantly trigger agent actions upon receiving new email messages or meeting invitations.
- **Low-Bandwidth Mobile & Edge Sync**: Performing incremental delta synchronization using state strings (e.g., `state: "s_99281a"`), ensuring agents fetch only updated or deleted records.

## Strengths
- **Unified JSON Data Model**: Consistent JSON API format across Email (`Email`), Mailbox (`Mailbox`), Calendars (`Calendar`, `CalendarEvent`), Tasks (`Task`), and Contacts (`Contact`).
- **High Network Efficiency**: Single HTTP POST request can contain multiple batched method calls with inter-method variable referencing (client call IDs), eliminating network roundtrips.
- **Native SSE Push Stream**: Server-Sent Events notification mechanism avoids polling and maintains low latency.
- **IETF Open Standard**: Fully standardized by the IETF (RFC 8620, RFC 8621, RFC 8887, RFC 9007), guaranteeing vendor neutrality and open-source interoperability.
- **FastMCP 3.1 Ready**: Easily wrapped inside FastMCP 3.1 tool servers to provide agents with calendar and task control.

## Limitations
- **Legacy Cloud Provider Adoption**: While Fastmail, Stalwart, and Cyrus natively support JMAP, major legacy cloud ecosystems (Google Workspace, Microsoft 365) prioritize proprietary REST APIs (Gmail API, MS Graph API) over native JMAP.
- **Server Implementation Complexity**: Implementing a full JMAP server requires state string version tracking, delta comparison engines, and push streaming infrastructure.

## When to use it
- When connecting AI agents or automation scripts to Fastmail, Stalwart, or Cyrus JMAP server backends.
- When building multi-account email, calendar, and task orchestration pipelines requiring low latency and low power consumption.
- For open-source, sovereign homelab or enterprise mail/calendar setups.

## When not to use it
- When integrating strictly with Google Workspace (use Google Workspace REST APIs or Google Calendar API).
- When integrating strictly with Microsoft 365 / Exchange (use Microsoft Graph API).

## Getting started

To interact with a JMAP server:

1. **Discover JMAP Session**:
   Request session configuration from your JMAP server (e.g., `https://api.fastmail.com/jmap/session`).
   ```bash
   curl -X GET "https://api.fastmail.com/jmap/session" \
        -H "Authorization: Bearer $JMAP_API_TOKEN"
   ```

2. **Extract API Endpoint & Account ID**:
   Parse the returned JSON session object to locate `apiUrl`, `downloadUrl`, `uploadUrl`, `eventSourceUrl`, and the primary `accountId`.

3. **Send Batched Method Calls**:
   Submit POST requests to `apiUrl` containing required capabilities (`using`) and batched method invocation arrays (`methodCalls`).

## CLI examples

### Fetch JMAP Session Discovery Document
```bash
curl -X GET "https://api.fastmail.com/jmap/session" \
     -H "Authorization: Bearer $JMAP_API_TOKEN" \
     -H "Content-Type: application/json"
```

### Querying Calendar Events via cURL
Submit a batched JMAP request to retrieve upcoming calendar events after a given timestamp:

```bash
curl -X POST "https://api.fastmail.com/jmap/api/" \
     -H "Authorization: Bearer $JMAP_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "using": [
         "urn:ietf:params:jmap:core",
         "urn:ietf:params:jmap:calendars"
       ],
       "methodCalls": [
         [
           "CalendarEvent/query",
           {
             "accountId": "u12345678",
             "filter": {
               "after": "2027-01-01T00:00:00Z"
             },
             "limit": 10
           },
           "call_events_01"
         ]
       ]
     }'
```

## API examples

### Python: JMAP Request Builder & Pydantic v2 Payload Validation
Below is a Python snippet using **Pydantic v2** to model JMAP `methodCalls`, handle response parsing, and perform state string delta checks:

```python
import os
import json
import requests
from typing import List, Any, Dict, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

# 1. Pydantic v2 schemas for RFC 8620 JMAP Request & Response payloads
class JMAPMethodCall(BaseModel):
    method_name: str = Field(..., description="JMAP method name, e.g. Email/query or CalendarEvent/get")
    arguments: Dict[str, Any] = Field(..., description="Method specific parameters dictionary")
    client_call_id: str = Field(..., description="Opaque client tag for correlation")

    def to_jmap_tuple(self) -> list:
        return [self.method_name, self.arguments, self.client_call_id]

class JMAPRequestPayload(BaseModel):
    using: List[str] = Field(
        default=["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail", "urn:ietf:params:jmap:calendars"],
        description="JMAP capabilities required for processing"
    )
    method_calls: List[JMAPMethodCall] = Field(..., description="Batched method invocation list")

class JMAPMethodResponse(BaseModel):
    method_name: str
    arguments: Dict[str, Any]
    client_call_id: str

class JMAPResponsePayload(BaseModel):
    method_responses: List[Any] = Field(..., alias="methodResponses")
    session_state: Optional[str] = Field(None, alias="sessionState")

# 2. Function executing validated JMAP query
def query_jmap_calendar_events(api_url: str, token: str, account_id: str) -> JMAPResponsePayload:
    method = JMAPMethodCall(
        method_name="CalendarEvent/query",
        arguments={
            "accountId": account_id,
            "filter": {"after": "2027-01-01T00:00:00Z"},
            "sort": [{"property": "start", "isAscending": True}],
            "limit": 5
        },
        client_call_id="c_events_101"
    )

    payload_model = JMAPRequestPayload(
        using=["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:calendars"],
        method_calls=[method]
    )

    formatted_json = {
        "using": payload_model.using,
        "methodCalls": [mc.to_jmap_tuple() for mc in payload_model.method_calls]
    }

    # Simulate network call response for validation test
    simulated_server_response = {
        "methodResponses": [
            [
                "CalendarEvent/query",
                {
                    "accountId": account_id,
                    "queryState": "qs_88412b",
                    "canCalculateChanges": True,
                    "ids": ["evt_301", "evt_302"]
                },
                "c_events_101"
            ]
        ],
        "sessionState": "state_jmap_9982"
    }

    validated_response = JMAPResponsePayload.model_validate(simulated_server_response)
    return validated_response

if __name__ == "__main__":
    endpoint = "https://api.fastmail.com/jmap/api/"
    api_token = os.getenv("JMAP_API_TOKEN", "mock_token")
    acc = "u8821940"

    res = query_jmap_calendar_events(endpoint, api_token, acc)
    print(f"Validated JMAP Session State: {res.session_state}")
    print(f"Method Responses Count: {len(res.method_responses)}")
```

### FastMCP 3.1 Server Integration for JMAP Calendar & Task Management
Exposing JMAP task and calendar scheduling capabilities to AI agents as a FastMCP 3.1 server:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import requests

mcp = FastMCP(
    name="JMAP-Calendar-Task-Server",
    version="3.1.0"
)

class CreateTaskParams(BaseModel):
    title: str = Field(..., description="Task title or summary")
    due_date: str = Field(..., description="ISO-8601 due date timestamp, e.g. 2027-01-15T18:00:00Z")
    priority: int = Field(default=3, ge=1, le=5, description="Priority level 1 (high) to 5 (low)")

@mcp.tool(name="jmap_create_task", description="Creates a new task item on a JMAP server using RFC 8887 Task protocol")
def jmap_create_task(params: CreateTaskParams) -> dict:
    # Construct JMAP Task/set payload
    jmap_body = {
        "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:tasks"],
        "methodCalls": [
            [
                "Task/set",
                {
                    "accountId": "u12345678",
                    "create": {
                        "k1": {
                            "title": params.title,
                            "due": params.due_date,
                            "priority": params.priority
                        }
                    }
                },
                "call_create_task"
            ]
        ]
    }

    # In real deployment, dispatch HTTP POST to JMAP apiUrl
    return {
        "status": "success",
        "created_task_id": "task_jmap_9942",
        "title": params.title,
        "due": params.due_date,
        "mcp_version": "3.1.0"
    }

if __name__ == "__main__":
    mcp.run(transport="sse", port=8001)
```

## Comparative Matrix: JMAP vs Legacy Mail & Calendar Synchronization Protocols

| Capability / Feature | JMAP Protocol (RFC 8620/8621) | IMAP + CalDAV + CardDAV | Microsoft Graph API | Google Workspace API |
| :--- | :--- | :--- | :--- | :--- |
| **Data Format** | Native Clean JSON | XML (CalDAV) + Raw MIME / Custom | JSON REST | JSON REST |
| **Request Batching** | Native Batched Method Calls | Separate HTTP / TCP Conns | Batch Endpoint ($batch) | Batch Requests Endpoint |
| **Network Latency** | Ultra-Low (Single Roundtrip) | High (Multiple Roundtrips) | Moderate | Moderate |
| **Push Event Stream** | Standardized SSE Channel (`/event/`) | IMAP IDLE / Custom Webhooks | MS Graph Webhooks | Google Cloud Pub/Sub |
| **Inter-Method Referencing**| Native Client Call IDs | Not Available | Dependent Operations | Not Available |
| **Standardization Body** | IETF Standard (RFC) | IETF Standard (RFC) | Proprietary Microsoft | Proprietary Google |
| **Mobile Battery Overhead**| Minimal (Stateless JSON over HTTP/2) | High (Keep-Alive TCP Sockets) | Moderate | Moderate |

## Production Deployment & Optimization Checklist

1. **JMAP Session Caching**:
   - Cache the JMAP session document locally in agent runtimes and refresh only when receiving HTTP `401 Unauthorized` or `sessionState` invalidation headers.

2. **Delta Sync via State Tokens**:
   - Store `queryState` and `state` strings following every `Email/query` or `CalendarEvent/query` call. Use `/changes` methods (e.g. `CalendarEvent/changes`) to retrieve delta changes instead of fetching entire collections.

3. **Batch Request Sizing**:
   - Limit batched method invocations inside a single POST payload to a maximum of 20-30 operations to prevent server request timeout or memory spike.

4. **SSE Event Stream Reconnection**:
   - Implement exponential backoff when reconnecting to the JMAP SSE endpoint (`eventSourceUrl`) during temporary network drops.

## Step-by-Step Troubleshooting Guide

### Issue 1: "JMAP Server returns 400 Bad Request with unknown capability error"
- **Root Cause**: The client included an unsupported capability URI inside the `"using"` array of the request payload.
- **Resolution**:
  1. Fetch the session document (`GET /jmap/session`) and inspect the `capabilities` dictionary.
  2. Ensure your request `"using"` array only includes capabilities explicitly advertised by the server (e.g., `urn:ietf:params:jmap:core`, `urn:ietf:params:jmap:mail`, `urn:ietf:params:jmap:calendars`).

### Issue 2: "Inter-method variable reference failure (invalid client call ID)"
- **Root Cause**: A method invocation tried to reference a result tag from a preceding method using invalid syntax or out-of-order execution tag.
- **Resolution**:
  1. Ensure referenced method call ID (e.g. `"c1"`) matches the exact string tag defined in the preceding method call tuple.
  2. Check path reference format: `"#accountId": "c1/accountId"`.

### Issue 3: "SSE Push Stream disconnects repeatedly"
- **Root Cause**: HTTP/2 connection timeout or reverse proxy buffering on the server endpoint.
- **Resolution**:
  1. Pass the `ping` parameter in event subscription query strings if supported by your JMAP server.
  2. Verify reverse proxies maintain keep-alive time of at least 300 seconds for `/event/` paths.

## Related tools / concepts
- [Fastmail](fastmail.md) — Flagship cloud provider natively built on JMAP protocol architecture.
- [Proton Calendar](proton_calendar.md) — Privacy-focused calendar service.
- [Apple Calendar](apple-calendar.md) — Consumer calendar client using CalDAV/JMAP bridges.
- [Outlook](outlook.md) — Enterprise mail and calendar platform using MS Graph.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for AI tool and calendar orchestration.

## Sources / references
- [JMAP Specification Portal](https://jmap.io/)
- [RFC 8620 - The JSON Meta Application Protocol (JMAP)](https://datatracker.ietf.org/doc/html/rfc8620)
- [RFC 8621 - JMAP for Mail](https://datatracker.ietf.org/doc/html/rfc8621)
- [RFC 8887 - JMAP for Building Calendars](https://datatracker.ietf.org/doc/html/rfc8887)
- [Fastmail JMAP Developer Documentation](https://www.fastmail.com/dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
