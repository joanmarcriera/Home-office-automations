# Diagrid Catalyst

Diagrid Catalyst is an enterprise-grade agentic durable execution, security, and governance platform purpose-built for deploying resilient AI agents and workflows at scale.

## What it is

Diagrid Catalyst is a serverless, durable execution platform designed to run AI workloads, agents, and long-running workflows with built-in checkpointing, self-recovery, and security. Built on the open-source Distributed Application Runtime (Dapr) and its high-performance workflow engine, Catalyst intercepts agent executions and tool calls in real time. It enables stateful, autonomous systems to seamlessly survive crashes, deployments, and infrastructure outages without starting over or repeating expensive model calls.

## What problem it solves

AI agents often execute complex, multi-step chains of thoughts, tool invocations, and API calls. In high-concurrency or long-running tasks, single-point failures—such as transient network errors, rate limits, server redeployments, or container crashes—traditionally cause the entire agent loop to fail. If an agent crashes at step 99 of a 100-step task, restarting it from scratch wastes massive latencies, token consumption, and API costs.

Diagrid Catalyst solves this by:
- **Zero-loss Failures**: Saving intermediate agent execution states, tool inputs, and model outputs at every step.
- **Self-Healing Loops**: Intercepting agent runners to replay from the last completed check-point or tool execution when restarted.
- **Security & Governance Gateways**: Providing mTLS, zero-trust cryptographic identities, and fine-grained Model Context Protocol (MCP) policy control on every agent and downstream tool call.
- **Action Attestation**: Creating a tamper-proof cryptographic audit trail to prove what an autonomous agent actually did.

## Where it fits in the stack

**Infrastructure / Durable Execution Layer**. Diagrid Catalyst sits as an orchestration, security, and persistence wrapper around popular agent frameworks (like LangGraph, CrewAI, Microsoft Agent Framework, or OpenAI Agents SDK) and downstream services (databases, custom tools, or cloud resources).

```
┌─────────────────────────────────────────────────────────┐
│              User / Multi-Agent Applications            │
│       (LangGraph, CrewAI, Google ADK, OpenAI Agents)    │
└────────────────────────────┬────────────────────────────┘
                             │ Intercepts Loop Cycles
┌────────────────────────────▼────────────────────────────┐
│                    DIAGRID CATALYST                     │
│        (Durable Execution, mTLS, Cryptographic Auditing)  │
└────────────────────────────┬────────────────────────────┘
                             │ Secure Tool Calls (MCP)
┌────────────────────────────▼────────────────────────────┐
│ Downstream Tools / VectorDBs / Databases / Cloud Infra   │
└─────────────────────────────────────────────────────────┘
```

## Typical use cases

- **Long-Horizon Multi-Agent Tasks**: Executing multi-hour software engineering, research, or data aggregation agents where transient failures are highly probable.
- **Enterprise Agent Security**: Enforcing zero-trust network boundaries and mTLS encryption on agents interacting with critical company databases or intranet systems.
- **Cryptographic Compliance and Auditing**: Generating secure, non-repudiable logs of agent actions for regulatory compliance in finance, healthcare, or security sectors.
- **Cost-Optimized Agent Orchestration**: Preventing duplicate model and tool invocations across system restarts.

## Strengths

- **Multi-Framework Support**: Seamlessly integrates with LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, and custom Python loops.
- **Fine-Grained Checkpoint Playback**: Leverages Dapr Workflows under the hood to replay orchestrations while instantly resolving previously completed activities.
- **Enterprise-Grade Identity**: Cryptographic identity verification and attestation at each tool and agent boundary.
- **Developer Simplicity**: Integrates into existing Python code bases with minimal modifications (e.g., swapping runners).

## Limitations

- **Ecosystem Constraints**: Requires integrating with supported agent runners, which may introduce minor overhead in simple single-step scripts.
- **Side Effect Handling**: Like all durable execution engines, external side effects must be designed carefully; downstream tools must support idempotency or reconciliation.
- **Kubernetes-Native Bias**: Optimized primarily for Kubernetes or cloud environments, making strictly offline, local-only lab deployments more complex to configure.

## When to use it

- When your agents execute high-cost, multi-step operations (e.g., autonomous software engineering, complex database migrations).
- When agents require strict security controls, audit logs, and secure access to databases/tools.
- When you are deploying agents to Kubernetes/production environments where system crashes and auto-scaling events are common.

## When not to use it

- For lightweight, single-step LLM questions or basic chatbot interfaces.
- For local-only, strictly air-gapped home environments with zero cloud connectivity or Dapr support.

## Getting started

To get started with Diagrid Catalyst, you first deploy the core platform in your Kubernetes environment or connect to Diagrid Cloud.

### 1. Installation

```bash
# Add the Diagrid Catalyst Helm repository
helm repo add diagrid https://charts.diagrid.io
helm repo update

# Install Diagrid Catalyst in your Kubernetes lab/production cluster
helm install catalyst diagrid/catalyst \
  --namespace diagrid-system \
  --create-namespace \
  --set joinToken="YOUR_DIAGRID_CLOUD_JOIN_TOKEN"
```

### 2. Verify Deployment

```bash
kubectl get pods -n diagrid-system
```

## CLI examples

Diagrid provides a CLI for managing, inspecting, and tracking durable agent sessions.

### Managing Agent Sessions

