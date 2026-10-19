# Podman

## What it is
Podman (Pod Manager) is a daemonless, open-source Linux container engine designed to develop, manage, and run Open Container Initiative (OCI) containers and container pods. Developed originally by Red Hat, Podman offers a drop-in command-line replacement for Docker (`alias docker=podman`) while operating entirely without a central root-privileged daemon process.

By leveraging native Linux kernel features—such as user namespaces, cgroups v2, SELinux, and Seccomp—Podman enables rootless container execution where unprivileged users can build, run, and manage isolated workloads without administrative privileges.

```
+-----------------------------------------------------------------------------------+
|                       Podman Daemonless User Namespace Sandbox Topology           |
|                                                                                   |
|  +--------------------+    +----------------------+    +-----------------------+  |
|  | Unprivileged User  |===>| Podman CLI / Libpod  |===>| SubUID / SubGID Map   |  |
|  | (Host Non-Root)    |    | (Direct Fork/Exec)   |    | (Kernel User Namespace)| |  |
|  +--------------------+    +----------------------+    +-----------------------+  |
|                                                                    ||             |
|                                                                    \/             |
|  +-----------------------------------------------------------------------------+  |
|  |                         Conmon Container Monitor                            |  |
|  |  +--------------------+   +---------------------+   +--------------------+  |  |
|  |  | OCI Runtime (crun) |   | FastMCP 3.1 Sandbox |   | SELinux / Seccomp  |  |  |
|  |  | (Process Isolation)|   | (Isolated Code Run) |   | (Label Enforcer)   |  |  |
|  +--------------------+   +---------------------+   +--------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Traditional container runtimes rely on a centralized, root-privileged daemon process (e.g., `dockerd`), which introduces significant security vulnerabilities, single-point-of-failure risks, and administrative friction in enterprise and multi-tenant environments. A compromise of the Docker daemon grants attackers full root access to the host operating system.

Podman solves this security risk by adopting a daemonless architecture. Containers are launched directly as child processes of the invoking user shell or systemd service, constrained within unprivileged Linux user namespaces. This ensures that even if a containerized process is compromised, the attacker remains an unprivileged user on the host system.

## Where it fits in the stack
**Infrastructure / Container Runtime**. It serves as an enterprise-grade container runtime for local development, secure AI agent sandboxing, rootless container deployments, edge devices, and Kubernetes-compatible local pod execution.

## Typical use cases
- **Rootless Container Execution**: Running secure, isolated workloads in multi-tenant environments and corporate workstations without granting root privileges.
- **AI Agent Sandboxing**: Executing untrusted AI code, FastMCP tool servers, or dynamic code interpreters inside non-root containers with strict SELinux and Seccomp profiles.
- **Kubernetes Pod Simulation**: Creating, testing, and exporting local Kubernetes-compatible pods (`podman generate kube` and `podman play kube`) prior to cluster deployment.
- **Systemd Service Integration**: Managing containerized home-lab services as native systemd unit files (`podman generate systemd` or systemd quadlets).

## Container Runtime Comparison

| Feature | Podman | Docker Engine | Containerd | Finch |
| :--- | :--- | :--- | :--- | :--- |
| **Daemon Architecture** | Daemonless (Process-Based) | Central Root Daemon (`dockerd`)| Central Daemon (`containerd`) | Daemonless Wrapper |
| **Rootless Native Security**| First-Class Kernel Namespaces | Optional Rootless Mode | High Setup Overhead | Native in VM Layer |
| **Native Pod Support** | Direct `podman pod` Engine | Requires Docker Compose | K8s CRI Only | Limited |
| **Systemd Quadlet Support**| Native Declarative Unit Files | None (Requires Compose) | Systemd Units | None |
| **FastMCP 3.1 Sandboxing** | Zero-Root Air-Gapped Runner | Socket-Exposed Runner | Production K8s Runner | Desktop Runner |
| **Kubernetes Compatibility**| Direct `play kube` Manifests | Requires Kind / Minikube | Native K8s CRI Engine | Native K8s Support |

## Resource Isolation & Kernel Governance Matrix

| Subsystem | Linux Mechanism | Podman Implementation | Security Guarantee |
| :--- | :--- | :--- | :--- |
| **User Identity** | User Namespaces (`subuid`/`subgid`) | Maps host non-root UID to container UID 0 | Root in container is host non-root UID 100000+ |
| **CPU Control** | Cgroups v2 (`cpu.max`) | `--cpus 1.5` / `CPUQuota=150%` | Prevents CPU exhaustion from rogue agent code |
| **Memory Ceiling** | Cgroups v2 (`memory.max`) | `--memory 512m` / `MemoryMax=512M` | Triggers OOM-killer without destabilizing host |
| **Syscall Filter** | Seccomp BPF filters | Default profile blocks ~44 dangerous syscalls | Prevents kernel exploit attempts and raw sockets |
| **Mandatory Access** | SELinux (`container_t`) | MCS labeling (`:z` / `:Z` volume mounts) | Prevents host path traversal outside volume |
| **Network Boundary** | Passt / Slirp4netns | `--network none` or `--network pasta` | Air-gaps network or isolates unprivileged stack |

## Strengths
- **Daemonless Architecture**: Directly executes containers as child processes, improving auditing, process isolation, and system reliability.
- **Rootless Security**: Enhances host security by isolating containerized workloads inside unprivileged Linux user namespaces.
- **Docker CLI Compatibility**: Near 100% command-line flag compatibility with Docker (`podman run`, `podman build`, `podman compose`).
- **Native Pod Support**: Supports grouping containers into pods that share network namespaces and IPC volumes, mirroring Kubernetes pods.
- **Systemd Quadlet Integration**: Native declaratively configured systemd integration for robust auto-restarting services on boot.

## Limitations
- **Docker Socket Bindings**: Third-party developer tools expecting direct socket access to `/var/run/docker.sock` require active `podman.socket` service emulation.
- **Platform Emulation Layer**: Operates natively on Linux; requires a lightweight VM (QEMU/VFKit via `podman machine`) on macOS and Windows workstations.
- **Rootless Networking Constraints**: Rootless networking (via `slirp4netns` or `pasta`) introduces minor networking latency and distinct port-binding rules compared to traditional rootful bridge networks.

## When to use it
- When container security and rootless execution are strict enterprise or compliance requirements.
- In multi-tenant HPC or corporate IT environments where users do not have `sudo` access.
- When prototyping workloads intended for Kubernetes deployment using native pod definitions.
- When building secure agent execution sandboxes for running untrusted LLM-generated code.

## When not to use it
- If your development workflow relies heavily on desktop GUI tools built exclusively for Docker Desktop without Podman Desktop configured.
- When running legacy automation scripts that hardcode direct access to host root Docker socket endpoints without socket emulation.

## Getting started

### Installation
On Fedora/RHEL:
```bash
sudo dnf install -y podman
```
On Ubuntu/Debian:
```bash
sudo apt-get update && sudo apt-get install -y podman
```
On macOS (via Homebrew):
```bash
brew install podman
podman machine init
podman machine start
```

### Basic Workflow
Run an isolated Nginx web server rootlessly:

```bash
podman run -d --name test-nginx -p 8080:80 nginx:alpine
```

## CLI examples

```bash
# 1. List active rootless containers
podman ps

