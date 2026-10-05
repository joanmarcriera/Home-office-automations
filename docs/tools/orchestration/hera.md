# Hera Python SDK

## What it is
Hera (Hera Workflows) is an open-source, strongly-typed Python SDK for **Argo Workflows**. It empowers data engineers, MLOps architects, and software developers to construct, validate, programmatically compile, and submit complex Kubernetes-native workflows using pure Python code instead of managing thousands of lines of raw Kubernetes YAML Custom Resource Definitions (CRDs). As of early 2027, Hera has integrated first-class support for **Model Context Protocol (FastMCP 3.1)** task servers, enabling autonomous agents running frontier models (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, and **DeepSeek-V4**) to dynamically spawn, monitor, and manage containerized DAG execution pipelines directly on Kubernetes.

```
+-----------------------------------------------------------------------------------+
|                        PYTHON APPLICATION / AGENT RUNTIME                         |
|                                                                                   |
|  +------------------------+   +-----------------------+   +--------------------+  |
|  |   Hera Python SDK      |   | FastMCP 3.1 Server    |   | Pydantic v2 Schema |  |
|  |   (Typed DAG Builder)  |   | (Tool Execution Bus)  |   | Validation Engine  |  |
|  +-----------+------------+   +-----------+-----------+   +---------+----------+  |
|              |                            |                         |             |
|              +----------------------------+-------------------------+             |
|                                           |                                       |
|                                           v                                       |
|  +-----------------------------------------------------------------------------+  |
|  |                       COMPILATION & SUBMISSION ENGINE                       |  |
|  |       Offline YAML Compiler      |       Argo REST / gRPC API Client       |  |
|  +--------------------------------------+--------------------------------------+  |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------+-----------------------------------------+
|                  KUBERNETES CLUSTER / ARGO WORKFLOW CONTROLLER                    |
|                                                                                   |
|  +-----------------------+      +------------------------+     +----------------+ |
|  | Workflow CRD Manifest |      | Container Task Pods    |     | Volume Claims  | |
|  | (Generated Spec)      |      | (DAG Step Execution)   |     | & Artifacts    | |
|  +-----------------------+      +------------------------+     +----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Argo Workflows is a highly capable, battle-tested Kubernetes-native engine for orchestrating parallel containerized tasks. However, defining complex pipelines directly in Kubernetes YAML CRDs introduces significant operational friction:

1. **YAML Verbosity & Maintenance Fatigue**: Production Argo workflows routinely span thousands of lines of YAML. Modifying nested step parameters or adding conditional branches is error-prone and tedious. Hera provides a clean, modular Python API with IDE autocompletion and type checking.
2. **Lack of Dynamic Pipeline Generation**: Statically defined YAML manifests cannot easily adapt to dynamic runtime parameters (e.g., dynamically varying numbers of dataset chunks or agentic sub-task decompositions). Hera allows building DAG topologies programmatically in standard Python loops (`for item in dataset:`).
3. **Integration Obstacles for AI Agents**: Autonomous agents cannot easily author or validate raw Kubernetes manifests safely. Hera abstracts Argo Workflows into strongly-typed Pydantic models and Python objects that agents can safely manipulate via FastMCP 3.1 tool interfaces.
4. **Testing and CI/CD Validation Bottlenecks**: Validating Argo YAML requires submitting it to a live Kubernetes cluster or running external linter binaries. Hera performs client-side schema validation during python compilation before sending payloads over the wire.

## Where it fits in the stack
**Orchestration / Workflow Engine SDK**. Hera functions as the developer SDK interface sitting directly above Argo Workflows:

- **Application / Agent Layer**: Sits beneath AI agent frameworks ([Ag2](../frameworks/ag2.md), [Smolagents](../frameworks/smolagents.md), [LangGraph](../frameworks/langgraph.md)) and FastMCP 3.1 task protocol servers.
- **Orchestration Layer**: Translates Python code into valid Kubernetes Argo Custom Resources (`Workflow`, `WorkflowTemplate`, `CronWorkflow`).
- **Infrastructure Layer**: Submits compiled specs to [K3s clusters](../infrastructure/k3s.md) or production Kubernetes environments hosting the Argo Workflows Controller and [Docker](../infrastructure/docker.md) container runtimes.

## Typical use cases
- **Multi-Node Distributed Model Fine-Tuning**: Orchestrating GPU data preparation, distributed LoRA/QLoRA fine-tuning steps, model evaluations, and registry pushes on Kubernetes clusters.
- **Dynamic Agentic Task Decomposition**: Programmatically converting a high-level goal generated by an LLM into a multi-step Kubernetes DAG containing parallel analysis tasks.
- **Scalable Data Ingestion & ETL**: Constructing containerized data extraction, document parsing, chunking, and embedding pipelines with volume mounts and artifact passing.
- **Automated CI/CD Test Matrix Execution**: Spawning isolated container pods in parallel to test software packages across multiple Python versions and Linux distributions.

## Strengths
- **Pure Python Syntax & IDE Support**: Construct workflows using standard Python functions, context managers (`with Workflow(...)`), and type annotations.
- **Client-Side Type Safety & Pydantic Integration**: Validates task parameters, volume claim configs, and step dependencies prior to API submission.
- **Direct REST API & YAML Manifest Generation**: Supports both direct programmatic submission via Argo Server REST APIs and offline compilation to native Argo YAML files.
- **Full Feature Parity with Argo CRDs**: Supports DAGs, Steps, parallel loops (`with_items`), memoization, volume claims, exit handlers, and metric emitters.

## Limitations
- **Requires Active Argo Workflows Infrastructure**: Tied directly to Kubernetes clusters running the Argo Workflows Controller.
- **Sub-Second Real-Time Task Latency**: Not designed for microsecond real-time streaming tasks; container creation overhead incurs pod startup latency (seconds).
- **CRD Propagation Lag**: Newly released cutting-edge features in Argo Workflows CRD specs may experience a short delay before being exposed in Hera Python bindings.

## When to use it
- When your team prefers writing maintainable, testable Python code over authoring and managing massive Kubernetes YAML manifests.
- When workflow DAG topologies, parallel step counts, or task parameters must be dynamically constructed at runtime by software code or AI agents.
- When building FastMCP 3.1 tools that programmatically trigger, inspect, and cancel Kubernetes container jobs.

## When not to use it
- If your stack relies on non-Kubernetes workflow orchestrators (such as Prefect, Dagster, or Apache Airflow) without Argo Workflows.
- For simple local single-process task scheduling where simple Python scripts or cron jobs are sufficient.

## Getting started

### Installation
Install the Hera Workflows SDK via pip:

```bash
pip install hera-workflows fastmcp pydantic
```

### Basic DAG Definition & YAML Compilation Example
Define a workflow with dependent script tasks and print the compiled Kubernetes YAML manifest:

```python
from hera.workflows import DAG, Script, Workflow

