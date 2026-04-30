# Kubernetes (K3s)

## What it is
K3s is a highly available, certified Kubernetes distribution designed for production workloads in resource-constrained environments like edge devices, IoT, and homelabs. It is developed by Rancher (now SUSE).

## What problem it solves
It simplifies the operation of Kubernetes by bundling necessary components into a single, lightweight binary (~50MB) and automating common tasks like certificate rotation and storage provisioning.

## Where it fits in the stack
**Infrastructure / Deployment**.

## Typical use cases
- **Homelab Orchestration**: Running containerized services (n8n, Paperless, etc.) with high availability.
- **Edge Computing**: Deploying applications on low-power devices like Raspberry Pis.
- **Local Development**: Testing Kubernetes manifests in a lightweight local cluster.

## Strengths
- **Low Footprint**: Minimal resource usage, making it ideal for home servers.
- **Easy Installation**: Can be installed with a single command.
- **Production Grade**: Fully CNCF certified Kubernetes distribution.

## Limitations
- **Single Binary**: While convenient, it differs slightly from "vanilla" Kubernetes in how some components are packaged.
- **Networking**: Uses Flannel by default, which may need replacement for advanced networking requirements.

## When to use it
- For managing multi-container home automation stacks that require auto-scaling or self-healing.
- When you want to learn Kubernetes without the overhead of a full enterprise distribution.

## When not to use it
- In extremely large enterprise environments where a managed service (EKS, GKE) or a full distribution (RKE, OpenShift) is preferred.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free.
- **Self-hostable**: Yes.

## Related tools / concepts
- [Docker](docker.md)
- [Home Assistant (via HASS-K8s)](../../services/home-assistant.md)
- [TrueNAS SCALE (Uses K3s internally)](../../architecture/infrastructure.md)

## Sources / References
- [Official Website](https://k3s.io/)
- [K3s GitHub](https://github.com/k3s-io/k3s)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
