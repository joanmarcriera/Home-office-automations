# Playbook: NFS CSI Driver Setup (K3s + TrueNAS SCALE)

## What it is

This playbook defines the technical process for configuring the NFS CSI (Container Storage Interface) driver on a K3s cluster. It enables Kubernetes pods to use persistent storage hosted on a [TrueNAS SCALE](../architecture/infrastructure.md) server via the NFS protocol, supporting dynamic volume provisioning.

## What problem it solves

Standard local path provisioning in K3s is limited to the storage available on individual nodes and does not support high availability or shared storage across nodes. This setup solves the "persistent storage bottleneck" by centralizing data on a dedicated NAS, allowing pods to migrate between nodes while maintaining access to their data.

## Where it fits in the stack

**Category**: Playbook / Infrastructure. It sits in the **storage abstraction layer**, connecting the **compute cluster** (K3s) to the **data persistence layer** (TrueNAS SCALE). It is a critical component for running stateful applications like [Paperless-ngx](../services/paperless-ngx.md) or [Home Assistant](../services/home-assistant.md) in a clustered environment.

## Typical use cases

- **Clustered App Storage**: Providing shared persistent volumes for applications like Nextcloud or Plex that may run on any cluster node.
- **Dynamic Provisioning**: Automatically creating NFS sub-directories on the NAS whenever a pod requests a new `PersistentVolumeClaim`, optimized for large model weight storage (GPT-5.5, Llama 4 Maverick).
- **High Availability**: Ensuring service continuity by allowing pods to restart on healthy nodes without data loss during a node failure.
- **Centralized Backups**: Leveraging TrueNAS snapshot and cloud sync features for all Kubernetes application data.
- **Agentic Infrastructure**: Supporting [Claude 4.7](../tools/ai_knowledge/claude.md) and [MCP](../tools/automation_orchestration/mcp.md) controlled storage lifecycle management.

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

## When not to use it

- For high-performance database clusters (like large Postgres or ClickHouse instances) that require sub-millisecond disk latency.
- If your nodes are connected via slow or unstable network links (e.g., Wi-Fi).

## Getting started

To setup the NFS CSI driver:

1. **NAS Preparation**: Create an NFS share on TrueNAS SCALE with `maproot` set to the appropriate user.
2. **Node Setup**: Install `nfs-common` on all K3s nodes: `sudo apt install nfs-common`.
3. **Driver Installation**: Use Helm to install the `nfs-subdir-external-provisioner`.
4. **StorageClass**: Define a `StorageClass` pointing to your TrueNAS IP and export path.
5. **Verification**: Deploy the test PVC provided in "Step 3" below.

## Prerequisites
- A functional K3s cluster.
- A TrueNAS SCALE server with an NFS share configured.
- `nfs-common` installed on all K3s nodes.

## Step 1: Install NFS CSI Driver
Install the driver using Helm:

```bash
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=<TRUENAS_IP> \
    --set nfs.path=/mnt/pool/dataset/nfs_share
```

## Step 2: Configure StorageClass
Verify the StorageClass was created:

```bash
kubectl get storageclass
```

You can create a custom `StorageClass` if needed:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: truenas-nfs
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner
parameters:
  archiveOnDelete: "true"
```

## Step 3: Test PersistentVolumeClaim
Create a test PVC to verify dynamic provisioning:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-nfs-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: truenas-nfs
  resources:
    requests:
      storage: 1Gi
```

Apply it and check status:
```bash
kubectl apply -f test-pvc.yaml
kubectl get pvc test-nfs-pvc
```

## Step 4: Troubleshooting
- **Mount Errors**: Ensure the NFS share on TrueNAS allows the K3s node IPs and has the correct permissions (maproot/mapall to the owner of the dataset).
- **Driver Pods**: Check the status of the provisioner pod:
  ```bash
  kubectl get pods -l app=nfs-subdir-external-provisioner
  ```

## Related tools / concepts

- [Infrastructure Architecture](../architecture/infrastructure.md)
- [Invisible Kubernetes](../knowledge_base/invisible_kubernetes.md)
- [K3s Cluster Setup](k3s-cluster-setup.md)
- [TrueNAS SCALE documentation](../architecture/infrastructure.md)
- [MetalLB Setup](../reference-implementations/k8s-infrastructure/metallb/)
- [Traefik Ingress](../reference-implementations/k8s-infrastructure/traefik/ingress-examples.yaml)
- [Longhorn Storage](../roadmap.md)
- [Paperless-ngx Service](../services/paperless-ngx.md)
- [Home Assistant Service](../services/home-assistant.md)
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md)

## Sources / References
- [NFS Subdir External Provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)
- [TrueNAS NFS Shares Documentation](https://www.truenas.com/docs/scale/scaletutorials/shares/nfs/)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
