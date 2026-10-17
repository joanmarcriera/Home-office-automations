# Todoist

## What it is
Todoist is an enterprise-grade task management platform designed for individuals, teams, and autonomous AI agents to organize projects, track deadlines, and automate personal or organizational workflows. As of early 2027, Todoist features deep integration with AI ecosystem standards including **FastMCP 3.1** (Model Context Protocol), **Ramble AI** high-accuracy voice-to-task capture across 38 languages, bi-directional calendar synchronization engines, and dynamic natural language processing engines.

## What problem it solves
Capturing ideas, tasks, and complex recurring schedules often suffers from UI friction, inconsistent multi-device synchronization, or rigid input forms. Furthermore, autonomous AI agents require a deterministic state store to log, track, and close sub-goals without polluting local memory buffers.

Todoist resolves this by offering intuitive natural language processing (e.g., "Review Q3 security policy every 2nd Tuesday at 4pm p1 #security"), real-time multi-platform sync, and structured REST/Sync API endpoints that allow AI agents (**Claude 5.6**, **GPT-5.6**, **Llama 4**) to inspect, create, decompose, and execute task graphs autonomously.

## System Architecture & FastMCP 3.1 Flow

The following diagram outlines the FastMCP 3.1 integration architecture between AI foundation models, local client agents, webhooks, and the Todoist REST API v2 / Sync API infrastructure:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   AI Foundation Models & Agents                        │
│          (Claude 5.6 / GPT-5.6 / Llama 4 / Multi-Agent Mesh)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ FastMCP 3.1 / MCP JSON-RPC Protocol
┌───────────────────────────────────▼────────────────────────────────────┐
│                  TODOIST MCP AGENT INTEGRATION SERVER                  │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────┐ │
│ │  OAuth2 / Token Auth │ │ Pydantic v2 Payload  │ │ REST API v2      │ │
│ │  Manager Module      │ │ Validator            │ │ Dispatcher       │ │
│ └──────────────────────┘ └──────────────────────┘ └──────────────────┘ │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Validated Task Sync / NLP Parsing
┌───────────────────────────────────▼────────────────────────────────────┐
│                    Todoist Cloud & Sync Ecosystem                      │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────┐ │
│ │ Google Calendar /    │ │ Reclaim.ai Time-     │ │ Ramble AI Voice  │ │
│ │ Outlook 2-Way Sync   │ │ Blocking Engine      │ │ Capture Stream   │ │
│ └──────────────────────┘ └──────────────────────┘ └──────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### Dynamic Webhook & Synchronization Sequence

1. **Voice / Agent Task Event Ingestion**: A user captures a voice task via Ramble AI or an autonomous agent dispatches a task via FastMCP 3.1.
2. **NLP & Entity Resolution**: Todoist parses natural language strings (due date, recurring rules, priority tags, project labels) into structured attributes.
3. **Webhook Dispatch & Event Streaming**: Todoist broadcasts a `item:added` or `item:completed` JSON event payload to registered FastMCP 3.1 webhook endpoints.
4. **State Reconciliation**: Local workflow tools (e.g., n8n, Home Assistant, or custom Python microservices) update local state buffers or trigger secondary subagent executions.

```
User / Voice / Agent       FastMCP Server         Todoist REST API         Google Calendar
         │                       │                       │                        │
         │─── Create Task Request ──>                    │                        │
         │   ("Audit Homelab p1")│                       │                        │
         │                       │─── POST /rest/v2 ────>│                        │
         │                       │    (Validated Payload)│                        │
         │                       │                       │─── 2-Way Event Sync ──>│
         │                       │<── 200 OK (Task UUID)─│                        │
         │<── Task Created Conf ─│                       │                        │
         │                       │                       │                        │
         │                       │<── Webhook Event ─────│                        │
         │                       │    (item:completed)   │                        │
```

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management. Serves as a centralized execution and task state repository connecting calendar engines ([Google Calendar](google_calendar.md), [Outlook](outlook.md)), automated schedulers ([Reclaim.ai](reclaim.md)), self-hosted workflow automation ([n8n](../../services/n8n.md)), and AI frameworks via FastMCP 3.1.

## Feature Comparison Matrix

