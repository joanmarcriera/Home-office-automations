# External-DNS Configuration for Cloudflare

This reference implementation shows how to set up [External-DNS](https://github.com/kubernetes-sigs/external-dns) in a [K3s](https://docs.k3s.io/) or Kubernetes cluster to automatically synchronize Kubernetes Ingresses and Services with [Cloudflare DNS](https://www.cloudflare.com/dns/).

## Prerequisites

1.  **Cloudflare API Token**: Create a token at the [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens) with `Zone:Read` and `DNS:Edit` permissions.
2.  **Kubernetes Secret**: Create a secret in the `kube-system` namespace to store the token securely:
    ```bash
    kubectl create secret generic cloudflare-api-token --from-literal=api-token=YOUR_CLOUDFLARE_API_TOKEN -n kube-system
    ```

## Installation Methods

### Static Manifest Deployment
Apply the provided `external-dns.yaml` which uses the `v0.16.0` (early 2027 SOTA baseline) image:
```bash
kubectl apply -f external-dns.yaml
```

### Helm Chart Deployment (Recommended)
For production environments, using the [Official Helm Chart](https://artifacthub.io/packages/helm/external-dns/external-dns) is recommended for better lifecycle management:
```bash
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm upgrade --install external-dns external-dns/external-dns \
  --namespace kube-system \
  --version 1.22.0 \
  --set provider.name=cloudflare \
  --set env[0].name=CF_API_TOKEN \
  --set env[0].valueFrom.secretKeyRef.name=cloudflare-api-token \
  --set env[0].valueFrom.secretKeyRef.key=api-token
```

## Configuration Options

### Domain Filtering
Update the `--domain-filter` argument in the deployment to restrict External-DNS to specific zones. This prevents accidental record creation in other domains managed by the same API token.

### Service vs Ingress Sources
By default, this configuration watches both [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) resources and [Services](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) of type `LoadBalancer`.

## Security Best Practices (RBAC)
The included manifest follows the [Least Privilege Principle](https://kubernetes.io/docs/concepts/security/rbac-good-practices/) by defining a specific `ClusterRole` for External-DNS.

## Dry-run Mode
To test changes without affecting live DNS records, add the `--dry-run` flag to the container arguments. Check the logs to see what actions *would* have been taken.

## Troubleshooting Common Issues

### Permission Denied (403)
Verify that the [Cloudflare API Token](https://dash.cloudflare.com/profile/api-tokens) has access to the specific zone you are trying to update.

### Missing Records
Ensure your Ingress or Service has the correct annotations if you are using non-standard behavior, or check that the resource is correctly picked up by the `--source` flags.

## Verification
Monitor the logs to ensure successful synchronization:
```bash
kubectl logs -f deployment/external-dns -n kube-system
```

## Related Tools / Concepts
- [Cert-Manager](../cert-manager/README.md): Automated TLS certificate management.
- [Traefik Ingress](../traefik/README.md): Popular ingress controller for K3s.
- [Authentik](../../../services/authentik.md): For securing exposed services.

## Sources / References
- [Official External-DNS Cloudflare Tutorial](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/cloudflare.md)
- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/concepts/authentication-events/access-control/rbac/)
- [External-DNS Artifact Hub](https://artifacthub.io/packages/helm/external-dns/external-dns)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
