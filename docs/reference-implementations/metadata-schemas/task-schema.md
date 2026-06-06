# Task Schema

## What it is
The Task Schema is a standardized metadata specification used within the OpenClaw ecosystem to represent actionable "tasks" or "tickets" across different platforms (e.g., ServiceNow, Jira, GitHub Issues). It provides a common language for AI agents to understand task state, priority, and assignment regardless of the underlying backend.

## What problem it solves
It eliminates the need for AI agents to understand the specific nuances of every ticketing system's API. By mapping platform-specific data (like ServiceNow's `incident` table or Jira's `issue` objects) to a unified Task Schema, agents can apply the same reasoning and tool-calling patterns across the entire enterprise.

## Where it fits in the stack
**Reference Implementations / Metadata Schemas**. It serves as a foundational data contract between [Automation & Orchestration Tools](../../tools/automation_orchestration/index.md) and agentic workflows.

## Schema Definition (v1.0.0)

The schema is defined using JSON Schema and covers core task attributes:

| Field | Type | Description |
| :--- | :--- | :--- |
| `task_id` | String | Unique identifier from the source system (e.g., `INC0012345`). |
| `title` | String | Short summary of the task. |
| `description`| String | Detailed explanation or body of the task. |
| `status` | Enum | Unified state: `open`, `in_progress`, `blocked`, `resolved`, `closed`. |
| `priority` | Enum | Unified priority: `critical`, `high`, `medium`, `low`. |
| `assignee` | Object | Standardized user object (email, name, platform_id). |
| `source` | String | Originating platform (e.g., `servicenow`, `jira`). |
| `created_at` | DateTime | ISO 8601 timestamp. |

## Typical use cases
- **Multi-Platform Triage**: An agent reads tasks from ServiceNow and Jira, triaging them into a single priority queue using the Task Schema.
- **Automated Syncing**: Synchronizing status updates between a developer's local task list and a corporate ticket system.
- **Reporting**: Generating aggregate metrics across multiple sources by querying unified schema objects.

## Strengths
- **Platform Agnostic**: Decouples agent logic from specific API schemas.
- **Interoperability**: Allows different MCP servers to produce data that any MCP client can consume consistently.
- **Simplified Tool-Calling**: Agents can use a single `update_task` tool pattern instead of learning `update_incident`, `update_issue`, etc.

## Limitations
- **Abstraction Loss**: Some platform-specific features (like ServiceNow's "Work Notes" vs Jira's "Comments") might be collapsed or lost in a generic schema.
- **Mapping Complexity**: Requires ongoing maintenance of mapping logic as underlying platform APIs evolve.
- **Context Depth**: A unified schema might not capture the full workflow complexity of highly specialized ticketing systems.

## When to use it
- When building multi-platform agentic triage or automation tools.
- To provide a stable interface for AI agents that needs to survive backend system migrations.
- When standardizing reporting and analytics across multiple ticketing sources.

## When not to use it
- For simple integrations that only ever talk to a single platform and require its full specialized feature set.
- When the overhead of maintaining a mapping layer outweighs the benefits of platform independence.

## Implementation Examples

### Mapping ServiceNow to Task Schema
In an MCP server implementation, a ServiceNow incident would be mapped as follows:

```json
{
  "task_id": "INC0992831",
  "title": "Database connection timeout in production",
  "status": "in_progress",
  "priority": "critical",
  "source": "servicenow",
  "assignee": {
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
  }
}
```

### Mapping Jira to Task Schema
Similarly, a Jira issue would follow the same structure:

```json
{
  "task_id": "PROJ-123",
  "title": "Implement new auth provider",
  "status": "open",
  "priority": "high",
  "source": "jira",
  "assignee": null
}
```

## Related tools / concepts
- [ServiceNow MCP Server](../../tools/automation_orchestration/servicenow-mcp.md)
- [Atlassian Jira MCP](../../tools/automation_orchestration/atlassian-jira-mcp.md)
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md)
- [Unified Search API Reference](unified-search-api.py)

## Sources / references
- [JSON Schema Standard](https://json-schema.org/)
- [OpenClaw Architecture Index](../../ARCHITECTURE.md)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
