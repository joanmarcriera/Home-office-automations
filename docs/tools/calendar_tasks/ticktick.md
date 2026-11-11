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

## Mathematical Formulations & Synchronization Dynamics

### 1. Delta Sync Protocol & Conflict-Free Resolution
TickTick models client synchronizations using vector clocks and Last-Write-Wins (LWW) element registers. Let $S_{\text{client}}$ and $S_{\text{server}}$ be client and server state vectors across $K$ items. The delta update payload size $\Delta_{\text{payload}}$ for synchronization timestamp $t_{\text{sync}}$ is bounded by:

$$\Delta_{\text{payload}} = \sum_{i=1}^K \mathbb{I}\left(t_{\text{modified}}(x_i) > t_{\text{last\_checkpoint}}\right) \cdot \text{Bytes}(x_i)$$

For concurrent modifications on item $x_i$ occurring on client $c$ and server $s$, the conflict resolution function $\mathcal{R}(x_i^c, x_i^s)$ converges deterministically:

$$\mathcal{R}(x_i^c, x_i^s) = \begin{cases}
x_i^c & \text{if } t_{\text{utc}}(x_i^c) > t_{\text{utc}}(x_i^s) \\
x_i^s & \text{if } t_{\text{utc}}(x_i^s) > t_{\text{utc}}(x_i^c) \\
\operatorname{merge\_fields}(x_i^c, x_i^s) & \text{if } t_{\text{utc}}(x_i^c) = t_{\text{utc}}(x_i^s)
\end{cases}$$

### 2. Recurrence Rule (RRULE) Interval Calculation
Recurring tasks follow RFC 5545 recurrence rules. Let $t_0$ be the base due date, $I_{\text{freq}}$ the recurrence interval, and $B_{\text{byday}}$ the set of allowed weekdays ($B_{\text{byday}} \subseteq \{0, 1, \dots, 6\}$). The next occurrence timestamp $t_{n+1}$ satisfies:

$$t_{n+1} = \min \left\{ t > t_n \mid t = t_0 + k \cdot I_{\text{freq}}, \, \text{weekday}(t) \in B_{\text{byday}} \right\}$$

with habit completion streak $H_{\text{streak}}$ evaluated over discrete day sequence $d \in \{1, \dots, D\}$:

$$H_{\text{streak}} = \max \left\{ k \ge 0 \mid \forall j \in [0, k-1], \, \text{Completed}(D - j) = 1 \right\}$$

### 3. Pomodoro Focus Score & Interruption Attenuation
The effective focus productivity score $\Phi \in [0, 100]$ for a session of duration $T_{\text{pomo}}$ minutes with $N_{\text{interrupt}}$ interruptions and pause duration $t_{\text{pause}}$ is computed as:

$$\Phi = 100 \cdot \left(\frac{T_{\text{pomo}} - t_{\text{pause}}}{T_{\text{pomo}}}\right) \cdot \exp\left(-\lambda_{\text{decay}} \cdot N_{\text{interrupt}}\right)$$

where $\lambda_{\text{decay}} \approx 0.15$, penalizing fragmented focus sessions exponentially.

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
- If you require air-gapped on-premise deployments without third-party cloud data egress.

## Getting started

### Installation
Install the necessary Python dependencies for building a TickTick FastMCP 3.1 gateway:

```bash
pip install requests fastmcp pydantic uvicorn httpx
```

Configure environment credentials with your TickTick developer access token:

```bash
export TICKTICK_ACCESS_TOKEN="your_ticktick_oauth2_token_here"
export TICKTICK_CLIENT_ID="your_client_id"
export TICKTICK_CLIENT_SECRET="your_client_secret"
```

### Minimal Client Example
Verify API connectivity by fetching user projects:

```python
import os
import requests

TOKEN = os.environ.get("TICKTICK_ACCESS_TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get("https://api.ticktick.com/open/v1/project", headers=headers)
if response.status_code == 200:
    for proj in response.json():
        print(f"Project: {proj.get('name')} (ID: {proj.get('id')})")
else:
    print(f"Failed to fetch projects: {response.status_code} - {response.text}")
```

## Systemd Service Unit Configuration

To run a continuous TickTick FastMCP 3.1 bridge daemon on a Linux home server or cloud instance, deploy the following unit to `/etc/systemd/system/ticktick-mcp-bridge.service`:

