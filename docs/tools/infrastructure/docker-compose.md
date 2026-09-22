# Docker Compose

## What it is
Docker Compose is a tool for defining and running multi-container Docker applications using YAML configuration files. As of 2027, Docker Compose v2 (integrated directly into the Docker CLI as `docker compose`) is the standard tool for managing local microservices stacks, self-hosted AI services, and complex multi-service developmental environments.

## What problem it solves
Managing multiple containerized services manually via isolated `docker run` commands requires long, complex shell scripts with fragile network and volume bindings. Docker Compose solves this by allowing developers to declare multi-container architectures—including dependencies, environment variables, network bridges, volume mounts, and health checks—in a single, declarative `docker-compose.yml` file.

## Where it fits in the stack
**Infrastructure / Container Orchestration**. It operates directly above Docker Engine and Podman, enabling single-node multi-container orchestration for local development, home lab deployments, and staging environments.

## Typical use cases
- **Multi-Service AI Stacks**: Orchestrating local LLM serving engines (vLLM, Ollama), vector databases (Qdrant, Milvus), and frontend web interfaces (Open WebUI) together.
- **FastMCP Server Environments**: Running interconnected Model Context Protocol servers alongside supporting databases or caching layers (Redis/Valkey).
- **Development & Staging Environments**: Spawning identical, reproducible local test environments with a single command (`docker compose up -d`).
- **Homelab Application Stacks**: Managing self-hosted services like Nextcloud, Paperless-ngx, and Authentik.

## Strengths
- **Declarative Configuration**: Infrastructure-as-code format (`docker-compose.yml`) defines all service requirements in a version-controlled file.
- **Single-Command Control**: Spin up, shut down, or rebuild complex multi-container topologies using `docker compose up -d` or `docker compose down`.
- **Isolated Networks & Volumes**: Automatically creates dedicated bridge networks for service-to-service DNS resolution and isolated volume management.
- **GPU and Resource Limits**: Native support for allocating NVIDIA GPUs and setting CPU/RAM limits per service.

## Limitations
- **Single-Node Focus**: Designed primarily for single-host deployments; not a replacement for multi-node Kubernetes clusters like K3s in production.
- **No Built-In Auto-Healing**: Lacks automated cross-host rescheduling or advanced load balancing found in full orchestrators.
- **Configuration Creep**: Large YAML files with dozens of services can become hard to maintain without modular file includes (`include:` syntax).

## When to use it
- When your application requires multiple interdependent services (e.g., app server, database, Redis cache, vector DB).
- For local development environments where consistency across team members is critical.
- For home lab automation or edge deployments on single physical servers or virtual machines.

## When not to use it
- For massive-scale multi-node production clusters requiring advanced rolling deployments, ingress routing, and service meshes (use Kubernetes or K3s).
- For simple single-container applications where a basic `docker run` or systemd unit suffices.

## Getting started

### Installation
Docker Compose v2 comes pre-installed with Docker Desktop and standard Docker Engine packages. Verify installation:

```bash
docker compose version
```

### Basic `docker-compose.yml` Architecture
Create a `docker-compose.yml` file in your repository root:

```yaml
version: '3.8'

services:
  llm-engine:
    image: ollama/ollama:latest
    container_name: local-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

  vector-db:
    image: qdrant/qdrant:latest
    container_name: local-qdrant
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

volumes:
  ollama_data:
  qdrant_data:
```

## CLI examples
```bash
# Start all defined services in detached mode
docker compose up -d

# View live logs for all services or a specific service
docker compose logs -f llm-engine

# Stop and remove all containers, networks, and defined resources
docker compose down

# Rebuild images before starting containers
docker compose up -d --build
```

## API examples
```python
# Interacting with Docker Compose stack via Python Docker SDK / Docker CLI wrapper
import subprocess

def deploy_stack(compose_file: str = "docker-compose.yml"):
    result = subprocess.run(["docker", "compose", "-f", compose_file, "up", "-d"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Stack deployed successfully.")
    else:
        print(f"Error deploying stack: {result.stderr}")
```

## Related tools / concepts
- **[Docker](docker.md)**: Foundational single-container engine runtime.
- **[Podman](podman.md)**: Daemonless container engine alternative.
- **[K3s](k3s.md)**: Lightweight Kubernetes distribution for multi-node production orchestration.

## Sources / references
- [Docker Compose Documentation](https://docs.docker.com/compose/?ref=2026-09-21-audit)
- [Docker Architecture Overview](https://docs.docker.com/engine/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
