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

Key operational problems solved include:
- **Terminal & Process Fragmentation**: Replaces dozens of dangling terminal windows or background tmux sessions with a single web-based management inbox.
- **Unmonitored Agent Privilege Escalation**: Enforces mandatory human-in-the-loop (HITL) authorization gates for destructive file operations, branch pushes, or deployment actions.
- **Silent Asynchronous Failures**: Captures worker crashes, model context overflows, or API rate limit timeouts, pushing immediate diagnostic notifications to developer channels.
- **Cross-Repository Work Coordination**: Tracks agent progress across multi-repo dependencies from a single unified control plane.

## Where it fits in the stack
**Tools / Agents & Background Execution Inbox**. Pizza Bot sits on top of autonomous agent runtimes (Claude Code, Roo Code, Plandex, Agentic Workbench) to provide orchestration management, task queuing, and Human-in-the-Loop (HITL) approval UI gates.

```
+-----------------------------------------------------------------------------------+
|                            STACK ARCHITECTURE POSITION                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Engineering UI / Web Dashboard / Slack App / FastMCP 3.1 Inbox Controller   |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Pizza Bot Central Orchestrator & HITL Approval Gate Manager                 |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Asynchronous Redis / PostgreSQL Dispatch Queue & Task Scheduler             |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Ephemeral Agent Sandboxes (Docker / gVisor / OpenAPPA / K3s MicroVMs)       |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | AI Coding Runtimes (Claude Code / Roo Code / OpenCode / Plandex)              |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Asynchronous PR Review & Auto-Fixing**: Queueing automated code quality analysis and patch creation across multiple GitHub repositories.
- **Human-in-the-Loop Approval Gates**: Pausing background agent database migration scripts or deployment requests until a human operator clicks approve in the Pizza Bot inbox.
- **Fleet Monitoring for Coding Agents**: Tracking parallel tasks dispatched to 10+ background coding agents from a single dashboard.
- **Automated Incident Remediation**: Receiving alert webhooks, dispatching triage agents, and staging suggested fixes for engineering review.
- **Dependency Migration Sweeps**: Dispatching background agents to refactor deprecated API usage across hundreds of internal repositories simultaneously.

## Strengths
- **Centralized Agent Inbox**: Unifies tasks, execution state, and approval requests into a clean web dashboard and Slack/Teams notification bot.
- **Asynchronous Task Queueing**: Queues and schedules long-running background tasks without locking local developer terminals.
- **Human-in-the-Loop (HITL) Controls**: Enforces explicit human approval steps for sensitive tool actions (e.g., git push, cloud resource provisioning).
- **FastMCP 3.1 Architecture**: Integrates natively with FastMCP agent servers and event stream webhooks.
- **Fine-Grained Audit Logging**: Records complete agent prompt/response histories, tool call logs, and human approval timestamps for security compliance.

## Limitations
- **Hosting Infrastructure**: Requires running a persistent backend server (Docker / PostgreSQL / Redis) for the inbox task queue.
- **Agent Protocol Integration**: Optimal monitoring requires agents to implement Pizza Bot state reporting endpoints or open telemetry hooks.
- **Approval Bottlenecks**: High volume background agent tasks can accumulate in the inbox if human reviewers become overloaded with approval requests.

## When to use it
- When orchestrating fleets of background AI agents working asynchronously on multi-repository software engineering tasks.
- When team workflow standards require explicit human review and approval before background agents can modify production code or infrastructure.
- When replacing fragmented terminal windows with a unified agent management dashboard.
- When establishing centralized security compliance oversight for AI agent tool executions across software development teams.

## When not to use it
- When executing short, single-turn interactive CLI prompts where real-time terminal output is sufficient.
- When building lightweight single-file scripts that do not require asynchronous task queuing or team collaboration.

## Architectural Deep Dive & Asynchronous Execution Pipeline

Pizza Bot unifies background agent lifecycle management using an event-driven architecture designed to scale across teams:

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

### Core Architecture Components

1. **Central Asynchronous Task Queue**: Ingests incoming task requests from webhooks, Slack commands, or API calls, assigning priorities and tracking job status.
2. **Ephemeral Execution Runtime**: Dispatches agent tasks to isolated runtime containers (Docker, gVisor, Kubernetes) for background processing.
3. **Human Approval Gate Controller**: Intercepts high-risk tool calls requested by agents (e.g., `git_push`, `delete_resource`, `db_migrate`) and posts interactive approval cards to the Pizza Bot inbox.
4. **Real-time Inbox Stream**: Pushes state updates, execution logs, and interactive approval buttons to developer interfaces via WebSockets or FastMCP SSE channels.

```
+---------------------------------------------------------------------------------------------------+
|                                  PIZZA BOT WORKFLOW STATE TRANSITIONS                             |
+-------------------+-------------------------------------------------------------------------------+
| State             | Description                                                                   |
+-------------------+-------------------------------------------------------------------------------+
| `queued`          | Task received and validated; awaiting worker allocation in Redis queue        |
| `executing`       | Sandbox container allocated; agent actively generating code and issuing tools |
| `paused_hitl`     | Sensitive tool call intercepted; execution frozen awaiting human button click |
| `approved`        | Human reviewer authorized tool action; execution resumed in sandbox          |
| `rejected`        | Human reviewer denied action; agent notified to attempt alternative strategy   |
| `completed`       | Task completed successfully; PR staged or issue updated                       |
| `failed`          | Unhandled exception or sandbox timeout occurred                               |
+-------------------+-------------------------------------------------------------------------------+
```

## Getting started

### Deployment with Docker Compose

Launch the Pizza Bot backend server using Docker Compose:

```bash
# Clone Pizza Bot repository
git clone https://github.com/pizzabot-ai/pizza-bot.git
cd pizza-bot

