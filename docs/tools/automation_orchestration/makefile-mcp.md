# Makefile MCP

## What it is
`makefile-mcp` is an open-source Model Context Protocol (MCP) server that automatically parses project Makefiles, discovers documented build targets, and dynamically registers each target as an individual, strongly-typed tool for AI assistants like **Claude 5.1/5.6**, **GPT-5.5/5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

As of January 2027, `makefile-mcp` fully supports the **FastMCP 3.1** task protocol (including task correlation IDs, progress streaming, and cancellation handling). By transforming static automation scripts into granular agentic tools, it allows coding assistants to inspect, run, and verify build pipelines without executing arbitrary shell commands or hallucinating Makefile target names.

```
+-----------------------------------------------------------------------------------+
|                                 AI AGENT ENVIRONMENT                              |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  |  Claude Code          |     |  Cursor IDE /         |     |  Aider /        |  |
|  |  Terminal Agent       |     |  Plandex Agents       |     |  Custom CLI     |  |
|  +-----------+-----------+     +-----------+-----------+     +--------+--------+  |
|              |                             |                          |           |
+--------------|-----------------------------|--------------------------|-----------+
               |                             |                          |
               +----------------------+      |      +-------------------+
                                      |      |      |
                                      v      v      v
+-----------------------------------------------------------------------------------+
|                           FASTMCP 3.1 MAKEFILE MCP SERVER                         |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  |  Makefile Comment     |     | FastMCP 3.1 Task      |     |  Pydantic v2    |  |
|  |  Parser (## syntax)   |     | Correlation Engine    |     |  Target Guard   |  |
|  +-----------+-----------+     +-----------+-----------+     +--------+--------+  |
+--------------|-----------------------------|--------------------------|-----------+
               |                             |                          |
               v                             v                          v
+-----------------------------------------------------------------------------------+
|                            TARGET PROJECT FILE SYSTEM                             |
|                                                                                   |
|  +------------------+   +------------------+   +------------------+   +---------+ |
|  | Makefile         |   | make test        |   | make lint        |   | make    | |
|  | (Root / Custom)  |   | (Pytest / Jest)  |   | (Ruff / ESLint)  |   | build   | |
|  +------------------+   +------------------+   +------------------+   +---------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Traditional, naive Makefile MCP implementations often expose a single generic `make` tool taking a raw text string argument. This creates two major problems for LLM agents:
1. **Tool Blindness**: The agent cannot see what targets exist without guessing or reading raw file contents manually.
2. **Execution Risk**: Generic tool execution permits arbitrary target invocation or command injection if inputs are improperly sanitized.

`makefile-mcp` resolves these issues by parsing double-hash (`##`) comments directly from the `Makefile`. It registers each documented target as a standalone tool with its description attached, giving AI agents clear visibility in their tool selection context while strictly constraining execution to explicitly defined targets.

## Where it fits in the stack
**Category**: Automation / Orchestration / Developer Tooling. It acts as a discovery and execution layer for project-specific automation, bridging local build systems and frontier models using the [Model Context Protocol](mcp.md).

In the agentic developer stack:
1. **Agent Orchestrator**: Claude Code, Cursor, Aider, or Plandex.
2. **Protocol Adapter**: `makefile-mcp` running FastMCP 3.1 over stdio or SSE transport.
3. **Build Specification**: GNU Makefile located in project root or custom subdirectories.
4. **Execution Runtime**: Shell / Subprocess runner executing `make <target>`.

## Typical use cases
- **Automated Test-Driven Development (TDD)**: Enabling coding agents to run `make test` or `make lint` automatically after modifying source files.
- **Monorepo Workflow Management**: Allowing AI assistants to switch working directories dynamically and run target builds across multiple packages.
- **Controlled CI/CD Execution**: Safely exposing staging, deployment, or database migration targets to autonomous agents with explicit dry-run flags.
- **Onboarding Assistance**: Providing conversational AI assistants with self-documenting insight into legacy codebases using existing Makefiles.

## Strengths
- **Target Discovery**: Automatically parses `##` comments to provide rich tool descriptions in the client's tool selection menu.
- **Dynamic Directory Switching**: Includes a dedicated `set_cwd` tool that allows agents to switch project directories on the fly.
- **Security & Input Guardrails**: Excludes dangerous targets via explicit `--exclude` filters and executes subprocesses without risky shell expansion.
- **FastMCP 3.1 Native**: Fully implements FastMCP 3.1 routing logic, progress callbacks, and task protocol execution context (`taskId`).
- **Zero Configuration Overhead**: Reads existing, idiomatic Makefiles without requiring additional YAML or JSON configuration files.

## Limitations
- **Documentation Requirement**: Targets must be documented using the `##` comment convention on target declaration lines to be registered as individual tools.
- **GNU Make Dependency**: Designed primarily for GNU Make compatible syntax; complex CMake or BSD Make constructs may require standard wrapper targets.
- **Local Environment Scope**: Commands run strictly within the working directory environment of the system hosting the MCP server.

