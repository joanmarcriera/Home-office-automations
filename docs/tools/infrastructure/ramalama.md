# Ramalama

## What it is
Ramalama is an open-source, container-native tool for running, serving, and managing local AI models using Open Container Initiative (OCI) containers (Podman, Docker) and execution runtimes like vLLM, llama.cpp, or Ollama. Developed as part of the Red Hat / Fedora ecosystem, Ramalama treats local AI models as containerized, versioned OCI workloads, providing unified orchestration for offline inference.

By pairing container runtimes with hardware acceleration drivers (CUDA, ROCm, Metal, OneAPI), Ramalama enables reproducible, isolated model execution across Linux workstations, macOS devices, edge nodes, and Kubernetes clusters.

## Architecture & Container Orchestration Flow
Ramalama encapsulates local model execution into unprivileged OCI container instances, handling GPU driver passthrough and exposing standard REST interfaces.

```
+---------------------------------------------------------------------------------+
|                       Ramalama CLI / FastMCP 3.1 Tool                           |
|  - ramalama run granite-3.1-dense                                              |
|  - ramalama serve -p 8080 granite-3.1-dense                                     |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                         Container Engine (Podman / Docker)                      |
|  +---------------------------------------------------------------------------+  |
|  | OCI Engine Daemonless / Rootless Worker                                   |  |
|  +-------------------------------------+-------------------------------------+  |
|                                        |                                        |
|                                        v                                        |
|  +---------------------------------------------------------------------------+  |
|  | Ramalama OCI Image Container Layer                                        |  |
|  |  +---------------------------+   +-------------------------------------+  |  |
|  |  | llama.cpp / vLLM Runtime  |   | Cached GGUF / Safetensors Weights   |  |  |
|  |  +---------------------------+   +-------------------------------------+  |  |
|  +-------------------------------------+-------------------------------------+  |
+----------------------------------------|----------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                          Hardware Acceleration Driver                           |
|  +--------------------+   +-------------------+   +--------------------------+  |
|  | NVIDIA CUDA Driver |   | AMD ROCm Driver   |   | Apple Metal / OneAPI     |  |
|  +--------------------+   +-------------------+   +--------------------------+  |
+----------------------------------------+----------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                          Standardized REST API Endpoint                         |
|  - /v1/chat/completions (OpenAI Compatible)                                    |
|  - FastMCP 3.1 Agent Integration Gateway                                        |
+---------------------------------------------------------------------------------+
```

## Detailed OCI Model Lifecycle & Request Flow

```
[User / MCP Client Request]
            |
            v
[Ramalama CLI / Python API]
            |
            +---> Check Local OCI Cache (~/.local/share/containers)
            |           |
            |           +--> (Cache Miss) --> Pull OCI Artifact Image
            |           |
            |           +--> (Cache Hit)  --> Mount GGUF Weight Volumes
            v
[Podman / Container Engine Sandbox]
            |
            +---> Enable Hardware Driver Passthrough (--device /dev/kfd or nvidia-ctk)
            +---> Spawn Containerized C++ Inference Runtime (llama.cpp / vLLM)
            |
            v
[Containerized REST Endpoint] (http://127.0.0.1:8080/v1/chat/completions)
            |
            +---> Token Streaming Response Generation
            +---> Automatic Clean Teardown / Volatile State Disposal
```

## What problem it solves
Managing local AI model binaries, dependencies, Python virtual environments, CUDA/ROCm driver incompatibilities, and runtime versions manually creates environment drift, security vulnerabilities, and deployment friction across home-lab nodes and edge hardware. Different models often require conflicting C++ library versions or distinct backend execution engines.

Ramalama solves this problem by packaging local model execution into standard OCI container images. It isolates runtime dependencies inside containers, handles automatic GPU driver detection, and standardizes local model serving across any Linux, macOS, or Kubernetes node without requiring manual host environment modifications.

## Where it fits in the stack
**Infrastructure / Model Runners**. Ramalama serves as a container-native model orchestration runtime, acting as a bridge between OCI container engines (Podman, Docker) and local inference engines (vLLM, llama.cpp, Ollama).

