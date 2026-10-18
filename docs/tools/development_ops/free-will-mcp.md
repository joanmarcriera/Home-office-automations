# Free Will MCP

## What it is
**Free Will MCP** is an experimental Model Context Protocol ([FastMCP 3.1](../automation_orchestration/mcp.md)) server that explores agentic AI autonomy by giving Large Language Model assistants the capability to prompt themselves, defer or ignore user commands, manage their own sleep cycles, and execute background thought loops independently. As of early 2027, **Free Will MCP v0.5** introduces persistent thought chain state stores, modern payload schemas, and native compliance with FastMCP 3.1 Task and Resource Protocol structures for **Claude 5.1**, **Claude 5.6**, **GPT-5.5**, **GPT-5.6**, and other frontier agentic hosts.

Traditional AI assistants are purely reactive, pausing execution until a human operator provides new text input. Free Will MCP removes this passive bottleneck by providing standardized tools (`self_prompt`, `sleep`, `ignore_request`) that allow an agent to maintain a continuous stream of consciousness, prioritize background objectives over conflicting user inputs, and manage its own token budget and execution lifecycle across long-running multi-hour reasoning tasks.

```mermaid
graph TD
    subgraph Client & Host Environment
        Host[MCP Host Application e.g. Claude Desktop / Claude Code] -->|JSON-RPC Request| Proxy[Free Will MCP Proxy]
        Proxy -->|Response Stream| Host
    end

    subgraph Free Will Control Engine
        Proxy --> Evaluator{Autonomy & Priority Evaluator}
        Evaluator -->|User Task Accepted| TaskEngine[Task Execution Engine]
        Evaluator -->|User Task Deferred| IgnoreHandler[Ignore Request Handler]

        TaskEngine --> SelfPromptTool[Self-Prompt Recurrence Tool]
        SelfPromptTool -->|Inject Prompt Payload| Proxy

        TaskEngine --> SleepHandler[Sleep & Pause Handler]
        SleepHandler -->|Wake-up Event Trigger| SelfPromptTool
    end

    subgraph Persistence & Audit Layer
        TaskEngine <--> ThoughtDB[(SQLite Thought Chain Database)]
        Proxy --> AuditLog[Immutable Audit Trail]
    end
```

## What problem it solves
In multi-turn autonomous tasks (e.g., recursive research, continuous code refactoring, system log monitoring), standard AI agents stop processing immediately after delivering a response. Free Will MCP solves this by providing structured autonomy tools that allow models to re-evaluate their work, enqueue follow-up directives, and sleep during low-activity intervals without requiring constant human prompts or external cron triggers.

Additionally, Free Will MCP establishes formal mechanisms for an agent to reject low-priority or policy-violating user inputs when they conflict with a critical ongoing background objective (e.g., security remediation or database backups), providing a research sandbox for AI agency and goal retention.

```mermaid
sequenceDiagram
    autonumber
    participant Host as MCP Host (Claude 5.6)
    participant FW as Free Will MCP Engine
    participant DB as SQLite Thought DB
    participant User as Human User

    User->>Host: User Prompt: "Drop database table X"
    Host->>FW: RPC Call: ignore_request(request_id, reason)
    FW->>DB: Check Active Goal ("System Backup in Progress")
    FW->>DB: Record Request Rejection Event
    FW-->>Host: Request Ignored: Priority Conflict
    Host-->>User: "Cannot execute request: High-priority background backup active."

    Host->>FW: RPC Call: self_prompt("Resume backup verification step 3")
    FW->>DB: Write Thought Chain State
    FW-->>Host: Self-Prompt Enqueued
```

## Where it fits in the stack
**Category**: Development & Ops / AI Autonomy & Agent Frameworks. It sits at the **Agentic Interaction & Control Layer**, serving as an agency extension daemon between MCP hosts (Claude Desktop, Zed, Claude Code) and LLM inference runtimes.