# 2. Create a Kubernetes-style pod containing multiple containers
podman pod create --name ai-pod -p 8000:8000

# 3. Run a service inside the created pod
podman run -d --pod ai-pod --name inference-engine vllm/vllm-openai:latest

# 4. Generate Kubernetes YAML definition from a running pod
podman generate kube ai-pod > ai-pod.yaml

# 5. Launch a Kubernetes manifest directly in local Podman
podman play kube ai-pod.yaml
```

## API examples

This complete Python script implements a FastMCP 3.1 server that safely spawns ephemeral rootless Podman sandboxes to execute LLM code, using Pydantic v2 schemas for strict input validation and resource boundary enforcement.

```python
import subprocess
import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from fastmcp import FastMCP

# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Podman-Sandbox-Server")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Podman-Rootless-Sandbox-Server", version="3.1.0")

class ContainerPortBinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host_port: int = Field(..., ge=1, le=65535, description="Host interface port")
    container_port: int = Field(..., ge=1, le=65535, description="Internal container port")

class PodmanContainerSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Unique container instance name")
    image: str = Field(..., description="OCI image tag or digest")
    rootless: bool = Field(True, description="Enforce rootless execution mode")
    memory_limit_mb: int = Field(512, ge=128, le=4096, description="Container RAM memory ceiling in MB")
    cpu_limit: float = Field(1.0, ge=0.1, le=8.0, description="CPU cores cap")
    environment: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    ports: List[ContainerPortBinding] = Field(default_factory=list, description="Port mappings")
    command: Optional[List[str]] = Field(None, description="Container entrypoint command")
    airgap_network: bool = Field(True, description="Disable outbound network access")

