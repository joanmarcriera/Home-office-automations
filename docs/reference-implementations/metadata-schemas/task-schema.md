# Task Schema

## What it is
The Task Schema is a standardized, platform-agnostic metadata specification used within the OpenClaw ecosystem to represent actionable tasks, tickets, or missions across different environments (such as ServiceNow, Jira, GitHub Issues, and Antigravity). In early January 2027, it serves as the foundational **Autonomous Task Object (ATO)** structure for multi-agent loops operating via the **FastMCP 3.1 Task Protocol**, allowing collaborative agents (powered by Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL) to declare, delegate, track, and synchronize sub-task states seamlessly.

## What problem it solves
It solves the "API Fragmentation" and interoperability problems in multi-agent environments. Traditional enterprise systems use highly customized, proprietary data formats (e.g., ServiceNow `incident` fields vs. Jira `issue` types vs. GitHub YAML specifications). Asking AI agents to understand and interact with each API natively leads to brittle tool-calling behaviors and frequent formatting errors. The Task Schema:
- **Normalizes Schemas**: Collapses disparate ticketing models into a single, unified data structure.
- **Simplifies Tool-Calling**: Enables agents to utilize a single consistent pattern (such as `create_task` or `update_task_state`) across multiple platforms.
- **Maintains Parent-Child Traceability**: Allows complex missions to be broken down recursively into sub-tasks with traceable execution trees.
- **Ensures State Synchronization**: Provides standard enums and transition rules to map task progress across different backends.

## Where it fits in the stack
**Reference Implementations / Metadata Schemas**. It serves as the primary data contract between the [Orchestration Layer](../../tools/orchestration/index.md) and [Agent Frameworks](../../tools/frameworks/index.md), ensuring schema consistency throughout agent execution pipelines.

```
+-----------------------------------------------------------------------------------+
|                        Agent Frameworks & LLM Loops                               |
|        (Claude 5.6, GPT-5.6, LangGraph, Antigravity Agent, FastMCP 3.1)           |
+-----------------------------------------------------------------------------------+
                                          |
                        [ Unified Autonomous Task Object (ATO) ]
                                          v
+-----------------------------------------------------------------------------------+
|                        Task Schema Engine & Adapter Layer                         |
|   +-----------------------+   +------------------------+   +-------------------+  |
|   | Pydantic v2 Schema    |   | State Transition Guard |   | Recursive Subtask |  |
|   | Validation            |   | Machine Engine         |   | Dependency Tree   |  |
|   +-----------------------+   +------------------------+   +-------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                  [ Platform Adapters: ServiceNow / Jira / GitHub ]
                                          v
+-----------------------------------------------------------------------------------+
|                        Enterprise Task Backends & APIs                            |
|             (Atlassian Jira, ServiceNow ITIL, GitHub Issues, Temporal)            |
+-----------------------------------------------------------------------------------+
```

## Architectural Overview & State Transition Machine

The Task Schema enforces a deterministic, state-machine-driven lifecycle to govern how agents transition tasks across platforms:

```
                  +-----------------------------------+
                  |             PENDING               |
                  +-----------------------------------+
                                    |
                           [ assign_agent ]
                                    v
                  +-----------------------------------+
        +-------->|           IN_PROGRESS             |<---------+
        |         +-----------------------------------+          |
        |                           |                            |
  [ unblock ]                 [ mark_blocked ]             [ retry ]
        |                           v                            |
  +-----------+   [ resolve ] +-------------------+   [ fail ] +-----------+
  |  RESOLVED | <------------ |      BLOCKED      | ---------> |  FAILED   |
  +-----------+               +-------------------+            +-----------+
        |
    [ verify ]
        v
  +-----------+
  |  CLOSED   |
  +-----------+
```

1. **PENDING**: Initial state upon ingestion or recursive decomposition. Unassigned or waiting for prerequisites.
2. **IN_PROGRESS**: Agent or human worker actively executing the task payload.
3. **BLOCKED**: Waiting on external API dependency, human-in-the-loop approval, or child subtask completion.
4. **RESOLVED**: Task execution completed successfully; awaiting automated validation or SRE audit.
5. **FAILED**: Terminal or retryable error condition recorded in the execution log history.
6. **CLOSED**: Finalized and archived state, synced back to primary enterprise databases.

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

## Comparison Matrix: Task Serialization & Modeling Standards

| Metric / Feature | Task Schema (ATO) | Raw JSON Schema | Protocol Buffers (v3) | OpenAPI 3.1 Spec |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Domain** | Agentic Workflows & Multi-Agent Loops | General Data Validation | High-performance RPC | REST API Specifications |
| **Pydantic v2 Native** | Yes (Built-in runtime models) | Requires code generator | Requires `protobuf` compiler | Requires generator |
| **State Machine Enforcement** | Strict Enums & Transition Guards | Manual validation | Enums only | Structural schemas |
| **Recursive Subtasks** | Native (`subtasks: List[TaskObject]`) | Complex `$ref` structures | Supported via `repeated` | Supported via `$ref` |
| **Execution Audit Trail** | Embedded (`history: List[ExecutionLog]`) | Custom array | Custom message | Custom array |
| **FastMCP 3.1 Compatibility** | Native Task Protocol Adapter | Manual Tool Specs | gRPC bridge required | REST Tool Bridge |

