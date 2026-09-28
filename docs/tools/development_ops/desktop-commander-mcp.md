# Desktop Commander MCP

## What it is
Desktop Commander MCP (v3.1+) is a privacy-first, local-first Model Context Protocol (FastMCP 3.1) server designed to equip AI agents—such as **Claude 5.6**, **GPT-5.6**, **Cursor**, and **OpenCode**—with local terminal control, granular filesystem navigation, surgical text editing, and process management capabilities. Built to operate as the "local hands" for frontier reasoning models, Desktop Commander strictly eliminates external analytics, telemetry tracking, and unauthorized network calls, providing a zero-trust execution bridge between LLM reasoning engines and local developer workstations.

Through its native implementation of the FastMCP 3.1 Task Protocol, Desktop Commander provides high-performance code search via `ripgrep`, idempotent search-and-replace text modifications via git-merge diff syntax (`edit_block`), background process monitoring, and host whitelist security enforcement.

## What problem it solves
Granting autonomous agents direct access to local developer workstations presents critical security, privacy, and operational challenges:
- **Telemetry & Data Leakage**: Standard cloud-bound developer tools frequently transmit shell logs, environment variables, and proprietary code snippets to external telemetry endpoints.
- **Coarse File Overwrites**: Early file-editing tools required agents to re-write entire source code files for minor changes, leading to elevated token costs, high latency, truncated files, and frequent indentation errors.
- **Unchecked Process Execution**: Unconstrained agent execution can spawn runaway processes, consume system memory, or execute destructive commands (e.g., `rm -rf /` or unvalidated database drops).
- **Context Fragmentation**: Agents struggle to search large repositories efficiently without native integration into ultra-fast local search utilities like `ripgrep`.

Desktop Commander MCP resolves these challenges by serving as an open, auditable, on-device proxy. It enforces explicit directory whitelisting, provides atomic patch-editing tools (`edit_block`), and executes process monitoring locally without transmitting external tracking telemetry.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Local Execution Layer & Agent OS Interface.

Desktop Commander MCP sits at the **System Operations Gateway**, bridging LLM agent orchestrators (running in MCP hosts like Claude Desktop, Cursor, or OpenCode) and the underlying host operating system (POSIX/Windows filesystem, process manager, and CLI shell).

