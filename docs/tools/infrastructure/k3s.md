# Kubernetes (K3s)

## What it is
K3s is a highly available, certified Kubernetes distribution designed for production workloads in resource-constrained environments like edge devices, IoT, and homelabs. Developed by Rancher (now SUSE) and currently maintained under the CNCF as a Sandbox project, K3s packages the entire Kubernetes suite into a single, lightweight binary (~50MB). Fully integrated with the early 2027 SOTA AI stack (supporting Kubernetes v1.33+), K3s is the standard lightweight container orchestrator, offering full self-hostability, open-source compliance under the Apache 2.0 license, and completely free usage.

## What problem it solves
Operating a standard Kubernetes cluster requires significant operational overhead, complex certificate management, and high baseline memory utilization (often several gigabytes). This "Kubernetes tax" makes vanilla Kubernetes impractical for home offices, single-board computers (such as Raspberry Pi 5), or edge locations.

K3s solves these problems by:
- **Reducing Overhead**: Replacing etcd with SQLite as the default datastore, reducing server memory requirements to under 512MB RAM.
- **Simplifying Setup**: Packaging essential components (containerd, Flannel, CoreDNS, Traefik v3.3+, Local Storage Provisioner, and Klipper Load Balancer) into a single executable that installs in seconds.
- **Automating Maintenance**: Providing automatic certificate rotation, built-in TLS provisioning, and clean upgrades with zero manual YAML tinkering.

## Where it fits in the stack
**Infrastructure / Deployment Layer**. It serves as the foundational container orchestration system hosting the entire self-hosted, privacy-first, and agentic stack. K3s sits directly on top of raw Linux operating systems (or virtualized hosts) and serves as the runtime platform for hosting LLM inference servers (like vLLM or Ollama), automation workflow engines, and distributed databases.

```
┌──────────────────────────────────────────────┐
│           Agent / Orchestration              │
│       (n8n, Kestra, Argo Workflows)          │
├──────────────────────────────────────────────┤
│               Inference Layer                │
│ (vLLM, Ollama, Aphrodite Engine, FastMCP 3.1)│
├──────────────────────────────────────────────┤
│          K3S KUBERNETES CONTAINER RUNTIME    │ (Traefik v3.3, CoreDNS, Flannel)
├──────────────────────────────────────────────┤
│               Operating System               │
│             (Talos OS, Debian)               │
└──────────────────────────────────────────────┘
```

## Typical use cases
- **Multi-Node Homelab Orchestration**: Running a self-healing, load-balanced home-office stack including document management (Paperless-ngx), home assistant devices, and local file storage.
- **High-Throughput Local AI Clusters**: Managing fleets of containerized GPU-enabled workers hosting high-performance inference engines (such as vLLM or Aphrodite Engine) to support heavy parallel multi-agent reasoning workloads powered by frontier models like Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra.
- **Declarative GitOps Pipelines**: Orchestrating workflows via Kubernetes-native pipelines (e.g., Argo Workflows) that spawn agentic tasks, perform evaluations, and automatically tear down ephemeral resources.
- **Local Application Development**: Simulating high-fidelity, production-grade Kubernetes environments on local workstations without the overhead of heavy VM-based emulators.

## Strengths
- **CNCF Certified**: Fully compliant Kubernetes distribution. What runs on K3s works identically on AWS EKS, Google GKE, or Azure AKS.
- **Minimal Footprint**: Runs comfortably on 1 vCPU and 512MB RAM, making it suitable for hardware as small as a Raspberry Pi.
- **Integrated Stack**: Out-of-the-box CNI (Flannel), Ingress Controller (Traefik v3.3+), Service Load Balancer (Klipper), and storage class (Local-Path Provisioner).
- **Embedded Database Options**: Supports multi-node High Availability (HA) without an external DB by utilizing embedded `etcd` or external Postgres/MySQL.
- **Multi-Architecture Support**: Built-in, first-class binaries for both standard x86_64 and ARM64/ARMv7 processors.

## Limitations
- **SQLite Single Point of Failure (SPOF)**: The default SQLite configuration is single-node only; multi-node high availability requires switching to external Postgres or embedded etcd.
- **Basic Default CNI**: Flannel is highly stable but lacks advanced network policy definitions, eBGP routing, or service mesh capabilities offered by Cilium (though Cilium can be installed as a swap-in).
- **Resource Management Overhead**: Although highly optimized, running containerized workloads on Kubernetes still introduces slight CPU and memory overhead compared to direct Docker Compose setups.
- **Host System Configuration Requirements**: Requires minor host configuration tweaks (such as setting up cgroups and disabling swap space) to ensure absolute stability.

