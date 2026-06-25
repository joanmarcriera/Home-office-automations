# Playbook: 3-Node K3s High Availability Cluster Setup

## What it is

A step-by-step operational guide for deploying a lightweight, highly available Kubernetes cluster using K3s. It focuses on the multi-master (control-plane) configuration with embedded etcd. As of June 2026, K3s v1.31+ and Cilium v1.17+ serve as the baseline for high-performance, agent-ready homelab clusters.

## What problem it solves

Managing a single-node Kubernetes cluster creates a single point of failure. This playbook provides a path to high availability, ensuring the cluster remains operational even if one control-plane node fails. It simplifies the complex process of setting up HA etcd and control-plane components, enabling "Invisible Kubernetes" patterns for autonomous service management.

## Where it fits in the stack

This playbook belongs to the **Infrastructure / Compute** layer. It provides the foundation for hosting all other containerized services and agents in the home-office stack. It enables the use of [EKS Auto Mode](../knowledge_base/invisible_kubernetes.md) style abstractions on-premises.

## Typical use cases

- **Critical Home Services**: Hosting Nextcloud, Home Assistant, and Authentik with 24/7 uptime.
- **Agentic Workflows**: Providing a resilient platform for [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md).
- **Scalable Compute**: Dynamically scaling compute for resource-intensive models like [Claude 4.8](../tools/ai_knowledge/claude.md).
- **Edge Resilience**: Managing small clusters where manual SRE intervention is minimized via autonomous controllers.

## Strengths

- **Low Resource Overhead**: K3s is optimized for edge and IoT, requiring significantly less RAM than vanilla Kubernetes.
- **Embedded etcd**: Simplifies HA by removing the need for an external database for cluster state.
- **Advanced Networking**: Leverages **Cilium** for eBPF-based networking, security, and observability.
- **Production-Ready**: Comes bundled with Traefik (ingress), Klipper (load balancer), and local-path-provisioner.
- **Fast Recovery**: Control-plane nodes can be replaced or added with a single CLI command.

## Limitations

- **etcd Scalability**: Embedded etcd is optimized for 3-5 nodes; very large clusters may require dedicated etcd nodes.
- **Setup Complexity**: HA networking requires a deeper understanding of VIPs (Virtual IPs) or external load balancing than single-node setups.
- **Hardware Minimums**: Requires at least three nodes for true quorum and high availability.

## When to use it

- When you have at least three physical or virtual nodes (e.g., Raspberry Pi 5, Intel NUCs, or Proxmox VMs).
- When you need a "set and forget" Kubernetes environment for mission-critical infrastructure.
- When you want to utilize modern CNI features like [Istio Ambient Mesh](../knowledge_base/invisible_kubernetes.md).

## When not to use it

- If you only have one or two nodes (use a standard K3s server/agent setup instead).
- If your hardware is extremely resource-constrained (< 2GB RAM per node), consider a lighter alternative or single-node K3s.
- If you require manual control over every kernel parameter and K8s component (use `kubeadm` instead).

## Getting started

To deploy a 3-node HA cluster:

1.  **Initialize Node 01**: Run the K3s installer with `--cluster-init`.
2.  **Join Nodes 02 & 03**: Use the token from Node 01 to join as server nodes.
3.  **Install CNI**: Deploy [Cilium](https://cilium.io/) for networking.
4.  **Configure VIP**: Set up a virtual IP (using Keepalived or Kube-Vip) for the control plane.
5.  **Step-by-Step Flow**:
    ```mermaid
    flowchart TD
        A[Node 01: k3s server --cluster-init] --> B[Retrieve Node Token]
        B --> C[Node 02: k3s server --server Node01]
        C --> D[Node 03: k3s server --server Node01]
        D --> E[Install Cilium CNI]
        E --> F[Verify HA Status: kubectl get nodes]
    ```

## CLI examples

### Initializing the HA Cluster (Node 01)
Disabling default Flannel and Network Policy to use Cilium:
```bash
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san k8s-vip.home.arpa \
  --flannel-backend=none \
  --disable-network-policy
```

### Joining a Second Server Node
Joining `node-02` to the cluster initialized by `node-01`:
```bash
# On Node 02
curl -sfL https://get.k3s.io | K3S_TOKEN=YOUR_NODE_TOKEN sh -s - server \
  --server https://node-01.home.arpa:6443 \
  --flannel-backend=none \
  --disable-network-policy
```

### Installing Cilium CNI
Using the Cilium CLI to install eBPF networking:
```bash
cilium install --version 1.17.0
```

## API examples

### Checking Node Health (Python)
An agent might use the Kubernetes API to verify the health of the 3-node cluster:
```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()

def check_cluster_health():
    nodes = v1.list_node()
    ready_nodes = [node for node in nodes.items if any(c.type == 'Ready' and c.status == 'True' for c in node.status.conditions)]
    print(f"Cluster Health: {len(ready_nodes)}/{len(nodes.items)} nodes are Ready.")

check_cluster_health()
```

### Dynamic Ingress Definition (YAML)
Creating a Traefik IngressRoute for a newly deployed agent service:
```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: jules-agent-route
  namespace: default
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`jules.home.arpa`)
      kind: Rule
      services:
        - name: jules-service
          port: 8080
```

## Related tools / concepts

- [NFS CSI Setup](nfs-csi-setup.md): Persistent storage for HA clusters.
- [Talos OS vs Ubuntu K3s](../knowledge_base/talos-vs-ubuntu-k3s.md): Comparing underlying operating systems.
- [Invisible Kubernetes](../knowledge_base/invisible_kubernetes.md): The architectural goal of this setup.
- [Authentik](../services/authentik.md): Identity management for cluster services.
- [Headscale](../services/headscale.md): Secure mesh networking for cross-site nodes.
- [Longhorn](../architecture/infrastructure.md): Cloud-native distributed block storage.
- [MetalLB](../architecture/infrastructure.md): Load-balancer provider for bare-metal K3s.

## Sources / References

- [K3s High Availability with Embedded etcd (Official Docs)](https://docs.k3s.io/datastore/ha-embedded)
- [Cilium: Getting Started with K3s](https://docs.cilium.io/en/stable/gettingstarted/k3s/)
- [K3s v1.31 Release Notes (GitHub)](https://github.com/k3s-io/k3s/releases)
- [Managing K3s Clusters with Helm](https://docs.k3s.io/helm)

## Contribution Metadata

- Last reviewed: 2026-06-25
- Confidence: high