| Feature / Aspect | Todoist | Vikunja | Motion | Reclaim.ai |
| :--- | :--- | :--- | :--- | :--- |
| **Deployment Model** | Cloud SaaS | 100% Self-Hosted | Cloud SaaS | Cloud SaaS |
| **NLP Speed & Accuracy**| Industry Gold Standard | Standard Syntax | Algorithmic Calendar | Calendar Blocking |
| **FastMCP 3.1 Integration**| Native (`@doist/mcp`) | Community Server | Custom API Wrapper | Calendar Tool |
| **Voice Task Capture** | Native Ramble AI | External Webhook | No | No |
| **Two-Way Calendar Sync**| Google / Outlook | CalDAV | Native | Native |
| **Free Tier Features** | Core Task Management | Full System (Self-host)| Trial Only | Core Schedules |
| **API Rate Limits** | 450 req / min | Unlimited (Self-host) | Vendor Dependent | Vendor Dependent |
| **Webhook Delivery SLA**| High Availability | Local Immediate | Vendor Dependent | Standard |

## Typical use cases
- **Personal and Team Task Capture**: Organize cross-functional work into hierarchical projects, sections, and sub-tasks with color-coded labels and priority tags.
- **Autonomous Agent Workflows**: Allow AI assistants (**Claude 5.6**, **GPT-5.6**) to inspect task queues, decompose high-level objectives into sub-tasks, and update task status via FastMCP 3.1 tools.
- **Voice-to-Task Ingestion**: Hands-free capture using the **Ramble AI** voice engine, automatically extracting due dates, project tags, and assignee metadata across 38 languages.
- **System Maintenance & Audit Logging**: Track homelab maintenance, infrastructure health checks, SSL certificate renewals, and recurring compliance audits through scheduled recurring tasks.
- **Multi-Agent Task Decomposition**: A primary router agent creates top-level epics in Todoist while worker subagents execute items and mark them completed in real time.

## Strengths
- **FastMCP 3.1 Native Protocol**: Full Model Context Protocol compatibility enabling plug-and-play agentic task management.
- **Best-in-Class NLP**: Industry-leading natural language parsing for scheduling, labels, priorities, and projects in a single line.
- **Extensive Ecosystem Integrations**: Native bi-directional sync with Google Calendar, Outlook, Reclaim.ai, and n8n workflow engines.
- **Cross-Platform Availability**: Web, desktop (macOS, Windows, Linux), iOS, Android, and wearable apps with offline sync support.
- **Sub-Second Webhook Latency**: Pushes task status mutations instantly to external automation endpoints.

## Limitations
- **Closed-Source SaaS**: Proprietary backend cloud infrastructure; not available for self-hosted local deployments (consider [Vikunja](../../services/vikunja.md) for self-hosted environments).
- **Freemium Tier Limits**: Reminders, activity history, and custom filters require a Pro or Business subscription tier.
- **Simple Dependency Modeling**: Lacks native Gantt chart visualization or complex dependency graph tracking out of the box.
- **API Rate Limiting**: Max 450 requests per minute per user token; rapid looping agents can trigger HTTP 429 errors without backoff strategy.

## Operational Best Practices & Troubleshooting

1. **OAuth Token Refreshing**: Store the `TODOIST_API_TOKEN` securely in secret managers (e.g., HashiCorp Vault) rather than hardcoded environment variables in production FastMCP subagents.
2. **Rate Limit Handling**: Implement exponential backoff with jitter in automated task ingestion loops to comply with Todoist's 450 requests per minute API limit.
3. **NLP Disambiguation**: Use explicit timezones in the `due_string` payload (e.g., `every Friday at 15:00 EST`) when automating tasks across distributed multi-region agent clusters.
4. **Project ID Caching**: Cache Todoist `project_id` and `section_id` UUID mappings locally in subagent memory to minimize lookup REST calls during high-frequency task creation.
5. **Webhook HMAC Signature Verification**: Always validate the `X-Todoist-Hmac-SHA256` header on incoming webhook endpoints to prevent unauthorized request injection.

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Resolution / Operational Action |
| :--- | :--- | :--- |
| **HTTP 429 Rate Limit Exceeded** | Subagent loop sending >450 req/min | Apply batching using Sync API or enforce a 150ms delay between REST calls. |
| **Due Date Parsed Incorrectly** | Implicit or ambiguous timezone | Use explicit ISO 8601 strings or pass `due_string` with timezone offset e.g., `at 14:00 UTC`. |
| **Webhook Secret Mismatch** | Stale or unverified client secret | Regenerate webhook secret in Developer Portal and verify HMAC SHA-256 header. |
| **Task Missing in Sync API** | Local sync sequence token (`sync_token`) out of date | Reset `sync_token="*"` to trigger full state re-synchronization. |
| **FastMCP Tool Execution Timeout** | Network latency or API token error | Check token validity with `curl -H "Authorization: Bearer $TOKEN" https://api.todoist.com/rest/v2/projects`. |

