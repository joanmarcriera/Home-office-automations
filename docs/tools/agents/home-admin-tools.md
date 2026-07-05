# Home Admin Agent Tools

## What it is
Home Admin Agent Tools are the local service adapters exposed to the Ralph home-admin agent for interacting with household infrastructure. They wrap the complex REST APIs of household services into simplified, agent-discoverable tools following the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) 3.0 Task Protocol. These tools enable frontier models like [Gemma 3](../ai_knowledge/local_llms.md), [Claude 4.8 Opus](../providers/anthropic.md), and [Llama 4 Maverick](../ai_knowledge/local_llms.md) to safely operate a household through standardized tool-calling interfaces.

## What problem it solves
They give the agent controlled, high-level interfaces for querying and changing household task and smart-home systems without requiring direct database access or unrestricted shell execution. This provides a critical layer of security, predictability, and auditability to autonomous home operations, ensuring that the agent's actions are restricted to a predefined safety schema.

## Where it fits in the stack
**Agents / Home administration tool layer**. It sits between the reasoning agent (Ralph) and the household's core services (e.g., Home Assistant, Vikunja), acting as a semantic translator that converts high-level agent intent into concrete, validated API actions.

## Typical use cases
- **Automated Morning Briefing**: Querying [Vikunja](../../services/vikunja.md) for today's tasks and [Home Assistant](../../services/home-assistant.md) for the current weather and house state.
- **Scene Management**: Triggering "Good Night" or "Away" scenes based on family schedules or detected occupancy intent.
- **Task Delegation**: Automatically creating maintenance tasks in [Vikunja](../../services/vikunja.md) when [Home Assistant](../../services/home-assistant.md) detects a sensor alert (e.g., "Fridge door left open for 10 minutes").
- **Visual Diagnostics**: Using [Gemma 3](../ai_knowledge/local_llms.md) to analyze camera feeds and trigger automation tools based on visual reasoning.

## Strengths
- **Standardized Protocol**: Leverages [MCP](../automation_orchestration/mcp.md) 3.0 for universal compatibility with modern agent harnesses.
- **Security**: Actions are strictly limited by the tool's defined JSON schema and API scopes.
- **FastMCP 3.0 Support**: Enables ultra-low latency tool execution for real-time home response.
- **High Discoverability**: Semantic argument definitions allow LLMs to reliably use tools without fine-tuning or extensive prompting.

## Limitations
- **Permission Scoping**: The tools operate with the permissions of the configured API tokens; broad tokens may grant the agent excessive access.
- **State Synchronicity**: Local network latency or service downtime can lead to "ghost" states where the agent believes an action succeeded when it did not.
- **No Native Rollback**: Most home state changes (e.g., toggling a switch) do not support ACID-style transactions or automatic rollbacks on workflow failure.

## When to use it
- When an autonomous agent needs to read from or write to the household's task and automation systems.
- When you want to provide a "Natural Language" interface for complex home operations.
- For integrating local household services into the [Anthropic Agent Skills](anthropic-agent-skills.md) ecosystem using [FastMCP 3.0](../automation_orchestration/mcp.md).

## When not to use it
- For services that lack configured credentials or clear ownership.
- When an action is extremely sensitive (e.g., unlocking a main door) and requires a human-in-the-loop (HITL) approval that is not yet implemented.
- For public-facing cloud services where direct API access is more efficient than agentic orchestration.

## Getting started

### Installation
The tools are typically deployed as part of a Python-based agent service or an MCP server.

```bash
# Clone the home-admin repository
git clone https://github.com/homelab/home-admin-tools
cd home-admin-tools

# Install dependencies for FastMCP 3.0
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

### Example: Tool Definition (MCP 3.0 Format)
This is an example of how the `vikunja_create_tool` would be defined in an [MCP](../automation_orchestration/mcp.md) server config following the Task Protocol.

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
Using a framework like [LangGraph](../frameworks/langgraph.md) or standard OpenAI tool calling with July 2026 patterns.

```python
import os
from mcp_client import FastMCPClient

# Initialize FastMCP 3.0 Client
client = FastMCPClient(server_url=os.environ['MCP_SERVER_URL'])

async def create_maintenance_task(title: str, project_id: int):
    # Execute tool via MCP Task Protocol
    result = await client.call_tool(
        "vikunja_create_tool",
        arguments={"title": title, "project_id": project_id}
    )
    return result

# Example invocation
# await create_maintenance_task("Fix leaking tap", 5)
```

## Related tools / concepts
- [Home Assistant](../../services/home-assistant.md)
- [Vikunja](../../services/vikunja.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [LangGraph](../frameworks/langgraph.md)
- [Claude 4.8 Opus](../providers/anthropic.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Cline](cline.md)
- [Agency Swarm](agency-swarm.md)
- [Anthropic Agent Skills](anthropic-agent-skills.md)

## Sources / References
- [Vikunja API Documentation](https://vikunja.io/docs/api/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
- [Model Context Protocol 3.0 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
