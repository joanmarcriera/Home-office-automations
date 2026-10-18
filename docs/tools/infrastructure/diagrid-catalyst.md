# Diagrid Catalyst

Diagrid Catalyst is an enterprise-grade agentic durable execution, security, and governance platform purpose-built for deploying resilient AI agents and multi-agent workflows at scale with native **FastMCP 3.1** protocol support.

## What it is

Diagrid Catalyst is a serverless, durable execution platform designed to run AI workloads, agents, and long-running workflows with built-in checkpointing, self-recovery, WebAssembly (Wasm) isolated micro-runtimes, and zero-trust security. Built on the open-source Distributed Application Runtime (Dapr) and its high-performance workflow engine, Catalyst intercepts agent executions and tool calls in real time. It enables stateful, autonomous systems to seamlessly survive crashes, cloud redeployments, and API outages without repeating expensive model invocations or losing intermediate execution state.

## What problem it solves

AI agents often execute complex, multi-step chains of thought, tool invocations, and API calls. In high-concurrency or long-running tasks, single-point failures—such as transient network errors, rate limits, server redeployments, or container crashes—traditionally cause the entire agent loop to fail. If an agent crashes at step 99 of a 100-step task, restarting it from scratch wastes massive latencies, token consumption, and API costs.

Diagrid Catalyst solves this by:
- **Zero-loss Failures**: Saving intermediate agent execution states, FastMCP 3.1 tool inputs, and model outputs at every step.
- **Self-Healing Loops**: Intercepting agent runners to replay from the last completed check-point or tool execution when restarted.
- **Security & Governance Gateways**: Providing mTLS, zero-trust cryptographic identities, and fine-grained Model Context Protocol (FastMCP 3.1) policy control on every agent and downstream tool call.
- **Action Attestation**: Creating a tamper-proof cryptographic audit trail to prove what an autonomous agent actually did.

## Where it fits in the stack

**Infrastructure / Durable Execution Layer**. Diagrid Catalyst sits as an orchestration, security, and persistence wrapper around popular agent frameworks (like LangGraph, CrewAI, Microsoft Agent Framework, or FastMCP 3.1 multi-agent topologies) and downstream services (databases, custom tools, or cloud resources).

```text
┌─────────────────────────────────────────────────────────┐
│              User / Multi-Agent Applications            │
│       (FastMCP 3.1, LangGraph, CrewAI, Google ADK)      │
└────────────────────────────┬────────────────────────────┘
                             │ Intercepts Loop Cycles
┌────────────────────────────▼────────────────────────────┐
│                    DIAGRID CATALYST                     │
│        (Durable Execution, mTLS, Cryptographic Auditing)  │
└────────────────────────────┬────────────────────────────┘
                             │ Secure Tool Calls (FastMCP 3.1)
┌────────────────────────────▼────────────────────────────┐
│ Downstream Tools / VectorDBs / Databases / Cloud Infra   │
└─────────────────────────────────────────────────────────┘
```

## Durable State Interception & Workflow Replay Sequence

```text
┌──────────────┐      ┌──────────────────┐      ┌──────────────────────────┐      ┌──────────────────┐
│ Agent Runner │      │ Diagrid Interceptor│     │ Catalyst State Store     │      │ External Tool    │
└──────┬───────┘      └────────┬─────────┘      └────────────┬─────────────┘      └────────┬─────────┘
       │                       │                             │                             │
       │ 1. Invoke Tool Call   │                             │                             │
       ├──────────────────────>│                             │                             │
       │                       │ 2. Check Cached Activity    │                             │
       │                       ├────────────────────────────>│                             │
       │                       │                             │                             │
       │                       │ 3. Cache Miss (New Step)    │                             │
       │                       │<────────────────────────────┤                             │
       │                       │                             │                             │
       │                       │ 4. Exec Tool with mTLS      │                             │
       │                       ├──────────────────────────────────────────────────────────>│
       │                       │                             │                             │
       │                       │ 5. Return Tool Execution Result                           │
       │                       │<──────────────────────────────────────────────────────────┤
       │                       │                             │                             │
       │                       │ 6. Persist Cryptographic Checkpoint                      │
       │                       ├────────────────────────────>│                             │
       │                       │                             │                             │
       │ 7. Return Result      │                             │                             │
       │<──────────────────────┤                             │                             │
       │                       │                             │                             │
```

