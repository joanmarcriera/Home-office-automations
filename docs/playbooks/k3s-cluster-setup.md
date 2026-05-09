# Playbook: 3-Node K3s High Availability Cluster Setup

## What it is
A step-by-step operational guide for deploying a lightweight, highly available Kubernetes cluster using K3s. It focuses on the multi-master (control-plane) configuration with embedded etcd.

## What problem it solves
Managing a single-node Kubernetes cluster creates a single point of failure. This playbook provides a path to high availability, ensuring the cluster remains operational even if one control-plane node fails. It simplifies the complex process of setting up HA etcd and control-plane components.

## Where it fits in the stack
This playbook belongs to the **Infrastructure / Compute** layer. It provides the foundation for hosting all other containerized services and agents in the home-office stack.

## Typical use cases
- Hosting critical home-office services (Nextcloud, Home Assistant, Authentik) that require 24/7 uptime.
- Learning Kubernetes HA concepts in a resource-constrained environment (e.g., Raspberry Pi or old laptops).
- Building a resilient platform for multi-agent KnowledgeOps workflows.

## Strengths
- **Low Resource Overhead**: K3s is optimized for edge and IoT, making it much lighter than vanilla K8s (kubeadm).
- **Simple HA**: Embedded etcd removes the need for an external database (like Postgres) for the control-plane state.
- **Production-Ready**: Includes bundled components like Traefik, Local Storage Provider, and CoreDNS.

## Limitations
- **Scaling Limits**: Embedded etcd is ideal for small clusters (3-5 nodes) but may struggle with very large-scale deployments compared to a dedicated etcd cluster.
- **Complexity**: While simpler than vanilla K8s, an HA setup still requires more networking and maintenance knowledge than a single-node setup.

## When to use it
- When you have at least three physical or virtual nodes available.
- When you need a resilient Kubernetes environment for "mission-critical" home lab services.
- When you want to minimize the manual configuration required for HA.

## When not to use it
- If you only have one or two nodes (use a standard K3s server-agent setup instead).
- If your hardware is extremely resource-constrained (e.g., < 1GB RAM per node), consider a lighter alternative or a single-node setup.
- If you require a non-Kubernetes container orchestrator (e.g., Docker Swarm).

## Prerequisites
- 3 Linux nodes (e.g., Ubuntu 24.04 or Talos OS).
- Static IP addresses for all nodes.
- SSH access between nodes (or console access).

## Step 1: Initialize the First Node
On the first node (`node-01`), run:
```bash
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san <cluster-vip-or-fqdn>
```

## Step 2: Join the Second and Third Nodes
Retrieve the node token from `node-01`:
```bash
cat /var/lib/rancher/k3s/server/node-token
```

On `node-02` and `node-03`, run:
```bash
curl -sfL https://get.k3s.io | sh -s - server \
  --server https://<node-01-ip>:6443 \
  --token <node-token>
```

## Step 3: Verify the Cluster
Check the status of the nodes:
```bash
kubectl get nodes
```
Ensure all 3 nodes show `Ready` and have the `control-plane,master` roles.

## Step 4: Configuration Details
- **Storage**: By default, K3s uses local storage. For HA, it is recommended to use [Longhorn](../reference-implementations/k8s-infrastructure/storage/longhorn-values.yaml) or [NFS CSI](../playbooks/nfs-csi-setup.md).
- **Networking**: [MetalLB](../reference-implementations/k8s-infrastructure/metallb/) should be configured for LoadBalancer services.

## Related tools / concepts
- [NFS CSI Setup](nfs-csi-setup.md) — for persistent shared storage across the cluster.
- [Talos OS vs Ubuntu K3s](../knowledge_base/talos-vs-ubuntu-k3s.md) — for choosing the underlying operating system.
- [Invisible Kubernetes](../knowledge_base/invisible_kubernetes.md) — philosophical overview of keeping K8s management low-touch.
- [Authentik](../services/authentik.md) — for identity management on top of the cluster.
- [Gitea](../services/gitea.md) — for hosting GitOps configurations.
- [Tailscale to Headscale Migration](tailscale-to-headscale-migration.md) — for secure cluster interconnectivity.
- [Raspberry Pi Kiosk Automation](raspberry-pi-kiosk-automation.md) — as a typical edge node use case.
- [Home Assistant](../services/home-assistant.md) — a primary service candidate for HA hosting.

## Sources / References
- [K3s High Availability with Embedded etcd](https://docs.k3s.io/datastore/ha-embedded)
- [K3s Installation Options](https://docs.k3s.io/installation/configuration)

## Contribution Metadata
- Last reviewed: 2026-05-09
- Confidence: high