# Configure environment secrets
cp .env.example .env
nano .env

# Start background inbox service, PostgreSQL, Redis, and Web UI
docker compose up -d

# Verify server running on port 3000
curl http://localhost:3000/api/v1/health
```

## CLI examples

```bash
# Submit a background coding job to Pizza Bot inbox
pizza-cli submit \
  --repo "org/app" \
  --task "Refactor authentication middleware to use JWT v2" \
  --assignee "claude-agent" \
  --priority "high"

# List active background tasks in Pizza Bot queue
pizza-cli tasks list --status paused_hitl

# Inspect details and logs of a paused agent task
pizza-cli tasks inspect task-9042

# Approve a paused agent action from terminal
pizza-cli approve --task-id task-9042 --comment "Approved database schema migration."
```

## Production Deployment & Systemd Unit Configuration

To run the Pizza Bot agent orchestrator daemon on a dedicated management host, configure the following systemd service unit.

### Systemd Service Unit Configuration (`/etc/systemd/system/pizzabot.service`)

```ini
[Unit]
Description=Pizza Bot Agent Orchestration Inbox Service (FastMCP 3.1)
After=network.target docker.service postgresql.service redis.service
Requires=docker.service postgresql.service redis.service
Documentation=https://github.com/pizzabot-ai/pizza-bot

[Service]
Type=simple
User=pizzabot
Group=pizzabot
WorkingDirectory=/opt/pizzabot
Environment="NODE_ENV=production"
Environment="PORT=3000"
Environment="DATABASE_URL=postgresql://pizzabot:secret@localhost:5432/pizzabot_db"
Environment="REDIS_URL=redis://localhost:6379/0"

ExecStart=/usr/bin/node /opt/pizzabot/dist/main.js
ExecReload=/bin/kill -HUP $MAINPID

Restart=always
RestartSec=5
MemoryMax=2G
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
systemctl daemon-reload
systemctl enable --now pizzabot.service
systemctl status pizzabot.service
```

## API examples

### FastMCP 3.1 Controller & Pydantic v2 Task Inbox Service
The following Python script implements a **FastMCP 3.1** controller for managing the Pizza Bot task inbox with **Pydantic v2** validation.

```python
import os
import logging
from typing import Optional, List, Dict, Any
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

class TaskInboxStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = Field(..., description="System health status")
    active_background_jobs: int = Field(..., description="Count of currently executing tasks")
    pending_human_approvals: int = Field(..., description="Count of tasks paused at HITL gates")
    completed_today: int = Field(..., description="Tasks finished successfully in last 24h")
    connected_agents: List[str] = Field(..., description="Registered agent runtimes")

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

    res = TaskInboxStatus(
        status="online",
        active_background_jobs=4,
        pending_human_approvals=1,
        completed_today=28,
        connected_agents=["claude-code-bot", "roo-code-worker-1", "openappa-sandbox"]
    )

    return res.model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

```
+-------------------------------------------------------------------------------------------------------------------------+
|                                    PIZZA BOT DIAGNOSTIC & TROUBLESHOOTING MATRIX                                        |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Symptom / Error                    | Root Cause                         | Remediation Action                            |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Tasks remain in `queued` status    | Redis background worker daemon is  | Inspect worker logs (`docker compose logs -f  |
| indefinitely                       | offline or max worker limit hit    | worker`) and verify Redis connection          |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Webhook approvals fail with 401    | Invalid or expired HMAC signature  | Verify `WEBHOOK_SECRET` environment setting   |
| Unauthorized error                 | token in GitHub/Slack webhook spec | matches incoming webhook header secret        |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Agent sandbox containers crash     | Memory limit exceeded during heavy | Increase memory allocations in compose file   |
| with OOM Killed status             | code parsing or test execution     | or configure gVisor swap limits               |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Paused HITL tasks missing in Slack | Slack bot token lost websocket     | Restart Pizza Bot Slack adapter daemon or     |
| notification channels              | connection to Slack API gateway    | execute `pizza-cli notifications reconnect`   |
+------------------------------------+------------------------------------+-----------------------------------------------+
```

## Integration patterns
- **GitHub Actions Webhook Bridge**: Post CI failure logs to Pizza Bot inbox to automatically trigger background diagnostic agents.
- **Slack HITL Approval Bot**: Connect Pizza Bot webhooks to Slack interactive blocks, allowing developers to approve agent PRs with a single tap.
- **Vikunja MCP Integration**: Sync task execution statuses between Pizza Bot agent inbox and [Vikunja MCP](../automation_orchestration/vikunja-mcp.md) project boards.

## Best practices & Security
- **Granular Approval Scenarios**: Require human approval specifically for file modifications, git commits, and shell command execution.
- **Isolated Sandbox Execution**: Run background agents inside isolated containers managed by OpenAPPA or Docker sandboxes to isolate environment dependencies.
- **Role-Based Authorization**: Restrict HITL approval privileges in the Pizza Bot web inbox to authorized repository maintainers.

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
    print("Pizza Bot Pydantic v2 schema validation passed successfully.")

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
