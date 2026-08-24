# Data Copilot: MCP Tool & Data Standardization

This document details the standardization of tool definitions and data access interfaces for the Data Copilot using the Model Context Protocol (FastMCP 3.1). By standardizing on FastMCP 3.1, specialized agents across Text-to-SQL, diagnostic RAG, and multi-agent workflows interact with heterogeneous data sources through machine-parseable, schema-verified primitives.

## What it is
The Model Context Protocol (FastMCP 3.1) operates as the universal integration layer for the Data Copilot. It decouples Direct Database Connectors, Document Search APIs, and KPI Metadata Registries into modular resources, prompts, and tools. FastMCP 3.1 enables LLMs (such as Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.8) to securely execute queries and tools with sub-millisecond overhead and Pydantic v2 schema enforcement.

## What problem it solves
Data Copilot environments require agents to interface with diverse data backends (PostgreSQL, SQLite, ClickHouse, Qdrant, REST APIs). Direct custom connectors result in fragile N×M integration matrices ("connector sprawl"). FastMCP 3.1 standardization solves this by providing a single protocol specification for tool registration, schema validation, and lifecycle transport, insulating agentic reasoning from underlying implementation mechanics.

## Where it fits in the stack
FastMCP 3.1 functions at the **Tool Execution, Protocol & Data Interface Layer**, bridging reasoning agents in the [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) with storage backends and operational tools.

## Typical use cases
- **Database Query Execution**: Exposing managed database interfaces via `fastmcp-sqlite` or `fastmcp-postgres`.
- **Glossary & Schema Discovery**: Serving corporate metric definitions and table schemas as read-only MCP resources (`mcp://schema/main`).
- **Hybrid RAG Tooling**: Providing semantic search and vector lookup capabilities to diagnostic agents ([Data Copilot Agentic RAG](data-copilot-agentic-rag.md)).
- **Asynchronous Task Lifecycle**: Managing multi-turn SQL generation tasks via MCP task protocol handlers.
- **Strict Host Config Validation**: Enforcing security safelists on host configurations via Pydantic v2 models.

## Strengths
- **Protocol Standardization**: Eliminates custom API wrappers through universal tool and resource primitives.
- **FastMCP 3.1 High Throughput**: Native Python and TypeScript FastMCP SDKs enable sub-millisecond RPC execution.
- **Security & Sandboxing**: Fine-grained parameter validation and command whitelisting limit execution privileges.
- **Schema Safety**: Enforces Pydantic v2 data models for request and response payloads.

## Limitations
- **Protocol Overhead**: IPC or transport abstractions introduce minor overhead compared to in-memory native function calls.
- **Ecosystem Migration**: Updating legacy MCP servers to FastMCP 3.1 specification requires server-side dependency updates.

## When to use it
- When building multi-agent systems that require verified tool schemas across disparate database systems.
- When isolating LLM agents from raw credentials or direct database connection handles.
- When standardizing enterprise data copilot tools on FastMCP 3.1.

## When not to use it
- For monolithic single-script applications with a single static database connection.
- When an existing native API already exposes a fully compliant agentic interface.

## Getting started

### 1. Install FastMCP 3.1 CLI & SDK
```bash
# Install FastMCP Python SDK with 3.1 features
pip install "fastmcp>=3.1.0"
```

### 2. Configure Host Integration
Define the server configuration in your host configuration file:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "python3",
      "args": ["-m", "fastmcp.servers.sqlite", "--db", "/data/inventory.db"]
    }
  }
}
```

### 3. Initialize FastMCP Client Connection
```python
from fastmcp import FastMCP

# Initialize FastMCP 3.1 server instance
mcp = FastMCP("DataCopilotServer", version="3.1")

@mcp.tool()
def execute_sql(query: str) -> str:
    """Execute validated read-only SQL query against inventory DB."""
    # Database execution logic
    return f"Query executed: {query}"

if __name__ == "__main__":
    mcp.run()
```

## CLI examples

### Inspecting Registered Tools via FastMCP CLI
```bash
# List available tools on a FastMCP server
fastmcp tools list --server sqlite

# Read a registered MCP resource
fastmcp resource read mcp://sqlite/schema/main
```

### Direct Tool Execution
```bash
# Call SQL tool via FastMCP 3.1 CLI
fastmcp tool call sqlite execute_sql --data '{"query": "SELECT COUNT(*) FROM inventory"}'
```

## API examples

### Programmatic Host Config Validation (Python & Pydantic v2)
Validating MCP host configuration parameters under **FastMCP 3.1** standards using Pydantic v2 schemas:

```python
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class McpServerConfig(BaseModel):
    """Configuration for an individual MCP Server process."""
    command: str = Field(..., description="Executable command to spawn server process.")
    args: List[str] = Field(default_factory=list, description="Command line arguments.")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables map.")

    @field_validator("command")
    @classmethod
    def enforce_safe_executables(cls, value: str) -> str:
        """Enforce strict executable safelist to prevent arbitrary code execution."""
        safe_commands = {"npx", "node", "python", "python3", "bun", "uv", "fastmcp"}
        clean_cmd = value.strip().lower()
        if clean_cmd not in safe_commands:
            raise ValueError(f"Command '{value}' is not in safe executable list: {safe_commands}")
        return clean_cmd

class DataCopilotMcpHostConfig(BaseModel):
    """Root configuration schema for Data Copilot FastMCP host."""
    mcp_version: str = Field(default="3.1", description="FastMCP protocol version.")
    mcp_servers: Dict[str, McpServerConfig] = Field(..., alias="mcpServers", description="Map of registered MCP servers.")

# Example Verification Usage
if __name__ == "__main__":
    payload = {
        "mcp_version": "3.1",
        "mcpServers": {
            "sqlite": {
                "command": "fastmcp",
                "args": ["run", "sqlite_server.py", "--db", "inventory.db"],
                "env": {"DEBUG": "0"}
            },
            "vector_search": {
                "command": "python3",
                "args": ["-m", "vector_mcp_server", "--index", "docs_index"]
            }
        }
    }

    try:
        validated_host = DataCopilotMcpHostConfig.model_validate(payload)
        print(f"Validated FastMCP Host Config (Version: {validated_host.mcp_version})")
        for s_name, s_cfg in validated_host.mcp_servers.items():
            print(f" - Server '{s_name}': command='{s_cfg.command}', args={s_cfg.args}")
    except ValidationError as err:
        print(f"Config Validation Error: {err.json(indent=2)}")
```

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) — Base architecture.
- [Data Copilot Agentic RAG](data-copilot-agentic-rag.md) — RAG integration with FastMCP.
- [FastMCP 3.1 Tool Calling Standard](tool-calling-and-mcp.md) — Specification details.
- [Agent Protocols](../agent_protocols.md) — Broader protocol landscape.

## Sources / references
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Python Repository](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