## When to use it
- When orchestrating complex, multi-agent systems that need to collaboratively work on and hand off tasks.
- To standardize task reporting, performance metrics, and compliance logs across multiple backends.
- When building lightweight developer integrations or custom personal task automations.
- For managing stateful [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) in early January 2027.

## When not to use it
- For simple, isolated integrations that only interact with a single platform and require zero cross-system mappings.
- When the overhead of maintaining a schema adapter exceeds the operational benefits of platform independence.
- For storing static data (such as corpus files or vectors) where a [Search Pattern](../../knowledge_base/patterns/search-patterns.md) is more appropriate.

## Getting started
1. **Adopt Task Schema v1.8.x**: Use the provided Pydantic specification to model tasks in your workspace.
2. **Implement Platform Adapters**: Write mapping layers to translate raw enterprise payloads (JSON) to and from the schema.
3. **Deploy FastMCP 3.1 Task Protocol**: Use a FastMCP server to expose the schema-compliant task manipulation tools to your agents.
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

### Production FastMCP 3.1 Task Server Implementation

The following Python script implements a production FastMCP 3.1 task orchestration server (`mcp_task_schema_engine.py`) exposing standardized task creation, state manipulation, and subtask decomposition tools.

```python
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime, timezone
from enum import Enum
import json
import logging

mcp = FastMCP("TaskSchemaEngine")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_task_schema")

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    RESOLVED = "resolved"
    FAILED = "failed"
    CLOSED = "closed"

class PriorityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ExecutionLog(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_id: str = Field(..., description="Identifier of agent taking action")
    action_taken: str = Field(..., description="Action description")
    output_summary: str = Field(..., description="Output or status note")

class TaskObject(BaseModel):
    task_id: str = Field(..., description="Unique platform-agnostic ID e.g. JIRA-101")
    title: str = Field(..., description="Actionable title summary")
    description: Optional[str] = Field(None, description="Detailed actionable body")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    source: str = Field(..., description="Originating backend (jira, servicenow, github)")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    assignee: Optional[str] = Field(None, description="Assigned worker agent ID")
    subtasks: List["TaskObject"] = Field(default_factory=list)
    history: List[ExecutionLog] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

# In-memory Task Repository for FastMCP Server
TASK_STORE: Dict[str, TaskObject] = {}

@mcp.tool()
def create_autonomous_task(
    task_id: str,
    title: str,
    source: str,
    priority: str = "medium",
    description: Optional[str] = None
) -> str:
    """
    Creates and stores a schema-compliant Autonomous Task Object (ATO).
    """
    try:
        task = TaskObject(
            task_id=task_id,
            title=title,
            source=source,
            priority=PriorityLevel(priority.lower()),
            description=description
        )
        TASK_STORE[task_id] = task
        logger.info(f"Task created successfully: {task_id}")
        return json.dumps({"status": "success", "task": task.model_dump(mode="json")}, indent=2)
    except (ValidationError, ValueError) as e:
        return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
def update_task_state(task_id: str, new_status: str, agent_id: str, summary: str) -> str:
    """
    Updates the state of an existing task and appends an entry to its history.
    """
    if task_id not in TASK_STORE:
        return json.dumps({"status": "error", "message": f"Task {task_id} not found"})

    task = TASK_STORE[task_id]
    try:
        status_enum = TaskStatus(new_status.lower())
        task.status = status_enum
        task.updated_at = datetime.now(timezone.utc).isoformat()

        log_entry = ExecutionLog(
            agent_id=agent_id,
            action_taken=f"Transitioned status to {status_enum.value}",
            output_summary=summary
        )
        task.history.append(log_entry)
        return json.dumps({"status": "success", "task": task.model_dump(mode="json")}, indent=2)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid status '{new_status}'"})

if __name__ == "__main__":
    mcp.run()
```

## API & Pydantic v2 Validation Schemas

Fully realized, nested Task Schema modeling with custom validation decorators and platform-mapping logic using `pydantic` (v2.13+) in Python:

