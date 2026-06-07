# Home Lab Architecture Overview

## What it is

The Home Lab Architecture is a multi-layered infrastructure design built on **TrueNAS SCALE**, an open-source storage platform based on Debian GNU/Linux. As of June 2026, the architecture has evolved to support high-density AI workloads using **NVMe-over-Fabrics (NVMe-oF)** and dedicated GPU pools.

## What problem it solves

Self-hosting a complex stack of AI and automation tools requires a stable, scalable, and secure environment. This architecture solves the problem of "service sprawl" by centralizing compute and storage, ensuring data integrity through ZFS, and providing a standardized way to deploy, network, and backup local services.

## Where it fits in the stack

**Category**: Architecture / Infrastructure. It is the **foundation layer** of the entire system, providing the hardware abstraction, storage primitives, and container orchestration (Docker/K8s) upon which all other services and tools are built.

## Typical use cases

- **Centralized Data Lake**: Storing all family documents, media, and backups in a single, high-availability ZFS pool.
- **Local AI Hosting**: Running large language models (LLMs) and embedding models on local GPU/CPU hardware for privacy and performance.
- **Service Orchestration**: Deploying and managing a suite of interrelated tools (n8n, Paperless, Nextcloud) as a cohesive unit.
- **Secure Remote Access**: Connecting to the home lab from anywhere in the world via a secure, encrypted mesh network without exposing ports to the open internet.

## Strengths

- **Data Integrity**: ZFS provides snapshots, replication, and self-healing to protect against data corruption and drive failure.
- **Scalability**: Easily add more storage or compute resources as the lab grows.
- **Privacy**: All processing and storage happen locally, ensuring sensitive family data never leaves the premises.
- **AI-Ready Storage**: Support for high-IOPS NVMe pools ensures that large model weights can be loaded into GPU memory in seconds.

## Limitations

- **Hardware Dependency**: Reliability is tied to the physical health of the local server and network equipment.
- **Complexity**: Requires significant technical expertise to set up and maintain a ZFS-based container environment.
- **Power Consumption**: Running a high-performance home server 24/7 can lead to increased electricity costs.

## When to use it

- When you want to host your own "private cloud" for family or small business use.
- When you need a high-performance environment for running local AI models (Ollama, LiteLLM).
- When you prioritize data ownership and privacy over the convenience of public cloud services.

## When not to use it

- If you do not have the technical skills or time to manage a Linux-based server environment.
- For extremely high-availability applications that require geographical redundancy beyond what a single home can provide.
- If your compute needs are very low and could be better served by a simple NAS or low-power SBC (like a Raspberry Pi).

## Hardware Recommendations (June 2026)
- **CPU**: Min 8 cores (AMD Ryzen 7000+ or Intel 13th Gen+ recommended).
- **RAM**: 64GB DDR5 (ECC preferred for ZFS).
- **GPU**: NVIDIA RTX 4090 or RTX 5000-series (24GB+ VRAM) for local LLM inference.
- **Networking**: 10GbE SFP+ for the storage backbone.

## Related tools / concepts

- [Tailscale](../services/tailscale.md)
- [Nextcloud](../services/nextcloud.md)
- [Syncthing](../services/syncthing.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [Ollama](../services/ollama.md)
- [n8n](../services/n8n.md)
- [rclone](../services/rclone-automation.md)
- [K3s Cluster Setup](../playbooks/k3s-cluster-setup.md)
- [TrueNAS SCALE](https://www.truenas.com/truenas-scale/)

## Contribution Metadata

- Last reviewed: 2026-06-07
- Confidence: high

## Sources / References

- [TrueNAS SCALE Official Documentation](https://www.truenas.com/docs/scale/)
- [ZFS on Linux Reference](https://openzfs.github.io/openzfs-docs/Getting%20Started/Ubuntu/index.html)
- [NVIDIA Home Lab Guide](https://www.nvidia.com/en-us/ai-data-science/generative-ai/)