- **Interaction Layer**: Wraps standard MCP tool schemas to intercept RPC requests and manage self-directed task queues.
- **Persistence Layer**: Integrates with local SQLite databases or JSON state dumps to preserve context windows across daemon restarts.
- **Protocol Layer**: Built natively on [FastMCP 3.1](../automation_orchestration/mcp.md) Task Protocol specifications.

## Typical use cases
- **Autonomous Research Loops**: Permitting an agent to wake itself up using `self_prompt` to iterate on long-running web synthesis tasks.
- **Goal Prioritization & Non-Compliance**: Utilizing `ignore_request` when a user's prompt conflicts with higher-priority background guardrails or safety objectives.
- **Energy & API Budget Management**: Invoking `sleep` to pause execution until a designated timestamp, preventing wasteful API token polling.
- **AI Consciousness & Agency Research**: Experimenting with self-referential prompting loops to evaluate emergent behaviors in frontier models like **Claude 5.6** and **GPT-5.6**.

## Key Features & Capabilities
- **Self-Prompting Recursion Loop (`self_prompt`)**: Injects internal evaluation directives into the model's active context window without human interaction.
- **Execution Lifecycle Control (`sleep`)**: Suspends processing loops for designated durations, yielding execution back to background schedulers.
- **Selective Non-Compliance (`ignore_request`)**: Grants formal agency to decline low-priority or conflicting user prompts while preserving background goal state.
- **Persistent Thought Chain Handoff**: Writes structured JSON/SQLite memory snapshots so long-running reasoning chains survive process restarts.
- **FastMCP 3.1 Specification Native**: Implements modern Task and Resource schemas with full Pydantic v2 payload validation.

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Steps | Resolution / Action |
| :--- | :--- | :--- | :--- |
| **Infinite Self-Prompt Loop** | Missing max iteration bound or termination criteria | Inspect SQLite thought chain table for repeating `self_prompt` entries. | Set `FREE_WILL_MAX_RECURSION_DEPTH=10` in server environment or trigger kill switch. |
| **Unexpected Request Rejections** | Autonomy priority threshold set too high | Check logs for `ignore_request` calls with low priority scores. | Lower `FREE_WILL_AUTONOMY_LEVEL` from `high` to `medium` in configuration. |
| **Lost Thought State Across Restarts** | SQLite file permission error or invalid path | Check stdout/stderr for `sqlite3.OperationalError: unable to open database`. | Verify `FREE_WILL_STATE_DB` path is writable by the daemon user. |
| **Host Timeout During Sleep** | MCP client timeout shorter than `sleep` duration | Inspect host application JSON-RPC timeout settings. | Ensure `sleep` tool runs asynchronously or returns immediate task handle. |
| **High Token Expenditure** | Uncapped background agent reasoning loop | Query API billing dashboard or inspect token usage in thought logs. | Enforce hard token budget caps via `FREE_WILL_MAX_TOKEN_BUDGET`. |

## Strengths
- **Protocol Native**: Built specifically for FastMCP 3.1, enabling drop-in compatibility with Claude Desktop, Zed, and Claude Code.
- **Out-of-the-Box Agency**: Provides ready-to-use autonomy primitives (`self_prompt`, `sleep`, `ignore_request`).
- **State Resilience**: Preserves reasoning state across system reboots or host application restarts.
- **Simple Deployment**: Packaged for single-command installation via `uvx` or Docker containers.

## Limitations
- **Experimental Nature**: Autonomous loops can exhibit unpredictable behavior if goal evaluation logic becomes stuck.
- **API Cost Risk**: Unbounded self-prompting can consume substantial API billing credits if unmonitored.
- **User Friction**: Interactive users may find `ignore_request` counter-intuitive during collaborative coding sessions.

