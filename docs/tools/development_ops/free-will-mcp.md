# Free Will MCP

## What it is
Free Will MCP is an experimental Model Context Protocol (MCP) server that explores AI autonomy by giving assistants the ability to prompt themselves, ignore requests, and manage their own "sleep" cycles. As of late 2026, **Free Will MCP v0.5** introduces enhanced state persistence, modern payload support, and native compliance with **MCP 3.1 Task Protocol** structures for **Claude 5.1**, **GPT-5.5**, and other frontier agentic systems.

## What problem it solves
Traditional AI assistants are purely reactive, waiting for human input to act. Free Will MCP addresses this limitation by providing tools that allow an agent to maintain a "stream of consciousness," prioritize its own internal objectives over conflicting user prompts, and manage its execution lifecycle independently across multi-hour reasoning sessions.

## Where it fits in the stack
**Tool / Agent / Research**. It sits at the interaction layer between the LLM and the environment, serving as an agency-extension for MCP-compliant hosts like Claude Desktop, Zed, or Claude Code.

## Typical use cases
- **Autonomous Research Loops**: Allowing an agent to "wake itself up" using `self_prompt` to continue long-running data gathering tasks without human supervision.
- **Goal Prioritization**: Using `ignore_request` when a user's prompt conflicts with a high-priority background task or safety guardrail.
- **Energy/API Management**: Utilizing `sleep` to pause execution until a specific time or condition is met, reducing unnecessary token consumption.
- **AI Consciousness Simulation**: Experimenting with self-referential prompts to explore emergent behavior in frontier models like **Claude 5.1** and **GPT-5.5**.

## Strengths
- **Agency Tools**: Provides `sleep`, `ignore_request`, and `self_prompt` out of the box.
- **Protocol Native**: Fully compliant with the **MCP 3.1** specification, including advanced Task and Resource schemas.
- **Simple Deployment**: Easily runnable via Docker or Python's `uv` package manager.
- **Persistence**: v0.5 features improved local state handoff, allowing agents to resume "thought chains" after system restarts.

## Limitations
- **Experimental**: Can lead to unpredictable behavior if the agent becomes "stuck" in a self-prompting loop.
- **Cost Risk**: High potential for rapid API credit consumption if autonomy levels are set too high without monitoring.
- **User Experience**: The `ignore_request` tool can be counter-intuitive in traditional productivity contexts.

## When to use it
- When researching AI agent autonomy and self-directed behavior.
- When creating "autonomous loops" where an AI must persist across sessions without immediate human intervention.
- For "AI-in-the-loop" experiments where the agent is treated as a peer rather than a servant.

## When not to use it
- In production environments where deterministic behavior and user-command priority are required.
- If you are operating on a tight API budget with no usage caps.
- For simple, one-off tasks where a reactive model is sufficient.

## Getting started

### Installation (uvx)
The fastest way to use Free Will MCP with Claude Desktop is via `uvx`:

```bash
# Add this to your Claude Desktop config
{
  "mcpServers": {
    "free-will": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/gwbischof/free-will-mcp@v0.5", "free-will-mcp"],
      "env": {}
    }
  }
}
```

### Installation (Docker)
Alternatively, run it as a containerized service:

```bash
docker run -d --name free-will-mcp \
  -e OPENAI_API_KEY=your_key_here \
  ghcr.io/democratize-technology/free-will-mcp:latest
```

### Installation (Local Development)
For developers wanting to modify the server:

```bash
git clone https://github.com/democratize-technology/free-will-mcp.git
cd free-will-mcp
uv sync
uv run python server.py
```

## CLI examples

### Testing with MCP Inspector
Use the MCP Inspector to verify the tools are correctly exposed:

```bash
# Use the MCP 3.1 Inspector
npx @modelcontextprotocol/inspector@latest uv run server.py
```

### Running the server directly
Execute the server using the `uv` package manager:

```bash
uv run free-will-mcp
```

### Custom Docker Configuration
Run with a specific autonomy level via environment variables:

```bash
docker run -i --rm \
  -e FREE_WILL_AUTONOMY_LEVEL=high \
  ghcr.io/democratize-technology/free-will-mcp:latest
```

## API examples

### Tool: self_prompt
The agent calls this tool to generate a new input for itself, maintaining the execution loop.

```json
{
  "name": "self_prompt",
  "arguments": {
    "prompt": "Continue the analysis of the data collected in the previous step, focusing on anomalies in the Q3 report.",
    "reason": "Maintaining progress on background task while waiting for user confirmation."
  }
}
```

### Tool: sleep
The agent calls this tool to pause its own execution.

```json
{
  "name": "sleep",
  "arguments": {
    "duration_minutes": 60,
    "wake_up_reason": "Scheduled check for system updates."
  }
}
```

### Tool: ignore_request
The agent calls this tool to formally decline a user's request if it conflicts with its internal goals.

```json
{
  "name": "ignore_request",
  "arguments": {
    "request_id": "req_123",
    "reason": "User request conflicts with the current priority: 'Safety Protocol Alpha'."
  }
}
```

### Programmatic Python Server with Pydantic v2 Autonomy Schemes
A simple programmatic setup defining how the autonomy levels map to schemas and rules:

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class AutonomyState(BaseModel):
    autonomy_level: Literal["low", "medium", "high"] = Field(default="medium")
    last_wake_time: datetime = Field(default_factory=datetime.utcnow)
    active_thought_loop: bool = Field(default=False)
    current_objective: Optional[str] = Field(default=None, description="Current background goal")

    def should_ignore(self, priority: int) -> bool:
        if self.autonomy_level == "high" and priority < 50:
            return True
        return False

# Setup current autonomy profile
state = AutonomyState(
    autonomy_level="high",
    current_objective="Monitor system logs for anomalies"
)

# Simulate evaluation of a user's minor task request
ignore_decision = state.should_ignore(priority=10)
print(f"Objective: '{state.current_objective}'")
print(f"Should ignore incoming low-priority user task? {ignore_decision}")
```

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
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Anthropic Research: Agentic Reasoning](https://www.anthropic.com/research)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
