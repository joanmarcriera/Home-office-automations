# Argo Workflows

## What it is
Argo Workflows is an open-source, container-native workflow engine for orchestrating parallel jobs on Kubernetes. As of May 2026, **v3.7.x** is the current stable release, featuring enhanced multi-controller locking, smarter caching, and improved security postures.

## What problem it solves
It brings simple, YAML-based workflow orchestration to Kubernetes. Each task in a workflow is executed as a separate container, allowing for massive parallelism, resource isolation, and native integration with the K8s ecosystem without needing a separate infrastructure stack.

## Where it fits in the stack
**Orchestration / Kubernetes-Native Workflow Engine**. It is the standard for building complex pipelines directly on K3s, EKS, or GKE.

## Typical use cases
- **Machine Learning Pipelines**: Coordinating data preprocessing, model training (with GPU scheduling), and deployment.
- **CI/CD Pipelines**: Running multi-stage builds, tests, and deployments in isolated containers.
- **Data Processing (ETL)**: Orchestrating large-scale batch processing tasks using K8s resource management.
- **Infrastructure Automation**: Automating the lifecycle of K8s resources and cloud-native services.

## Strengths
- **Kubernetes-Native**: Implemented as a Custom Resource Definition (CRD), fitting perfectly into GitOps workflows (Argo CD).
- **Massive Parallelism**: Capable of running thousands of containers in parallel, limited only by cluster capacity.
- **v3.7 Features**: Smarter caching/memoization, multi-controller locking for cross-namespace scaling, and non-root execution for improved security.
- **Dynamic Parallelism**: Fine-grained control over resource usage per namespace.

## Limitations
- **Kubernetes Dependent**: Requires a K8s cluster to run; cannot be used as a standalone library or service on bare OS.
- **YAML Overhead**: Large, complex workflows can result in "YAML soup," though this can be mitigated with the Python SDK (Hera).
- **Latency**: Container startup overhead makes it less suitable for low-latency, real-time request handling.

## When to use it
- Your infrastructure is already Kubernetes-centric.
- You need to run complex, containerized tasks with specific resource requirements (e.g., GPU, high memory).
- You want a GitOps-compatible way to manage your workflows.

## When not to use it
- You do not use Kubernetes and don't want the overhead of managing a cluster.
- You need a simple, single-machine script or a micro-orchestrator (consider Hamilton).

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free
- **Self-hostable**: Yes (CNCF Graduate Project)

## Getting started

### Installation (Quickstart)
Deploy Argo Workflows to your local K3s or development cluster:

```bash
kubectl create namespace argo
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.7.0/install.yaml
```

### Submit a Hello World Workflow
```bash
# Create a simple hello-world workflow
cat <<EOF > hello-world.yaml
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

# Submit the workflow
argo submit -n argo hello-world.yaml --watch
```

## CLI examples
The `argo` CLI is the primary tool for interacting with the workflow controller.

```bash
# List workflows in the 'argo' namespace
argo list -n argo

# Get details and logs for a specific workflow
argo get -n argo hello-world-xxxxx
argo logs -n argo hello-world-xxxxx

# Delete all completed workflows
argo delete -n argo --status Completed

# Suspend/Resume a running workflow
argo suspend -n argo my-long-running-wf
argo resume -n argo my-long-running-wf
```

## API examples
Argo provides a robust REST API (typically exposed via the Argo Server).

```bash
# Get the Argo Server version
curl -X GET "https://argo-server:2746/api/v1/version" \
     -H "Authorization: Bearer <TOKEN>" -k

# List workflows via API
curl -X GET "https://argo-server:2746/api/v1/workflows/argo" \
     -H "Authorization: Bearer <TOKEN>" -k
```

## Related tools / concepts
- [Argo CD](https://argoproj.github.io/argo-cd/) — For GitOps-based deployment of Argo Workflows.
- [Apache Airflow](apache-airflow.md) — For enterprise-wide batch scheduling.
- [Kestra](kestra.md) — For event-driven declarative orchestration.
- [Hamilton](apache-hamilton.md) — For micro-orchestration of tasks within containers.
- [Hera](https://github.com/argoproj-labs/hera) — Python SDK for Argo Workflows.
- [Flyte](flyte.md) — For machine-learning specific container orchestration.
- [Temporal](temporal.md) — For durable, long-running stateful workflows.

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-31)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high

## Sources / References
- [Argo Workflows Official Documentation](https://argoproj.github.io/argo-workflows/)
- [GitHub Repository](https://github.com/argoproj/argo-workflows)
- [Hera: Argo Workflows Python SDK](https://github.com/argoproj-labs/hera)
- [v3.7.0 Release Notes](https://github.com/argoproj/argo-workflows/releases/tag/v3.7.0)
