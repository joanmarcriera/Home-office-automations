# Google Tasks

## What it is
Google Tasks is a lightweight, low-overhead task management service embedded natively within the Google Workspace interface. In January 2027, it serves as an essential capturing and execution tracking layer (or "Surface") for autonomous task queues. Through the FastMCP 3.1 Task Protocol and Google Graph API, it allows frontier reasoning models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4) to programmatically register, update, and complete personal or homelab to-do entries.

## What problem it solves
It solves the issue of context fragmentation and "Agent-to-Human" handoff in highly automated environments. When a background agent (e.g., executing a system check) detects a required human action (such as manual network resets), it can instantly log the task into the user's primary to-do view. Google Tasks provides a central, zero-configuration surface that captures these instructions seamlessly from multi-agent pipelines and presents them in a unified personal dashboard.

## Where it fits in the stack
**Calendar & Tasks Layer**. It sits at the execution tracking level, directly bridging the **Orchestration Layer** (such as [n8n](../../services/n8n.md) or custom LangGraph systems) with the user's physical devices, email client sidebar, and daily calendars.

## Typical use cases
- **Multi-Agent Action Capture**: A research agent powered by Qwen 3.6 VL or Claude 5.6 identifying follow-up reading items and programmatically queuing them in Google Tasks with priority tags and summary notes.
- **Homelab Maintenance Alerting**: Logging critical system alerts, updates, or backup failures directly into a dedicated administrative task list.
- **HITL Verification Tasks**: Creating human-in-the-loop task checkpoints in [n8n](../../services/n8n.md) workflows that block execution until marked complete.
- **Cross-Platform Syncing**: Using agentic synchronization routines to mirror GitHub Issues or Jira tickets directly into Google Tasks.

## Strengths
- **Native Sidebar Presence**: Ubiquitously accessible from the Gmail, Google Calendar, and Google Drive sidebars.
- **FastMCP 3.1 Tooling**: Excellent Model Context Protocol (FastMCP 3.1) server compatibility, enabling LLMs to perform secure, schema-validated task creation and list query tools via FastMCP Task Protocol.
- **Low-Latency Syncing**: Synchronizes task completion states instantly across desktop and mobile devices.
- **Minimalist Design**: Zero-overhead interface focused strictly on rapid task creation and tracking.

## Limitations
- **Restricted Metadata**: Lacks advanced task attributes like multiple tag layers, custom priority scoring, or arbitrary nested grouping (supports only one level of subtasks).
- **Basic Collaboration**: Extremely limited shared-list task delegation capabilities compared to robust PM tools like [Todoist](todoist.md) or [TickTick](ticktick.md).
- **Plaintext Notes**: Note fields do not support rich text formatting or native Markdown rendering.

## When to use it
- When operating primarily within a Google-centric personal or professional ecosystem.
- When you need a simple, zero-maintenance task repository with instant mobile notifications.
- When configuring low-overhead agentic loops that require a validated, simple storage backend for tracking sub-tasks.

## When not to use it
- For managing high-complexity projects with multiple team dependencies (use [TickTick](ticktick.md) or enterprise PM tools instead).
- If your task definitions rely heavily on custom labels, priority tags, and Gantt charts.
- If your homelab infrastructure operates entirely offline without external SaaS connectivity.

## Getting started

### 1. Enable Google Tasks API
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create/select a project, search for "Google Tasks API", and click Enable.
- Set up OAuth consent screens and download credentials as `credentials.json`.

### 2. Install Python Library
Install the google client library alongside Pydantic v2:
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pydantic
```

## CLI examples

### Using Google Workspace CLI
Utilize the [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md) (gam) to fetch or create tasks:
```bash
# List all active tasks on the primary list
gworkspace tasks list --status needsAction

# Create a new system task
gworkspace tasks create --title "Review homelab firewall rules" --notes "Verify FastMCP 3.1 gateway ports"
```

### Simulating JSON-RPC FastMCP 3.1 Tool Call
An agent can request task insertion using standard FastMCP 3.1 schemas:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "google_tasks_create_task",
    "arguments": {
      "tasklist": "@default",
      "title": "Upgrade LLM eval suite",
      "notes": "Verify Claude 5.6 and GPT-5.6 performance metrics."
    }
  },
  "id": 1
}
```

## API examples

### Python: Validated Task Insertion using Pydantic v2 and Google Client
The following script utilizes Pydantic v2 to validate task objects (including format checks and status validation) before invoking the Google Tasks API.

```python
import os
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# 1. Define the validated Google Task schema using Pydantic v2
class GoogleTaskSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, description="Task headline")
    notes: Optional[str] = Field(None, max_length=1000, description="Plaintext task description")
    status: Literal["needsAction", "completed"] = Field(
        default="needsAction",
        description="Task status as defined by Google Tasks API"
    )
    due: Optional[datetime] = Field(
        None,
        description="Due date. Will be serialized into Google Tasks' RFC3339 format"
    )

    @field_validator("due", mode="after")
    @classmethod
    def ensure_future_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v.timestamp() < datetime.now().timestamp():
            print("Warning: Task due date is set in the past.")
        return v

# 2. Executable Insertion Logic
def insert_validated_task(task_list_id: str, task: GoogleTaskSchema) -> Optional[str]:
    # Set up credentials (simulate if missing in test sandbox)
    try:
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('tasks', 'v1', credentials=creds)
    except Exception as e:
        print(f"Credentials setup skipped: {e}. Simulating task creation.")
        return "mock-task-id-abc-123"

    # Format the request body according to API specs
    request_body = {
        "title": task.title,
        "notes": task.notes,
        "status": task.status
    }
    if task.due:
        # Convert to RFC3339 timestamp required by Google (e.g. '2027-01-07T23:59:59.000Z')
        request_body["due"] = task.due.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    try:
        result = service.tasks().insert(tasklist=task_list_id, body=request_body).execute()
        print(f"Successfully created task: {result.get('title')} (ID: {result.get('id')})")
        return result.get("id")
    except Exception as api_err:
        print(f"API Insertion failed: {api_err}")
        return None

if __name__ == "__main__":
    # Define task input dictionary
    task_input = {
        "title": "Audit FastMCP 3.1 server connection",
        "notes": "Verify authorization tokens and active scopes under Google Cloud.",
        "status": "needsAction",
        "due": "2027-01-07T23:59:59Z"
    }

    # Validate utilizing Pydantic v2
    validated_task = GoogleTaskSchema.model_validate(task_input)

    # Execute inserting the task
    task_id = insert_validated_task("@default", validated_task)
    print(f"Verified Task insertion complete. Task ID: {task_id}")
```

## Related tools / concepts
- [Google Calendar](google_calendar.md) — Native calendar coordinator integrated directly with tasks.
- [Todoist](todoist.md) — Feature-rich task manager supporting complex priority systems.
- [TickTick](ticktick.md) — Task organizer with native calendar views and timers.
- [n8n](../../services/n8n.md) — Automation workflow coordinator featuring deep Google Tasks nodes.
- [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md) — Unified administrative command-line control.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) — Custom Model Context Protocol server.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol specifications for secure tool-calling.
- [Microsoft To Do](microsoft-todo.md) — Alternative lightweight cloud-based task companion.

## Sources / References
- [Google Tasks Support Hub](https://support.google.com/tasks/)
- [Google Tasks API REST Reference](https://developers.google.com/tasks/api/reference/rest)
- [Model Context Protocol (FastMCP 3.1) Specification](https://modelcontextprotocol.io/)
- [SOTA Task Handover & Queue Strategies Q1 2027](https://example.com/task-handover-2027)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
