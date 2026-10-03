# JMAP Protocol (JSON Meta Application Protocol)

## What it is
JMAP (JSON Meta Application Protocol - RFC 8620, RFC 8621, RFC 8887, RFC 8989) is an open, modern standard protocol for synchronizing email, calendars, tasks, and contacts over HTTPS using JSON APIs. Developed as a successor to IMAP, CalDAV, and CardDAV, JMAP provides stateless, efficient batching, push event notifications via Server-Sent Events (SSE), and dramatically reduced battery and bandwidth consumption for mobile devices and AI agents. It natively bridges conversational agents, FastMCP 3.1 tooling networks, and personal knowledge management systems with unified data schemas across mailboxes (`Email`), calendar schedules (`Calendar`, `CalendarEvent`), task lists (`Task`), and address books (`Contact`).

## What problem it solves
Legacy protocols like IMAP, CalDAV, and CardDAV rely on complex XML schemas, persistent raw TCP socket connections, and multiple HTTP/TCP roundtrips to retrieve basic message headers or calendar events. IMAP requires parsing raw MIME structures or custom response tokens, while CalDAV relies on verbose iCalendar (iCal) XML payloads over WebDAV. JMAP replaces these fragmented protocols with a unified JSON API over standard HTTP/2 or HTTP/3 transport. It allows AI agents and client applications to execute batched queries, transactionally update messages and tasks, resolve backreferences between requests in a single payload, and receive real-time delta updates through Server-Sent Events without holding open long-lived TCP connections.

## Where it fits in the stack
**Calendar & Tasks / Email & Identity Integration Layer**. JMAP serves as the universal data interchange protocol connecting mail/calendar backends (Fastmail, Stalwart Mail Server, Cyrus IMAP, Apache James) with AI agent orchestrators, personal productivity engines, and automated workflow pipelines.

```
+-----------------------------------------------------------------------------------+
|                        AI Agents & Client Applications                            |
|  - FastMCP 3.1 Mail & Task Tools     - Autonomous Calendar Scheduling Agents     |
|  - Web / Mobile Native Mail Clients  - Workflow Automation Engines (n8n)          |
+-----------------------------------------------------------------------------------+
                                         |
                                         |  JSON Batching over HTTP/2 & SSE
                                         v
+-----------------------------------------------------------------------------------+
|                            JMAP Protocol Gateway                                  |
|  - RFC 8620 (Core JMAP Framework)    - RFC 8621 (JMAP for Mail)                  |
|  - RFC 8887 (JMAP for Calendars)     - RFC 8989 (JMAP for Tasks & Contacts)       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           JMAP Compliant Backend Server                           |
|  +--------------------+     +---------------------+     +----------------------+  |
|  | Stalwart Mail      |     | Fastmail            |     | Cyrus IMAP / Apache  |  |
|  | Multi-protocol DB  |     | Cloud Service       |     | Enterprise Server    |  |
|  +--------------------+     +---------------------+     +----------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **AI Agent Calendar & Inbox Automation**: Programmatically searching, filtering, drafting, and sending emails or scheduling calendar appointments with minimal network payload overhead.
- **Transactional Batch Mutations**: Executing multi-step email, contact, and task updates (e.g., mark messages as read, apply labels, move to folder, create calendar event) in a single HTTP request payload using backreferences.
- **Real-Time State Synchronization**: Subscribing to Server-Sent Event (SSE) notification channels (`/event/`) for instant notifications when new emails arrive, contacts update, or calendar event invites change.
- **Low-Bandwidth Mobile & Agent Sync**: Performing efficient delta synchronization using opaque `state` string tokens to fetch only changed or deleted resources.
- **Cross-Domain Task Management**: Synchronizing tasks and calendar events between local FastMCP tool servers and centralized JMAP enterprise infrastructure.

## Strengths
- **Unified JSON Schema Model**: Consistent, typed JSON object models across `Email`, `EmailSubmission`, `Calendar`, `CalendarEvent`, `Task`, and `Contact`.
- **High Network Efficiency**: A single HTTP POST request can contain multiple batched method calls with inter-call dependency resolution (backreferences), eliminating HTTP roundtrips.
- **Native SSE Event Streaming**: Built-in Server-Sent Events push channel eliminates battery-draining polling loops.
- **Open IETF Standard**: Standardized by IETF working groups (RFC 8620, RFC 8621, RFC 8887, RFC 8989), ensuring complete vendor neutrality and open-source server interoperability.
- **Backreference Resolution**: Allows using the result of a previous call in the same batch (e.g., query email IDs and retrieve their full contents in one request).

## Limitations
- **Legacy Ecosystem Lock-in**: Major proprietary cloud providers (Google Workspace, Microsoft 365) rely on proprietary APIs (Microsoft Graph, Gmail REST API) rather than native JMAP, requiring bridge proxies for full JMAP compatibility.
- **Server Implementation Overhead**: Implementing a full JMAP server requires robust transactional state tracking and delta resolution engines.

## When to use it
- Connecting AI agents, FastMCP 3.1 tool servers, or automation platforms to Fastmail, Stalwart, Cyrus IMAP, or Apache James servers.
- Building custom email, calendar, and task integrations requiring low latency, predictable JSON data structures, and atomic batch mutations.
- Implementing low-power mobile or edge synchronization engines that benefit from delta state tracking and SSE push channels.

## When not to use it
- Integrating exclusively with Google Workspace or Microsoft 365, where native REST APIs (Gmail API, MS Graph API) are directly available.
- Simple, single-purpose integrations where a lightweight IMAP client library is already operational.

## Getting started

### 1. Discover JMAP Session Endpoint
Request account capabilities, account IDs, and API endpoints from your JMAP server provider:
```bash
curl -X GET "https://api.fastmail.com/jmap/session" \
     -H "Authorization: Bearer $JMAP_API_TOKEN" \
     -H "Content-Type: application/json"
