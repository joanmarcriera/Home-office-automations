# Model Context Protocol (MCP)

## What it is
The Model Context Protocol (MCP) is an open, universal standard that enables developers to build secure, two-way connections between their data sources and AI models. Introduced by Anthropic in late 2024, it has become the industry standard for "Agentic Tooling," allowing models to interact with the world through a unified interface. As of June 2026, **MCP 3.0** is the current stable version, featuring enhanced multi-agent orchestration and native discovery capabilities.

## What problem it solves
It eliminates the need to write custom integration code for every tool/LLM combination. By providing a universal interface, an MCP-compliant server (e.g., for Google Search, GitHub, or Postgres) can work instantly with any MCP-compliant client, such as [Claude Code](../development_ops/claude-code.md), [Roo Code](../agents/roo-code.md), [Vellum](vellum.md), or [Open WebUI](../../services/open-webui.md).

## Where it fits in the stack
**Protocol / Automation & Orchestration / Pattern**. It acts as the "Standard Interface" between the Reasoning Layer (LLMs) and the Action Layer (APIs, Databases, Filesystems).

## Typical use cases
- **Universal Tool Access**: Giving an LLM access to a local filesystem, database, or API through a standard server.
- **Dynamic Context Injection**: Allowing models to pull in relevant documentation or code snippets as needed during a task.
- **Cross-Platform Agents**: Writing a tool once (e.g., a "Search" tool) and using it across multiple agent frameworks without modification.
- **Agent Orchestration**: Coordinating multiple specialized agents (e.g., using **Claude 4.8** for reasoning and **Llama 4 Maverick** for task execution) via a shared protocol.
- **Self-Healing Automation**: Using MCP-based log analyzers to automatically fix homelab service failures.

## Strengths
- **Ecosystem Neutrality**: Designed to be used by any model provider (Anthropic, OpenAI, Meta, Google).
- **Security**: Focuses on secure, locally-controlled execution; tools are strictly scoped by the user.
- **Massive Ecosystem**: Over 5,000 community-contributed MCP servers available in the [MCP Registry](mcp-registry.md).
- **Performance**: High-speed communication over standardized transport layers (Stdio, HTTP/SSE).
- **Multi-Agent Native**: MCP 3.0 includes protocols for handoffs and shared memory between agents.

## Limitations
- **Client Implementation Required**: Only works with applications that have explicitly implemented the MCP client spec.
- **State Management**: While improved in v3.0, managing complex state across multiple tool calls still requires careful agent design.
- **Latency**: Network-based MCP servers (HTTP/SSE) introduce small latencies compared to native local functions.

## When to use it
- When you want to provide an LLM with access to private or local data in a standardized, secure way.
- When building tools that you want to be reusable across different AI environments (IDEs, desktop assistants, web UIs).
- For building modular [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) that require swappable tools.

## When not to use it
- For very simple, one-off tool implementations where a basic hard-coded API call is sufficient.
- If you are building a closed ecosystem where cross-tool interoperability is not a requirement.

## Getting started
### MCP Architecture
MCP uses a client-server architecture. A **Client** (e.g., Claude Desktop) connects to a **Server** (a small program that exposes tools) over a transport layer.

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
  name: "weather-mcp",
  version: "3.0.0"
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
The `mcp` CLI and inspector are the primary tools for testing and managing protocol connections.

### Protocol Inspection
```bash
# Test an MCP server using the official MCP Inspector
npx @modelcontextprotocol/inspector <command-to-run-server>

# List tools available on a local server (via Stdio)
echo '{"jsonrpc":"2.0","method":"tools/list","id":1,"params":{}}' | node my-mcp-server.js
```

### Server Management
```bash
# Install the universal MCP CLI (June 2026)
pip install mcp-cli

# Connect to a remote MCP server over SSE
mcp-cli connect sse --url https://mcp.example.com/sse
```

## API examples
MCP relies on JSON-RPC 2.0 for all communication between clients and servers.

### Tool Call (Client to Server)
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "location": "Berlin, DE"
    }
  },
  "id": 1
}
```

### Resource Read (Client to Server)
```json
{
  "jsonrpc": "2.0",
  "method": "resources/read",
  "params": {
    "uri": "file:///path/to/doc.md"
  },
  "id": 2
}
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — The reference implementation for high-fidelity MCP 3.0 use.
- [Roo Code](../agents/roo-code.md) — Multi-agent IDE extension with deep MCP support.
- [Vellum](vellum.md) — macOS assistant using MCP for desktop orchestration.
- [MCP Registry](mcp-registry.md) — Central catalog of available MCP servers and tools.
- [Chronos MCP](../automation_orchestration/mcp.md) — specialized MCP implementation for calendar sync.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Standard patterns for using MCP in autonomous loops.
- [n8n](../../services/n8n.md) — Orchestrator that can execute and expose MCP tools.
- [Open WebUI](../../services/open-webui.md) — Popular frontend for models with native MCP 3.0 support.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Recommended local model for private MCP actions.

## Sources / references
- [Official Model Context Protocol Site](https://modelcontextprotocol.io/)
- [Anthropic MCP SDK (GitHub)](https://github.com/modelcontextprotocol)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/docs/specification)
- [Building Document Agents with MCP](https://www.llamaindex.ai/blog/llamaparse-mcp-the-tooling-layer-for-your-document-agents)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
