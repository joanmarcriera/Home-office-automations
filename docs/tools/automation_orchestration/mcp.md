# Model Context Protocol (MCP)

## What it is
The Model Context Protocol (MCP) is an open standard that enables developers to build secure, two-way connections between their data sources and AI models. It was introduced by Anthropic to standardize how models interact with external tools and information.

## What problem it solves
It eliminates the need to write custom integration code for every tool/LLM combination. By providing a universal interface, an MCP-compliant server can work with any MCP-compliant client (like Claude Desktop or Roo Code).

## Where it fits in the stack
**Protocol / Automation & Orchestration / Pattern**.

## Typical use cases
- **Universal Tool Access**: Giving an LLM access to a local filesystem, database, or API through a standard server.
- **Dynamic Context Injection**: Allowing models to pull in relevant documentation or code snippets as needed.
- **Cross-Platform Agents**: Writing a tool once and using it in multiple agent frameworks.

## Strengths
- **Ecosystem Neutrality**: Designed to be used by any model provider or agent developer.
- **Security**: Focuses on secure, locally-controlled execution of tools.
- **Extensibility**: Growing library of community-contributed MCP servers (Google Maps, GitHub, Postgres, etc.).

## Limitations
- **Adoption**: While growing rapidly, it is still a relatively new standard.
- **Client Support**: Requires specific support in the LLM client or agent framework.

## When to use it
- To provide LLMs with access to local or private data sources in a standardized way.
- When building tools that you want to be reusable across different AI environments.

## When not to use it
- For very simple, one-off tool implementations where a basic API call is sufficient.

## Getting started

### MCP Architecture
MCP uses a client-server architecture. A **Client** (like Claude Desktop) connects to a **Server** (a small program that exposes tools) over a transport layer like Stdio or HTTP/SSE.

### Example: Using a Local MCP Server (Claude Desktop)
To add a local MCP server to Claude Desktop, edit your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    }
  }
}
```

### Developing a Simple MCP Server (Node.js)
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({
  name: "example-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "get_weather",
    description: "Get the weather for a location",
    inputSchema: {
      type: "object",
      properties: { location: { type: "string" } }
    }
  }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md)
- [Roo Code](../agents/roo-code.md)
- [MCP Registry](mcp-registry.md)
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Cline](../agents/cline.md)

## Sources / References
- [Official Website](https://modelcontextprotocol.io/)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [MCP Documentation](https://modelcontextprotocol.io/docs/concepts/architecture)
- [MCP SDKs](https://github.com/modelcontextprotocol)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
