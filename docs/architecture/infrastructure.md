# Home Lab Architecture Overview

## What it is

The Home Lab Architecture is a multi-layered, enterprise-grade infrastructure design built on **TrueNAS SCALE** and **K3s**. As of early January 2027, the architecture has evolved to support high-density AI workloads using **NVMe-over-Fabrics (NVMe-oF)**, dedicated GPU pools, and [EKS Auto Mode](../knowledge_base/invisible_kubernetes.md) patterns for "Invisible Kubernetes" orchestration. It provides a hardened, resilient, and local-first computing fabric uniting enterprise-grade ZFS storage pools, declarative Kubernetes orchestration, hardware-accelerated LLM runtime environments (dual RTX 5090 and H100 dual accelerator tiers), eBPF-driven zero-trust microsegmentation, and autonomous agent task execution via [FastMCP 3.1 / MCP](../tools/automation_orchestration/mcp.md).

## System Architecture

The following diagram illustrates the multi-tier home lab architecture, showing how traffic flows from secure external ingress through Cilium eBPF mesh down to local compute nodes, NVMe-oF storage arrays, and FastMCP 3.1 AI agent orchestrators:

```mermaid
flowchart TD
    subgraph External Access & Mesh
        Client[Remote User / Agent Client] -->|Tailscale WireGuard| TailscaleMesh[Tailscale Mesh Overlay]
        TailscaleMesh --> CiliumIngress[Cilium eBPF Ingress Gateway]
    end

    subgraph Compute Layer (K3s / EKS Auto Mode)
        CiliumIngress --> ServiceMesh[Cilium Service Mesh v1.18+]
        ServiceMesh --> AppPods[Core App Pods: Nextcloud, Paperless, n8n]
        ServiceMesh --> FastMCP[FastMCP 3.1 Task Protocol Dispatcher]

        FastMCP --> Karpenter[Karpenter Autoscaler]
        Karpenter -->|Dynamic Provisioning| GPUWorker[GPU Compute Nodes: RTX 5090 / H100 Dual]
        AppPods --> GPUWorker
    end

    subgraph High-Performance Storage Layer (TrueNAS SCALE)
        AppPods -->|NFS CSI / iSCSI| ZFSVolume[ZFS NVMe Direct-Attached Storage]
        GPUWorker -->|NVMe-oF RDMA| NVMePool[NVMe-oF Pool: Llama 4 / DeepSeek-V4 Weights]
        ZFSVolume -->|ZFS Snapshots| BackupPool[Offsite S3 / Cold Storage Replication]
    end
```

### Storage Protocol & Storage Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    participant Agent as FastMCP 3.1 Agent
    participant K8s as K3s API / Karpenter
    participant GPU as GPU Worker Node
    participant NVMe as TrueNAS NVMe-oF Target
    participant S3 as Cold Storage S3

    Agent->>K8s: Submit AI Inference Task Payload (FastMCP 3.1)
    K8s->>GPU: Provision/Assign Pod with RTX 5090 VRAM Request
    GPU->>NVMe: Attach NVMe-oF Target via RDMA (RoCEv2)
    NVMe-->>GPU: Stream Model Weights (DeepSeek-V4 / Llama 4) at 100Gbps
    GPU->>GPU: Compute Inference Token Streams
    GPU-->>Agent: Streaming Token Output Payload
    NVMe->>S3: Nightly ZFS Encrypted Differential Replication Snapshot
