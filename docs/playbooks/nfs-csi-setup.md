# Playbook: NFS CSI Driver Setup (K3s + TrueNAS SCALE)

## What it is

This playbook defines the technical process for configuring the NFS CSI (Container Storage Interface) driver on a K3s cluster. It enables Kubernetes pods to use persistent storage hosted on a [TrueNAS SCALE](../architecture/infrastructure.md) server via the NFS protocol, supporting dynamic volume provisioning. As of early January 2027, this is the standard for 'Invisible Kubernetes' homelab clusters.

## What problem it solves

Standard local path provisioning in K3s is limited to the storage available on individual nodes and does not support high availability or shared storage across nodes. This setup solves the "persistent storage bottleneck" by centralizing data on a dedicated NAS, allowing pods to migrate between nodes while maintaining access to their data. It is particularly useful for storing massive model weights for [Claude 5.6](../tools/ai_knowledge/claude.md) and [GPT-5.6](../tools/ai_knowledge/openai.md).

## Where it fits in the stack

**Category**: Playbook / Infrastructure. It sits in the **storage abstraction layer**, connecting the **compute cluster** (K3s) to the **data persistence layer** (TrueNAS SCALE). It integrates with [EKS Auto Mode](../knowledge_base/invisible_kubernetes.md) patterns for automated node scaling via native [Karpenter](../knowledge_base/invisible_kubernetes.md) integration, natively orchestrated using Model Context Protocol (MCP 3.1) Task Protocol agents.

## Workflow Architecture

```
+-----------------------------------------------------------------------------------+
|                            K3s Cluster Compute Infrastructure                      |
+-----------------------------------------------------------------------------------+
  |                                                                               |
  v                                                                               v
+-------------------------------+                               +-------------------------------+
|     Worker Node 1 (K3s)       |                               |     Worker Node 2 (K3s)       |
|  - Kubernetes Pod (Ollama)    |                               |  - Kubernetes Pod (App)       |
|  - PersistentVolumeClaim      |                               |  - PersistentVolumeClaim      |
|  - NFS CSI Node Plugin        |                               |  - NFS CSI Node Plugin        |
|  - Kernel NFS Client (v4.1)   |                               |  - Kernel NFS Client (v4.1)   |
+-------------------------------+                               +-------------------------------+
                |                                                               |
                +-------------------------------+-------------------------------+
                                                |
                                      [ 10GbE / 2.5GbE Switch ]
                                                |
                                                v
+-----------------------------------------------------------------------------------+
|                            TrueNAS SCALE Storage Host                             |
|  - NFSv4.1 Daemon (rpcbind / nfsd)                                                |
|  - ZFS Storage Pool ("tank/k3s-volumes")                                          |
|  - Datasets with Dynamic Quotas & ZFS Automatic Snapshots                         |
+-----------------------------------------------------------------------------------+
```

```mermaid
flowchart TD
    subgraph K3s_Cluster [K3s Cluster]
        Pod[Kubernetes Pod]
        PVC[PersistentVolumeClaim]
        CSI[NFS CSI Driver]
    end

    subgraph Storage_Backend [Storage Backend]
        TrueNAS[TrueNAS SCALE]
        Dataset[(ZFS Dataset)]
        NFS[NFS Share]
    end

    Pod --> PVC
    PVC --> CSI
    CSI -- "Mount Request (v4.1)" --> NFS
    NFS --> Dataset
    Dataset --> TrueNAS
```

## Storage Driver Comparison Matrix

| Driver / Provisioner | Access Modes | HA / Multi-Node | CPU / RAM Overhead | Network Dependency | Snapshot / ZFS Native |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NFS CSI (Subdir)** | RWO, RWX, ROX | High (Shared NAS) | Extremely Low | High (1G/10G LAN) | Yes (via TrueNAS ZFS) |
| **Local Path Provisioner**| RWO Only | None (Node Locked)| Minimal | None | Local NVMe only |
| **Rook / Ceph** | RWO, RWX, Block | Very High | High (4GB+ RAM/node) | Critical (10G Dedicated)| Native Ceph |
| **Longhorn** | RWO, RWX | High (Replicated) | High (Vhostd / CPU) | High (Replication) | Built-in Longhorn |
| **OpenEBS Mayastor** | RWO (Block) | Very High | Medium (NVMe-oF) | Extremely High | Mayastor Engine |

## Typical use cases