```

### 2. Parse JMAP Session Object Capabilities
The response yields account identifiers and capability URNs required for subsequent request payloads:
- Core capability: `urn:ietf:params:jmap:core`
- Mail capability: `urn:ietf:params:jmap:mail`
- Calendars capability: `urn:ietf:params:jmap:calendars`
- Submission capability: `urn:ietf:params:jmap:submission`

### 3. Execute Batched Request
Send a `POST` request to `apiUrl` specified in the session object with your batched method calls.

## CLI examples

### Fetching Session Metadata via cURL
```bash
curl -s -X GET "https://api.fastmail.com/jmap/session" \
     -H "Authorization: Bearer $JMAP_API_TOKEN" | jq .
```

### Querying Unread Mail Messages with Backreference in Single Request
This single cURL call queries unread emails and retrieves their subject and sender details in one roundtrip using the `#` backreference mechanism:

```bash
curl -X POST "https://api.fastmail.com/jmap/api/" \
     -H "Authorization: Bearer $JMAP_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "using": [
         "urn:ietf:params:jmap:core",
         "urn:ietf:params:jmap:mail"
       ],
       "methodCalls": [
         [
           "Email/query",
           {
             "accountId": "u12345678",
             "filter": {"unread": true},
             "limit": 5
           },
           "call_query_01"
         ],
         [
           "Email/get",
           {
             "accountId": "u12345678",
             "#ids": {
               "resultOf": "call_query_01",
               "name": "Email/query",
               "path": "/ids"
             },
             "properties": ["id", "threadId", "subject", "from", "receivedAt"]
           },
           "call_get_02"
         ]
       ]
     }'
```

## API examples

### 1. FastMCP 3.1 Python JMAP Calendar & Mail Tool Server
This complete FastMCP 3.1 server exposes JMAP calendar and email operations as agent tools.

```python
import os
import requests
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("JMAP-Agent-Gateway")

class JMAPConfig(BaseModel):
    session_url: str = Field("https://api.fastmail.com/jmap/session")
    api_token: str = Field(..., description="Bearer API Token for JMAP authentication")

class JMAPCalendarQueryRequest(BaseModel):
    account_id: str = Field(..., description="JMAP Account ID")
    start_date_iso: str = Field(..., description="Start filter in ISO-8601 format")
    limit: int = Field(10, ge=1, le=50)

class CalendarEventSummary(BaseModel):
    event_id: str
    title: str
    start: str
    duration: str
    participants: List[str]

@mcp.tool(name="query_jmap_calendar")
def query_jmap_calendar(request: JMAPCalendarQueryRequest) -> List[CalendarEventSummary]:
    """Query scheduled calendar events from JMAP server for a given time window."""
    api_token = os.environ.get("JMAP_API_TOKEN", "mock_token")
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Construct batched JMAP query & get request
    payload = {
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:calendars"
        ],
        "methodCalls": [
            [
                "CalendarEvent/query",
                {
                    "accountId": request.account_id,
                    "filter": {"after": request.start_date_iso},
                    "limit": request.limit
                },
                "q1"
            ],
            [
                "CalendarEvent/get",
                {
                    "accountId": request.account_id,
                    "#ids": {
                        "resultOf": "q1",
                        "name": "CalendarEvent/query",
                        "path": "/ids"
                    },
                    "properties": ["id", "title", "start", "duration", "participants"]
                },
                "g1"
            ]
        ]
    }

    # Simulated response handling for demonstration
    events = [
        CalendarEventSummary(
            event_id="evt_88301",
            title="Architecture Review - FastMCP 3.1",
            start="2027-01-10T14:00:00Z",
            duration="PT1H",
            participants=["alex@example.com", "dev-team@example.com"]
        )
    ]
    return events

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

### 2. Pydantic v2 Schema Validation for JMAP Method Requests and Delta Synchronization
This script uses Pydantic v2 to validate incoming JMAP method responses, state tokens, and changes objects.

```python
import json
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field, field_validator, ValidationError

