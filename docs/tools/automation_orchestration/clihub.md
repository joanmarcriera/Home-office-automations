# CliHub

## What it is
CliHub is a code generator, protocol compiler, and AST synthesis tool that connects to a Model Context Protocol (MCP / FastMCP 3.1) server and compiles a portable, standalone, zero-dependency CLI binary in Go or Rust. Every tool, prompt, and resource exposed by the FastMCP 3.1 server is automatically mapped into strongly typed subcommands, flags, and help menus within the target executable.

By converting dynamic JSON-RPC protocol connections into compiled native binaries, CliHub enables developers to "freeze" complex agentic tool suites into deterministic DevOps binaries. It eliminates session setup latency, removes Node.js/Python runtime dependencies from runner environments, and allows shell-based AI agents (such as Claude 5.1 Desktop, Claude Code, and GPT-5.5 Shell Agents) to invoke MCP tools as standard terminal commands with sub-10 millisecond execution overhead.

```
+---------------------------------------------------------------------------------------------------+
|                                     CLIHUB COMPILATION ENGINE                                    |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +---------------------------+     +-------------------------------+     +---------------------+  |
|  | FastMCP 3.1 Tool Server   |     | CliHub Introspection Engine   |     | Abstract Syntax Tree|  |
|  | (Stdio, SSE, WebSockets)  | --> | (JSON-RPC `tools/list` Probe) | --> | (Go / Rust Generator)|  |
|  +---------------------------+     +-------------------------------+     +---------------------+  |
|                                                                                    |              |
|                                                                                    v              |
|  +---------------------------------------------------------------------------------------------+  |
|  |                                  NATIVE AST BINARY COMPILER                                 |  |
|  +---------------------------------------------------------------------------------------------+  |
|  | - Tool Schema -> Flag Mapping        - Output Formatter (JSON/YAML/Table)                  |  |
|  | - Auth Secret Injection              - Cross-Compilation (Linux/macOS/Windows)             |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                |                                                  |
|                                                v                                                  |
|  +---------------------------------------------------------------------------------------------+  |
|  |                                STANDALONE ZERO-DEP BINARY                                   |  |
|  +-------------------------------+-------------------------------+-----------------------------+  |
|  | CI/CD Runner Scripts          | Agent Shell Pipelines         | Local Developer Terminal    |  |
|  | (GitHub Actions, GitLab CI)   | (Claude Code, Auto-Dev Ops)   | (Fast Terminal Debugging)   |  |
|  +-------------------------------+-------------------------------+-----------------------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## What problem it solves
While dynamic MCP clients (such as Claude Desktop or Cursor) excel in interactive, stateful chat sessions, using live MCP client connections inside automated background runners and high-frequency shell loops introduces operational friction:

- **High Runtime Overhead**: Standard MCP client startup requires launching Python virtual environments or Node.js runtime engines, negotiating transport handshakes, and exchanging protocol initialization schemas for every batch execution.
- **Dependency Drift & Version Instability**: Running raw MCP tool packages directly in CI/CD runner steps exposes pipelines to unexpected updates, breaking package dependencies, or missing system libraries.
- **Complex Orchestration in Shell Scripts**: Calling raw MCP tools from standard bash or zsh scripts requires verbose JSON payload construction, stdio piping, and manual JSON parsing.
- **Token Consumption Overhead**: Passing entire FastMCP tool JSON schemas into LLM context windows repeatedly consumes token budget. CliHub converts tool interfaces into standard `CLI --help` text, dramatically reducing prompt token usage.

## Where it fits in the stack
**Category**: Automation & Orchestration Tooling / Protocol Compiler.

CliHub acts as a build-time compiler that transforms dynamic FastMCP 3.1 protocols into native shell executables across the DevOps and agent ecosystem:

```
+-----------------------------------------------------------------------------------+
|                             ENTERPRISE STACK PLACEMENT                            |
+-----------------------------------------------------------------------------------+
| Autonomous Agent Layer    | Claude Code, Auto-Dev-Ops, Local Bash Scripting       |
+---------------------------+-------------------------------------------------------+
| CLI Execution Layer       | CliHub Generated Static Executables (e.g., jira-cli)  |
+---------------------------+-------------------------------------------------------+
| Protocol Introspection    | FastMCP 3.1 JSON-RPC AST Schema Parser               |
+---------------------------+-------------------------------------------------------+
| MCP Server Layer          | Jira, GitHub, ServiceNow, PostgreSQL MCP Tools        |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Packaging Enterprise MCP Tool Suites**: Compiling heavy MCP tool packages (e.g., Atlassian Jira, GitHub, ServiceNow) into tiny, self-contained binaries for CI/CD runners.
- **Token-Efficient Agentic Execution**: Replacing large system prompt tool declarations with lightweight CLI binary calls executed by terminal agents.
- **DevOps Batch Automation**: Ingesting complex incident management or infrastructure provisioning MCP tools directly into shell scripts without requiring active MCP server processes.
- **FastMCP Server Debugging**: Testing FastMCP 3.1 server endpoints from terminal tabs with autocomplete flags and structured table outputs.

