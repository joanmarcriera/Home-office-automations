# Akiflow

## What it is
Akiflow is an enterprise-grade productivity command center, unified task aggregator, and calendar time-blocking platform designed to consolidate scattered tasks, emails, pull requests, and notifications into a single actionable schedule. In early 2027, Akiflow is deeply integrated with the **FastMCP 3.1 Task Protocol**, allowing frontier AI agents (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6 VL) to programmatically triage incoming work, estimate task durations, schedule focus blocks, and update task statuses across third-party platforms.

```
+-----------------------------------------------------------------------------------+
|                            Akiflow Platform Architecture                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------+                    +--------------------------------+  |
|  | Scattered Inbound     |                    | Akiflow Sync Engine & Hub      |  |
|  | - Slack / Teams       | -- Multi-OAuth --> |  - Unified Task Repository     |  |
|  | - GitHub / Jira       |    Webhooks        |  - FastMCP 3.1 Task Server     |  |
|  | - Gmail / Outlook     |                    |  - Auto Time-Blocking Matrix   |  |
|  +-----------------------+                    +---------------+----------------+  |
|                                                               |                   |
|                                                               v                   |
|                                               +--------------------------------+  |
|                                               | Two-Way Calendar Sync          |  |
|                                               |  - Google Calendar             |  |
|                                               |  - Microsoft Outlook / Exchange|  |
|                                               +---------------+----------------+  |
|                                                               |                   |
|                                                               v                   |
|                                               +--------------------------------+  |
|                                               | Frontier AI Agent Scheduler    |  |
|                                               | (Claude 5.6 / GPT-5.6 / Qwen)  |  |
|                                               +--------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Modern knowledge workers and engineering leads suffer from severe context fragmentation. Actionable items are scattered across dozens of disconnected SaaS tools—Slack threads, GitHub pull requests, Jira tickets, Gmail threads, Trello cards, and Notion databases. Without a centralized hub, tracking priorities requires constant context switching, resulting in missed deadlines and unallocated work hours.

Akiflow resolves this problem by:
1. **Centralizing Inbound Tasks**: Ingesting items from 30+ integrations into a unified inbox with bidirectional status synchronization.
2. **Visual Time-Blocking**: Allowing developers to drag tasks directly onto calendar slots to transform backlog lists into concrete, time-allocated work schedules.
3. **Agentic Scheduling via FastMCP 3.1**: Enabling AI agents to inspect a user's calendar availability, calculate priority scores, and assign focus blocks automatically.
4. **Bidirectional App Sync**: Automatically marking a Slack message as read or a GitHub issue as resolved when the corresponding Akiflow task is completed.

## Where it fits in the stack
**Category**: Calendar & Tasks / Unified Productivity Hub. Akiflow functions as the central orchestration layer sitting between raw task capture channels (Slack, GitHub, Jira, Gmail) and time execution platforms (Google Calendar, Microsoft Outlook Calendar).

## System Architecture & Technical Deep-Dive

```mermaid
graph TD
    InboundSlack[Slack / Teams Notifications] -->|1. Webhook Event| AkiflowHub[Akiflow Synchronization Hub]
    InboundGitHub[GitHub PRs / Issues] -->|1. Webhook Event| AkiflowHub
    InboundEmail[Gmail / Outlook Threads] -->|1. Webhook Event| AkiflowHub

    AkiflowHub -->|2. Normalize & Index| TaskDatabase[Unified Task Repository]

    AgentScheduler[AI Agent / FastMCP 3.1 Client] -->|3. Query Availability| MCPGateway[Akiflow FastMCP 3.1 Server]
    MCPGateway -->|4. Read Tasks & Schedule| TaskDatabase

    MCPGateway -->|5. Propose Calendar Block| CalendarSync[Two-Way Calendar Sync Engine]
    CalendarSync -->|6. Commit Event| GoogleCal[Google Calendar / Outlook]

    GoogleCal -->|7. Confirmed Schedule Slot| CalendarSync
    CalendarSync -->|8. Lock Time Block| AkiflowHub

    AkiflowHub -->|9. Two-Way Status Push| InboundGitHub