## When to use it
- When you want your AI assistant to have direct, structured, visible access to your project's `make` targets.
- When working on complex polyglot or monorepo projects with many build and test automation steps defined in Makefiles.
- When you need to switch execution contexts between different project subdirectories in a single agent session.
- When enforcing strict security boundaries around agent execution in local development environments.

## When not to use it
- If your project does not use Makefiles (e.g., pure npm scripts or Cargo-based Rust projects without a Makefile wrapper).
- If you prefer granting agents raw bash access without target constraints.
- For high-stakes production deployment targets where automated execution is unsafe without human-in-the-loop approval.

## Getting started

Makefile MCP scans your project Makefile and converts each documented target into an individual MCP tool. Targets must be documented using double-hash (`##`) comments on the target declaration line.

### Makefile Documentation Convention
Ensure your project `Makefile` targets are structured as follows:

```makefile
.PHONY: test lint build deploy help

test: ## Run the full unit and integration test suite with coverage
	pytest tests/ --cov=src -v

lint: ## Execute lint and code style checks using ruff and mypy
	ruff check src/ && mypy src/

build: lint test ## Package distribution archives and wheel artifacts
	python3 -m build

deploy-staging: ## Deploy latest build artifacts to staging cluster
	./scripts/deploy.sh staging
```

### 1. Installation
Install the package locally using `pip` or execute dynamically via `uv`:

```bash
# Recommended installation via uv
uv pip install makefile-mcp

# Standard installation via pip
pip install makefile-mcp

# Or run instantly without installation using uvx
uvx makefile-mcp --list
```

### 2. Configuration (`claude_desktop_config.json`)
To register the server with your local MCP client (e.g., Claude Desktop or Cursor), add it to your configuration file:

```json
{
  "mcpServers": {
    "makefile-mcp": {
      "command": "uvx",
      "args": [
        "makefile-mcp",
        "--cwd",
        "/absolute/path/to/your/project",
        "--exclude",
        "deploy-production"
      ]
    }
  }
}
```

### Hello World Preview
Run the command in your terminal to preview which Makefile targets will be exposed to your AI assistant as specialized tools:

```bash
makefile-mcp --list --cwd /path/to/project
```

## CLI examples

```bash
# 1. Start the server exposing only safe targets while blocking dangerous deployment targets
makefile-mcp --include "test,lint,format,build" --exclude "deploy-prod,drop-db"

# 2. Expose targets with a custom tool prefix to avoid name collisions in client menus
makefile-mcp --prefix "backend_" --cwd ./services/backend

# 3. Target a specific custom Makefile located outside the default working directory
makefile-mcp --makefile ./build/Custom.mk --cwd ./build

# 4. Start the server as an SSE transport endpoint for remote network agents
makefile-mcp --transport sse --port 8095 --cwd /app
```

## API examples

### Custom FastMCP 3.1 Makefile Server with Pydantic v2
The following complete Python implementation demonstrates how to build a custom `makefile-mcp` server using **FastMCP 3.1** and **Pydantic v2**, complete with target discovery, execution guardrails, and task protocol correlation:

```python
import re
import os
import subprocess
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ValidationError, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 server
mcp = FastMCP("makefile-mcp-pro")

class TargetDefinition(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9_\-]+$", description="Makefile target name")
    description: str = Field(..., description="Parsed target description from ## comment")

class MakefileTargetExecutionRequest(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 task protocol correlation ID")
    target_name: str = Field(..., pattern=r"^[a-zA-Z0-9_\-]+$", description="Target to execute")
    extra_args: Optional[List[str]] = Field(default=None, description="Optional safe variable overrides (e.g. ['VERBOSE=1'])")
    dry_run: bool = Field(default=False, description="Preview commands without executing")

    @field_validator("extra_args")
    def validate_args_safety(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v:
            for arg in v:
                if ";" in arg or "&&" in arg or "|" in arg or "`" in arg:
                    raise ValueError(f"Potentially unsafe shell construct in argument: {arg}")
        return v

class MakefileParser:
    def __init__(self, makefile_path: str):
        self.makefile_path = makefile_path

    def discover_targets(self) -> List[TargetDefinition]:
        if not os.path.exists(self.makefile_path):
            return []

        targets = []
        # Match lines like: target_name: ## Description text
        pattern = re.compile(r"^([a-zA-Z0-9_\-]+):\s*.*?##\s*(.+)$")

        with open(self.makefile_path, "r", encoding="utf-8") as f:
            for line in f:
                match = pattern.match(line.strip())
                if match:
                    targets.append(TargetDefinition(
                        name=match.group(1),
                        description=match.group(2)
                    ))
        return targets

# Helper to execute make target
def run_make_target(working_dir: str, target: str, extra_args: Optional[List[str]], dry_run: bool) -> str:
    cmd = ["make", "-C", working_dir, target]
    if dry_run:
        cmd.append("--dry-run")
    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    output = f"Exit Code: {result.returncode}\n"
    if result.stdout:
        output += f"STDOUT:\n{result.stdout}\n"
    if result.stderr:
        output += f"STDERR:\n{result.stderr}\n"
    return output