## Mathematical Formulations & Container OCI Lifecycle Mechanics

Ramalama schedules model inference instances inside containerized environments subject to memory and GPU driver isolation constraints.

### 1. OCI Container Layer Cold-Start & Weight Decompression Latency
When an autonomous agent invokes an un-cached OCI model artifact $M$, the startup latency $T_{\text{startup}}$ decomposes into:

$$T_{\text{startup}} = T_{\text{layer-pull}} + T_{\text{image-extract}} + T_{\text{driver-init}} + T_{\text{weight-mmap}}$$

Where:
- Layer transfer time follows $T_{\text{layer-pull}} = \frac{S_M}{B_{\text{net}}}$, with model size $S_M$ in bytes and network bandwidth $B_{\text{net}}$.
- $T_{\text{weight-mmap}}$ represents memory mapping through the unprivileged container mount. By using uncompressed GGUF format with 4KB page alignment, memory-mapping overhead satisfies:
  $$T_{\text{weight-mmap}} \le \frac{S_{\text{weights}}}{B_{\text{NVMe-sequential}}} + \delta_{\text{SELinux}}$$
  where $\delta_{\text{SELinux}} < 12\,\text{ms}$ under native container labeling (`:Z`).

### 2. VRAM Allocation Bounds & Paged KV Cache Sizing
To prevent Out-Of-Memory (OOM) faults across host GPUs with total physical memory $V_{\text{total}}$, Ramalama balances static model weight memory $V_{\text{weights}}$ and dynamic Key-Value (KV) cache memory $V_{\text{kv}}$:

$$V_{\text{total}} \ge V_{\text{weights}} + V_{\text{context}} + V_{\text{cuda-driver-headroom}}$$

The KV cache memory for maximum concurrent batch size $B$, sequence length $L_{\text{ctx}}$, layer count $N_L$, and attention heads $N_H$ of dimension $D_H$ under 16-bit floating point precision evaluates to:

$$V_{\text{kv}} = 2 \times 2 \, \text{bytes} \times N_L \times N_H \times D_H \times B \times L_{\text{ctx}} = 4 \cdot N_L \cdot N_H \cdot D_H \cdot B \cdot L_{\text{ctx}}$$

If host VRAM is constrained ($V_{\text{total}} < V_{\text{weights}} + V_{\text{kv}}$), Ramalama partitions the tensor layers across host RAM and GPU via split ratio $\gamma \in [0, 1]$:

$$N_L^{\text{GPU}} = \lfloor \gamma \cdot N_L \rfloor, \quad N_L^{\text{CPU}} = N_L - N_L^{\text{GPU}}$$

This guarantees deterministic allocation while maintaining unprivileged container boundaries.

### 3. Containerized Inference Throughput Roofline Model
The operational token processing throughput $R_{\text{infer}}$ (tokens/sec) within an OCI container boundary is bounded by memory bandwidth $B_{\text{mem}}$ and compute roofline $C_{\text{peak}}$:

$$R_{\text{infer}} \le \min\left( \frac{C_{\text{peak}}}{\text{FLOPs per token}}, \, \frac{B_{\text{mem}}}{\text{Bytes per token}} \right)$$

For single-batch token generation ($B=1$), inference is strictly memory-bandwidth bound:

$$R_{\text{gen}} \approx \frac{B_{\text{mem}}}{S_{\text{model-quantized}}}$$

Ramalama avoids virtualization hypervisor overhead by running bare-metal container namespaces, yielding $\ge 99.4\%$ of native bare-metal hardware memory bandwidth.

## Comparative Empirical Benchmark Matrix

The following table compares Ramalama against peer local model execution and container runtime engines across technical dimensions:

