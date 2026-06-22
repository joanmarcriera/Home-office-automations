# Kubernetes (K3s)

## What it is
K3s is a highly available, certified Kubernetes distribution designed for production workloads in resource-constrained environments like edge devices, IoT, and homelabs. It is developed by Rancher (now SUSE).

## What problem it solves
It simplifies the operation of Kubernetes by bundling necessary components into a single, lightweight binary (~50MB) and automating common tasks like certificate rotation and storage provisioning.

## Where it fits in the stack
**Infrastructure / Deployment**.

## Typical use cases
- **Homelab Orchestration**: Running containerized services (n8n, Paperless, etc.) with high availability.
- **Edge Computing**: Deploying applications on low-power devices like Raspberry Pis.
- **Local Development**: Testing Kubernetes manifests in a lightweight local cluster.

## Strengths
- **Low Footprint**: Minimal resource usage, making it ideal for home servers.
- **Easy Installation**: Can be installed with a single command.
- **Production Grade**: Fully CNCF certified Kubernetes distribution.

## Limitations
- **Single Binary**: While convenient, it differs slightly from "vanilla" Kubernetes in how some components are packaged.
- **Networking**: Uses Flannel by default, which may need replacement for advanced networking requirements.

## When to use it
- For managing multi-container home automation stacks that require auto-scaling or self-healing.
- When you want to learn Kubernetes without the overhead of a full enterprise distribution.

## When not to use it
- In extremely large enterprise environments where a managed service (EKS, GKE) or a full distribution (RKE, OpenShift) is preferred.

## Getting started
K3s is designed for easy installation and low overhead.

### 1. Installation
The simplest way to install K3s on a Linux host is via the official install script:
```bash
curl -sfL https://get.k3s.io | sh -
# Check node status
sudo k3s kubectl get node
```

### 2. Hello World (Deploying a Workload)
Create a file named `whoami.yaml` to deploy a simple web service:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: whoami
spec:
  replicas: 1
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
      - name: whoami
        image: traefik/whoami
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: whoami
spec:
  ports:
  - port: 80
  selector:
    app: whoami
```

Apply the manifest:
```bash
sudo k3s kubectl apply -f whoami.yaml
```

## CLI examples

### Check Cluster Configuration
Verify if your host meets the requirements for running K3s:
```bash
k3s check-config
```

### Manage Nodes
List all nodes in the cluster with additional details:
```bash
sudo k3s kubectl get nodes -o wide
```

### View Server Logs
Monitor the K3s server process logs for troubleshooting:
```bash
sudo journalctl -u k3s -f
```

## API examples
K3s is fully compatible with the standard Kubernetes API. You can use any Kubernetes client, such as the official Python client.

### List Pods (Python)
```python
from kubernetes import client, config

# Load config from the default K3s location
config.load_kube_config(config_file="/etc/rancher/k3s/k3s.yaml")

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free.
- **Self-hostable**: Yes.

## Related tools / concepts
- [Docker](docker.md)
- [Home Assistant (via HASS-K8s)](../../services/home-assistant.md)
- [TrueNAS SCALE (Uses K3s internally)](../../architecture/infrastructure.md)
- [Talos OS](../../knowledge_base/talos-vs-ubuntu-k3s.md)
- [Longhorn](https://longhorn.io/)

## Sources / References
- [Official Website](https://k3s.io/)
- [K3s GitHub](https://github.com/k3s-io/k3s)
- [K3s Documentation](https://docs.k3s.io/)
- [Longhorn Storage](https://longhorn.io/)

## Contribution Metadata
- Last reviewed: 2026-06-02
- Confidence: high
