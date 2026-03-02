# Tool Calling & Model Context Protocol (MCP)

## What it is
**Tool calling** (also known as function calling) is a standardized pattern where Large Language Models (LLMs) generate structured data (typically JSON) to signal their intent to invoke external functions, rather than just generating text. This allows the model to act as a "reasoning engine" that can decide when and how to use external capabilities.

**Model Context Protocol (MCP)** is an open, universal standard introduced by Anthropic that provides a unified way to connect LLMs to external tools and data sources. It decouples the model from the specific implementations of tools, allowing a single MCP server to provide capabilities to any compatible LLM host (IDE, agent framework, or chat interface).

## What problem it solves
LLMs are traditionally "isolated" from the real world, limited by their training data and the text-based interface of their context window. Tool calling and MCP solve several critical limitations:
- **Dynamic Data Access**: Allows LLMs to query databases, search the web, or read local files to get up-to-date information.
- **Real-World Actions**: Enables LLMs to perform operations like sending emails, updating Jira tickets, or controlling a browser.
- **Complex Logic**: Offloads tasks like mathematical calculations, data processing, or code execution to specialized software.
- **Ecosystem Portability**: MCP specifically solves the "N-to-M" problem where every agent framework needs its own integration for every tool. With MCP, you build a tool once and it works everywhere.

## How tool calling works
The tool calling cycle typically follows these steps:
1.  **Tool Definition**: The developer provides the LLM with a list of available tools, defined using a structured schema (usually JSON Schema) that includes names, descriptions, and parameter types.
2.  **LLM Decision**: Based on the user prompt, the LLM determines if a tool is needed. If so, it generates a structured call (JSON) instead of a text response.
3.  **Client Execution**: The application (the "host" or "client") receives the JSON, validates it, and executes the corresponding function in its environment.
4.  **Result Feedback**: The tool's output is sent back to the LLM as a new message in the conversation history.
5.  **Final Response**: The LLM incorporates the tool result into its reasoning to provide a final answer to the user.

### Example: Tool Definition (JSON Schema)
```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"]
      }
    },
    "required": ["location"]
  }
}
```

### Example: LLM Response (Tool Call)
```json
{
  "tool_calls": [
    {
      "id": "call_12345abc",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"location\": \"San Francisco, CA\", \"unit\": \"celsius\"}"
      }
    }
  ]
}
```

## MCP architecture
MCP uses a client-server architecture to standardize the connection between AI applications and data/tools.

### Core Components
- **Hosts**: The primary application where the LLM is running (e.g., Claude Desktop, Zed, Cursor, or a custom agent). The host manages the LLM's lifecycle.
- **Clients**: Reside within the host and maintain 1:1 connections with MCP servers.
- **Servers**: Lightweight programs that expose specific capabilities (tools, resources, or prompts) through the MCP protocol.
- **Transport Layer**: The communication medium between client and server.
    - **stdio**: Standard input/output (most common for local tools).
    - **SSE**: Server-Sent Events (used for remote servers over HTTP).
    - **HTTP/TCP**: Direct socket-based communication.
