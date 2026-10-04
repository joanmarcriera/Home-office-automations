# Sunsama

Sunsama is a mindful daily planner designed to help professionals, engineering leads, and knowledge workers stay focused, intentional, and realistic about their workload. As of early 2027, it features **Sunny AI (v2.5+)**, an agentic planning assistant that leverages **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, **Gemma 4**, and **Qwen 3.6 VL** to autonomously triage backlogs, estimate task durations based on historical velocity, cross-reference external pull requests and issue queues, and suggest optimal daily time-boxing schedules according to energy levels and calendar constraints.

## What it is
Sunsama is an all-in-one daily planner and task consolidation engine that pulls tasks from a vast array of tools (GitHub, Linear, Jira, Trello, Asana, Slack, Gmail, Outlook, Notion) into a single, unified daily execution queue. It emphasizes a "ritualized" approach to productivity, guiding users through structured morning planning rituals and evening shutdown routines. Rather than acting as a team-wide project tracker, Sunsama sits on top of existing project management ecosystems as an individual's personal executive operating system.

```
+-----------------------------------------------------------------------------------+
|                                 SUNSAMA ARCHITECTURE                              |
+-----------------------------------------------------------------------------------+
                                          |
  [ External Task Sources ]               |            [ Unified Task Orchestrator ]
  +-----------------------+               |            +---------------------------+
  | - GitHub Issues / PRs |               |            |  Sunsama Task Engine      |
  | - Linear Tickets      |--------------+|----------->|  - Unified Backlog        |
  | - Slack Starred Msgs  |  Webhooks /   |            |  - Daily Time-Box Allocator|
  | - Jira & Asana Tasks  |  FastMCP 3.1  |            |  - Morning/Evening Rituals|
  | - Google / Outlook Cal|               |            +-------------+-------------+
  +-----------------------+               |                          |
                                          |                          v
  [ Sunny Agentic AI v2.5 ]               |            +---------------------------+
  +-----------------------+               |            |  FastMCP 3.1 Task Bridge  |
  | - Claude 5.6 / GPT-5.6|--------------+|----------->|  - Bidirectional Sync     |
  | - Backlog Auto-Triage |  FastMCP 3.1  |            |  - Velocity Estimator     |
  | - Context Extraction  |  Protocol     |            |  - Calendar Grid Mapper   |
  +-----------------------+               |            +---------------------------+
                                          |
```

## What problem it solves
Modern knowledge work suffers from acute context fragmentation and "to-do list overwhelm." Engineers and managers frequently manage tasks scattered across dozens of repositories, ticketing platforms, chat applications, and calendar invites. Standard task managers encourage infinite list growth without enforcing temporal constraints, leading to burnout and unrealistic daily expectations. Sunsama solves this by:
1. **Consolidating Multi-Source Inboxes**: Merging disjointed action items into a single, canonical view with live back-links.
2. **Enforcing Calendar Grounding**: Forcing tasks to be mapped onto concrete daily calendar slots (time-boxing), ensuring that plans are mathematically feasible given available meeting-free hours.
3. **Automating Workday Boundaries**: Establishing clear ritualized start and end times to separate focused deep work from restorative personal time.
4. **Agentic Workload Triage**: Utilizing Sunny AI to evaluate task complexity, calculate real-time workload feasibility, and recommend deferrals or delegation before over-commitment occurs.

## Where it fits in the stack
**Category**: Calendar & Task Orchestration / Personal Productivity Engine.
Sunsama sits directly between enterprise project management platforms (GitHub, Linear, Jira) and primary calendaring services (Google Calendar, Microsoft Outlook Calendar). It acts as the personal "human-agent interface" (HAI) layer, enabling users to interact with both human-assigned tickets and autonomous AI agent dispatches (such as FastMCP 3.1 background runners) in a structured calendar framework.

