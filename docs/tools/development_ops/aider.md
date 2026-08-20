# Aider

## What it is
Aider is a leading terminal-native AI pair programmer that empowers developers to edit code bases, refactor multi-file architectures, and manage Git repositories using natural language prompts. As of early 2027, Aider features advanced **Architect Mode** powered by **Claude 5.1**, **Claude 3.7 Sonnet**, **GPT-5.5**, and **Gemini 4.0 Pro**, combined with native **FastMCP 3.1** protocol support for dynamic tool and resource integration.

## What problem it solves
Managing multi-file refactorings manually requires context tracking across AST trees, editing multiple files, and managing Git commit histories. Aider bridges high-level architectural requirements with granular file edits. It automatically builds repository maps, applies precise git diffs directly to the local filesystem, runs test suites to verify edits, and creates clean Git commit messages for every change set.

## Where it fits in the stack
**Development & Ops / AI-Assisted Coding**. Aider functions as an autonomous terminal agent and pair-programming assistant, operating directly in local developer environments or SSH sessions alongside tools like [Claude Code](claude-code.md) and [Mentat](mentat.md).

## Typical use cases
- **Multi-File Refactoring**: Implementing cross-cutting API schema changes or framework migrations across multiple repository files.
- **Architect-Editor Decomposition**: Running Architect Mode to generate high-level technical plans before delegating implementation diff generation.
- **Automated Bug Fixing**: Feeding test failure outputs (`pytest`, `jest`) directly into Aider to analyze tracebacks and execute immediate patches.
- **FastMCP 3.1 Tool Expansion**: Connecting external MCP servers for database schema introspection, vector search, or live telemetry.

## Strengths
- **Repository Mapping**: Builds and updates AST-based repo maps to maintain token-efficient context across large projects.
- **Git Native Automation**: Generates clean, atomic Git commits with descriptive messages for all file modifications.
- **Dual-Model Architect Mode**: Uses high-reasoning frontier models (e.g., Claude 5.1) for planning while delegating diff execution to faster models.
- **Multi-Provider Flexibility**: Broad model support across Anthropic, OpenAI, Google Gemini, DeepSeek-V4, and local Ollama / vLLM hosts.

## Limitations
- **Terminal Workflows**: Requires comfort with CLI command flags, terminal prompts, and keyboard-driven workflows.
- **Context Limits on Monoliths**: Unconstrained monorepos with hundreds of thousands of LOC require careful file inclusion boundaries.
- **Token Usage on Complex Tasks**: Intensive iterative sessions with frontier models consume significant API token allocations.

## When to use it
- When implementing complex, multi-file features or performing structural refactors from the command line.
- For hands-free bug remediation workflows where test suites provide instant execution feedback loops.
- In terminal environments, SSH remote servers, or developer devcontainers.

## When not to use it
- When a graphical IDE interface with inline popups (such as [Cursor](cursor.md) or [Windsurf](windsurf.md)) is preferred.
- For simple single-line completion tasks where lightweight IDE completion plugins are faster.

## Getting started

### Installation
Install Aider via `pip` or `pipx`:

```bash
pip install aider-chat pydantic>=2.10.0
```

### Initial Run & Launch
Configure provider API keys and launch Aider in your repository root:

```bash
export ANTHROPIC_API_KEY=your_key_here
aider --model claude-5-1-sonnet-20261022 --architect
```

### Project Configuration (`.aider.conf.yml`)
Standardize team defaults in `.aider.conf.yml` at project root:

```yaml
model: claude-5-1-sonnet-20261022
architect: true
auto-commits: true
map-tokens: 2048
mcp-servers:
  - "uvx mcp-server-git"
```

## CLI examples

### Architect Mode Execution
Engage Architect Mode for multi-stage planning and diff execution:

```bash
aider --architect --message "Refactor authentication flow to use OAuth2 OIDC and strict FastMCP 3.1 endpoints"
```

### Automated Bug Fixing Loop
Pipe pytest failures directly to Aider for automated analysis and patching:

```bash
pytest | aider --message "Fix all failing assertions in the test output"
```

### FastMCP 3.1 Tool Server Binding
Connect Aider to a live database or repository MCP server:

```bash
aider --mcp-server "npx @modelcontextprotocol/server-postgres postgres://localhost/db"
```

## API examples

### Python Programmatic Configuration Validation (Pydantic v2)
Validate Aider configuration files programmatically in automation scripts:

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class AiderConfig(BaseModel):
    model: str = Field(default="claude-5-1-sonnet-20261022", description="Frontier model ID")
    architect: bool = Field(default=True, description="Enable Architect Mode")
    auto_commits: bool = Field(default=True, alias="auto-commits")
    map_tokens: int = Field(default=2048, alias="map-tokens", ge=512, le=8192)
    mcp_servers: List[str] = Field(default_factory=list, alias="mcp-servers")

    class Config:
        populate_by_name = True

# Validate sample configuration payload
config_data = {
    "model": "claude-5-1-sonnet-20261022",
    "architect": True,
    "auto-commits": True,
    "map-tokens": 4096,
    "mcp-servers": ["uvx mcp-server-git"]
}

session_config = AiderConfig.model_validate(config_data)
print(f"Validated Aider Session Config for Model: {session_config.model}")
print(f"Active MCP Servers: {session_config.mcp_servers}")
```

## Related tools / concepts
- [Claude Code](claude-code.md) — Anthropic's official terminal agent for agentic development.
- [Mentat](mentat.md) — Terminal-native multi-file AI pair programmer.
- [Plandex](plandex.md) — Plan-first engineering engine for complex codebase refactoring.
- [Cursor](cursor.md) — AI-native graphical IDE with deep index navigation.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standardized tool and context sharing protocol.

## Sources / references
- [Official Aider Website](https://aider.chat/)
- [Aider GitHub Repository](https://github.com/paul-gauthier/aider)
- [Aider Architect Mode Documentation](https://aider.chat/docs/architect.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