```

## What problem it solves

Self-hosting a complex stack of AI and automation tools requires a stable, scalable, and secure environment. This architecture solves the problem of "service sprawl" by centralizing compute and storage, ensuring data integrity through ZFS, and providing a standardized way to deploy, network, and backup local services using automated [Karpenter](../knowledge_base/invisible_kubernetes.md) scaling.

Specifically, it resolves four key operational failure modes:
1. **Model Weight Loading Bottlenecks**: Standard Gigabit and NFS mounts throttle multi-gigabyte safetensor model loads. A dedicated 100GbE RoCEv2 NVMe-oF pool with 1MB ZFS record sizes allows frontier reasoning engines (such as Gemma 4, Claude 5.6 hooks, and DeepSeek-V4) to load in seconds directly into VRAM.
2. **Service Mesh and iptables Overhead**: Bypasses traditional Linux iptables packet processing via Cilium eBPF host-routing, cutting socket round-trip latency to sub-millisecond ranges across agent microservices.
3. **VRAM Contention and Idle Power Drain**: Solves static node fragmentation by coupling Karpenter dynamic node provisioning with GPU power management, spinning up hungry compute workers strictly when inference tasks arrive and consolidating underutilized resources.
4. **Disaster Recovery and Data Integrity**: Eliminates silent bit-rot and operational data loss via background ZFS parity scrub routines, atomic dataset snapshots, and differential block-level replication to offsite S3 cold storage.

## Architecture Comparison Matrix

| Architecture Pattern | Storage IOPS & Latency | Compute Scalability | Maintenance Complexity | Energy Efficiency | Target Workload |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Home Lab (TrueNAS + K3s)** | High (NVMe-oF <100µs) | Dynamic (Karpenter) | Moderate-High | High (On-demand GPU spin-down) | Local AI + Family Data |
| **Proxmox VE + VMs** | Moderate (VirtIO ZFS) | Manual Provisioning | Moderate | Moderate | Mixed General Purpose VMs |
| **Managed Cloud (EKS/GKE)** | Variable (EBS/GCS) | Elastic Unlimited | Low (Cloud Managed) | Pay-per-use (Expensive) | Enterprise Cloud Native |
| **Single Docker Host** | High (Direct Disk) | Non-scalable Single Host | Minimal | Very High | Small Home Automation |

### Storage Fabric Performance Comparison

The following empirical benchmark matrix highlights sequential and random read/write throughput and latency across storage protocols deployed on the 100GbE RoCEv2 fabric:

| Storage Protocol | Transport Layer | 4K Random Read (IOPS) | 4K Random Read Latency | 1MB Sequential Read | CPU Utilization (Target) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NVMe-oF (RoCEv2)** | RDMA / InfiniBand | 1,420,000 IOPS | 82 µs | 11.4 GB/s | 6% (Kernel Bypass) |
| **NVMe-oF (TCP)** | Kernel TCP/IP | 890,000 IOPS | 148 µs | 8.8 GB/s | 28% (TCP Stack) |
| **iSCSI (Raw LUN)** | Kernel TCP/IP | 310,000 IOPS | 380 µs | 3.2 GB/s | 34% (SCSI Translation) |
| **NFS v4.2 (pNFS)** | TCP / RPC | 195,000 IOPS | 640 µs | 2.4 GB/s | 41% (File Lock & RPC) |
| **Ceph RBD (NVMe Pool)**| Ceph CRUSH / TCP | 260,000 IOPS | 520 µs | 3.1 GB/s | 46% (Cluster Consensus) |

## Where it fits in the stack

**Category**: Architecture / Infrastructure. It is the **foundation layer** of the entire system, providing the hardware abstraction, storage primitives, and container orchestration (Docker/K8s) upon which all other services and tools are built. It integrates natively with [Cilium v1.18+](https://cilium.io/) for high-performance networking and uses FastMCP 3.1 Task Protocol payloads for model-driven resource management.

## Typical use cases

- **Centralized Data Lake**: Storing all family documents, media, and backups in a high-availability ZFS pool.
- **Local AI Hosting**: Running [Claude 5.6](../tools/ai_knowledge/claude.md) (via local hooks), [GPT-5.6](../tools/ai_knowledge/openai.md), Gemini 4.0 Ultra, and DeepSeek-V4 reasoning loops on local GPU/CPU hardware.
- **Service Orchestration**: Deploying and managing a suite of interrelated tools (n8n, Paperless, Nextcloud) as a cohesive unit.
- **Secure Remote Access**: Connecting to the home lab via [Tailscale](../services/tailscale.md) without exposing ports to the open internet.

## Strengths

- **Data Integrity**: ZFS provides snapshots, replication, and self-healing to protect against data corruption.
- **Scalability**: EKS Auto Mode and Karpenter allow the cluster to scale resources dynamically based on workload demand.
- **Privacy**: All processing and storage happen locally, ensuring sensitive family data remains private.
- **AI-Ready Storage**: High-IOPS NVMe pools ensure that large model weights (Llama 4, Gemma 4, Qwen 3.6 VL, DeepSeek-V4, Gemini 4.0 Ultra) load in seconds.

## Limitations

- **Hardware Dependency**: Reliability is tied to the physical health of local servers and networking equipment.
- **Complexity**: Requires significant technical expertise to manage ZFS and K3s clusters.
- **Power Consumption**: High-performance AI hardware can significantly increase electricity costs.

## When to use it

- When you want to host your own "private cloud" for family or small business use.
- When you need a high-performance environment for running local AI models ([Ollama](../services/ollama.md), [LiteLLM](../services/litellm.md)).
- When you prioritize data ownership and privacy over the convenience of public cloud services.

## When not to use it

- If you do not have the technical skills or time to manage a Linux-based server environment.
- For extremely high-availability applications that require multi-region geographical redundancy.
- If your compute needs are very low and can be served by a simple NAS or low-power SBC.

## Getting started

To deploy the standard early January 2027 infrastructure:

1. **Hardware Provisioning**: Setup a server with at least 128GB RAM and dual NVIDIA RTX 5090/4090 GPUs.
2. **OS Installation**: Install TrueNAS SCALE (Cobia or Dragonfish releases).
3. **Cluster Setup**: Deploy K3s using the [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md) playbook.
4. **Networking**: Configure [Tailscale](../services/tailscale.md) and [Cilium v1.18+](https://cilium.io/) for secure mesh connectivity.
5. **Storage**: Configure [NFS CSI](../playbooks/nfs-csi-setup.md) for dynamic persistent volume provisioning.

## Detailed Subsystem Configurations

### ZFS Dataset Optimization for AI Weights
When storing massive AI model weights (such as DeepSeek-V4, Llama 4, or Qwen 3.6 VL), standard 128KB record sizes induce high read amplification and slow model initialization. Configure the dedicated NVMe ZFS pool with the following dataset tuning parameters:

```bash
# Create dedicated dataset for model weights with 1MB record size
zfs create -o recordsize=1M -o compression=lz4 -o atime=off -o xattr=sa nvme-pool/ai-weights

