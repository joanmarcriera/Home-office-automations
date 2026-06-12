# Claude Context Mode

## What it is
Claude Context Mode refers to community and workflow patterns for giving [Claude Code](claude-code.md) richer, better-structured operating context. This is typically achieved through [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers, repository memory files (`AGENTS.md`), and scoped task documents. It is the practice of "context engineering" specifically for agentic coding workflows in June 2026.

## What problem it solves
It reduces prompt sprawl and makes agent behavior more repeatable than pasting large amounts of context into every session. It solves the "context window amnesia" problem by ensuring the agent has access to a durable, versioned source of truth about the project's architecture, standards, and progress.

## Where it fits in the stack
**Development & Ops / Context Engineering Pattern**. It is a practical operating pattern around [Claude Code](claude-code.md), [MCP](../automation_orchestration/mcp.md), and AI-native IDEs like [Cursor](cursor.md) or [Zed](zed.md).

## Typical use cases
- **Repository Onboarding**: Giving an agent a high-level map of a new codebase via `AGENTS.md`.
- **Architectural Guardrails**: Enforcing specific design patterns (e.g., "always use [FastAPI](../frameworks/fastapi.md) dependency injection").
- **Task Persistence**: Resuming complex, multi-day coding tasks across different chat sessions using progress logs.
- **Dynamic Context Injection**: Using [FastMCP 3.0](../automation_orchestration/mcp.md) to fetch real-time data into the agent's reasoning loop.

## Strengths
- **Consistency**: Agent behavior becomes more predictable across sessions.
- **Efficiency**: Reduces the amount of manual context pasting required.
- **Versionable**: Context files live in the repo and evolve alongside the code.
- **Standardized**: Leverages the official [Model Context Protocol](../automation_orchestration/mcp.md) for tool-based context.

## Limitations
- **Maintenance Overhead**: Requires human (or agent) discipline to keep context files up to date.
- **Noise**: Poorly designed context layers can overwhelm the model and cause "distraction."
- **Model specific**: Optimized for frontier models like [Claude 4.8 Opus](claude.md) and [GPT-5.5](openai.md); may be less effective on smaller models.

## When to use it
- When working on complex, long-running projects where architectural consistency is critical.
- When collaborating with multiple agents or human-agent teams.
- When you need to provide the agent with external tool context via MCP.

## When not to use it
- For trivial, one-off scripts where the overhead of creating context files exceeds the task effort.
- When the task is simple enough for the agent to infer everything from local file context alone.

## Getting started

### 1. Initialize Repository Memory
Create an `AGENTS.md` file in your repository root to serve as the primary context source.
```bash
touch AGENTS.md
```

### 2. Configure Claude Code
Add repository-specific instructions or MCP servers to your [Claude Code Setup](claude-code-setup.md).
```bash
claude mcp add project-docs -- npx -y @upstash/context7-mcp
```

### 3. Establish the Loop
At the start of each session, point the agent to the memory file:
```bash
claude --prompt "Project context: $(cat AGENTS.md)"
```

## CLI examples

### Injecting Repo Context
Force Claude to read the project's operating manual at startup:
```bash
claude --prompt "Please follow the standards in AGENTS.md"
```

### Configuring MCP Context
Add a documentation context server to the session:
```bash
claude mcp add tailwind -- npx -y @modelcontextprotocol/server-documentation https://tailwindcss.com/docs
```

### Context-Aware Refactoring
Use [Aider](aider.md) with context mapping for multi-file changes:
```bash
aider --message "Apply the refactoring pattern defined in AGENTS.md to the auth module"
```

## API examples

### MCP Configuration (`claude_desktop_config.json`)
Standardize context delivery across different clients using a shared configuration.

```json
{
  "mcpServers": {
    "repo-context": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_TOKEN": "your-token"
      }
    }
  }
}
```

### FastMCP 3.0 Context Provider (Python)
Create a custom context provider using the [FastMCP 3.0 SDK](../automation_orchestration/mcp.md).

```python
from mcp.server import FastMCP

mcp = FastMCP("ContextHelper")

@mcp.tool()
async def get_architecture_map() -> str:
    """Returns the latest architecture map from ARCHITECTURE.md."""
    with open("docs/architecture/component_map.md", "r") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Claude Code](claude-code.md): The primary agent for context-aware coding.
- [Model Context Protocol](../automation_orchestration/mcp.md): The underlying transport for dynamic context.
- [AGENTS.md](../../AGENTS.md): The repository-wide operating contract.
- [Aider](aider.md): Terminal-native AI pair programming with repository mapping.
- [Claude Hooks](claude-hooks.md): Middleware for deterministic session guardrails.
- [OpenClaw Workflow Prompts](../../knowledge_base/patterns/openclaw-workflow-prompts.md): Advanced prompting patterns.
- [Context7](context7.md): Live documentation context layer.
- [FastMCP 3.0 SDK](../frameworks/mastra.md): For building context-rich servers.

## Sources / references
- [Anthropic: Context Engineering Best Practices](https://docs.anthropic.com/claude/docs/context-engineering)
- [FastMCP 3.0 Specification](https://github.com/modelcontextprotocol/fastmcp)
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