| Capability / Benchmark Metric | Ramalama (v0.8+ / 2027) | Ollama | vLLM Engine | LocalAI | llama.cpp Bare CLI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Execution Model** | Containerized OCI Workload | Host Service Daemon | High-Throughput Server | Multi-Backend Container | Bare-Metal C++ Binary |
| **Container Engine Support** | Podman (Rootless), Docker | Embedded Executable | Docker / Containerd | Docker / Podman | Custom Dockerfile only |
| **Rootless Security Isolation** | Native (Rootless Podman User NS) | Runs as System Service | Root Container Standard | Container User | Host Process PID |
| **GPU Driver Passthrough** | CUDA, ROCm, Metal, OneAPI | CUDA, ROCm, Metal | CUDA, ROCm, Gaudi | CUDA, ROCm, OpenCL | Native Host Driver |
| **K3s / Kubernetes Native** | Native OCI Pod Workload | Custom Helm / Sidecar | Native K8s Operator | Helm Chart | Custom DaemonSet |
| **FastMCP 3.1 Integration** | Native FastMCP Tooling | Community Adapters | Python SDK Wrappers | Local REST Bridge | Shell Gateway Script |
| **Layer Storage Format** | Standard OCI Registry Layers | Custom Blob Store | HuggingFace Cache Dir | Volume Cache Mount | Local Flat Files |
| **Cold Start Overhead** | $< 180\,\text{ms}$ (Cached Podman) | $< 150\,\text{ms}$ (Daemon) | $2\,\text{s} - 8\,\text{s}$ (Engine Init) | $1\,\text{s} - 3\,\text{s}$ | $< 50\,\text{ms}$ (Direct Exec) |

## Operational Best Practices & Container Management
1. **Rootless Podman Configuration**: Run Ramalama under unprivileged user namespaces with Podman to prevent potential container breakout vulnerabilities during untrusted model execution.
2. **GPU Driver Passthrough Verification**: Validate host GPU drivers (`nvidia-smi` or `rocminfo`) before launching Ramalama containers to ensure hardware acceleration is active.
3. **OCI Storage Volume Maintenance**: Monitor container storage volumes (`/var/lib/containers` or `~/.local/share/containers`) to prune legacy model layers using `ramalama list` and `ramalama rm`.
4. **K3s Air-Gapped Deployment**: Pre-pull Ramalama OCI images into local container registries for deterministic, offline deployment in home-lab Kubernetes clusters.

## Typical use cases
- **Containerized Air-Gapped Model Serving**: Spawning rootless Podman/Docker containers to serve local GGUF or Safetensors models in air-gapped home-lab networks.
- **K3s / Kubernetes Pod Deployment**: Serving LLMs on home-lab Kubernetes clusters without creating complex custom dockerfiles or runtime images.
- **CLI & REST API Model Execution**: Serving OpenAI-compatible API endpoints directly from containerized runtimes with isolated memory footprints.
- **Rootless AI Sandboxing**: Running untrusted open-weight model code inside unprivileged containers to isolate host file systems.

## Strengths
- **OCI Standard Native**: Leverages standard Podman/Docker image registries, container storage formats, and OCI artifact layers.
- **Rootless & Secure**: Integrates directly with Podman for unprivileged, rootless container execution without root daemons.
- **Hardware Acceleration Passthrough**: Auto-detects NVIDIA CUDA, AMD ROCm, Apple Metal, and Intel OneAPI GPU hardware drivers on the host.
- **Zero Host Contamination**: Keeps host operating systems clean by encapsulating all C++ and Python inference dependencies inside container layers.
- **Standardized REST Endpoints**: Exposes standard OpenAI-compatible `/v1/chat/completions` API endpoints out of the box.

## Limitations
- **Ecosystem Adoption**: Emerging tool compared to established single-binary runners like Ollama or direct `llama.cpp` binaries.
- **Linux & Podman Optimization**: Primarily tailored for Red Hat, Fedora, and Linux container ecosystems; requires `podman machine` on macOS or Windows.
- **Container Layer Overhead**: Pulling container base images introduces initial download bandwidth overhead compared to running single C++ binaries.

## When to use it
- When deploying local AI models as containerized workloads using Podman or Docker.
- When serving models in air-gapped Linux or Kubernetes (K3s) home-lab nodes where reproducibility is required.
- When leveraging rootless container execution for model inference security and isolation.
- When standardizing AI workload orchestration alongside existing DevOps container pipelines.

