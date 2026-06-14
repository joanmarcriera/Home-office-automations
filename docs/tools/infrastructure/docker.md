# Docker

## What it is
Docker is an open-source platform that enables developers to build, deploy, run, update, and manage containers—standardized, executable components that combine application source code with the operating system (OS) libraries and dependencies required to run that code in any environment. In June 2026, it remains the industry standard for containerization, powering everything from local development to massive AI inference clusters.

## What problem it solves
It eliminates the "it works on my machine" problem by providing consistent environments across development, testing, and production. Containers are lightweight alternatives to virtual machines, sharing the host OS kernel and starting almost instantly. This is critical for AI agents like Claude 4.8 Opus and GPT-5.5, which require isolated, reproducible environments to safely execute code.

## Where it fits in the stack
**Infrastructure / Containerization**. It is the foundational layer for running self-hosted services, AI workloads, and MCP servers in isolated environments. It sits below the orchestration layer (e.g., K3s) and above the host operating system.

## Typical use cases
- **AI Agent Sandboxing**: Providing isolated environments for agents to run and test code (e.g., Claude Code Container MCP).
- **Self-Hosted AI Services**: Deploying inference engines like vLLM or TGI.
- **MCP Server Deployment**: Hosting Model Context Protocol servers in a standardized environment.
- **Microservices Orchestration**: Running multi-container applications with Docker Compose.
- **CI/CD Pipelines**: Standardizing build and test environments.

## Strengths
- **Reproducibility**: Identical environments from dev to prod.
- **Efficiency**: Lower overhead than VMs; fast startup and scaling.
- **Ecosystem**: Massive library of pre-built images on Docker Hub.
- **Security**: Process isolation and resource constraints, enhanced by June 2026 security patches for AI workloads.

## Limitations
- **Overhead**: While lighter than VMs, it still adds some overhead compared to bare metal.
- **Networking Complexity**: Can be difficult to manage complex networking across many containers without orchestration.
- **Persistence**: Managing persistent data requires careful volume configuration.
- **Kernel Dependency**: Shared kernel means it cannot run a different OS (e.g., Windows containers on Linux).

## When to use it
- When you need to ensure an application runs identically everywhere.
- For microservices architectures and AI agent execution environments.
- When running self-hosted tools that require specific OS dependencies.
- For isolating AI agent execution environments (e.g., Docker Sandboxes).

## When not to use it
- For simple, static websites that can be served directly.
- When maximum performance on bare metal is absolutely critical and isolation isn't needed.
- On very resource-constrained systems where the Docker daemon overhead is too much.

## Getting started

### Installation
Follow the official guides for:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (macOS, Windows, Linux)
- [Docker Engine](https://docs.docker.com/engine/install/) (Server/Linux)

### Basic Workflow
1. **Create a `Dockerfile`**: Define your environment.
2. **Build the image**: `docker build -t my-agent-env .`
3. **Run the container**: `docker run -it my-agent-env`

## CLI examples
```bash
# Run an MCP server in a container
docker run -d --name mcp-server -e API_KEY=$API_KEY my-mcp-image

# List running containers
docker ps

# Inspect container logs for an AI agent session
docker logs -f ai-agent-sandbox

# Build an image with a specific tag
docker build -t local-inference:vLLM-0.5 .

# Stop and remove all containers for a project
docker-compose down
```

## API examples

### Docker Engine API (Python SDK)
AI agents often use the Docker Python SDK to manage their own sandboxes.

```python
import docker

client = docker.from_env()

# Create a secure sandbox for code execution
container = client.containers.run(
    "python:3.11-slim",
    "python -c 'print(\"Hello from the sandbox\")'",
    detach=True,
    mem_limit="512m",
    network_disabled=True
)

# Capture output
exit_code = container.wait()
logs = container.logs()
print(logs.decode("utf-8"))

# Cleanup
container.remove()
```

### Docker Compose (YAML)
```yaml
services:
  inference:
    image: vllm/vllm-openai:latest
    volumes:
      - ~/.cache/huggingface:/root/.cache/huggingface
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Related tools / concepts
- [Docker Compose](https://docs.docker.com/compose/)
- [Kubernetes (K3s)](k3s.md)
- [vLLM](vllm.md)
- [OpenHands](../development_ops/openhands.md)
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md)
- [Paperless-ngx](../../services/paperless-ngx.md)
- [Home Assistant](../../services/home-assistant.md)
- [Portracker](../../services/portracker.md)
- [Podman](https://podman.io/)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Sandboxed Code Execution](../../knowledge_base/patterns/sandboxed-execution.md)

## Sources / references
- [Official Website](https://www.docker.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Engine API Reference](https://docs.docker.com/engine/api/v1.45/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
