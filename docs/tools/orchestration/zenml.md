# ZenML

## What it is
ZenML is an open-source, extensible MLOps framework designed to create portable, production-ready AI pipelines and agentic workflows. It provides a standardized abstraction layer (the "Stack") that decouples pipeline logic from the underlying infrastructure. As of December 2026, **v1.2.x** is the stable release, featuring native **MLStack** management, robust **Experiment Tracking** integrations, and full support for the **Model Control Plane (FastMCP 3.1)** to empower multi-agent autonomous operations.

## What problem it solves
ZenML bridges the "production gap" and tackles tooling fragmentation in machine learning operations. It allows developers to write pipeline code once and run it anywhere—from a local machine to enterprise clusters like Kubernetes, Vertex AI, or AWS SageMaker. With its late 2026 **MLStack** and **Experiment Tracking** specifications, ZenML eliminates the complexity of manually coordinating orchestrators, artifact stores, and tracking backends (such as MLflow and Weights & Biases), ensuring absolute repeatability and strict metadata lineage for every model run.

## Where it fits in the stack
**Orchestration / MLOps Pipeline Framework**. It serves as the management and coordination layer that sits above specialized tools for data versioning, experiment tracking, and model registries. ZenML translates high-level pipeline declarations into target-specific execution steps while maintaining a unified control plane.

## Typical use cases
- **MLStack Experiment Tracking**: Integrating unified experiment tracking components (e.g., MLflow, Weights & Biases, or TensorBoard) into swappable stacks to monitor model parameters, training metrics, and artifacts automatically.
- **Agentic Workflows**: Orchestrating multi-stage AI agents (utilizing models like Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Gemma 3) that require durable state, observability, and structured execution across distributed environments.
- **Portable ML Pipelines**: Developing cloud-agnostic machine learning lifecycles that can be migrated between environments (local vs. cloud) without modifications to the core code.
- **Autonomous MLOps**: Enabling autonomous coding agents like Claude Code to independently inspect active stack configurations, run pipelines, and evaluate experiment metrics via FastMCP 3.1 tool interfaces.

## Strengths
- **Infrastructure Agnostic**: "Write once, run anywhere" across local compute, Kubernetes, Apache Airflow, Flyte, and cloud-native orchestrators.
- **Unified MLStack Concept**: First-class abstractions for modular stack components, making it simple to plug in and swap experiment trackers, model registries, and data validators.
- **Deep Experiment Tracking Integration**: Automated parameter logging, metrics tracking, and artifact lineage association through native SDK wrappers.
- **FastMCP 3.1 Compatibility**: Out-of-the-box Model Control Plane support, exposing active stacks, component statuses, and experiment logs as tools for agentic workflows.
- **Developer-Centric SDK**: Elegant, Pythonic decorators and a CLI that simplifies pipeline definition for data scientists and AI engineers alike.

## Limitations
- **Operational Setup**: While executing pipelines is straightforward, configuring and maintaining production-grade cloud stacks requires solid DevOps and infrastructure knowledge.
- **ML Specificity**: Deeply optimized for data, model, and agentic workflows; may be over-engineered for standard, non-AI automation or microservices choreography.
- **Component Coordination**: Relies on external services (e.g., MLflow servers, cloud storage) which must be individually managed or provisioned.

## When to use it
- You need to build reproducible, portable machine learning and AI agent pipelines that run across diverse environments.
- You want automatic versioning, metadata logging, and tracking of data and models without writing boilerplate integration code.
- You are utilizing swappable **MLStack** setups to switch between local experiments and cloud-based training clusters.
- You want to enable autonomous AI agents to run training loops, analyze experiment tracking charts, and auto-optimize pipelines.

## When not to use it
- For simple, linear data ingestion scripts with no model training or tracking lifecycle requirements (see [Hamilton](apache-hamilton.md)).
- If you are fully committed to a single, proprietary cloud ML platform and do not require portability or open-source stack control.
- If you need a visual-first automation tool optimized for non-technical users (see [n8n](../../services/n8n.md)).

## Getting started

### Installation
To get started with ZenML and the MLStack experiment tracking tools, install the core library:
```bash
pip install zenml
zenml init
```

### Basic Agentic Pipeline with Experiment Tracking
This example showcases a pipeline step registered with an MLStack experiment tracker to log run metrics:
```python
from zenml import pipeline, step
from zenml.client import Client

@step(experiment_tracker="mlflow_tracker")
def train_and_track_step(data: str) -> dict:
    # Log training metrics to the active MLStack experiment tracker
    import mlflow

    accuracy = 0.945
    mlflow.log_param("data_source", data)
    mlflow.log_metric("accuracy", accuracy)

    return {"status": "success", "accuracy": accuracy, "model_path": "s3://my-bucket/models/classifier.bin"}

@pipeline
def agentic_ml_pipeline():
    train_and_track_step(data="december_2026_dataset")

if __name__ == "__main__":
    agentic_ml_pipeline()
```

### Enable ZenML Dashboard
```bash
zenml up
```

## CLI examples
The `zenml` CLI manages the lifecycle of your MLStack, registered components, and experiment trackers.

```bash
# Register an MLStack experiment tracker (using MLflow flavor)
zenml experiment-tracker register mlflow_tracker --flavor mlflow

# Register an orchestrator and artifact store
zenml orchestrator register local_orchestrator --flavor local
zenml artifact-store register local_store --flavor local

# Register a unified MLStack combining orchestrator, artifact store, and experiment tracker
zenml stack register dev_mlstack \
  -o local_orchestrator \
  -a local_store \
  -e mlflow_tracker

# Activate the MLStack
zenml stack set dev_mlstack

# List all registered stacks
zenml stack list

# Run a pipeline
python run.py

# List recent pipeline runs
zenml pipeline runs list
```

