# Tool Calling & Model Context Protocol (MCP)

## What it is
**Tool calling** (also known as function calling) is a pattern where Large Language Models (LLMs) generate structured data (typically JSON) to signal their intent to invoke external functions, rather than just generating text.

**Model Context Protocol (MCP)** is an open standard, introduced by Anthropic, that provides a universal way to connect LLMs to external tools and data sources. It standardizes the interface between "hosts" (like IDEs or agent frameworks), "clients", and "servers" that provide specific capabilities.

## What problem it solves
LLMs are traditionally limited to the knowledge present in their training data and the text-based interface of their context window. Tool calling and MCP extend these capabilities by allowing LLMs to:
- **Interact with the real world**: Perform database queries, send emails, or trigger API calls.
- **Access fresh data**: Retrieve real-time information from the web or internal systems.
- **Perform complex computations**: Offload mathematical or logic-heavy tasks to specialized code.
- **Control environments**: Manipulate files, run shell commands, or navigate browsers.

## How tool calling works
1.  **Function/Tool Definition**: The developer provides the LLM with a list of available tools, defined using a structured schema (usually JSON Schema).
2.  **LLM Generates Structured Call**: When the LLM decides a tool is needed, it outputs a JSON object containing the tool name and the required arguments.
3.  **Runtime Executes**: The application (runtime) parses the JSON, executes the actual function, and captures the result.
4.  **LLM Incorporates Result**: The result is sent back to the LLM as a "tool" message. The LLM then uses this information to continue the conversation or generate a final response.

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
MCP introduces a standardized client-server architecture to make tools portable across different LLM applications.

- **Hosts**: The environment where the LLM lives (e.g., Claude Desktop, Zed, Cursor, an agent framework).
- **Clients**: Connect to MCP servers and handle the communication protocol.
- **Servers**: Provide specific tools, resources, or prompts via the MCP standard.
- **Transport Layer**: Defines how messages move between client and server (e.g., `stdio` for local processes, `SSE` for remote web servers).
- **Components**:
    - **Resources**: Read-only data (files, database records).
    - **Tools**: Executable functions that can change state.
    - **Prompts**: Pre-defined templates for interacting with the LLM.
    - **Sampling**: Allowing servers to request completions from the LLM via the client.

### MCP Client-Server Flow
```text
  [ Host Application ]
          |
  [   MCP Client    ] <--- (Transport: stdio/SSE/HTTP) ---> [   MCP Server    ]
          |                                               |
  (1) List Tools    -------------------------------------> |
  (2) Tool List     <------------------------------------- (Return available tools)
          |                                               |
  (3) Call Tool     -------------------------------------> |
  (4) Execution     <------------------------------------- (Run code/API call)
  (5) Tool Result   <------------------------------------- |
```

## Getting started

### 1. Basic Tool Calling (Anthropic Python SDK)
```python
import anthropic

client = anthropic.Anthropic()

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

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What is the price of AAPL?"}]
)

print(message.content) # Contains the tool use request
```

### 2. Simple MCP Server (Python SDK)
```python
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("WeatherService")

@mcp.tool()
def get_weather(location: str) -> str:
    """Get the weather for a specific location."""
    return f"The weather in {location} is sunny, 25°C."

if __name__ == "__main__":
    mcp.run()
```

## Patterns
- **Single Tool Use**: The LLM calls one tool to answer a specific question.
- **Multi-tool Chaining**: The LLM uses the output of one tool as the input for another (e.g., search for a user ID, then fetch their orders).
- **Parallel Tool Calls**: The LLM requests multiple tool executions simultaneously to save time (e.g., checking prices from three different vendors at once).
- **Tool Use with Confirmation (Human-in-the-Loop)**: The application intercepts sensitive tool calls (like "delete_database" or "send_email") and waits for user approval before execution.
- **MCP Server Composition**: A single MCP client connecting to multiple specialized MCP servers, aggregating their capabilities into a unified agent.

## When to use it
- When you need to bridge the gap between LLM reasoning and external systems.
- When you want to build reusable toolkits that work across different agents/IDEs (MCP).
- When you need factual accuracy that requires querying a source of truth.

## When not to use it
- For tasks that are purely creative or linguistic.
- When the latency of an external call is unacceptable.
- When the task can be solved by simply providing the information in the system prompt.

## Related tools / concepts
- [Agent Protocols](../agent_protocols.md)
- [LangChain](../../tools/ai_knowledge/langchain.md)
- [OpenRouter](../../tools/ai_knowledge/openrouter.md)
- [Browser Use](../../tools/automation_orchestration/browser-use.md)
- [Composio](../../tools/agents/composio.md)
- **Agent Frameworks**: [LangGraph](../../tools/agents/langgraph.md), [CrewAI](../../tools/frameworks/crewai.md), [AutoGen](../../tools/frameworks/autogen.md), [Agno](../../tools/agents/agno.md), [Agency Swarm](../../tools/agents/agency-swarm.md), [Smolagents](../../tools/frameworks/smolagents.md)

## Sources / references
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)

## Contribution Metadata
- Last reviewed: 2026-02-27
- Confidence: high