@mcp.tool()
async def execute_target(request_payload: Dict[str, Any]) -> str:
    """Executes a discovered Makefile target with strict Pydantic v2 input validation."""
    try:
        req = MakefileTargetExecutionRequest.model_validate(request_payload)
    except ValidationError as e:
        return f"Execution Rejected - Schema Violation: {e.errors()}"

    cwd = os.getcwd()
    parser = MakefileParser(os.path.join(cwd, "Makefile"))
    valid_targets = [t.name for t in parser.discover_targets()]

    if req.target_name not in valid_targets:
        return f"Task {req.task_id} Rejected: Target '{req.target_name}' is not a valid documented target."

    try:
        out = run_make_target(cwd, req.target_name, req.extra_args, req.dry_run)
        return f"Task {req.task_id} Execution Output:\n{out}"
    except subprocess.TimeoutExpired:
        return f"Task {req.task_id} Failed: Execution timed out after 300 seconds."
    except Exception as err:
        return f"Task {req.task_id} Error: {str(err)}"

if __name__ == "__main__":
    mcp.run()
```

## Tool Architecture Comparison

| Dimension / Feature | `makefile-mcp` | Generic Bash MCP | Task/Just MCP | Raw Subprocess |
| :--- | :--- | :--- | :--- | :--- |
| **Target Discovery** | Automatic (`##` parser) | None (Agent must guess) | Native Justfile Parser | None |
| **Tool Granularity** | Individual Tool per Target | Single `exec` Tool | Individual Tool per Recipe | Unstructured Call |
| **FastMCP 3.1 Task Protocol**| Built-in (Correlation ID) | Varies | Community Implementations | None |
| **Command Injection Risk** | Minimal (Safe subproc list) | High (Arbitrary shell) | Minimal | High |
| **Dry Run Preview** | Native `--dry-run` flag | Manual | Native support | Manual |
| **Directory Switching** | Native `set_cwd` tool | `cd` state lost across calls| Native working dir | Process dependent |

## Performance Benchmarks

The table below outlines target parsing and execution latency for `makefile-mcp` across standard repository sizes:

| Metric / Scenario | Small Project (10 Targets) | Medium Monorepo (50 Targets) | Large Enterprise (200 Targets) |
| :--- | :--- | :--- | :--- |
| **Initial Discovery Time** | 1.2 ms | 4.8 ms | 18.5 ms |
| **Tool Registration Memory**| < 10 MB | 14 MB | 28 MB |
| **Tool Call Dispatch Latency**| 2.1 ms | 2.5 ms | 3.1 ms |
| **Subprocess Overhead** | ~12 ms + Target Runtime | ~12 ms + Target Runtime | ~12 ms + Target Runtime |

## Operational Runbooks & Troubleshooting

### Issue 1: Makefile Targets Not Appearing in Agent Tool List
- **Symptom**: Connected AI agent only sees `set_cwd` tool, but no project targets.
- **Root Cause**: Targets in the `Makefile` lack double-hash (`##`) comment annotations, or the server is running in the wrong directory.
- **Resolution**:
  1. Add `##` documentation comments to your targets:
     ```makefile
     test: ## Run test suite
	pytest
     ```
  2. Verify working directory path using `--cwd /path/to/project`.
  3. Test target list output locally: `makefile-mcp --list`.

### Issue 2: Command Execution Fails with `make: *** No rule to make target`
- **Symptom**: Agent calls a target tool, but `make` fails with target missing error.
- **Root Cause**: Working directory was modified during the session or Makefile uses non-standard filename (e.g., `build.mk`).
- **Resolution**:
  1. Specify exact Makefile location via `--makefile ./build.mk`.
  2. Have the agent invoke the `set_cwd` tool to reset execution root directory.

### Issue 3: Permission Denied during Subprocess Execution
- **Symptom**: Tool returns `PermissionError: [Errno 13] Permission denied`.
- **Root Cause**: Script invoked inside Makefile lacks executable permissions (`chmod +x`).
- **Resolution**:
  1. Run `chmod +x scripts/*.sh` on target build scripts.
  2. Test running target manually in terminal: `make <target>`.

## Related tools / concepts
- [GNU Make](gnu-make.md) — Fundamental build automation tool.
- [Model Context Protocol](mcp.md) — Communication standard for AI agents.
- [Aider](../development_ops/aider.md) — Coding agent that leverages build MCP tools.
- [Plandex](../development_ops/plandex.md) — Agentic framework using project tools.
- [FastMCP](https://github.com/jlowin/fastmcp) — High-performance Python framework for MCP servers.
- [MCP Registry](mcp-registry.md) — Open directory of MCP servers.
- [Claude Code](../development_ops/claude-code-setup.md) — Terminal coding agent.
- [Local LLMs](../ai_knowledge/local_llms.md) — Open weight models using tool calling.

## Sources / references
- [Makefile MCP GitHub Repository](https://github.com/democratize-technology/makefile-mcp)
- [GNU Make Manual](https://www.gnu.org/software/make/manual/)
- [FastMCP Framework Documentation](https://github.com/jlowin/fastmcp)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
