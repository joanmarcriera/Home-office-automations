# Temporal

## What it is
Temporal is an open-source workflow orchestration engine that provides reliable execution for complex, long-running, and stateful applications. In late November/December 2026, the Temporal ecosystem has evolved to become the default 'Durable State' and execution persistence layer for frontier autonomous agents and multi-agent systems, providing a resilient foundation for long-running workflows orchestrating frontier models (such as Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.6) alongside Model Context Protocol (FastMCP 3.1) endpoints.

## What problem it solves
It solves the distributed-systems complexity of managing state, retries, timeouts, and state recovery in highly agentic workflows. As autonomous agents conduct multi-step tasks across several hours or days, network failures, API rate limits, or context window reboots can halt execution. Temporal guarantees complete execution safety, solving the "flaky agent" problem by making agentic chains, API calls, and tool integrations fully durable, observable, and re-executable.

## Where it fits in the stack
**Orchestration / Reliability Layer**. It sits underneath high-level multi-agent orchestration frameworks like [LangGraph](../frameworks/langgraph.md), [AG2](../frameworks/ag2.md), and [Mastra](../frameworks/mastra.md), providing the underlying durability and fault tolerance for active and background agent missions.

## Typical use cases
- **Long-Running AI Agents**: Executing autonomous coding, recursive research, or long-form business intelligence over days or weeks.
- **Reliable Multi-step Pipelines**: Coordinating complex sequences of tool calls, retrieval-augmented generation (RAG) loops, and human-in-the-loop approvals.
- **Durable Multi-Agent Negotiations**: Persisting conversations and negotiation states across distinct, specialized agents.
- **Agentic Session Management**: Safely maintaining session history, tool-execution results, and recovery checkpoints across intermittent network disconnections.

## Strengths
- **Infallible Fault Tolerance**: Automatically tracks state history and handles retries, state recovery, and timeouts without manual developer overhead.
- **Massive Scalability**: Horizontally scales to manage millions of concurrent active workflows with distributed workers.
- **Deterministic Replay**: Provides the ability to "replay" workflow state transitions to debug and audit agent reasoning.
- **FastMCP 3.1 Native Integration**: Exposes lightweight, secure, and durable activity targets conforming to late 2026 MCP specifications.
- **Serverless Worker Support**: Simplifies operations by enabling workers to scale up or down on serverless compute platforms (AWS Lambda, Modal, etc.).

## Limitations
- **Operational Complexity**: Initial setup, scaling, and management of a dedicated Temporal cluster can be high for small projects.
- **Development Constraints**: Code written within a Workflow definition must be completely deterministic (no random numbers, external API calls, or timezone queries directly in the workflow; those must be delegated to Activities).
- **Learning Curve**: Mastering event sourcing, activities vs. workflows, and state-reconstruction paradigms requires a cognitive shift.

## When to use it
- When orchestrating production-grade, multi-step autonomous agents that must survive server crashes, restarts, and network drops.
- When managing workflows with complex state recovery rules, human-in-the-loop approvals, or long waiting delays.
- When building mission-critical business automation using Claude 5.1 or GPT-5.5.

## When not to use it
- For trivial, single-request LLM completions where traditional retry libraries (e.g., Tenacity) are sufficient.
- For low-latency conversational apps where the added network roundtrips and queuing overhead of a distributed workflow engine are unacceptable.

## Getting started
Temporal consists of a local development server and language-specific SDKs.

### Installation (Server via CLI)
```bash
brew install temporal
temporal server start-dev
```

### Python SDK Installation
```bash
pip install temporalio pydantic
```

## CLI examples

### Starting a Workflow via CLI
```bash
temporal workflow start \
    --type RobustAgentWorkflow \
    --workflow-id agent-workflow-2026 \
    --task-queue agent-task-queue \
    --input '{"task_id": "T1", "agent_name": "Claude-5.1", "prompt": "Process Q4 metrics"}'
```

### Inspecting Workflow State
```bash
temporal workflow show --workflow-id agent-workflow-2026
```

### Listing Active Workflows
```bash
temporal workflow list
```

## API examples
The following Python example showcases a robust Temporal workflow and activity pattern utilizing **Pydantic v2** (`BaseModel`, `Field`, `model_validate`, `ValidationError`) for strict input and output validation in late 2026 SOTA agent pipelines.

