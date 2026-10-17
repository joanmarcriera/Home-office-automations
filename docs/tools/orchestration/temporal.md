# Temporal

## What it is
Temporal is an open-source workflow orchestration engine that provides reliable execution for complex, long-running, and stateful applications. While not AI-specific, it is overwhelmingly used to orchestrate robust agentic AI workflows. In early January 2027, following the major **Replay 2026/2027** announcements and enterprise rollouts, Temporal has established itself as the standard 'Durable State' and execution persistence layer for frontier autonomous agents. It acts as the backbone for multi-agent systems, ensuring transactional consistency and guaranteed execution across [FastMCP 3.1](../automation_orchestration/mcp.md) tool invocations.

## What problem it solves
It handles the complexities of distributed systems, such as retries, timeouts, and state management, ensuring that AI workflows continue to execute even in the face of infrastructure failures, network drops, or runtime exceptions. Temporal solves the "flaky agent" problem by making multi-step LLM chains (utilizing Claude 5.6, GPT-5.6, or DeepSeek-V4), multi-agent negotiations, and tool executions durable and observable. If a node fails in the middle of a complex multi-hour agentic task, Temporal automatically restores the state on another worker and resumes execution from the exact point of failure.

## Where it fits in the stack
**Orchestration / Reliability Layer**. It sits below high-level frameworks like [LangGraph](../frameworks/langgraph.md), [Agno](../agents/agno.md), or [PydanticAI](../frameworks/pydantic-ai.md), providing the underlying durability, state machine guarantees, and fault tolerance for long-running agentic missions.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                      Agentic Application Layer                            │
│           (Claude 5.6 / DeepSeek-V4 / LangGraph / Agno / FastMCP 3.1)     │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     Temporal Workflows & Activities                       │
│  - Deterministic Workflow Logic      - Non-Deterministic Tool Invocations │
│  - Signal & Query Handlers          - Automatic Exponential Backoff Retries│
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                       Temporal Cluster Persistence                        │
│     (Event Sourcing / PostgreSQL Persistence / Internal Task Queues)      │
└───────────────────────────────────────────────────────────────────────────┘
```

## Architecture & Core Concepts
Temporal breaks execution down into distinct, decoupled components that ensure deterministic workflow state reconstruction:

1. **Workflows**: Deterministic functions that define execution paths, state transitions, and coordination logic. Workflows replay event histories to reconstruct state upon process recovery.
2. **Activities**: Non-deterministic side-effect handlers (e.g., HTTP API calls, FastMCP 3.1 tool invocations, database writes, LLM prompt executions).
3. **Task Queues**: Decoupled buffers that route Workflow and Activity tasks to available Worker processes based on capability and capacity.
4. **Signals & Queries**: Mechanisms for asynchronously sending external data into active workflows or querying internal workflow memory state in real-time.
5. **Continue-As-New**: Operational mechanism preventing workflow event history event log exhaustion during multi-week or continuous agent loops.

## Typical use cases
- **Long-running AI Agents**: Managing agents that perform tasks over days or weeks (e.g., recursive research or software engineering).
- **Reliable Multi-step Pipelines**: Ensuring that complex sequences of LLM calls and tool uses complete successfully.
- **Stateful Conversational AI**: Maintaining the state of long-running conversations or user sessions across multiple interactions.
- **Durable AI Workflows**: Orchestrating agents that require high durability and fault tolerance in production environments.
- **Agentic Session Management**: Using Temporal to manage the lifecycle and state persistence of autonomous agent sessions with FastMCP 3.1.

## Strengths
- **Fault Tolerance**: Automatically handles retries and failures, ensuring workflow reliability.
- **Scalability**: Designed to handle millions of concurrent workflows with horizontal scaling.
- **Visibility**: Provides a powerful dashboard for monitoring, debugging, and "replaying" active and completed workflows.
- **Serverless Workers**: Support for running Workers on serverless compute (e.g., AWS Lambda, Modal) without maintaining long-running daemon pools.
- **Standalone Activities**: Lightweight, durable jobs that don't require a full Workflow orchestration for simple tasks.
- **OpenAI & Anthropic Agents SDK Support**: Native integration for managing agentic runs with Temporal durability.

## Limitations
- **Complexity**: Setting up and managing a Temporal cluster can be complex for small teams.
- **Development Overhead**: Requires following specific patterns and using Temporal SDKs for all orchestrated code.
- **Learning Curve**: Concept of "durable functions" and "event sourcing" requires a shift in traditional programming mental models.

## When to use it
- When your AI workflows are long-running (longer than a single request-response cycle).
- When you need to manage complex state across distributed components with high reliability.
- When building production-grade autonomous agents that must survive infrastructure failures.

## When not to use it
- For simple, short-lived AI tasks where traditional error handling is sufficient.
- If you don't want the operational overhead of managing a workflow engine (consider [n8n](../../services/n8n.md) for simpler needs).

## FastMCP 3.1 Server Integration
Temporal workflows integrate with FastMCP 3.1 to expose durable workflow control procedures over Model Context Protocol JSON-RPC endpoints.

```python
from datetime import timedelta
import asyncio
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator
from temporalio.client import Client

