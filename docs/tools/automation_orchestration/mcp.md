# Model Context Protocol (MCP)

## What it is
The Model Context Protocol (MCP) is an open standard that enables developers to build secure, two-way connections between their data sources and AI models. It was introduced by Anthropic to standardize how models interact with external tools and information. As of July 2026, **MCP 3.0** is the industry standard for agentic tool discovery, natively supported by **Claude 5.1** and **Gemma 3**.

## What problem it solves
It eliminates the need to write custom integration code for every tool/LLM combination. By providing a universal interface, an MCP-compliant server can work with any MCP-compliant client (like Claude Desktop, Roo Code, or Vellum). It solves the "tool fragmentation" problem in the AI ecosystem by decoupling tool implementation from model-specific logic.

## Where it fits in the stack
**Category**: Protocol / Automation & Orchestration / Pattern. It serves as the "Resource Glue" and "Tool Interface" between the Reasoning Layer (LLMs) and the Action/Data Layer (Databases, APIs, Filesystems).

## Typical use cases
- **Universal Tool Access**: Giving an LLM access to a local filesystem, database, or API through a standard server.
- **Dynamic Context Injection**: Allowing models to pull in relevant documentation or code snippets as needed via "Resources".
- **Cross-Platform Agents**: Writing a tool once and using it in multiple agent frameworks (e.g., [Goose](../agents/goose.md) and [Cline](../agents/cline.md)).
- **Agent Orchestration**: Coordinating multiple specialized agents (e.g., using **Claude 5.1** for reasoning and **Gemma 3** for task-specific execution) via a shared protocol.

## Strengths
- **Ecosystem Neutrality**: Designed to be used by any model provider or agent developer (Standardized by Anthropic but vendor-agnostic).
- **Security**: Focuses on secure, locally-controlled execution of tools with fine-grained capability negotiation.
- **Extensibility**: Massive library of community-contributed MCP servers available via the [MCP Registry](mcp-registry.md).
- **Performance**: Standardized transport layers (Stdio, HTTP/SSE, and the **X402** micropayment transport) ensure low-latency communication.

## Limitations
- **Configuration Overhead**: Implementing and maintaining separate MCP services can lead to significant configuration "bloat" on both the service and client applications, especially when managing granular permissions and access tokens.
- **Service vs. Library Debate**: For simple or individual use cases, running a separate web service for basic tasks (like getting the current time) may be overkill compared to using standard programming language libraries.
- **Client Support**: Requires native support in the LLM client or agent framework to fully leverage capability negotiation.
- **Complexity for Beginners**: Designing robust, secure MCP servers requires understanding of JSON-RPC and asynchronous capability handshakes.
- **State Management**: MCP is primarily stateless; complex multi-turn state must be managed at the application layer.

## When to use it
- To provide LLMs with access to local or private data sources in a standardized way across multiple clients.
- When building tools that you want to be reusable across different AI environments (IDEs, desktop assistants, web apps).
- In enterprise environments where centralized tool management and secure, audited access to internal resources are required.
- When implementing "Agentic RAG" patterns where the model needs to decide which context to retrieve.

## When not to use it
- **Simple, One-off Tools**: For individual developers building a tool for a single system, the overhead of the MCP protocol may not be justified.
- **CLI-Native Agents**: If an agent already has shell/terminal access, standard CLI tools are often more efficient and easier to integrate than wrapping them in an MCP service.
- **Library-First Architectures**: When tools can be easily shared as standard package libraries (npm, pip) and integrated directly into the agent's runtime.
- For very simple, one-off tool implementations where a basic API call is sufficient and reusability is not a concern.

## Getting started

### MCP Architecture
MCP uses a client-server architecture. A **Client** (like Claude Desktop) connects to a **Server** (a small program that exposes tools) over a transport layer.

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
  version: "3.0.0"
}, {
  capabilities: { tools: {}, resources: {} }
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
# Test an MCP server using the MCP Inspector (July 2026 version)
npx @modelcontextprotocol/inspector <command-to-run-server>

# List available tools on a local server (via Stdio)
echo '{"jsonrpc":"2.0","method":"tools/list","id":1,"params":{}}' | node my-mcp-server.js

# Use the MCP CLI to connect to a server and interact
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
- [Claude Code](../development_ops/claude-code.md) — Uses MCP for all tool interaction.
- [Roo Code](../agents/roo-code.md) — Open-source agent supporting MCP v3.0.
- [MCP Registry](mcp-registry.md) — Central catalog of MCP servers.
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) — Specific implementation pattern.
- [Cline](../agents/cline.md) — IDE agent with deep MCP integration.
- [GPT-5.5](../ai_knowledge/openai.md) — Integrated with MCP via standardized gateways.
- [n8n](../../services/n8n.md) — Supports MCP for workflow tool execution.
- [Vellum](vellum.md) — macOS assistant utilizing MCP for desktop automation.
- [Chronos MCP](chronos-mcp.md) — Standard for agentic calendar orchestration.

## Sources / references
- [Official Website](https://modelcontextprotocol.io/)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [MCP Documentation](https://modelcontextprotocol.io/docs/concepts/architecture)
- [MCP SDKs (GitHub)](https://github.com/modelcontextprotocol)
- [Reddit: MCP... Is bad? (1uvaqxp)](https://www.reddit.com/r/LocalLLaMA/comments/1uvaqxp/mcp_is_bad/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
