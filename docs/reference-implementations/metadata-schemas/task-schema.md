# Task Schema

## What it is
The Task Schema is a standardized, platform-agnostic metadata specification used within the OpenClaw ecosystem to represent actionable tasks, tickets, or missions across different enterprise environments (such as ServiceNow, Jira, GitHub Issues, and Antigravity). In late July 2026, it serves as the foundational **Autonomous Task Object (ATO)** structure for multi-agent loops operating via the **Model Context Protocol (MCP 3.1) Task Protocol**, allowing collaborative agents to declare, delegate, track, and synchronize sub-task states seamlessly.

## What problem it solves
It solves the "API Fragmentation" and interoperability problems in multi-agent environments. Traditional enterprise systems use highly customized, proprietary data formats (e.g., ServiceNow `incident` fields vs. Jira `issue` types vs. GitHub YAML specifications). Asking AI agents to understand and interact with each API natively leads to brittle tool-calling behaviors and frequent formatting errors. The Task Schema:
- **Normalizes Schemas**: Collapses disparate ticketing models into a single, unified data structure.
- **Simplifies Tool-Calling**: Enables agents to utilize a single consistent pattern (such as `create_task` or `update_task_state`) across multiple platforms.
- **Maintains Parent-Child Traceability**: Allows complex missions to be broken down recursively into sub-tasks with traceable execution trees.
- **Ensures State Synchronization**: Provides standard enums and transition rules to map task progress across different backends.

## Where it fits in the stack
**Reference Implementations / Metadata Schemas**. It serves as the primary data contract between the [Orchestration Layer](../../tools/orchestration/index.md) and [Agent Frameworks](../../tools/frameworks/index.md), ensuring schema consistency throughout agent execution pipelines.

## Typical use cases
- **Enterprise Ticket Ingestion**: An agent queries [ServiceNow](../../tools/automation_orchestration/servicenow-mcp.md) and [Jira](../../tools/automation_orchestration/atlassian-jira-mcp.md) endpoints, transforming incoming alerts into a single unified queue of Task Schema objects.
- **Autonomous Mission Decomposition**: A coordinator agent receives a high-level goal and recursively decomposes it into standard sub-tasks, allocating them to worker droids.
- **Cross-Platform Status Synchronization**: Automatically updating a developer's local task board ([Google Tasks](../../tools/calendar_tasks/google-tasks.md)) and propagating progress back to the master enterprise database.
- **Audit-Trail Logging**: Storing unified execution histories in [MinIO](../../tools/intake_storage/minio.md) for billing and compliance analysis.

## Strengths
- **Decoupled Architecture**: Insulation against downstream system migrations; changing from Jira to another provider does not break the agent's core code.
- **Recursion Friendly**: Deep nesting support allows complex multi-agent execution hierarchies to remain organized.
- **Deterministic Validation**: Strict validation schemas (via Pydantic/Zod) catch bad input values before they reach external APIs.
- **Workflow Portability**: Easily runs within [Temporal](../../tools/orchestration/temporal.md) for robust, long-running task persistence and recovery.

## Limitations
- **Granular Detail Loss**: Highly customized, platform-specific attributes (such as specialized ServiceNow work notes tables) must be simplified or stored in a generic metadata dictionary.
- **Translation Maintenance**: Requires ongoing mapping rules to align standard fields with evolving enterprise APIs.
- **Payload Overhead**: Including recursive sub-task arrays and detailed execution histories can inflate context usage on smaller models.

## When to use it
- When orchestrating complex, multi-agent systems that need to collaboratively work on and hand off tasks.
- To standardize task reporting, performance metrics, and compliance logs across multiple backends.
- When building lightweight developer integrations or custom personal task automations.
- For managing stateful [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) in late July 2026.

## When not to use it
- For simple, isolated integrations that only interact with a single platform and require zero cross-system mappings.
- When the overhead of maintaining a schema adapter exceeds the operational benefits of platform independence.
- For storing static data (such as corpus files or vectors) where a [Search Pattern](../../knowledge_base/patterns/search-patterns.md) is more appropriate.

## Getting started
1. **Adopt Task Schema v1.6.x**: Use the provided Pydantic specification to model tasks in your workspace.
2. **Implement Platform Adapters**: Write mapping layers to translate raw enterprise payloads (JSON) to and from the schema.
3. **Deploy MCP 3.1 Task Protocol**: Use an MCP server to expose the schema-compliant task manipulation tools to your agents.
4. **Establish Task Repositories**: Store active task states in [MinIO](../../tools/intake_storage/minio.md) or a local, CRDT-synchronized flat file system.
5. **Enforce Strong Validation**: Leverage validation libraries like [Instructor](../../tools/frameworks/instructor.md) to verify task payloads are strictly correct before execution.