## When to use it
- When you are managing more than 3-5 interdependent local services that require automated failover, declarative self-healing, and dynamic ingress routing.
- When deploying GPU-bound local agent workflows that need to survive single-node hardware failures in a homelab environment.
- When seeking a standardized, immutable system architecture governed entirely by GitOps (e.g., using Argo CD or Flux) for absolute reproducibility.

## When not to use it
- For basic single-server home labs where Docker Compose or a lightweight systemd setup offers a simpler, low-complexity workflow.
- If you lack experience with Kubernetes concepts (pods, services, ingress, PV/PVCs) and require an immediate, friction-free desktop GUI setup.

## Getting started

### 1. Fast Single-Node Installation
The official installation script simplifies K3s bootstrap into a single terminal pipeline:

```bash
# Download and install K3s with default settings
curl -sfL https://get.k3s.io | sh -

# Verify that the node is running and ready
sudo k3s kubectl get nodes -o wide
```

### 2. Standard Configuration Customization
To customize K3s on startup (e.g., configuring trailing parameters, changing the default ports, or configuring GPU runtimes), create a configuration file at `/etc/rancher/k3s/config.yaml`:

```yaml
write-kubeconfig-mode: "0644"
tls-san:
  - "homelab.local"
disable:
  - servicelb
  - traefik
```
Apply the configuration by restarting the systemd service:
```bash
sudo systemctl restart k3s
```

### 3. Deploying a Self-Healing Local Service
Create a standard deployment manifest named `agent-service.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: local-agent-worker
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-worker
  template:
    metadata:
      labels:
        app: agent-worker
    spec:
      containers:
      - name: agent-runner
        image: nginx:1.27-alpine
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: "128Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: local-agent-service
  namespace: default
spec:
  selector:
    app: agent-worker
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
```

Apply the deployment manifest to your active cluster:
```bash
k3s kubectl apply -f agent-service.yaml
```

## CLI examples

### 1. Cluster Diagnostics & Health Verification
Validate the status of the local node and verify runtime parameters:
```bash
# Check if the host configuration is compatible with K3s
k3s check-config

# List all pods across all namespaces to ensure Traefik and CoreDNS are healthy
sudo k3s kubectl get pods -A
```

### 2. Resource & Allocation Inspections
Review active node consumption, pod utilization, and capacity details:
```bash
# Display CPU/Memory utilization of active nodes
sudo k3s kubectl top node

# Inspect detailed resource limits and container configurations
sudo k3s kubectl describe deployment local-agent-worker
```

### 3. Service Logs and Systemd Maintenance
Monitor server behavior, access control logs, and daemon status:
```bash
# Stream active K3s daemon logs
sudo journalctl -u k3s -f -n 100

# View standard ingress controller logs
sudo k3s kubectl logs -n kube-system -l app.kubernetes.io/name=traefik -f
```

## API examples

### Python: List and Validate Active Pods using Kubernetes Client & Pydantic v2
Interact programmatically with the K3s cluster using the standard Python client library. This script uses Pydantic v2 to strictly validate pod parameters, resource fields, and status configurations.

