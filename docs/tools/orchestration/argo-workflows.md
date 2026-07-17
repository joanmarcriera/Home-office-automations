# Argo Workflows

## What it is
Argo Workflows is an open-source, container-native workflow engine for orchestrating parallel jobs on Kubernetes. It is implemented as a Kubernetes Custom Resource Definition (CRD), allowing for native integration with the K8s ecosystem. As of July 2026, **v4.0.8** is the stable release, featuring **GRPC-based Pluggable Artifact Drivers**, dynamic parallelism updates via ConfigMaps without controller restarts, server-side CEL (Common Expression Language) validations, and native Model Context Protocol (MCP 3.0) client/server tasks.
- **Licensing**: Apache License 2.0 (Open Source)
- **Cost**: Free
- **Self-hostable**: Yes (CNCF Graduated Project)

## What problem it solves
Argo Workflows brings powerful, containerized orchestration to Kubernetes, solving the complexity of managing parallel, multi-step pipelines. Each task runs in its own isolated container, which eliminates "dependency hell" and allows for massive scalability. It enables developers to define complex workflows using YAML (or Python via Hera) that are fully integrated with Kubernetes' resource management and security models.

## Where it fits in the stack
**Orchestration / Kubernetes-Native Workflow Engine**. It serves as the backbone for container-native pipelines on K3s, EKS, GKE, and on-premise Kubernetes clusters, orchestrating agentic workflows and large-scale data/model workloads.

## Typical use cases
- **Machine Learning & AI Agent Pipelines**: Coordinating high-performance data preprocessing, GPU-accelerated model training, and batch evaluation utilizing Gemma 3 and Claude 5.1 models.
- **Parallel Agent Reasoning Workflows**: Running multi-step reasoning steps in parallel containers and compiling the results using agentic orchestration.
- **CI/CD Workflows**: Running multi-stage builds, automated testing, and secure deployments in isolated environments.
- **Data Processing (ETL)**: Orchestrating large-scale batch processing and data transformation tasks using K8s native scaling.
- **Infrastructure Automation**: Automating the lifecycle of cloud-resources and Kubernetes components via GitOps (Argo CD integration).

