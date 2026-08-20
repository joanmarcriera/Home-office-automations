# Aider

## What it is
Aider is a leading terminal-based AI pair programmer that allows developers to edit code, create new projects, and manage Git repositories using natural language. As of early 2027, Aider features advanced **Architect Mode** powered by **Claude 5.1** and native **FastMCP 3.1** integration for sophisticated tool-use capabilities and repository-map analysis.

## What problem it solves
It bridges the gap between high-level reasoning and low-level file manipulation. Aider eliminates the need for manual copy-pasting by directly applying AI-generated diffs to the local filesystem, handling Git commits automatically, and maintaining a coherent "map" of the entire codebase for context.

## Where it fits in the stack
**Development & Ops / AI-Assisted Coding**. It serves as the primary interface for "hands-on" AI engineering, sitting between the developer's terminal and the LLM reasoning layer.

## Typical use cases
- **Rapid Feature Implementation**: Describing a new feature and letting Aider generate the necessary files and logic.
- **Codebase Refactoring**: Executing complex, multi-file refactors by giving high-level instructions.
- **Automated Bug Fixing**: Providing error logs or failing test cases and asking Aider to diagnose and repair the issue.
- **Documentation Updates**: Keeping READMEs and technical docs in sync with code changes automatically.

## Strengths
- **Multi-file Editing**: Excels at coordinating changes across large codebases using its "repository map."
- **Git Integration**: Automatically creates descriptive commit messages and manages local branches.
- **Tool Choice**: Supports a wide range of models including **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and local models via **Ollama**.
- **Architect Mode**: Separates high-level planning from low-level implementation for better reliability on complex tasks.

## Limitations
- **Terminal Reliance**: Requires comfort with command-line interfaces.
- **Context Limits**: While the repo map helps, very large monolithic projects can still hit LLM context window constraints.
- **Cost**: Heavy usage with frontier models can lead to significant API credit consumption.

## When to use it
- For "greenfield" project development where rapid iteration is key.
- When performing repetitive refactoring tasks that are easy to describe but tedious to execute.
- When working in a language or framework where you need "on-the-fly" expert assistance.

## When not to use it
- For very simple, single-line changes where a manual edit is faster.
- In environments where you cannot grant an external process write access to your filesystem.
- If you require a GUI-first experience (consider **Cursor** or **Windsurf** instead).

## Getting started

### Installation
Install Aider via `pip` or `pipx`:

```bash
pip install aider-chat
```

### Initial Setup
Set your API key and launch Aider in your project directory:

```bash
export ANTHROPIC_API_KEY=your_key_here
aider
```

### Modern Architecture Setup
Aider supports advanced frontier models and `architect` mode natively:

```bash
aider --model claude-5-1-sonnet-20261022 --architect
```

## CLI examples

### Architect Mode with Claude 5.1
Use the high-level architect mode to plan and execute a complex feature:

```bash
aider --architect --message "Implement a new authentication flow using OIDC and FastMCP 3.1"
```

### Automated Bug Fixing
Pipe a failing test output directly into Aider for immediate repair:

```bash
pytest | aider --message "Fix the failing tests in the output"
```

### Native MCP Integration
Connect Aider to specialized FastMCP 3.1 servers for enhanced context:

```bash
aider --mcp-server "npx @modelcontextprotocol/server-postgres postgres://localhost/db"
```

## API examples

### Non-interactive Python Scripting
Aider can be used as a library or via shell scripts for automated maintenance:

```python
import subprocess

def auto_refactor(instruction):
    subprocess.run(["aider", "--message", instruction, "--yes"])

# auto_refactor("Update all docstrings to follow the Google Style Guide")
```

### Configuration via .aider.conf.yml
Standardize Aider behavior across a team using a project-level config:

```yaml
model: claude-5-1-sonnet-20261022
architect: true
auto-commits: true
map-tokens: 2048
mcp-servers:
  - "uvx mcp-server-git"
```

### Programmatic Setup with Pydantic v2
Validating Aider workspace sessions and configurations:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class AiderSessionConfig(BaseModel):
    model: str = Field(default="claude-5-1-sonnet-20261022")
    architect: bool = Field(default=True)
    auto_commits: bool = Field(default=True, alias="auto-commits")
    map_tokens: int = Field(default=2048, alias="map-tokens")
    mcp_servers: List[str] = Field(default_factory=list, alias="mcp-servers")

    class Config:
        populate_by_name = True

# Parse and validate setup configuration
config_data = {
    "model": "claude-5-1-sonnet-20261022",
    "architect": True,
    "auto-commits": True,
    "mcp-servers": ["uvx mcp-server-git"]
}

session = AiderSessionConfig.model_validate(config_data)
print(f"Validated session model: {session.model}")
print(f"Configured MCP servers: {session.mcp_servers}")
```

## Related tools / concepts
- [Claude Code](claude-code.md) — Anthropic's official terminal agent.
- [Cursor](cursor.md) — AI-native IDE with deep indexing.
- [Plandex](plandex.md) — Plan-first AI engineering engine.
- [Mentat](mentat.md) — Alternative terminal-native editor.
- [Model Context Protocol](../automation_orchestration/mcp.md) — For extending Aider's capabilities.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Theoretical background.
- [GPT Engineer](gpt_engineer.md) — For full-project generation.
- [Windsurf](windsurf.md) — Next-gen flow-based IDE.
- [Claude Hooks](claude-hooks.md) — Guardrails for agent sessions.

## Sources / references
- [Official Website](https://aider.chat/)
- [Aider GitHub Repository](https://github.com/paul-gauthier/aider)
- [Aider Documentation: Architect Mode](https://aider.chat/docs/architect.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