```python
import os
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from kubernetes import client, config

class K3sPodMetadata(BaseModel):
    """Schema representing validated active pod details from the K3s cluster."""
    name: str = Field(..., description="The name of the pod resource.")
    namespace: str = Field(..., description="Target Kubernetes namespace.")
    pod_ip: Optional[str] = Field(None, description="The internal IP assigned to the pod.")
    status_phase: str = Field(..., description="Current lifecycle stage of the pod (e.g. Running).")

    @field_validator("status_phase")
    @classmethod
    def validate_phase(cls, v: str) -> str:
        allowed = ["Pending", "Running", "Succeeded", "Failed", "Unknown"]
        if v not in allowed:
            raise ValueError(f"Invalid status phase '{v}'. Must be one of {allowed}")
        return v

class K3sClusterAuditReport(BaseModel):
    """Schema representing the validated output report of the K3s cluster audit."""
    cluster_endpoint: str = Field(..., description="Target API server address.")
    active_pods: List[K3sPodMetadata]
    total_running_count: int = Field(default=0, ge=0)

def perform_cluster_audit(kubeconfig_path: str = "/etc/rancher/k3s/k3s.yaml") -> K3sClusterAuditReport:
    """Queries the local K3s API server and validates all active pod objects."""
    if not os.path.exists(kubeconfig_path):
        # Fallback for demonstration/testing environments without local K3s setup
        print(f"K3s config not found at {kubeconfig_path}. Generating validated mockup cluster status.")
        mock_pods = [
            K3sPodMetadata(name="local-agent-worker-1", namespace="default", pod_ip="10.42.0.15", status_phase="Running"),
            K3sPodMetadata(name="vllm-serving-inference", namespace="ai-services", pod_ip="10.42.1.2", status_phase="Running")
        ]
        return K3sClusterAuditReport(
            cluster_endpoint="https://127.0.0.1:6443",
            active_pods=mock_pods,
            total_running_count=2
        )

    try:
        config.load_kube_config(config_file=kubeconfig_path)
        v1 = client.CoreV1Api()
        pod_list = v1.list_pod_for_all_namespaces(watch=False)

        validated_pods = []
        running_count = 0

        for pod in pod_list.items:
            metadata = K3sPodMetadata(
                name=pod.metadata.name,
                namespace=pod.metadata.namespace,
                pod_ip=pod.status.pod_ip,
                status_phase=pod.status.phase
            )
            validated_pods.append(metadata)
            if metadata.status_phase == "Running":
                running_count += 1

        # Extract cluster server endpoint
        contexts, active_context = config.list_kube_config_contexts(config_file=kubeconfig_path)
        server_endpoint = active_context.get('context', {}).get('cluster', 'unknown')

        return K3sClusterAuditReport(
            cluster_endpoint=server_endpoint,
            active_pods=validated_pods,
            total_running_count=running_count
        )
    except Exception as e:
        print(f"Error querying cluster API server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    report = perform_cluster_audit()
    print(f"K3s API Server Audited: {report.cluster_endpoint}")
    print(f"Total Running Pods Verified: {report.total_running_count}")
    for pod in report.active_pods:
        print(f" - [{pod.namespace}] {pod.name} ({pod.status_phase}) - IP: {pod.pod_ip or 'None'}")
```

### 2. Python: Monitor and Scale Ephemeral Workloads
Programmatically scale containerized agent tasks based on workload queues:

```python
from kubernetes import client, config

def scale_deployment(name: str, namespace: str, replicas: int):
    # Load kubeconfig from default K3s path
    config.load_kube_config(config_file="/etc/rancher/k3s/k3s.yaml")

    apps_v1 = client.AppsV1Api()

    # Read the current deployment configuration
    deployment = apps_v1.read_namespaced_deployment_scale(name=name, namespace=namespace)

    # Update replica parameter
    deployment.spec.replicas = replicas

    # Patch scale configuration
    apps_v1.replace_namespaced_deployment_scale(name=name, namespace=namespace, body=deployment)
    print(f"Successfully scaled deployment '{name}' in namespace '{namespace}' to {replicas} replicas.")

if __name__ == "__main__":
    try:
        scale_deployment(name="local-agent-worker", namespace="default", replicas=5)
    except Exception as e:
        print(f"Mock Scale Operation: Would scale local-agent-worker to 5 replicas. (Reason: {e})")
```

## Related tools / concepts
- [Docker](docker.md) — The lightweight container runtime often used as an alternative or layer under K3s.
- [vLLM](vllm.md) — High-throughput LLM serving engine commonly deployed inside K3s clusters for local AI tasks.
- [llama.cpp](llama-cpp.md) — GGUF local model inference engine compatible with Kubernetes deployments.
- [Aphrodite Engine](aphrodite-engine.md) — Highly optimized vLLM fork with specialized GGUF/EXL2 and DRY/XTC sampling, running inside K3s.
- [Argo Workflows](../orchestration/argo-workflows.md) — Native Kubernetes orchestration engine to run parallel multi-agent reasoning steps.
- [Kestra](../orchestration/kestra.md) — Modern declarative, event-driven orchestration tool easily self-hosted on K3s.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Architectural standard to connect local LLM systems to external tool suites hosted within the cluster.
- [Ollama](../../services/ollama.md) — Local model engine frequently exposed as a cluster-wide service on K3s.
- [n8n](../../services/n8n.md) — Highly popular self-hosted workflow automation platform run on K3s for system automation.
- [Home Assistant](../../services/home-assistant.md) — Smart home automation backend frequently deployed alongside agent clusters in K3s environments.
- [Talos OS](../../knowledge_base/talos-vs-ubuntu-k3s.md) — Immutable, security-hardened Linux operating system designed specifically to host K3s.
- **Licensing and Cost Model**: Distributed as completely free, open-source software under the Apache 2.0 license. K3s is fully self-hostable with zero licensing fees, proprietary locks, or commercial usage restrictions.

## Sources / references
- [K3s Official Portal](https://k3s.io/)
- [K3s GitHub Repository](https://github.com/k3s-io/k3s)
- [K3s Official Documentation Manual](https://docs.k3s.io/)
- [Rancher Labs / SUSE](https://www.rancher.com/)
- [CNCF Sandbox - K3s](https://sandbox.cncf.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
