# Composio

## What it is
Composio is a tool integration platform that connects AI agents to over 250+ external applications and services. It provides a unified way to handle authentication (OAuth, API Keys) and tool execution across different LLM frameworks. In July 2026, it serves as the "connective tissue" for agents built with **Claude 4.8 Opus** and **GPT-5.5**, and now features native **FastMCP 3.0** tool hosting for ultra-low latency tool execution.

## What problem it solves
Connecting agents to real-world tools usually requires writing massive amounts of boilerplate for authentication, token management, and API calls. Composio abstracts this away, allowing agents to "login" to services like GitHub, Google Calendar, or Slack with minimal effort, while providing the developer with full observability into every tool call. It now also solves the problem of "tool latency" by leveraging the FastMCP protocol.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as a **Tool Integration & Auth Middleware** that acts as the "hands" for an agent.

## Typical use cases
- **Engineering Agents**: Managing GitHub issues, repositories, and CI/CD pipelines autonomously.
- **Executive Assistants**: Coordinating across Google Calendar, Gmail, and Slack to manage schedules and communications.
- **Customer Support Bots**: Checking live data in Jira, Zendesk, or Salesforce to resolve tickets with real-time context.
- **DevOps Agents**: Using [FastMCP](../automation_orchestration/mcp.md) to execute high-frequency infrastructure commands with minimal overhead.

## Strengths
- **Massive Library**: 250+ pre-built integrations with major SaaS platforms.
- **Managed Auth**: Automatically handles complex OAuth flows, secret storage, and token refreshes.
- **Framework Agnostic**: Works with OpenAI, [LangChain](../ai_knowledge/langchain.md), [CrewAI](../frameworks/crewai.md), [Autogen](../frameworks/autogen.md), and the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).
- **FastMCP 3.0 Integration**: Native support for high-performance tool hosting and standardized agentic interactions.

## Limitations
- **External Dependency**: Relies on Composio's platform for managing connections and routing tool calls.
- **Privacy & Compliance**: Tool calls transit through Composio's infrastructure, which may require additional scrutiny for enterprise data privacy.
- **Pricing**: While there is a free tier, high-volume production use requires a paid subscription.

## When to use it
- When you need to connect an agent to multiple SaaS tools quickly and securely.
- To avoid building and maintaining your own custom OAuth integration logic for every tool.
- For projects requiring high observability and audit trails for agent-initiated actions.
- When using **Claude 4.8** or **GPT-5.5** and wanting the most robust tool-calling ecosystem available.

## When not to use it
- For simple agents that don't need external tool access or use only a single, simple API.
- If you have strict privacy requirements that forbid third-party tool routers or managed authentication.
- In environments with no external internet access (unless using a self-hosted enterprise version).

## Getting started
### Installation
```bash
pip install composio-core composio-openai
```

### Basic Usage (with Claude 4.8 and FastMCP)
```python
from composio_anthropic import ComposioToolSet, App
from anthropic import Anthropic

# 1. Initialize Anthropic client and Composio Toolset
client = Anthropic(api_key="YOUR_ANTHROPIC_KEY")
toolset = ComposioToolSet(api_key="YOUR_COMPOSIO_KEY")

# 2. Get tools for a specific app (e.g., GitHub) using FastMCP
tools = toolset.get_tools(apps=[App.GITHUB], protocol="fastmcp")

# 3. Create an agentic completion request using Claude 4.8
response = client.messages.create(
    model="claude-4.8-opus",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Star the repository 'composiohq/composio' on GitHub"}],
    tools=tools
)

# 4. Execute the tool call via Composio
result = toolset.handle_tool_calls(response)
print(result)
```

## CLI examples
```bash
# Login to Composio and authenticate your machine
composio login

# Add an integration (this will open an OAuth flow in your browser)
composio add github

# List all active integrations and their status
composio list

# Execute an action directly from the CLI for testing
composio run github star-repo --params '{"owner": "composiohq", "repo": "composio"}'
```

## API examples
```python
from composio_openai import ComposioToolSet, App

toolset = ComposioToolSet(api_key="YOUR_COMPOSIO_KEY")

# List all available actions for an application to understand its capabilities
actions = toolset.get_actions(apps=[App.SLACK])
for action in actions:
    print(f"Action: {action.name} - {action.description}")

# Manually trigger an action without a full LLM loop
result = toolset.execute_action(
    action="GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER",
    params={"owner": "composiohq", "repo": "composio"}
)
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Zapier](../automation_orchestration/zapier.md)
- [Make](../automation_orchestration/make.md)
- [CrewAI](../frameworks/crewai.md)
- [LangGraph](../frameworks/langgraph.md)
- [Agno](./agno.md)
- [Phidata](./phidata.md)
- [Agency Swarm](./agency-swarm.md)

## Sources / references
- [Official Website](https://composio.dev/)
- [Documentation](https://docs.composio.dev/)
- [GitHub Repository](https://github.com/composiohq/composio)
- [FastMCP Integration Docs](https://docs.composio.dev/protocols/fastmcp)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
