# Pizza Bot

## What it is
Pizza Bot is an open-source, background agent orchestration platform designed as an unified "inbox" for managing asynchronous, multi-step AI tasks. Built for software engineering teams and automated operations, Pizza Bot captures long-running agent jobs—such as background refactoring, automated PR reviews, dependency updates, and continuous integration diagnostics—and aggregates their inputs, execution status, and human approval requests into a single stream. In 2027, Pizza Bot acts as an intelligent control room for supervising fleets of background autonomous agents.

```
+-----------------------------------------------------------------------------------+
|                            PIZZA BOT AGENT INBOX                                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Incoming Tasks      | ----> | Asynchronous Dispatch | ---> | Agent Execution | |
|  | (Webhook / GitHub)  |       | & Queue Controller    |      | Sandboxes       | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | FastMCP 3.1 Gateway | <---- | Human-in-the-Loop     | <--- | Central Agent   | |
|  | Webhook / Slack UI  |       | Approval Dashboard    |      | Status Inbox    | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing multiple background AI agents operating across different repositories and cloud environments leads to fragmented tracking, lost context, and unmonitored agent actions. Without centralized supervision, long-running agent tasks either fail silently or execute risky actions without human verification. Pizza Bot addresses this by unifying background agent lifecycle management into an interactive dashboard and API inbox where developers can monitor execution logs, review proposed code changes, and approve high-stakes actions before merge.

## Where it fits in the stack
**Tools / Agents & Background Execution Inbox**. Pizza Bot sits on top of autonomous agent runtimes (Claude Code, Roo Code, Plandex, Agentic Workbench) to provide orchestration management, task queuing, and Human-in-the-Loop (HITL) approval UI gates.

## Typical use cases
- **Asynchronous PR Review & Auto-Fixing**: Queueing automated code quality analysis and patch creation across multiple GitHub repositories.
- **Human-in-the-Loop Approval Gates**: Pausing background agent database migration scripts or deployment requests until a human operator clicks approve in the Pizza Bot inbox.
- **Fleet Monitoring for Coding Agents**: Tracking parallel tasks dispatched to 10+ background coding agents from a single dashboard.
- **Automated Incident Remediation**: Receiving alert webhooks, dispatching triage agents, and staging suggested fixes for engineering review.

## Strengths
- **Centralized Agent Inbox**: Unifies tasks, execution state, and approval requests into a clean web dashboard and Slack/Teams notification bot.
- **Asynchronous Task Queueing**: Queues and schedules long-running background tasks without locking local developer terminals.
- **Human-in-the-Loop (HITL) Controls**: Enforces explicit human approval steps for sensitive tool actions (e.g., git push, cloud resource provisioning).
- **FastMCP 3.1 Architecture**: Integrates natively with FastMCP agent servers and event stream webhooks.

## Limitations
- **Hosting Infrastructure**: Requires running a persistent backend server (Docker / PostgreSQL) for the inbox task queue.
- **Agent Protocol Integration**: Optimal monitoring requires agents to implement Pizza Bot state reporting endpoints.

## When to use it
- When orchestrating fleets of background AI agents working asynchronously on multi-repository software engineering tasks.
- When team workflow standards require explicit human review and approval before background agents can modify production code or infrastructure.
- When replacing fragmented terminal windows with a unified agent management dashboard.

## When not to use it
- When executing short, single-turn interactive CLI prompts where real-time terminal output is sufficient.
- When building lightweight single-file scripts that do not require asynchronous task queuing or team collaboration.

## Architecture & Technical Deep Dive

Pizza Bot unifies background agent lifecycle management using an event-driven architecture:

```
                         PIZZA BOT ARCHITECTURE PIPELINE

    Task Triggers (GitHub Webhooks, Slack Messages, Scheduled Cron)
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Central Asynchronous Queue   │  <--- Redis / PostgreSQL Task Dispatcher
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Ephemeral Agent Executor     │  <--- Sandboxed Container Execution
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Human Approval Gate Controller│ <--- Pauses Execution for Sensitive Actions
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ FastMCP 3.1 Controller UI    │  <--- Real-Time WebSocket / SSE Inbox Stream
     └──────────────────────────────┘
```

1. **Central Asynchronous Task Queue**: Ingests incoming task requests from webhooks, Slack commands, or API calls, assigning priorities and tracking job status.
2. **Ephemeral Execution Runtime**: Dispatches agent tasks to isolated runtime containers (Docker, Kubernetes, microVMs) for background processing.
3. **Human Approval Gate Controller**: Intercepts high-risk tool calls requested by agents (e.g., `git_push`, `delete_resource`) and posts approval cards to the Pizza Bot inbox.
4. **Real-time Inbox Stream**: Pushes state updates, execution logs, and interactive approval buttons to developer interfaces via WebSockets or FastMCP SSE channels.

## Getting started

Launch the Pizza Bot backend server using Docker Compose and connect your agent framework:

```bash
# Clone Pizza Bot repository
git clone https://github.com/pizzabot-ai/pizza-bot.git
cd pizza-bot