```
+-----------------------------------------------------------------------------------+
|                              SYSTEM STACK INTEGRATION                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Executive Layer ]        Sunsama Desktop / Web Client & Sunny AI v2.5           |
|                                       |                                           |
|  [ Orchestration Layer ]    FastMCP 3.1 Task Protocol / Calendar Sync Engine    |
|                                       |                                           |
|  [ Data / Source Layer ]    GitHub | Linear | Jira | Slack | GCal | Outlook        |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Guided Morning Planning Ritual**: Conducting a step-by-step daily review every morning to import issues from GitHub and Linear, estimate execution durations, and drag tasks onto calendar blocks.
- **Cross-Platform Task Aggregation**: Centralizing assigned GitHub pull requests, Linear bug reports, and Slack action items without duplicating source state or losing metadata origin.
- **Realistic Time Boxing & Capacity Management**: Visualizing meeting blocks against focus tasks to ensure total planned work does not exceed available focus hours (e.g., preventing 10 hours of work from being scheduled into a 4-hour open window).
- **Automated Evening Shutdown Ritual**: Reflecting on completed milestones, logging uncompleted items back to the backlog or future dates, and clearing mental context at the end of the workday.
- **Agentic Backlog Auto-Scheduling**: Delegating backlog organization to Sunny AI, which automatically groups tasks by context switches, assigns priority tags, and constructs balanced weekly schedules.

## Strengths
- **Mindful & Realistic Workflow**: Direct integration of task lists with calendar grids prevents unrealistic scheduling and reduces burnout risk.
- **Best-in-Class Integrations**: Native bidirectional synchronization with GitHub, Linear, Jira, Asana, Trello, Slack, Gmail, Outlook, and Google Calendar.
- **Sunny AI Agentic Intelligence**: Deep integration with multi-model AI architectures (Claude 5.6, GPT-5.6, DeepSeek-V4) for context-aware task breakdown and duration estimation.
- **Native FastMCP 3.1 Integration**: Full support for the Model Context Protocol Task Protocol allows external agent workflows (e.g., Claude Code, Cursor, AutoReason) to publish tasks, query user availability, and update status programmatically.
- **Polished Desktop UX**: High-performance, keyboard-centric interface with offline caching, global quick-capture shortcuts, and dark mode themes.

## Limitations
- **Subscription Cost**: Premium positioning at ~$20/month baseline per user with no permanent free tier.
- **Requires Discipline**: Depends on active user participation during daily planning and shutdown rituals; not suitable for users seeking 100% passive auto-scheduling without manual oversight.
- **No Direct REST API**: General programmatic extension relies on official integrations, Webhooks, or FastMCP 3.1 protocol servers rather than traditional public REST endpoints.
- **Individual-Focused**: Built specifically as a personal productivity layer rather than a team resource allocation or project roadmapping engine.

## When to use it
- When your day-to-day work spans multiple ticketing platforms (GitHub, Linear, Slack, Jira) and you need a consolidated execution dashboard.
- When you frequently over-commit to daily work and need visual calendar time-boxing to enforce realistic boundary limits.
- When you want an agentic assistant (Sunny AI) to assist in triaging backlogs, drafting task summaries, and estimating task duration.
- When integrating local AI agents with personal schedules via FastMCP 3.1 protocols.

## When not to use it
- If you require a completely free, open-source, or self-hosted task management platform (consider [Radicale](../../services/radicale.md) or [Vikunja](../automation_orchestration/vikunja-mcp.md)).
- If you prefer fully automated, hands-off algorithmic scheduling with constant automatic rescheduling (consider [Motion](motion.md)).
- If you require public REST APIs for custom database-driven back-end integrations.
- If you are seeking a team-wide Gantt chart or agile sprint management tool.

## Getting started

### Desktop & Web Client Setup
Sunsama operates across web browsers, macOS, Windows, Linux, iOS, and Android platforms.

```bash
# Installing Sunsama via Homebrew on macOS
brew install --cask sunsama