### Python: Robust Agent Workflows with Pydantic v2 Validation
```python
import os
from datetime import timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from pydantic import BaseModel, Field, ValidationError

# Pydantic v2 Schema for robust workflow inputs
class AgentTaskInput(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the task run")
    agent_name: str = Field(..., description="Target frontier model (e.g., Claude 5.1, GPT-5.5, Gemini 4.0 Pro)")
    prompt: str = Field(..., description="System or user instructions for the agentic loop")
    max_steps: int = Field(default=5, ge=1, le=20, description="Max execution steps for safety")

# Pydantic v2 Schema for workflow outputs
class AgentTaskOutput(BaseModel):
    task_id: str
    status: str = Field(..., description="Terminal status of the run: 'success' or 'failed'")
    final_response: str = Field(..., description="Synthesized response from the agent")
    steps_executed: int

@activity.definition
async def run_agent_activity(input_dict: dict) -> dict:
    """
    Temporal Activity to invoke a frontier model using FastMCP 3.1 tools.
    Strictly validates raw input dictionary into a typed Pydantic Model.
    """
    try:
        # Pydantic v2 validation of raw activity inputs
        validated_input = AgentTaskInput.model_validate(input_dict)
    except ValidationError as ve:
        raise ValueError(f"Invalid activity payload schema: {ve}")

    # Simulated SOTA execution with Claude 5.1/GPT-5.5 via FastMCP 3.1 endpoints
    print(f"Executing robust loop for task {validated_input.task_id} with {validated_input.agent_name}")

    # Simulate successful agentic execution outcome
    output = AgentTaskOutput(
        task_id=validated_input.task_id,
        status="success",
        final_response=f"Successfully executed '{validated_input.prompt[:30]}...' via {validated_input.agent_name} with FastMCP 3.1 tools integration.",
        steps_executed=3
    )

    # Return serializable dict output
    return output.model_dump()

@workflow.definition
class RobustAgentWorkflow:
    @workflow.run
    async def run(self, raw_input: dict) -> dict:
        """
        Durable workflow orchestrating agent activities.
        Validates workflow-level input dict to ensure contract guarantees.
        """
        try:
            # Validate input immediately inside the workflow using Pydantic v2
            AgentTaskInput.model_validate(raw_input)
        except ValidationError as ve:
            raise ValueError(f"Workflow rejected: Input does not conform to AgentTaskInput: {ve}")

        # Execute Activity with strict retry policy
        raw_result = await workflow.execute_activity(
            run_agent_activity,
            raw_input,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=workflow.RetryPolicy(
                initial_interval=timedelta(seconds=2),
                backoff_coefficient=2.0,
                maximum_attempts=3
            )
        )

        # Validate output schema before completing workflow to preserve downstream contract consistency
        try:
            validated_output = AgentTaskOutput.model_validate(raw_result)
        except ValidationError as ve:
            raise ValueError(f"Activity returned corrupted output: {ve}")

        return validated_output.model_dump()

async def main():
    client = await Client.connect("localhost:7233")

    # Define our raw input parameters
    input_payload = {
        "task_id": "task-dec-2026-991",
        "agent_name": "Claude-5.1-Sonnet",
        "prompt": "Synthesize the latest Q4 2026 financial metrics",
        "max_steps": 10
    }

    # Execute workflow with strict input-output guarantees
    result_dict = await client.execute_workflow(
        RobustAgentWorkflow.run,
        input_payload,
        id="agent-workflow-id-2026-batch-352",
        task_queue="agent-task-queue",
    )

    # Parse final workflow output
    final_output = AgentTaskOutput.model_validate(result_dict)
    print(f"Workflow Complete. Status: {final_output.status}, Response: {final_output.final_response}")
```

## Related tools / concepts
- [LangGraph](../frameworks/langgraph.md) - High-level graph-based agent orchestration.
- [n8n](../../services/n8n.md) - Low-code automation with Temporal-like capabilities.
- [Mastra](../frameworks/mastra.md) - TypeScript framework for AI agents with Temporal orchestration support.
- [AG2](../frameworks/ag2.md) - Universal runtime for multi-agent systems.
- [Apache Airflow](apache-airflow.md) - Traditional data orchestration.
- [Argo Workflows](argo-workflows.md) - Container-native orchestration.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) - Overarching architectural pattern.

## Sources / references
- [Official Temporal Website](https://temporal.io/)
- [Temporal GitHub Repository](https://github.com/temporalio/temporal)
- [Replay 2026 Product Announcements](https://temporal.io/blog/replay-2026-product-announcements)
- [Durable Agents: Building for Reliability (Late 2026 Update)](https://temporal.io/blog/durable-agents-2026)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
