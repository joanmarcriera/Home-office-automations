# Model Context Protocol Servers

## What it is
Model Context Protocol (MCP) Servers are standardized, lightweight microservices implementing the open Model Context Protocol (FastMCP 3.1). They expose tools, resource capabilities, and prompts to AI agents (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4) over stdio or SSE transports.

## What problem it solves
Before MCP, every AI agent framework (LangChain, AutoGen, LlamaIndex) required custom, proprietary integrations to connect LLMs to external systems like GitHub, Home Assistant, SQLite, or Paperless-ngx. MCP servers provide a universal, framework-agnostic protocol standard that allows any compliant AI client to discover and invoke tools seamlessly.

## Where it fits in the stack
**Automation / Orchestration**. MCP servers act as the execution layer that connects reasoning AI models with homelab infrastructure, local databases, and enterprise APIs.

## Typical use cases
- **Homelab System Control**: Controlling Home Assistant lights and scenes via `homeassistant-mcp`.
- **Document Management**: Querying and staging documents in Paperless-ngx or Vikunja task lists.
- **Developer Workflows**: Interacting with local Git repositories, Docker containers, and database schemas.

## Strengths
- **Protocol Standardization**: Built on FastMCP 3.1 with standardized tool, resource, and prompt JSON-RPC messaging.
- **Universal Compatibility**: Works natively across Claude Code, Open WebUI, Cursor, and custom agent loops.
- **Security & Sandboxing**: Server instances can run in isolated Docker or Podman containers with strict environment variable controls.

## Limitations
- **State Management**: MCP servers are stateless by default and rely on clients or external state stores for long-running workflows.
- **Transport Latency**: Remote SSE transport adds network latency compared to local stdio communication.

## When to use it
- When connecting AI agents (Claude Code, Cursor, Open WebUI) to homelab APIs and local databases.
- When creating reusable, framework-independent tool integrations for LLMs.
- When standardizing agent tool calling using FastMCP 3.1 protocols.

## When not to use it
- When implementing simple, inline function calls without external agent access needs.
- When communicating over restricted legacy protocols that prohibit JSON-RPC over stdio/SSE.

## Getting started
To register and run a self-hosted stdio MCP server:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/data/homelab.db"]
    }
  }
}
```

## CLI examples

```bash
# Launch an MCP server via uvx
uvx mcp-server-sqlite --db-path /data/homelab.db

# Inspect running FastMCP server tools
mcp dev server.py
```

## API examples

### 1. Pydantic v2 Schema for MCP Server Tool Registration
```python
from typing import Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field

class MCPToolDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Unique tool identifier")
    description: str = Field(..., description="Human-readable tool prompt description")
    parameters_schema: Dict[str, Any] = Field(..., description="JSON Schema for tool arguments")

class MCPServerCatalog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    server_id: str
    protocol_version: str = "3.1"
    tools: List[MCPToolDefinition]

def validate_mcp_catalog(data: Dict[str, Any]) -> MCPServerCatalog:
    return MCPServerCatalog.model_validate(data)

if __name__ == "__main__":
    payload = {
        "server_id": "paperless-mcp",
        "protocol_version": "3.1",
        "tools": [
            {
                "name": "search_documents",
                "description": "Searches Paperless documents by query",
                "parameters_schema": {"type": "object", "properties": {"query": {"type": "string"}}}
            }
        ]
    }
    catalog = validate_mcp_catalog(payload)
    print(f"Validated MCP Server '{catalog.server_id}' with {len(catalog.tools)} tool(s)")
```

### 2. FastMCP 3.1 Server Definition
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("homelab-task-server")

@mcp.tool()
def get_system_status() -> dict:
    """Returns homelab cluster operational health metrics."""
    return {"status": "healthy", "cluster": "k3s-primary"}

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [MCP Registry](mcp-registry.md) — Central directory for MCP servers.
- [Model Context Protocol (MCP)](mcp.md) — Specification and architecture.
- [FastMCP 3.1](mcp.md) — SDK for building MCP servers.

## Sources / references
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP GitHub Repository](https://github.com/jlowin/fastmcp)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
