# ZenML

## What it is
ZenML is an open-source, extensible MLOps framework designed to create portable, production-ready AI pipelines and agentic workflows. It provides a standardized abstraction layer (the "Stack") that decouples pipeline logic from the underlying infrastructure. As of June 2026, **v0.95.x** is the stable release, featuring native **Agentic Pipeline** patterns, **Agent Skills** integration for autonomous MLOps, and deep support for the **Model Control Plane (MCP 3.0)**.

## What problem it solves
ZenML bridges the "production gap" by allowing developers to write pipeline code once and run it anywhere—from a local laptop to enterprise clusters like Kubernetes, Vertex AI, or AWS SageMaker. It solves the complexity of infrastructure management, artifact tracking, and reproducibility in AI development, ensuring that local experiments translate seamlessly into reliable production services.

## Where it fits in the stack
**Orchestration / MLOps Pipeline Framework**. It serves as the management and coordination layer that sits above specialized tools for data versioning, experiment tracking, and model serving.

## Typical use cases
- **Agentic Workflows**: Building multi-stage AI agents that require durable state, observability, and artifact tracking across distributed environments.
- **Portable ML Pipelines**: Developing end-to-end machine learning lifecycles that can be migrated between cloud providers without code changes.
- **LLMOps and RAG**: Coordinating the ingestion of data into vector databases, fine-tuning frontier models, and evaluating retrieval performance.
- **Autonomous MLOps**: Utilizing ZenML "Agent Skills" to allow agents like Claude Code to independently audit and improve pipeline configurations.

## Strengths
- **Infrastructure Agnostic**: "Write once, run anywhere" across Local, K8s, Airflow, Vertex AI, and more.
- **Strong Artifact Lineage**: Automatically tracks every input, output, and metadata piece for every pipeline step.
- **Extensible Plugin Architecture**: Native integrations with MLflow, Weights & Biases, BentoML, and LiteLLM.
- **v0.95 Features**: Support for Agent Skills (modular instruction packages for agentic coding tools) and native Model Control Plane (MCP) integration.
- **Developer-Centric**: A Pythonic SDK that prioritizes ease of use for data scientists and AI engineers.

## Limitations
- **Operational Setup**: While it simplifies usage, initial configuration of production-grade stacks requires DevOps and infrastructure knowledge.
- **ML Specificity**: Optimized for data and model-driven workflows; may be over-engineered for simple, non-AI automation tasks.
- **Learning Curve**: Requires understanding ZenML-specific concepts like Stacks, Orchestrators, and Artifact Stores.

## When to use it
- You need to build reproducible, portable AI/ML pipelines that run across diverse environments.
- You want automatic versioning and tracking of data and models without writing boilerplate code.
- You are developing complex AI agents that require structured execution and full observability.
- You want to enable agentic coding tools to maintain and optimize your MLOps infrastructure via Agent Skills.

## When not to use it
- For simple, linear automation scripts with no data or model lifecycle requirements (see [Hamilton](apache-hamilton.md)).
- If you are fully committed to a single, proprietary cloud ML platform and do not require portability.
- If you need a visual-first automation tool for non-technical users (see [n8n](../../services/n8n.md)).

## Getting started

### Installation
```bash
pip install zenml
zenml init
```

### Basic Agentic Pipeline Example
```python
from zenml import pipeline, step
from zenml.client import Client

@step
def load_context() -> str:
    return "Initial Agent Context"

@step
def agent_reasoning(context: str) -> str:
    # Logic for Claude 4.8 or GPT-5.5 integration
    return f"Processed: {context}"

@pipeline
def my_agent_pipeline():
    context = load_context()
    agent_reasoning(context)

if __name__ == "__main__":
    my_agent_pipeline()
```

### Enable ZenML Dashboard
```bash
zenml up
```

## CLI examples
The `zenml` CLI manages the entire lifecycle of stacks and components.

```bash
# List all registered stacks
zenml stack list

# Register a new local orchestrator
zenml orchestrator register my_orchestrator --flavor local

# Create and activate a stack
zenml stack register my_prod_stack -o my_orchestrator -a my_artifact_store
zenml stack set my_prod_stack

# Run a pipeline
python run.py

# List recent pipeline runs
zenml pipeline runs list
```

## API examples
The ZenML Python Client provides programmatic access to the control plane.

```python
from zenml.client import Client

client = Client()

# Retrieve a specific pipeline run
run = client.get_pipeline_run("my_agent_pipeline-run-2026-06-21")
print(f"Status: {run.status}")

# Access artifacts from a run
for step_name, step_run in run.steps.items():
    for output_name, artifact in step_run.outputs.items():
        print(f"Step {step_name} produced {output_name}: {artifact.uri}")
```

## Related tools / concepts
- [Flyte](flyte.md) — For large-scale, containerized ML workflows.
- [Dagster](dagster.md) — For asset-centric data orchestration.
- [Apache Airflow](apache-airflow.md) — Often used as a backend orchestrator for ZenML.
- [Hera](https://github.com/argoproj-labs/hera) — For Pythonic interaction with Argo Workflows.
- [LiteLLM](../../services/litellm.md) — For managing LLM providers within ZenML steps.
- [Model Control Plane (MCP)](../../architecture/multi_agent_knowledgeops.md) — ZenML v0.95+ integration standard.
- [Agent Skills](../../knowledge_base/patterns/prompt_requests.md) — Extending agentic capabilities in MLOps.

## Sources / References
- [ZenML Official Documentation](https://docs.zenml.io/)
- [ZenML v0.95 Release Blog](https://www.zenml.io/blog)
- [ZenML Agent Skills: Quick Wins](https://www.zenml.io/blog/introducing-zenml-agent-skills-let-ai-upgrade-your-mlops-setup-in-minutes)
- [GitHub: ZenML Core](https://github.com/zenml-io/zenml)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
