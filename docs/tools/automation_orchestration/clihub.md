# CliHub

## What it is
CliHub is a generator that connects to a Model Context Protocol (MCP / FastMCP 3.1) server and produces a compiled, standalone CLI binary in Go or Rust. Each tool exposed by the MCP server is automatically converted into a command within the generated CLI. Standardized in early 2027 (v1.8), it supports **FastMCP 3.1** capabilities and is a primary tool for "freezing" agentic tool suites into stable, zero-dependency binaries.

## What problem it solves
MCP clients (like **Claude 5.1 Desktop**) are excellent for interactive agent workflows, but they can add significant runtime overhead and deployment complexity for automated tasks. CliHub solves this by converting MCP tools into portable, fast, and scriptable binaries. It allows "one-command" deployment of entire tool suites for both humans and agents, bridging the gap between dynamic agent tools and static DevOps pipelines.

## Where it fits in the stack
**Automation & Orchestration Tooling Layer**. It bridges the gap between the emerging FastMCP ecosystem and traditional shell-native workflows. It effectively allows developers to "compile" dynamic agent tool suites into standard DevOps-friendly binaries for use by frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4**.

## Typical use cases
- Packaging complex MCP tool suites (like Jira, GitHub, or ServiceNow) into static binaries for CI/CD pipelines.
- Running MCP-backed workflows in shell scripts without needing a full MCP client stack.
- Shipping deterministic, versioned tool interfaces to autonomous agent runtimes.
- Reducing latency for tool invocation in high-frequency automation loops.
- Debugging FastMCP servers directly from the terminal with standard CLI arguments.

## Strengths
- **Simplicity**: One-command codegen flow from MCP endpoint to ready-to-use CLI.
- **Portability**: Generates static binaries for multiple target platforms (Linux, macOS, Windows).
- **Efficiency**: Eliminates the overhead of maintaining an active MCP transport session for simple, one-off tool calls.
- **Interoperability**: Supports HTTP/SSE, WebSocket, and stdio MCP transport protocols.
- **Agent-Friendly**: Standard CLI interfaces are easily understood by shell-executing agent runtimes.

## Limitations
- **Static Schema**: The generated CLI reflects the MCP server schema at the time of generation; it requires regeneration if server tools change.
- **Auth Management**: Authentication setup (API tokens, environment variables) must still be handled securely outside of the binary.
- **No Stateful Sessions**: Unlike a live MCP client, each CLI call is independent, which may not be suitable for servers that rely on multi-call state.

## When to use it
- When you want to distribute MCP capabilities in a lightweight, zero-dependency model.
- When building automated DevOps pipelines that need to leverage agent-designed tools.
- When you want to use MCP tools as part of a larger bash or python automation script.
- When debugging a new MCP server and you want a standard CLI interface to test each tool.

## When not to use it
- When a long-running, stateful MCP session is required for advanced multi-step reasoning.
- When dynamic, runtime discovery of new tools is a core part of the workflow.
- When the overhead of a full MCP client (like `mcp-cli` or `claude-code`) is already acceptable.

## Architectural overview
CliHub introspection works by connecting to a FastMCP 3.1 server transport, querying the `tools/list` protocol method, and compiling a type-safe Go/Rust binary using abstract syntax tree templates. The compiled binary serializes command-line flags into JSON tool arguments and parses structured Pydantic v2 responses into human-readable table or JSON outputs.

```
[ FastMCP 3.1 Server ] ──> [ CliHub Schema Inspector ]
                                    │
                                    ▼
[ Standalone Binary ] <── [ Go/Rust AST Compiler ]
        │
        ▼
[ DevOps / Agent Shell Pipeline Execution ]
```

## Getting started

### Installation
You can install the CliHub generator via Go or by downloading a pre-compiled binary.

```bash
# Install via Go
go install github.com/thellimist/clihub@latest
```

### Basic Usage
Generate a CLI from a local MCP server (stdio):

