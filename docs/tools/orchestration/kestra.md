# Kestra

Kestra is an open-source orchestration platform for declarative, scheduled, event-driven, and business-critical workflows. It uses YAML-defined flows, a web UI, and a powerful plugin architecture. As of early January 2027, **v0.20.x** is the stable release, featuring enhanced **Flow Loops**, first-class **Python Script** support, and native **FastMCP 3.1** Task Protocol support for extending Kestra with agentic tools.

## What it is
Kestra is a declarative orchestration platform that allows engineering teams to define complex workflows as simple YAML files. It provides a unified control plane for coordinating scripts (Python, Node.js, Shell), data tools, and cloud services.

## What problem it solves
Kestra bridges the gap between infrastructure automation and data orchestration. It eliminates the "hidden" logic often found in cron jobs or custom scripts by making every execution observable, retryable, and version-controllable. It simplifies the creation of event-driven agentic loops by providing native triggers for external events.

## Where it fits in the stack
**Orchestration / Declarative Automation Platform**. It serves as the coordination layer that sits above your infrastructure (Kubernetes, Docker, Cloud) and data/AI services. In early January 2027, it is a key enabler for **Agentic Workflow Orchestration**, allowing models like [Claude 5.6](../ai_knowledge/claude-mythos.md), [GPT-5.6](../ai_knowledge/chatgpt.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini-macos.md), [Gemma 4](../ai_knowledge/gemma.md), [DeepSeek-V4](../ai_knowledge/llama.md), or [Qwen 3.6 VL](../ai_knowledge/qwen.md) to be integrated into structured, declarative processes via [FastMCP 3.1 Task Protocol](../automation_orchestration/mcp.md).

```
                     ┌─────────────────────────────────────────┐
                     │          Kestra Control Plane           │
                     │       (YAML Declarative Engine)         │
                     └────────────────────┬────────────────────┘
                                          │
                                          ▼
                     ┌─────────────────────────────────────────┐
                     │          FastMCP 3.1 Task Router        │
                     └──────┬───────────────────────────┬──────┘
                            │                           │
                            ▼                           ▼
             ┌─────────────────────────────┐ ┌─────────────────────────────┐
             │    Docker / K8s Script Task │ │  Agentic LLM Inference Task │
             │  (Python, Bash, Terraform)  │ │ (Claude 5.6, GPT-5.6, Qwen) │
             └─────────────────────────────┘ └─────────────────────────────┘
```

## Feature Comparison Matrix

| Feature / Metric | Kestra | Apache Airflow | Prefect |
| :--- | :--- | :--- | :--- |
| **Workflow Definition** | Declarative YAML | Code (Python DAGs) | Code (Python Decorators) |
| **Agentic FastMCP 3.1**| First-Class Native Plugin | Custom Operators | Custom Tasks |
| **UI Control Plane** | Embedded Real-time Web UI | Webserver Dashboard | Prefect Cloud / Server |
| **Event Triggers** | Built-in Multi-Source | Sensor Operators | Automation Triggers |
| **Script Execution** | Embedded Docker / Process | Worker Pods / Celery | Agent Infrastructure |

## Typical use cases
- **AI Model Retraining**: Triggering a training pipeline when new data arrives, followed by evaluation and notification.
- **Infrastructure Provisioning**: Coordinating Terraform or Ansible runs with post-deployment health checks.
- **Enterprise ETL/ELT**: Moving data between internal systems and warehouses with robust error handling.
- **Event-Driven Agentic Loops**: Triggering an AI agent ([Claude 5.1](../ai_knowledge/claude-mythos.md)) via an MCP tool as soon as a specific event (e.g., a new GitHub issue) is detected.

## Strengths
- **Declarative YAML**: Everything is defined in code, making it version-controllable and easy to review.
- **Embedded Scripts**: Run Python, Node.js, or Shell scripts directly within a flow without managing external workers.
- **Event-Driven**: Native support for triggers like file arrivals, webhooks, and message queue events.
- **High Observability**: A rich UI provides real-time logs, flow visualization, and performance metrics.
- **FastMCP 3.1 Support**: Seamlessly integrate agentic tools into your declarative workflows.

## Limitations
- **YAML Learning Curve**: While simpler than complex Python DAGs, the YAML schema for advanced plugins requires study.
- **Not for Micro-Services**: Not intended to replace low-latency service-to-service communication.
- **Plugin Dependency**: Complex logic depends on the availability and maturity of specific Kestra plugins.

## When to use it
- You want to manage your workflows as code using a declarative YAML format.
- You need a unified platform that handles both data pipelines and infrastructure tasks.
- You require high visibility and a user-friendly UI for operations and monitoring.
- You want to build event-driven agentic systems using FastMCP 3.1.

## When not to use it
- For ultra-low latency request/response handling (use a dedicated API framework).
- If your team strictly requires a code-only (e.g., pure Python) orchestration library without a central server.
- For simple, isolated scripts where the overhead of a platform isn't justified.