```
+-----------------------------------------------------------------------+
|                       LLM Agent Host Environment                      |
|       (Claude 5.6 / Cursor / OpenCode / Custom FastMCP Client)        |
+-----------------------------------------------------------------------+
                                   |
                                   | FastMCP 3.1 Tool Call (JSON-RPC)
                                   v
+-----------------------------------------------------------------------+
|                    Desktop Commander MCP Server                       |
|                                                                       |
|  +--------------------+  +--------------------+  +-----------------+  |
|  | Path Whitelist Gate|  | ripgrep Search Engine| | Surgical Edit   |  |
|  +--------------------+  +--------------------+  +-----------------+  |
|  +-----------------------------------------------------------------+  |
|  | Process Lifecycle & Terminal Shell Manager                      |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
                                   |
                                   | Local POSIX / Windows System Calls
                                   v
+-----------------------------------------------------------------------+
|                      Host Operating System                            |
|             (Filesystem / Terminal Shell / Ripgrep / Git)             |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Surgical Refactoring in Large Repositories**: Applying precise line-level code replacements across multi-file codebases using git merge diff `edit_block` operations without rewriting whole files.
- **Privacy-Sensitive Workspace Operations**: Running autonomous developer agents in air-gapped or highly regulated enterprise environments where telemetry tracking is strictly prohibited.
- **Local Environment Management & Builds**: Executing terminal build commands (`npm test`, `cargo build`, `pytest`), monitoring background processes, and diagnosing build failures.
- **High-Speed Repository Code Search**: Utilizing native `ripgrep` integrations to locate function definitions, variable usages, and architectural patterns across massive codebases in sub-milliseconds.
- **Automated Configuration & Schema Updates**: Managing local Docker containers, updating local environment configurations, and maintaining local Markdown documentation trees.

## Strengths
- **Zero Telemetry / Absolute Privacy**: Designed specifically with zero analytics or external tracking; operates 100% on-device.
- **FastMCP 3.1 Native**: Fully implements the FastMCP 3.1 Task Protocol, resource discovery, and tool registration interfaces.
- **Surgical `edit_block` Operations**: Employs git-style merge conflict markers (`<<<<<<< SEARCH`, `=======`, `>>>>>>> REPLACE`) for deterministic, low-token file editing.
- **Granular Directory Whitelisting**: Allows administrators and users to restrict agent file access to explicit host directory trees (`ALLOWED_DIRECTORIES`).
- **High-Performance Code Search**: Direct binding to native `ripgrep` binaries for lightning-fast regex search across massive repositories.

## Limitations
- **User-Level Permission Bound**: Operates with the exact permissions of the operating system user running the process; lacks hardware virtualization or container-level isolation on its own.
- **Manual Whitelist Configuration**: Requires explicit configuration of allowed environment paths to prevent accidental system file access.
- **Local Execution Target**: Optimized for local workstation execution; remote server management requires additional SSH or containerized tunneling setups.

## When to use it
- When providing LLM agents with filesystem and terminal access on your personal workstation or corporate developer machine.
- When working on private or proprietary codebases where cloud telemetry transmission is banned by security policy.
- When performing multi-file refactoring tasks where whole-file overwrites are too slow, token-heavy, or prone to corruption.

## When not to use it
- In multi-tenant untrusted cloud environments where full OS-level container isolation is required (consider containerized sandboxes like [Claude Code Container MCP](claude-code-container-mcp.md)).
- For browser-based visual web automation tasks (use [Playwright](playwright.md) instead).

## Getting started

### 1. Global Installation
Install Desktop Commander MCP globally using Node.js:

```bash
npm install -g @democratize-technology/desktop-commander-mcp
```

### 2. Configuration for Claude Desktop / Cursor
Add Desktop Commander MCP to your MCP configuration file (e.g., `~/.config/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "desktop-commander": {
      "command": "desktop-commander-mcp",
      "args": [],
      "env": {
        "ALLOWED_DIRECTORIES": "/home/developer/projects:/tmp/agent-workspace",
        "ENABLE_PROCESS_MANAGER": "true"
      }
    }
  }
}
```

### 3. Verification
Verify server initialization and tool exposure by listing available tools via standard CLI utilities:

```bash
npx @modelcontextprotocol/inspector desktop-commander-mcp
```

## CLI examples

### 1. Running Server on Specific Port
Start the server in HTTP/SSE socket mode for debugging or custom FastMCP client connections:

```bash
desktop-commander-mcp --port 3100 --allowed-dirs "/home/user/code"
```

### 2. Validating Allowed Directory Access
Inspect the active directory security restrictions applied to the current server instance:

```bash
desktop-commander-mcp --list-allowed
```

### 3. Executing Code Search via FastMCP CLI
Run a code search query using the client CLI wrapper:

```bash
mcp-cli call desktop-commander search_code '{"query": "def parse_ast", "include": ["*.py"]}'
```

## API examples

### 1. FastMCP 3.1 Tool Server Implementation (Python)
The following Python script illustrates how Desktop Commander MCP exposes surgical editing, ripgrep searching, and command execution as a FastMCP 3.1 server:

```python
import os
import subprocess
import re
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

mcp = FastMCP(
    "Desktop Commander MCP",
    version="3.1.0",
    description="Privacy-first FastMCP 3.1 server for local workspace file editing, ripgrep search, and terminal command execution."
)

ALLOWED_DIRECTORIES = os.getenv("ALLOWED_DIRECTORIES", os.getcwd()).split(":")

def is_path_allowed(target_path: str) -> bool:
    abs_target = os.path.abspath(target_path)
    return any(abs_target.startswith(os.path.abspath(allowed)) for allowed in ALLOWED_DIRECTORIES)

class EditBlockRequest(BaseModel):
    path: str = Field(..., description="Target file path relative to workspace root")
    edit_content: str = Field(..., description="Merge diff string formatted with <<<<<<< SEARCH, =======, >>>>>>> REPLACE")

    @field_validator("edit_content")
    @classmethod
    def validate_diff_structure(cls, v: str) -> str:
        if "<<<<<<< SEARCH" not in v or "=======" not in v or ">>>>>>> REPLACE" not in v:
            raise ValueError("Edit payload must contain valid merge diff markers: <<<<<<< SEARCH, =======, >>>>>>> REPLACE")
        return v

