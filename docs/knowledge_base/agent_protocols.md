# AI Agent Protocols

## What it is
AI Agent Protocols are open standards that enable interoperability between AI agents, tools, development environments, and data sources. This document focuses on the **Model Context Protocol (MCP)** and the **Agent Client Protocol (ACP)**, which together form the backbone of a modern, modular AI ecosystem.

## What problem it solves
The AI landscape is fragmented, with agents often locked into proprietary tool integrations or specific IDEs. Protocols solve this by decoupling the "brain" (the LLM) from the "tools" (APIs, databases, filesystems) and the "interface" (IDE components). This allows developers to build a tool once and use it across any compatible agent framework or code editor.

## Where it fits in the stack
Protocols act as the **Communication Layer** in the AI stack. They sit between agent frameworks (like LangGraph or Bee) and external resources (like GitHub, Slack, or local SQLite databases), ensuring that every component can "speak the same language" regardless of its implementation.

## Typical use cases
- **Universal Tool Access**: Using an MCP server for Google Calendar in both a terminal-based agent (Claude Code) and a visual IDE (Zed).
- **Local-First Development**: Running a local MCP server to give an agent access to private project files without uploading them to a third-party cloud.
- **Cross-IDE Agents**: Implementing an agent once using ACP so it can seamlessly edit code and show diffs in Cursor, Zed, and VS Code.

## Strengths
- **Modular Architecture**: Swap LLMs or tools without rewriting integration logic.
- **Privacy & Security**: Keep sensitive data access local via private MCP servers.
- **Ecosystem Growth**: Fast-tracks the adoption of new AI tools by making them instantly compatible with established frameworks.

## Limitations
- **Latency**: Protocol-based communication can introduce minor overhead compared to direct native integrations.
- **Standardization Lag**: As frontier model capabilities evolve rapidly, protocols must be updated frequently to support new interaction patterns.

## When to use it
- When building a modular AI system that needs to support multiple toolsets or environments.
- To ensure your AI tools remain compatible with the widest possible range of agent frameworks.
- When local data privacy and controlled resource access are primary requirements.

## When not to use it
- For extremely simple, single-purpose agents where the overhead of implementing a protocol outweighs the benefits of modularity.
- When using a closed, end-to-end proprietary platform that does not support external protocol integrations.

## Getting started

### 1. Simple MCP Server (Python SDK)
To build a server, use the `mcp` Python SDK and `FastMCP` for a high-level API. This example creates a weather tool that can be used by any MCP-compatible host.

```python
# pip install mcp
from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("WeatherService")

@mcp.tool()
def get_weather(location: str) -> str:
    """Get the weather for a specific location.

    Args:
        location: The city and state (e.g., London, UK)
    """
    # In a real implementation, you'd call a weather API here
    return f"The weather in {location} is currently sunny, 22°C."

if __name__ == "__main__":
    # Runs the server using the stdio transport by default
    mcp.run()
```

### 2. Consuming MCP Tools
Once your server is running, you can add it to an MCP host like **Claude Desktop**. Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/your/weather_server.py"]
    }
  }
}
```

## Protocol Details

### 1. Model Context Protocol (MCP)
The Model Context Protocol (MCP) is an open standard that standardizes how applications interact with LLMs and provide them with tools and resources. It decouples the "brain" (LLM) from the "tools" (data sources and APIs), allowing for a plug-and-play AI ecosystem.
- **Developer**: Anthropic

#### Architecture & Components
- **Hosts**: The primary application where the LLM is running (e.g., Claude Desktop, Zed, Cursor, or a custom agent). The host manages the LLM's lifecycle and orchestrates the connection to servers.
- **Clients**: Reside within the host and maintain 1:1 connections with MCP servers.
- **Servers**: Lightweight programs that expose specific capabilities (tools, resources, or prompts) through the MCP protocol.

#### Transport Layers
MCP supports multiple communication mediums between clients and servers:
- **stdio**: Standard input/output. This is the most common transport for local tools and command-line utilities.
- **SSE**: Server-Sent Events. Used for remote servers communicating over HTTP.
- **HTTP/TCP**: Direct socket-based communication for specialized high-performance needs.

#### Capabilities
- **Resources**: Read-only data sources that the model can reference (e.g., a file's content, a database schema, or a documentation page).
- **Tools**: Executable functions that allow the model to perform actions (e.g., "create_file", "search_web", or "send_email").
- **Prompts**: Reusable prompt templates that can be dynamically populated by the server.
- **Sampling**: An advanced feature that allows a server to ask the client to run an LLM completion, enabling agentic servers to recurse or delegate tasks.

- **Pattern Guide**: [Tool Calling & MCP Patterns](patterns/tool-calling-and-mcp.md)

### 2. Agent Client Protocol (ACP)
The Agent Client Protocol (ACP) enables any AI agent to integrate seamlessly with any code editor or editing environment. While MCP focuses on the connection between the model and its tools, ACP focuses on the connection between the agent and the developer's workspace.
- **Developer**: Zed

#### Key Concepts
- **Universal IDE Compatibility**: ACP provides a standardized interface for agents to interact with different code editors (Cursor, Zed, VS Code) without needing custom plugins for each.
- **Multi-file Editing**: Standardizes how agents propose changes across multiple files simultaneously, ensuring atomic updates and consistency.
- **Rich Feedback**: Enables agents to receive syntax highlighting, linting errors, and test results directly from the IDE.
- **Diff Management**: Provides a consistent way for agents to present diffs to the user for review and approval before applying changes.
- **Privacy First**: Designed to be local-first, ensuring that workspace data and agent interactions remain on the user's machine.

## Related tools / concepts
- [Tool Calling & MCP Patterns](patterns/tool-calling-and-mcp.md)
- [LangGraph](../tools/agents/langgraph.md)
- [Bee Agent Framework](../tools/agents/bee-agent-framework.md)
- [Composio](../tools/agents/composio.md)
- [Agno](../tools/agents/agno.md)
- [Mistral AI](../tools/providers/mistral.md)
- [Claude Agent SDK](../tools/ai_knowledge/claude-howto.md)
- [OpenClaw Patterns](patterns/openclaw-use-case-catalog.md)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15

## Sources / References
- [Making MCP cheaper via CLI](https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Agent Client Protocol Announcement](https://zed.dev/blog/agent-client-protocol)
