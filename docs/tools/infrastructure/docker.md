# Docker

## What it is
Docker is an open-source platform that enables developers to build, deploy, run, update, and manage containers—standardized, executable components that combine application source code with the operating system (OS) libraries and dependencies required to run that code in any environment. As of January 2027, Docker Engine 27+ and Compose v2.30+ remain the industry standard for containerization, powering everything from local development sandboxes to multi-GPU AI inference clusters.

## What problem it solves
It eliminates the "it works on my machine" problem by providing consistent environments across development, testing, and production. Containers are lightweight alternatives to virtual machines, sharing the host OS kernel and starting almost instantly. This is critical for AI agents like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Qwen 3.6 VL**, which require isolated, reproducible environments to safely execute code under strict memory and hardware caps.

## Where it fits in the stack
**Infrastructure / Containerization**. It is the foundational layer for running self-hosted services, AI workloads, and FastMCP 3.1 Task Protocol servers in isolated environments. It sits below the orchestration layer (e.g., K3s) and above the host operating system.

## Typical use cases
- **AI Agent Sandboxing**: Providing isolated environments for agents to run and test code safely.
- **Self-Hosted AI Services**: Deploying inference engines like vLLM, TGI, or Ollama for DeepSeek-V4, Gemma 4, and Qwen 3.6 VL.
- **FastMCP 3.1 Server Deployment**: Hosting Model Context Protocol Task Protocol servers in a standardized, security-hardened network environment.
- **Microservices Orchestration**: Running multi-container applications with Docker Compose v2.30+.
- **CI/CD Pipelines**: Standardizing build and test environments across devops pipelines.

## Strengths
- **Reproducibility**: Identical environments from dev to prod.
- **Efficiency**: Lower overhead than VMs; fast startup and scaling.
- **Ecosystem**: Massive library of pre-built images on Docker Hub and GitHub Container Registry.
- **Security**: Process isolation and resource constraints, enhanced by modern security patches for sandboxed LLM execution.

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
# Run a FastMCP 3.1 Task Protocol server in a container
docker run -d --name mcp-server -e API_KEY=$API_KEY my-mcp-image

# List running containers
docker ps

# Inspect container logs for an AI agent session
docker logs -f ai-agent-sandbox

# Build an image with a specific tag
docker build -t local-inference:vLLM-0.6 .

# Stop and remove all containers for a project
docker compose down
```

## API examples

### Docker Engine API (Python SDK with Pydantic v2 Schema)
AI agents often use the Docker Python SDK to manage their own sandboxes securely, incorporating limits on memory, CPU, and networking configured with strict Pydantic v2 schemas.

```python
import docker
from docker.errors import ContainerError, ImageNotFound
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class SandboxConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    image: str = Field(default="python:3.12-slim", description="Docker image for execution sandbox")
    memory_limit: str = Field(default="256m", description="RAM allocation cap")
    nano_cpus: int = Field(default=1000000000, description="CPU resource limit (10^9 = 1 CPU)")
    network_disabled: bool = Field(default=True, description="Disable outbound network access for security")
    read_only: bool = Field(default=True, description="Enforce read-only root filesystem")
    timeout_seconds: int = Field(default=10, ge=1, le=60)

class ExecutionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool
    output: str
    exit_code: Optional[int] = None

def run_sandboxed_code(script_content: str, config: Optional[SandboxConfig] = None) -> ExecutionResult:
    cfg = config or SandboxConfig()
    client = docker.from_env()

    escaped_script = script_content.replace("'", "'\\''")
    command = f"python -c '{escaped_script}'"

    try:
        container = client.containers.run(
            image=cfg.image,
            command=command,
            detach=True,
            mem_limit=cfg.memory_limit,
            nano_cpus=cfg.nano_cpus,
            network_disabled=cfg.network_disabled,
            read_only=cfg.read_only,
            volumes={'/tmp': {'bind': '/tmp', 'mode': 'rw'}}
        )

        res = container.wait(timeout=cfg.timeout_seconds)
        logs = container.logs().decode("utf-8")
        container.remove()

        return ExecutionResult(success=True, output=logs, exit_code=res.get("StatusCode", 0))

    except ImageNotFound:
        return ExecutionResult(success=False, output=f"Image {cfg.image} not found locally.")
    except ContainerError as ce:
        return ExecutionResult(success=False, output=f"Runtime error in sandbox: {ce}")
    except Exception as e:
        return ExecutionResult(success=False, output=f"Failed to execute sandboxed code: {e}")

if __name__ == "__main__":
    test_script = "import sys; print(f'Secure Sandbox verified on Python {sys.version_info.major}.{sys.version_info.minor}')"
    result = run_sandboxed_code(test_script)
    print(f"Success: {result.success}\nOutput: {result.output.strip()}")
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
- [Podman](https://podman.io/)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Sandboxed Code Execution](../../knowledge_base/patterns/sandboxed-execution.md)

## Sources / references
- [Official Website](https://www.docker.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Engine API Reference](https://docs.docker.com/engine/api/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
