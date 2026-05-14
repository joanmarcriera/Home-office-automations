# MCP Registry

## What it is
The MCP Registry is the central discovery platform and directory for Model Context Protocol (MCP) servers. It provides a standardized way for developers to publish and for users to discover tools that extend the capabilities of AI agents (like Claude Desktop, IDEs, or autonomous scripts).

## What problem it solves
Before the registry, MCP implementations were fragmented across GitHub, NPM, and private blogs. The registry addresses this fragmentation by providing a single, authoritative source for discovering publicly available MCP servers. It standardizes server metadata (via `server.json`), making it easier to find, evaluate, and install tools.

## Where it fits in the stack
**Automation / Orchestration**. It acts as the "app store" or "package manager" equivalent for the AI tool-calling ecosystem. It provides the metadata infrastructure that allows agents to find the right tool for a specific task.

## Typical use cases
- **Discovering Integrations**: Finding an MCP server that connects Claude to a specific database (e.g., PostgreSQL), service (e.g., Slack), or local tool (e.g., terminal).
- **Evaluating Maturity**: Checking the popularity, maintenance status, and exposed toolsets of different MCP implementations before integrating them.
- **Publishing Tools**: Providing a standardized way for developers to share their custom MCP servers with the wider community.
- **Protocol Compliance**: Verifying that a server follows the official MCP standards for metadata and communication.

## Strengths
- **Official Status**: Backed by Anthropic and the core MCP development team as the canonical directory.
- **Standardized Metadata**: Enforces the use of `server.json` for consistent tool representation across the ecosystem.
- **Unified Discovery**: Creators publish once, and all consumers (IDEs, desktop apps, CLI tools) can reference the same canonical data.
- **Searchable Index**: Provides a categorized and searchable interface for finding specific functionalities.

## Limitations
- **Discovery Only**: Does not host the actual server code or binaries; it provides links to where they are hosted (GitHub, NPM, Docker Hub).
- **Early Stage**: The ecosystem is growing rapidly, so quality and documentation of listed servers can vary significantly.
- **Permissions**: The registry does not handle authentication or credential management for the servers it lists.

## When to use it
- When you want to see what integrations are available to extend your AI agent's capabilities.
- When you are developing a new MCP server and want it to be discoverable by other users.
- When you need to find the correct installation command for an official or community-maintained MCP server.

## When not to use it
- When you are working with private, internal, or proprietary tools that should not be publicly indexed.
- When using non-MCP-based tool-calling systems (e.g., legacy OpenAI Function Calling).

## Getting started

### Browsing the Registry
You can browse the registry through the web interface at [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/).

### Using Registry Metadata in Config
Many MCP clients use the registry metadata to simplify configuration. For example, if a tool is listed on the registry, you can often find the exact `claude_desktop_config.json` snippet required to run it.

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

## Technical examples

### Publishing to the Registry
To list a server, developers typically create a `mcp-server.json` file in their repository root and submit a PR to the official registry repository.

```json
{
  "mcp-server": {
    "name": "my-custom-server",
    "description": "Exposes my custom home automation tools",
    "version": "1.0.0",
    "repository": "https://github.com/user/my-custom-server",
    "license": "MIT"
  }
}
```

### Programmatic Discovery
Advanced clients can fetch the registry index as JSON to provide an "in-app" discovery experience.

```bash
# Example of fetching registry metadata (hypothetical endpoint)
curl https://registry.modelcontextprotocol.io/v1/servers/search?q=postgres
```

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md)
- [CliHub](clihub.md)
- [ServiceNow MCP Server](servicenow-mcp.md)
- [Atlassian Jira MCP Implementations](atlassian-jira-mcp.md)
- [Playwright MCP Server](playwright-mcp.md)
- [Claude Desktop](../development_ops/vscode.md)
- [PulseMCP](https://pulsemcp.com/) (Community-driven alternative directory)

## Sources / references
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)
- [Model Context Protocol Website](https://modelcontextprotocol.io/)
- [MCP GitHub Organization](https://github.com/modelcontextprotocol)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
