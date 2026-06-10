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
- **Agent Orchestration**: Coordinating multiple specialized agents (e.g., using Claude 4.7 for reasoning and Llama 4 Maverick for task execution) via a shared protocol.

## Strengths
- **Ecosystem Neutrality**: Designed to be used by any model provider or agent developer.
- **Security**: Focuses on secure, locally-controlled execution of tools.
- **Extensibility**: Growing library of community-contributed MCP servers (Google Maps, GitHub, Postgres, etc.).
- **Performance**: Standardized transport layers (Stdio, HTTP/SSE) ensure low-latency communication.

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

## CLI examples
MCP servers and clients can be managed and tested via CLI tools.

```bash
# Test an MCP server using the MCP Inspector
npx @modelcontextprotocol/inspector <command-to-run-server>

# List available tools on a local server (via Stdio)
echo '{"jsonrpc":"2.0","method":"tools/list","id":1,"params":{}}' | node my-mcp-server.js

# Use the MCP CLI to connect to a server
mcp-cli connect stdio --command node --args my-mcp-server.js
```

## API examples
Clients can interact with MCP servers via the defined protocol over various transports.

### Client Request (JSON-RPC)
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "location": "San Francisco"
    }
  },
  "id": 1
}
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — Uses MCP for tool interaction.
- [Roo Code](../agents/roo-code.md) — Open-source agent supporting MCP.
- [MCP Registry](mcp-registry.md) — Central catalog of MCP servers.
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) — Specific implementation pattern.
- [Cline](../agents/cline.md) — IDE agent with MCP support.
- [GPT-5.5](../providers/openai.md) — Integrated with MCP via third-party gateways.
- [n8n](../../services/n8n.md) — Supports MCP for workflow tool execution.
- [OpenWebUI](../../services/open-webui.md) — Integrated with MCP for tool discovery.
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk) — Official Python implementation.

## Sources / References
- [Official Website](https://modelcontextprotocol.io/)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [MCP Documentation](https://modelcontextprotocol.io/docs/concepts/architecture)
- [MCP SDKs](https://github.com/modelcontextprotocol)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
