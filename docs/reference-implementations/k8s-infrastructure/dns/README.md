# External-DNS Configuration for Cloudflare

This reference implementation shows how to set up [External-DNS](https://github.com/kubernetes-sigs/external-dns) in a K3s cluster to automatically synchronize Kubernetes Ingresses and Services with Cloudflare DNS.

## Prerequisites

1.  **Cloudflare API Token**: Create a token with `Zone:Read` and `DNS:Edit` permissions for your zones.
2.  **Kubernetes Secret**: Create a secret in the `kube-system` namespace:
    ```bash
    kubectl create secret generic cloudflare-api-token --from-literal=api-token=YOUR_CLOUDFLARE_API_TOKEN -n kube-system
    ```

## Usage

1.  Update the `--domain-filter` argument in `external-dns.yaml` to match your domain.
2.  Apply the manifest:
    ```bash
    kubectl apply -f external-dns.yaml
    ```

## Verification

Check the logs of the External-DNS pod to ensure it is connecting to Cloudflare and processing resources:

```bash
kubectl logs -f deployment/external-dns -n kube-system
```

## Sources / References
- [External-DNS Cloudflare Tutorial](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/cloudflare.md)

## Contribution Metadata
- Last reviewed: 2026-04-20
- Confidence: high
