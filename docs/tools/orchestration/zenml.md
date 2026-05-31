# ZenML

## What it is
ZenML is an open-source, extensible MLOps framework that enables data scientists and AI engineers to build portable, production-ready pipelines. It provides a standardized way to define machine learning and agentic workflows that are decoupled from the underlying infrastructure. As of May 2026, **v0.62.x** is the current stable release, featuring advanced **Agentic Pipeline** patterns and improved **Stack Component** management.

## What problem it solves
The "gap" between local development and production infrastructure is a major hurdle in AI development. ZenML solves this by abstracting the infrastructure layer (the "Stack") from the pipeline logic. This means the same code that runs on a developer's laptop can be deployed to Kubernetes, Vertex AI, or AWS SageMaker without modification, ensuring reproducibility and reducing time-to-market.

## Where it fits in the stack
**Orchestration / MLOps Pipeline Framework**. It acts as a management layer that coordinates specialized tools for experiment tracking, artifact storage, and model deployment across different cloud and local environments.

## Typical use cases
- **Portable AI Agents**: Building agents that can be developed locally and deployed to production environments while maintaining consistent state and artifact tracking.
- **End-to-End ML Pipelines**: Managing the entire lifecycle from data ingestion and preprocessing to model training, evaluation, and serving.
- **LLMOps and RAG**: Coordinating the periodic update of vector databases, fine-tuning of models, and evaluation of retrieval performance.
- **Multi-Cloud Strategies**: Standardizing ML workflows across different cloud providers to avoid vendor lock-in.

## Strengths
- **Infrastructure Agnostic**: Write once, run anywhere (Local, K8s, Airflow, Vertex AI, etc.).
- **Strong Artifact Tracking**: Automatically tracks every input and output of every pipeline step, ensuring full lineage.
- **Extensible Plugin System**: Easy to integrate with existing tools like MLflow, Weights & Biases, BentoML, and more.
- **Developer-Centric**: Focused on providing a clean Python SDK that feels natural to data scientists.
- **v0.62 Features**: Enhanced support for Agentic pipelines, improved secrets management, and streamlined stack registration via the CLI.

## Limitations
- **Learning Curve**: Teams must understand the "Stack" and "Stack Component" concepts to fully leverage the framework.
- **Operational Overhead**: While it simplifies infrastructure for the developer, the initial setup of a production stack requires DevOps knowledge.
- **ML Focus**: Might be overly complex for simple, non-ML automation tasks where general-purpose orchestrators like n8n or Prefect suffice.

## When to use it
- You need to build portable, reproducible AI/ML pipelines that run across multiple environments.
- You want to enforce best practices for artifact versioning and experiment tracking without writing boilerplate code.
- You are building complex AI agents that require a structured, observable execution environment.

## When not to use it
- For simple, single-use automation scripts with no data or model lifecycle requirements.
- If your team is already standardized on a single, all-encompassing cloud ML platform (e.g., pure Vertex AI) and doesn't need portability.
- If you are looking for a purely visual automation tool (see [n8n](../../services/n8n.md)).

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free open-source core; ZenML Pro offers a managed control plane and enterprise features.
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install zenml
zenml init
```

### Basic Pipeline Example
```python
from zenml import pipeline, step

@step
def load_data() -> str:
    return "Sample AI Data"

@step
def process_data(data: str) -> str:
    return f"Processed: {data}"

@pipeline
def my_ai_pipeline():
    data = load_data()
    process_data(data)

if __name__ == "__main__":
    my_ai_pipeline()
```

### Visualize the Pipeline
```bash
zenml up
```
Access the ZenML dashboard to view pipeline runs and artifacts.

## CLI examples
The `zenml` CLI is the primary tool for stack and pipeline management.

```bash
# List all registered stacks
zenml stack list

# Register a new stack component (e.g., an orchestrator)
zenml orchestrator register my_local_orchestrator --flavor local

# Register and activate a new stack
zenml stack register my_stack -o my_local_orchestrator -a my_artifact_store
zenml stack set my_stack

# View details of a specific pipeline run
zenml pipeline runs list
```

## API examples
ZenML provides a Python-based Client for programmatic access to the control plane.

```python
from zenml.client import Client

client = Client()

# Get a list of all pipelines
pipelines = client.list_pipelines()
for p in pipelines:
    print(f"Pipeline: {p.name}")

# Get the latest run of a specific pipeline
latest_run = client.get_pipeline("my_ai_pipeline").runs[0]
print(f"Status: {latest_run.status}")
```

## Related tools / concepts
- [Flyte](flyte.md) — For large-scale, containerized ML workflows.
- [Dagster](dagster.md) — For asset-centric data orchestration.
- [Apache Airflow](apache-airflow.md) — Often used as a backend orchestrator for ZenML.
- [DVC](../development_ops/index.md) — For data versioning alongside ZenML.
- [MLflow](../development_ops/index.md) — For experiment tracking integration.
- [BentoML](../frameworks/index.md) — For model serving and deployment.
- [LiteLLM](../../services/litellm.md) — For integrating LLMs into ZenML steps.

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-31)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high

## Sources / References
- [ZenML Official Documentation](https://docs.zenml.io/)
- [ZenML v0.62 Release Blog](https://www.zenml.io/blog)
- [GitHub: ZenML Core](https://github.com/zenml-io/zenml)
