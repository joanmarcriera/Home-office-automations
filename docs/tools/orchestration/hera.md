# Hera Python SDK

## What it is
Hera (Hera Workflows) is an open-source, strongly-typed Python SDK for **Argo Workflows**. It allows data engineers, MLOps practitioners, and developers to construct, validate, and submit complex Kubernetes-native workflows using pure Python instead of writing verbose Kubernetes YAML manifests.

## What problem it solves
Argo Workflows is a powerful Kubernetes-native workflow engine, but defining workflows directly in YAML manifests can be repetitive, error-prone, and difficult to test or integrate into Python-centric data pipelines. Hera solves this problem by providing a Pythonic abstraction that enables programmatic workflow creation with type safety, IDE autocompletion, reusable function decorators, and direct submission to Argo Server REST APIs.

## Where it fits in the stack
**Orchestration / Workflow Engine SDK**. It operates as the developer-facing SDK layer on top of Argo Workflows, translating Python code into Argo Custom Resource Definitions (CRDs) or submitting workflow specs to Kubernetes clusters.

## Typical use cases
- **ML & AI Pipelines**: Programmatically orchestrating multi-step LLM fine-tuning, embedding generation, and model evaluation pipelines on Kubernetes.
- **Dynamic Workflow Generation**: Creating dynamic directed acyclic graphs (DAGs) whose step execution paths depend on runtime data or configuration files.
- **Data Engineering ETL**: Building reproducible containerized data ingestion, transformation, and batch processing pipelines using Python.

## Strengths
- **Pythonic Interface**: Defines workflows using standard Python functions, decorators, and context managers.
- **Strong Typing**: Leverages Pydantic and type annotations to catch configuration errors before submitting workflows to the cluster.
- **Direct Submission**: Submits workflows directly to the Argo Server REST API or exports them as native YAML manifests.
- **Feature Parity**: Supports advanced Argo features including DAGs, steps, loops, memoization, volume mounts, metrics, and artifact management.

## Limitations
- **Argo Workflows Dependency**: Requires an operational Argo Workflows controller running on a Kubernetes cluster.
- **Abstraction Overhead**: Advanced or brand-new Argo Custom Resource features may occasionally lag behind raw YAML CRD spec releases.

## When to use it
- When your team prefers writing maintainable, version-controlled Python code rather than managing large Kubernetes YAML files.
- For MLOps or data pipelines where workflow tasks and parameters are dynamically computed at runtime.
- When building Python applications that programmatically trigger or monitor containerized jobs on Kubernetes.

## When not to use it
- If your team is not using Argo Workflows (e.g., using Prefect, Dagster, or Apache Airflow).
- For non-Kubernetes workloads or simple single-node script executions.

## Getting started

### Installation
Install the Hera Workflows SDK via pip:

```bash
pip install hera-workflows
```

### Basic DAG Example
Define and submit a workflow containing dependent tasks:

```python
from hera.workflows import DAG, Script, Workflow

def say_hello(name: str):
    print(f"Hello, {name}!")

def build_report():
    print("Generating workflow report...")

with Workflow(
    generate_name="hera-demo-",
    entrypoint="dags",
) as w:
    with DAG(name="dags"):
        t1 = Script(name="hello-task", source=say_hello, inputs={"name": "Argo"})
        t2 = Script(name="report-task", source=build_report)
        t1 >> t2  # Define dependency: t1 runs before t2

# Print the resulting Kubernetes YAML spec
print(w.to_yaml())
```

## CLI examples
```bash
# Generating Argo Workflow YAML from a Hera Python script via CLI
python my_hera_workflow.py > workflow.yaml

# Submitting generated YAML to Kubernetes using kubectl or argo CLI
argo submit -n argo workflow.yaml --watch
```

## API examples
```python
# Submitting a workflow directly to Argo Server via Hera API
from hera.shared import global_config
from hera.workflows import Workflow, Container

global_config.host = "https://argo.mycompany.org"
global_config.token = "YOUR_ARGO_SERVER_TOKEN"

w = Workflow(
    name="container-job",
    entrypoint="whalesay",
)
c = Container(
    name="whalesay",
    image="docker/whalesay:latest",
    command=["cowsay"],
    args=["Hera simplifies Argo Workflows!"],
)
w.add_child(c)

# Create and submit the workflow directly to Argo Server
w.create()
```

## Related tools / concepts
- **[Argo Workflows](argo-workflows.md)**: Kubernetes-native workflow orchestration engine.
- **[Kubectl](argo-workflows.md)**: Kubernetes command-line management tool.
- **[Prefect](prefect.md)**: Modern Python data workflow orchestration platform.

## Sources / references
- [Hera GitHub Repository](https://github.com/argoproj-labs/hera?ref=2026-09-21-audit)
- [Hera Documentation](https://hera.readthedocs.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