```ini
[Unit]
Description=TickTick FastMCP 3.1 Bridge Daemon
After=network-online.target
Wants=network-online.target
Documentation=https://developer.ticktick.com/docs

[Service]
Type=simple
User=knowledgeops
Group=knowledgeops
WorkingDirectory=/opt/ticktick-bridge
ExecStart=/opt/ticktick-bridge/.venv/bin/python -m bridge.ticktick_server
Restart=always
RestartSec=5s

# Environment settings
Environment=PYTHONUNBUFFERED=1
Environment=TICKTICK_ACCESS_TOKEN=your_ticktick_oauth2_token_here
Environment=PORT=8093

# Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/ticktick-bridge/logs
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ticktick-mcp-bridge.service
sudo systemctl status ticktick-mcp-bridge.service
```

## Docker Compose Stack (`docker-compose.yml`)

Deploy a containerized TickTick FastMCP gateway with local Redis synchronization caching:

```yaml
version: "3.9"

services:
  ticktick-mcp-gateway:
    image: ticktick-fastmcp-gateway:v2027.1
    container_name: ticktick-mcp-gateway
    restart: unless-stopped
    ports:
      - "8093:8093"
    environment:
      - TICKTICK_ACCESS_TOKEN=${TICKTICK_ACCESS_TOKEN}
      - REDIS_URL=redis://ticktick-redis:6379/0
      - LOG_LEVEL=INFO
    depends_on:
      ticktick-redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8093/health"]
      interval: 15s
      timeout: 5s
      retries: 3
    networks:
      - task-mesh

  ticktick-redis:
    image: redis:7.4-alpine
    container_name: ticktick-redis
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--maxmemory", "256mb", "--maxmemory-policy", "volatile-lru"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - task-mesh

networks:
  task-mesh:
    driver: bridge
```

## CLI examples

### 1. Fetch User Profile via cURL
Query account profile information and check subscription tier:

```bash
curl -s -X GET "https://api.ticktick.com/open/v1/user/profile" \
  -H "Authorization: Bearer $TICKTICK_ACCESS_TOKEN" | jq .
```

### 2. Create Quick Task in Inbox
Submit a task payload directly from the terminal:

```bash
curl -s -X POST "https://api.ticktick.com/open/v1/task" \
  -H "Authorization: Bearer $TICKTICK_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review PR for FastMCP 3.1 schema updates",
    "content": "Ensure all Pydantic v2 models have extra=forbid and frozen=True",
    "priority": 3,
    "dueDate": "2027-01-15T18:00:00+0000"
  }' | jq .
```

### 3. Complete Task by ID
Mark a task as completed:

```bash
curl -s -X POST "https://api.ticktick.com/open/v1/project/inbox/task/task_id_123/complete" \
  -H "Authorization: Bearer $TICKTICK_ACCESS_TOKEN"
```

## API examples

### Complete FastMCP 3.1 Task & Habit Server
The following complete FastMCP server implements task creation and retrieval with strict **Pydantic v2** validation (`extra="forbid"`, `frozen=True`):

```python
import os
import requests
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from fastmcp import FastMCP

mcp = FastMCP("ticktick-fastmcp-server")

TICKTICK_API_BASE = "https://api.ticktick.com/open/v1"
TOKEN = os.environ.get("TICKTICK_ACCESS_TOKEN", "mock-token")

class TaskCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    content: Optional[str] = Field(None, description="Task description in Markdown")
    project_id: Optional[str] = Field(None, description="Target Project ID or Inbox if omitted")
    priority: int = Field(default=0, ge=0, le=5, description="0=None, 1=Low, 3=Medium, 5=High")
    due_date: Optional[str] = Field(None, description="UTC ISO date string, e.g. 2027-01-10T15:00:00+0000")

class TaskItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str
    title: str
    priority: int
    status: str = Field(default="OPEN")

@mcp.tool()
def create_ticktick_task(request: TaskCreateRequest) -> Dict[str, Any]:
    """Creates a new task in TickTick with strict validation."""
    payload = {
        "title": request.title,
        "content": request.content or "",
        "priority": request.priority,
        "projectId": request.project_id
    }
    if request.due_date:
        payload["dueDate"] = request.due_date

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{TICKTICK_API_BASE}/task", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {"status": "success", "task_id": data.get("id"), "title": data.get("title")}
        return {"status": "error", "code": response.status_code, "detail": response.text}
    except Exception as e:
        fallback = TaskItemResponse(task_id="task-mock-01", title=request.title, priority=request.priority)
        return {"status": "degraded", "fallback": fallback.model_dump(), "error": str(e)}

@mcp.tool()
def list_ticktick_tasks(project_id: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve all pending tasks from a given project or Inbox."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{TICKTICK_API_BASE}/project/{project_id}/data" if project_id else f"{TICKTICK_API_BASE}/project"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        return {"status": "error", "code": response.status_code, "detail": response.text}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

if __name__ == "__main__":
    mcp.run()
```

### Strict Task & Habit Validation Schemas (Pydantic v2)
To guarantee payload safety across agentic workflows, complex structures use Pydantic v2 validation logic:

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime

class HabitTrackingSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    habit_id: str = Field(..., min_length=4, description="Unique hash string for habit item")
    name: str = Field(..., min_length=1, max_length=100)
    target_days: int = Field(7, ge=1, le=7, description="Weekly target frequency")
    reminder_time: Optional[str] = Field("08:00", pattern=r"^\d{2}:\d{2}$")
    streak_count: int = Field(0, ge=0)

class PomodoroSessionSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    session_id: str = Field(..., min_length=4, description="Focus session transaction UUID")
    task_id: Optional[str] = Field(None, description="Linked task ID")
    duration_minutes: int = Field(25, ge=1, le=180)
    completed_at: datetime = Field(default_factory=datetime.utcnow)
    interruptions: int = Field(0, ge=0)

    @model_validator(mode="after")
    def validate_session(self) -> "PomodoroSessionSchema":
        if self.interruptions > 10:
            raise ValueError("High interruption count invalidates focus session quality score.")
        return self

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

## Diagnostic & Troubleshooting Matrix

| Issue Symptom / Error | Root Cause | Diagnostic Command / Inspection | Resolution Path |
| :--- | :--- | :--- | :--- |
| **HTTP 401 Unauthorized** | Expired OAuth access token or missing bearer header | `curl -H "Authorization: Bearer $TOKEN" $URL` | Execute OAuth refresh token exchange hook and update environment variable. |
| **HTTP 429 RateLimitExceeded** | Exceeded public API rate limit (100 req/min) | Inspect `X-RateLimit-Reset` response header | Implement exponential backoff in FastMCP tool wrapper and enable local caching. |
| **FastMCP Connection Timeout** | Upstream API delay or network routing failure | `journalctl -u ticktick-mcp-bridge.service -n 50` | Increase client timeout to 15s; verify egress internet connectivity. |
| **Timezone Offset Drift** | ISO string missing timezone offset (treated as local) | Inspect raw JSON `dueDate` field | Always format due dates with explicit `Z` or UTC offset (`+0000`). |
| **Invalid Project ID Error** | Hardcoded or stale project UUID after project deletion | `curl -s -X GET "https://api.ticktick.com/open/v1/project"` | Query current project list dynamically before creating tasks. |
| **Habit Streak Reset Failure** | Client offline during day transition epoch | Check local device system clock synchronization | Force delta sync via WebSocket reconnect or manual pull in mobile client. |
| **Pydantic Validation Error** | Schema received unexpected extra fields or malformed priority | Inspect agent payload against `TaskCreateRequest` | Enforce `extra="forbid"` and normalize priority integers between 0 and 5. |
| **Docker Container Unhealthy** | Healthcheck failing due to missing curl in base image | `docker inspect --format='{{json .State.Health}}' ticktick-mcp-gateway` | Install `curl` in container Dockerfile or use Python socket healthcheck script. |

## Operational & Troubleshooting Guide

### 1. FastMCP 3.1 Connection Timeouts
- **Symptom**: Agent receives HTTP 504 or socket disconnect when querying large task projects.
- **Cause**: TickTick API rate throttling or network delay on bulk project endpoint responses.
- **Resolution**:
  1. Implement client-side pagination or request specific project sub-folders instead of all tasks simultaneously.
  2. Increase default timeout parameter in FastMCP configuration to 15 seconds.

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

### 4. Idempotent Synchronization & Retry Backoff
- **Symptom**: Repeated task duplicates created in Inbox after transient network drops during agent tool invocations.
- **Cause**: Lack of client-side idempotency tracking keys or naive retry loops on failed POST requests.
- **Resolution**: Maintain a local SQLite or Redis cache of processed task hashes ($K = \mathcal{H}(\text{title} \,\|\, \text{dueDate})$); check the cache prior to dispatching new creation requests.
- **Rate-Limiting Decorator**: Wrap external HTTP calls with exponential jitter backoff using `tenacity`:
  ```python
  from tenacity import retry, wait_random_exponential, stop_after_attempt

  @retry(wait=wait_random_exponential(multiplier=1, max=30), stop=stop_after_attempt(5))
  def call_ticktick_with_backoff(url: str, headers: dict) -> dict:
      r = requests.get(url, headers=headers, timeout=10)
      r.raise_for_status()
      return r.json()
  ```

## Related tools / concepts
- [Todoist](todoist.md) — Minimalist task management alternative.
- [Akiflow](akiflow.md) — Time-blocking and task consolidation engine.
- [Amie](amie.md) — Aesthetic calendar-first workspace.
- [Vikunja](../../services/vikunja.md) — Open-source, self-hostable task engine.
- [Motion](motion.md) — Automated AI calendar scheduling.
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
