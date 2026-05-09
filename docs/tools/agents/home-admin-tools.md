# Home Admin Agent Tools

This page documents the specialized tools available to the Home Admin Agent (Ralph) for interacting with home services.

## What it is
Home Admin Agent Tools are the local service adapters exposed to the Ralph home-admin agent. They wrap the complex REST APIs of household services into simplified, agent-discoverable tools following the [MCP](../../tools/automation_orchestration/mcp.md) or standard tool-calling patterns.

## What problem it solves
They give the agent controlled, high-level interfaces for querying and changing household task and smart-home systems. This prevents the agent from needing direct database access or unrestricted shell execution, providing a layer of security and predictability to autonomous home operations.

## Where it fits in the stack
**Agents / Home administration tool layer**. It sits between the reasoning agent (Ralph) and the household's core services, acting as a translator for intent-to-action.

## Typical use cases
- **Automated Morning Briefing**: Querying Vikunja for today's tasks and Home Assistant for the current weather/house state.
- **Scene Management**: Triggering "Good Night" or "Away" scenes based on family schedule or manual intent.
- **Task Delegation**: Automatically creating maintenance tasks in Vikunja when Home Assistant detects a sensor alert (e.g., "Fridge door left open").

## Strengths
- **Security**: Actions are limited by the tool's defined schema and API scopes.
- **Discoverability**: Standard argument definitions allow LLMs to reliably use the tools without retraining.
- **Portability**: The tools follow patterns that can be easily ported to other agent frameworks (e.g., LangGraph or MCP).

## Limitations
- **Permission Scoping**: The tools operate with the permissions of the configured API tokens. If a token has broad access, the agent inherits that access.
- **Lack of Transactional Rollback**: Home state changes (e.g., turning on a light) or task creations in Vikunja cannot always be automatically rolled back if a multi-step workflow fails.
- **Dependency on Local Network**: These tools require stable connectivity to the local instances of Home Assistant and Vikunja.

## When to use it
- When an autonomous agent needs to read from or write to the household's task and automation systems.
- When you want to provide a "Natural Language" interface for complex home operations.

## When not to use it
- For services that lack configured credentials or clear ownership.
- When an action is extremely sensitive and requires a human-in-the-loop (HITL) approval that is not yet implemented.

## Vikunja Tools

These tools allow the agent to manage tasks and projects in [Vikunja](../../services/vikunja.md).

### `vikunja_query_tool`
- **Description**: Queries tasks from Vikunja.
- **Arguments**:
    - `project_id` (optional): Filter by project ID.
    - `filter_query` (optional): Custom filter string.
    - `search` (optional): Search term for task titles.

### `vikunja_create_tool`
- **Description**: Creates a new task in a specified project.
- **Arguments**:
    - `title`: Task title.
    - `project_id`: ID of the target project.
    - `description` (optional): Task description.
    - `due_date` (optional): ISO 8601 due date.
    - `priority` (optional): Priority (1-5).

### `vikunja_update_tool`
- **Description**: Updates an existing task.
- **Arguments**:
    - `task_id`: ID of the task to update.
    - `title` (optional): New title.
    - `description` (optional): New description.
    - `due_date` (optional): New due date.
    - `done` (optional): Completion status.
    - `priority` (optional): New priority.

### `vikunja_relation_tool`
- **Description**: Links two tasks together.
- **Arguments**:
    - `task_id`: Source task ID.
    - `other_task_id`: Target task ID.
    - `relation_type`: Type of relation (e.g., `subtask`, `blocking`).

## Home Assistant Tools

These tools allow the agent to monitor and control smart home devices via [Home Assistant](../../services/home-assistant.md).

### `ha_state_query_tool`
- **Description**: Gets the current state of any entity.
- **Arguments**:
    - `entity_id`: The ID of the entity (e.g., `sensor.temperature`).

### `ha_scene_trigger_tool`
- **Description**: Triggers a predefined scene.
- **Arguments**:
    - `scene_id`: The ID of the scene (e.g., `scene.good_morning`).

### `ha_light_control_tool`
- **Description**: Turns lights on/off or adjusts brightness.
- **Arguments**:
    - `entity_id`: The ID of the light.
    - `action`: `turn_on` or `turn_off`.
    - `brightness` (optional): 0-255.

## Configuration

These tools require the following environment variables to be set:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `VIKUNJA_API_URL` | Base URL for Vikunja API | `http://localhost:3456/api/v1` |
| `VIKUNJA_API_TOKEN` | API token for Vikunja | (Required) |
| `HOME_ASSISTANT_URL` | Base URL for HA API | `http://localhost:8123/api` |
| `HOME_ASSISTANT_TOKEN` | Long-lived access token for HA | (Required) |

## Related tools / concepts
- [Home Assistant](../../services/home-assistant.md)
- [Vikunja](../../services/vikunja.md)
- [n8n](../../services/n8n.md)
- [LangGraph](../frameworks/langgraph.md)
- [MCP](../automation_orchestration/mcp.md)
- [Agency Swarm](agency-swarm.md)
- [Anthropic Agent Skills](anthropic-agent-skills.md)

## Sources / References

- [Vikunja API Documentation](https://vikunja.io/docs/api/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)

## Contribution Metadata

- Last reviewed: 2026-04-16
- Confidence: high
