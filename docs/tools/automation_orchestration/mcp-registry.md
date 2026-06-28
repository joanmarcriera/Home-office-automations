# MCP Registry

## What it is
The MCP Registry is the central discovery platform and directory for Model Context Protocol (MCP) servers. Managed by the **Agentic AI Foundation** (under the Linux Foundation) since December 2025, it provides a standardized way for developers to publish and for users to discover tools that extend the capabilities of AI agents like Claude 4.8, GPT-5.5, and Llama 4 Maverick.

## What problem it solves
Before the registry, MCP implementations were fragmented across GitHub, NPM, and private blogs. The registry addresses this fragmentation by providing a single, authoritative source for discovering publicly available MCP servers. It standardizes server metadata (via `server.json` and FastMCP 3.0), making it easier to find, evaluate, and install tools.

## Where it fits in the stack
**Automation / Orchestration**. It acts as the "app store" or "package manager" equivalent for the AI tool-calling ecosystem. It provides the metadata infrastructure that allows agents to find the right tool for a specific task.

## Typical use cases
- **Discovering Integrations**: Finding an MCP server that connects Claude to a specific database (e.g., PostgreSQL), service (e.g., Slack), or local tool (e.g., terminal).
- **Evaluating Maturity**: Checking the popularity, maintenance status, and exposed toolsets of different MCP implementations before integrating them.
- **Publishing Tools**: Providing a standardized way for developers to share their custom MCP servers with the wider community.
- **Protocol Compliance**: Verifying that a server follows the official MCP standards (FastMCP 3.0) for metadata and communication.

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
Clients like Claude 4.8 can programmatically interact with the registry to discover tools on-the-fly using the FastMCP 3.0 SDK.

```python
from mcp.client import FastMCP

# Initialize a client that can discover tools from the registry
client = FastMCP("my-agent")

# Discover tools for a specific domain
tools = client.discover_tools("database")
for tool in tools:
    print(f"Found tool: {tool.name}")
```

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) — The underlying protocol.
- [FastMCP 3.0](mcp.md) — The June 2026 standard for building MCP servers.
- [CliHub](clihub.md) — A community repository for CLI tools.
- [ServiceNow MCP Server](servicenow-mcp.md) — Enterprise integration example.
- [Atlassian Jira MCP Implementations](atlassian-jira-mcp.md) — Project management integration.
- [Playwright MCP Server](playwright-mcp.md) — Browser automation tool.
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md) — Sandbox environment.
- [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md) — OS-level automation.
- [Claude 4.8 (Opus)](../providers/anthropic.md) — Primary consumer of MCP tools.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) - Open source model support.

## Sources / references
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)
- [Model Context Protocol Website](https://modelcontextprotocol.io/)
- [Agentic AI Foundation Announcements](https://agentic-ai.foundation/)
- [FastMCP 3.0 Documentation](https://github.com/modelcontextprotocol/fastmcp)

## Contribution Metadata

- Last reviewed: 2026-06-28
- Confidence: high
