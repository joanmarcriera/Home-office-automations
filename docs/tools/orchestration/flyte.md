# Flyte

Flyte is an open-source, container-native workflow orchestrator built on Kubernetes, specifically designed for machine learning and data processing at scale. As of July 2026, **Flyte 2.x** is the stable major release, featuring a reimagined Python SDK, native async support, and deep integration with the **MCP 3.0** Task Protocol for agentic orchestration.

## What it is
Flyte is a container-native orchestrator that manages the execution of complex ML and data workflows on Kubernetes. It ensures that every task is isolated, versioned, and reproducible, making it ideal for large-scale AI platforms. It provides a strongly-typed interface that allows for safe and predictable workflow execution across heterogeneous compute resources.

## What problem it solves
It solves the challenges of reproducibility, scalability, and maintainability in ML pipelines. Flyte ensures that infrastructure (like GPUs) is provisioned dynamically and that workflows can scale to thousands of containers. In July 2026, Flyte addresses the "Agentic Loop" problem by allowing [Claude 5.1](../../tools/ai_knowledge/claude-macos.md) or [Gemma 3](../../tools/ai_knowledge/gemini-macos.md) to dynamically steer containerized tasks via [MCP 3.0](../automation_orchestration/mcp.md) integration.

## Where it fits in the stack
**Orchestration / ML Platform**. It acts as the backbone for large-scale AI and data platforms, sitting on top of Kubernetes. It coordinates between data storage, compute resources (CPU/GPU), and model registries. It is often used alongside [ZenML](zenml.md) for experiment tracking and [NVIDIA](../providers/nvidia.md) for hardware-accelerated training.

## Typical use cases
- **Large-Scale ML Training**: Orchestrating distributed training jobs across hundreds of GPUs (including NVIDIA H100/B200 support).
- **Agentic Workflows**: Building self-healing AI systems that make dynamic decisions at runtime based on containerized agent execution using [MCP 3.0](../automation_orchestration/mcp.md).
- **Data Engineering**: Running complex ETL pipelines with strong type safety and task-level caching.
- **Bioinformatics**: Processing massive datasets with strict auditability and reproducibility requirements.

## Strengths
- **Flyte 2.x SDK**: An intuitive, Pythonic API that supports `asyncio` for parallelism and standard `try-except` for error handling.
- **MCP 3.0 Native**: Built-in support for the Model Context Protocol, allowing Flyte workflows to be exposed as tools to AI agents.
- **Strong Typing**: Interfaces are strictly typed, catching errors at registration-time rather than runtime.
- **Dynamic Infrastructure**: Fine-grained resource allocation (CPU, Mem, GPU) per task.
- **Reproducibility**: Every execution is versioned and reproducible, with built-in task-level caching.

## Limitations
- **Kubernetes Native**: Requires a K8s cluster for full production features, which adds operational complexity.
- **Learning Curve**: The concept of strongly-typed workflows and registration can be unfamiliar to users used to imperative scripts.
- **Platform Overhead**: Managing a full Flyte installation requires dedicated DevOps effort for the control plane.

## When to use it
- You are building production-grade ML pipelines that need to scale to thousands of containers.
- You require strict reproducibility and auditability of your data and model versions.
- You want to leverage Kubernetes' resource management for heterogeneous workloads (CPU vs. GPU).
- You are executing containerized AI agents that require strict isolation and [MCP 3.0](../automation_orchestration/mcp.md) compliance.

## When not to use it
- For simple, lightweight automation where a single machine or a basic orchestrator is sufficient.
- If you don't have access to or the expertise to manage a Kubernetes cluster (see [Invisible Kubernetes](../../knowledge_base/invisible_kubernetes.md)).
- For low-latency request/response handling.

## Getting started

### Flyte Devbox (Local)
The Devbox provides a full Flyte backend and UI on your local machine:

```bash
# Install the Flyte CLI
curl -sL https://ctl.flyte.org/install | bash

# Start the Devbox
flyte dev start
```
Access the UI at `http://localhost:3000`.

### Basic Flyte 2.x Example
```python
import flyte

# Define an environment
env = flyte.TaskEnvironment(name="my_env")

@env.task
async def greet(name: str) -> str:
    return f"Hello, {name}!"

@env.task
async def main(name: str) -> str:
    message = await greet(name)
    return message.upper()

if __name__ == "__main__":
    flyte.init_from_config()
    result = flyte.run(main, name="Flyte 2.x")
    print(result.wait())
```

## CLI examples
The `flyte` CLI manages tasks, workflows, and executions.

```bash
# Register an app to the backend
flyte register my_app.py --project my_project --domain development

# Execute a workflow on the cluster
flyte run my_app.py main --name "Production Run"

# List executions in a project
flyte list execution --project my_project --domain development

# Register Flyte tasks as MCP tools (July 2026)
flyte mcp register --project my_project --domain development --workflow main
```

## API examples
Flyte 2.x exposes a gRPC and REST API for programmatic interaction.

```bash
# Health check via REST
curl -X GET "http://flyte-admin:8088/api/v1/health"

# List projects via API
curl -X GET "http://flyte-admin:8088/api/v1/projects"
```

**Executing an Agentic Task (July 2026):**
```python
from flyte import task, workflow
from mcp.client import MCPClient

@task
def agent_reasoning(task_input: str) -> str:
    # Interaction with a July 2026 agent (e.g., Claude 5.1) via MCP
    client = MCPClient(url="http://mcp-server:8000")
    response = client.call_tool("analyze", {"input": task_input})
    return response.content

@workflow
def agent_workflow(input_data: str) -> str:
    return agent_reasoning(task_input=input_data)
```

## Related tools / concepts
- [Argo Workflows](argo-workflows.md) — The underlying workflow engine often compared with Flyte.
- [Apache Airflow](apache-airflow.md) — For general-purpose batch orchestration.
- [Dagster](dagster.md) — For asset-centric data orchestration.
- [ZenML](zenml.md) — MLStack integration and experiment tracking.
- [NVIDIA](../providers/nvidia.md) — Flyte has first-class support for H100/B200 GPUs.
- [MCP](../automation_orchestration/mcp.md) — The protocol used to extend Flyte with agentic tools.
- [Claude 5.1](../../tools/ai_knowledge/claude-macos.md) — Frontier model for orchestrating Flyte tasks.
- [Gemma 3](../../tools/ai_knowledge/gemini-macos.md) — Lightweight model for task-level logic.
- [Invisible Kubernetes](../../knowledge_base/invisible_kubernetes.md) — Simplifies K8s management for Flyte.
- [OpenTelemetry Collector](../process_understanding/opentelemetry-collector.md) — For tracing Flyte executions.
- [Prefect](prefect.md) — Alternative Python-native orchestrator.

## Sources / references
- [Flyte Official Documentation](https://docs.flyte.org/)
- [Union.ai: Flyte 2.x Migration and MCP Guide](https://www.union.ai/docs/v2/flyte/user-guide/mcp-integration)
- [GitHub Repository](https://github.com/flyteorg/flyte)
- [Flyte MCP 3.0 Specification](https://flyte.org/mcp)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
