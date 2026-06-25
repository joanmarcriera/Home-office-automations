# Home Lab Architecture Overview

## What it is

The Home Lab Architecture is a multi-layered infrastructure design built on **TrueNAS SCALE** and **K3s**. As of June 2026, the architecture has evolved to support high-density AI workloads using **NVMe-over-Fabrics (NVMe-oF)**, dedicated GPU pools, and [EKS Auto Mode](../knowledge_base/invisible_kubernetes.md) patterns for "Invisible Kubernetes" orchestration.

## What problem it solves

Self-hosting a complex stack of AI and automation tools requires a stable, scalable, and secure environment. This architecture solves the problem of "service sprawl" by centralizing compute and storage, ensuring data integrity through ZFS, and providing a standardized way to deploy, network, and backup local services using automated [Karpenter](../knowledge_base/invisible_kubernetes.md) scaling.

## Where it fits in the stack

**Category**: Architecture / Infrastructure. It is the **foundation layer** of the entire system, providing the hardware abstraction, storage primitives, and container orchestration (Docker/K8s) upon which all other services and tools are built. It integrates natively with [Cilium v1.17+](https://cilium.io/) for high-performance networking.

## Typical use cases

- **Centralized Data Lake**: Storing all family documents, media, and backups in a high-availability ZFS pool.
- **Local AI Hosting**: Running [Claude 4.8](../tools/ai_knowledge/claude.md) (via local hooks) and [GPT-5.5](../tools/ai_knowledge/openai.md) reasoning loops on local GPU/CPU hardware.
- **Service Orchestration**: Deploying and managing a suite of interrelated tools (n8n, Paperless, Nextcloud) as a cohesive unit.
- **Secure Remote Access**: Connecting to the home lab via [Tailscale](../services/tailscale.md) without exposing ports to the open internet.

## Strengths

- **Data Integrity**: ZFS provides snapshots, replication, and self-healing to protect against data corruption.
- **Scalability**: EKS Auto Mode and Karpenter allow the cluster to scale resources dynamically based on workload demand.
- **Privacy**: All processing and storage happen locally, ensuring sensitive family data remains private.
- **AI-Ready Storage**: High-IOPS NVMe pools ensure that large model weights (Llama 4 Maverick) load in seconds.

## Limitations

- **Hardware Dependency**: Reliability is tied to the physical health of local servers and networking equipment.
- **Complexity**: Requires significant technical expertise to manage ZFS and K3s clusters.
- **Power Consumption**: High-performance AI hardware can significantly increase electricity costs.

## When to use it

- When you want to host your own "private cloud" for family or small business use.
- When you need a high-performance environment for running local AI models ([Ollama](../services/ollama.md), [LiteLLM](../tools/development_ops/litellm.md)).
- When you prioritize data ownership and privacy over the convenience of public cloud services.

## When not to use it

- If you do not have the technical skills or time to manage a Linux-based server environment.
- For extremely high-availability applications that require multi-region geographical redundancy.
- If your compute needs are very low and can be served by a simple NAS or low-power SBC.

## Getting started

To deploy the standard June 2026 infrastructure:

1.  **Hardware Provisioning**: Setup a server with at least 64GB RAM and an NVIDIA RTX 4090/5090.
2.  **OS Installation**: Install TrueNAS SCALE (Cobia or Dragonfish releases).
3.  **Cluster Setup**: Deploy K3s using the [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md) playbook.
4.  **Networking**: Configure [Tailscale](../services/tailscale.md) and [Cilium](https://cilium.io/) for secure mesh connectivity.
5.  **Storage**: Configure [NFS CSI](../playbooks/nfs-csi-setup.md) for dynamic persistent volume provisioning.

## CLI examples

```bash
# Check the status of the K3s cluster nodes
kubectl get nodes -o wide

# Monitor GPU utilization on the AI node
nvidia-smi -l 1

# Check ZFS pool health on TrueNAS
zpool status -v

# Verify Karpenter node scaling events
kubectl get events -n karpenter --field-selector involvedObject.kind=Node
```

## API examples

```yaml
# Example of a Karpenter NodePool for AI workloads (June 2026)
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: gpu-pool
spec:
  template:
    spec:
      requirements:
        - key: "node.kubernetes.io/instance-type"
          operator: In
          values: ["p4d.24xlarge", "g5.12xlarge"] # Or local equivalents
        - key: "karpenter.sh/capacity-type"
          operator: In
          values: ["on-demand"]
      taints:
        - key: "nvidia.com/gpu"
          value: "true"
          effect: "NoSchedule"
  disruption:
    consolidationPolicy: WhenUnderutilized
```

## Related tools / concepts

- [Tailscale](../services/tailscale.md)
- [Nextcloud](../services/nextcloud.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [Ollama](../services/ollama.md)
- [n8n](../services/n8n.md)
- [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md)
- [NFS CSI Setup](../playbooks/nfs-csi-setup.md)
- [Invisible Kubernetes](../knowledge_base/invisible_kubernetes.md)
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md)

## Sources / References

- [TrueNAS SCALE Official Documentation](https://www.truenas.com/docs/scale/)
- [Karpenter Documentation](https://karpenter.sh/docs/)
- [Cilium Networking Guide](https://docs.cilium.io/en/stable/)
- [ZFS on Linux Reference](https://openzfs.github.io/openzfs-docs/)

## Contribution Metadata

- Last reviewed: 2026-06-25
- Confidence: high
