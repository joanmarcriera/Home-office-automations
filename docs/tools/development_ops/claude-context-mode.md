# Claude Context Mode

## What it is
Claude Context Mode refers to community and workflow patterns for giving Claude Code richer, better-structured operating context, often through MCP servers, repository memory files, and scoped task documents. It is the practice of "context engineering" specifically for agentic coding workflows using frontier models like **Claude 5.1** (`claude-5.1-sonnet-20261220`) and **GPT-5.5**.

## What problem it solves
It reduces prompt sprawl and makes agent behavior more repeatable than pasting large amounts of context into every session. It solves the "context window amnesia" problem by ensuring the agent has access to a durable, versioned source of truth about the project's architecture, standards, and progress. It leverages **FastMCP 3.1** to dynamically inject context as needed.

## Where it fits in the stack
**Development & Ops / Context Engineering Pattern**. It is a practical operating pattern around Claude Code, MCP, and AI-native IDEs (like Cursor 3.0 or VS Code with Continue).

## Typical use cases
- **Repository Onboarding**: Giving an agent a high-level map of a new codebase using `find_oldest_issues.py`.
- **Architectural Guardrails**: Ensuring the agent follows specific design patterns (e.g., "always use FastAPI dependency injection").
- **Task Persistence**: Resuming a complex, multi-day coding task across different chat sessions.
- **Standardized Workflows**: Using `AGENTS.md` to define repository-wide operating contracts for autonomous agents.

## Strengths
- **Consistency**: Agent behavior becomes more predictable across sessions.
- **Efficiency**: Reduces the amount of manual context pasting required.
- **Versionable**: Context files (like `MEMORY.md` or `AGENTS.md`) live in the repo and evolve with the code.
- **Native Integration**: Supported natively by **FastMCP 3.1** for dynamic context injection and resource discovery.

## Limitations
- **Maintenance Overhead**: Requires human (or agent) discipline to keep context files up to date.
- **Noise**: Poorly designed context layers can still overwhelm the model and cause "distraction" from the immediate task.
- **Staleness**: If not updated after every successful task, the agent may work against outdated progress notes.

## When to use it
- When working on complex, long-running projects where architectural consistency is critical.
- When collaborating with multiple agents or human-agent teams.
- When you need to provide the agent with external tool context via specialized MCPs like **Chronos MCP** or **Free Will MCP**.

## When not to use it
- For trivial, one-off scripts where the overhead of creating context files exceeds the task effort.
- When the task is simple enough for the agent to infer everything from local file context alone.
- If you are using a model with a very small context window (less than 32k tokens).

## Getting started

To get started with Claude Context Mode, you can install the official Claude Code CLI and set up a repository context file.

### Installation
```bash
# Install Claude Code globally via NPM
npm install -g @anthropic-ai/claude-code
```

### Hello-World Example
To bootstrap a project with persistent memory, create an `AGENTS.md` file in the repository root and launch the `claude` CLI:
```bash
# 1. Create a basic context file
echo -e "# Repository Rules\n- Use Node.js v20+\n- Write clean TypeScript" > AGENTS.md

# 2. Start Claude Code with the loaded context
claude
```

## CLI examples

Here are 3 common CLI commands to manage and inject repository context files during developer workflows.

```bash
# 1. Inject context into a single prompt execution
claude --prompt "Project context: $(cat AGENTS.md) -- Review current folder structure."

# 2. Append a newly completed feature to your progress log
claude --prompt "Task complete. Update AGENTS.md progress list with 'Authentication added'."

# 3. Serve a directory of context documents using FastMCP 3.1
uvx mcp-server-context7 --path ./docs/knowledge_base
```

## API examples

### Python (Injecting Context with Pydantic v2 Validation)
For automated pipelines, you can load, validate the project's context rules, and pass the verified context directly to the system prompt of the Anthropic SDK.

```python
import os
import anthropic
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# Define strict Pydantic v2 schemas for repository rules and context limits
class ContextRule(BaseModel):
    rule_id: str = Field(..., pattern=r"^RULE-\d{3}$")
    description: str = Field(..., min_length=10)
    severity: str = Field(..., pattern=r"^(high|medium|low)$")

class RepoContextConfig(BaseModel):
    project_name: str = Field(..., min_length=2)
    mcp_servers: List[str] = Field(default_factory=list)
    rules: List[ContextRule]
    max_context_tokens: int = Field(200000, gt=0)

    @field_validator("mcp_servers")
    @classmethod
    def validate_servers(cls, v: List[str]) -> List[str]:
        for server in v:
            if not server.startswith("mcp://") and not server.startswith("http://"):
                raise ValueError("All MCP servers must start with 'mcp://' or 'http://'")
        return v

# Load and validate context configuration payload
config_payload = {
    "project_name": "Home-Office Automation",
    "mcp_servers": ["mcp://chronos-server", "mcp://free-will-server"],
    "max_context_tokens": 200000,
    "rules": [
        {"rule_id": "RULE-001", "description": "Always follow standards.md schema structures.", "severity": "high"},
        {"rule_id": "RULE-002", "description": "Strictly implement FastMCP 3.1 interface contracts.", "severity": "high"}
    ]
}

config = RepoContextConfig.model_validate(config_payload)

# Initialize the official Anthropic client
client = anthropic.Anthropic()

# Send the prompt containing the validated context config to Claude 5.1
response = client.messages.create(
    model="claude-5.1-sonnet-20261220",
    max_tokens=1024,
    system=f"Project Operating Context rules:\n{config.model_dump_json(indent=2)}",
    messages=[{"role": "user", "content": "Analyze the codebase structure."}]
)
print(response.content)
```

## Related tools / concepts
- [Claude Code](claude-code.md)
- [Aider](aider.md) — Terminal-native AI pair programming.
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Claude Hooks](claude-hooks.md)
- [OpenClaw Workflow Prompts](../../knowledge_base/patterns/openclaw-workflow-prompts.md)
- [Standards and Conventions](../../standards.md)
- [Architecture Index](../../architecture/README.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Free Will MCP](free-will-mcp.md)

## Sources / References
- [Anthropic: Context Window Engineering](https://docs.anthropic.com/claude/docs/long-context-window-tips)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Claude Desktop Documentation](https://docs.anthropic.com/claude/docs/claude-desktop-overviews)
- [Architecture Index Search & Verification](https://github.com/search?q=Architecture+Index&ref=2026-07-27-audit)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