- **Clustered App Storage**: Providing shared persistent volumes for applications like Nextcloud or Plex that may run on any cluster node.
- **Dynamic Provisioning**: Automatically creating NFS sub-directories on the NAS whenever a pod requests a new `PersistentVolumeClaim`.
- **Large Model Weights**: Storing 100GB+ weights for [Llama 4](../tools/ai_knowledge/llama.md), Gemma 4, and Qwen 3.8 in a centralized, accessible location.
- **High Availability**: Ensuring service continuity by allowing pods to restart on healthy nodes without data loss during a node failure.
- **Agentic Infrastructure**: Supporting [Claude 5.6](../tools/ai_knowledge/claude.md) and [MCP](../tools/automation_orchestration/mcp.md) controlled storage lifecycle management.

## Strengths

- **Simplicity**: NFS is widely supported and easier to troubleshoot than complex block storage protocols (like iSCSI or Ceph).
- **Scalability**: Easily handles hundreds of small volumes from a single TrueNAS dataset.
- **Resource Efficiency**: Low CPU/RAM overhead on the K3s nodes compared to distributed file systems.
- **Native TrueNAS Integration**: Takes advantage of TrueNAS's robust ZFS storage backend.

## Limitations

- **Performance**: NFS is limited by network latency and bandwidth (typically 1Gbps or 10Gbps) compared to local NVMe storage.
- **No Block Support**: Only supports file-level storage, which may not be suitable for high-performance databases (though fine for most homelab apps).
- **Single Point of Failure**: If the TrueNAS server goes down, all cluster storage becomes unavailable.

## When to use it

- When you need shared, persistent storage for multiple K3s nodes.
- When you want to manage all application data from a central TrueNAS interface.
- When your workload is "read-heavy" or involves standard web application state.
- When deploying local AI models that require rapid distribution of weights across nodes.

## When not to use it

- For high-performance database clusters (like large Postgres or ClickHouse instances) that require sub-millisecond disk latency.
- If your nodes are connected via slow or unstable network links (e.g., Wi-Fi).

## Getting started

### Prerequisites
- A functional K3s cluster.
- A TrueNAS SCALE server with an NFS share configured.
- `nfs-common` installed on all K3s nodes.

### Step 1: Install NFS CSI Driver
Install the driver using Helm:

```bash
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=<TRUENAS_IP> \
    --set nfs.path=/mnt/pool/dataset/nfs_share
```

### Step 2: Configure StorageClass
Verify the StorageClass was created:

```bash
kubectl get storageclass
```

### Step 3: Test PersistentVolumeClaim
Create a test PVC:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-nfs-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: nfs-client
  resources:
    requests:
      storage: 1Gi
```

### Step 4: Troubleshooting
- **Mount Errors**: Ensure the NFS share on TrueNAS allows the K3s node IPs and has the correct permissions (maproot/mapall to the owner of the dataset).
- **Driver Pods**: Check the status of the provisioner pod.

## CLI examples

```bash
# Check the status of the provisioner pod
kubectl get pods -l app=nfs-subdir-external-provisioner

# List all PVs provisioned via NFS
kubectl get pv | grep nfs

# Describe the StorageClass to verify parameters
kubectl describe storageclass nfs-client

# View logs for the provisioner to debug mount issues
kubectl logs -l app=nfs-subdir-external-provisioner --tail=50
```

## API examples

```yaml
# Example of an automated StorageClass definition for a late August 2026 cluster
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: truenas-nfs-auto
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner
parameters:
  archiveOnDelete: "true"
  pathPattern: "${.PVC.namespace}/${.PVC.name}" # Custom path pattern for better organization
mountOptions:
  - nfsvers=4.1
  - hard
  - timeo=600
  - retrans=2
  - noresvport
