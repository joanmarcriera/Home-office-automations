# Claude Code

## What it is
Claude Code is Anthropic's premier terminal-native developer agent and command-line interface (CLI) for AI-native software engineering. Operating directly within local shell environments, it utilizes **Claude 5.6** and frontier **o4-reasoning** / **GPT-5.6** / **DeepSeek-V4** (via hybrid adapters) as its primary reasoning backends. As of early 2027, Claude Code is fully standardized on the **Model Context Protocol (MCP 3.1 / FastMCP 3.1)**, allowing it to seamlessly coordinate with local services, execute secure shell commands, write and edit files, and self-correct based on compiler or test outputs.

## What problem it solves
Traditional software engineering involves continuous context-switching between code editors, web search engines, terminal logs, and chat windows. Claude Code bridges this "Execution Gap" by embedding a frontier-tier agent directly inside the terminal. It solves:
- **Brittle Automation Loops**: Rather than simple text generation, it conducts autonomous file editing, runtime debugging, and verification loops.
- **Out-of-Date Context**: It reads the active workspace dynamically, resolving complex multi-file relationships without manual copy-pasting.
- **Sandbox Containerization**: Integrates with local container environments via **FastMCP 3.1** endpoints, preventing risky raw execution of untrusted operations on the host system.

## Where it fits in the stack
**Category**: Agent / [Development & Ops](index.md). It acts as the primary orchestrator of local repository changes, working in tandem with static analysis tools, CI runners, and local execution runtimes (like Ollama and Docker).

## Typical use cases
- **Autonomous Feature Sprints**: Describing requirements and letting the agent write the implementation, craft tests, and verify success autonomously.
- **Interactive Multi-File Refactoring**: Transitioning legacy frameworks or libraries across large repository surfaces while maintaining API consistency.
- **Agentic Debugging**: Feeding raw stack traces or test failures to the CLI, enabling it to pinpoint, patch, and re-run test suites.
- **Documentation Hygiene**: Maintaining configuration files (`mkdocs.yml`), dependency maps, and operational manuals (`CLAUDE.md`, `AGENTS.md`) in sync with source code.
- **Local Tool Execution**: Coordinating local Docker environments, database migrations, and web scraping utilities via FastMCP 3.1 servers.

## Strengths
- **SOTA SWE-bench Performance**: Reaches over 94.8% on SWE-bench Verified, outperforming traditional pair programming environments.
- **MCP 3.1 & FastMCP 3.1 Native**: Supports the latest transport standards and schema-validating tool call handlers for safe execution.
- **Interactive Shell Mode**: Merges the simplicity of a standard terminal shell with a continuous conversation history and real-time reasoning insights.
- **Robust Failure Shrinking**: Dynamically isolates failing test parameters and modifies its approach iteratively without losing context.
- **Resource Consciousness**: Features advanced context compacting (`/compact`) and token budget configuration (`--budget`) to keep API costs predictable.

## Limitations
- **Token Amplification**: Massive repositories with long execution loops can quickly consume input tokens with high-tier models.
- **Platform OS Dependency**: Certain native terminal executions behave differently on Windows PowerShell versus UNIX environments.
- **Varying Tool Latency**: Complex tool chaining over multi-step FastMCP workflows can introduce execution delays.

## When to use it
- For Git-tracked project development where you can easily review and rollback changes.
- When performing repetitive or tedious code migrations, test generation, and documentation maintenance.
- In multi-agent environments where standardized tools must be exposed via **FastMCP 3.1** endpoints.
- When deep, agentic reasoning is required to solve complex, hidden logical errors across multiple modules.

## When not to use it
- In raw, untracked directories containing sensitive personal or financial configuration files without Git protection.
- For simple, one-line code completions where inline IDE autocomplete extensions (like GitHub Copilot or Codeium) offer lower latency.
- In fully air-gapped environments that do not permit secure outbound API access to Anthropic or partner endpoints.

## Getting started

### Installation
Claude Code is distributed as a high-performance Node.js executable:
```bash
npm install -g @anthropic-ai/claude-code@latest
```

### Authentication and Setup
Run the authentication and configuration wizard to link your Anthropic Console account:
```bash
claude auth login
claude init
```

## CLI examples

### Start interactive agentic session
```bash
# Launch inside your project root
claude
```

### Run an autonomous command
```bash
# Instruct Claude to fix a test and verify using NPM
claude "Fix the failing tests in src/auth.spec.ts and verify they pass with 'npm test'"
```

### Built-in CLI commands
Within the Claude Code interactive prompt, the following slash commands are fully supported:
```bash
/usage    # Displays current cost, session token counts, and remaining budget
/compact  # Summarizes past execution history to optimize the model's context window
/review   # Audits current staged git changes for bugs, design flaws, and metadata adherence
/doctor   # Executes connection, authentication, and FastMCP 3.1 status diagnostics
```

## API examples

The following Python example demonstrates how a developer can programmatically validate Claude Code's tool definitions using **Pydantic v2** validation to ensure correct schema format before registering them with a **FastMCP 3.1** server.

```python
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import json

# Define the FastMCP 3.1 compatible schema for an agentic tool registration
class MCPToolDefinition(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    description: str = Field(..., min_length=10)
    input_schema: dict = Field(..., description="Valid JSON Schema representation of inputs")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "verify_test_suite",
                "description": "Runs a target test suite using jest or pytest.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "test_file": {"type": "string"},
                        "verbose": {"type": "boolean", "default": True}
                    },
                    "required": ["test_file"]
                }
            }
        }
    }

def validate_and_register_tool(tool_data: dict) -> str:
    """Validates the tool definition using Pydantic v2 and formats it for FastMCP 3.1."""
    try:
        # Pydantic v2 validation trigger
        validated_tool = MCPToolDefinition.model_validate(tool_data)
        return json.dumps({
            "status": "success",
            "registered_tool": validated_tool.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    tool_payload = {
        "name": "run_cargo_audit",
        "description": "Executes a cargo security audit on the local crate structure.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ignore_warnings": {"type": "boolean", "default": False}
            }
        }
    }
    print(validate_and_register_tool(tool_payload))
```

## Related tools / concepts
- [Aider](aider.md) — Excellent command-line AI programming tool leveraging Git repository state.
- [Devin](devin.md) — Autonomous agent platform with a dedicated workspace, terminal, and browser environment.
- [Roo Code](../agents/roo-code.md) — Highly customizer-friendly VS Code agent extension.
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Conceptual patterns governing model tool calling.
- [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) — The lightweight framework used to build secure extension backends.

## Sources / references
- [Anthropic Claude Code Docs](https://code.claude.com/)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