```bash
# List all active durable agent sessions
diagrid sessions list

# Describe a specific failed agent session to pinpoint the exact failure step
diagrid sessions describe agent-session-091a4

# Force resume a suspended agent workflow from its last saved activity
diagrid sessions resume agent-session-091a4
```

### Securely Invoking Tools (MCP)

```bash
# Register a secure MCP tool endpoint with policy controls
diagrid tools register --name "customer-db" --url "http://mcp-server.internal:5005" --policy zero-trust
```

## API examples

### Programmatic Durable State Validation (Python & Pydantic v2)

This Python script showcases how an agentic application can validate and register task execution states, checkpoint payloads, and recovery metadata using **Pydantic v2** prior to handing off execution loops to Diagrid Catalyst runners.

```python
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator

class ToolExecutionRecord(BaseModel):
    tool_name: str = Field(..., description="The name of the invoked tool")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Input parameters passed to the tool")
    result_hash: str = Field(..., description="Cryptographic hash of the tool's return payload")
    execution_time: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of invocation")

class AgentCheckpointState(BaseModel):
    session_id: str = Field(..., description="Unique UUID for the durable execution session")
    current_step: int = Field(..., ge=0, description="The sequential index of the active step")
    completed_tools: List[ToolExecutionRecord] = Field(default_factory=list, description="List of successfully completed tools")
    framework: str = Field(..., description="The underlying agent framework (e.g. LangGraph, CrewAI)")
    state_variables: Dict[str, Any] = Field(default_factory=dict, description="Agent's current memory dictionary")

    @field_validator("framework")
    @classmethod
    def validate_framework_choice(cls, value: str) -> str:
        allowed = {"LANGGRAPH", "CREWAI", "GOOGLE_ADK", "OPENAI_AGENTS", "MICROSOFT_AGENT_FRAMEWORK", "CUSTOM"}
        if value.upper() not in allowed:
            raise ValueError(f"Framework must be one of {allowed}")
        return value.upper()

def create_durable_checkpoint(session_id: str, step: int, tool_runs: List[dict], framework: str, state: dict) -> AgentCheckpointState:
    # Prepare structured run tracking records
    records = []
    for run in tool_runs:
        records.append(ToolExecutionRecord(
            tool_name=run["tool"],
            arguments=run.get("args", {}),
            result_hash=run["hash"]
        ))

    # Instantiate and validate checkpoint using Pydantic v2
    checkpoint = AgentCheckpointState(
        session_id=session_id,
        current_step=step,
        completed_tools=records,
        framework=framework,
        state_variables=state
    )
    return checkpoint

# Example Scenario: Pre-validating state before registering with Diagrid Catalyst Graph Runner
if __name__ == "__main__":
    session_id = str(uuid.uuid4())
    simulated_tool_runs = [
        {"tool": "fetch-user-profile", "args": {"user_id": 105}, "hash": "0x91a4b83ef29"},
        {"tool": "query-vector-db", "args": {"query": "durable execution"}, "hash": "0x3c7db8281fe"}
    ]

    validated_checkpoint = create_durable_checkpoint(
        session_id=session_id,
        step=2,
        tool_runs=simulated_tool_runs,
        framework="LangGraph",
        state={"active_query": "durable execution", "user_authenticated": True}
    )

    print("Durable checkpoint state successfully validated for Diagrid Catalyst:")
    print(validated_checkpoint.model_dump_json(indent=2))
```

### Running with Diagrid DaprWorkflowGraphRunner

Swapping standard agent run loops with Catalyst's durable runner is highly straightforward:

```python
from langgraph.graph import StateGraph
from diagrid.catalyst.runners import DaprWorkflowGraphRunner

# Define a standard LangGraph agent graph
builder = StateGraph(dict)
# ... [define nodes, edges, entry points] ...
graph = builder.compile()

# Wrap compiled graph with Diagrid Catalyst durable workflow runner
durable_agent = DaprWorkflowGraphRunner(
    graph=graph,
    session_id="agent-session-091a4",
    catalyst_endpoint="http://localhost:50001"
)

# Run or automatically resume the agent workflow seamlessly from the last crash point
result = durable_agent.run(inputs={"task": "Perform security audit of local cluster"})
print(f"Agent finished successfully. Final output: {result}")
```

## Related tools / concepts

- [Dapr](https://dapr.io/) — The Distributed Application Runtime on which Catalyst is built.
- [Temporal](../orchestration/temporal.md) — Comparative code-first durable execution orchestrator.
- [LangGraph](../agents/cline.md) — The leading agent graph framework optimized for Catalyst.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Secure protocol used by Catalyst for resource governance.
- [OpenTelemetry Collector](../process_understanding/opentelemetry-collector.md) — Unified telemetry collector for Catalyst metrics.
- [Infrastructure Index](index.md) — Index of the home-office infrastructure components.

## Sources / references

- [Diagrid Official Website](https://www.diagrid.io/)
- [Dapr Integrations: Diagrid Catalyst](https://docs.dapr.io/integrations/diagrid/diagrid-catalyst/)
- [Diagrid Catalyst vs Temporal: Durable Execution comparison](https://www.diagrid.io/infrastructure/diagrid-catalyst-vs-temporal)
- [Diagrid gives failed AI agents a way to resume - The New Stack](https://thenewstack.io/diagrid-catalyst-agent-recovery/)

## Contribution Metadata

- Last reviewed: 2026-11-23
- Confidence: high