def extract_data(source_id: str):
    print(f"Extracting data from source: {source_id}")

def process_data():
    print("Processing extracted data in container...")

with Workflow(
    generate_name="hera-etl-pipeline-",
    entrypoint="main-dag",
) as w:
    with DAG(name="main-dag"):
        task1 = Script(name="extract-task", source=extract_data, inputs={"source_id": "s3-bucket-2027"})
        task2 = Script(name="process-task", source=process_data)
        task1 >> task2  # Set execution dependency: task1 must finish before task2 starts

# Output compiled Kubernetes Argo Workflow YAML manifest
print(w.to_yaml())
```

## CLI examples

```bash
# Export Hera workflow script to native Argo Workflow YAML manifest
python my_hera_pipeline.py > argo_workflow.yaml

# Submit generated workflow manifest using Argo CLI
argo submit -n argo argo_workflow.yaml --watch

# List running Argo workflows in the cluster
argo list -n argo
```

## API examples

### Python FastMCP 3.1 & Pydantic v2 Hera Submission Server
The following code snippet demonstrates submitting Argo Workflows programmatically via Hera inside a FastMCP 3.1 server with Pydantic v2 validation schemas:

```python
import os
import logging
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from hera.shared import global_config
from hera.workflows import Workflow, Container, DAG
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hera_mcp_server")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    "Hera-Argo-Orchestrator",
    version="3.1.0",
    description="FastMCP 3.1 server for programmatically creating & submitting Argo Workflows using Hera"
)

# Pydantic v2 Schemas for Workflow Configuration
class ContainerTaskConfig(BaseModel):
    task_name: str = Field(..., description="Unique name of the container execution task.")
    image: str = Field(..., description="Docker/OCI container image to execute.")
    command: List[str] = Field(..., description="Entrypoint command list.")
    args: List[str] = Field(default_factory=list, description="Arguments passed to command.")
    depends_on: Optional[str] = Field(None, description="Optional name of prerequisite task that must finish first.")