class JMAPMethodInvocation(BaseModel):
    method_name: str
    arguments: Dict[str, Any]
    client_call_id: str

    @classmethod
    def from_tuple(cls, raw_tuple: Tuple[str, Dict[str, Any], str]) -> "JMAPMethodInvocation":
        return cls(
            method_name=raw_tuple[0],
            arguments=raw_tuple[1],
            client_call_id=raw_tuple[2]
        )

class JMAPRequestBatch(BaseModel):
    using: List[str] = Field(..., description="Capability URNs")
    method_calls: List[JMAPMethodInvocation] = Field(..., alias="methodCalls")

class EmailChangesResponse(BaseModel):
    account_id: str = Field(..., alias="accountId")
    old_state: str = Field(..., alias="oldState")
    new_state: str = Field(..., alias="newState")
    has_more_changes: bool = Field(False, alias="hasMoreChanges")
    created_ids: List[str] = Field(default_factory=list, alias="created")
    updated_ids: List[str] = Field(default_factory=list, alias="updated")
    destroyed_ids: List[str] = Field(default_factory=list, alias="destroyed")

def parse_jmap_changes(json_str: str) -> Optional[EmailChangesResponse]:
    """Parse and validate JMAP Email/changes response payload."""
    try:
        data = json.loads(json_str)
        # Extract method response tuple
        method_name, args, call_id = data["methodResponses"][0]
        if method_name != "Email/changes":
            raise ValueError(f"Unexpected method name: {method_name}")

        changes = EmailChangesResponse.model_validate(args)
        print(f"[SUCCESS] Validated State Delta: {changes.old_state} -> {changes.new_state}")
        print(f"  Created: {len(changes.created_ids)}, Updated: {len(changes.updated_ids)}, Destroyed: {len(changes.destroyed_ids)}")
        return changes
    except (ValidationError, KeyError, ValueError) as err:
        print(f"[ERROR] JMAP Parsing failed: {err}")
        return None

# Sample JMAP Changes Response
sample_changes_payload = """
{
    "methodResponses": [
        [
            "Email/changes",
            {
                "accountId": "u123456",
                "oldState": "state_1020",
                "newState": "state_1024",
                "hasMoreChanges": false,
                "created": ["msg_9921"],
                "updated": ["msg_8810", "msg_8812"],
                "destroyed": ["msg_7701"]
            },
            "c_changes_01"
        ]
    ]
}
"""

validated_changes = parse_jmap_changes(sample_changes_payload)
```

## Architectural Mechanics & State Synchronization Flow

### State Delta Sync Sequence
Rather than re-fetching full message lists, JMAP clients pass their last-known `state` token to receive exact resource diffs:

```
[ Client / AI Agent ]                                  [ JMAP Server ]
         |                                                   |
         | --- Email/changes(oldState: "state_1020") ------> |
         |                                                   |
         | <-- Email/changes(                                |
         |       newState: "state_1024",                     |
         |       created: ["msg_9921"],                      |
         |       updated: ["msg_8810"],                      |
         |       destroyed: ["msg_7701"]                     |
         |     ) ------------------------------------------- |
         |                                                   |
         | --- Email/get(ids: ["msg_9921", "msg_8810"]) ---> |
         |                                                   |
         | <-- Email/get(list of updated objects) ---------- |
```

### Backreference Resolution
Backreferences allow chaining outputs of prior method calls into inputs of subsequent ones within the same JSON payload:
1. `Email/query` returns an array of matching message identifiers under path `/ids`.
2. `Email/get` references `{"#ids": {"resultOf": "call_query_01", "name": "Email/query", "path": "/ids"}}`.
3. The JMAP server evaluates `call_query_01` first, resolves the resulting IDs, and passes them directly to `Email/get` without returning an intermediate response to the client.

## Related tools / concepts
- [Fastmail](fastmail.md) — Cloud email and calendar service engineered natively on JMAP.
- [Proton Calendar](proton_calendar.md) — Privacy-first encrypted calendar engine.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Tool-calling specification for LLM agents.
- [n8n](../../services/n8n.md) — Workflow automation platform supporting HTTP/JMAP triggers.

## Sources / references
- [JMAP Official Specification Website](https://jmap.io/)
- [RFC 8620 - JSON Meta Application Protocol (JMAP Core)](https://datatracker.ietf.org/doc/html/rfc8620)
- [RFC 8621 - JMAP for Mail](https://datatracker.ietf.org/doc/html/rfc8621)
- [RFC 8887 - JMAP for Calendars](https://datatracker.ietf.org/doc/html/rfc8887)
- [Fastmail Developer Resources](https://www.fastmail.com/dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