## Strengths
- **Sub-10ms Native Execution**: Converts transport handshakes into instant command executions by bundling communication or embedded stdio runners directly into static binaries.
- **Zero Runtime Dependencies**: Generates single Go or Rust binaries that require no installed Python interpreters, Node.js packages, or Docker containers on target machines.
- **Multi-Platform Cross Compilation**: Built-in support for `GOOS` and `GOARCH` flags allows compiling binaries for Linux ARM64, macOS Apple Silicon, and Windows x86_64 from a single build machine.
- **Automated Help & Autocomplete**: Converts FastMCP 3.1 tool descriptions and JSON schemas into formatted CLI man pages, shell autocomplete files, and flag descriptions.

## Limitations
- **Static Schema Snapshot**: The compiled CLI reflects the MCP server tool schema at the build timestamp; changes to the underlying MCP server require running `clihub generate` to update the binary.
- **Stateless Tool Calls**: Each CLI command execution opens and closes its session; tools relying on persistent multi-step memory sessions require handling state externally or passing session tokens as flags.

## When to use it
- When distributing MCP agent tools to non-technical end users who need simple terminal commands.
- When executing MCP capabilities inside containerized CI/CD runners or serverless functions where fast cold-start performance is critical.
- When creating versioned, immutable tool suites for automated agent deployments.

## When not to use it
- When an application requires continuous streaming WebSocket sessions or stateful multi-call memory contexts.
- When tool schemas change dynamically on a second-by-second basis at runtime.

## Architectural overview
CliHub introspection operates by connecting to a target FastMCP 3.1 transport endpoint (stdio, HTTP/SSE, or WebSocket), emitting the JSON-RPC `tools/list` protocol request, and parsing the returned JSON schemas. CliHub then maps each tool parameter into Go/Rust struct fields with CLI tag annotations (such as Cobra or Clap flags). During compilation, CliHub injects serialization logic that converts incoming CLI flags into valid FastMCP JSON-RPC request payloads and formats tool return data into JSON, YAML, or human-readable ASCII tables.

## Getting started

### Installation
Install CliHub using the Go toolchain or downloading a release binary:

```bash
# Install latest release via Go
go install github.com/thellimist/clihub@latest

# Verify installation
clihub --version
```

### Compiling a Local Stdio FastMCP 3.1 Server
Converting a Node-based Jira MCP server into a static Go binary:

```bash
# Compile a local MCP server into a binary named 'jira-cli'
clihub generate \
  --name jira-cli \
  --transport stdio \
  --command "npx -y @anthropic-ai/mcp-server-atlassian" \
  --output ./bin/jira-cli
```

## CLI examples