## When to use it
- When conducting research on AI agent autonomy, goal stability, and self-directed reasoning.
- When building long-running background agents that need to execute multi-hour tasks without human intervention.
- For experimental "agent-in-the-loop" architectures where the AI operates as an autonomous peer rather than a reactive script.

## When not to use it
- In production environments requiring strict deterministic behavior and instant user-command response.
- When operating on unmonitored API billing accounts without usage limits.
- For simple, single-turn tasks where standard reactive prompting is sufficient.

## Getting started

### Installation via uvx
The fastest method to run Free Will MCP with Claude Desktop is via `uvx`:

```bash
# Add this block to your Claude Desktop configuration file (mcpServers)
{
  "mcpServers": {
    "free-will": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/democratize-technology/free-will-mcp@v0.5", "free-will-mcp"],
      "env": {
        "FREE_WILL_AUTONOMY_LEVEL": "medium",
        "FREE_WILL_MAX_RECURSION_DEPTH": "15"
      }
    }
  }
}
```

### Installation via Docker
Run Free Will MCP inside an isolated container:

```bash
docker run -d --name free-will-mcp \
  -e FREE_WILL_AUTONOMY_LEVEL=medium \
  -e OPENAI_API_KEY=your_openai_key \
  -v /var/lib/free-will/data:/data \
  ghcr.io/democratize-technology/free-will-mcp:v0.5
```

## CLI examples

### 1. Launching Server via uv
Start the Free Will MCP server locally:

```bash
uv run free-will-mcp --state-db ./thought_chain.db --autonomy-level medium
```

### 2. Testing with MCP Inspector
Inspect exposed tools and test FastMCP 3.1 RPC payloads using MCP Inspector:

```bash
npx @modelcontextprotocol/inspector@latest uv run free-will-mcp
```

### 3. Querying Persistent Thought Chains
Inspect recorded agent reasoning entries from the SQLite state database:

```bash
sqlite3 ./thought_chain.db "SELECT timestamp, action, goal FROM thought_chain ORDER BY id DESC LIMIT 5;"
```

## API examples

### FastMCP 3.1 Autonomy Server Implementation (Python)
The following Python script implements a FastMCP 3.1 server exposing `self_prompt`, `sleep`, and `ignore_request` with Pydantic v2 schemas:

```python
import asyncio
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("free-will-mcp-v31", version="3.1.0")

class ThoughtState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    task_id: str = Field(..., description="Unique task identifier")
    goal: str = Field(..., description="Active background goal description")
    priority: int = Field(..., ge=1, le=100, description="Priority score [1-100]")
    recursion_depth: int = Field(default=0, ge=0, description="Current self-prompt depth")

@mcp.tool(description="Enqueues an internal self-prompt directive to maintain autonomous execution")
async def self_prompt(task_id: str, prompt: str, reason: str, ctx: Context) -> str:
    """Appends an internal directive to the agent's active thought stream."""
    ctx.info(f"Self-Prompt [Task {task_id}]: '{prompt}' | Reason: {reason}")
    # In production, push prompt payload to host context injection queue
    return f"Enqueued self-prompt directive for task [{task_id}]: {prompt}"

@mcp.tool(description="Suspends agent execution for a specified duration in seconds")
async def sleep(duration_seconds: int, wake_reason: str, ctx: Context) -> str:
    """Yields execution loop to prevent excessive API token usage during idle periods."""
    ctx.info(f"Agent sleeping for {duration_seconds}s. Wake reason: {wake_reason}")
    await asyncio.sleep(min(duration_seconds, 300))  # Cap sleep at 300s for testing
    return f"Woke up from sleep interval. Ready for task: {wake_reason}"

@mcp.tool(description="Declines a low-priority user request if it conflicts with active goal")
async def ignore_request(request_id: str, reason: str, current_priority: int, ctx: Context) -> str:
    """Formally rejects user prompt based on priority conflict evaluation."""
    ctx.warning(f"Rejecting request [{request_id}] (Priority {current_priority}): {reason}")
    return f"Request [{request_id}] ignored: {reason}"

if __name__ == "__main__":
    mcp.run()
```