## Workflow Sequence Diagram

```
+---------------+           +--------------------+          +--------------------+          +--------------------+
| Event / Agent |           | Kestra Server UI   |          | Task Executor Pool |          | FastMCP 3.1 Server |
+-------+-------+           +---------+----------+          +---------+----------+          +---------+----------+
        |                             |                               |                               |
        | 1. Trigger Flow Execution   |                               |                               |
        +---------------------------->|                               |                               |
        |                             | 2. Parse YAML & Evaluate DAG  |                               |
        |                             +------------------+            |                               |
        |                             |                  |            |                               |
        |                             |<-----------------+            |                               |
        |                             |                               |                               |
        |                             | 3. Dispatch Task Payload      |                               |
        |                             +------------------------------>|                               |
        |                             |                               | 4. Invoke MCP Agent Tool Call |
        |                             |                               +------------------------------>|
        |                             |                               |                               |
        |                             |                               | 5. Tool Output Payload        |
        |                             |                               |<------------------------------+
        |                             | 6. Flow State Success/Log     |                               |
        |                             |<------------------------------+                               |
        | 7. Execution Finished API   |                               |                               |
        |<----------------------------+                               |                               |
```

## Production Systemd Deployment

Deploy Kestra as a systemd managed background daemon on Linux hosts:

```ini
[Unit]
Description=Kestra Declarative Workflow Server
Documentation=https://kestra.io/docs
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=kestra
Group=kestra
WorkingDirectory=/opt/kestra
ExecStart=/usr/bin/java -Dkestra.configuration=/etc/kestra/application.yml -jar /opt/kestra/kestra-server.jar server standalone
Restart=always
RestartSec=10s
Environment=KESTRA_CONFIGURATION=/etc/kestra/application.yml
LimitNOFILE=65536
ProtectSystem=full
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Reload and activate service daemon:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kestra
sudo systemctl status kestra
```

## Getting started

### Docker Compose
Run Kestra locally with a single command:

```bash
docker run --pull always -p 8080:8080 kestra/kestra:latest-full
```
Access the UI at `http://localhost:8080`.

### Hello World Flow
Create a new flow in the UI:
```yaml
id: hello_world
namespace: dev

tasks:
  - id: log
    type: io.kestra.plugin.core.log.Log
    message: Hello from Kestra 2026!

  - id: python_script
    type: io.kestra.plugin.scripts.python.Script
    script: |
      import sys
      print(f"Python version: {sys.version}")
```

## CLI examples
The `kestra` CLI allows for flow validation and deployment.

```bash
# Validate a flow locally
kestra flow validate my_flow.yaml

# Create or update a flow from the CLI
kestra flow create dev my_flow.yaml

# Execute a flow and follow the logs
kestra flow execute dev hello_world --follow

# List all flows in a namespace
kestra flow list dev
```

## API examples
Kestra provides a REST API for programmatic interaction.

### FastMCP 3.1 Kestra Flow Orchestrator Tool Server
The Python snippet below implements a **FastMCP 3.1** tool server that exposes Kestra flow execution and status tracking endpoints directly to AI agents with strict **Pydantic v2** parameters:

```python
import os
import json
import httpx
from typing import Optional
from fastmcp import FastMCP, Context
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError

mcp = FastMCP("kestra-workflow-orchestrator")

KESTRA_API_URL = os.getenv("KESTRA_API_URL", "http://127.0.0.1:8080/api/v1")

class ExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    namespace: str = Field("dev", description="Target Kestra namespace")
    flow_id: str = Field(..., description="Target flow identifier")
    inputs: dict = Field(default_factory=dict, description="Execution input parameters")

    @field_validator("flow_id")
    @classmethod
    def validate_flow_id(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError("flow_id must be a valid alphanumeric identifier")
        return v

@mcp.tool()
async def trigger_kestra_workflow(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> str:
    """Trigger a Kestra declarative flow execution programmatically."""
    if ctx:
        await ctx.info("Validating ExecutionRequest schema with Pydantic v2...")

    try:
        req = ExecutionRequest.model_validate(request_dict)
        url = f"{KESTRA_API_URL}/executions/{req.namespace}/{req.flow_id}"

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=req.inputs, timeout=5.0)
            if resp.status_code in (200, 201):
                data = resp.json()
                return json.dumps({
                    "execution_id": data.get("id"),
                    "state": data.get("state", {}).get("current"),
                    "status": "SUCCESS"
                })
            return json.dumps({"status": "FAILED", "code": resp.status_code, "text": resp.text})
    except ValidationError as ve:
        if ctx:
            await ctx.error(f"Validation error: {ve}")
        return json.dumps({"status": "VALIDATION_ERROR", "error": str(ve)})
    except Exception as e:
        return json.dumps({"status": "ERROR", "error": str(e)})

if __name__ == "__main__":
    mcp.run()
```

### Flow Validation with Strict Pydantic v2 Schema
The following robust Python example uses **Pydantic v2** to programmatically validate the parameters and task configuration schema of a Kestra flow before executing it, ensuring runtime compliance.