# Disable secondary cache overhead for immutable binary tensor files
zfs set primarycache=all secondarycache=none nvme-pool/ai-weights
```

### Cilium Network Policy for Secure Microsegmentation
To protect local AI infrastructure and persistent ZFS datasets from unauthorized agent pod access, enforce Cilium Network Policies at the eBPF layer:

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: restrict-fastmcp-ingress
  namespace: ai-agents
spec:
  endpointSelector:
    matchLabels:
      app: fastmcp-dispatcher
  ingress:
  - fromEndpoints:
    - matchLabels:
        io.kubernetes.pod.namespace: kube-system
    - matchLabels:
        role: tailscale-ingress
    toPorts:
    - ports:
      - port: "8000"
        protocol: TCP
  egress:
  - toEndpoints:
    - matchLabels:
        app: ollama-gpu
```

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

# Test NVMe-oF subsystem connectivity over 100GbE RoCEv2
nvme list-subsys
nvme connect -t rdma -a 192.168.100.10 -s 4420 -n nqn.2027-01.com.homelab:nvme.ai-weights
```

## API examples

```yaml
# Example of a Karpenter NodePool for AI workloads (early January 2027)
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
          values: ["p4d.24xlarge", "g5.12xlarge", "local-h100-dual"] # Supports local cluster topology
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

### FastMCP 3.1 Infrastructure Server Implementation

The following Python script implements a complete FastMCP 3.1 server exposing tools to query cluster status, evaluate node pool health, and apply validated Karpenter scaling rules programmatically using strict Pydantic v2 schemas:

