# TickTick

TickTick is a powerful, all-in-one task management app that integrates a calendar, Pomodoro timer, habit tracker, and Markdown notes. As of early January 2027, it remains the most feature-dense choice for personal productivity, having added native AI transcription, summarization, and **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** Task Protocol support for seamless AI agent integration with frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, and Qwen 3.6 VL.

## What it is
TickTick is a multi-platform productivity suite that consolidates essential tools into a single application. It is designed for individuals who want to manage their entire life—tasks, habits, focus, and schedule—without context switching between separate apps.

### Core Architectural Engine & Synchronization Model
TickTick operates as a multi-tier client-server architecture with an optimized offline-first synchronization protocol. The core engine synchronizes state across mobile, web, and desktop clients via real-time WebSocket subscriptions and REST delta sync fallbacks.

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT APPLICATIONS                               |
|   +--------------------+     +--------------------+     +---------------------+   |
|   | iOS / Android App  |     | Web / Desktop App  |     | CLI & Agent Clients |   |
|   +---------+----------+     +---------+----------+     +----------+----------+   |
+-------------|--------------------------|---------------------------|--------------+
              |                          |                           |
              | REST/WS Sync             | Real-time Delta Sync      | FastMCP 3.1
              v                          v                           v
+-----------------------------------------------------------------------------------+
|                              TICKTICK AGENT & MCP GATEWAY                         |
|   +---------------------------------------------------------------------------+   |
|   |                       FastMCP 3.1 Server Infrastructure                   |   |
|   |  - Task CRUD Tools       - Habit Tracker Tools     - Calendar Sync Tools |   |
|   |  - Pomodoro Timers       - Priority Search Filters - Pydantic v2 Models  |   |
|   +-------------------------------------+-------------------------------------+   |
+-----------------------------------------|-----------------------------------------+
                                          | Internal API
                                          v
+-----------------------------------------------------------------------------------+
|                             TICKTICK CORE BACKEND SERVICES                        |
|   +-------------------+    +--------------------+    +------------------------+   |
|   |  Task Engine      |    |  Calendar & Time   |    |  Habits & Focus Engine |   |
|   |  (GTD & Folders)  |    |  (e.g., CalDAV)    |    |  (Pomodoro & Matrix)   |   |
|   +---------+---------+    +---------+----------+    +-----------+------------+   |
|             |                        |                           |                |
|             +------------------------+---------------------------+                |
|                                      |                                            |
|                                      v                                            |
|                       +-------------------------------+                           |
|                       | High-Availability Cloud Store |                           |
|                       +-------------------------------+                           |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It reduces "app sprawl" and cognitive load by providing a unified interface for the Getting Things Done (GTD) methodology, Eisenhower Matrix prioritization, and time-blocking. It solves the fragmentation problem by keeping tasks and their associated calendar events and timers in one place, enabling seamless scheduling workflows.

## Where it fits in the stack
**Calendar & Tasks**. It serves as a unified human-facing interface for personal intelligence and task management. It sits between low-level calendar providers and the user, offering a rich set of capture and organization tools.

## Typical use cases
- **Unified GTD**: Capturing, clarifying, and organizing life and work tasks into Inbox, Next Actions, and Projects.
- **Time Blocking**: Dragging tasks onto the integrated calendar view to turn to-do items into scheduled calendar time blocks.
- **Habit Formation**: Tracking daily routines with streak targets, flexible reminder times, and statistics.
- **Deep Work & Focus**: Utilizing integrated Pomodoro timers with white noise soundscapes and task-specific session tracking.
- **Agentic Task Management**: Orchestrating task scheduling using Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, or Qwen 3.6 VL via FastMCP 3.1 Task Protocol to automatically turn code review feedback, pull request reviews, or meeting notes into structured tasks.

## Strengths
- **Feature Density**: Combines task tracking, full calendar view, habits, focus timers, and Markdown notes in a single subscription.
- **AI Voice & Transcription**: Built-in voice message capture with automatic AI transcription, entity extraction, and due-date inference.
- **Persistent Reminders**: Configurable repeat alerts ("nag mode") ensuring critical notifications repeat until acknowledged or completed.
- **Integrated Calendar**: Complete multi-project calendar view (Month, Week, Day, Timeline) supporting drag-and-drop time-boxing.
- **FastMCP 3.1 Integration**: First-class MCP server support allowing autonomous agents to query, schedule, and complete items safely.

## Limitations
- **Public API Rate Limits**: Official public API rate limits (e.g., max 100 requests/minute) require retry logic and local caching for bulk operations.
- **Proprietary & Closed Source**: Cloud sync relies on proprietary servers with no official self-hosted container option.
- **Data Privacy Controls**: Lacks end-to-end zero-knowledge encryption for notes and attachment files.

