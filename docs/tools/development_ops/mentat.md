# Mentat

## What it is
Mentat is a high-performance AI coding assistant that coordinates complex changes across multiple files directly from the terminal. As of June 2026, it features native integration with the **Model Context Protocol (MCP)** and is optimized for the latest frontier models, including **Claude 4.8 Opus** (`claude-4-8-opus-20260528`) and **GPT-5.5**.

## What problem it solves
Mentat enables developers to make coordinated, multi-file changes from the terminal with AI assistance, reducing the manual effort of large refactors and cross-cutting edits. It eliminates the need to manually copy-paste code into a chat interface by providing a direct terminal-based "edit-loop" that understands the entire repository structure.

## Where it fits in the stack
**Development & Ops**. Functions as a terminal-based AI coding assistant for multi-file editing, typically used alongside a standard IDE or text editor. It sits between high-level orchestration and direct file editing.

## Typical use cases
- Coordinating complex changes across multiple files.
- Codebase-wide refactoring from the terminal.
- Applying precise, controlled edits with AI assistance.
- Generating unit tests for existing codebases.
- **MCP-Powered Tooling**: Using Mentat to call external tools (e.g., database schema inspectors, API explorers) via the Model Context Protocol during a coding session.

## Strengths
- **Terminal-native workflow**: Ideal for developers who prefer the command line.
- **Precise control**: Allows users to include or exclude specific files from the context.
- **Multi-file coordination**: Handles dependencies and cross-file impacts effectively.
- **Native MCP Support**: Can leverage a vast ecosystem of MCP servers for enhanced capabilities.

## Limitations
- **External LLM dependence**: Requires an API key for OpenAI, Anthropic, or other providers.
- **Learning curve**: Terminal commands and configuration may be less intuitive than GUI alternatives.

## When to use it
- When you need precise, multi-file edits from the terminal.
- When codebase standardization tasks require coordinated changes across several modules.
- When you want to leverage [MCP](../automation_orchestration/mcp.md) servers natively within your terminal-based coding workflow.

## When not to use it
- When a graphical editor experience (like [Cursor](cursor.md)) is preferred.
- When real-time inline completions are the primary need (use [Codeium](codeium.md)).

## Getting started

### Installation
Mentat can be installed via pip:

```bash
pip install mentat-ai
```

### Configuration
Create a `.mentat_config.json` in your project root to manage model preferences and context inclusion rules. For June 2026, you can specify Claude 4.8:

```json
{
  "model": "claude-4-8-opus-20260528",
  "temperature": 0.1,
  "file_exclude": [
    "node_modules/",
    "dist/",
    ".git/"
  ]
}
```

## CLI examples

### Context Management
Mentat allows granular control over what the AI can see:

```bash
# Include specific files and a directory
mentat src/main.py src/utils/ tests/

# Use glob patterns to include all python files
mentat "scripts/**/*.py"

# Include an MCP server for additional context
mentat --mcp-server http://localhost:3000/mcp
```

### Interactive Refactoring Loop
The core workflow involves describing a task in the Mentat shell:

```text
> Search the codebase for all occurrences of hardcoded API endpoints and move them to a new config.py file.
>
> Mentat: [Proposes changes to 4 files]
>
> [y/n/i/e] (y: apply, n: skip, i: individual, e: explain)
```

### Scripting and Automation
Run Mentat in a non-interactive mode for CI/CD or automated tasks:

```bash
# Run a specific command and exit
mentat --run "Refactor all imports to use absolute paths"
```

## API examples
Mentat exposes a Python API for building custom agents or extending its functionality.

### Programmatic File Editing
```python
from mentat import MentatSession

async def main():
    # Initialize a Mentat session for the current directory
    session = await MentatSession.create(path=".")

    # Ask Mentat to perform a task
    await session.talk("Add type hints to all functions in src/utils.py")

    # Review and apply changes programmatically
    changes = await session.get_pending_changes()
    for change in changes:
        print(f"File: {change.file_path}")
        await session.apply_change(change)

    await session.close()
```

## Related tools / concepts
- [Aider](aider.md) — Another popular terminal-based AI pair programmer.
- [Plandex](plandex.md) — For terminal-native complex refactoring.
- [Codeium](codeium.md) — For IDE-native AI assistance.
- [Claude Code](./claude-code.md) — Anthropic's official CLI for agentic coding.
- [Cursor](cursor.md) — An AI-native IDE for a GUI-first approach.
- [Continue](./continue_dev.md) — An open-source IDE extension for AI assistance.
- [Sweep](./sweep_dev.md) — For automating GitHub issues into PRs.
- [Superconductor](./superconductor.md) — Parallel agent sessions for rapid development.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for connecting models to tools.

## Sources / references
- [Official Website](https://www.mentat.ai/)
- [GitHub Repository](https://github.com/AbanteAI/mentat)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