## When to use it
- When you need a reliable, fast task management hub accessible across all user devices.
- When pairing task capture with AI agents that manipulate task queues via FastMCP 3.1.
- When natural language date and time parsing is essential for rapid entry.
- When syncing schedules bi-directionally with Google Calendar or Reclaim.ai.

## When not to use it
- If your policy demands 100% self-hosted, local-first air-gapped data retention (use [Vikunja](../../services/vikunja.md)).
- For complex, multi-team software issue tracking requiring custom workflow transitions and sprint boards (use Jira or GitHub Issues).

## Getting started

### API Access Setup
1. Log into Todoist and navigate to **Settings > Integrations > Developer**.
2. Copy your **API Token**.
3. Verify basic API connectivity via cURL:
   ```bash
   curl -X GET https://api.todoist.com/rest/v2/projects \
     -H "Authorization: Bearer $TODOIST_API_TOKEN"
   ```

## CLI examples

### Official Todoist CLI Usage
Power users and script automation workflows can interact directly with Todoist via CLI binaries:

```bash
# Install via Homebrew
brew install todoist-cli

# Authenticate with API Token
todoist auth $TODOIST_API_TOKEN

# List all tasks due today
todoist list --filter "today"

# Add a task with project, priority, and due date
todoist add "Run weekly database backup audit" --project "Homelab" --priority 4 --date "every Sunday at 02:00"

# Complete task by ID
todoist close 84920184
```

## API examples

### Pydantic v2 Task Creation & Validation
Programmatic task creation should be validated using **Pydantic v2** prior to making REST API v2 calls under early 2027 standards.

```python
import os
import requests
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class TodoistTaskPayload(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, description="Task summary or title")
    description: Optional[str] = Field(default=None, max_length=15000, description="Detailed Markdown notes")
    project_id: Optional[str] = Field(default=None, description="Target Todoist project ID")
    section_id: Optional[str] = Field(default=None, description="Target section ID within project")
    parent_id: Optional[str] = Field(default=None, description="Parent task ID for sub-tasks")
    order: Optional[int] = Field(default=None, description="Task position index")
    labels: List[str] = Field(default_factory=list, description="List of label strings")
    priority: int = Field(default=1, ge=1, le=4, description="Priority integer: 1 (normal) to 4 (urgent)")
    due_string: Optional[str] = Field(default=None, description="Natural language due string e.g. 'tomorrow at 3pm'")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: int) -> int:
        if value not in (1, 2, 3, 4):
            raise ValueError("Priority must be 1 (normal), 2 (medium), 3 (high), or 4 (urgent)")
        return value

# Raw incoming data payload from AI Agent or pipeline
raw_payload = {
    "content": "Perform quarterly security audit on FastMCP 3.1 endpoints",
    "description": "Verify OAuth2 tokens, rate limits, and SSL certificate expiration dates.",
    "labels": ["security", "infrastructure", "ai-ops"],
    "priority": 4,
    "due_string": "next Monday at 09:00"
}

try:
    # Perform strict Pydantic v2 validation
    validated_task = TodoistTaskPayload.model_validate(raw_payload)
    print(f"Validated task payload: '{validated_task.content}'")

    # Dispatch request to Todoist API v2
    api_token = os.getenv("TODOIST_API_TOKEN", "mock_token")
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Execute POST request logic
    # response = requests.post(
    #     "https://api.todoist.com/rest/v2/tasks",
    #     headers=headers,
    #     json=validated_task.model_dump(exclude_none=True)
    # )
except ValidationError as e:
    print(f"Payload validation failed: {e}")
```

