# Mentat

## What it is
Mentat is an AI tool that coordinates complex changes across multiple files directly from the terminal. It uses LLMs to understand the codebase and apply edits, focusing on developer productivity and precise control. Unlike many IDE-based assistants, Mentat is designed to handle large-scale refactors where the context spans dozens of files. In early 2027, Mentat features native integration with **FastMCP 3.1** and frontier reasoning models (**Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**).

## What problem it solves
Enables developers to make coordinated, multi-file changes from the terminal with AI assistance, reducing the manual effort of large refactors and cross-cutting edits. It eliminates the need to manually copy-paste code into a chat interface by providing a direct terminal-based "edit-loop".

## Where it fits in the stack
**Development & Ops**. Functions as a terminal-based AI coding assistant for multi-file editing, typically used alongside a standard IDE or text editor.

## Typical use cases
- Coordinating complex changes across multiple files.
- Codebase-wide refactoring from the terminal.
- Applying precise, controlled edits with AI assistance.
- Generating unit tests for existing codebases.

## Strengths
- **Terminal-native workflow**: Ideal for developers who prefer the command line.
- **Precise control**: Allows users to include or exclude specific files from the context.
- **Multi-file coordination**: Handles dependencies and cross-file impacts effectively.
- **Native MCP Support**: Direct integration with Model Context Protocol (FastMCP 3.1) servers for extended tool capabilities.

## Limitations
- **External LLM dependence**: Requires an API key for OpenAI, Anthropic, or other providers.
- **Learning curve**: Terminal commands and configuration may be less intuitive than GUI alternatives.

## When to use it
- When you need precise, multi-file edits from the terminal.
- When codebase standardization tasks require coordinated changes across several modules.
- When leveraging [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) tools for enhanced codebase interaction.

## When not to use it
- When a graphical editor experience (like [Cursor](cursor.md)) is preferred.
- When single-file completions are the primary need.

## Getting started

### Installation
Mentat can be installed via pip:

```bash
pip install mentat-ai pydantic>=2.0.0
```

### Hello-world example
Run Mentat in non-interactive mode on a target file:

```bash
mentat main.py --run "Add type hints and docstrings to all functions"
```

### Configuration
Create a `.mentat_config.json` in your project root to manage model preferences, temperature, and context inclusion rules. Claude 5.1 is the recommended model for complex reasoning:

```json
{
  "model": "claude-5-1-sonnet-20261022",
  "temperature": 0.1,
  "file_exclude": [
    "node_modules/",
    "dist/",
    "*.log",
    ".git/",
    "__pycache__/"
  ],
  "maximum_context": 200000
}
```

## CLI examples

### 1. Granular Context Selection
Include specific files and directories while excluding patterns:

```bash
mentat src/main.py src/utils/ tests/ --exclude tests/legacy/
```

### 2. Batch Non-Interactive Command
Execute refactoring commands directly without entering the interactive shell:

```bash
mentat --run "Refactor database query logic in repository layer" --model gpt-5.5-preview src/
```

### 3. Model Context Protocol (MCP) Integration
Connect to MCP servers to provide Mentat with database introspection or search capabilities:

```bash
mentat --mcp-server "npx @modelcontextprotocol/server-postgres"
```

## API examples

### Python Programmatic Access with Pydantic v2 validation
Mentat can be integrated into custom automation scripts using its Python API and verified using Pydantic v2 schemas.

```python
from pydantic import BaseModel, Field
from mentat import MentatSession

class RefactorTask(BaseModel):
    paths: list[str] = Field(..., min_length=1)
    instruction: str = Field(..., min_length=10)
    model: str = Field(default="claude-5-1-sonnet-20261022")

async def run_validated_refactor(task_data: dict) -> None:
    # Validate the task configuration using Pydantic v2
    task = RefactorTask(**task_data)

    session = await MentatSession.create(
        paths=task.paths,
        model=task.model
    )
    await session.process_instruction(task.instruction)
    await session.apply_changes()
    await session.close()
```

### Automated Scripting
Run Mentat in a non-interactive mode for CI integration or batch tasks:

```bash
# Run a specific command and exit
mentat --run "Generate docstrings for all functions in lib/"

# Use GPT-5.5 for a specific reasoning task
mentat --model gpt-5.5-preview src/
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

## Sources / references
- [Official Website](https://www.mentat.ai/)
- [GitHub Repository](https://github.com/AbanteAI/mentat)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
