# Ramalama

## What it is
Ramalama is an open-source, container-native tool for running, serving, and managing local AI models using OCI (Open Container Initiative) containers (Podman, Docker) and engine runtimes like vLLM, llama.cpp, or Ollama. Developed as part of the Red Hat / Fedora ecosystem, it treats local AI models as containerized workloads.

## What problem it solves
Managing local AI model binaries, dependencies, CUDA/ROCm driver versions, and runtimes manually creates environment drift and deployment friction across home-lab nodes. Ramalama solves this by packaging local model execution into standard container images, allowing reproducible execution and air-gapped serving across any Linux, macOS, or Kubernetes cluster node.

## Where it fits in the stack
**Infrastructure / Model Runners**. Ramalama serves as a container-native model orchestration alternative to monolithic desktop apps or custom Python virtual environments.

## Typical use cases
- **Containerized Air-Gapped Model Serving**: Spawning Podman/Docker containers to host local GGUF or Safetensors models.
- **K3s / Kubernetes Pod Deployment**: Serving LLMs on home-lab Kubernetes clusters without custom runtime configuration.
- **CLI & REST API Model Execution**: Serving OpenAI-compatible API endpoints directly from containerized runtimes.

## Strengths
- **OCI Standard Native**: Leverages standard Podman/Docker image registries and OCI artifact formats.
- **Rootless & Secure**: Integrates with Podman for unprivileged, rootless container execution.
- **Hardware Acceleration Ready**: Auto-detects NVIDIA CUDA, AMD ROCm, Apple Metal, and Intel OneAPI GPU drivers.

## Limitations
- **Ecosystem Adoption**: Emerging tool compared to established runners like Ollama or llama.cpp directly.
- **Linux / Podman Centric**: Optimized primarily for Red Hat, Fedora, and Linux container environments.

## When to use it
- When deploying local AI models as containerized workloads using Podman or Docker.
- When serving models in air-gapped Linux or Kubernetes (K3s) home-lab nodes.
- When leveraging rootless container execution for model inference security.

## When not to use it
- When preferring simple single-binary CLI wrappers on non-containerized Windows workstations.
- When using managed cloud inference endpoints where local container orchestration is unnecessary.

## Getting started
To run a local model container using Ramalama and Podman:

```bash
# Install Ramalama
pip install ramalama

# Run an LLM containerized using Podman
ramalama run granite-3.1-dense

# Serve an OpenAI-compatible endpoint on port 8080
ramalama serve -p 8080 granite-3.1-dense
```

## CLI examples

```bash
# Pull and run a containerized model via Ramalama CLI
ramalama run granite-3.1-dense

# List locally cached OCI model containers
ramalama ls
```

## API examples

### 1. Pydantic v2 Schema for Ramalama Container Runtime Metrics
```python
from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class RamalamaRuntimeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_tag: str = Field(..., description="OCI image tag or HuggingFace model path")
    engine: str = Field(default="llama.cpp", description="Containerized runtime engine")
    port: int = Field(default=8080, ge=1024, le=65535)
    gpu_accelerator: str = Field(default="cuda", description="Hardware acceleration driver")

class RamalamaContainerStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    container_id: str
    status: str
    endpoint_url: str

def start_ramalama_container(config: RamalamaRuntimeConfig) -> RamalamaContainerStatus:
    # Simulated Podman container spawn for model execution
    return RamalamaContainerStatus(
        container_id="podman_a1b2c3d4",
        status="running",
        endpoint_url=f"http://localhost:{config.port}/v1"
    )

if __name__ == "__main__":
    cfg = RamalamaRuntimeConfig(model_tag="granite-3.1-dense", port=8080)
    status = start_ramalama_container(cfg)
    print(f"Ramalama container {status.container_id} active at {status.endpoint_url}")
```

### 2. FastMCP 3.1 Task Protocol Integration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ramalama-orchestrator")

@mcp.tool()
def deploy_model_container(model_name: str, port: int = 8080) -> dict:
    """Deploys a containerized local model using Ramalama and Podman."""
    return {"status": "deployed", "model": model_name, "port": port}
```

## Related tools / concepts
- [Ollama](ollama.md) — Popular local model runner.
- [Docker](docker.md) — Container runtime infrastructure.
- [K3s Cluster Setup](../../playbooks/k3s-cluster-setup.md) — Kubernetes deployment playbook.

## Sources / references
- [Ramalama GitHub Repository](https://github.com/containers/ramalama)
- [Containers.ai Documentation](https://containers.ai/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