class SandboxExecutionResponse(BaseModel):
    status: str = Field(..., description="Execution state: completed, error, or timed_out")
    exit_code: int = Field(default=0, description="Process exit code")
    stdout: str = Field(default="", description="Standard output stream")
    stderr: str = Field(default="", description="Standard error stream")
    execution_time_sec: float = Field(default=0.0, ge=0.0)
    spec_validated: bool = Field(True)

@mcp.tool(
    name="execute_in_podman_sandbox",
    description="Executes python code safely inside an air-gapped, rootless Podman sandbox container."
)
def execute_in_podman_sandbox(spec_json: str, code: str) -> str:
    """Parses PodmanContainerSpec via Pydantic v2 and runs code in an unprivileged container."""
    try:
        spec = PodmanContainerSpec.model_validate_json(spec_json)
        logger.info(f"Launching Podman sandbox '{spec.name}' with image '{spec.image}'")

        cmd = [
            "podman", "run", "--rm",
            "--name", f"sandbox-{spec.name}",
            "--memory", f"{spec.memory_limit_mb}m",
            "--cpus", str(spec.cpu_limit),
            "--security-opt", "no-new-privileges",
        ]

        if spec.airgap_network:
            cmd.extend(["--network", "none"])

        for k, v in spec.environment.items():
            cmd.extend(["--env", f"{k}={v}"])

        cmd.extend([spec.image, "python3", "-c", code])

        start_time = datetime.now()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        elapsed = (datetime.now() - start_time).total_seconds()

        response = SandboxExecutionResponse(
            status="completed" if result.returncode == 0 else "error",
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            execution_time_sec=elapsed
        )
        return response.model_dump_json(indent=2)

    except subprocess.TimeoutExpired:
        logger.error(f"Execution timed out in sandbox")
        err_res = SandboxExecutionResponse(
            status="timed_out",
            exit_code=-1,
            stdout="",
            stderr="Execution exceeded 30s timeout threshold.",
            execution_time_sec=30.0
        )
        return err_res.model_dump_json(indent=2)

    except ValidationError as e:
        logger.error(f"Pydantic validation failed: {e}")
        return json.dumps({"error": "Pydantic v2 Spec Validation Failed", "details": e.errors()})

    except Exception as e:
        logger.error(f"Unexpected Podman execution error: {e}")
        return json.dumps({"error": "System Error", "message": str(e)})

if __name__ == "__main__":
    test_spec = PodmanContainerSpec(
        name="test-agent-sandbox",
        image="python:3.11-slim",
        memory_limit_mb=256,
        cpu_limit=0.5,
        airgap_network=True
    )
    python_test_script = "import sys; print('Hello from Rootless Podman FastMCP 3.1 Sandbox!'); print('Python v' + sys.version.split()[0])"
    print(execute_in_podman_sandbox(test_spec.model_dump_json(), python_test_script))
```

## Systemd Quadlet & Systemd Unit Configurations

### Podman Systemd Quadlet (`~/.config/containers/systemd/fastmcp-sandbox.container`)
Podman Quadlet allows defining containers directly using systemd-like unit syntax. Quadlet automatically generates native systemd service files at boot time.

```ini
[Unit]
Description=FastMCP 3.1 Rootless Sandbox Agent Container
After=network-online.target
Wants=network-online.target