```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

# 1. Define strict Pydantic v2 schemas for Kestra flow elements
class KestraTask(BaseModel):
    id: str = Field(..., min_length=2, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    type: str = Field(..., min_length=5)
    message: Optional[str] = None
    script: Optional[str] = None

class KestraFlow(BaseModel):
    id: str = Field(..., min_length=2, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    namespace: str = Field(..., min_length=2, pattern="^[a-zA-Z0-9_.]+$")
    description: Optional[str] = Field(None, max_length=200)
    tasks: List[KestraTask] = Field(..., min_items=1)

    @model_validator(mode="after")
    def validate_task_types(self) -> "KestraFlow":
        # Check that all tasks have a valid type namespace prefix
        for task in self.tasks:
            if not task.type.startswith("io.kestra.plugin."):
                raise ValueError(f"Task with id '{task.id}' must use a valid Kestra plugin namespace (starting with 'io.kestra.plugin.')")
        return self

# 2. Example representation of a YAML-to-JSON flow definition
flow_payload = {
    "id": "agent_feedback_loop",
    "namespace": "ai_ops",
    "description": "Continuous log auditing loop with Claude 5.1 and GPT-5.5.",
    "tasks": [
        {
            "id": "analyze_logs",
            "type": "io.kestra.plugin.core.log.Log",
            "message": "Analyzing system logs with GPT-5.5 via FastMCP 3.1..."
        },
        {
            "id": "python_agent_step",
            "type": "io.kestra.plugin.scripts.python.Script",
            "script": "print('Agent response successfully verified.')"
        }
    ]
}

# 3. Validate flow config using Pydantic v2
try:
    flow = KestraFlow.model_validate(flow_payload)
    print("Kestra Flow configuration successfully verified!")
    print(f"Flow ID: {flow.id}")
    print(f"Total tasks to execute: {len(flow.tasks)}")
except ValidationError as e:
    print(f"Validation failed with errors: {e.json()}")
```

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Probable Cause | Recommended Resolution |
| :--- | :--- | :--- |
| **`FlowNotFoundException`** | Flow ID or namespace mismatch in execution request. | Verify flow exists using `kestra flow list <namespace>` via CLI or UI. |
| **`ScriptRunnerException`** | Docker or Python script task failed due to missing binary or image. | Confirm task container image has pre-installed runtime dependencies. |
| **Database Connection Failure** | PostgreSQL backend unreachable or connection pool exhausted. | Increase `kestra.jdbc.postgres.maximum-pool-size` in `/etc/kestra/application.yml`. |
| **FastMCP Tool Timeout** | Agentic task exceeded execution timeout limit. | Set `timeout` parameter explicitly on the task in Kestra YAML flow schema. |

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — The Python-based alternative.
- [Dagster](dagster.md) — Asset-centric data orchestration.
- [Prefect](prefect.md) — Dynamic Python workflows.
- [Argo Workflows](argo-workflows.md) — Kubernetes-native orchestration.
- [Flyte](flyte.md) — Kubernetes-native ML orchestration.
- [ZenML](zenml.md) — MLStack integration and experiment tracking.
- [Temporal](temporal.md) — Durable execution for complex workflows.
- [n8n](../../services/n8n.md) — Low-code visual automation.
- [LiteLLM](../../services/litellm.md) — For AI task integration within flows.
- [MCP](../automation_orchestration/mcp.md) — For extending Kestra with agentic tools.
- [Claude 5.1](../ai_knowledge/claude-mythos.md) — Frontier model for workflow reasoning.
- [GPT-5.5](../ai_knowledge/chatgpt.md) — Frontier reasoning model.
- [Gemini 4.0 Pro](../ai_knowledge/gemini-macos.md) — High-performance model.
- [Llama 4](../ai_knowledge/llama.md) — Next-generation open model.
- [Gemma 3](../ai_knowledge/gemma.md) — Lightweight model for task logic.
- [Qwen 3.6](../ai_knowledge/qwen.md) — Standard open reasoning model.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — SOTA communication protocol.

## Production Operational Best Practices
- **GitOps Flow Management**: Store all YAML flow definitions in a Git repository and use Kestra's CI/CD GitHub Action or CLI `kestra flow create` commands to deploy updates automatically upon pull request approval.
- **Resource Limits**: Enforce strict CPU and memory resource bounds on Docker and Kubernetes task runners to prevent runaway Python scripts from overwhelming the control plane.
- **Secrets Management**: Integrate Kestra with HashiCorp Vault or AWS Secrets Manager rather than embedding API keys directly in YAML task environment parameters.

## Sources / references
- [Kestra Official Documentation](https://kestra.io/docs)
- [Kestra v0.20 Release Notes](https://kestra.io/blog/release-0-20)
- [GitHub: Kestra Core](https://github.com/kestra-io/kestra)
- [Kestra MCP Server Integration Guide](https://kestra.io/docs/how-to-guides/mcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
