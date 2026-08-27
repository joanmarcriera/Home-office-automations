# Home Admin Agent Tools

## What it is
Home Admin Agent Tools are the local service adapters exposed to the Ralph home-admin agent for interacting with household infrastructure. They wrap the complex REST APIs of household services into simplified, agent-discoverable tools following the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) / FastMCP 3.1 specification. These tools enable frontier models like [Gemma 4](../ai_knowledge/local_llms.md), [Claude 5.6](../providers/anthropic.md), GPT-5.6, and [Llama 4](../ai_knowledge/local_llms.md) to safely operate a household through standardized, strongly-typed tool-calling interfaces.

## What problem it solves
They give the agent controlled, high-level interfaces for querying and changing household task and smart-home systems without requiring direct database access or unrestricted shell execution. This provides a critical layer of security, predictability, and auditability to autonomous home operations, ensuring that the agent's actions are restricted to a predefined safety schema.

## Where it fits in the stack
**Agents / Home administration tool layer**. It sits between the reasoning agent (Ralph) and the household's core services (e.g., Home Assistant, Vikunja), acting as a semantic translator that converts high-level agent intent into concrete, validated API actions.

## Typical use cases
- **Automated Morning Briefing**: Querying [Vikunja](../../services/vikunja.md) for today's tasks and [Home Assistant](../../services/home-assistant.md) for the current weather and house state.
- **Scene Management**: Triggering "Good Night" or "Away" scenes based on family schedules or detected occupancy intent.
- **Task Delegation**: Automatically creating maintenance tasks in [Vikunja](../../services/vikunja.md) when [Home Assistant](../../services/home-assistant.md) detects a sensor alert (e.g., "Fridge door left open for 10 minutes").
- **Visual Diagnostics**: Using [Gemma 4](../ai_knowledge/local_llms.md) to analyze camera feeds and trigger automation tools based on visual reasoning.

## Strengths
- **Standardized Protocol**: Leverages FastMCP 3.1 for universal compatibility with modern agent harnesses.
- **Security**: Actions are strictly limited by the tool's defined JSON schema and API scopes.
- **FastMCP 3.1 Support**: Enables ultra-low latency tool execution for real-time home response.
- **High Discoverability**: Semantic argument definitions allow LLMs to reliably use tools without fine-tuning or extensive prompting.

## Limitations
- **Permission Scoping**: The tools operate with the permissions of the configured API tokens; broad tokens may grant the agent excessive access.
- **State Synchronicity**: Local network latency or service downtime can lead to "ghost" states where the agent believes an action succeeded when it did not.
- **No Native Rollback**: Most home state changes (e.g., toggling a switch) do not support ACID-style transactions or automatic rollbacks on workflow failure.

## When to use it
- When an autonomous agent needs to read from or write to the household's task and automation systems.
- When you want to provide a "Natural Language" interface for complex home operations.
- For integrating local household services into the [Anthropic Agent Skills](claude-skills-ecosystem.md) ecosystem using FastMCP 3.1.

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

# Install dependencies for FastMCP 3.1
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

### Example: Tool Definition (FastMCP 3.1 Format)
This is an example of how the `vikunja_create_tool` would be defined in a FastMCP 3.1 server config following the Task Protocol.

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

### Example: Programmatic Python Tool and Payload Validation (Pydantic v2)
The following script demonstrates how to define, parse, and validate tool payloads for home automation and smart-home operations using Pydantic v2. This ensures type safety and semantic integrity before executing local service API calls.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

# Define Pydantic v2 schemas for validating home automation actions
class VikunjaTaskPayload(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Task title")
    project_id: int = Field(..., gt=0, description="Target project ID")
    description: Optional[str] = Field(None, description="Detailed task notes")
    priority: int = Field(default=3, ge=1, le=5, description="Priority level from 1 (highest) to 5 (lowest)")

    @field_validator('title')
    @classmethod
    def clean_title(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Task title cannot be empty or pure whitespace.")
        return stripped

class HomeAssistantActionPayload(BaseModel):
    entity_id: str = Field(..., pattern=r"^[a-z_]+\.[a-z0-9_]+$", description="Entity domain and ID (e.g., light.kitchen)")
    action: str = Field(..., description="Action to call (e.g., turn_on, turn_off, toggle)")
    brightness_pct: Optional[int] = Field(None, ge=0, le=100, description="Optional brightness level percentage")

def execute_home_action(raw_data: dict) -> None:
    try:
        # Validate the raw input payload against the Pydantic v2 model
        validated_payload = HomeAssistantActionPayload.model_validate(raw_data)
        print(f"Payload validated successfully for entity: {validated_payload.entity_id}")
        print(f"Executing action '{validated_payload.action}' with parameters: {validated_payload.model_dump_json(exclude_none=True)}")
        # In a real implementation, this would trigger the Home Assistant REST or WebSocket API
    except Exception as e:
        print(f"Validation failed for Home Assistant action payload: {e}", file=sys.stderr)

if __name__ == "__main__":
    print("Initializing Home Admin tool payload validation (Pydantic v2 / FastMCP 3.1 context)...")

    # Test valid payload
    valid_input = {
        "entity_id": "light.living_room",
        "action": "turn_on",
        "brightness_pct": 75
    }
    execute_home_action(valid_input)

    # Test invalid payload (should gracefully capture validation error)
    invalid_input = {
        "entity_id": "invalid-entity-id",
        "action": "turn_on"
    }
    execute_home_action(invalid_input)
```

## Related tools / concepts
- [Home Assistant](../../services/home-assistant.md)
- [Vikunja](../../services/vikunja.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [LangGraph](../frameworks/langgraph.md)
- [Claude 5.6](../providers/anthropic.md)
- [Gemma 4](../ai_knowledge/local_llms.md)
- [Cline](cline.md)
- [Agency Swarm](agency-swarm.md)
- [Anthropic Agent Skills](claude-skills-ecosystem.md)

## Sources / References
- [Vikunja API Documentation](https://vikunja.io/docs/api/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
- [Model Context Protocol 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