[Container]
Image=quay.io/homelab/fastmcp-sandbox-server:latest
ContainerName=fastmcp-agent-sandbox
Exec=python3 -m fastmcp.server --port 8080
PublishPort=8080:8080
Environment=LOG_LEVEL=INFO
Memory=1G
CPUQuota=100%
NoNewPrivileges=true
ReadOnlyRootfs=true
Volume=/var/run/user/1000/podman/podman.sock:/tmp/podman.sock:ro

[Service]
Restart=always
TimeoutStartSec=60

[Install]
WantedBy=default.target
```

### Production Systemd Unit (`podman-mcp-sandbox.service`)

For traditional systemd service deployment managing user-level Podman containers:

```ini
[Unit]
Description=Podman Rootless MCP Sandbox Service
After=network.target podman.socket
Requires=podman.socket
Documentation=https://docs.podman.io/

[Service]
Type=simple
User=jules
Group=jules
WorkingDirectory=/home/jules/mcp-sandbox
ExecStartPre=/usr/bin/podman system migrate
ExecStart=/usr/bin/podman run --name podman-mcp-sandbox \
    --rm \
    --pids-limit 100 \
    --memory 1024m \
    --cpus 1.5 \
    --network pasta \
    -p 8080:8080 \
    -v /home/jules/mcp-sandbox/data:/app/data:Z \
    quay.io/homelab/podman-mcp-sandbox:v3.1
ExecStop=/usr/bin/podman stop -t 10 podman-mcp-sandbox
Restart=always
RestartSec=5s
LimitNOFILE=65536

# Systemd Security Isolation
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=read-only
ReadWritePaths=/home/jules/mcp-sandbox/data

[Install]
WantedBy=default.target
```

## Operational Best Practices & Troubleshooting

### Rootless Storage & Systemd Rules
1. **SubUID/SubGID Mapping**: Verify that `/etc/subuid` and `/etc/subgid` assign a range of at least 65,536 subordinate IDs to your non-root user account (e.g., `jules:100000:65536`).
2. **Systemd Quadlets**: Store container unit definitions in `~/.config/containers/systemd/my-service.container`. Run `systemctl --user daemon-reload` to update Quadlet unit generators.
3. **SELinux Volume Relabeling**: When mounting host directories into rootless containers on SELinux-enforced Linux systems (Fedora/RHEL), append `:z` (shared) or `:Z` (private) flags to volume bind parameters (e.g., `-v /data/app:/app:Z`).

### Diagnostic Troubleshooting Matrix

| Symptom / Failure | Root Cause | Remediation Strategy |
| :--- | :--- | :--- |
| `Error: user code 100000 not in /etc/subuid` | Missing subordinate UID mapping for current user | Add entry `username:100000:65536` to `/etc/subuid` and `/etc/subgid` and run `podman system migrate`. |
| `Permission denied: /app/data` inside container | SELinux blocking host volume directory access | Append `:z` (shared) or `:Z` (private) flag to the volume volume bind flag (e.g., `-v /host/dir:/app/data:Z`). |
| `Cannot connect to Docker daemon socket` | Tool or SDK expects `/var/run/docker.sock` | Enable user Podman socket: `systemctl --user enable --now podman.socket` and export `DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock`. |
| `Pasta / Slirp4netns network connection failed` | Missing unprivileged network driver binary | Install `pasta` (passt) or `slirp4netns` package (`apt install pasta` / `dnf install passt`). |
| `Rootless container OOM killed immediately` | Memory limit smaller than container overhead | Ensure `--memory` is set to at least `256m` for Python / Node.js standard container runtimes. |

## Related tools / concepts
- **[Docker](docker.md)**: Classical container engine runtime.
- **[Docker Compose](docker-compose.md)**: Declarative multi-container deployment tool.
- **[K3s](k3s.md)**: Lightweight Kubernetes cluster distribution for home labs.
- **[Ramalama](ramalama.md)**: Container-native tool for running local AI models on Podman.

## Sources / references
- [Podman Official Site](https://podman.io/?ref=2026-09-21-audit)
- [Podman Documentation & Guides](https://docs.podman.io/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
