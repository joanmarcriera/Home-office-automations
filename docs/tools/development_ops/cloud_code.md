# Cloud Code

## What it is
A set of IDE plugins for VS Code and IntelliJ that help developers develop, deploy, and debug cloud-native applications. It provides tools for working with Kubernetes, Google Cloud, and other cloud providers directly from the IDE.

## What problem it solves
Reduces context switching by bringing cloud-native development workflows (Kubernetes management, deployment, debugging) directly into the IDE.

## Where it fits in the stack
**Development & Ops**. Bridges the gap between local development and cloud infrastructure management.

## Typical use cases
- Developing and debugging Kubernetes applications from the IDE
- Deploying applications to Google Cloud or other providers
- Setting up Kubernetes development environments

## Strengths
- Deep integration with VS Code and IntelliJ
- Native support for Kubernetes and Google Cloud workflows
- Reduces context switching between IDE and cloud consoles

## Limitations
- Primarily oriented toward Google Cloud; less useful for other providers
- Requires familiarity with Kubernetes concepts
- Plugin overhead may affect IDE performance on lower-end hardware

## When to use it
- When developing cloud-native applications targeting Kubernetes or Google Cloud
- When you want to manage deployments without leaving the IDE
- When you need integrated secret management via Secret Manager

## When not to use it
- When working on projects that do not involve cloud infrastructure
- When a standalone Kubernetes management tool (e.g., [Lens](https://k8slens.dev/)) is preferred
- When working exclusively in AWS or Azure (use their respective toolkits)

## Key Features
- **Kubernetes Explorer**: Browse, manage, and view logs for clusters, nodes, and workloads.
- **Cloud Run Support**: Develop and debug serverless applications locally and in the cloud.
- **Secret Manager Integration**: Create and manage secrets directly within the IDE.
- **Cloud Code AI**: Assist in writing Kubernetes YAML and Cloud Run service definitions.

## Inner Loop Development with Skaffold
Cloud Code integrates with [Skaffold](./skaffold.md) for real-time rebuilds:
1. Open the "Cloud Code" status bar menu.
2. Select **Run on Kubernetes**.
3. Cloud Code will build your image, push it to a registry, and deploy it to your cluster (local or remote), then stream logs back to the IDE.

## Getting started

Cloud Code is primarily used via its VS Code or IntelliJ extensions to accelerate Kubernetes and Cloud Build workflows.

### 1. Kubernetes YAML Authoring
Cloud Code provides smart snippets for Kubernetes resources. In a YAML file, trigger the completion (e.g., `Ctrl+Space`) and select a snippet:
```yaml
# Example: Using a Cloud Code snippet for a Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: gcr.io/my-project/my-app:v1
```

### 2. Secret Manager Integration
Cloud Code allows you to inject secrets into your code without exposing them in version control.
```python
# Cloud Code can help generate the client code for Secret Manager
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
response = client.access_secret_version(request={"name": name})
payload = response.payload.data.decode("UTF-8")
```

## Related tools / concepts
- [Skaffold](https://skaffold.dev/)
- [Docker](../infrastructure/docker.md)
- [Helm](https://helm.sh/)
- [Claude Code — Project Setup Guide](claude-code-setup.md)
- [Windsurf](./windsurf.md)
- [Cursor](./cursor.md)
- [Aider](./aider.md)
- [Kubernetes Architecture](../../architecture/infrastructure.md)
- [Lens](https://k8slens.dev/)

## Sources / references
- [Official Website](https://cloud.google.com/code)
- [Cloud Code for VS Code Documentation](https://cloud.google.com/code/docs/vscode)
- [YAML Editing in Cloud Code](https://cloud.google.com/code/docs/vscode/yaml-editing)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
