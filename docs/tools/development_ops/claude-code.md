# Claude Code

## What it is
Claude Code is Anthropic's premier terminal-native developer agent and command-line interface (CLI) for AI-native software engineering. Operating directly within local shell environments, it utilizes **Claude 5.6** and frontier **o4-reasoning** / **GPT-5.6** / **DeepSeek-V4** (via hybrid adapters) as its primary reasoning backends. As of early 2027, Claude Code is fully standardized on the **Model Context Protocol (MCP 3.1 / FastMCP 3.1)**, allowing it to seamlessly coordinate with local services, execute secure shell commands, write and edit files, and self-correct based on compiler or test outputs.

```
+-----------------------------------------------------------------------------------+
|                        Developer / Shell Environment                              |
|                       "claude 'Fix bug in auth service'"                          |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            Claude Code Agent Core                                 |
|  +-----------------------+  +------------------------+  +-----------------------+ |
|  | Context Management    |  | Reasoning & Planning   |  | Tool Dispatcher       | |
|  | (/compact, CLAUDE.md) |  | (Claude 5.6 / GPT-5.6) |  | (MCP 3.1 / FastMCP)   | |
|  +-----------------------+  +------------------------+  +-----------------------+ |
+-----------------------------------------------------------------------------------+
                                          |
                        +-----------------+-----------------+
                        |                                   |
           Local Workspace Operations              FastMCP 3.1 Tools
                        |                                   |
                        v                                   v
+---------------------------------------+   +---------------------------------------+
|  File System & Terminal Execution     |   |  External Server Integrations         |
|  - Reads/Writes workspace files       |   |  - Database connections               |
|  - Executes test suites & linters     |   |  - Docker & K8s sandboxes             |
|  - Analyzes compiler error streams    |   |  - Web scraping & API drivers         |
+---------------------------------------+   +---------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Git Version Control & Verification                         |
|   - Inspects diffs, verifies tests pass, generates descriptive commit messages   |
+-----------------------------------------------------------------------------------+
```

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

## Architecture & Tool Calling Engine

### Claude Code Tool Execution Loop
Claude Code relies on a deterministic tool execution loop that safely executes operations and reports results back to the LLM backend:

```
+-----------------------------------------------------------------------------------+
| 1. Request Analysis & Tool Selection                                              |
|    - Evaluates terminal command, file inspection, or FastMCP tool requirements.   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. Input Schema Validation (Pydantic v2 / FastMCP 3.1)                            |
|    - Validates tool arguments against strict JSON schema.                        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. Execution & Safety Verification                                                |
|    - Checks operation against permission rules and workspace sandbox policies.    |
|    - Executes file edit, bash command, or gRPC/SSE FastMCP call.                  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. Outcome Observation & Feedback Analysis                                        |
|    - Captures stdout, stderr, exit status, and compilation results.              |
|    - If execution fails -> Triggers internal self-correction reasoning step.     |
+-----------------------------------------------------------------------------------+
```

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

### Pydantic v2 FastMCP Tool Definition
The following Python example demonstrates how a developer can programmatically validate Claude Code's tool definitions using **Pydantic v2** validation to ensure correct schema format before registering them with a **FastMCP 3.1** server.

```python
import json
import sys
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError

class FastMCPToolParameter(BaseModel):
    name: str = Field(..., description="Parameter identifier")
    param_type: str = Field(..., description="JSON Schema type (string, integer, boolean)")
    description: str = Field(..., description="Explanation of parameter behavior")
    is_required: bool = Field(default=True)

class ClaudeCodeToolSchema(BaseModel):
    tool_name: str = Field(..., description="Identifier for Claude Code tool")
    description: str = Field(..., min_length=15, description="Tool purpose summary")
    parameters: List[FastMCPToolParameter] = Field(default_factory=list)
    timeout_seconds: int = Field(default=30, ge=1, le=300)

    @field_validator("tool_name")
    @classmethod
    def validate_tool_name(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError("tool_name must be a valid Python identifier")
        return v

def generate_fastmcp_registration(tool_def: Dict[str, Any]) -> str:
    """Validates tool schema with Pydantic v2 and returns FastMCP 3.1 registration JSON."""
    try:
        validated = ClaudeCodeToolSchema.model_validate(tool_def)

        # Build FastMCP 3.1 compliant payload
        properties = {}
        required = []
        for param in validated.parameters:
            properties[param.name] = {
                "type": param.param_type,
                "description": param.description
            }
            if param.is_required:
                required.append(param.name)

        fastmcp_payload = {
            "name": validated.tool_name,
            "description": validated.description,
            "inputSchema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
        return json.dumps(fastmcp_payload, indent=2)

    except ValidationError as ve:
        print(f"Pydantic Validation Error: {ve}", file=sys.stderr)
        raise

if __name__ == "__main__":
    sample_tool = {
        "tool_name": "execute_pytest_suite",
        "description": "Runs targeted unit tests using pytest with coverage reporting.",
        "parameters": [
            {
                "name": "test_path",
                "param_type": "string",
                "description": "Path to test file or directory",
                "is_required": True
            },
            {
                "name": "fail_fast",
                "param_type": "boolean",
                "description": "Stop execution on first failed test",
                "is_required": False
            }
        ],
        "timeout_seconds": 60
    }

    print(generate_fastmcp_registration(sample_tool))
```

### FastMCP 3.1 Server Integration
This snippet shows a FastMCP 3.1 Python server that exposes custom tool capabilities directly to Claude Code:

```python
import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("ClaudeCodeIntegrationServer")

class RefactorRequest(BaseModel):
    filepath: str = Field(description="Target source code file")
    refactor_instructions: str = Field(description="Instructions for restructuring")

class RefactorResult(BaseModel):
    filepath: str
    status: str
    changes_made: int

@mcp.tool()
async def trigger_automated_refactor(request: RefactorRequest) -> RefactorResult:
    """Triggers an automated code refactoring task for Claude Code."""
    await asyncio.sleep(0.05)  # Simulate execution

    return RefactorResult(
        filepath=request.filepath,
        status="COMPLETED",
        changes_made=14
    )

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Aider](aider.md) — Command-line AI programming tool leveraging Git repository state.
- [Devin](devin.md) — Autonomous agent platform with a dedicated workspace, terminal, and browser environment.
- [Roo Code](../agents/roo-code.md) — Highly customizer-friendly VS Code agent extension.
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Conceptual patterns governing model tool calling.
- [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) — The lightweight framework used to build secure extension backends.

## Sources / references
- [Anthropic Claude Code Official Documentation](https://code.claude.com/)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.io/spec)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
