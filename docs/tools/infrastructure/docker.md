# Docker

## What it is
Docker is an open-source platform that enables developers to build, deploy, run, update, and manage containers—standardized, executable components that combine application source code with the operating system (OS) libraries and dependencies required to run that code in any environment. In September 2026, it remains the industry standard for containerization, powering everything from local development to massive AI inference clusters.

## What problem it solves
It eliminates the "it works on my machine" problem by providing consistent environments across development, testing, and production. Containers are lightweight alternatives to virtual machines, sharing the host OS kernel and starting almost instantly. This is critical for AI agents like Claude 5.1 and GPT-5.5, which require isolated, reproducible environments to safely execute code under strict memory and hardware caps.

## Where it fits in the stack
**Infrastructure / Containerization**. It is the foundational layer for running self-hosted services, AI workloads, and MCP servers in isolated environments. It sits below the orchestration layer (e.g., K3s) and above the host operating system.

## Typical use cases
- **AI Agent Sandboxing**: Providing isolated environments for agents to run and test code (e.g., Claude Code Container MCP).
- **Self-Hosted AI Services**: Deploying inference engines like vLLM or TGI for Llama 4, Gemma 3, and Qwen 3.6.
- **MCP Server Deployment**: Hosting Model Context Protocol (MCP 3.1) servers in a standardized, security-hardened network environment.
- **Microservices Orchestration**: Running multi-container applications with Docker Compose.
- **CI/CD Pipelines**: Standardizing build and test environments.

## Strengths
- **Reproducibility**: Identical environments from dev to prod.
- **Efficiency**: Lower overhead than VMs; fast startup and scaling.
- **Ecosystem**: Massive library of pre-built images on Docker Hub.
- **Security**: Process isolation and resource constraints, enhanced by late 2026 security patches for sandboxed LLM execution.

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
# Run an MCP 3.1 server in a container
docker run -d --name mcp-server -e API_KEY=$API_KEY my-mcp-image

# List running containers
docker ps

# Inspect container logs for an AI agent session
docker logs -f ai-agent-sandbox

# Build an image with a specific tag
docker build -t local-inference:vLLM-0.6 .

# Stop and remove all containers for a project
docker-compose down
```

## API examples

### Docker Engine API (Python SDK)
AI agents often use the Docker Python SDK to manage their own sandboxes securely, incorporating limits on memory, CPU, and networking to avoid agent escapes.

```python
import docker
from docker.errors import ContainerError, ImageNotFound

def run_sandboxed_code(script_content: str) -> str:
    client = docker.from_env()

    # Escape single quotes in user script
    escaped_script = script_content.replace("'", "'\\''")
    command = f"python -c '{escaped_script}'"

    try:
        # Create a secure sandbox with restricted memory, CPU, and NO network access
        container = client.containers.run(
            image="python:3.12-slim",
            command=command,
            detach=True,
            mem_limit="256m",
            nano_cpus=1000000000, # Max 1 CPU core
            network_disabled=True,
            read_only=True, # Prevent writes to the system root
            volumes={'/tmp': {'bind': '/tmp', 'mode': 'rw'}} # Allow writing to /tmp only
        )

        # Wait with a timeout (e.g., 10 seconds max run time)
        result = container.wait(timeout=10)
        logs = container.logs()

        container.remove()
        return logs.decode("utf-8")

    except ImageNotFound:
        return "Error: python:3.12-slim image not found locally."
    except ContainerError as ce:
        return f"Runtime error in sandbox: {ce}"
    except Exception as e:
        return f"Failed to execute sandboxed code: {e}"

if __name__ == "__main__":
    test_script = "import sys; print(f'Secure Sandbox verified on Python {sys.version_info.major}.{sys.version_info.minor}')"
    output = run_sandboxed_code(test_script)
    print(output)
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
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)

## Sources / references
- [Official Website](https://www.docker.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Engine API Reference](https://docs.docker.com/engine/api/v1.45/)

## Contribution Metadata
- Last reviewed: 2026-09-02
- Confidence: high