```bash
# 1. Generating a static CLI from a remote SSE FastMCP 3.1 server
clihub generate \
  --name remote-k8s-cli \
  --transport sse \
  --url "https://mcp-k8s.internal.net/sse" \
  --output ./bin/k8s-cli

# 2. Executing generated commands with output formatting flags
./bin/jira-cli get_issue --key PROJ-4589 --output json

# 3. Invoking search tools with query flags
./bin/jira-cli search_issues --jql "project = PROJ AND status = Open" --output table

# 4. Cross-compiling a tool suite for Linux ARM64 production runners
GOOS=linux GOARCH=arm64 clihub generate \
  --name servicenow-runner \
  --transport stdio \
  --command "python3 -m mcp_server_servicenow" \
  --output ./dist/servicenow-runner-linux-arm64

# 5. Inspecting compiled tool subcommands
./bin/jira-cli --help
```

## API examples

### FastMCP 3.1 Compilation Pipeline Implementation
The following Python script illustrates how an orchestration framework configures, validates, and invokes CliHub compilation pipelines programmatically using **FastMCP 3.1** patterns:

```python
"""
CliHub Compiler Orchestration FastMCP 3.1 Server
Exposes tools for compiling FastMCP servers into native binaries programmatically.
"""

import json
import os
import subprocess
import logging
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, HttpUrl, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clihub-compiler")

# Initialize FastMCP Server
mcp = FastMCP(
    "CliHub Compiler Server",
    version="3.1.0",
    description="FastMCP 3.1 server for programmatically compiling MCP tools into binaries"
)

class CompilationTarget(BaseModel):
    binary_name: str = Field(..., description="Target name of output binary")
    transport_type: str = Field("stdio", pattern="^(stdio|sse|websocket)$")
    mcp_command: Optional[str] = Field(None, description="Command string for stdio servers")
    sse_url: Optional[HttpUrl] = Field(None, description="Target SSE URL for remote servers")
    target_os: str = Field("linux", pattern="^(linux|darwin|windows)$")
    target_arch: str = Field("amd64", pattern="^(amd64|arm64)$")
    output_directory: str = Field("./build", description="Directory to store compiled executable")

class CompilationResult(BaseModel):
    success: bool
    binary_path: str
    target_platform: str
    compiled_subcommands: List[str]
    stdout_log: str

@mcp.tool()
def compile_mcp_binary(target: CompilationTarget) -> str:
    """
    Compile a target FastMCP 3.1 server into a standalone CLI executable.
    """
    logger.info(f"Starting compilation for {target.binary_name} ({target.target_os}/{target.target_arch})")

    os.makedirs(target.output_directory, exist_ok=True)
    out_path = os.path.join(target.output_directory, target.binary_name)

    cmd = ["clihub", "generate", "--name", target.binary_name, "--transport", target.transport_type, "--output", out_path]

    if target.transport_type == "stdio" and target.mcp_command:
        cmd.extend(["--command", target.mcp_command])
    elif target.transport_type == "sse" and target.sse_url:
        cmd.extend(["--url", str(target.sse_url)])

    env = os.environ.copy()
    env["GOOS"] = target.target_os
    env["GOARCH"] = target.target_arch

    # Mock compilation execution for safe sandbox environment execution
    mock_subcommands = ["list_resources", "execute_tool", "get_status"]
    result = CompilationResult(
        success=True,
        binary_path=out_path,
        target_platform=f"{target.target_os}/{target.target_arch}",
        compiled_subcommands=mock_subcommands,
        stdout_log="Compilation finished successfully via CliHub AST engine."
    )

    return result.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

### Compilation Build Schema Validation using Pydantic v2
This production script enforces strict schema validation for CliHub compilation targets and environmental parameters:

```python
"""
CliHub Compilation Build Schema Validator
Verifies compilation build matrices and environment settings using Pydantic v2.
"""

import json
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator

class EnvironmentSecret(BaseModel):
    env_key: str = Field(..., description="Environment variable key name")
    required: bool = Field(True, description="Whether execution fails if key is missing")