## When to use it
- If you want a single app to handle tasks, habits, and time-boxing without maintaining multiple standalone tools.
- If you need aggressive, persistent alerts across mobile and desktop devices.
- If you require an agent-accessible task system via FastMCP 3.1 for automated scheduling.
- If you rely heavily on dragging tasks directly onto daily or weekly calendar views.

## When not to use it
- If you strictly require open-source or local-first data storage (see [Vikunja](../../services/vikunja.md)).
- If you need enterprise project management with complex multi-team permission hierarchies.
- If you prefer a minimalist, text-only Markdown or terminal workflow.

## Getting started

### Installation
TickTick is available across web, mobile, and desktop environments:
- **Web App**: [TickTick.com](https://ticktick.com/)
- **Desktop**: macOS, Windows, Linux (Snap/AppImage)
- **Mobile**: iOS, Android, Apple Watch, Wear OS
- **Python Client**: `pip install ticktick-py pydantic fastmcp`

### Basic Automation (Python)
```python
from ticktick.api import TickTickClient

# Initialize client with OAuth credentials or user credentials
client = TickTickClient('your_email@domain.com', 'your_secure_password')

# Construct and dispatch a structured task
task = client.task.builder(
    title='Perform Ralph-loop Batch Audit',
    content='Review documentation coverage and execute quality validation checks.',
    priority=3,
    dueDate='2027-01-15T18:00:00+0000'
)
created_task = client.task.create(task)
print(f"Task created with ID: {created_task['id']}")
```

## CLI examples
Automate TickTick workspace interaction using `curl` or custom shell scripts via the TickTick Open API (V1).

```bash
# Retrieve all user project lists
curl -s -X GET "https://api.ticktick.com/open/v1/project" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" | jq '.'

# Create a task with priority and due date
curl -s -X POST "https://api.ticktick.com/open/v1/task" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Deploy FastMCP 3.1 Microservice",
    "content": "Verify Pydantic v2 schemas and register endpoints in MCP registry.",
    "priority": 5,
    "dueDate": "2027-01-10T12:00:00.000+0000",
    "timeZone": "UTC"
  }' | jq '.'

# Complete a specific task by ID
curl -s -X POST "https://api.ticktick.com/open/v1/project/${PROJECT_ID}/task/${TASK_ID}/complete" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}" \
  -H "Content-Type: application/json"
```

## API examples

### Advanced FastMCP 3.1 Task Server
Below is a full Python implementation of a **FastMCP 3.1** server exposing tools for TickTick task management, Pomodoro focus tracking, and habit checks.

```python
import os
import requests
from typing import Optional, List
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

# Initialize FastMCP Server
mcp = FastMCP("TickTick Enterprise Server", dependencies=["requests", "pydantic"])

TICKTICK_API_BASE = "https://api.ticktick.com/open/v1"
TOKEN = os.getenv("TICKTICK_ACCESS_TOKEN", "mock_token")

class CreateTaskInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the task")
    content: Optional[str] = Field(None, description="Detailed Markdown notes or description")
    priority: int = Field(0, ge=0, le=5, description="Priority level: 0 (None), 1 (Low), 3 (Medium), 5 (High)")
    project_id: Optional[str] = Field(None, description="ID of the target project folder")
    due_date: Optional[str] = Field(None, description="Due date in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the task")

    @field_validator("title")
    def validate_title(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Task title cannot be blank or contain only whitespace.")
        return clean

@mcp.tool()
def create_ticktick_task(task_data: CreateTaskInput) -> dict:
    """Create a new task in TickTick with strict Pydantic v2 validation."""
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": task_data.title,
        "content": task_data.content,
        "priority": task_data.priority,
        "projectId": task_data.project_id,
        "dueDate": task_data.due_date,
        "tags": task_data.tags
    }
    # Clean None fields
    payload = {k: v for k, v in payload.items() if v is not None}

    response = requests.post(f"{TICKTICK_API_BASE}/task", json=payload, headers=headers)
    if response.status_code in (200, 201):
        return {"status": "success", "task": response.json()}
    return {"status": "error", "code": response.status_code, "detail": response.text}

@mcp.tool()
def list_ticktick_tasks(project_id: Optional[str] = None) -> dict:
    """Retrieve all pending tasks from a given project or Inbox."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{TICKTICK_API_BASE}/project/{project_id}/data" if project_id else f"{TICKTICK_API_BASE}/project"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return {"status": "success", "data": response.json()}
    return {"status": "error", "code": response.status_code, "detail": response.text}

if __name__ == "__main__":
    mcp.run()
```

### Strict Task & Habit Validation Schemas (Pydantic v2)
To guarantee payload safety across agentic workflows, complex structures use Pydantic v2 validation logic:

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime

class HabitTrackingSchema(BaseModel):
    habit_id: str = Field(..., description="Unique hash string for habit item")
    name: str = Field(..., min_length=1, max_length=100)
    target_days: int = Field(7, ge=1, le=7, description="Weekly target frequency")
    reminder_time: Optional[str] = Field("08:00", pattern=r"^\d{2}:\d{2}$")
    streak_count: int = Field(0, ge=0)

class PomodoroSessionSchema(BaseModel):
    session_id: str = Field(..., description="Focus session transaction UUID")
    task_id: Optional[str] = Field(None, description="Linked task ID")
    duration_minutes: int = Field(25, ge=1, le=180)
    completed_at: datetime = Field(default_factory=datetime.utcnow)
    interruptions: int = Field(0, ge=0)

    @model_validator(mode="after")
    def validate_session(self) -> "PomodoroSessionSchema":
        if self.interruptions > 10:
            raise ValueError("High interruption count invalidates focus session quality score.")
        return self

# Example execution check
session_data = {
    "session_id": "pomo-9942-ax",
    "task_id": "task-8831",
    "duration_minutes": 50,
    "interruptions": 2
}
validated_pomo = PomodoroSessionSchema.model_validate(session_data)
print("Validated Pomodoro Session:", validated_pomo.model_dump_json(indent=2))
```

## Feature Comparison Matrix

| Feature | TickTick | Todoist | Akiflow | Vikunja | Motion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | All-in-one GTD & Timebox | Minimalist GTD | Time Blocking & Consolidation | Open-Source Self-Hosted | AI Auto-Scheduling |
| **Integrated Calendar** | Full (Day/Week/Month) | Basic Sync | Native Full Calendar | Basic Kanban/Cal | Full AI Engine |
| **Focus Timer / Pomodoro**| Built-in Native | Third-party / Extension | Integrated | None | None |
| **Habit Tracker** | Built-in Native | Integration Required | None | None | None |
| **FastMCP 3.1 Support** | Native Community Gateway | Community Server | Community Server | Community API Bridge | Community Plugin |
| **Self-Hostable** | No | No | No | Yes (Docker / K8s) | No |
| **Monthly Cost (2027)** | ~$3.00 / mo | ~$4.00 / mo | ~$15.00 / mo | Free (Self-hosted) | ~$19.00 / mo |

## Operational & Troubleshooting Guide

### 1. FastMCP 3.1 Connection Timeouts
- **Symptom**: Agent receives HTTP 504 or socket disconnect when querying large task projects.
- **Cause**: TickTick API rate throttling or network delay on bulk project endpoint responses.
- **Resolution**:
  1. Implement client-side pagination or request specific project sub-folders instead of all tasks simultaneously.
  2. Increase default timeout parameter in FastMCP configuration to 15 seconds:
     ```json
     "ticktick": {
       "command": "python",
       "args": ["ticktick_mcp_server.py"],
       "timeout": 15
     }
     ```

### 2. OAuth Token Refresh Failure
- **Symptom**: API calls return HTTP 401 Unauthorized after 24-48 hours of autonomous operation.
- **Cause**: Access tokens expire and automatic OAuth refresh token exchange was omitted in long-running services.
- **Resolution**: Store both `access_token` and `refresh_token` in secure secret storage. Use an explicit token refresh hook when catching HTTP 401:
  ```python
  def refresh_ticktick_token(refresh_token: str) -> str:
      resp = requests.post("https://api.ticktick.com/open/v1/oauth/token", data={
          "client_id": os.environ["CLIENT_ID"],
          "client_secret": os.environ["CLIENT_SECRET"],
          "grant_type": "refresh_token",
          "refresh_token": refresh_token
      })
      return resp.json()["access_token"]
  ```

### 3. Time Zone Offset Misalignment in Scheduled Tasks
- **Symptom**: Tasks created via agents appear shifted by several hours in TickTick calendar view.
- **Cause**: Missing explicit ISO 8601 offset or incorrect `timeZone` field in JSON API payload.
- **Resolution**: Always supply UTC ISO timestamp strings ending in `Z` or explicit offsets (e.g., `2027-01-10T14:00:00+00:00`) and pass `"timeZone": "UTC"`.

## Related tools / concepts
- [Todoist](todoist.md) — Minimalist task management alternative.
- [Akiflow](akiflow.md) — Time-blocking and task consolidation engine.
- [Amie](amie.md) — Aesthetic calendar-first workspace.
- [Vikunja](../../services/vikunja.md) — Open-source, self-hostable task engine.
- [Motion](../automation_orchestration/motion.md) — Automated AI calendar scheduling.
- [Habitica](../../services/habitica.md) — Gamified task tracking alternative.
- [n8n](../../services/n8n.md) — Workflow automation connector for TickTick.

## Sources / references
- [Official Website](https://ticktick.com/)
- [TickTick OpenAPI Documentation](https://developer.ticktick.com/docs)
- [FastMCP 3.1 Framework Documentation](https://github.com/jina-ai/fastmcp)
- [TickTick MCP Gateway Repository](https://github.com/alexarevalo/mcp-server-ticktick)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