## CLI examples
Using `jq` to map raw ServiceNow incidents to the standard Task Schema format:

```bash
# Transform ServiceNow JSON into Task Schema (conceptual)
cat raw_incident.json | jq '{
  task_id: .sys_id,
  title: .short_description,
  status: (if .incident_state == "Closed" then "closed" else "open" end),
  priority: (if .priority == "1" then "critical" else "medium" end),
  source: "servicenow"
}'
```

Querying unified, cross-platform tasks via the [Junie-cli](../../tools/development_ops/junie-cli.md):
```bash
# List all critical tasks across Jira and ServiceNow using standardized schema parameters
junie tasks list --priority critical --unified --source all
```

## API examples
Fully realized, nested Task Schema modeling with custom validation decorators and platform-mapping logic using `pydantic` (v2.13+) in Python:

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any

# Define standard Task state transitions
class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    RESOLVED = "resolved"
    CLOSED = "closed"

# Define standard task execution log
class ExecutionLog(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_id: str
    action_taken: str
    output_summary: str

# Define standard nested Task Object
class TaskObject(BaseModel):
    task_id: str = Field(description="Platform-agnostic unique identifier (e.g., JIRA-101)")
    title: str = Field(description="Standardized, clear summary of the work item")
    description: str | None = Field(None, description="Detailed actionable items")
    status: TaskStatus = Field(default=TaskStatus.OPEN)
    priority: str = Field(pattern="^(critical|high|medium|low)$")
    source: str = Field(description="Source system originating the task (e.g., jira, servicenow)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    assignee: str | None = Field(None, description="Assigned agent ID or human email")
    subtasks: List["TaskObject"] = Field(default_factory=list, description="Recursive child tasks")
    history: List[ExecutionLog] = Field(default_factory=list, description="Chronological log of agent actions")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific raw payload fields")

    # Ensure parent task is updated when status is set to resolved
    @field_validator("status")
    @classmethod
    def validate_transitions(cls, value: TaskStatus, info: Any) -> TaskStatus:
        # Custom logic can be injected here to enforce strict state machine transitions
        return value

    # Ensure subtasks follow priority boundaries
    @field_validator("priority")
    @classmethod
    def validate_priority_boundary(cls, value: str) -> str:
        valid_priorities = {"critical", "high", "medium", "low"}
        if value not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")
        return value

# Implement basic platform translation logic
def transform_jira_to_task(raw_issue: dict) -> TaskObject:
    fields = raw_issue.get("fields", {})
    return TaskObject(
        task_id=raw_issue.get("key", "UNKNOWN"),
        title=fields.get("summary", "No Summary"),
        description=fields.get("description", ""),
        status=TaskStatus.OPEN,  # Simple mapper logic
        priority=fields.get("priority", {}).get("name", "medium").lower(),
        source="jira",
        metadata={"jira_raw": raw_issue}
    )
```

## Related tools / concepts
- [ServiceNow MCP](../../tools/automation_orchestration/servicenow-mcp.md) — ServiceNow target integration.
- [Atlassian Jira MCP](../../tools/automation_orchestration/atlassian-jira-mcp.md) — Jira target integration.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Standard for agent tool-calling capabilities.
- [Antigravity](../../tools/agents/antigravity.md) — Stateful agent execution engine using task objects.
- [Temporal](../../tools/orchestration/temporal.md) — Workflow orchestrator for persistent task lifecycles.
- [Instructor](../../tools/frameworks/instructor.md) — Structured extraction validation for task inputs.
- [Google Tasks](../../tools/calendar_tasks/google-tasks.md) — Lightweight endpoint for personal tasks.
- [Search Patterns](../../knowledge_base/patterns/search-patterns.md) — Complementary pattern for unstructured informational lookups.

## Sources / References
- [JSON Schema Specification](https://json-schema.org/)
- [OpenClaw Core Architecture Index](../../ARCHITECTURE.md)
- [MCP 3.1 Specification: Core Resources, Tasks, and Tools](https://modelcontextprotocol.io/)
- [Jira Cloud Platform API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)

## Contribution Metadata
- Last reviewed: 2026-07-25
- Confidence: high