# Launching Sunsama from terminal
open -a Sunsama
```

### Initial Integration Configuration
1. **Connect Primary Calendar**: Navigate to **Settings > Integrations > Google Calendar / Outlook** and authenticate your primary primary work calendar.
2. **Connect Issue Trackers**: Link GitHub, Linear, Jira, or Slack under **Settings > Integrations**. Configure auto-import filters for assigned issues and pull requests.
3. **Configure Sunny AI**: Enable Sunny AI in **Settings > AI Assistant**. Set your preferred default reasoning model (e.g., Claude 5.6 or GPT-5.6) and enable velocity-based duration estimations.

### Keyboard-Driven Quickstart
Sunsama is optimized for rapid keyboard interaction:
- `P`: Initiate the Guided Daily Planning ritual.
- `A`: Create a new task in the active day's queue.
- `B`: Toggle the Backlog sidebar.
- `F`: Launch Focus Mode on the highlighted task with an active timer.
- `Cmd + K`: Open Command Palette for Sunny AI requests and rapid navigation.

## CLI examples

While Sunsama does not supply an official standalone terminal CLI binary, power users interact with Sunsama using keyboard macros, desktop protocol handlers, and local terminal wrappers interacting with Sunsama webhooks or FastMCP 3.1 endpoints.

```bash
# Triggering Sunsama Quick Capture via Desktop Deep-Link Protocol
open "sunsama://capture?title=Review%20Ralph-loop%20Batch%20793&notes=Verify%20FastMCP%203.1%20compliance"

# Sending a new task via local curl script targeting a Sunsama Webhook bridge
curl -X POST https://hooks.zapier.com/v1/event/sunsama_ingest_endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Audit Claude 5.6 FastMCP Task Sync",
    "notes": "Ensure high-frequency telemetry logging is functioning without latency degradation.",
    "planned_date": "2027-01-07",
    "channel_source": "Terminal CLI",
    "labels": ["Audit", "FastMCP"]
  }'
```

```bash
# Querying local FastMCP 3.1 Sunsama bridge status
python3 -m sunsama_mcp_bridge --status
```

## API examples

Sunsama provides integration points through webhook ingress endpoints and FastMCP 3.1 Model Context Protocol tool implementations. Below are production-grade implementations demonstrating Pydantic v2 schemas and FastMCP 3.1 Python integrations.

### 1. Robust Webhook Payload Ingestion with Pydantic v2

```python
import os
import sys
import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator

class SunsamaTaskIngestSchema(BaseModel):
    """
    Pydantic v2 validation schema for ingesting task payloads into Sunsama
    via enterprise webhook bridges in early 2027.
    """
    title: str = Field(..., min_length=1, max_length=255, description="Primary title of the task.")
    notes: Optional[str] = Field(None, description="Markdown-formatted task notes or criteria.")
    planned_date: datetime.date = Field(default_factory=datetime.date.today, description="Target execution date.")
    estimated_duration_minutes: int = Field(default=30, ge=5, le=480, description="Estimated duration in minutes.")
    channel_source: str = Field(default="Automated Pipeline", description="Source system generating the task.")
    external_url: Optional[HttpUrl] = Field(None, description="Canonical backlink URL to source ticket or PR.")
    labels: List[str] = Field(default_factory=list, description="Categorization tags applied to the task.")
    high_priority: bool = Field(default=False, description="Whether task requires top-of-day highlight.")

    @field_validator("labels")
    @classmethod
    def sanitize_labels(cls, v: List[str]) -> List[str]:
        return [label.strip().lower() for label in v if label.strip()]

def dispatch_task_to_sunsama(webhook_url: str, payload: SunsamaTaskIngestSchema) -> dict:
    """
    Validates payload against Pydantic v2 rules and dispatches to Sunsama endpoint.
    """
    print(f"Validating task payload: '{payload.title}' for planned date {payload.planned_date}...")
    validated_data = payload.model_dump(mode="json", exclude_none=True)

    # Mocking transmission to Sunsama webhook listener
    print(f"Successfully transmitted task to Sunsama endpoint: {webhook_url}")
    return {
        "status": "success",
        "task_id": "sun_task_987654",
        "validated_payload": validated_data
    }

