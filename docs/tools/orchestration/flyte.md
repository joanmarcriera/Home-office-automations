# Flyte

## What it is
Flyte is an open-source workflow orchestration platform for AI, machine learning, and data workflows. It uses Python authoring with strongly typed tasks and workflows, while executing at scale on cloud or Kubernetes-backed infrastructure.

## What problem it solves
Flyte helps teams move ML and AI workflows from notebooks and scripts into reproducible, versioned, and scalable pipelines. It is designed for workloads where compute, data movement, caching, lineage, and reproducibility matter as much as the execution graph.

## Where it fits in the stack
**Orchestration / AI and ML workflow platform**.

## Typical use cases
- Model training and evaluation pipelines.
- Batch inference, data processing, and feature generation.
- Agentic or long-running AI workflows that need durable execution and infrastructure awareness.
- Reproducible experimentation that later runs at production scale.

## Strengths
- Python-first authoring with typed interfaces.
- Designed for ML and AI workloads rather than only generic scheduling.
- Strong reproducibility, caching, and versioning model.
- Can bridge local development and scalable production execution.

## Limitations
- Platform setup can be heavier than lightweight local orchestrators.
- Best value appears when teams already need production ML infrastructure.
- Less useful for simple office automation or SaaS app chaining.
- Requires learning Flyte concepts and operational model.

## When to use it
- You need production-grade AI or ML pipelines with strong reproducibility.
- Workloads need scalable infrastructure and clear artifact lineage.
- Python developers need a path from local workflow development to production.

## When not to use it
- You only need scheduled scripts or small automations.
- Your organization is not ready to operate an ML workflow platform.
- A visual SaaS automation builder would serve the users better.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free open-source edition; paid enterprise platform available through Union.ai.
- **Self-hostable**: Yes

## Related tools / concepts
- [Dagster](dagster.md)
- [Argo Workflows](argo-workflows.md)
- [ZenML](zenml.md)
- [Kubernetes (K3s)](../infrastructure/k3s.md)

## Sources / References
- [Official website](https://flyte.org/)
- [Official documentation](https://docs.flyte.org/)
- [GitHub](https://github.com/flyteorg/flyte)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