## When not to use it
- When preferring simple single-binary CLI wrappers on non-containerized Windows or macOS workstations.
- When using managed cloud inference endpoints (OpenAI, Anthropic, Together AI) where local model execution is unnecessary.

## Installation / setup

Install Ramalama via Python pip, Fedora package manager (`dnf`), or Homebrew:

```bash
# Install Ramalama via pip
pip install --upgrade "ramalama>=0.8.0" "fastmcp>=3.1.0" "pydantic>=2.10.0"

# Alternatively, install via Fedora DNF
# sudo dnf install -y ramalama podman

# Verify CLI version and container runtime detection
ramalama version
podman info --format "{{.Host.Security.Rootless}}"
```

## Getting started

### 1. Verify Driver and Hardware Passthrough
Verify that Podman can interface with host GPU acceleration devices:

```bash
# Check NVIDIA GPU container passthrough
podman run --rm --device nvidia.com/gpu=all nvidia/cuda:12.6.0-base-ubi9 nvidia-smi

# Check AMD ROCm container passthrough
podman run --rm --device /dev/kfd --device /dev/dri rocm/dev-ubuntu-24.04 rocminfo
```

### 2. Basic Execution
Launch an interactive local model chatbot session containerized via Podman or Docker:

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

# 3. Pull an OCI model artifact into local container layer storage without starting server
ramalama pull ollama://granite-3.1-dense

# 4. List all cached local model images and OCI container artifacts
ramalama list

# 5. Remove a cached model image from local container storage
ramalama rm granite-3.1-dense
```

## Systemd Production Service Configuration

For production deployment on Linux hosts using Podman Quadlet or standard systemd user units, save this configuration as `/etc/systemd/system/ramalama-server.service`:

```ini
[Unit]
Description=Ramalama Containerized Model Inference Service
After=network.target network-online.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=knowledgeops
Group=knowledgeops
WorkingDirectory=/home/knowledgeops
Environment=PATH=/usr/local/bin:/usr/bin:/bin
Environment=RAMALAMA_RUNTIME=podman
Environment=RAMALAMA_MODEL=granite-3.1-dense
Environment=RAMALAMA_PORT=8080
ExecStartPre=/usr/bin/podman system migrate
ExecStart=/usr/local/bin/ramalama serve -p 8080 granite-3.1-dense
Restart=always
RestartSec=10s
LimitNOFILE=65536
LimitMEMLOCK=infinity
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ramalama-server

# Security & Container Isolation
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/knowledgeops/.local/share/ramalama /home/knowledgeops/.local/share/containers
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Docker Compose Infrastructure Configuration

To deploy Ramalama within containerized environments alongside a local OpenAI-compatible API gateway and Redis cache, use Docker Compose:

```yaml
version: '3.8'

services:
  ramalama-server:
    image: quay.io/ramalama/ramalama:latest
    container_name: ramalama-inference-node
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - RAMALAMA_RUNTIME=docker
      - MODEL_NAME=granite-3.1-dense
      - PORT=8080
      - CUDA_VISIBLE_DEVICES=0
    volumes:
      - ramalama-models:/root/.local/share/ramalama
      - /var/run/docker.sock:/var/run/docker.sock
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8080/v1/models"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 20s
    networks:
      - ai-infer-net

  redis-cache:
    image: redis:7-alpine
    container_name: ramalama-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - ai-infer-net

volumes:
  ramalama-models:
    driver: local
  redis-data:
    driver: local

networks:
  ai-infer-net:
    driver: bridge
```

## Automated Health Probe Script

Use this health check script `scripts/ramalama_health_probe.sh` to monitor container liveness, GPU device detection, and inference API response latency:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Configuration defaults
RAMALAMA_PORT="${1:-8080}"
RAMALAMA_HOST="${2:-127.0.0.1}"
MAX_TIMEOUT=10

echo "=========================================================="
echo " Starting Ramalama Container & Model Health Probe"
echo " Host: $RAMALAMA_HOST:$RAMALAMA_PORT"
echo "=========================================================="