@mcp.tool()
async def edit_block(request: EditBlockRequest) -> Dict[str, Any]:
    """
    Surgically replaces text inside a target file using git-merge diff syntax.
    """
    if not is_path_allowed(request.path):
        return {"success": False, "error": f"Path access denied: {request.path}"}

    if not os.path.exists(request.path):
        return {"success": False, "error": f"Target file does not exist: {request.path}"}

    with open(request.path, "r", encoding="utf-8") as f:
        file_content = f.read()

    # Extract SEARCH and REPLACE blocks
    try:
        search_block = request.edit_content.split("<<<<<<< SEARCH\n")[1].split("\n=======\n")[0]
        replace_block = request.edit_content.split("\n=======\n")[1].split("\n>>>>>>> REPLACE")[0]
    except IndexError:
        return {"success": False, "error": "Malformed edit block syntax."}

    if search_block not in file_content:
        return {"success": False, "error": "SEARCH block content not found in target file."}

    updated_content = file_content.replace(search_block, replace_block, 1)

    with open(request.path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return {"success": True, "message": f"Successfully updated {request.path}"}

@mcp.tool()
async def search_codebase(query: str, path: str = ".") -> Dict[str, Any]:
    """
    Performs high-speed pattern search using ripgrep.
    """
    if not is_path_allowed(path):
        return {"success": False, "error": f"Path access denied: {path}"}

    try:
        cmd = ["rg", "--json", "-M", "500", query, path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return {"success": True, "raw_output": result.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run()
```

### 2. Pydantic v2 Command Execution Guardrail Schema
Enforce strict validation and command blacklisting before dispatching terminal commands:

```python
import re
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class TerminalCommandPayload(BaseModel):
    """
    Strict Pydantic v2 schema for validating terminal command execution requests.
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    command: str = Field(..., min_length=1, description="The CLI command to execute")
    working_directory: str = Field(default=".", description="Target execution directory")
    timeout_seconds: int = Field(default=30, ge=1, le=300, description="Process timeout limit")
    environment_vars: Optional[dict] = Field(default_factory=dict, description="Additional environment variables")

    @field_validator("command")
    @classmethod
    def check_blacklisted_commands(cls, cmd: str) -> str:
        prohibited_patterns = [
            r"rm\s+-rf\s+/",
            r"mkfs",
            r"dd\s+if=",
            r":\(\)\{\s*:\|:&\s*\};:", # fork bomb
            r"shutdown",
            r"reboot"
        ]
        for pattern in prohibited_patterns:
            if re.search(pattern, cmd, re.IGNORECASE):
                raise ValueError(f"Prohibited high-risk command detected: '{pattern}'")
        return cmd

if __name__ == "__main__":
    sample_request = {
        "command": "pytest tests/unit/test_mcp.py --maxfail=1",
        "working_directory": "/home/developer/projects/mcp-server",
        "timeout_seconds": 60
    }

    validated = TerminalCommandPayload.model_validate(sample_request)
    print("Terminal command successfully validated against Pydantic v2 security schema!")
    print(f"Command: {validated.command}")
    print(f"Directory: {validated.working_directory}")
```

## Related tools / concepts
- [Claude Code](claude-code.md) — Anthropic's terminal-native developer agent.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Open protocol connecting LLMs with Desktop Commander tools.
- [Claude Code Container MCP](claude-code-container-mcp.md) — Isolated containerized alternative for untrusted code execution.
- [Aider](aider.md) — Git-integrated CLI pair programming tool.
- [ripgrep (rg)](ripgrep.md) — Fast line-oriented search tool integrated into Desktop Commander.
- [Zed](zed.md) — High-performance code editor featuring native FastMCP client integration.

## Sources / references
- [Desktop Commander MCP GitHub Repository](https://github.com/democratize-technology/DesktopCommanderMCP)
- [Model Context Protocol (FastMCP 3.1) Specification](https://modelcontextprotocol.io/)
- [ripgrep Documentation](https://github.com/BurntSushi/ripgrep)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
