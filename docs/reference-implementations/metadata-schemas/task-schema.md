# Task Schema

## What it is
The Task Schema is a standardized metadata specification used within the OpenClaw ecosystem to represent actionable "tasks," "tickets," or "missions" across different platforms (e.g., ServiceNow, Jira, GitHub Issues, Antigravity). In June 2026, it serves as the foundational **Autonomous Task Object** for agents operating via the [Model Context Protocol (MCP 3.0)](../../tools/automation_orchestration/mcp.md).

## What problem it solves
It eliminates the need for AI agents to understand the specific nuances of every ticketing system's API. By mapping platform-specific data (like ServiceNow's `incident` table or Jira's `issue` objects) to a unified Task Schema, agents can apply the same reasoning and tool-calling patterns across the entire enterprise. This solves the "API Fragmentation" problem in multi-agent environments.

## Where it fits in the stack
**Reference Implementations / Metadata Schemas**. It serves as the primary data contract between [Orchestration Tools](../../tools/orchestration/index.md) and [Agent Frameworks](../../tools/frameworks/index.md).

## Typical use cases
- **Multi-Platform Triage**: An agent reads tasks from [ServiceNow](../../tools/automation_orchestration/servicenow-mcp.md) and [Jira](../../tools/automation_orchestration/atlassian-jira-mcp.md), triaging them into a single priority queue.
- **Automated Syncing**: Synchronizing status updates between a developer's local task list ([Google Tasks](../../tools/calendar_tasks/google-tasks.md)) and a corporate ticket system.
- **Reporting**: Generating aggregate metrics across multiple sources by querying unified schema objects in [MinIO](../../tools/intake_storage/minio.md).
- **Mission Decomposition**: Breaking down a complex [Antigravity](../../tools/agents/antigravity.md) mission into standardized sub-tasks.

## Strengths
- **Platform Agnostic**: Decouples agent logic from specific backend API schemas.
- **Interoperability**: Allows different MCP servers to produce data that any MCP client can consume consistently.
- **Simplified Tool-Calling**: Agents can use a single `update_task` tool pattern instead of learning platform-specific update methods.
- **Durable State**: Compatible with [Temporal](../../tools/orchestration/temporal.md) for long-running task persistence.

## Limitations
- **Abstraction Loss**: Some platform-specific features (e.g., ServiceNow's "Work Notes" vs Jira's "Comments") might be collapsed or simplified.
- **Mapping Complexity**: Requires ongoing maintenance of mapping logic as underlying platform APIs (ServiceNow, Jira, etc.) evolve.
- **Context Depth**: A unified schema might not capture the full workflow complexity of highly specialized systems like SAP or Salesforce without extensions.

## When to use it
- When building multi-platform agentic triage or automation tools.
- To provide a stable interface for AI agents that need to survive backend system migrations.
- When standardizing reporting and analytics across multiple ticketing sources.
- When implementing [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) using MCP 3.0.

## When not to use it
- For simple integrations that only ever talk to a single platform and require its full specialized feature set.
- When the overhead of maintaining a mapping layer outweighs the benefits of platform independence.
- For non-actionable data (e.g., logs, documents) where a [Search Pattern](../../knowledge_base/patterns/search-patterns.md) is more appropriate.

## Getting started
1. **Define the Mapping**: Create a transformer that converts source data (JSON) into the Task Schema format.
2. **Implement an MCP Server**: Use the [Model Context Protocol](../../tools/automation_orchestration/mcp.md) to expose the Task Schema to agents.
3. **Set Up a Storage Layer**: Use [MinIO](../../tools/intake_storage/minio.md) or a local JSON-LD store to persist unified tasks.
4. **Configure Your Agent**: Instruct the agent (e.g., Claude 4.8) to use the `task_schema` for all ticket-related operations.
5. **Add Validation**: Use [Instructor](../../tools/frameworks/instructor.md) or [Pydantic](../../tools/frameworks/instructor.md) to ensure all tasks conform to the schema.

## CLI examples
Using `jq` to transform a ServiceNow incident into a Task Schema object:

```bash
# Map ServiceNow JSON to Task Schema (conceptual)
cat incident.json | jq '{
  task_id: .number,
  title: .short_description,
  status: (if .state == "7" then "closed" else "open" end),
  source: "servicenow"
}'
```

Querying unified tasks via an MCP-compatible CLI (e.g., [Junie-cli](../../tools/development_ops/junie-cli.md)):
```bash
# List all critical tasks across all platforms
junie tasks list --priority critical --unified
```

## API examples
Schema definition (v1.5.0) using Pydantic for an [Instructor](../../tools/frameworks/instructor.md) workflow:

```python
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Task(BaseModel):
    task_id: str = Field(description="Unique ID from source system")
    title: str
    status: TaskStatus
    priority: str = Field(pattern="^(critical|high|medium|low)$")
    source: str = Field(description="Origin platform (jira, servicenow, etc.)")
    created_at: datetime = Field(default_factory=datetime.now)
    assignee: str | None = None
```

## Related tools / concepts
- [ServiceNow MCP](../../tools/automation_orchestration/servicenow-mcp.md) — Source for task data.
- [Atlassian Jira MCP](../../tools/automation_orchestration/atlassian-jira-mcp.md) — Source for task data.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Protocol for task exchange.
- [Antigravity](../../tools/agents/antigravity.md) — Agent framework using unified tasks.
- [Temporal](../../tools/orchestration/temporal.md) — Durable execution for tasks.
- [Instructor](../../tools/frameworks/instructor.md) — Validation for task objects.
- [Google Tasks](../../tools/calendar_tasks/google-tasks.md) — Lightweight task target.
- [Search Patterns](../../knowledge_base/patterns/search-patterns.md) — Complementary pattern for non-actionable data.

## Sources / References
- [JSON Schema Standard](https://json-schema.org/)
- [OpenClaw Architecture Index](../../ARCHITECTURE.md)
- [MCP 3.0 Specification: Resources and Tools](https://modelcontextprotocol.io/)
- [ServiceNow API Documentation](https://developer.servicenow.com/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