## Typical use cases

- **Long-Horizon Multi-Agent Tasks**: Executing multi-hour software engineering, research, or data aggregation agents where transient failures are highly probable.
- **Enterprise Agent Security**: Enforcing zero-trust network boundaries and mTLS encryption on agents interacting with critical company databases or intranet systems.
- **Cryptographic Compliance and Auditing**: Generating secure, non-repudiable logs of agent actions for regulatory compliance in finance, healthcare, or security sectors.
- **Cost-Optimized Agent Orchestration**: Preventing duplicate model and tool invocations across system restarts.

## Strengths

- **FastMCP 3.1 Integration**: Seamlessly intercepts and durably records FastMCP 3.1 tool invocations across distributed microservices.
- **Multi-Framework Support**: Seamlessly integrates with FastMCP 3.1, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, and custom Python loops.
- **Fine-Grained Checkpoint Playback**: Leverages Dapr Workflows under the hood to replay orchestrations while instantly resolving previously completed activities.
- **Enterprise-Grade Identity**: Cryptographic identity verification and attestation at each tool and agent boundary.

## Limitations

- **Ecosystem Constraints**: Requires integrating with supported agent runners, which may introduce minor overhead in simple single-step scripts.
- **Side Effect Handling**: External side effects must be designed carefully; downstream tools must support idempotency or reconciliation.

## When to use it

- When your agents execute high-cost, multi-step operations (e.g., autonomous software engineering, complex database migrations).
- When agents require strict security controls, audit logs, and secure access to databases/tools.
- When deploying agents to Kubernetes/production environments where system crashes and auto-scaling events are common.

## When not to use it

- For lightweight, single-step LLM questions or basic chatbot interfaces.
- For local-only, strictly air-gapped home environments with zero cloud connectivity or Dapr support.

## Getting started

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

### Securely Invoking Tools (FastMCP 3.1)

```bash
# Register a secure FastMCP 3.1 tool endpoint with policy controls
diagrid tools register --name "customer-db" --url "http://mcp-server.internal:5005" --protocol fastmcp-v3.1 --policy zero-trust
```

## API examples

### Programmatic Durable State Validation (Python & Pydantic v2)

This Python script showcases how an agentic application can validate and register task execution states, checkpoint payloads, and recovery metadata using **Pydantic v2** prior to handing off execution loops to Diagrid Catalyst runners.

```python
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ToolExecutionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    tool_name: str = Field(..., description="The name of the invoked tool")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Input parameters passed to the tool")
    result_hash: str = Field(..., description="Cryptographic hash of the tool's return payload")
    execution_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of invocation")

class AgentCheckpointState(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    session_id: str = Field(..., description="Unique UUID for the durable execution session")
    current_step: int = Field(..., ge=0, description="The sequential index of the active step")
    completed_tools: List[ToolExecutionRecord] = Field(default_factory=list, description="List of successfully completed tools")
    framework: str = Field(..., description="The underlying agent framework (e.g. FASTMCP, LANGGRAPH, CREWAI)")
    state_variables: Dict[str, Any] = Field(default_factory=dict, description="Agent's current memory dictionary")

    @field_validator("framework")
    def validate_framework_choice(cls, value: str) -> str:
        allowed = {"FASTMCP", "LANGGRAPH", "CREWAI", "GOOGLE_ADK", "OPENAI_AGENTS", "MICROSOFT_AGENT_FRAMEWORK", "CUSTOM"}
        if value.upper() not in allowed:
            raise ValueError(f"Framework must be one of {allowed}")
        return value.upper()

def create_durable_checkpoint(session_id: str, step: int, tool_runs: List[dict], framework: str, state: dict) -> AgentCheckpointState:
    records = []
    for run in tool_runs:
        records.append(ToolExecutionRecord(
            tool_name=run["tool"],
            arguments=run.get("args", {}),
            result_hash=run["hash"]
        ))

    checkpoint = AgentCheckpointState(
        session_id=session_id,
        current_step=step,
        completed_tools=records,
        framework=framework,
        state_variables=state
    )
    return checkpoint

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
        framework="FASTMCP",
        state={"active_query": "durable execution", "user_authenticated": True}
    )

    print("Durable checkpoint state successfully validated for Diagrid Catalyst:")
    print(validated_checkpoint.model_dump_json(indent=2))
```

### FastMCP 3.1 Integration & Server Implementation

