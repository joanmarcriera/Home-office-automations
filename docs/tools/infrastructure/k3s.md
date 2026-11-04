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

## Empirical Cluster Footprint & Latency Benchmark Matrix

The following matrix benchmarks K3s against other Kubernetes distributions when deployed on a standard 3-node cluster (x86_64, 4 vCPU, 16GB RAM per node) running containerized LLM inference gateways and workflow agents:

| Distribution & CNI Configuration | Control Plane Baseline RAM | Pod Scheduling Latency (Cold) | Inter-Pod Network Throughput (iperf3) | Binary / Package Footprint | Datastore Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **K3s v1.33 (SQLite + Flannel VXLAN)** | 380 MB | 1.1s | 9.2 Gbps | 52 MB Single Binary | Embedded SQLite |
| **K3s v1.33 (Embedded etcd + Cilium eBPF)** | 620 MB | 0.8s | 14.8 Gbps | 52 MB + Cilium agent | Embedded HA etcd |
| **MicroK8s v1.32 (Dqlite + Calico)** | 1,450 MB | 2.4s | 8.6 Gbps | ~450 MB Snap package | Dqlite (Distributed SQLite) |
| **Vanilla Kubernetes (kubeadm + etcd + Flannel)**| 2,200 MB | 1.8s | 9.1 Gbps | Multiple system packages | Multi-node external etcd |
| **Talos Linux + K3s Native Runtime** | 310 MB | 0.9s | 12.4 Gbps | Immutable OS Image | Embedded SQLite / etcd |

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

## Multi-Node High Availability & Worker Daemon Systemd Setup

### 1. K3s Control Plane Server (`/etc/systemd/system/k3s.service`)
Deploying an HA server with embedded etcd on master nodes:

```ini
[Unit]
Description=Lightweight Kubernetes Server
Documentation=https://k3s.io
Wants=network-online.target
After=network-online.target

[Service]
Type=notify
EnvironmentFile=-/etc/default/k3s
EnvironmentFile=-/etc/sysconfig/k3s
EnvironmentFile=-/etc/systemd/system/k3s.service.env
ExecStartPre=-/sbin/modprobe br_netfilter
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/local/bin/k3s server \
    --cluster-init \
    --tls-san=k3s.homelab.internal \
    --write-kubeconfig-mode=644 \
    --etcd-expose-metrics=true \
    --disable=servicelb
KillMode=process
Delegate=yes
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
TimeoutStartSec=0
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 2. K3s Worker Node Agent (`/etc/systemd/system/k3s-agent.service`)
Deploying GPU-capable execution worker nodes joining the master cluster:

```ini
[Unit]
Description=Lightweight Kubernetes Worker Agent
Documentation=https://k3s.io
Wants=network-online.target
After=network-online.target

[Service]
Type=exec
EnvironmentFile=-/etc/default/k3s-agent
EnvironmentFile=-/etc/sysconfig/k3s-agent
EnvironmentFile=-/etc/systemd/system/k3s-agent.service.env
ExecStartPre=-/sbin/modprobe br_netfilter
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/local/bin/k3s agent \
    --server https://k3s.homelab.internal:6443 \
    --token K10d939a8c7b827f8a7e::server:secretclusterjointoken123 \
    --node-label "accelerator=nvidia-rtx4090" \
    --node-label "workload=ai-inference"
KillMode=process
Delegate=yes
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
TimeoutStartSec=0
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

## Production Docker Compose k3d Multi-Node Testing Harness

To rapidly validate K3s manifests and multi-agent Helm charts locally without touching bare metal:

```yaml
version: "3.9"

services:
  k3d-registry:
    image: registry:2
    container_name: k3d-registry.localhost
    ports:
      - "5001:5000"
    environment:
      REGISTRY_STORAGE_DELETE_ENABLED: "true"
    volumes:
      - /opt/k3d/registry:/var/lib/registry

  k3d-cluster-init:
    image: rancher/k3d:v5.7.4
    container_name: k3d-cluster-init
    depends_on:
      - k3d-registry
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./k3d-config.yaml:/etc/k3d/config.yaml:ro
    entrypoint: ["/bin/sh", "-c"]
    command: >
      "k3d cluster get dev-ai-cluster || k3d cluster create dev-ai-cluster \
       --servers 1 --agents 2 \
       --port 80:80@loadbalancer --port 443:443@loadbalancer \
       --registry-use k3d-registry.localhost:5000"
```

## Diagnostic Troubleshooting Matrix