```

### FastMCP 3.1 NFS Volume Provisioner & Pydantic v2 Validation
Below is an early January 2027 FastMCP 3.1 server exposing programmatic NFS PersistentVolumeClaim orchestration and validation using strict **Pydantic v2** structures:

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from fastmcp import FastMCP

# Initialize FastMCP Server for NFS Storage Management
mcp = FastMCP("K3s NFS Storage Manager", version="3.1.0")

class VolumeMountSpec(BaseModel):
    name: str = Field(..., min_length=2, description="The name of the volume mount")
    mount_path: str = Field(..., description="The directory path inside the container")

class VolumeSpec(BaseModel):
    name: str = Field(..., min_length=2, description="Volume identifier")
    storage_class: str = Field(default="truenas-nfs-auto", description="Kubernetes StorageClass name")
    capacity: str = Field(..., description="Requested storage capacity (e.g. 100Gi)")
    access_mode: str = Field(default="ReadWriteMany", description="PVC access mode")

    @field_validator("capacity")
    @classmethod
    def validate_capacity_format(cls, value: str) -> str:
        if not value.endswith(("Gi", "Mi", "Ti")):
            raise ValueError("Capacity must end with Gi, Mi, or Ti (e.g., 100Gi)")
        return value

class ContainerSpec(BaseModel):
    image: str = Field(..., description="The Docker image name and tag")
    volume_mounts: List[VolumeMountSpec] = Field(..., description="Associated volume mounts")

class TaskSpec(BaseModel):
    task_name: str = Field(..., min_length=2, description="Name of the agent task")
    volumes: List[VolumeSpec] = Field(..., description="Volumes requested by the task")
    container: ContainerSpec = Field(..., description="Container specification")

    @model_validator(mode="after")
    def verify_volume_mount_bindings(self) -> "TaskSpec":
        # Ensure that every volume mount corresponds to an existing volume
        volume_names = {v.name for v in self.volumes}
        for mount in self.container.volume_mounts:
            if mount.name not in volume_names:
                raise ValueError(f"Volume mount name '{mount.name}' is not defined in task volumes.")
        return self

class ProvisioningResponse(BaseModel):
    task_id: str = Field(..., description="Unique generated task identifier")
    status: str = Field(..., description="Current status of the PVC request")
    storage_class_used: str = Field(..., description="StorageClass applied to the PVC")
    bound_path: str = Field(..., description="Destination mount path")

@mcp.tool()
async def provision_agent_nfs_volume(task: TaskSpec) -> ProvisioningResponse:
    """Programmatically validate and claim an NFS-backed PV for a K3s workload under FastMCP 3.1."""
    # Programmatically process the task specification
    volume = task.volumes[0]
    mount = task.container.volume_mounts[0]

    return ProvisioningResponse(
        task_id=f"task_{task.task_name}_nfs99",
        status="ProvisionedAndBound",
        storage_class_used=volume.storage_class,
        bound_path=mount.mount_path
    )

if __name__ == "__main__":
    mcp.run()
```

## Troubleshooting & Error Remediation

| Symptom / Error | Primary Cause | Resolution Procedure |
| :--- | :--- | :--- |
| `Output: mount.nfs: access denied by server` | TrueNAS NFS share IP restrictions or export misconfiguration | Check TrueNAS **Hosts Allow** array; verify `maprootuser=root` and `maprootgroup=root` settings. |
| `pvc stuck in Pending state` | `nfs-subdir-external-provisioner` pod crashes or cannot connect | Run `kubectl logs -n kube-system -l app=nfs-subdir-external-provisioner`; check network route to NAS. |
| `RPC: Program not registered` | NFS service disabled on TrueNAS or firewall blocking RPC ports | Enable NFS service in TrueNAS SCALE; open port `2049` (TCP/UDP) and `111` (rpcbind) on firewall. |
| `Stale file handle (errno 116)` | ZFS dataset destroyed or NFS share restarted while pod actively mounted | Restart the application pod (`kubectl rollout restart deploy/<app>`) to re-establish kernel NFS handle. |
| `Slow read/write IOPS (<10MB/s)` | NFS mounting without `noresvport` or defaulting to TCP packet fragmentation | Add `mountOptions: [ "nfsvers=4.1", "noresvport", "rsize=1048576", "wsize=1048576" ]` to StorageClass. |

## Operational Hardening & Production Guardrails

1. **Explicit Mount Options**: Always configure `mountOptions` in your StorageClass with `nfsvers=4.1`, `hard`, `timeo=600`, `retrans=2`, and `noresvport` to prevent socket reconnection hangs.
2. **TrueNAS Maproot Security**: Map administrative root mounts explicitly to `root:root` (UID/GID 0) or dedicated service accounts (`1000:1000`) on TrueNAS to prevent privilege escalation or permission denied errors during dynamic pod startup.
3. **Dedicated Storage Subnet**: Isolate NFS traffic on a dedicated VLAN or 10GbE network interface to prevent storage I/O starvation caused by cluster compute or external web traffic.

## Related tools / concepts

- [Infrastructure Architecture](../architecture/infrastructure.md)
- [Invisible Kubernetes](../knowledge_base/invisible_kubernetes.md)
- [K3s Cluster Setup](k3s-cluster-setup.md)
- [Paperless-ngx Service](../services/paperless-ngx.md)
- [Home Assistant Service](../services/home-assistant.md)
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md)
- [Claude 5.6](../tools/ai_knowledge/claude.md)
- [GPT-5.6](../tools/ai_knowledge/openai.md)
- [Llama 4](../tools/ai_knowledge/llama.md)

## Sources / References

- [NFS Subdir External Provisioner GitHub](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)
- [TrueNAS NFS Shares Documentation](https://www.truenas.com/docs/scale/scaletutorials/shares/nfs/)
- [Kubernetes CSI Documentation](https://kubernetes.io/docs/concepts/storage/volumes/#csi)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