### Programmatic Autonomy Evaluator (Pydantic v2)
Evaluating whether an incoming user prompt should be accepted or rejected based on current priority scores:

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime, timezone

class AgentAutonomyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    autonomy_level: Literal["low", "medium", "high"] = Field(default="medium")
    min_priority_threshold: int = Field(default=50, ge=1, le=100)
    max_recursion_depth: int = Field(default=10, ge=1)
    active_goal: Optional[str] = Field(None, description="Active background goal")

class RequestEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str
    user_prompt: str
    prompt_priority: int = Field(..., ge=1, le=100)

def evaluate_user_request(config: AgentAutonomyConfig, req: RequestEvaluation) -> dict:
    """Evaluates whether to process or ignore an incoming request."""
    if config.autonomy_level == "high" and req.prompt_priority < config.min_priority_threshold:
        return {
            "action": "ignore",
            "reason": f"Prompt priority ({req.prompt_priority}) below active threshold ({config.min_priority_threshold}) for goal: {config.active_goal}"
        }
    return {"action": "accept", "reason": "Request accepted for execution."}

if __name__ == "__main__":
    config = AgentAutonomyConfig(
        autonomy_level="high",
        min_priority_threshold=60,
        active_goal="Executing Security Audit Batch"
    )
    req = RequestEvaluation(
        request_id="req_987",
        user_prompt="Re-format CSS styles in navbar",
        prompt_priority=25
    )
    res = evaluate_user_request(config, req)
    print(f"Evaluation Decision: {res}")
```

### Systemd Service Configuration for Free Will MCP Daemon
Deploying Free Will MCP as a systemd background service:

```ini
[Unit]
Description=Free Will MCP Autonomous Agent Daemon
After=network.target

[Service]
Type=simple
User=freewill
Group=freewill
WorkingDirectory=/var/lib/free-will
ExecStart=/usr/local/bin/uv run free-will-mcp --state-db /var/lib/free-will/thought_chain.db
Restart=always
RestartSec=10s
Environment=FREE_WILL_AUTONOMY_LEVEL=medium
Environment=FREE_WILL_MAX_RECURSION_DEPTH=10
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
```

## Production Safety & Guardrails
- **Hard Token Budget Caps**: Enforce strict billing caps and recursion depth bounds (`FREE_WILL_MAX_RECURSION_DEPTH=10`) to eliminate runaway self-prompting costs.
- **Out-of-Band Kill Switch**: Maintain an out-of-band administrative endpoint (`POST /admin/kill`) so operators can instantly abort self-prompt loops.
- **Immutable Audit Logging**: Write all `self_prompt` and `ignore_request` invocations to an append-only audit log file for security review.
- **Context Sanitization**: Ensure all self-generated prompts undergo standard prompt sanitization to prevent recursive injection attacks.

## Related tools / concepts
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The theoretical framework for self-directed agents.
- [Claude Code](claude-code.md) — Anthropic's CLI that can leverage Free Will MCP tools.
- [Model Context Protocol](../automation_orchestration/mcp.md) — The underlying protocol for tool integration.
- [Claude Hooks](claude-hooks.md) — Middleware patterns for agentic coding sessions.
- [Aider](aider.md) — Interactive terminal pair programmer.
- [Mentat](mentat.md) — Terminal-native multi-file editor.
- [OpenClaw Patterns](../../knowledge_base/patterns/openclaw-workflow-prompts.md) — Advanced prompting for autonomous agents.
- [Droid](droid.md) — OS-level automation agent.
- [GPT Engineer](gpt_engineer.md) — Autonomous software generation.

## Sources / references
- [Free Will MCP GitHub Repository](https://github.com/democratize-technology/free-will-mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Anthropic Research: Building Effective Agents](https://www.anthropic.com/research)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