```python
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Dict, Any, Optional

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    RESOLVED = "resolved"
    FAILED = "failed"
    CLOSED = "closed"

class ExecutionLog(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent_id: str
    action_taken: str
    output_summary: str

class TaskObject(BaseModel):
    task_id: str = Field(description="Platform-agnostic unique identifier (e.g., JIRA-101)")
    title: str = Field(description="Standardized, clear summary of the work item")
    description: Optional[str] = Field(None, description="Detailed actionable items")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: str = Field(default="medium", pattern="^(critical|high|medium|low)$")
    source: str = Field(description="Source system originating the task (e.g., jira, servicenow)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    assignee: Optional[str] = Field(None, description="Assigned agent ID or human email")
    subtasks: List["TaskObject"] = Field(default_factory=list, description="Recursive child tasks")
    history: List[ExecutionLog] = Field(default_factory=list, description="Chronological log of agent actions")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific raw payload fields")

    @field_validator("priority")
    @classmethod
    def validate_priority_boundary(cls, value: str) -> str:
        valid_priorities = {"critical", "high", "medium", "low"}
        if value.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")
        return value.lower()

def transform_jira_to_task(raw_issue: dict) -> TaskObject:
    """Transforms raw Jira issue JSON payloads into standard TaskObject schemas."""
    fields = raw_issue.get("fields", {})
    priority_name = fields.get("priority", {}).get("name", "medium").lower()
    if priority_name not in {"critical", "high", "medium", "low"}:
        priority_name = "medium"

    return TaskObject(
        task_id=raw_issue.get("key", "UNKNOWN"),
        title=fields.get("summary", "No Summary"),
        description=fields.get("description", ""),
        status=TaskStatus.PENDING,
        priority=priority_name,
        source="jira",
        metadata={"jira_raw": raw_issue}
    )

if __name__ == "__main__":
    sample_jira_payload = {
        "key": "OPS-402",
        "fields": {
            "summary": "Deploy Karpenter autoscaler to production cluster",
            "description": "Configure NodePool CRD and IAM instance profiles",
            "priority": {"name": "High"}
        }
    }
    task = transform_jira_to_task(sample_jira_payload)
    print(task.model_dump_json(indent=2))
```

## Operational Hardening & Schema Migration Rules

1. **Schema Version Tagging**: Include a mandatory `schema_version: "1.8.0"` attribute in the `metadata` dictionary to support backward compatibility during multi-agent system updates.
2. **Prevent Infinite Subtask Recursion**: Cap child subtask depth at `depth <= 4` within decomposition adapters to avoid blowing up context windows or execution limits.
3. **Strict Validation Fail-Fast**: Always pass incoming raw payloads through `TaskObject.model_validate()` before persisting into database tables or passing to FastMCP tools.
4. **Idempotent Task Keys**: Enforce deterministic `task_id` prefixing (`servicenow:<sys_id>`, `jira:<issue_key>`, `github:<owner>/<repo>/<issue_num>`) to prevent duplicate ingestion.
5. **PII & Credential Scrubbing**: Intercept `description` and `metadata` text blocks to strip passwords, OAuth tokens, and sensitive private user data before sending payloads to LLM APIs.

## Troubleshooting & Diagnostics

| Symptoms / Failure Mode | Root Cause Analysis | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **`ValidationError`: Priority Regex Mismatch** | Platform adapter passed non-standard priority string (e.g. `P1`, `Blocker`) | Check adapter transformation code | Map source priorities (`Blocker` -> `critical`, `P3` -> `medium`) before instantiation |
| **Infinite Recursion / Context Exhaustion** | Recursive child subtasks pointing back to parent `task_id` | `jq '.subtasks[] | .task_id'` | Implement parent-id checking in decomposition loop to prevent circular links |
| **State Machine Guard Violation** | Agent attempted forbidden state transition (e.g., `PENDING` -> `CLOSED` directly) | Inspect agent history log array | Enforce state machine transitions via Pydantic `@field_validator("status")` |
| **Jira / ServiceNow Sync Drift** | Updated status in Task Schema failed to sync back to enterprise API | `curl -i -X PUT <api-endpoint>` | Verify target platform API credentials and webhook subscription health |
| **FastMCP Tool De-serialization Error** | Missing optional string default values caused `NoneType` attribute error | `python3 -m pydantic.v2` test script | Set explicit `Optional[str] = None` and default values on all nullable schema fields |

## Related tools / concepts
- [ServiceNow MCP](../../tools/automation_orchestration/servicenow-mcp.md) — ServiceNow target integration.
- [Atlassian Jira MCP](../../tools/automation_orchestration/atlassian-jira-mcp.md) — Jira target integration.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Standard for agent tool-calling capabilities.
- [Antigravity](../../tools/ai_knowledge/antigravity-agent.md) — Stateful agent execution engine using task objects.
- [Temporal](../../tools/orchestration/temporal.md) — Workflow orchestrator for persistent task lifecycles.
- [Instructor](../../tools/frameworks/instructor.md) — Structured extraction validation for task inputs.
- [Google Tasks](../../tools/calendar_tasks/google-tasks.md) — Lightweight endpoint for personal tasks.
- [Search Patterns](../../knowledge_base/patterns/search-patterns.md) — Complementary pattern for unstructured informational lookups.

## Sources / References
- [JSON Schema Specification](https://json-schema.org/)
- [OpenClaw Core Architecture Index](../../../ARCHITECTURE.md)
- [FastMCP 3.1 Specification: Core Resources, Tasks, and Tools](https://modelcontextprotocol.io/)
- [Jira Cloud Platform API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