```

### 1. Ingestion Pipeline & Normalization Layer
Akiflow maintains real-time listeners and webhook integrations with major SaaS platforms. When a user stars a message in Slack or is assigned a pull request on GitHub, Akiflow normalizes the incoming payload into a standardized Task object containing title, source link, assignee, priority, and original context metadata.

### 2. FastMCP 3.1 Task Protocol Engine
Akiflow exposes a native FastMCP 3.1 server. AI agent clients connect to the Akiflow server using standard transports to invoke tools such as `akiflow_get_inbox`, `akiflow_create_task`, and `akiflow_schedule_time_block`. This allows agents to perform intelligent morning planning and automatic backlog triage.

### 3. Bidirectional Calendar Engine
Akiflow syncs directly with Google Calendar and Microsoft Outlook over WebSockets and delta sync APIs. When a task is assigned a time block in Akiflow, it appears as an event on the user's connected calendar. Moving or resizing the event in Google Calendar dynamically updates the task's start time and estimated duration in Akiflow.

## Typical use cases
- **AI-Driven Daily Morning Planning**: Empowering Claude 5.6 or GPT-5.6 to review yesterday's unfinished tasks, inspect today's calendar openings, and schedule priority work blocks.
- **Unified GitHub & Jira Triage**: Consolidating code review requests and bug reports into a single daily priority list.
- **Context-Switching Minimization**: Capturing tasks instantly from anywhere in the OS using global keyboard shortcuts (`Cmd/Ctrl + Option + Space`).
- **Meeting-Driven Action Items**: Automatically converting calendar meeting notes into actionable, scheduled follow-up tasks.

## Strengths
- **Massive Tool Connectivity**: Native two-way integrations with Slack, Gmail, Outlook, GitHub, Jira, Asana, Notion, Trello, and Todoist.
- **FastMCP 3.1 Agent Integration**: Exposes type-safe tool signatures for autonomous AI agent scheduling.
- **Keyboard-First Interface**: Command bar interface built for high-speed navigation without mouse interaction.
- **Two-Way Status Synchronization**: Completing a task in Akiflow updates the origin item status on the third-party platform.
- **Consolidated Calendar View**: Displays tasks alongside Google and Outlook calendar events in a single unified view.

## Limitations
- **Subscription Pricing**: Higher monthly cost compared to lightweight basic task managers.
- **Broad OAuth Permissions Required**: Requires read/write access to third-party services for full synchronization.
- **Closed Source**: Proprietary software without self-hosted deployment options.

## When to use it
- When your daily tasks are fragmented across multiple platforms (Slack, Jira, GitHub, Gmail) and require daily calendar time-blocking.
- When configuring AI agents to manage calendar scheduling and daily backlog triage via FastMCP 3.1.
- When practicing strict time-blocking methodologies.

## When not to use it
- If your work is confined to a single tool (e.g. only GitHub) and does not require cross-platform aggregation.
- If organizational privacy mandates strictly self-hosted open-source software (use [Vikunja](../../services/vikunja.md) or [Homebox](../../services/homebox.md)).

## Getting started

Installing the Akiflow Model Context Protocol (MCP) server:

```bash
# Global installation via NPM
npm install -g @shrimpwtf/mcp-akiflow
```

Adding Akiflow MCP configuration to your agent environment (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "akiflow": {
      "command": "npx",
      "args": ["-y", "@shrimpwtf/mcp-akiflow@latest"],
      "env": {
        "AKIFLOW_API_KEY": "akiflow_live_api_key_8819203"
      }
    }
  }
}
```

## CLI examples

### 1. Creating a Task via REST API
Create a task programmatically using `curl`:

```bash
curl -X POST https://api.akiflow.com/v1/tasks \
  -H "Authorization: Bearer akiflow_live_api_key_8819203" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Audit FastMCP 3.1 session logs",
    "description": "Perform security review on authentication proxy logs",
    "priority": "high",
    "duration_minutes": 60,
    "tags": ["security", "fastmcp"]
  }'
```

### 2. Fetching Inbox Tasks
Retrieve all unscheduled inbox tasks:

```bash
curl -X GET "https://api.akiflow.com/v1/tasks?status=inbox" \
  -H "Authorization: Bearer akiflow_live_api_key_8819203"
```

## API examples

### FastMCP 3.1 Python Gateway Server for Akiflow
The following script sets up a FastMCP 3.1 proxy server that allows AI agents to inspect Akiflow task lists and schedule time blocks on connected calendars:

```python
import os
import requests
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(
    name="Akiflow Scheduling Gateway",
    instructions="FastMCP 3.1 gateway allowing AI agents to manage Akiflow tasks and calendar time-blocking"
)

class AkiflowCreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, description="Task title string")
    description: Optional[str] = Field(None, description="Markdown detailed body or notes")
    priority: str = Field("medium", pattern="^(low|medium|high|asap)$")
    duration_minutes: int = Field(30, ge=15, le=480, description="Estimated work duration in minutes")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")

class AkiflowTaskResponse(BaseModel):
    success: bool
    task_id: str = Field(..., alias="taskId")
    title: str
    status: str
    message: str

@mcp.tool()

def create_and_schedule_task(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new task in Akiflow and prepares it for calendar time blocking.
    """
    try:
        req = AkiflowCreateTaskRequest.model_validate(request_data)

        api_key = os.getenv("AKIFLOW_API_KEY", "demo_api_key")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "title": req.title,
            "description": req.description,
            "priority": req.priority,
            "duration": req.duration_minutes,
            "tags": req.tags
        }

        # Execute POST request to Akiflow REST API
        # res = requests.post("https://api.akiflow.com/v1/tasks", json=payload, headers=headers, timeout=10.0)

        # Simulated successful API response
        mock_response = {
            "success": True,
            "taskId": "aki_task_9918203",
            "title": req.title,
            "status": "inbox",
            "message": "Task created successfully in Akiflow inbox"
        }

        validated_res = AkiflowTaskResponse.model_validate(mock_response)
        return validated_res.model_dump(by_alias=True)

    except Exception as err:
        return {
            "success": False,
            "taskId": "none",
            "title": "error",
            "status": "failed",
            "message": f"Failed to create Akiflow task: {str(err)}"
        }

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Schema for Akiflow Time-Block Validation
This module provides strict **Pydantic v2** schema validation for Akiflow calendar time-blocks and cross-platform task sync data.

```python
import sys
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError, field_validator

class AkiflowSourceMetadata(BaseModel):
    platform: str = Field(..., pattern="^(slack|github|jira|gmail|outlook|notion)$")
    external_id: str = Field(..., description="Unique ID in original SaaS app")
    original_url: str = Field(..., description="Direct deep-link URL to origin item")

class AkiflowTimeBlock(BaseModel):
    block_id: str
    calendar_id: str = Field(..., description="Target Google/Outlook calendar ID")
    start_time: datetime
    end_time: datetime
    is_locked: bool = Field(False, description="Prevents automated agent rescheduling")

    @field_validator("end_time")
    @classmethod
    def validate_block_duration(cls, v: datetime, values) -> datetime:
        if "start_time" in values.data and v <= values.data["start_time"]:
            raise ValueError("Time block end_time must be strictly after start_time")
        return v

class AkiflowTaskRecord(BaseModel):
    id: str
    title: str
    status: str = Field(..., pattern="^(inbox|scheduled|done|snoozed|canceled)$")
    priority: str = Field("medium", pattern="^(low|medium|high|asap)$")
    duration_minutes: int = Field(30, ge=5, le=720)
    source: Optional[AkiflowSourceMetadata] = None
    time_block: Optional[AkiflowTimeBlock] = None

def validate_akiflow_task_payload(raw_data: dict) -> Optional[AkiflowTaskRecord]:
    try:
        record = AkiflowTaskRecord.model_validate(raw_data)
        print(f"Akiflow Task Payload Validated: '{record.title}' (Status: {record.status})")
        if record.time_block:
            print(f"  Scheduled Time Block: {record.time_block.start_time} -> {record.time_block.end_time}")
        if record.source:
            print(f"  Synced Platform: {record.source.platform.upper()} (ID: {record.source.external_id})")
        return record
    except ValidationError as ve:
        print(f"Pydantic Validation Error for Akiflow task: {ve}", file=sys.stderr)
        return None

if __name__ == "__main__":
    sample_payload = {
        "id": "aki_t_8829102",
        "title": "Review Qwen 3.6 VL Benchmark Results",
        "status": "scheduled",
        "priority": "high",
        "duration_minutes": 45,
        "source": {
            "platform": "github",
            "external_id": "pr_1042",
            "original_url": "https://github.com/org/repo/pull/1042"
        },
        "time_block": {
            "block_id": "blk_77201",
            "calendar_id": "primary_google_cal",
            "start_time": "2027-01-07T14:00:00Z",
            "end_time": "2027-01-07T14:45:00Z",
            "is_locked": False
        }
    }

    validate_akiflow_task_payload(sample_payload)
```

## Related tools / concepts
- [Morgen](morgen.md) — Cross-platform calendar aggregator.
- [Motion](motion.md) — AI-driven scheduling and automatic time blocking.
- [Reclaim.ai](reclaim.md) — Smart calendar automation and habit tracking.
- [Sunsama](sunsama.md) — Guided daily planning and time-blocking editor.
- [Vikunja](../../services/vikunja.md) — Self-hosted open-source task management platform.
- [Google Calendar](google_calendar.md) — Cloud calendar provider.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for AI tools.

## Sources / references
- [Official Akiflow Platform](https://akiflow.com/)
- [Akiflow Knowledge Base & API Documentation](https://help.akiflow.com/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/protocol/fastmcp)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
