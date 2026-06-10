# Model Context Protocol (MCP)

## What it is
The Model Context Protocol (MCP) is an open standard that enables developers to build secure, two-way connections between their data sources and AI models. Introduced by Anthropic in late 2024 and donated to the **Agentic AI Foundation (Linux Foundation)** in December 2025, it has become the de facto industry standard for tool-model interoperability.

## What problem it solves
It eliminates the "N×M" integration problem where every AI application needs a custom connector for every data source. By providing a universal interface, an MCP-compliant server works seamlessly with any MCP-compliant client (e.g., Claude 4.8, GPT-5.5, Gemini 2.0).

## Where it fits in the stack
**Protocol / Automation & Orchestration / Pattern**. It acts as the "USB-C for AI," standardizing how models interact with external tools and private data.

## Typical use cases
- **Universal Tool Access**: Providing models like Claude 4.7/4.8 with access to local filesystems, databases, or APIs.
- **Dynamic Context Injection**: Allowing agents to pull in documentation or code snippets in real-time.
- **Enterprise Agentic Workflows**: Standardizing internal tool access for Fortune 500 AI deployments (28% adoption as of 2026).

## Strengths
- **Vendor Neutrality**: Governed by the Linux Foundation, ensuring broad adoption by Anthropic, OpenAI, Google, and Microsoft.
- **Security**: Focuses on secure, locally-controlled execution and fine-grained permissions to mitigate "tool poisoning" risks.
- **Ecosystem Growth**: 97M+ monthly SDK downloads and over 10,000 active community servers.
- **UI Integration**: "MCP Apps" extension support allows servers to provide custom UI elements directly within chat interfaces.

## Limitations
- **Security Overhead**: Requires rigorous validation of tool inputs to prevent prompt injection and data exfiltration.
- **Transport Complexity**: High-scale deployments may require advanced load balancing for Stdio and SSE transports.

## When to use it
- To provide LLMs with access to local or private data sources in a standardized way.
- When building tools that must be reusable across different AI environments and agent frameworks.

## When not to use it
- For trivial, static tool implementations where a basic JSON API call is sufficient.
- In environments where the transport overhead of a separate server process is unacceptable.

## Getting started

### MCP Architecture
MCP uses a client-server architecture. A **Host** (AI application) connects to a **Server** (program exposing tools/resources) over transports like **Stdio**, **HTTP/SSE**, or the new **gRPC-based** high-throughput transport introduced in the 2026-07-28 spec.

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

### Developing a FastMCP Server (Python)
As of 2026, **FastMCP 3.0** is the preferred way to build production-ready servers in Python.

```python
from fastmcp import FastMCP

mcp = FastMCP("weather-service", description="Fetch real-time weather data")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather for a specific location."""
    # Logic to fetch weather
    return f"The weather in {location} is sunny, 22°C."

if __name__ == "__main__":
    mcp.run()
```

## CLI examples
The MCP CLI helps in testing and debugging servers.

```bash
# Inspect a local server
mcp inspect npx @modelcontextprotocol/server-postgres

# List tools exposed by a server
mcp tools list --transport stdio --command python3 --args [ "server.py" ]

# Test a specific tool call
mcp call get_weather --params '{ "location": "San Francisco" }'
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — Uses MCP for deep filesystem and terminal access.
- [Roo Code](../agents/roo-code.md) — Open-source agent framework with native MCP support.
- [MCP Registry](mcp-registry.md) — Community hub for discovering MCP servers.
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) — Pattern for enterprise data access.
- [Cline](../agents/cline.md) — VS Code extension leveraging MCP for autonomous coding.
- [Verba](../intake_storage/verba.md) — Native MCP support for RAG-based tool calling.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The architectural context for MCP usage.
- [Ollama](../../services/ollama.md) — Local inference engine often used as an MCP client.

## Sources / References
- [Official Website](https://modelcontextprotocol.io/)
- [Agentic AI Foundation](https://agentic-ai.org/)
- [MCP 2026 Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- [The State of MCP H1 2026](https://serpapi.com/blog/the-state-of-mcp-everything-that-changed-in-h1-2026/)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
