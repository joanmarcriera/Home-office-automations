# Docker Compose

## What it is
Docker Compose is an open-source tool for defining and running multi-container Docker applications. Using a declarative YAML configuration file (`docker-compose.yml`), developers specify multi-container services, networks, storage volumes, environment variables, dependencies, and container build contexts. With a single command (`docker compose up`), Docker Compose orchestrates the lifecycle of all configured containers.

In modern devops and local AI development stacks (2027), Docker Compose serves as the standard runtime orchestrator for self-hosted AI stacks, combining local inference servers (Ollama, vLLM), vector databases (Chroma, Qdrant), web UIs (Open WebUI), and automation engines (n8n) into reproducible environment templates.

## What problem it solves
Running applications composed of multiple microservices manually using standard `docker run` commands is error-prone and unwieldy. Developers must execute dozens of long terminal commands with complex flags for volume mounts, port mappings, network linkages, and environment variables. Managing service boot ordering and cleanup across environments introduces configuration drift.

Docker Compose solves these issues by:
- **Declarative Infrastructure-as-Code**: Encapsulating the entire multi-container service architecture in a single version-controlled `docker-compose.yml` file.
- **Isolated Environments**: Automatically creating dedicated container networks for inter-service communication (`http://service-name:port`).
- **Single-Command Lifecycle Management**: Orchestrating build, start, stop, scale, logs, and volume cleanup commands across all service containers concurrently.

## Where it fits in the stack
**Infrastructure / Container Orchestration Layer**. Docker Compose sits on top of the engine layer of [Docker](docker.md) and container runtimes ([Podman](podman.md)), bridging developer environments and production containerized deployments.

## Typical use cases
- **Self-Hosted Local AI & Agent Stacks**: Spinning up combined stacks featuring Ollama, vector stores, and web interfaces.
- **Full-Stack Application Development**: Launching web frontends ([Next.js](../development_ops/nextjs.md)), backend API microservices, PostgreSQL databases, and Redis caches locally.
- **Microservice Integration Testing**: Orchestrating ephemeral multi-container test environments in CI/CD automation pipelines.

## Strengths
- **Simplicity & Standardized Spec**: Highly readable declarative Compose Spec YAML format used across the industry.
- **Service Dependency Control**: Supports `depends_on` with health checks (`condition: service_healthy`) to ensure database services boot before dependent API containers start.
- **Environment Variable Overrides**: Easily customisable across development, staging, and production using `.env` files and profile flags (`--profile`).
- **Native GPU Resource Allocation**: Direct support for NVIDIA GPU passthrough specifications (`deploy.resources.reservations.devices`).

## Limitations
- **Single-Host Focus**: Docker Compose is optimized for single-host container orchestration. For multi-node distributed clusters across hosts, Kubernetes or [Argo Workflows](../orchestration/argo-workflows.md) are preferred.
- **Production High-Availability**: Lacks built-in automatic rolling updates or distributed failover capabilities present in Kubernetes.

## When to use it
- When developing or self-hosting multi-container applications locally on a single machine or VM.
- When orchestrating local AI agent stacks comprising an LLM server, database, and web UI.
- When standardizing local development setups across team members using a single repository file.

## When not to use it
- For enterprise-scale multi-node cluster deployments requiring automated pod scaling and ingress routing (use Kubernetes or Helm).
- For single isolated containers where a simple `docker run` command or container service platform suffices.

## Getting started

### Installation
Docker Compose is included by default in Docker Desktop and modern Docker CLI plugins:

```bash
# Verify Docker Compose CLI plugin
docker compose version
```

## CLI examples

### Common Compose Operations
```bash
# Boot all services in detached background mode with container building
docker compose up -d --build

# View real-time aggregated logs across all running stack containers
docker compose logs -f --tail=100

# Inspect status and health of stack services
docker compose ps

# Gracefully stop and remove all stack containers, networks, and volumes
docker compose down -v
```

## API examples

### Python (Interfacing with Docker Compose via Docker SDK for Python)
```python
import docker

def inspect_compose_containers(project_name: str):
    client = docker.from_env()
    containers = client.containers.list(filters={"label": f"com.docker.compose.project={project_name}"})
    for c in containers:
        print(f"Container: {c.name} | Status: {c.status}")
```

## Configuration & Code examples

### Multi-Container Local AI Stack (`docker-compose.yml`)
The following configuration demonstrates deploying a local AI stack containing an Ollama inference engine with GPU access, a vector database, and an Open WebUI frontend with automated healthchecks and internal network isolation.

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ai_ollama_engine
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - ai_network
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    healthcheck:
      test: ["CMD-SHELL", "wget -q --spider http://localhost:11434/ || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: ai_web_frontend
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - openwebui_data:/app/backend/data
    networks:
      - ai_network
    depends_on:
      ollama:
        condition: service_healthy
    restart: unless-stopped

networks:
  ai_network:
    driver: bridge

volumes:
  ollama_data:
  openwebui_data:
```

## Related tools / concepts
- [Docker](docker.md) — Fundamental containerization platform powered by Docker Compose.
- [Podman](podman.md) — Daemonless container engine supporting `podman-compose`.
- [Argo Workflows](../orchestration/argo-workflows.md) — Kubernetes workflow engine for multi-node cluster execution.

## Sources / references
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose Specification Standard](https://www.compose-spec.io/)
- [Docker Compose GitHub Repository](https://github.com/docker/compose)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
