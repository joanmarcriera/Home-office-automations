# MCP Registry

## What it is
The MCP Registry is the central discovery platform and directory for Model Context Protocol (MCP) servers. Managed by the **Agentic AI Foundation** (under the Linux Foundation) since December 2025, it provides a standardized way for developers to publish and for users to discover tools that extend the capabilities of AI agents like Claude 5.1, GPT-5.5, Gemini 4.0, and Llama 4 Maverick.

## What problem it solves
Before the registry, MCP implementations were fragmented across GitHub, NPM, and private blogs. The registry addresses this fragmentation by providing a single, authoritative source for discovering publicly available MCP servers. It standardizes server metadata (via `server.json` and FastMCP 3.1), making it easier to find, evaluate, and install tools.

## Where it fits in the stack
**Automation / Orchestration**. It acts as the "app store" or "package manager" equivalent for the AI tool-calling ecosystem. It provides the metadata infrastructure that allows agents to find the right tool for a specific task.

## Typical use cases
- **Discovering Integrations**: Finding an MCP server that connects Claude to a specific database (e.g., PostgreSQL), service (e.g., Slack), or local tool (e.g., terminal).
- **Evaluating Maturity**: Checking the popularity, maintenance status, and exposed toolsets of different MCP implementations before integrating them.
- **Publishing Tools**: Providing a standardized way for developers to share their custom MCP servers with the wider community.
- **Protocol Compliance**: Verifying that a server follows the official MCP standards (FastMCP 3.1) for metadata and communication.

## Strengths
- **Official Status**: Backed by the Agentic AI Foundation as the canonical directory.
- **Standardized Metadata**: Enforces the use of `server.json` for consistent tool representation across the ecosystem.
- **Unified Discovery**: Creators publish once, and all consumers (IDEs, desktop apps, CLI tools) can reference the same canonical data.
- **Searchable Index**: Provides a categorized and searchable interface for finding specific functionalities.

## Limitations
- **Discovery Only**: Does not host the actual server code or binaries; it provides links to where they are hosted (GitHub, NPM, Docker Hub).
- **Quality Variance**: While the registry is curated, the quality and security of community-contributed servers vary.
- **Permissions**: The registry does not handle authentication or credential management for the servers it lists.

## When to use it
- When you want to see what integrations are available to extend your AI agent's capabilities.
- When you are developing a new MCP server and want it to be discoverable by other users.
- When you need to find the correct installation command for an official or community-maintained MCP server.

## When not to use it
- When you are working with private, internal, or proprietary tools that should not be publicly indexed.
- When using non-MCP-based tool-calling systems.

## Getting started
To discover and use tools from the registry, you typically find the server you need and add its configuration to your MCP client (like Claude Desktop or an MCP-native IDE).

1. Browse the registry at [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/).
2. Locate a server (e.g., `@modelcontextprotocol/server-everything`).
3. Copy the configuration snippet into your client config.

```json
{
  "mcpServers": {
    "everything": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"]
    }
  }
}
```

## CLI examples
The MCP Registry can be interacted with via the MCP CLI or through `npx` for individual servers.

```bash
# Search for a server in the registry
mcp search postgres

# List all official MCP servers
mcp list --official

# Install a server from the registry
mcp install @modelcontextprotocol/server-postgres
```

## API examples

### 1. Dynamic Discovery via FastMCP 3.1 (Python)
Clients like Claude 5.1, GPT-5.5, and Gemini 4.0 Pro can programmatically interact with the registry to discover tools on-the-fly using the FastMCP 3.1 SDK:

```python
from mcp.client import FastMCP

# Initialize a client that can discover tools from the registry
client = FastMCP("my-agent")

# Discover tools for a specific domain
tools = client.discover_tools("database")
for tool in tools:
    print(f"Found tool: {tool.name}")
```

### 2. Programmatic Registry Verification with Pydantic v2 Validation
Verifying registry server catalog configurations (via `server.json` schema) using Pydantic v2 (Python) according to early 2027 SOTA standards:

```python
import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl

# Pydantic v2 models representing the schema of registry server metadata
class MCPServerConfig(BaseModel):
    command: str = Field(..., description="Startup executable or runtime command (e.g., npx, python)")
    args: List[str] = Field(default_factory=list, description="Array of arguments passed to the server execution")
    env: Dict[str, str] = Field(default_factory=dict, description="Environment variables needed for authorization")

class RegistryServerMeta(BaseModel):
    name: str = Field(..., description="Name of the MCP server as registered")
    github_url: Optional[HttpUrl] = Field(None, alias="githubUrl")
    npm_package: Optional[str] = Field(None, alias="npmPackage")
    default_config: MCPServerConfig = Field(..., alias="defaultConfig")

def fetch_and_validate_registry_meta(server_id: str) -> RegistryServerMeta:
    # Simulating standard registry API response payload for validation
    mock_payload = {
        "name": "postgresql-mcp-server",
        "githubUrl": "https://github.com/modelcontextprotocol/server-postgres",
        "npmPackage": None,
        "defaultConfig": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": {
                "DATABASE_URL": "postgresql://localhost:5432/homelab"
            }
        }
    }

    # Strictly validate against the early 2027 Registry contract schemas
    validated = RegistryServerMeta.model_validate(mock_payload)
    return validated

if __name__ == "__main__":
    meta = fetch_and_validate_registry_meta("postgres")
    print(f"Validated MCP Registry Server: {meta.name}")
    print(f"Run command: {meta.default_config.command} {' '.join(meta.default_config.args)}")
```

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) — The underlying protocol.
- [FastMCP 3.1](mcp.md) — The SOTA standard for building MCP servers.
- [CliHub](clihub.md) — A community repository for CLI tools.
- [ServiceNow MCP Server](servicenow-mcp.md) — Enterprise integration example.
- [Atlassian Jira MCP Implementations](atlassian-jira-mcp.md) — Project management integration.
- [Playwright MCP Server](playwright-mcp.md) — Browser automation tool.
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md) — Sandbox environment.
- [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md) — OS-level automation.
- [Claude 5.1 (Opus)](../providers/anthropic.md) — Primary consumer of MCP tools.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) - Open source model support.

## Sources / references
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)
- [Model Context Protocol Website](https://modelcontextprotocol.io/)
- [Spline V2 MCP Agents - The New Stack](https://thenewstack.io/spline-v2-mcp-agents/)
- [Agentic AI Foundation Announcements](https://agentic-ai.foundation/)
- [FastMCP 3.1 Documentation](https://github.com/modelcontextprotocol/fastmcp)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