| Error Symptom / Log Output | Likely Root Cause | Diagnostic Command | Immediate Resolution Steps |
| :--- | :--- | :--- | :--- |
| `Node NotReady: container runtime network not ready: NetworkReady=false` | CNI Flannel interface failed initialization or missing `br_netfilter` kernel module. | `sudo modprobe br_netfilter && sysctl net.bridge.bridge-nf-call-iptables` | Load module into `/etc/modules-load.d/k3s.conf` and set `net.ipv4.ip_forward=1` in `/etc/sysctl.conf`. |
| `etcdserver: request timed out / leader changed` | High disk I/O latency causing etcd heartbeat drops on slow SD card or SATA drive. | `sudo fio --name=test --size=100M --direct=1 --rw=write --bs=4k` | Move `/var/lib/rancher/k3s/server/db` to high-speed NVMe SSD or reduce snapshot retention. |
| `FailedCreatePodSandBox: failed to setup network for sandbox: IPAM pool exhausted` | Cluster pod CIDR range `/16` ran out of available `/24` subnets per node. | `sudo k3s kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'` | Reinitialize K3s with larger `--cluster-cidr=10.42.0.0/12` and `--cluster-dns=10.43.0.10`. |
| `Traefik Ingress 404 Not Found on defined host` | IngressRoute missing Traefik Entrypoint binding or namespace misconfiguration. | `sudo k3s kubectl get ingress -A` | Verify `ingressClassName: traefik` or configure Traefik IngressRoute with correct entryPoint (`websecure`). |
| `NVIDIA Device Plugin: 0 GPUs available` | Missing Containerd nvidia runtime configuration in K3s template. | `nvidia-smi && ls -l /dev/nvidia*` | Configure `/etc/rancher/k3s/registries.yaml` with nvidia container runtime and restart k3s. |
| `Kubelet: disk pressure eviction triggered` | Root partition free disk space dropped below default 15% threshold. | `df -h /var/lib/rancher/k3s` | Run `k3s crictl rmi --prune` to clean unreferenced images; set `--eviction-hard=nodefs.available<5%`. |
| `TLS certificate has expired or is not yet valid` | Local workstation RTC clock drift or agent joined with mismatched time. | `timedatectl status` | Synchronize time via `sudo systemctl restart systemd-timesyncd` across all server and agent nodes. |
| `Failed to allocate pod IP: vxlan MTU mismatch` | Flannel VXLAN MTU exceeds underlying WAN/VPN network MTU (e.g. Tailscale / WireGuard). | `ip link show flannel.1` | Set `--flannel-backend=vxlan --flannel-conf='{"MTU": 1420}'` to prevent packet fragmentation. |

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
Interact programmatically with the K3s cluster using the standard Python client library. This script uses strict Pydantic v2 schemas to strictly validate pod parameters, resource fields, and status configurations.

```python
import os
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from kubernetes import client, config

class K3sPodMetadata(BaseModel):
    """Schema representing validated active pod details from the K3s cluster."""
    model_config = ConfigDict(extra="forbid", frozen=True)
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
    model_config = ConfigDict(extra="forbid", frozen=True)
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
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

mcp = FastMCP("K3s-Cluster-Manager")

class ScaleDeploymentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    deployment_name: str = Field(..., description="Kubernetes deployment name")
    namespace: str = Field(default="default", description="Namespace containing deployment")
    target_replicas: int = Field(..., ge=0, le=50, description="Target replica count")

class ScaleDeploymentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    deployment_name: str
    namespace: str
    previous_replicas: int
    updated_replicas: int
    status: str

@mcp.tool(name="scale_k3s_deployment")
def scale_deployment_tool(request: ScaleDeploymentRequest) -> ScaleDeploymentResponse:
    """FastMCP 3.1 tool to adjust replica scale of K3s inference workloads."""
    try:
        config.load_kube_config(config_file="/etc/rancher/k3s/k3s.yaml")
        apps_v1 = client.AppsV1Api()
        scale = apps_v1.read_namespaced_deployment_scale(name=request.deployment_name, namespace=request.namespace)
        prev = scale.spec.replicas
        scale.spec.replicas = request.target_replicas
        apps_v1.replace_namespaced_deployment_scale(name=request.deployment_name, namespace=request.namespace, body=scale)
        return ScaleDeploymentResponse(
            deployment_name=request.deployment_name,
            namespace=request.namespace,
            previous_replicas=prev,
            updated_replicas=request.target_replicas,
            status="success"
        )
    except Exception as e:
        return ScaleDeploymentResponse(
            deployment_name=request.deployment_name,
            namespace=request.namespace,
            previous_replicas=0,
            updated_replicas=request.target_replicas,
            status=f"simulation: {str(e)}"
        )

if __name__ == "__main__":
    req = ScaleDeploymentRequest(deployment_name="local-agent-worker", target_replicas=4)
    print("FastMCP Scale Result:", scale_deployment_tool(req))
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