## API examples
The ZenML Python Client provides programmatic access to active MLStacks, run details, and experiment tracking logs.

```python
from zenml.client import Client

client = Client()

# Retrieve active MLStack details
active_stack = client.active_stack
print(f"Active MLStack: {active_stack.name}")
print(f"Experiment Tracker: {active_stack.experiment_tracker.name if active_stack.experiment_tracker else 'None'}")

# Query latest pipeline runs and access logged step metadata
runs = client.list_pipeline_runs(sort_by="created")
for run in runs:
    print(f"Pipeline Run: {run.name} | Status: {run.status}")
    if "train_and_track_step" in run.steps:
        step_run = run.steps["train_and_track_step"]
        # Retrieve and log metadata associated with the step run
        print(f"Step outputs: {step_run.outputs}")
```

### MLStack Configuration Validation with Strict Pydantic v2 Schema
The following robust Python example uses **Pydantic v2** to programmatically validate the schema of a ZenML MLStack registration, ensuring that critical telemetry and security properties are satisfied before stack registration.

```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

# 1. Define MLStack schema using Pydantic v2
class StackComponentSchema(BaseModel):
    name: str = Field(..., min_length=3, pattern="^[a-zA-Z0-9_-]+$")
    flavor: str = Field(..., min_length=2)
    configuration: Dict[str, Any] = Field(default_factory=dict)

class MLStackSchema(BaseModel):
    stack_name: str = Field(..., min_length=3, pattern="^[a-zA-Z0-9_-]+$")
    orchestrator: StackComponentSchema
    artifact_store: StackComponentSchema
    experiment_tracker: Optional[StackComponentSchema] = None
    telemetry_enabled: bool = Field(default=True)

    @model_validator(mode="after")
    def validate_artifact_flavor(self) -> "MLStackSchema":
        if self.artifact_store.flavor == "local" and "local_path" not in self.artifact_store.configuration:
            raise ValueError("Local artifact stores must specify 'local_path' in their configuration.")
        return self

# 2. Example representation of stack definition metadata
stack_definition = {
    "stack_name": "production_mlstack",
    "orchestrator": {
        "name": "k8s_orchestrator",
        "flavor": "kubernetes",
        "configuration": {"namespace": "mlops-prod"}
    },
    "artifact_store": {
        "name": "s3_store",
        "flavor": "s3",
        "configuration": {"bucket": "zenml-artifacts-prod"}
    },
    "experiment_tracker": {
        "name": "mlflow_tracker",
        "flavor": "mlflow",
        "configuration": {"tracking_uri": "http://mlflow.mlops:5000"}
    },
    "telemetry_enabled": False
}

# 3. Perform validation using Pydantic v2
try:
    validated_stack = MLStackSchema.model_validate(stack_definition)
    print("ZenML MLStack configuration validated and ready for registration!")
    print(f"Stack Name: {validated_stack.stack_name}")
    print(f"Orchestrator Flavor: {validated_stack.orchestrator.flavor}")
except ValidationError as e:
    print(f"Validation failed: {e.json()}")
```

## Related tools / concepts
- [Flyte](flyte.md) — For large-scale, containerized ML workflows and orchestrations.
- [Dagster](dagster.md) — For asset-centric data orchestration.
- [Apache Airflow](apache-airflow.md) — Commonly used as a backend orchestrator for complex ZenML MLStacks.
- [Prefect](prefect.md) — Alternative Python-native orchestrator with dynamic flows and state tracking.
- [Temporal](temporal.md) — Durable execution engine for long-running workflows.
- [Argo Workflows](argo-workflows.md) — Kubernetes-native orchestration for parallel containerized pipelines.
- [Apache Hamilton](apache-hamilton.md) — Elegant micro-framework for defining data and model pipelines.
- [Model Control Plane (MCP)](../automation_orchestration/mcp.md) — The core protocol standard for extending ZenML with agentic tooling.
- [Claude 5.1](../ai_knowledge/claude-mythos.md) — Primary frontier model for orchestrating ZenML tasks and auditing experiment parameters.
- [GPT-5.5](../ai_knowledge/chatgpt.md) — SOTA model for advanced pipeline synthesis.
- [Gemini 4.0 Pro](../ai_knowledge/gemini-macos.md) — High-performance reasoner.
- [Llama 4](../ai_knowledge/llama.md) — Next-generation open model.
- [Gemma 3](../ai_knowledge/gemma.md) — Lightweight, high-performance model for local task execution.
- [Qwen 3.6](../ai_knowledge/qwen.md) — Next-generation open reasoning model.
- [LiteLLM](../../services/litellm.md) — Proxy tool for managing multiple LLM providers within pipeline steps.
- [n8n](../../services/n8n.md) — Visual workflow automation alternative.
- [Agent Skills](../../knowledge_base/patterns/prompt_requests.md) — Standard instruction packages for empowering agentic coding tools.

## Sources / references
- [ZenML Official Documentation](https://docs.zenml.io/)
- [ZenML MLStack & Experiment Tracking Guides](https://www.zenml.io/blog)
- [ZenML Agent Skills: Quick Wins](https://www.zenml.io/blog/introducing-zenml-agent-skills-let-ai-upgrade-your-mlops-setup-in-minutes)
- [GitHub: ZenML Core Repository](https://github.com/zenml-io/zenml)

## Contribution Metadata
- Last reviewed: 2026-12-26
- Confidence: high
