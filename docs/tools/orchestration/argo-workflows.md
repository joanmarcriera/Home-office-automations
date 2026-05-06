# Argo Workflows

## What it is
Argo Workflows is an open-source, Kubernetes-native workflow engine for running containerized DAG and step-based workflows. Workflows are represented as Kubernetes custom resources, and each step typically runs as a container.

## What problem it solves
Argo Workflows gives Kubernetes teams a native way to run parallel, compute-heavy, and dependency-aware jobs without bolting a separate scheduler beside the cluster. For AI systems, it is useful for batch inference, evaluation sweeps, data processing, training jobs, and other workloads that benefit from Kubernetes scheduling and isolation.

## Where it fits in the stack
**Orchestration / Kubernetes-native workflow engine**.

## Typical use cases
- Parallel data processing or ML jobs on Kubernetes.
- Batch inference and evaluation workflows.
- CI/CD-style workflows that should run inside the same Kubernetes control plane.
- Containerized pipelines that need resource limits, secrets, volumes, and cluster scheduling.

## Strengths
- Deep Kubernetes integration through custom resources.
- Good fit for highly parallel container jobs.
- Cloud-agnostic when the underlying Kubernetes platform is portable.
- Works naturally with GitOps and Kubernetes-native operational controls.

## Limitations
- Requires Kubernetes fluency and cluster operations.
- YAML-heavy workflow authoring can become difficult for complex application logic.
- Less suited to interactive or long-running conversational agents.
- Not the right abstraction for simple local automations.

## When to use it
- Your workloads are already containerized and run on Kubernetes.
- You need high parallelism and cluster-native scheduling.
- Platform teams want workflows controlled through Kubernetes APIs and GitOps.

## When not to use it
- You do not run Kubernetes.
- The team wants Python-native workflow code as the primary authoring surface.
- You need a SaaS automation product for non-technical users.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free self-hosted; infrastructure costs depend on the Kubernetes environment.
- **Self-hostable**: Yes

## Related tools / concepts
- [Flyte](flyte.md)
- [Apache Airflow](apache-airflow.md)
- [Temporal](temporal.md)
- [Kubernetes (K3s)](../infrastructure/k3s.md)

## Sources / References
- [Official documentation](https://argoproj.github.io/workflows/)
- [GitHub](https://github.com/argoproj/argo-workflows)
- [Argo project](https://argoproj.github.io/)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
