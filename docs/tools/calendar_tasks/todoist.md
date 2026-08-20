# Todoist

## What it is
A popular task management application that helps individuals and teams organize, plan, and collaborate on projects. As of early 2027, it features advanced AI capabilities through the **Ramble AI** voice engine and native FastMCP 3.1 (Model Context Protocol) support.

## What problem it solves
Provides a simple yet powerful interface for capturing tasks, setting deadlines, and organizing work into projects and sub-tasks. It excels at natural language parsing, allowing users to schedule complex recurring tasks via text or voice across desktop, web, and mobile clients.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management. Functions as a core task store and capture engine that connects to calendars (Google Calendar, Outlook) and AI agents.

## Typical use cases
- **Daily task management**: Capture and organize personal and work items using the "Inbox" and "Today" views.
- **AI-assisted planning**: Use the **Ramble AI** voice-to-task feature for hands-free capture in 38+ languages.
- **Agentic workflows**: Connect Todoist to **Claude 5.1**, **GPT-5.5**, or **Llama 4** via FastMCP 3.1 to automate task sorting, breakdown, and prioritization.
- **Maintenance patterns**: Use recurring tasks for system health checks and routine homelab or administrative tasks.

## Strengths
- Clean, intuitive interface across all platforms (including Linux and wearables).
- Best-in-class natural language parsing for deadlines (e.g., "every second Thursday at 3pm").
- Two-way sync with Google Calendar and Reclaim.ai.
- **FastMCP 3.1 Native**: Supports the Model Context Protocol for seamless integration with AI agents.

## Limitations
- Advanced features like reminders and location filters require a Pro/Business subscription.
- Lacks native Gantt charts or complex dependency graph modeling (better suited for GTD than complex enterprise PM).

## When to use it
- For personal or small group task organization.
- When you need a fast, reliable way to capture and categorize tasks using natural language.
- If you want an AI agent to manage your todo list autonomously via FastMCP 3.1.

## When not to use it
- For complex software development projects with strict code dependencies (prefer Jira or GitHub Issues).
- If you require a fully local-first or self-hosted solution (consider [Vikunja](../../services/vikunja.md)).

## Getting started
### Official Integration
Todoist offers native apps for all major platforms. To integrate with AI tools:
1. Generate an API token in **Settings > Integrations > Developer**.
2. **Hello-world example**: Create a task via cURL:
   ```bash
   curl -X POST https://api.todoist.com/rest/v2/tasks \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"content": "Audit 2027 playbooks", "due_string": "tomorrow"}'
   ```

## CLI examples

> [!NOTE]
> While there is an official CLI, many users prefer the **Todoist FastMCP Server** for agentic use cases.

### Using the Official CLI
```bash
# Install (macOS/Linux)
brew install todoist-cli

# List tasks due today
todoist list --filter "today"

# Add a task
todoist add "Check server logs every morning" --date "every day"
```

## API examples
Todoist provides a stable REST API v2 for developers.

### Create and Validate a Task (Python)
Programmatic task creation should be validated using **Pydantic v2** prior to making requests to the Todoist REST API v2 under early 2027 guidelines.

```python
import requests
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Define Pydantic v2 Model for Task Creation
class TodoistTaskPayload(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, description="The task text description")
    description: Optional[str] = Field(default=None, description="Detailed task description")
    project_id: Optional[str] = None
    section_id: Optional[str] = None
    parent_id: Optional[str] = None
    order: Optional[int] = None
    labels: List[str] = Field(default_factory=list)
    priority: int = Field(default=1, ge=1, le=4, description="1 (normal) to 4 (urgent)")
    due_string: Optional[str] = Field(default=None, description="Natural language due date, e.g. 'tomorrow at 12pm'")

# Validate task data payload
raw_data = {
    "content": "Verify backup retention policy with Claude 5.1",
    "description": "Ensure offsite snapshots are secure under FastMCP 3.1 architectures.",
    "labels": ["homelab", "security"],
    "priority": 4,
    "due_string": "next Friday at 4pm"
}

try:
    validated_payload = TodoistTaskPayload.model_validate(raw_data)
    print(f"Validated Todoist payload: '{validated_payload.content}'")

    # POST payload via requests
    API_TOKEN = "YOUR_TODOIST_API_TOKEN"
    API_URL = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    # response = requests.post(API_URL, headers=headers, json=validated_payload.model_dump(exclude_none=True))
except Exception as e:
    print(f"Validation failed: {e}")
```

### Model Context Protocol (FastMCP 3.1) Integration
Integrate Todoist with agents like **Claude 5.1**, **GPT-5.5**, or **Llama 4** using an MCP server.

**Recommended Server**: `Doist/todoist-ai` (Official) or `shockedrope/todoist-mcp` (Community).

**Tools available**:
- `create_task`: Create tasks with full natural language date parsing.
- `list_tasks`: Fetch tasks filtered by project, label, or date.
- `update_task`: Modify existing entries.
- `get_stats`: View productivity metrics and completed task counts.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Personal) / Paid (Pro/Business)
- **Self-hostable**: No

## Related tools / concepts
- [Reclaim.ai](reclaim.md) — Automatically time-blocks Todoist tasks.
- [Google Calendar](google_calendar.md) — Two-way calendar sync partner.
- [Outlook](outlook.md) — Microsoft calendar partner.
- [Vikunja](../../services/vikunja.md) — Open-source, self-hosted alternative.
- [n8n](../../services/n8n.md) — Used for advanced Todoist automations.
- [Model Context Protocol](../automation_orchestration/mcp.md) — FastMCP 3.1 specification.

## Sources / references
- [Official Website](https://todoist.com/)
- [Todoist API v2 Documentation](https://developer.todoist.com/rest/v2/)
- [Todoist AI MCP Server (GitHub)](https://github.com/Doist/todoist-ai)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
