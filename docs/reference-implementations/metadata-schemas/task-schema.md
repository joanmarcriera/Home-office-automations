# Task Schema

## What it is
The Task Schema is a standardized metadata specification used within the OpenClaw ecosystem to represent actionable "tasks" or "tickets" across different platforms (e.g., ServiceNow, Jira, GitHub Issues, Vikunja). In 2026, this has evolved into the **Autonomous Task Object (ATO)**, which serves as a portable, platform-agnostic container for task state, priority, and cross-platform history, enabling agents to coordinate complex workflows across disparate systems.

## What problem it solves
It eliminates the need for AI agents to understand the specific nuances of every ticketing system's API. By mapping platform-specific data (like ServiceNow's `incident` table or Jira's `issue` objects) to a unified Task Schema, agents can:
- **Normalize Intent**: Apply the same reasoning patterns regardless of the backend.
- **Cross-Platform Orchestration**: Move a task from a Slack conversation to a Jira ticket and then to a GitHub PR seamlessly.
- **State Synchronization**: Maintain a "single source of truth" for task status in multi-system environments.
- **Agentic Handoff**: Enable one agent to "hand off" a task object to another agent with all necessary context preserved.

## Where it fits in the stack
**Reference Implementations / Metadata Schemas**. It serves as a foundational data contract between [Automation & Orchestration Tools](../../tools/automation_orchestration/index.md) and agentic workflows, often delivered via the Model Context Protocol (MCP 3.0).

## Typical use cases
- **Multi-Platform Triage**: An agent reads tasks from [ServiceNow](../../tools/automation_orchestration/servicenow-mcp.md) and [Jira](../../tools/automation_orchestration/atlassian-jira-mcp.md), triaging them into a single priority queue.
- **Autonomous Project Management**: An agent uses the [Vikunja MCP](../../tools/automation_orchestration/vikunja-mcp.md) to manage a developer's daily tasks based on high-level goals in a corporate tracker.
- **Incident Remediation**: Automatically creating and updating "Self-Healing" tasks in response to system alerts.
- **Consolidated Reporting**: Generating executive dashboards that aggregate metrics across GitHub, Jira, and internal tools.

## Strengths
- **Platform Agnostic**: Decouples agent reasoning from specific vendor APIs.
- **Interoperability**: Allows different MCP servers to produce data that any MCP client (Claude 4.8, GPT-5.5) can consume consistently.
- **Simplified Tool-Calling**: Agents use a single `update_task` pattern instead of learning multiple platform-specific tools.
- **Durable Context**: ATOs carry their own history and metadata, making them resilient to system-level outages.

## Limitations
- **Abstraction Loss**: Some platform-specific features (e.g., Jira's "Story Points" vs GitHub's "Labels") might be collapsed into generic fields.
- **Mapping Overhead**: Requires ongoing maintenance of the mapping layer as platform APIs evolve.
- **Lowest Common Denominator**: A unified schema might miss highly specialized workflow features unique to a single tool.

## When to use it
- When building multi-platform agentic triage or automation tools.
- To provide a stable interface for AI agents that needs to survive backend system migrations.
- When standardizing reporting and analytics across multiple ticketing sources.
- For high-level agentic planning where specific platform details are secondary to task completion.

## When not to use it
- For simple integrations that only ever talk to a single platform and require its full specialized feature set.
- When the overhead of maintaining a mapping layer outweighs the benefits of platform independence.
- For extremely low-latency operations where the transformation step adds prohibited delay.

## Getting started
To implement the Task Schema in your workflow:
1. **Define your Mappings**: Map your source system (e.g., GitHub) fields to the ATO fields.
2. **Deploy an MCP Server**: Use or build an MCP server that implements the [Task Schema](task-schema.md).
3. **Configure your Agent**: Provide the agent with the `get_tasks` and `update_task` tool definitions.
4. **Implement a Transformer**: Create a middleware layer that converts platform-specific JSON to ATO format.

## CLI examples
Using the `mcp-cli` to list tasks from multiple sources in ATO format:

```bash
# List all 'critical' tasks from Jira and ServiceNow
mcp-cli call list_tasks --params '{"priority": "critical"}'
```

Output:
```json
[
  {
    "task_id": "JIRA-123",
    "source": "jira",
    "title": "Fix auth bug",
    "status": "open",
    "priority": "critical"
  },
  {
    "task_id": "INC009",
    "source": "servicenow",
    "title": "Server down",
    "status": "in_progress",
    "priority": "critical"
  }
]
```

## API examples
Example of a Python mapping function using Pydantic:

```python
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class TaskPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"

class TaskATO(BaseModel):
    task_id: str
    source: str
    title: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime

def map_jira_to_ato(jira_issue: dict) -> TaskATO:
    return TaskATO(
        task_id=jira_issue["key"],
        source="jira",
        title=jira_issue["fields"]["summary"],
        status=TaskStatus.OPEN if jira_issue["fields"]["status"]["name"] == "To Do" else TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH if jira_issue["fields"]["priority"]["name"] == "High" else TaskPriority.MEDIUM,
        created_at=datetime.fromisoformat(jira_issue["fields"]["created"])
    )
```

## Related tools / concepts
- [ServiceNow MCP Server](../../tools/automation_orchestration/servicenow-mcp.md) — Enterprise ticketing integration.
- [Atlassian Jira MCP](../../tools/automation_orchestration/atlassian-jira-mcp.md) — Standard agile task tracker integration.
- [Vikunja MCP](../../tools/automation_orchestration/vikunja-mcp.md) — Open-source personal/team task management.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — The delivery mechanism for ATOs.
- [Chronos MCP](../../tools/automation_orchestration/chronos-mcp.md) — For time-aware task scheduling.
- [Autonomous Task Object (ATO)](../patterns/autonomous-task-object.md) — The pattern behind the schema.
- [Unified Search API Reference](../../scripts/unified_search.py) — Cross-platform search implementation.
- [Task Schema Standard](task-schema.md) — The full JSON schema definition.

## Sources / References
- [JSON Schema Standard](https://json-schema.org/)
- [OpenClaw Architecture Index](../../ARCHITECTURE.md)
- [Model Control Protocol (MCP 3.0) Specification](https://modelcontrolprotocol.org)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