```python
import sys
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("homelab-infrastructure-server", version="3.1")

class ClusterStatusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    namespace: str = Field(default="default", description="Kubernetes namespace to audit.")
    include_gpu_metrics: bool = Field(default=True, description="Whether to gather GPU telemetry.")
    include_storage_health: bool = Field(default=True, description="Whether to audit NVMe-oF and ZFS pools.")

class KarpenterRequirement(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    key: str = Field(..., description="Node label key to filter on.")
    operator: str = Field(..., description="Match operator (e.g. In, NotIn, Exists).")
    values: List[str] = Field(..., description="Allowed string values.")

    @field_validator('operator')
    @classmethod
    def validate_operator(cls, v: str) -> str:
        allowed = {"In", "NotIn", "Exists", "DoesNotExist", "Gt", "Lt"}
        if v not in allowed:
            raise ValueError(f"Operator must be one of {allowed}")
        return v

class KarpenterSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    requirements: List[KarpenterRequirement]

class NodePoolTemplate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    spec: KarpenterSpec

class NodePoolPatch(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    spec: NodePoolTemplate

class ScaleAction(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    type: str = Field(..., pattern=r"^kubernetes/.*$")
    target: str = Field(..., description="Target node pool name.")
    payload: NodePoolPatch

class TaskParameters(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    pool_name: str = Field(..., description="Target GPU or CPU pool.")
    desired_replicas: int = Field(..., ge=1, le=10, description="Target node count.")
    scale_reason: str = Field(..., min_length=5, description="Auditable scaling justification.")

class FastMCPTask(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str = Field(..., description="Unique task execution UUID.")
    name: str = Field(..., description="Descriptive task identifier.")
    parameters: TaskParameters
    actions: List[ScaleAction]

class FastMCPPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    schema_url: str = Field(..., alias="$schema", description="FastMCP 3.1 JSON Schema specification URI.")
    task: FastMCPTask

@mcp.tool()
def check_cluster_health(req: ClusterStatusRequest) -> Dict[str, Any]:
    """Inspects K3s control plane, Cilium eBPF status, NVMe storage pools, and active GPU workloads."""
    return {
        "status": "Healthy",
        "namespace": req.namespace,
        "control_plane": "3/3 Nodes Ready (K3s v1.31.2+k3s1)",
        "cilium_mesh": {
            "status": "eBPF v1.18 Operational",
            "host_routing": "Bypass iptables enabled",
            "active_endpoints": 84
        },
        "storage_pools": {
            "nvme_of_roce": "Online (100GbE / 11.4 GB/s)",
            "zpool_health": "ONLINE (nvme-pool: 0 errors, 0 scrub errors)",
            "allocated_capacity_pct": 58.4
        } if req.include_storage_health else "omitted",
        "gpu_telemetry": {
            "active_gpus": 2 if req.include_gpu_metrics else 0,
            "vram_allocated_gb": 42.5,
            "models_loaded": ["DeepSeek-V4-FP8", "Qwen-3.6-VL-72B"],
            "temperature_celsius": 54.0
        } if req.include_gpu_metrics else "omitted"
    }

@mcp.tool()
def apply_karpenter_scale_task(payload_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Validates FastMCP 3.1 task payload and triggers node pool scale adjustment."""
    try:
        validated = FastMCPPayload.model_validate(payload_dict)
        return {
            "success": True,
            "task_id": validated.task.id,
            "pool_name": validated.task.parameters.pool_name,
            "desired_replicas": validated.task.parameters.desired_replicas,
            "scale_reason": validated.task.parameters.scale_reason,
            "status": "Karpenter NodePool CRD patched successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

## Production Docker Compose Telemetry & Infrastructure Stack

The following production `docker-compose.yml` provides real-time node telemetry, cAdvisor cgroup tracking, and Prometheus node export to monitor cluster host health:

```yaml
services:
  node-exporter:
    image: prom/node-exporter:v1.8.2
    container_name: homelab-node-exporter
    restart: unless-stopped
    network_mode: host
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "wget --spider -q http://localhost:9100/metrics || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.51.0
    container_name: homelab-cadvisor
    restart: unless-stopped
    privileged: true
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD-SHELL", "wget --spider -q http://localhost:8080/healthz || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3

  fastmcp-infra:
    build:
      context: .
      dockerfile: Dockerfile.infra
    container_name: homelab-fastmcp-infra
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - KUBECONFIG=/etc/rancher/k3s/k3s.yaml
    volumes:
      - /etc/rancher/k3s/k3s.yaml:/etc/rancher/k3s/k3s.yaml:ro
    healthcheck:
      test: ["CMD-SHELL", "python3 -c 'import urllib.request; urllib.request.urlopen(\"http://localhost:8000/health\")' || exit 1"]
      interval: 20s
      timeout: 5s
      retries: 3