### Complete FastMCP 3.1 Subagent Tool Server Example
Integrate Todoist with AI agent runtimes (**Claude 5.6**, **GPT-5.6**, **Llama 4**) using a custom Python **FastMCP 3.1** tool server supporting full task lifecycle CRUD operations.

```python
import os
import requests
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

mcp = FastMCP("Todoist-Agent-Manager")
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN", "")
BASE_URL = "https://api.todoist.com/rest/v2"

def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}",
        "Content-Type": "application/json"
    }

class CreateTaskInput(BaseModel):
    content: str = Field(..., description="Summary title of the task")
    description: Optional[str] = Field(default=None, description="Detailed notes or agent context")
    due_string: Optional[str] = Field(default="today", description="Natural language due date e.g. 'tomorrow at 5pm'")
    priority: int = Field(default=1, ge=1, le=4, description="1=Normal, 4=Urgent")
    labels: List[str] = Field(default_factory=list, description="List of labels e.g. ['agent', 'homelab']")

class FilterTasksInput(BaseModel):
    filter_query: str = Field(default="today", description="Todoist filter string e.g. 'today | overdue'")

class CloseTaskInput(BaseModel):
    task_id: str = Field(..., description="Todoist unique task ID to mark as completed")

@mcp.tool()
async def create_todoist_task(payload: CreateTaskInput) -> Dict[str, Any]:
    """Creates a new task in Todoist with natural language scheduling."""
    if not TODOIST_API_TOKEN:
        return {"error": "TODOIST_API_TOKEN environment variable not set."}

    res = requests.post(
        f"{BASE_URL}/tasks",
        headers=get_headers(),
        json=payload.model_dump(exclude_none=True)
    )
    if res.status_code == 200:
        return res.json()
    return {"error": f"Failed with status {res.status_code}: {res.text}"}

@mcp.tool()
async def list_todoist_tasks(payload: FilterTasksInput) -> Dict[str, Any]:
    """Queries active tasks filtered by date, priority, project, or label query string."""
    if not TODOIST_API_TOKEN:
        return {"error": "TODOIST_API_TOKEN environment variable not set."}

    res = requests.get(
        f"{BASE_URL}/tasks",
        headers=get_headers(),
        params={"filter": payload.filter_query}
    )
    if res.status_code == 200:
        return {"tasks": res.json()}
    return {"error": f"Failed with status {res.status_code}: {res.text}"}

@mcp.tool()
async def close_todoist_task(payload: CloseTaskInput) -> Dict[str, Any]:
    """Closes and completes a Todoist task by ID."""
    if not TODOIST_API_TOKEN:
        return {"error": "TODOIST_API_TOKEN environment variable not set."}

    res = requests.post(
        f"{BASE_URL}/tasks/{payload.task_id}/close",
        headers=get_headers()
    )
    if res.status_code == 204:
        return {"status": "success", "closed_task_id": payload.task_id}
    return {"error": f"Failed with status {res.status_code}: {res.text}"}

if __name__ == "__main__":
    mcp.run()
```

### Model Context Protocol (`claude_desktop_config.json`) Configuration
```json
{
  "mcpServers": {
    "todoist": {
      "command": "python",
      "args": ["-m", "todoist_fastmcp_server"],
      "env": {
        "TODOIST_API_TOKEN": "YOUR_TODOIST_API_TOKEN"
      }
    }
  }
}
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Free tier available; Pro tier at ~$4/mo; Business tier for teams at ~$6/user/mo)
- **Self-hostable**: No

## Related tools / concepts
- [Reclaim.ai](reclaim.md) — Smart AI calendar time-blocking and Todoist sync engine.
- [Google Calendar](google_calendar.md) — Two-way event and task sync partner.
- [Outlook](outlook.md) — Microsoft email and task integration partner.
- [Vikunja](../../services/vikunja.md) — Open-source, self-hosted task management alternative.
- [n8n](../../services/n8n.md) — Workflow automation engine for custom Todoist triggers.
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — FastMCP 3.1 agent architecture standard.

## Sources / references
- [Todoist Official Site](https://todoist.com/)
- [Todoist REST API v2 Reference](https://developer.todoist.com/rest/v2/)
- [Doist Todoist AI FastMCP Server Repository](https://github.com/Doist/todoist-ai)
- [Ramble AI Voice Feature Guide](https://todoist.com/help/articles/ramble-ai)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