class WorkflowSubmitRequestSchema(BaseModel):
    workflow_prefix: str = Field(..., min_length=3, max_length=63, description="Prefix for generated Kubernetes workflow instance name.")
    namespace: str = Field(default="argo", description="Target Kubernetes namespace.")
    tasks: List[ContainerTaskConfig] = Field(..., min_items=1, description="List of container tasks.")

class WorkflowSubmitResponseSchema(BaseModel):
    workflow_name: str = Field(..., description="Name of the submitted Argo workflow instance.")
    namespace: str = Field(..., description="Kubernetes namespace where workflow was spawned.")
    status: str = Field(..., description="Initial submission status.")
    total_tasks: int = Field(..., description="Number of tasks in the DAG.")

# Configure Hera global Argo Server settings
global_config.host = os.environ.get("ARGO_SERVER_URL", "https://argo.internal.domain:2746")
global_config.token = os.environ.get("ARGO_BEARER_TOKEN", "secret_token")

@mcp.tool()
def submit_container_dag(request_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Programmatically compiles and submits a multi-task container DAG workflow to Argo Workflows using Hera.
    """
    try:
        validated_req = WorkflowSubmitRequestSchema.model_validate(request_payload)
    except ValidationError as ve:
        return {"status": "validation_error", "errors": ve.errors()}

    try:
        # Construct Workflow using Hera Python SDK
        with Workflow(
            generate_name=f"{validated_req.workflow_prefix}-",
            namespace=validated_req.namespace,
            entrypoint="dag-entrypoint"
        ) as w:
            with DAG(name="dag-entrypoint"):
                task_map = {}
                for t_cfg in validated_req.tasks:
                    c_task = Container(
                        name=t_cfg.task_name,
                        image=t_cfg.image,
                        command=t_cfg.command,
                        args=t_cfg.args
                    )
                    task_map[t_cfg.task_name] = c_task

                    # Handle dependency chaining
                    if t_cfg.depends_on and t_cfg.depends_on in task_map:
                        task_map[t_cfg.depends_on] >> c_task

        # Submit directly to Argo Server REST API endpoint
        created_workflow = w.create()

        response_obj = WorkflowSubmitResponseSchema(
            workflow_name=created_workflow.metadata.name,
            namespace=validated_req.namespace,
            status="Submitted",
            total_tasks=len(validated_req.tasks)
        )

        return {
            "status": "success",
            "data": response_obj.model_dump(mode="json")
        }

    except Exception as e:
        logger.error(f"Hera workflow submission failed: {e}")
        return {"status": "submission_error", "message": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Python Test Harness
```python
def test_hera_validation():
    sample_request = {
        "workflow_prefix": "agent-etl-job",
        "namespace": "argo-jobs",
        "tasks": [
            {
                "task_name": "fetch-data",
                "image": "python:3.11-slim",
                "command": ["python", "-c"],
                "args": ["print('Fetching data...')"]
            },
            {
                "task_name": "process-data",
                "image": "python:3.11-slim",
                "command": ["python", "-c"],
                "args": ["print('Processing data...')"],
                "depends_on": "fetch-data"
            }
        ]
    }

    print("--- Simulating Hera FastMCP Request Validation ---")
    req = WorkflowSubmitRequestSchema.model_validate(sample_request)
    print(f"Workflow Prefix: {req.workflow_prefix} | Total Tasks: {len(req.tasks)}")
    print(f"Task 2 '{req.tasks[1].task_name}' depends on '{req.tasks[1].depends_on}'")

if __name__ == "__main__":
    test_hera_validation()
```

## Related tools / concepts
- [Argo Workflows](argo-workflows.md) — The underlying Kubernetes-native workflow execution engine.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Standardized tool connection bus interfacing agents with Hera SDK.
- [K3s](../infrastructure/k3s.md) — Lightweight Kubernetes cluster manager hosting Argo Workflows.
- [Docker](../infrastructure/docker.md) — Container runtime standard powering individual DAG task pods.
- [Dolt](../intake_storage/dolt.md) — Version-controlled relational database for storing workflow execution state.

## Sources / references
- [Hera GitHub Repository](https://github.com/argoproj-labs/hera)
- [Hera Official Documentation](https://hera.readthedocs.io/)
- [Argo Workflows Documentation](https://argo-workflows.readthedocs.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