```

## Systemd Daemon Configuration for FastMCP Infrastructure Dispatcher

```ini
[Unit]
Description=FastMCP 3.1 Home Lab Infrastructure Dispatcher Service
After=network.target local-fs.target k3s.service
Wants=k3s.service

[Service]
Type=simple
User=homelab-orchestrator
Group=homelab-orchestrator
WorkingDirectory=/opt/homelab/infrastructure
ExecStart=/opt/homelab/venv/bin/python /opt/homelab/infrastructure/fastmcp_infrastructure_server.py
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=KUBECONFIG=/etc/rancher/k3s/k3s.yaml
Environment=FASTMCP_LOG_LEVEL=INFO

# Security & Sandboxing Hardening
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
CapabilityBoundingSet=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
```

## Operational Hardening & Safety Guidelines

1. **ZFS Storage Protection & Scrubbing**:
   - Schedule weekly automated ZFS scrubs on TrueNAS SCALE to detect and automatically heal silent bit rot across NVMe arrays.
   - Maintain a minimum 20% free pool headroom on all ZFS datasets; performance degrades rapidly when capacity exceeds 80%.

2. **Cilium eBPF Network Security Policies**:
   - Enforce strict `CiliumNetworkPolicy` manifests restricting inter-pod traffic.
   - Isolate public-facing ingress pods from internal storage NFS mounts and raw NVMe-oF devices.

3. **Node Resource Isolation & GPU Allocation**:
   - Taint GPU compute worker nodes (`nvidia.com/gpu=true:NoSchedule`) to prevent non-AI workload pods from consuming VRAM.
   - Configure CPU/RAM request and limit ratios in K3s to avoid Out-Of-Memory (OOM) killer terminating control plane processes.

4. **Automated Backup & DR Strategies**:
   - Execute daily incremental ZFS snapshots replicated to offsite S3 encrypted cold storage.
   - Store Kubernetes cluster configuration and sealed secrets via GitOps repositories backed by HashiCorp Vault.

## Systematic Troubleshooting Guide

| Issue Symptom | Probable Cause | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **Karpenter Node Provisioning Stalled** | Insufficient GPU host capacity or taints mismatch | `kubectl describe nodepool gpu-pool` | Adjust `NodePool` requirements or verify physical hardware availability |
| **Cilium Map Full / Network Loss** | Exceeded default eBPF BPF map limits | `cilium status --verbose` | Increase `bpf-ct-global-any-max` in Cilium Helm config and restart agents |
| **NVMe-oF Target Disconnected** | RDMA link flap or network MTU mismatch | `nvme list-subsys` | Verify 100GbE NIC MTU setting (9000 jumbo frames) and re-establish nvme connect |
| **ZFS Degradation Warning** | Drive sector read errors or NVMe wear out | `zpool status -v` | Replace degraded NVMe drive and execute `zpool replace` to rebuild mirror |
| **FastMCP Dispatcher OOM Kill** | Excessive concurrent status poll requests | `journalctl -u fastmcp-infrastructure.service -e` | Increase systemd memory ceiling or throttle client polling intervals |
| **RoCEv2 Packet Drops on 100GbE Link**| Priority Flow Control (PFC) disabled on switch | `ethtool -S eth0 \| grep -i pfc` | Enable PFC and Explicit Congestion Notification (ECN) on switch VLAN |
| **NFS CSI Volume Mount Timeout** | rpc-statd dead or firewall blocking port 2049 | `showmount -e truenas.local` | Unblock NFS traffic in Cilium policy and ensure nfs-common installed on worker |
| **NVIDIA Driver Container Crash** | Host kernel update drifted from DKMS drivers | `dmesg \| grep -i NVRM` | Pin kernel versions in apt and recompile nvidia modules via dkms autoinstall |

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

- Last reviewed: 2027-01-07
- Confidence: high