## Strengths
- **Kubernetes-Native**: Deeply integrated with K8s RBAC, namespaces, and resource quotas; fits perfectly into GitOps workflows.
- **Massive Parallelism**: Orchestrates thousands of concurrent containers, limited only by cluster capacity.
- **v4.0 Features**: Extensible Artifact Plugins (GRPC-based), dynamic parallelism (update global limits via ConfigMap without restarts), and server-side CEL validations.
- **Agentic Orchestration**: Native integration with MCP 3.0 Task Protocol for calling external tools and LLM endpoints securely from inside workflow steps.
- **Python-Friendly**: Excellent support for the [Hera Python SDK](https://github.com/argoproj-labs/hera), allowing for complex logic and programmatic DAGs without "YAML soup."
- **Observability**: Robust UI for visualizing workflow execution, logs, and artifact lineage in real-time.

## Limitations
- **Kubernetes Dependency**: Cannot run standalone; requires a functioning Kubernetes cluster (even a local K3s/Kind instance).
- **YAML Complexity**: Large workflows can become difficult to manage in pure YAML, though Hera mitigates this.
- **Overhead**: Container startup latency makes it less suitable for ultra-low-latency, real-time request/response workflows.

## When to use it
- Your infrastructure is already Kubernetes-centric.
- You need to run complex, containerized tasks with specific resource requirements (e.g., GPU, high memory).
- You want a GitOps-compatible way to manage your workflows using tools like Argo CD.
- You are building large-scale ML or agentic data pipelines that require container-level isolation.

## When not to use it
- You do not use Kubernetes and want a lightweight, single-server solution (consider [Prefect](prefect.md) or [n8n](../../services/n8n.md)).
- You need a simple, single-file script orchestrator with minimal overhead (consider [Hamilton](apache-hamilton.md)).
- Your workflows are mostly interactive or involve frequent manual human-in-the-loop steps better suited for [Temporal](temporal.md).

## Getting started

### Quickstart Installation
Deploy the Argo Workflows controller and UI to your K3s or development cluster:

```bash
# Create namespace and install
kubectl create namespace argo
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v4.0.8/install.yaml

# Patch the server to use 'server' auth mode for local development
kubectl patch deployment argo-server -n argo --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/args", "value": ["server", "--auth-mode=server"]}]'
```

### Submit a Hello World Workflow
```bash
cat <<EOF > hello.yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: hello-world-
spec:
  entrypoint: whalesay
  templates:
  - name: whalesay
    container:
      image: docker/whalesay:latest
      command: [cowsay]
      args: ["hello world"]
EOF

argo submit -n argo hello.yaml --watch
```

## CLI examples
The `argo` CLI is the primary management tool for workflows, cron jobs, and native MCP 3.0 integrations.

```bash
# List workflows in the 'argo' namespace
argo list -n argo

# Get logs for a specific workflow (supports follow)
argo logs -n argo hello-world-xxxxx -f

# Suspend/Resume a running workflow
argo suspend -n argo my-workflow
argo resume -n argo my-workflow

# Delete completed workflows to free up cluster resources
argo delete -n argo --status Completed

# Watch the progress of a specific workflow
argo watch -n argo hello-world-xxxxx

# Register an MCP 3.0 server tool with Argo Workflows
argo mcp register --name "k8s-ops" --command "mcp-server-k8s" --args=["--namespace", "argo"]
```

## API examples
Argo Server provides a robust REST API (gRPC and HTTP) and first-class programmatic interfaces via Python SDKs.

### 1. Hera Python SDK Parallel Agent Reasoning Workflow
The following Hera Python SDK example defines a workflow that orchestrates parallel agent reasoning tasks using Claude 5.1:

```python
from hera.workflows import DAG, Task, Workflow, Container

def run_agent_reasoning():
    # Define a reusable container for agent tasks
    agent_image = "rag-agent-claude:latest"

    with Workflow(generate_name="agent-reasoning-", entrypoint="d") as w:
        with DAG(name="d"):
            # Task to generate sub-queries
            plan = Task(
                name="generate-plan",
                image=agent_image,
                command=["python", "agent.py"],
                args=["--action", "plan", "--query", "Optimize K3s cluster performance"]
            )

            # Parallel reasoning steps across different indices
            reason_step_1 = Task(
                name="reason-infrastructure",
                image=agent_image,
                command=["python", "agent.py"],
                args=["--action", "reason", "--domain", "infrastructure"]
            )
            reason_step_2 = Task(
                name="reason-storage",
                image=agent_image,
                command=["python", "agent.py"],
                args=["--action", "reason", "--domain", "storage"]
            )

            # Final compile step
            compile_results = Task(
                name="compile-results",
                image=agent_image,
                command=["python", "agent.py"],
                args=["--action", "compile"]
            )

            # Establish dependencies
            plan >> [reason_step_1, reason_step_2] >> compile_results

    w.create()

if __name__ == "__main__":
    run_agent_reasoning()
```

### 2. Submit a Workflow via API (REST)
```bash
# Submit a workflow using REST API endpoint
curl -X POST "https://argo-server:2746/api/v1/workflows/argo" \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d @hello.json -k
```

## Related tools / concepts
- [Argo CD](https://argoproj.github.io/argo-cd/) — For GitOps-based deployment of workflows.
- [Hera Python SDK](https://github.com/argoproj-labs/hera) — The standard for building Argo workflows in Python.
- [K3s](../infrastructure/k3s.md) — A lightweight Kubernetes distribution ideal for running Argo locally.
- [Supabase](../infrastructure/supabase.md) — Vector search database for embedding storage.
- [Apache Airflow](apache-airflow.md) — For enterprise-wide batch scheduling (often integrated with Argo).
- [Flyte](flyte.md) — A container-native orchestrator focused on ML lifecycle.
- [Kestra](kestra.md) — For event-driven declarative orchestration.
- [Temporal](temporal.md) — For stateful, durable workflows with long-running state.
- [Dagster](dagster.md) — Data orchestrator with asset-based tracking and native July 2026 standards.
- [Prefect](prefect.md) — Highly flexible Pythonic orchestrator for rapid deployments.
- [ZenML](zenml.md) — Swappable experiment tracking and MLStack management.
- [Hamilton](apache-hamilton.md) — Lightweight micro-orchestrator for code and data pipelines.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open standard for agentic context integration.
- [Claude Mythos](../ai_knowledge/claude-mythos.md) — Technical details of modern Claude model orchestration.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Data framework for connecting custom data sources to LLMs.
- [Open Interpreter](../automation_orchestration/open-interpreter.md) — Natural language interface for running code locally.

## Sources / References
- [Argo Workflows Official Documentation](https://argoproj.github.io/argo-workflows/)
- [GitHub: Argo Workflows](https://github.com/argoproj/argo-workflows)
- [Hera: Argo Workflows Python SDK](https://github.com/argoproj-labs/hera)
- [Argo Workflows v4.0.8 Release Notes](https://github.com/argoproj/argo-workflows/releases/tag/v4.0.8)
- [Argo Workflows endoflife.date](https://endoflife.date/argo-workflows)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