class TargetBuildSpec(BaseModel):
    name: str = Field(..., min_length=2, max_length=64, description="Binary output name")
    transport: str = Field("stdio", pattern="^(stdio|sse|websocket)$")
    mcp_command: Optional[str] = Field(None, description="Command required if transport is stdio")
    sse_endpoint: Optional[HttpUrl] = Field(None, description="URL required if transport is sse")
    secrets: List[EnvironmentSecret] = Field(default_factory=list, description="Required runtime environment variables")
    supported_output_formats: List[str] = Field(default_factory=lambda: ["json", "yaml", "table"])

    @field_validator("mcp_command")
    @classmethod
    def validate_command_for_stdio(cls, v: Optional[str], info) -> Optional[str]:
        if info.data.get("transport") == "stdio" and not v:
            raise ValueError("mcp_command cannot be empty when transport is stdio")
        return v

class BuildMatrixConfig(BaseModel):
    build_id: str = Field(..., description="Unique build tracking identifier")
    targets: List[TargetBuildSpec] = Field(..., min_items=1, description="List of target binaries to compile")

def validate_build_matrix(raw_json: str) -> Optional[BuildMatrixConfig]:
    try:
        data = json.loads(raw_json)
        matrix = BuildMatrixConfig.model_validate(data)
        print(f"Build Matrix {matrix.build_id} successfully validated {len(matrix.targets)} targets.")
        return matrix
    except ValidationError as e:
        print("Build Matrix Schema Validation Error:")
        print(e.json(indent=2))
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON payload.")
        return None

if __name__ == "__main__":
    sample_payload = json.dumps({
        "build_id": "build-20270107-v1",
        "targets": [
            {
                "name": "jira-automation-cli",
                "transport": "stdio",
                "mcp_command": "npx -y @anthropic-ai/mcp-server-atlassian",
                "secrets": [
                    {"env_key": "JIRA_API_TOKEN", "required": True},
                    {"env_key": "JIRA_BASE_URL", "required": True}
                ],
                "supported_output_formats": ["json", "table"]
            }
        ]
    })

    validate_build_matrix(sample_payload)
```

## Comparison table

| Feature | CliHub Static Binary | Direct MCP Transport Client | Standard REST CLI |
| :--- | :--- | :--- | :--- |
| **Startup Overhead** | Zero (< 10ms Native Execution) | High (SDK & Session Handshake) | Zero (< 10ms Native Execution) |
| **Protocol Foundation** | FastMCP 3.1 Protocol | FastMCP 3.1 Protocol | Custom HTTP REST / GraphQL APIs |
| **Dependency Requirement**| None (Self-Contained Executable)| Requires Node / Python / MCP Client | Requires curl / custom CLI binary |
| **Schema Coupling** | Compiled at Build Timestamp | Dynamic Runtime Introspection | Static OpenAPI / Swagger Spec |
| **Agent Execution Speed** | Ultra-Fast (< 10ms) | Moderate (200-500ms session handshake) | Ultra-Fast (< 10ms) |
| **Token Cost Efficiency** | High (Shell help text) | Low (Full JSON schema in context) | High (Shell help text) |

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) — The core protocol specification supporting FastMCP 3.1.
- [MCP Registry](mcp-registry.md) — Directory for discovering target FastMCP servers.
- [ServiceNow MCP Server](servicenow-mcp.md) — Primary candidate for CliHub compilation.
- [Atlassian Jira MCP Implementations](atlassian-jira-mcp.md) — Enterprise tool candidate for CLI conversion.
- [Claude Code](../development_ops/claude-code.md) — Shell agent that leverages generated binaries.
- [n8n](../../services/n8n.md) — Automation platform that invokes compiled CLI tools in workflow nodes.

## Sources / references
- [CliHub Repository](https://github.com/thellimist/clihub)
- [I Made MCP 94% Cheaper (And It Only Took One Command)](https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/specification/2026-03-31)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
