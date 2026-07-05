# Home Admin Agent Tools

This page documents the specialized tools available to the Home Admin Agent (Ralph) for interacting with home services.

## What it is
Home Admin Agent Tools are the local service adapters exposed to the Ralph home-admin agent. They wrap the complex REST APIs of household services into simplified, agent-discoverable tools following the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) or standard tool-calling patterns. These tools enable frontier models like [Claude 4.8 Opus](../providers/anthropic.md), [Gemma 3](../ai_knowledge/local_llms.md), and [Llama 4 Maverick](../ai_knowledge/local_llms.md) to safely operate a household.

## What problem it solves
They give the agent controlled, high-level interfaces for querying and changing household task and smart-home systems. This prevents the agent from needing direct database access or unrestricted shell execution, providing a layer of security and predictability to autonomous home operations.

## Where it fits in the stack
**Agents / Home administration tool layer**. It sits between the reasoning agent (Ralph) and the household's core services, acting as a translator for intent-to-action.

## Typical use cases
- **Automated Morning Briefing**: Querying Vikunja for today's tasks and Home Assistant for the current weather/house state.
- **Scene Management**: Triggering "Good Night" or "Away" scenes based on family schedule or manual intent.
- **Task Delegation**: Automatically creating maintenance tasks in Vikunja when Home Assistant detects a sensor alert (e.g., "Fridge door left open").
- **Autonomous Resource Optimization**: Scaling home services based on predicted usage patterns using [Gemma 3](../ai_knowledge/local_llms.md).

## Strengths
- **Security**: Actions are limited by the tool's defined schema and API scopes.
- **Discoverability**: Standard argument definitions allow LLMs to reliably use the tools without retraining.
- **Portability**: The tools follow patterns that can be easily ported to other agent frameworks (e.g., LangGraph or MCP).
- **Interoperability**: Optimized for MCP 3.0 and the **MCP 3.0 Task Protocol**, allowing seamless integration with [Claude Desktop](../ai_knowledge/claude.md) and [Cline](cline.md).
- **Performance**: Support for **FastMCP 3.0** ensures ultra-low latency execution for real-time home automation.

## Limitations
- **Permission Scoping**: The tools operate with the permissions of the configured API tokens. If a token has broad access, the agent inherits that access.
- **Lack of Transactional Rollback**: Home state changes (e.g., turning on a light) or task creations in Vikunja cannot always be automatically rolled back if a multi-step workflow fails.
- **Dependency on Local Network**: These tools require stable connectivity to the local instances of [Home Assistant](../../services/home-assistant.md) and [Vikunja](../../services/vikunja.md).

## When to use it
- When an autonomous agent needs to read from or write to the household's task and automation systems.
- When you want to provide a "Natural Language" interface for complex home operations.
- For integrating local household services into the [Anthropic Agent Skills](anthropic-agent-skills.md) ecosystem.
- When leveraging **Gemma 3** for low-latency, local-first home orchestration.

## When not to use it
- For services that lack configured credentials or clear ownership.
- When an action is extremely sensitive and requires a human-in-the-loop (HITL) approval that is not yet implemented.
- For public-facing services where direct API access is more efficient than agentic orchestration.

## Getting started

### Installation
The tools are typically deployed as part of a Python-based agent service or an MCP server.

```bash
# Clone the home-admin repository
git clone https://github.com/homelab/home-admin-tools
cd home-admin-tools

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Set the required environment variables in your `.env` file:
- `VIKUNJA_API_TOKEN`: Your Vikunja personal access token.
- `HOME_ASSISTANT_TOKEN`: Long-lived access token from your HA profile.

## CLI examples

### Testing Vikunja Connection
Verify that the tools can communicate with the local Vikunja instance.

```bash
python3 scripts/test_home_admin_tools.py --service vikunja --action ping
```

### Manual Tool Execution
Manually trigger a tool call to verify configuration.

```bash
python3 scripts/home_assistant_tool.py --action toggle_light --entity_id light.kitchen
```

## API examples

### Example: Tool Definition (MCP Format)
This is an example of how the `vikunja_create_tool` would be defined in an [MCP](../automation_orchestration/mcp.md) server config.

```json
{
  "name": "vikunja_create_tool",
  "description": "Creates a new task in a specified project.",
  "input_schema": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "description": "Task title" },
      "project_id": { "type": "integer", "description": "ID of the target project" },
      "description": { "type": "string", "description": "Task description" }
    },
    "required": ["title", "project_id"]
  }
}
```

### Example: Agent Tool Calling (Python)
Using a framework like [LangGraph](../frameworks/langgraph.md) or standard OpenAI tool calling.

```python
import requests
import os

def vikunja_create_tool(title: str, project_id: int, description: str = ""):
    url = f"{os.environ['VIKUNJA_API_URL']}/projects/{project_id}/tasks"
    headers = {"Authorization": f"Bearer {os.environ['VIKUNJA_API_TOKEN']}"}
    data = {"title": title, "description": description}

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Example invocation by an agent
new_task = vikunja_create_tool(
    title="Buy milk",
    project_id=1,
    description="Needed for breakfast tomorrow"
)
print(f"Created task: {new_task['id']}")
```

## Related tools / concepts
- [Home Assistant](../../services/home-assistant.md)
- [Vikunja](../../services/vikunja.md)
- [n8n](../../services/n8n.md)
- [LangGraph](../frameworks/langgraph.md)
- [MCP](../automation_orchestration/mcp.md)
- [Agency Swarm](agency-swarm.md)
- [Anthropic Agent Skills](anthropic-agent-skills.md)
- [Claude 4.8 Opus](../providers/anthropic.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)
- [Cline](cline.md)

## Sources / References
- [Vikunja API Documentation](https://vikunja.io/docs/api/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-07-05
- Confidence: high
