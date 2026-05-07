# Home Admin Agent Tools

This page documents the specialized tools available to the Home Admin Agent (Ralph) for interacting with home services.

## What it is
Home Admin Agent Tools are the local service adapters exposed to the Ralph home-admin agent. <!-- needs-content -->

## What problem it solves
They give the agent controlled interfaces for querying and changing household task and smart-home systems. <!-- needs-content -->

## Where it fits in the stack
**Agents / Home administration tool layer**. <!-- needs-content -->

## Typical use cases
Use these tools for task creation, task updates, home-state checks, and scene control. <!-- needs-content -->

## Strengths
The tools keep home-admin actions behind explicit API wrappers instead of unrestricted shell or browser access. <!-- needs-content -->

## Limitations
The page still needs fuller operational notes on permissions, failure handling, and audit logging. <!-- needs-content -->

## When to use it
Use these tools when Ralph needs to interact with Vikunja or Home Assistant through defined service APIs. <!-- needs-content -->

## When not to use it
Do not use these tools for services that lack configured credentials, clear ownership, or rollback expectations. <!-- needs-content -->

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

- [Agency Swarm](agency-swarm.md)
- [Agency-Agents](agency-agents.md)
- [Agentic Automation Canvas (AAC)](agentic-automation-canvas.md)
- [Agno](agno.md)
- [Anthropic Agent Skills](anthropic-agent-skills.md)

## Sources / References

- [Vikunja API Documentation](https://vikunja.io/docs/api/)
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)

## Contribution Metadata

- Last reviewed: 2026-04-16
- Confidence: high