# Start background inbox service and Web UI
docker compose up -d

# Verify server running on port 3000
curl http://localhost:3000/api/health
```

## CLI examples

```bash
# Submit a background coding job to Pizza Bot inbox
pizza-cli submit --repo "org/app" --task "Refactor authentication middleware to use JWT v2" --assignee "claude-agent"

# List active background tasks in Pizza Bot queue
pizza-cli tasks list --status pending-approval

# Approve a paused agent action from terminal
pizza-cli approve --task-id task-9042 --comment "Approved database schema migration."
```

## API examples

### FastMCP 3.1 Controller & Pydantic v2 Task Inbox Service
The following Python script implements a **FastMCP 3.1** controller for managing the Pizza Bot task inbox with **Pydantic v2** validation.

```python
import os
import logging
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PizzaBot-InboxController")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("pizza-bot-inbox")

# Pydantic v2 Task Submission Schema
class AgentTaskSubmission(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=3, max_length=200, description="Task summary or PR review title")
    repository: str = Field(..., description="Target repository (e.g., org/repo-name)")
    assigned_agent: str = Field(default="auto-assigned", description="Target agent runtime (claude-code, roo-code, custom)")
    priority: str = Field(default="medium", description="Task priority (low, medium, high, critical)")
    require_human_approval: bool = Field(default=True, description="Whether sensitive tool actions require HITL check")
    payload: Dict[str, str] = Field(default_factory=dict, description="Task execution context parameters")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        valid = ["low", "medium", "high", "critical"]
        if v.lower() not in valid:
            raise ValueError(f"Priority must be one of {valid}")
        return v.lower()

@mcp.tool()
async def submit_task_to_inbox(
    task_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Submits a new background agent job into Pizza Bot inbox queue.

    Args:
        task_dict: Task payload matching AgentTaskSubmission.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating task payload with Pydantic v2...")

    try:
        task = AgentTaskSubmission.model_validate(task_dict)
        if ctx:
            await ctx.info(f"Submitting '{task.title}' for repo '{task.repository}' (Priority: {task.priority})...")

        return {
            "status": "queued",
            "task_id": "task-b882-9901",
            "title": task.title,
            "repository": task.repository,
            "assigned_agent": task.assigned_agent,
            "human_approval_required": task.require_human_approval,
            "inbox_url": "http://localhost:3000/inbox/task-b882-9901"
        }
    except ValidationError as ve:
        logger.error(f"Task validation failure: {ve}")
        raise ValueError(f"Invalid task submission: {ve}")

@mcp.tool()
async def query_inbox_metrics(ctx: Optional[Context] = None) -> dict:
    """Queries active Pizza Bot task counts, pending HITL approvals, and worker health."""
    if ctx:
        await ctx.info("Fetching Pizza Bot inbox status...")

    return {
        "status": "online",
        "active_background_jobs": 4,
        "pending_human_approvals": 1,
        "completed_today": 28,
        "connected_agents": ["claude-code-bot", "roo-code-worker-1", "openappa-sandbox"]
    }

if __name__ == "__main__":
    mcp.run()
```

## Integration patterns
- **GitHub Actions Webhook Bridge**: Post CI failure logs to Pizza Bot inbox to automatically trigger background diagnostic agents.
- **Slack HITL Approval Bot**: Connect Pizza Bot webhooks to Slack interactive blocks, allowing developers to approve agent PRs with a single tap.

## Best practices & Security
- **Granular Approval Scenarios**: Require human approval specifically for file modifications, git commits, and shell command execution.
- **Isolated Sandbox Execution**: Run background agents inside isolated containers managed by OpenAPPA or Docker sandboxes to isolate environment dependencies.

## Reference implementation

```python
# Standalone test for Pizza Bot Pydantic v2 validation
from pydantic import ValidationError

def test_pizza_bot_schema():
    payload = {
        "title": "Fix security vulnerability in auth middleware",
        "repository": "my-company/backend-service",
        "priority": "high",
        "require_human_approval": True
    }
    task = AgentTaskSubmission.model_validate(payload)
    assert task.title == "Fix security vulnerability in auth middleware"
    assert task.priority == "high"
    print("Pizza Bot schema test passed successfully.")

if __name__ == "__main__":
    test_pizza_bot_schema()
```

## Related tools / concepts
- [OpenAPPA](openappa.md) — Security framework for sandboxing agent tool execution.
- [Claude Code](../development_ops/claude-code.md) — CLI coding agent backend.
- [Docker Sandbox](../infrastructure/docker.md) — Ephemeral agent container execution.
- [Vikunja MCP](../automation_orchestration/vikunja-mcp.md) — Task management integration.

## Sources / references
- [Pizza Bot Agent Inbox Announcement](https://www.infoq.com/news/2026/10/pizza-bot-ai-agents/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=AI%2C+ML+%26+Data+Engineering)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