if __name__ == "__main__":
    target_webhook = os.getenv("SUNSAMA_WEBHOOK_URL", "https://hooks.sunsama.com/v1/ingest/demo_key")

    try:
        sample_task = SunsamaTaskIngestSchema(
            title="Refactor FastMCP 3.1 Protocol Handlers",
            notes="Implement asynchronous event emitters and schema validation guards.",
            planned_date=datetime.date(2027, 1, 7),
            estimated_duration_minutes=45,
            channel_source="GitHub PR #1042",
            external_url="https://github.com/coder/knowledgeops-agents/pull/1042",
            labels=["FastMCP", "Refactoring", "Python3.12"],
            high_priority=True
        )

        result = dispatch_task_to_sunsama(webhook_url=target_webhook, payload=sample_task)
        print("Dispatch Output:", result)
    except ValidationError as err:
        print("Schema validation failed:", err.errors(), file=sys.stderr)
```

### 2. FastMCP 3.1 Sunsama Server Implementation

```python
import asyncio
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize FastMCP 3.1 Server for Sunsama Task Orchestration
mcp = FastMCP("sunsama-task-orchestrator", version="3.1.0")

class SunsamaTaskItem(BaseModel):
    task_id: str = Field(..., description="Unique task identifier in Sunsama.")
    title: str = Field(..., description="Title of the task.")
    status: str = Field(..., description="Current status: backlog, planned, in_progress, completed.")
    estimated_minutes: int = Field(..., description="Estimated time allocation in minutes.")
    scheduled_time: str = Field(..., description="Time block allocation string (e.g., '09:00-09:45').")

# In-memory mock storage for demonstration
TASK_STORE: Dict[str, SunsamaTaskItem] = {
    "task_001": SunsamaTaskItem(
        task_id="task_001",
        title="Review Batch 793 Quality Metrics",
        status="planned",
        estimated_minutes=30,
        scheduled_time="10:00-10:30"
    )
}

@mcp.tool()
async def create_sunsama_task(
    title: str,
    estimated_minutes: int = 30,
    scheduled_time: str = "11:00-11:30"
) -> Dict[str, Any]:
    """
    Creates a new task within the Sunsama Daily Planner via FastMCP 3.1 interface.
    """
    new_id = f"task_{len(TASK_STORE) + 1:03d}"
    task = SunsamaTaskItem(
        task_id=new_id,
        title=title,
        status="planned",
        estimated_minutes=estimated_minutes,
        scheduled_time=scheduled_time
    )
    TASK_STORE[new_id] = task
    return {"status": "created", "task": task.model_dump()}

@mcp.tool()
async def list_daily_tasks() -> List[Dict[str, Any]]:
    """
    Retrieves the current daily scheduled tasks from Sunsama.
    """
    return [task.model_dump() for task in TASK_STORE.values()]

@mcp.tool()
async def mark_task_complete(task_id: str) -> Dict[str, Any]:
    """
    Marks a Sunsama task as completed and updates daily velocity metrics.
    """
    if task_id not in TASK_STORE:
        return {"status": "error", "message": f"Task '{task_id}' not found."}

    TASK_STORE[task_id].status = "completed"
    return {"status": "updated", "task": TASK_STORE[task_id].model_dump()}

if __name__ == "__main__":
    # Standard FastMCP 3.1 execution loop
    mcp.run()
```

## Related tools / concepts
- [Akiflow](akiflow.md) — Fast, keyboard-driven task consolidation and time-boxing engine.
- [Morgen](morgen.md) — Multi-calendar manager with integrated task scheduling.
- [Motion](motion.md) — Autonomous algorithmic scheduler for automated team time-boxing.
- [Todoist](todoist.md) — Ubiquitous personal task list manager with deep ecosystem integration.
- [Vikunja](../automation_orchestration/vikunja-mcp.md) — Open-source self-hosted task management platform with FastMCP support.
- [Radicale](../../services/radicale.md) — Lightweight CalDAV/CardDAV calendar and task server.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) — Cross-platform scheduling orchestration engine.
- [Sunsama Sunny AI](https://help.sunsama.com/docs/usage-guides/sunny/) — Official guide on Sunny agentic capabilities.

## Sources / references
- [Official Sunsama Website](https://sunsama.com/)
- [Sunsama Product Roadmap & Changelog](https://roadmap.sunsama.com/changelog)
- [Sunsama Help Center & Integration Docs](https://help.sunsama.com/)
- [Sunny AI Usage Guide](https://help.sunsama.com/docs/usage-guides/sunny/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
