# Playbook: NFS CSI Driver Setup (K3s + TrueNAS SCALE)

This playbook outlines the steps required to configure the NFS CSI driver on a K3s cluster to use persistent storage hosted on a TrueNAS SCALE server.

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

## Sources / References
- [NFS Subdir External Provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)
- [TrueNAS NFS Shares Documentation](https://www.truenas.com/docs/scale/scaletutorials/shares/nfs/)

## Contribution Metadata
- Last reviewed: 2026-04-20
- Confidence: high