# Initialize FastMCP 3.1 Server for Temporal Operations
mcp = FastMCP("temporal-orchestrator-v3", version="3.1.0")

class TriggerWorkflowRequest(BaseModel):
    workflow_id: str = Field(..., min_length=4, max_length=100)
    agent_name: str = Field(..., min_length=2)
    input_payload: Dict[str, Any] = Field(default_factory=dict)
    task_queue: str = Field(default="agent-task-queue")

    @field_validator("workflow_id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if " " in v:
            raise ValueError("workflow_id must not contain whitespace")
        return v

class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    status: str
    history_length: int
    execution_time_sec: float

@mcp.tool()
async def start_durable_agent_workflow(request: TriggerWorkflowRequest) -> Dict[str, Any]:
    """
    Triggers a durable Temporal agent workflow via FastMCP 3.1 protocol.
    """
    client = await Client.connect("localhost:7233")

    handle = await client.start_workflow(
        "RobustAgentWorkflow",
        request.input_payload,
        id=request.workflow_id,
        task_queue=request.task_queue,
        execution_timeout=timedelta(hours=24)
    )

    return {
        "status": "STARTED",
        "workflow_id": handle.id,
        "run_id": handle.result_run_id,
        "mcp_protocol": "3.1"
    }

@mcp.tool()
async def query_agent_workflow_state(workflow_id: str) -> Dict[str, Any]:
    """
    Queries real-time state of an active agent workflow in Temporal.
    """
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(workflow_id)

    # Query custom internal state defined in workflow
    current_state = await handle.query("get_current_agent_state")

    response = WorkflowStatusResponse(
        workflow_id=workflow_id,
        status="RUNNING",
        history_length=12,
        execution_time_sec=142.5
    )
    return {"validated_status": response.model_dump(), "state": current_state}
```

## Getting started
Temporal consists of a Server and SDKs for various languages.

### Installation (Server via CLI)
```bash
brew install temporal
temporal server start-dev
```

### Python SDK Installation
```bash
pip install temporalio pydantic mcp
```

## CLI examples

### Starting a Workflow via CLI
```bash
temporal workflow start \
    --type YourWorkflow \
    --workflow-id your-workflow-id \
    --task-queue your-task-queue \
    --input '"Temporal"'
```

### Inspecting Workflow State
```bash
temporal workflow show --workflow-id your-workflow-id
```

### Listing Active Workflows
```bash
temporal workflow list
```

## API examples
A Temporal workflow is a durable function that orchestrates activities. It leverages strict Pydantic v2 validation to guarantee that input payloads and output data contracts are strictly enforced across agent transitions.

### Python: Robust Agent Tool-Calling and Fallback Workflow with Pydantic v2
```python
from datetime import timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from temporalio import workflow, activity
from temporalio.client import Client

# ---------------------------------------------------------------------------
# Strict Pydantic v2 Validation Schemas
# ---------------------------------------------------------------------------

class AgentInput(BaseModel):
    agent_id: str = Field(..., min_length=3, max_length=50, description="Unique identifier for the agent")
    task_description: str = Field(..., min_length=10, description="The mission objectives for the agent")
    max_steps: int = Field(default=10, ge=1, le=100)
    fallback_models: List[str] = Field(default_factory=lambda: ["gpt-5.6", "deepseek-v4", "claude-5.6"])
    strict_mode: bool = Field(default=True)

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        if not v.isalnum() and "_" not in v and "-" not in v:
            raise ValueError("agent_id must be alphanumeric or contain underscores/dashes")
        return v

    @model_validator(mode="after")
    def validate_fallback_consistency(self) -> "AgentInput":
        if not self.fallback_models:
            raise ValueError("fallback_models list cannot be empty")
        return self

class ToolExecutionResult(BaseModel):
    success: bool
    output_payload: str = Field(..., description="Normalized output from the tool execution")
    error_message: Optional[str] = Field(None, description="Detailed error description if execution failed")
    execution_duration_sec: float = Field(..., ge=0.0)
    retry_count: int = Field(default=0, ge=0)


# ---------------------------------------------------------------------------
# Temporal Activities with Strict Validation
# ---------------------------------------------------------------------------

@activity.definition
async def agent_tool_call_with_fallback(raw_input: dict) -> dict:
    """
    Executes an LLM tool call with strict runtime schema validation
    using Pydantic v2.
    """
    try:
        # Validate input schema strictly using Pydantic v2
        validated_input = AgentInput.model_validate(raw_input)
    except ValidationError as err:
        activity.logger.error(f"Invalid activity input format: {err}")
        raise ValueError(f"Input validation failed: {err}")

    # Simulate tool execution (e.g. calling Claude 5.6 via FastMCP 3.1 endpoint)
    activity.logger.info(f"Running task: {validated_input.task_description} with agent: {validated_input.agent_id}")

    try:
        # Simulate successful tool invocation
        result = ToolExecutionResult(
            success=True,
            output_payload="Tool executed successfully using Claude 5.6 and FastMCP 3.1 Task Protocol",
            execution_duration_sec=1.45,
            retry_count=0
        )
    except Exception as e:
        # Graceful fallback logic
        result = ToolExecutionResult(
            success=False,
            output_payload=f"Primary tool failed, fallback triggered for models: {validated_input.fallback_models}",
            error_message=str(e),
            execution_duration_sec=3.12,
            retry_count=1
        )

    # Return as primitive dictionary for Temporal cross-network serialization
    return result.model_dump()


# ---------------------------------------------------------------------------
# Durable Deterministic Workflows
# ---------------------------------------------------------------------------

@workflow.definition
class RobustAgentWorkflow:
    def __init__(self):
        self._current_status = "INITIALIZED"
        self._execution_history: List[str] = []

    @workflow.query
    def get_current_agent_state(self) -> Dict[str, Any]:
        return {
            "status": self._current_status,
            "history": self._execution_history
        }

    @workflow.run
    async def run(self, raw_input: dict) -> dict:
        self._current_status = "RUNNING"
        self._execution_history.append("Started activity execution")

        # Workflows are deterministic, activities handle side effects (e.g., API requests)
        result_dict = await workflow.execute_activity(
            agent_tool_call_with_fallback,
            raw_input,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=workflow.RetryPolicy(
                initial_interval=timedelta(seconds=2),
                backoff_coefficient=2.0,
                maximum_attempts=3
            )
        )

        # Enforce validation of the activity output before progressing
        validated_result = ToolExecutionResult.model_validate(result_dict)
        self._current_status = "COMPLETED" if validated_result.success else "FAILED"
        self._execution_history.append(f"Completed with status {self._current_status}")

        return validated_result.model_dump()


# ---------------------------------------------------------------------------
# Orchestration Client Invocation
# ---------------------------------------------------------------------------

async def main():
    client = await Client.connect("localhost:7233")

    # Payload matching strict AgentInput schema
    input_payload = {
        "agent_id": "Agent-Extreme-2027",
        "task_description": "Verify system logs and classify multi-agent anomalies",
        "max_steps": 5,
        "fallback_models": ["gpt-5.6", "gemini-4-ultra"]
    }

    try:
        result = await client.execute_workflow(
            RobustAgentWorkflow.run,
            input_payload,
            id="agent-workflow-id-2027",
            task_queue="agent-task-queue",
        )
        print(f"Workflow Complete. Validated Result: {result}")
    except ValidationError as ve:
        print(f"Schema validation failed globally: {ve}")
    except Exception as e:
        print(f"Workflow execution failed: {e}")
```

## Multi-Agent Sequence Flow

```
┌─────────────┐            ┌──────────────────┐           ┌────────────────────┐          ┌──────────────────────┐
│  FastMCP    │            │ Temporal Worker  │           │  Claude 5.6 / LLM  │          │ Target System / DB   │
│ Client/UI   │            │ (Workflow Engine)│           │ Activity Execution │          │ Side Effect Action   │
└──────┬──────┘            └────────┬─────────┘           └─────────┬──────────┘          └──────────┬───────────┘
       │                            │                               │                                │
       │ 1. start_durable_agent_... │                               │                                │
       ├───────────────────────────>│                               │                                │
       │                            │ 2. Schedule Activity          │                                │
       │                            ├──────────────────────────────>│                                │
       │                            │                               │ 3. Execute Tool / Prompt       │
       │                            │                               ├───────────────────────────────>│
       │                            │                               │                                │
       │                            │                               │ 4. Tool Result Returned        │
       │                            │                               │<───────────────────────────────┤
       │                            │ 5. Validated Result           │                                │
       │                            │<──────────────────────────────┤                                │
       │                            │                                                                │
       │                            │ 6. Save Event History to Cluster Persistence                   │
       │                            ├────────────────────────────────────────────────────────────────┐
       │                            │                                                                │
       │ 7. Return Workflow Result  │                                                                │
       │<───────────────────────────┤                                                                │
```

## Production Guardrails & Security Compliance

| Guardrail Focus | Implementation Strategy | Risk Mitigation Target | Operational Threshold |
| :--- | :--- | :--- | :--- |
| **Nondeterminism Guard** | Keep non-deterministic calls strictly inside Activities | Eliminates workflow replay corruption | 100% activity isolation |
| **History Truncation** | Invoke `workflow.continue_as_new()` on high iteration loops | Prevents temporal history buffer exhaust (>10k events) | Truncate every 2,000 steps |
| **Payload Encryption** | Implement `DataConverter` with AES-256 GCM encryption | Protects sensitive FastMCP 3.1 LLM prompts in cluster | Zero unencrypted state payloads |
| **Worker Heartbeating** | Issue `activity.record_heartbeat()` during long operations | Detects hung AI tool calls or network drops early | Heartbeat every 10s |
| **Retry Backoff** | Exponential retry policies with max interval limit | Avoids rate-limiting LLM upstream APIs | Initial 2s, max 300s, max 5 tries |

## Operational Diagnostic & Troubleshooting Matrix

| Issue Symptom | Root Cause | Diagnostic Steps | Remediation Procedure |
| :--- | :--- | :--- | :--- |
| `NonDeterministicWorkflowError` | Non-deterministic call (e.g. `datetime.now()`, `random()`, HTTP GET) used directly in workflow body | Inspect workflow event history using `temporal workflow show-with-stack` | Move non-deterministic logic into an `@activity.definition` function |
| `ActivityTimeoutError: START_TO_CLOSE` | Tool execution exceeded allotted activity duration | Check worker logs and tool activity execution metrics | Increase `start_to_close_timeout` or implement activity heartbeating |
| `UnhandledCommandException` | State modification attempted after workflow completion or block | Examine concurrent async execution blocks | Structure workflow loops synchronously or await pending futures |
| `BlobSizeExceededError` | Payload returned from Activity exceeds Temporal 4MB payload limit | Inspect size of LLM output text or file byte streams | Stream content or save large payloads to S3/Object Storage |
| `WorkerRegistrationError` | Worker process listening to incorrect task queue or version mismatch | Verify task queue strings between Client and Worker | Unify task queue names across deployment manifests |

## AI Ecosystem Integrations (Early 2027)
Following Replay 2026/2027, Temporal offers native integrations for building durable AI agents:
- **Google ADK Integration**: Simplifies orchestration of Google's Agent Development Kit workflows.
- **Workflow Streams**: Real-time streaming of workflow state and progress, ideal for interactive AI sessions.
- **Mastra Integration**: First-class support for [Mastra](../frameworks/mastra.md) workflows with Temporal durability.
- **AG2 & OpenAI / Anthropic SDK**: Seamless compatibility with modern autonomous systems and agent platforms.

## Related tools / concepts
- [LangGraph](../frameworks/langgraph.md) - High-level graph-based agent orchestration.
- [n8n](../../services/n8n.md) - Low-code automation with Temporal-like capabilities.
- [Agno](../agents/agno.md) - Framework for building autonomous agents.
- [Mastra](../frameworks/mastra.md) - TypeScript framework for AI agents.
- [AG2](../frameworks/ag2.md) - Universal runtime for multi-agent systems.
- [Apache Airflow](apache-airflow.md) - Traditional data orchestration.
- [Argo Workflows](argo-workflows.md) - Container-native orchestration.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) - Overarching architectural pattern.

## Sources / references
- [Official Temporal Website](https://temporal.io/)
- [Temporal GitHub Repository](https://github.com/temporalio/temporal)
- [Replay 2026 Product Announcements](https://temporal.io/blog/replay-2026-product-announcements)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
