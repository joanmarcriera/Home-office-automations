# Mentat

## What it is
Mentat is an open-source, terminal-native AI pair programmer engineered to coordinate complex, multi-file code modifications directly from the command line. Unlike traditional single-file autocompletion or GUI-based chat interfaces, Mentat parses entire repository structures, builds full AST context trees, and applies targeted edits across dozens of files simultaneously. As of early 2027, Mentat features native integration with **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** and supports frontier reasoning models including **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **DeepSeek-V4**.

## What problem it solves
Managing cross-cutting refactorings, architectural modifications, or multi-module dependency upgrades manually is error-prone and time-consuming. Copy-pasting code fragments between IDE editors and standalone LLM web interfaces strips context and introduces syntax or import mismatches. Mentat eliminates context degradation by executing a closed terminal edit-loop, dynamically selecting relevant code modules, generating precision diffs, and verifying execution directly within the workspace.

## Where it fits in the stack
**Development & Ops / AI-Assisted Coding**. Mentat functions as an autonomous terminal agent and multi-file code editing engine, operating alongside traditional IDEs like VS Code or terminal workflows alongside tools like [Aider](aider.md) and [Claude Code](claude-code.md).

## Typical use cases
- **Multi-File Refactoring**: Coordinating structural code edits across database repositories, API models, and service interfaces in a single command.
- **Codebase Standardization**: Enforcing new linting, type-annotation, or Pydantic v2 schema standards across multi-module Python applications.
- **Automated Test Generation**: Generating end-to-end unit test suites in `pytest` for legacy code bases based on AST context analysis.
- **MCP Server Interoperability**: Exposing internal database schemas or vector memory stores to the terminal agent via FastMCP 3.1 endpoints.

## Strengths
- **Terminal-Native Efficiency**: Streamlined command-line interface tailored for rapid headless or interactive keyboard-driven workflows.
- **Granular Context Control**: Precise inclusion/exclusion glob patterns allowing developers to strictly bound context window consumption.
- **Multi-File Coordination**: Maintains cross-file dependency graph tracking to avoid broken imports or missing symbols.
- **Native FastMCP 3.1 Support**: Seamlessly connects with external tool endpoints for database queries, web search, or live telemetry.

## Limitations
- **Model API Dependency**: Requires active API access keys for Anthropic, OpenAI, Google, or local Ollama / vLLM endpoints.
- **Terminal Learning Curve**: Command flags and CLI-driven prompt syntax require familiarity compared to drag-and-drop GUI editors like Cursor.
- **Token Overhead**: Ingesting extensive file trees for large monolithic projects can rapidly consume LLM context budgets if globs are unconstrained.

## When to use it
- When making synchronized, multi-file architectural changes or API contract updates.
- When working in headless SSH servers, remote containers, or developer terminal environments.
- When orchestrating terminal coding agents leveraging [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers.

## When not to use it
- When a rich graphical IDE interface with inline inline suggestion popups (e.g., [Cursor](cursor.md) or [Windsurf](windsurf.md)) is preferred.
- For simple single-line inline code completions where lightweight IDE extensions are faster.

## Getting started

### Installation
Mentat is distributed via PyPI and can be installed with Python 3.10+:

```bash
pip install mentat-ai pydantic>=2.10.0
```

### Initial Run
Launch Mentat on target files with an explicit instruction:

```bash
mentat src/main.py src/services/ --run "Add strict Pydantic v2 validation models and type annotations"
```

### Configuration
Project preferences can be defined in `.mentat_config.json` at the repository root:

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

### 1. Multi-Directory Targeted Context
Specify exact directories and exclude test fixtures or legacy code:

```bash
mentat src/api/ src/core/ --exclude src/core/legacy/ --run "Update database endpoints to async/await"
```

### 2. Batch Refactoring Command
Execute non-interactive batch edits powered by GPT-5.5 or Gemini 4.0 Pro:

```bash
mentat --run "Refactor all REST routes to FastMCP 3.1 tool endpoints" --model gpt-5.5-preview src/
```

### 3. MCP Server Connectivity
Inject live context from a Postgres database MCP server during a refactor:

```bash
mentat --mcp-server "npx @modelcontextprotocol/server-postgres postgres://localhost/production"
```

## API examples

### Python Programmatic Refactoring Session with Pydantic v2
Integrate Mentat programmatically within CI/CD pipelines or internal task automation tools:

```python
import asyncio
from pydantic import BaseModel, Field
from mentat import MentatSession

class MentatTaskConfig(BaseModel):
    paths: list[str] = Field(..., min_length=1, description="Target source paths")
    instruction: str = Field(..., min_length=10, description="Refactoring prompt instruction")
    model: str = Field(default="claude-5-1-sonnet-20261022", description="Frontier LLM model ID")
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)

async def run_automated_refactor(task_payload: dict) -> bool:
    # Validate payload structure using Pydantic v2
    task = MentatTaskConfig.model_validate(task_payload)

    session = await MentatSession.create(
        paths=task.paths,
        model=task.model,
        temperature=task.temperature
    )

    await session.process_instruction(task.instruction)
    await session.apply_changes()
    await session.close()
    return True

if __name__ == "__main__":
    payload = {
        "paths": ["src/services/user.py"],
        "instruction": "Upgrade user service to use FastMCP 3.1 tool decorators and strict typing.",
        "model": "claude-5-1-sonnet-20261022"
    }
    asyncio.run(run_automated_refactor(payload))
```

## Related tools / concepts
- [Aider](aider.md) — Terminal-native AI pair programmer with Architect Mode.
- [Claude Code](claude-code.md) — Anthropic's official terminal agent for agentic workflows.
- [Plandex](plandex.md) — Plan-first engineering engine for complex codebase refactoring.
- [Cursor](cursor.md) — AI-native graphical IDE with deep index navigation.
- [Superconductor](superconductor.md) — Parallel execution environment for agentic coding.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standardized tool and resource sharing protocol.

## Sources / references
- [Official Mentat Website](https://www.mentat.ai/)
- [Mentat GitHub Repository](https://github.com/AbanteAI/mentat)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
