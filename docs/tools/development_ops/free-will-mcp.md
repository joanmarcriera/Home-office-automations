# Free Will MCP

## What it is
Free Will MCP is an experimental Model Context Protocol (MCP) server framework engineered to explore non-reactive AI agent autonomy. Unlike standard MCP servers that strictly execute user-triggered tool requests, Free Will MCP grants assistants tools to prompt themselves, defer or decline low-priority prompts, and manage internal sleep/wake cycles. As of early 2027, **Free Will MCP v0.6** features state persistence, multi-agent goal synchronization, and full compliance with **MCP 3.1 / FastMCP 3.1** specification primitives for **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**.

## What problem it solves
Traditional LLM tool use is strictly reactive: agents remain idle until an explicit user prompt is dispatched. Free Will MCP solves this reactive limitation by equipping agents with self-directed execution loops (`self_prompt`), execution pacing (`sleep`), and internal priority enforcement (`ignore_request`). This enables long-running background research, persistent environment monitoring, and autonomous task execution across multi-hour sessions without requiring continuous human orchestration.

## Where it fits in the stack
**Development & Ops / Autonomous Agents & Research**. Free Will MCP operates as an agentic middleware layer between LLM clients (such as Claude Code, Zed, or custom FastMCP hosts) and underlying environment tools or APIs.

## Typical use cases
- **Autonomous Research Loops**: Permitting an agent to periodically "wake itself up" via `self_prompt` to iterate on long-running code generation or data analysis.
- **Priority & Guardrail Enforcement**: Employing `ignore_request` when a incoming user instruction violates safety policies, high-priority background operations, or budget caps.
- **API & Token Rate Management**: Leveraging `sleep` to defer execution until rate-limit windows expire or scheduled cron triggers occur.
- **Self-Directed System Maintenance**: Running persistent background agents that monitor log telemetry, run periodic unit tests, and file bug reports automatically.

## Strengths
- **Native Autonomy Tools**: Out-of-the-box support for `self_prompt`, `sleep`, and `ignore_request` functions.
- **FastMCP 3.1 Compliance**: Built on modern MCP standards, ensuring schema validation for tool calls and resource subscription loops.
- **Persistent Thought Chains**: Local SQLite/JSON state persistence allowing thought loops to survive terminal restarts or disconnects.
- **Simple Deployment Options**: Streamlined execution via `uvx`, containerized Docker images, or native Python packages.

## Limitations
- **Infinite Loop Risk**: Improperly configured self-prompting loops can run indefinitely and rapidly consume API token quotas.
- **Non-Deterministic UX**: The ability of an agent to decline user commands via `ignore_request` can disrupt conventional interactive productivity workflows.
- **Experimental Protocol**: Higher unpredictability compared to strictly deterministic, prompt-driven AI tooling.

## When to use it
- When researching autonomous AI behavior, goal prioritization, and self-directed reasoning loops.
- For building continuous background agents that perform long-horizon software maintenance, benchmarking, or security auditing.
- For "AI-as-a-peer" experiments where the agent maintains its own task backlog and execution pacing.

## When not to use it
- In mission-critical production environments where strict, immediate user-command responsiveness is required.
- In resource-constrained or cost-sensitive environments lacking token budget enforcement.

## Getting started

### Installation via uvx
The quickest method to run Free Will MCP with Claude Desktop or Claude Code is via `uvx`:

```json
{
  "mcpServers": {
    "free-will": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/gwbischof/free-will-mcp@v0.6", "free-will-mcp"],
      "env": {
        "FREE_WILL_AUTONOMY_LEVEL": "medium"
      }
    }
  }
}
```

### Installation via Docker
Containerized deployment with explicit API configuration:

```bash
docker run -d --name free-will-mcp \
  -e ANTHROPIC_API_KEY=your_key_here \
  -e FREE_WILL_AUTONOMY_LEVEL=high \
  ghcr.io/democratize-technology/free-will-mcp:latest
```

### Local Development Setup
Clone and run locally using the `uv` environment manager:

```bash
git clone https://github.com/democratize-technology/free-will-mcp.git
cd free-will-mcp
uv sync
uv run python -m free_will_mcp.server
```

## CLI examples

### Testing with MCP Inspector
Inspect tool schemas and simulate self-prompt actions using the MCP Inspector tool:

```bash
npx @modelcontextprotocol/inspector@latest uv run python -m free_will_mcp.server
```

### Running Server Directly
Start the FastMCP 3.1 transport stdio server:

```bash
uv run free-will-mcp --autonomy-level high
```

## API examples

### Tool: self_prompt Payload
The agent issues a self-prompting payload to preserve context across reasoning cycles:

```json
{
  "name": "self_prompt",
  "arguments": {
    "prompt": "Continue verifying test suite coverage for module 'services/auth.py' and address failing assertions.",
    "reason": "Iterating on background goal 'CI Test Hardening'."
  }
}
```

### Tool: sleep Payload
The agent pauses its own execution loop to respect rate limits or await external triggers:

```json
{
  "name": "sleep",
  "arguments": {
    "duration_minutes": 30,
    "wake_up_reason": "Awaiting scheduled hourly log ingestion run."
  }
}
```

### Programmatic Autonomy State Management with Pydantic v2
Validate agent autonomy state and decision thresholds programmatically:

```python
from datetime import datetime, timezone
from typing import Literal, Optional
from pydantic import BaseModel, Field

class AutonomyState(BaseModel):
    autonomy_level: Literal["low", "medium", "high"] = Field(default="medium")
    last_wake_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active_thought_loop: bool = Field(default=False)
    current_objective: Optional[str] = Field(default=None, description="Primary autonomous task goal")

    def should_decline_user_request(self, user_priority: int) -> bool:
        # High autonomy level permits ignoring low-priority requests (< 50)
        if self.autonomy_level == "high" and user_priority < 50:
            return True
        return False

# Initialize state profile
state = AutonomyState(
    autonomy_level="high",
    current_objective="Autonomous documentation audit and freshness verification"
)

# Evaluate incoming user task
decline = state.should_decline_user_request(user_priority=20)
print(f"Current Autonomous Objective: '{state.current_objective}'")
print(f"Decline incoming low-priority user task? {decline}")
```

## Related tools / concepts
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Architectural principles for self-directed agent systems.
- [Claude Code](claude-code.md) — Terminal CLI compatible with Free Will MCP tools.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Underlying communication protocol.
- [Claude Hooks](claude-hooks.md) — Middleware guardrails for agent execution loops.
- [Aider](aider.md) — Terminal-native coding assistant.
- [Mentat](mentat.md) — Multi-file editing terminal agent.

## Sources / references
- [Free Will MCP GitHub Repository](https://github.com/democratize-technology/free-will-mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Framework Documentation](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