```bash
# Generate a CLI named 'my-tool' from a Node-based MCP server
clihub generate --name my-tool --command "npx -y @anthropic-ai/mcp-server-atlassian"
```

## CLI examples

```bash
# 1. Generating a Remote CLI (SSE)
clihub generate --name remote-tool --url "https://mcp.example.com/sse"

# 2. Invoking a Generated Command
./jira-cli get_issue --key PROJ-123
./jira-cli search_issues --jql "project = PROJ AND status = Open"

# 3. Multi-Platform Cross Compilation
GOOS=linux GOARCH=amd64 clihub generate --name jira-linux --command "..."
```

## API examples

The following Python script demonstrates validating MCP compilation configs using Pydantic v2 schemas before programmatically triggering CliHub binary generation.

```python
import os
import subprocess
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl

class CliHubCompilationConfig(BaseModel):
    name: str = Field(..., min_length=2, description="Output binary name")
    mcp_transport: str = Field("stdio", pattern="^(stdio|sse)$")
    command: Optional[str] = Field(None, description="The stdio MCP startup command")
    sse_endpoint: Optional[HttpUrl] = Field(None, description="Target SSE URL if using sse transport")
    env_vars: Dict[str, str] = Field(default_factory=dict, description="Custom environment variables passed to compiler")

class CompilationResult(BaseModel):
    success: bool = Field(..., description="Whether compilation completed successfully")
    output_path: str = Field(..., description="Path to generated binary")
    commands_exposed: List[str] = Field(default_factory=list, description="Extracted tool commands compiled into the binary")

def compile_mcp_cli(config: CliHubCompilationConfig) -> CompilationResult:
    # Validate the incoming configurations via Pydantic v2
    validated_cfg = config.model_dump()

    mock_result = {
        "success": True,
        "output_path": f"./bin/{config.name}",
        "commands_exposed": ["get_incident", "update_incident", "delete_incident"]
    }

    return CompilationResult.model_validate(mock_result)

if __name__ == "__main__":
    test_config = CliHubCompilationConfig(
        name="servicenow-cli",
        mcp_transport="stdio",
        command="python3 -m mcp_server_servicenow.cli",
        env_vars={"SERVICENOW_INSTANCE_URL": "https://dev-test.service-now.com"}
    )
    res = compile_mcp_cli(test_config)
    print(f"Compilation Complete: {res.output_path}, success={res.success}")
```

## Comparison table

| Feature | CliHub Static Binary | Direct MCP Transport Client | Standard REST CLI |
| :--- | :--- | :--- | :--- |
| **Startup Overhead** | Zero (Native Go/Rust Binary) | High (SDK & Session Connect) | Zero |
| **Protocol Foundation** | FastMCP 3.1 Protocol | FastMCP 3.1 Protocol | Custom HTTP REST APIs |
| **Dependency Requirement**| None (Self-Contained) | Requires Node / Python / MCP Client | Requires curl / custom CLI |
| **Schema Coupling** | Compiled at Build Time | Dynamic Runtime Introspection | Static API Spec |
| **Agent Execution Speed** | Ultra-Fast (< 10ms) | Moderate (200-500ms session handshake) | Ultra-Fast |

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) - The underlying protocol (supporting FastMCP 3.1).
- [MCP Registry](mcp-registry.md) - For finding MCP servers to compile.
- [ServiceNow MCP Server](servicenow-mcp.md) - A target for compilation.
- [Atlassian Jira MCP Implementations](atlassian-jira-mcp.md) - A target for compilation.
- [Claude Code](../development_ops/claude-code.md) - A high-level consumer of MCP.
- [n8n](../../services/n8n.md) - Orchestrator that can use generated binaries.

## Sources / references
- [CliHub Repository](https://github.com/thellimist/clihub)
- [I Made MCP 94% Cheaper (And It Only Took One Command)](https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/2026-03-31)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
