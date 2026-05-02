# Docker

## What it is
Docker is an open-source platform that enables developers to build, deploy, run, update, and manage containers—standardized, executable components that combine application source code with the operating system (OS) libraries and dependencies required to run that code in any environment.

## What problem it solves
It eliminates the "it works on my machine" problem by providing consistent environments across development, testing, and production. Containers are lightweight alternatives to virtual machines, sharing the host OS kernel and starting almost instantly.

## Where it fits in the stack
[Infrastructure / Containerization] - It is the foundational layer for running self-hosted services and AI workloads in isolated, reproducible environments.

## Typical use cases
- Packaging applications and their dependencies into a single image.
- Running multiple isolated services on a single host without dependency conflicts.
- Deploying AI models and agents (e.g., via Docker Sandboxes or MCP servers).
- Standardizing development environments across a team.

## Strengths
- **Reproducibility**: Identical environments from dev to prod.
- **Efficiency**: Lower overhead than VMs; fast startup and scaling.
- **Ecosystem**: Massive library of pre-built images on Docker Hub.
- **Security**: Process isolation and resource constraints.

## Limitations
- **Overhead**: While lighter than VMs, it still adds some overhead compared to bare metal.
- **Networking Complexity**: Can be difficult to manage complex networking across many containers without orchestration.
- **Persistence**: Managing persistent data requires careful volume configuration.

## When to use it
- When you need to ensure an application runs identically everywhere.
- For microservices architectures.
- When running self-hosted tools that require specific OS dependencies.
- For isolating AI agent execution environments (e.g., Docker Sandboxes).

## When not to use it
- For simple, static websites that can be served directly.
- When maximum performance on bare metal is absolutely critical and isolation isn't needed.
- On very resource-constrained systems where the Docker daemon overhead is too much.

## CLI examples
```bash
# Run a container from an image
docker run -d --name my-app -p 8080:80 nginx

# List running containers
docker ps

# Build an image from a Dockerfile
docker build -t my-custom-app .

# Stop and remove a container
docker stop my-app && docker rm my-app
```

## Getting started
### Installation
Follow the official guides for:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (macOS, Windows, Linux)
- [Docker Engine](https://docs.docker.com/engine/install/) (Server/Linux)

### Basic Workflow
1. Create a `Dockerfile`.
2. `docker build -t my-image .`
3. `docker run my-image`

## Licensing and cost
- **Open Source**: Docker Engine and many components are open source (Apache 2.0).
- **Cost**: Free for personal use, small businesses, and open-source projects. Docker Desktop requires a paid subscription for large enterprises.
- **Self-hostable**: Yes.

## Related tools / concepts
- [Docker Compose](https://docs.docker.com/compose/)
- [Kubernetes (K3s)](k3s.md)
- [Portracker](../../services/portracker.md)
- [Podman](https://podman.io/)
- [LXC/LXD](https://linuxcontainers.org/)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / References
- [Official Website](https://www.docker.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)

## Contribution Metadata
- Last reviewed: 2026-03-30
- Confidence: high