```python
"""
FastMCP 3.1 Durable Execution State Server for Diagrid Catalyst
Manages state checkpoints, activity replays, and event orchestration.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CatalystMCP")

mcp = FastMCP("Diagrid-Catalyst-Durable-Server", version="3.1.0")

@mcp.tool()
def save_durable_checkpoint(catalyst_url: str, session_id: str, state: AgentCheckpointState) -> Dict[str, Any]:
    """Persists an agent execution checkpoint into Diagrid Catalyst state engine."""
    endpoint = f"{catalyst_url.rstrip('/')}/v1.0/state/catalyst-statestore"
    payload = [{
        "key": f"session-{session_id}",
        "value": json.loads(state.model_dump_json())
    }]
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(endpoint, json=payload, headers=headers, timeout=5)
        res.raise_for_status()
        return {"status": "checkpoint_saved", "session_id": session_id, "step": state.current_step}
    except Exception as err:
        logger.error(f"Failed to persist checkpoint: {err}")
        return {"error": str(err), "status": "checkpoint_failed"}

if __name__ == "__main__":
    mcp.run()
```

## Production Kubernetes Manifests

Below is a complete Kubernetes manifest template deploying Diagrid Catalyst sidecars alongside an agent runtime workload:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-durable-runner
  namespace: default
  labels:
    app: agent-runner
spec:
  replicas: 2
  selector:
    matchLabels:
      app: agent-runner
  template:
    metadata:
      labels:
        app: agent-runner
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "agent-runner-app"
        dapr.io/app-port: "8080"
        dapr.io/enable-mtls: "true"
        diagrid.io/catalyst-enabled: "true"
    spec:
      containers:
        - name: agent-container
          image: myregistry.internal/agent-runner:v1.4.0
          ports:
            - containerPort: 8080
          env:
            - name: DIAGRID_CATALYST_URL
              value: "http://localhost:3500"
            - name: FASTMCP_VERSION
              value: "3.1"
          resources:
            requests:
              cpu: "500m"
              memory: "1Gi"
            limits:
              cpu: "2000m"
              memory: "4Gi"
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Possible Cause | Diagnostic Command | Resolution |
| :--- | :--- | :--- | :--- |
| `StateStoreConnectionRefused` | Dapr state component not bound to Catalyst statestore | `kubectl logs -l app=agent-runner -c daprd` | Verify Catalyst joinToken and statestore binding in Dapr component YAML. |
| `DuplicateActivityReplayError` | External tool call was not idempotent | `diagrid sessions describe <session_id>` | Wrap non-idempotent tool calls in Catalyst activity handlers to ensure single execution. |
| `mTLSIdentityVerificationFailed` | Cryptographic certificate mismatch between agent and sidecar | `diagrid certs status` | Rotate mTLS certificates or check SPIFFE trust domain configuration. |
| `CheckpointPayloadTooLarge` | Agent memory payload exceeded maximum gRPC size (4MB) | Inspect state_variables size in python logs | Store large payloads in vector store and keep checkpoint state minimal. |

## Zero-Trust Security & Operational Guardrails

1. **Cryptographic Action Attestation**: Enforce Wasm isolated micro-runtimes with signed cryptographic digests for all external tool executions.
2. **mTLS Policy Enforcement**: Reject unencrypted TCP traffic between agent runners and downstream database connectors.
3. **Idempotency Mandate**: Ensure all write-heavy tools invoked via FastMCP 3.1 support transaction keys or deduplication tokens to handle replay safety.
4. **Least-Privilege Token Scopes**: Assign short-lived JWT tokens with minimal tool invocation privileges to autonomous agent instances.

## Related tools / concepts

- [Dapr](dapr.md) — The Distributed Application Runtime on which Catalyst is built.
- [Temporal](../orchestration/temporal.md) — Code-first durable execution orchestrator.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool and resource governance protocol.
- [OpenTelemetry Collector](../process_understanding/opentelemetry-collector.md) — Unified telemetry collector for Catalyst metrics.

## Sources / references

- [Diagrid Official Website](https://www.diagrid.io/)
- [Dapr Integrations: Diagrid Catalyst](https://docs.dapr.io/integrations/diagrid/diagrid-catalyst/)
- [Diagrid Catalyst Agent Recovery](https://thenewstack.io/diagrid-catalyst-agent-recovery/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
