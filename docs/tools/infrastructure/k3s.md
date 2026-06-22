# Kubernetes (K3s)

## What it is
K3s is a highly available, certified Kubernetes distribution designed for production workloads in resource-constrained environments like edge devices, IoT, and homelabs. Developed by Rancher (now SUSE), it is the industry standard for lightweight container orchestration as of June 2026.

## What problem it solves
It simplifies the operation of Kubernetes by bundling necessary components into a single, lightweight binary (~50MB) and automating complex tasks like certificate rotation, storage provisioning, and multi-architecture cluster management. It removes the "Kubernetes tax" for small-to-medium deployments.

## Where it fits in the stack
**Infrastructure / Deployment**. It serves as the foundational orchestration layer for hosting agentic services, databases, and workflow engines (n8n, Langflow) in private or edge clouds.

## Typical use cases
- **Homelab Orchestration**: Running containerized services like Home Assistant, Paperless-ngx, and Nextcloud with high availability.
- **Edge AI Deployment**: Running lightweight inference engines (Ollama, vLLM) on low-power devices.
- **Local Development**: Testing production-grade Kubernetes manifests on a laptop without the overhead of Minikube.
- **Agentic Clusters**: Managing fleets of specialized agents across multiple Raspberry Pi or Jetson nodes.

## Strengths
- **Low Footprint**: Minimal resource usage (under 512MB RAM for the server), ideal for home servers.
- **Single Binary**: Easy installation and updates via a single executable.
- **Production Grade**: Fully CNCF certified; what runs on K3s will run on EKS/GKE.
- **Integrated Storage/Networking**: Comes with Flannel (networking), CoreDNS, and Local Storage Provisioner out of the box.

## Limitations
- **Single-Node DB by Default**: Uses SQLite for state by default; requires external DB (Postgres/ETCD) for true high availability.
- **Networking Constraints**: The default Flannel CNI may lack advanced features found in Cilium or Calico (though these can be swapped).
- **Manual Scaling**: Unlike managed cloud services, hardware scaling and cluster expansion require manual node provisioning.

## When to use it
- When managing a multi-container home automation stack that requires auto-scaling or self-healing.
- When deploying agentic workflows that need to survive hardware failures.
- When running Kubernetes on ARM64 or other non-x86 architectures.

## When not to use it
- For massive, thousands-of-nodes enterprise deployments where a full ETCD-backed distribution (RKE2, K8s) is standard.
- If you require deep, out-of-the-box integration with proprietary cloud APIs (use managed services like EKS instead).

## Getting started

### Installation
The standard installation uses the official script:
```bash
curl -sfL https://get.k3s.io | sh -
# Verify installation
sudo k3s kubectl get nodes
```

### Deploying a Service
Create a file `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-agent
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-agent
  template:
    metadata:
      labels:
        app: web-agent
    spec:
      containers:
      - name: web-agent
        image: nginx:alpine
```
Apply to the cluster:
```bash
sudo k3s kubectl apply -f deployment.yaml
```

## CLI examples

### Cluster Health Check
```bash
# Check if host is ready for K3s
k3s check-config
```

### Resource Management
```bash
# Get all pods across all namespaces
sudo k3s kubectl get pods -A

# Describe a specific node to check resource pressure
sudo k3s kubectl describe node <node-name>
```

### Log Monitoring
```bash
# Follow server process logs
sudo journalctl -u k3s -f
```

## API examples
K3s is fully compatible with the standard Kubernetes API.

### Listing Pods (Python)
```python
from kubernetes import client, config

# Load config from the standard K3s location
config.load_kube_config(config_file="/etc/rancher/k3s/k3s.yaml")

v1 = client.CoreV1Api()
print("Cluster Pods:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free.
- **Self-hostable**: Yes.

## Related tools / concepts
- [Docker](docker.md) — The underlying container technology.
- [Home Assistant (via HASS-K8s)](../../services/home-assistant.md) — Common workload.
- [Talos OS](../../knowledge_base/talos-vs-ubuntu-k3s.md) — Immutable alternative for K3s.
- [Longhorn](https://longhorn.io/) — Distributed block storage for K3s.
- [Ollama](../../services/ollama.md) — Local LLM runner often deployed on K3s.
- [n8n](../../services/n8n.md) — Workflow automation runner.
- [Argo Workflows](../orchestration/argo-workflows.md) — Kubernetes-native workflow engine.
- [Kestra](../orchestration/kestra.md) — Event-driven orchestrator compatible with K3s.

## Sources / references
- [K3s Official Website](https://k3s.io/)
- [K3s GitHub Repository](https://github.com/k3s-io/k3s)
- [K3s Documentation](https://docs.k3s.io/)
- [SUSE Rancher](https://www.rancher.com/)
- [CNCF Landscape](https://landscape.cncf.io/)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
