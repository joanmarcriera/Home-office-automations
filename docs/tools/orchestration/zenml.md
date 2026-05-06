# ZenML

## What it is
ZenML is an open-source MLOps framework for building portable machine learning, AI, and agent pipelines across local and production infrastructure. It uses stack components, including orchestrators, artifact stores, experiment trackers, model deployers, and cloud integrations.

## What problem it solves
ZenML helps teams standardize the path from experimentation to production for ML and AI workflows. It separates pipeline code from the underlying infrastructure, making it easier to run the same pipeline locally, on Kubernetes, or through managed cloud services.

## Where it fits in the stack
**Orchestration / MLOps pipeline framework**.

## Typical use cases
- End-to-end ML pipelines from preprocessing through training and deployment.
- LLMOps workflows for evaluation, retrieval, and model lifecycle management.
- Multi-environment pipelines that should move from local development to cloud execution.
- Agent or AI workflows that need metadata, artifacts, and stack portability.

## Strengths
- Explicit MLOps stack abstraction keeps infrastructure choices swappable.
- Supports multiple orchestrator backends, including local, Kubernetes, Airflow, Kubeflow, Vertex AI, SageMaker, AzureML, and Tekton.
- Good fit for teams standardizing ML lifecycle practices.
- Includes concepts for artifacts, metadata, deployments, and production pipeline execution.

## Limitations
- More ML-platform oriented than general office or SaaS automation.
- Requires understanding ZenML stack components and integrations.
- Actual orchestration behavior depends on the chosen backend.
- May be more structure than needed for simple Python scripts.

## When to use it
- You need a portable MLOps framework across local, cloud, and Kubernetes environments.
- AI or ML pipelines require metadata, artifact, and deployment discipline.
- The team wants to avoid hard-coding one orchestrator into pipeline logic.

## When not to use it
- You only need a single workflow scheduler.
- Workflows are not ML or AI lifecycle focused.
- A direct Airflow, Prefect, or Dagster setup would be simpler for the team.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free open-source framework; paid ZenML Pro/managed options available.
- **Self-hostable**: Yes

## Related tools / concepts
- [Flyte](flyte.md)
- [Dagster](dagster.md)
- [Apache Airflow](apache-airflow.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## Sources / References
- [Official website](https://www.zenml.io/)
- [Official documentation](https://docs.zenml.io/)
- [GitHub](https://github.com/zenml-io/zenml)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
