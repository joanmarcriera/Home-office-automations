# Composio

## What it is
Composio is a tool integration platform that connects AI agents to over 250+ external applications and services. It provides a unified way to handle authentication (OAuth, API Keys) and tool execution across different LLM frameworks.

## What problem it solves
Connecting agents to real-world tools usually requires writing boilerplate for authentication and API calls. Composio abstracts this away, allowing agents to "login" to services like GitHub, Google Calendar, or Slack with minimal effort.

## Where it fits in the stack
[Tool / Infrastructure / Middleware] - It acts as the "hands" for an agent, providing a standard interface to external APIs.

## Typical use cases
- Agents that need to manage GitHub issues or repositories
- Personal assistants that interact with Google Calendar or Gmail
- Customer support bots that check Jira or Slack

## Strengths
- **Massive Library**: 250+ pre-built integrations.
- **Managed Auth**: Handles complex OAuth flows and token refreshes automatically.
- **Framework Agnostic**: Works with OpenAI, LangChain, CrewAI, Autogen, and more.
- **Observability**: Detailed logs of every tool call and its output.

## Limitations
- **External Dependency**: Relies on Composio's platform for managing connections (unless self-hosted).
- **Privacy**: Tool calls go through Composio's infrastructure.

## When to use it
- When you need to connect an agent to multiple SaaS tools quickly.
- To avoid building and maintaining your own OAuth integration logic.

## When not to use it
- For simple agents that don't need external tool access.
- If you have strict privacy requirements that forbid third-party tool routers.

## Getting started
### Installation
```bash
pip install composio-core
# Or for specific frameworks
pip install composio-openai
```

### Working Example
```python
from composio import Composio, App
from openai import OpenAI

client = OpenAI()
composio = Composio()

# Initialize session for a user
session = composio.create(user_id="user_1")

# Get tools for GitHub
tools = session.tools(apps=[App.GITHUB])

# Use in OpenAI
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Create a GitHub issue in my test repo"}],
    tools=tools
)

# Handle tool calls
result = session.handle_tool_calls(response)
print(result)
```

## Licensing and cost
- **Open Source**: The SDK is open source.
- **Cost**: Freemium (Free tier available, paid for higher usage/enterprise features).
- **Self-hostable**: Enterprise versions support self-hosting.

## Related tools / concepts
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [Zapier](../automation_orchestration/zapier.md)
- [Make](../automation_orchestration/make.md)

## Sources / References
- [Official Website](https://composio.dev/)
- [Documentation](https://docs.composio.dev/)
- [GitHub](https://github.com/composiohq/composio)

## Contribution Metadata
- Last reviewed: 2026-02-27
- Confidence: high