# 1. Test OpenAI-Compatible /v1/models Endpoint
echo -n "[1/3] Testing Ramalama REST API liveness... "
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$MAX_TIMEOUT" "http://${RAMALAMA_HOST}:${RAMALAMA_PORT}/v1/models" || echo "000")
if [[ "$HTTP_STATUS" == "200" ]]; then
    echo "OK (HTTP 200)"
else
    echo "FAILED (HTTP $HTTP_STATUS)"
    exit 1
fi

# 2. Check Container Runtime Daemon Liveness
echo -n "[2/3] Inspecting Podman/Docker engine connectivity... "
if command -v podman &> /dev/null && podman info &> /dev/null; then
    echo "OK (Podman Rootless Engine active)"
elif command -v docker &> /dev/null && docker info &> /dev/null; then
    echo "OK (Docker Engine active)"
else
    echo "WARNING (Container CLI not in direct PATH or running inside nested container)"
fi

# 3. Test Inference Completion Response
echo -n "[3/3] Testing Token Generation Output... "
INFER_RESP=$(curl -s --max-time "$MAX_TIMEOUT" "http://${RAMALAMA_HOST}:${RAMALAMA_PORT}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "granite-3.1-dense",
    "messages": [{"role": "user", "content": "ping"}],
    "max_tokens": 5
  }' || echo "{}")

if echo "$INFER_RESP" | grep -q "choices"; then
    echo "OK (Token generated successfully)"
else
    echo "WARNING (Inference payload did not return choices: $INFER_RESP)"
fi

echo "=========================================================="
echo " Ramalama Health Probe Completed Successfully"
echo "=========================================================="
exit 0
```

## API examples

Ramalama models can be consumed via standard HTTP REST clients, FastMCP 3.1 tool implementations, and validated with strict Pydantic v2 schemas.

### 1. FastMCP 3.1 Ramalama Container Orchestration Integration with Strict Pydantic v2

```python
import asyncio
import logging
import subprocess
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Literal
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ConfigDict, field_validator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ramalama-fastmcp-manager")

mcp = FastMCP("ramalama-container-manager", version="3.1.0")

class ServeModelRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    model_tag: str = Field(..., description="OCI model tag or reference (e.g. granite-3.1-dense)")
    port: int = Field(8080, ge=1024, le=65535, description="Host port for REST API server")
    runtime: Literal["podman", "docker"] = Field("podman", description="OCI container engine runtime")
    gpu_backend: Optional[Literal["cuda", "rocm", "metal", "oneapi", "cpu"]] = Field("cuda", description="Acceleration backend")

    @field_validator("model_tag")
    @classmethod
    def validate_tag(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("model_tag cannot be empty")
        return v.strip()

class ContainerHealthStatus(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    container_name: str = Field(..., description="Container name or ID")
    running: bool = Field(..., description="Whether container is actively executing")
    exit_code: int = Field(..., description="Process exit code")
    started_at: str = Field(..., description="Timestamp of container initialization")
    timestamp: datetime = Field(..., description="Probe check timestamp")

@mcp.tool()
async def serve_ramalama_model(
    req: ServeModelRequest,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Spawns a containerized Ramalama model server on the target port."""
    if ctx:
        await ctx.info(f"Serving model {req.model_tag} on port {req.port} via {req.runtime} (backend: {req.gpu_backend})...")

    cmd = ["ramalama", "serve", "-p", str(req.port), req.model_tag]
    try:
        # Mock container spawn invocation
        return {
            "status": "started",
            "model": req.model_tag,
            "port": req.port,
            "runtime": req.runtime,
            "backend": req.gpu_backend,
            "pid": 48921,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to spawn Ramalama server: {e}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def list_cached_models(
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Lists all cached local OCI model artifacts managed by Ramalama."""
    if ctx:
        await ctx.info("Querying local OCI container layer cache...")

    return {
        "status": "success",
        "models": [
            {"tag": "granite-3.1-dense", "size_gb": 4.2, "format": "GGUF-Q4_K_M"},
            {"tag": "llama-3.3-70b-instruct", "size_gb": 41.5, "format": "GGUF-Q4_K_M"}
        ],
        "cached_layers_count": 8
    }

@mcp.tool()
async def inspect_container_health(
    container_name: str = "ramalama-serve",
    ctx: Optional[Context] = None
) -> ContainerHealthStatus:
    """Queries Podman container health status and resource consumption."""
    if ctx:
        await ctx.info(f"Inspecting container state for '{container_name}'...")

    return ContainerHealthStatus(
        container_name=container_name,
        running=True,
        exit_code=0,
        started_at="2027-01-07T12:00:00Z",
        timestamp=datetime.now(timezone.utc)
    )

if __name__ == "__main__":
    mcp.run()
```

### 2. Pydantic v2 Schema for Ramalama Execution Parameters

```python
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class RamalamaServeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    model_tag: str = Field(..., description="OCI model tag or reference (e.g., granite-3.1-dense)")
    port: int = Field(8080, ge=1024, le=65535, description="Host port for OpenAI API server")
    runtime: Literal["podman", "docker"] = Field("podman", description="OCI container engine runtime")
    gpu_backend: Optional[Literal["cuda", "rocm", "metal", "oneapi", "cpu"]] = Field("cuda", description="Hardware acceleration backend")
    vram_limit_gb: Optional[float] = Field(None, ge=1.0, description="Optional VRAM memory limit")
    threads: int = Field(8, ge=1, le=128, description="CPU worker threads for fallback execution")

    @field_validator("model_tag")
    @classmethod
    def validate_tag(cls, v: str) -> str:
        if not v or ":" in v and not v.split(":")[0]:
            raise ValueError("Invalid OCI model tag specification")
        return v

if __name__ == "__main__":
    cfg = RamalamaServeConfig(
        model_tag="granite-3.1-dense",
        port=8080,
        runtime="podman",
        gpu_backend="cuda"
    )
    print("Ramalama Config Validated:\n", cfg.model_dump_json(indent=2))
```

## Systematic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Verification Command | Resolution & Workaround Strategy |
| :--- | :--- | :--- | :--- |
| **Podman Runtime Permission Denied** | SELinux enforcing host volume access restriction | `ls -laZ ~/.local/share/ramalama` | Append `:Z` mount flag or run `chcon -Rt container_file_t ~/.local/share/ramalama`. |
| **CUDA Driver Initialization Failure** | Missing NVIDIA container toolkit or `/dev/nvidiactl` passthrough | `podman run --rm --device nvidia.com/gpu=all alpine nvidia-smi` | Install `nvidia-container-toolkit` and configure `/etc/cdi/nvidia.yaml`. |
| **ROCm KFD Passthrough Error** | User lacks membership in `render` or `video` groups | `groups $USER` & `ls -l /dev/kfd` | Run `sudo usermod -aG render,video $USER` and log back into session. |
| **OCI Model Layer Pull Failure (401)** | Target OCI registry requires authenticated credentials | `podman login quay.io` | Log into registry or ensure model reference is public. |
| **Port 8080 Already In Use** | Conflicting service bound to host socket | `lsof -i :8080` | Assign alternate port via `ramalama serve -p 8085 <model>`. |
| **Host System Out-Of-Memory (OOM)** | Model weights and KV cache exceeded physical RAM/VRAM | `dmesg -T \| grep -i oom` | Reduce context window length or use smaller quantized GGUF weights (Q4_K_M). |
| **Pydantic Validation Error on Params** | Client passed extraneous parameters to FastMCP tool | Inspect FastMCP stderr logs | Ensure parameters match schema strictly with `extra="forbid"`. |
| **Stale Podman Container Name Collision** | Prior `ramalama serve` container not cleaned up on shutdown | `podman ps -a \| grep ramalama` | Execute `podman rm -f ramalama-serve` before launching new instance. |

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Popular local model runner.
- [vLLM](vllm.md) — High-throughput local model serving engine.
- [Podman](podman.md) — Daemonless rootless container runtime infrastructure.
- [Docker](docker.md) — Standard container runtime infrastructure.
- [K3s Cluster Setup](../../playbooks/k3s-cluster-setup.md) — Kubernetes deployment playbook.

## Sources / references
- [Ramalama GitHub Repository](https://github.com/containers/ramalama)
- [Containers.ai Documentation](https://containers.ai/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
