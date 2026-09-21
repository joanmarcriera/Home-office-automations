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
Install Ramalama via `pip` or Fedora package manager (`dnf install ramalama`), then launch a local model containerized using Podman or Docker:

```bash
pip install ramalama
```

A minimal working hello-world example pulling and executing a containerized LLM chatbot using Ramalama:

```bash
# Run interactive chatbot session inside isolated container runtime
ramalama run granite-3.1-dense
```

## CLI examples

```bash
# 1. Run a containerized AI model chatbot in interactive terminal mode
ramalama run granite-3.1-dense

# 2. Serve an OpenAI-compatible REST API endpoint on port 8080 using container runtime
ramalama serve -p 8080 granite-3.1-dense

# 3. List all cached local model images and OCI container artifacts
ramalama list

# 4. Remove a cached model image from local container storage
ramalama rm granite-3.1-dense
```

## API examples

Minimal Python code snippet querying a served Ramalama OpenAI-compatible `/v1/chat/completions` REST endpoint:

```python
import json
import urllib.request

url = "http://localhost:8080/v1/chat/completions"
payload = {
    "model": "granite-3.1-dense",
    "messages": [
        {"role": "system", "content": "You are a helpful home-lab assistant."},
        {"role": "user", "content": "How do I configure rootless Podman?"}
    ],
    "temperature": 0.7
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode("utf-8"))
    answer = result["choices"][0]["message"]["content"]
    print("Ramalama Response:\n", answer)
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Popular local model runner.
- [vLLM](vllm.md) — High-throughput local model serving engine.
- [Docker](docker.md) — Container runtime infrastructure.
- [K3s Cluster Setup](../../playbooks/k3s-cluster-setup.md) — Kubernetes deployment playbook.

## Sources / references
- [Ramalama GitHub Repository](https://github.com/containers/ramalama)
- [Containers.ai Documentation](https://containers.ai/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
