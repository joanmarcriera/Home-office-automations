# AI Agent Protocols

This document describes the key protocols that enable interoperability between AI agents, tools, and development environments.

## 1. Model Context Protocol (MCP)
The Model Context Protocol (MCP) is an open standard that standardizes how applications interact with large language models (LLMs) and provide them with tools and resources.

- **Developer**: Anthropic
- **Purpose**: Decouples the "brain" (LLM) from the "tools" (APIs, databases, local files).
- **Key Concepts**:
    - **MCP Servers**: Host specific tools (e.g., Google Calendar, GitHub, ClickHouse).
    - **MCP Clients**: Frameworks or IDEs that connect to servers to use their tools (e.g., Claude Agent SDK, Zed, Cursor).
- **Benefits**: Build a tool once as an MCP server and use it in any compatible agent framework or editor.
- **Pattern Guide**: [Tool Calling & MCP Patterns](patterns/tool-calling-and-mcp.md)
- **Compatible Frameworks**: [LangGraph](../tools/agents/langgraph.md), [Bee Agent Framework](../tools/agents/bee-agent-framework.md), [Composio](../tools/agents/composio.md), [Agno](../tools/agents/agno.md).
- **Sources**: [Making MCP cheaper via CLI](https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html) (Exploring lightweight CLI implementations vs server-side MCP).

## 2. Agent Client Protocol (ACP)
The Agent Client Protocol (ACP) is an open standard designed to enable any AI agent to integrate seamlessly with any code editor or editing environment.

- **Developer**: Zed
- **Purpose**: Standardizes the interface between terminal-based or external agents and the IDE's UI components (multi-file editing, syntax highlighting, diff viewing).
- **Key Concepts**:
    - **Universal Compatibility**: Any agent implementing ACP can gain access to an IDE's full codebase context and powerful reviewing tools.
    - **Privacy First**: ACP is designed to be local-first; data doesn't necessarily touch cloud servers unless specifically configured.
- **Benefits**: Allows developers to use specialized external agents (like Claude Code or Gemini CLI) directly inside their preferred IDE without proprietary plugins for each agent.

## Sources / References

- [Reference](https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: medium