- **Capabilities**:
    - **Resources**: Read-only data (e.g., a file's content, a database schema).
    - **Tools**: Executable functions (e.g., "create_file", "search_web").
    - **Prompts**: Reusable prompt templates (e.g., "analyze_codebase").
    - **Sampling**: Allows a server to ask the client to run an LLM completion (agentic servers).

### MCP Client-Server Flow
```text
  ┌──────────────┐             ┌──────────────┐             ┌──────────────┐
  │     Host     │             │  MCP Client  │             │  MCP Server  │
  │ (IDE, Agent) │             │ (in context) │             │ (Local/Remote)│
  └──────┬───────┘             └──────┬───────┘             └──────┬───────┘
         │                            │                            │
         │  Initialize Connection     │                            │
         ├───────────────────────────>│      List Capabilities     │
         │                            ├───────────────────────────>│
         │                            │    Tools, Resources, etc.  │
         │                            |<───────────────────────────┤
         │                            │                            │
         │    User Request            │                            │
         ├───────────────────────────>│                            │
         │   (LLM decides tool use)   │                            │
         │                            │      Call Tool (args)      │
         │                            ├───────────────────────────>│
         │                            │      Execute Function      │
         │                            │                            │
         │                            │      Tool Result           │
         │                            |<───────────────────────────┤
         │    Process Result          │                            │
         |<───────────────────────────┤                            │
         │                            │                            │
  ┌──────┴───────┐             ┌──────┴───────┘             ┌──────┴───────┐
```

## Getting started

### 1. Basic Tool Calling

=== "Anthropic Python SDK"
    ```python
    import anthropic

    client = anthropic.Anthropic()

    # (1) Define tools
    tools = [{
        "name": "get_stock_price",
        "description": "Retrieves the current stock price for a given ticker symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "The stock ticker, e.g. AAPL"}
            },
            "required": ["ticker"]
        }
    }]

    # (2) Request completion with tools
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[{"role": "user", "content": "What is the price of AAPL?"}]
    )

    # (3) Process the tool_use content block
    print(message.content)
    ```

=== "OpenAI Python SDK"
    ```python
    from openai import OpenAI

    client = OpenAI()

    # (1) Define functions
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state"}
                },
                "required": ["location"]
            }
        }
    }]

    # (2) Request chat completion
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "What's the weather in London?"}],
        tools=tools
    )

    # (3) Access tool_calls from the message
    print(response.choices[0].message.tool_calls)
    ```

### 2. Simple MCP Server (Python SDK)

To build a server, use the `mcp` Python SDK and `FastMCP` for a high-level API.

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

## Patterns

### Single Tool Use
The model identifies that a specific tool is required to satisfy the user request, generates the call, and waits for the result. This is the simplest implementation, used for queries like "Check the weather" or "Look up this user's email."

### Multi-tool Chaining
The LLM uses multiple tools in sequence, where the output of one tool serves as the input (or part of the reasoning) for the next call.
- **Example**: An agent first calls `search_files` to find a specific document, then calls `read_file` using the path returned, and finally calls `summarize_text` on the content.

### Parallel Tool Calls
Modern LLMs can generate multiple tool calls in a single turn. This is highly efficient for fetching independent pieces of information.
- **Example**: When asked to "compare the stock prices of Apple, Nvidia, and Microsoft," the model can return three `get_stock_price` calls at once. The runtime executes them in parallel and returns all results to the model simultaneously.

### Tool Use with Confirmation (Human-in-the-Loop)
For sensitive operations (writing files, deleting data, sending emails), the runtime intercepts the tool call and prompts the user for approval.
- **Implementation**: The host application renders the proposed tool arguments to the user. The tool is only executed if the user confirms; otherwise, a "user canceled" error is sent back to the model.

### MCP Server Composition
A core benefit of MCP is the ability for a single client (like Claude Desktop or an agent) to connect to many independent servers. This creates a "composable brain" where specialized servers for Google Calendar, Slack, GitHub, and local databases can be aggregated into a single assistant without code changes.

## When to use it
- **Factual Accuracy**: When you need the model to use real-time or verified data instead of hallucinating answers.
- **Action-Oriented Agents**: When the purpose of the LLM is to perform tasks, not just provide information.
- **Standardizing Toolkits**: Use MCP when building tools that need to be shared across different AI environments (Zed, Cursor, Claude).
- **Security & Control**: When you want to strictly control what actions the LLM can take by defining a rigid API (tool schema).

## When not to use it
- **Simple Creative Writing**: When the task is purely linguistic (e.g., "Write a poem about a cat").
- **High Latency Concerns**: If the external API or database is slow and real-time response is required.
- **Static Knowledge**: If the information is common knowledge and the training data is sufficient.
- **Over-Complexity**: If the task can be solved more reliably by simple prompt engineering or fixed data insertion.

## Related tools / concepts
- [Agent Protocols](../agent_protocols.md) — Broader context for MCP and ACP.
- [LangChain](../../tools/ai_knowledge/langchain.md) — Multi-model library for tool calling.
- [OpenRouter](../../tools/ai_knowledge/openrouter.md) — Unified API for accessing multiple tool-calling models.
- [Browser Use](../../tools/automation_orchestration/browser-use.md) — Agentic browser control via tool calling.
- [Composio](../../tools/agents/composio.md) — Tool integration platform.

### Agent Frameworks
- [Agency Swarm](../../tools/agents/agency-swarm.md)
- [Agno](../../tools/agents/agno.md)
- [Bee Agent Framework](../../tools/agents/bee-agent-framework.md)
- [LangGraph](../../tools/agents/langgraph.md)
- [Phidata](../../tools/agents/phidata.md)
- [AutoGen](../../tools/frameworks/autogen.md)
- [CrewAI](../../tools/frameworks/crewai.md)
- [DSPy](../../tools/frameworks/dspy.md)
- [Haystack](../../tools/frameworks/haystack.md)
- [Mycelium](../../tools/frameworks/mycelium.md)
- [Semantic Kernel](../../tools/frameworks/semantic-kernel.md)
- [Smolagents](../../tools/frameworks/smolagents.md)

### Specific MCP Implementations
- [Atlassian Jira MCP](../../tools/automation_orchestration/atlassian-jira-mcp.md)
- [ServiceNow MCP](../../tools/automation_orchestration/servicenow-mcp.md)
- [MCP Registry](../../tools/automation_orchestration/mcp-registry.md)

## Sources / references
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
