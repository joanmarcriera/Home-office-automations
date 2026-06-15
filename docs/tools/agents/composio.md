# Composio

## What it is
Composio is a tool integration platform that connects AI agents to over 250+ external applications and services. It provides a unified way to handle authentication (OAuth, API Keys) and tool execution across different LLM frameworks. In June 2026, it serves as the "connective tissue" for agents built with **Claude 4.8 Opus** and **GPT-5.5**, enabling them to interact with complex SaaS ecosystems.

## What problem it solves
Connecting agents to real-world tools usually requires writing massive amounts of boilerplate for authentication, token management, and API calls. Composio abstracts this away, allowing agents to "login" to services like GitHub, Google Calendar, or Slack with minimal effort, while providing the developer with full observability into every tool call.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as a **Tool Integration & Auth Middleware** that acts as the "hands" for an agent.

## Typical use cases
- **Engineering Agents**: Managing GitHub issues, repositories, and CI/CD pipelines autonomously.
- **Executive Assistants**: Coordinating across Google Calendar, Gmail, and Slack to manage schedules and communications.
- **Customer Support Bots**: Checking live data in Jira, Zendesk, or Salesforce to resolve tickets with real-time context.

## Strengths
- **Massive Library**: 250+ pre-built integrations with major SaaS platforms.
- **Managed Auth**: Automatically handles complex OAuth flows, secret storage, and token refreshes.
- **Framework Agnostic**: Works with OpenAI, LangChain, CrewAI, Autogen, and the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).
- **Observability**: Detailed execution logs and debugging tools for every action performed by the agent.

## Limitations
- **External Dependency**: Relies on Composio's platform for managing connections and routing tool calls.
- **Privacy & Compliance**: Tool calls transit through Composio's infrastructure, which may require additional scrutiny for enterprise data privacy.
- **Pricing**: While there is a free tier, high-volume production use requires a paid subscription.

## When to use it
- When you need to connect an agent to multiple SaaS tools quickly and securely.
- To avoid building and maintaining your own custom OAuth integration logic for every tool.
- For projects requiring high observability and audit trails for agent-initiated actions.

## When not to use it
- For simple agents that don't need external tool access or use only a single, simple API.
- If you have strict privacy requirements that forbid third-party tool routers or managed authentication.

## Getting started
### Installation
```bash
pip install composio-core composio-openai
```

### Basic Usage
```python
from composio_openai import ComposioToolSet, App
from openai import OpenAI

# 1. Initialize OpenAI client and Composio Toolset
client = OpenAI(api_key="YOUR_OPENAI_KEY")
toolset = ComposioToolSet(api_key="YOUR_COMPOSIO_KEY")

# 2. Get tools for a specific app (e.g., GitHub)
tools = toolset.get_tools(apps=[App.GITHUB])

# 3. Create an agentic completion request using GPT-5.5
response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[{"role": "user", "content": "Star the repository 'composiohq/composio' on GitHub"}],
    tools=tools,
    tool_choice="auto"
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
- [Agno](agno.md)
- [Phidata](phidata.md)

## Sources / references
- [Official Website](https://composio.dev/)
- [Documentation](https://docs.composio.dev/)
- [GitHub Repository](https://github.com/composiohq/composio)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
