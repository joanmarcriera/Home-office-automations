# Tool Calling & Model Context Protocol (MCP)

## What it is
**Tool calling** (also known as function calling) is a standardized pattern where Large Language Models (LLMs) generate structured data (typically JSON) to signal their intent to invoke external functions, rather than just generating text. This allows the model to act as a "reasoning engine" that can decide when and how to use external capabilities.

**Model Context Protocol (MCP 3.0)** is the June 2026 universal standard that provides a unified, secure way to connect LLMs (like Claude 4.8 and GPT-5.5) to external tools, resources, and data sources. It decouples the model from specific tool implementations, allowing a single MCP server to provide capabilities to any compatible host (IDE, agent framework, or chat interface).

## What problem it solves
LLMs are traditionally "isolated" from the real world, limited by their training data and the text-based interface of their context window. Tool calling and MCP solve several critical limitations:
- **Dynamic Data Access**: Allows LLMs to query databases, search the web, or read local files to get up-to-date information.
- **Real-World Actions**: Enables LLMs to perform operations like sending emails, updating Jira tickets, or controlling a browser.
- **Ecosystem Portability**: MCP specifically solves the "N-to-M" problem where every agent framework needs its own integration for every tool. With MCP 3.0, you build a tool once and it works across all agentic platforms.
- **Agentic Recursion**: Through the "Sampling" capability, MCP allows tools to recursively call back into the model to solve sub-problems.

## Where it fits in the stack
Within the AI Tooling Landscape, Tool Calling and MCP sit at **Layer 4 (Protocols & Standards)**. They serve as the critical interface between Layer 2/3 (Models and Inference) and Layer 5/6 (Frameworks and Agents), enabling standardized communication between the "brain" and its "hands."

## Typical use cases
- **Autonomous Development**: Searching codebases, running tests, and managing Git repositories via [Claude Code](../../tools/development_ops/claude-code-container-mcp.md) or [Aider](../../tools/development_ops/aider.md).
- **Personal Agentic Planning**: Checking calendars, scheduling meetings, and managing tasks via [Google Calendar](../../tools/calendar_tasks/google_calendar.md) and [Vikunja](../../services/vikunja.md) MCP servers.
- **Enterprise Automation**: Connecting AI agents to legacy systems like [Jira](../../tools/automation_orchestration/atlassian-jira-mcp.md), [ServiceNow](../../tools/automation_orchestration/servicenow-mcp.md), or Slack.
- **Secure System Remediation**: Allowing agents to interact with host operating systems via [Desktop Commander](../../tools/development_ops/desktop-commander-mcp.md) to fix configuration drift.

## Strengths
- **Universal Interoperability**: MCP 3.0 allows one tool implementation to serve multiple LLMs (Claude, GPT, Llama, Gemini).
- **Grounding & Trust**: Reduces hallucinations by forcing the model to rely on external, verifiable data sources.
- **Dynamic Discovery**: MCP servers describe their capabilities to the host at runtime, enabling plug-and-play agentic architectures.
- **Security Isolation**: Supports secure SSH tunneling and containerized execution for sensitive tool operations.

## Limitations
- **Latency Overheads**: Each tool call requires an extra round-trip to the model, which can impact real-time responsiveness.
- **Token Consumption**: Tool definitions and result data consume space in the context window, increasing cost.
- **Reasoning Failures**: Even frontier models can occasionally fail to generate valid JSON or choose the wrong tool for a complex task.
- **Permission Complexity**: Granting an LLM autonomous tool access requires sophisticated "Human-in-the-Loop" approval flows for sensitive actions.

## When to use it
- **Factual Accuracy**: When you need the model to use real-time or verified data instead of relying on training data.
- **Action-Oriented Agents**: When the purpose of the LLM is to perform tasks (e.g., "Book a flight") rather than just summarize information.
- **Standardizing Toolkits**: When building tools that need to be shared across different IDEs (Zed, Cursor, Windsurf) or frameworks.
- **Secure Data Retrieval**: When accessing private databases or local files that cannot be sent to a model for training.

## When not to use it
- **Purely Linguistic Tasks**: For creative writing, poetry, or summarization where no external data is required.
- **Sub-100ms Latency Requirements**: If the task must be completed faster than a model round-trip allows.
- **Static Knowledge Queries**: If the information is common knowledge (e.g., "What is the capital of France?").
- **Low-Reliability Environments**: Where the connection to the MCP server or the external API is unstable.

## Getting started

### 1. Building an MCP 3.0 Server (Python)
The `FastMCP` SDK is the recommended way to build servers in 2026.

```python
# pip install mcp
from mcp.server.fastmcp import FastMCP

# Create a server instance
mcp = FastMCP("SystemHealth")

@mcp.tool()
def get_cpu_usage() -> str:
    """Get the current CPU usage of the host system."""
    import psutil
    return f"Current CPU usage: {psutil.cpu_percent()}%"

if __name__ == "__main__":
    mcp.run()
```

### 2. Registering an MCP Server in Claude Desktop
Add the server configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "health-check": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

## CLI examples

### Inspecting an MCP Server
Using the `mcp-cli` to verify server capabilities:

```bash
# List all tools and resources provided by a local server
mcp-cli list --server-path ./my_server.py

# Manually trigger a tool call for testing
mcp-cli call get_cpu_usage --server-path ./my_server.py
```

### Managing Remote MCP Connections
```bash
# Connect to a remote MCP server via secure SSH tunnel
mcp-cli connect ssh://user@remote-host:port/server-name
```

## API examples

### Sampling with MCP 3.0
The Sampling capability allows an MCP server to ask the client (host) to run an LLM completion.

```python
# In an MCP server tool definition
async def complex_task(query: str, ctx: Context):
    # Ask the client to use its LLM to summarize intermediate results
    summary = await ctx.sample(
        prompt=f"Summarize these technical logs: {query}",
        max_tokens=100
    )
    return f"Analysis complete: {summary}"
```

### Parallel Tool Calling (OpenAI SDK)
Frontier models can generate multiple calls in one turn.

```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5.5-pro",
    messages=[{"role": "user", "content": "Check the weather in London, NYC, and Tokyo."}],
    tools=weather_tools # Defined with list of 3 calls
)

# Process all 3 tool calls in parallel
for tool_call in response.choices[0].message.tool_calls:
    execute_tool(tool_call)
```

## Related tools / concepts
- [Agent Protocols](../agent_protocols.md) — The broader context for MCP and ACP.
- [Agno](../../tools/agents/agno.md) — Agentic framework with native MCP 3.0 support.
- [Bee Agent Framework](../../tools/agents/bee-agent-framework.md) — IBM's framework for observability-by-design tool use.
- [Desktop Commander MCP](../../tools/development_ops/desktop-commander-mcp.md) — Standard server for local OS interaction.
- [Symbolic MCP](../../tools/development_ops/symbolic-mcp.md) — Formal verification via tool calling.
- [Vikunja MCP](../../tools/automation_orchestration/vikunja-mcp.md) — Task management via MCP.
- [Chronos MCP](../../tools/automation_orchestration/chronos-mcp.md) — Advanced scheduling tool.
- [Jupyter Kernel MCP](../../tools/development_ops/jupyter-kernel-mcp.md) — Code execution environment.

## Sources / references
- [Model Context Protocol (MCP) Official Specification](https://modelcontextprotocol.io/)
- [Anthropic: Introducing MCP 3.0 (June 2026)](https://www.anthropic.com/news/model-context-protocol-3)
- [MCP Registry: A Global Catalog of MCP Servers](https://mcp-registry.org/)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
