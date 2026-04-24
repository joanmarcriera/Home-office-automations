# Playbook: 3-Node K3s High Availability Cluster Setup

This playbook describes how to deploy a production-ready, highly available K3s cluster with three control-plane nodes.

## Overview
A 3-node HA setup uses an embedded etcd database for the control plane, providing resilience against the failure of any single node.

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

## Sources / References
- [K3s High Availability with Embedded etcd](https://docs.k3s.io/datastore/ha-embedded)
- [K3s Installation Options](https://docs.k3s.io/installation/configuration)

## Contribution Metadata
- Last reviewed: 2026-04-24
- Confidence: high
