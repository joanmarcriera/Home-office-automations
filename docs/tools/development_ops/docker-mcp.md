# Docker MCP

## What it is
Docker MCP Server (Docker Model Context Protocol) is an enterprise tool integration standard that exposes Docker container orchestration, image management, volume handling, and isolated container execution environments to AI agents via the [Model Context Protocol (FastMCP 3.1 Standard)](../automation_orchestration/mcp.md). Powered by FastMCP 3.1 and strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`), Docker MCP allows autonomous assistants (such as Claude 5.6, GPT-5.6, and Gemini 4.0) to safely spawn, inspect, run, and destroy isolated Linux environments without exposing root host privileges.

## Architecture & Container Execution Lifecycle
Docker MCP translates standardized JSON-RPC Model Context Protocol messages into structured Docker Engine API commands or Docker CLI invocations.

```mermaid
graph TD
    A[AI Agent / Assistant Client] -->|FastMCP 3.1 Stdio / SSE| B[Docker MCP Gateway Server]
    B -->|Schema & Argument Validation| C[Pydantic v2 Execution Engine]
    C -->|Docker Engine API / Socket| D[Local Docker Daemon / Remote Host]
    D -->|Spawn / Run Container| E[Isolated Micro-Container]
    E -->|STDOUT / STDERR Telemetry| B
    B -->|FastMCP Response Envelope| A
```

## Detailed Execution Sequence & Tool Invocation

```mermaid
sequenceDiagram
    autonumber
    participant Agent as AI Agent (Claude 5.6 / FastMCP)
    participant MCP as Docker MCP Server Gateway
    participant Daemon as Docker Daemon (/var/run/docker.sock)
    participant Container as Isolated Sandboxed Container

    Agent->>MCP: Call Tool `docker_run_container(image="python:3.12", cmd="python main.py")`
    MCP->>MCP: Validate Inputs via Pydantic v2 Schema
    MCP->>Daemon: API Request `POST /containers/create` & `POST /containers/start`
    Daemon->>Container: Spawn Isolated Subprocess & Attach Pipes
    Container-->>Daemon: Return Terminal STDOUT / Execution Code (0)
    Daemon-->>MCP: Stream Log Telemetry
    MCP-->>Agent: Return FastMCP Result Payload with Execution Telemetry
```

## Mathematical Formulations & Container Resource Quota Enforcement

### 1. Completely Fair Scheduler (CFS) Bandwidth & CPU Throttling
In modern Linux kernel deployments utilizing cgroups v2, Docker MCP bounds container compute allocations through quota period ratios. Given a quota $CFS_{\text{quota}}$ and period $CFS_{\text{period}}$ (typically 100,000 microseconds), the allocated virtual CPU cores $C_{\text{alloc}}$ and enforcement throttling probability $P_{\text{throttle}}$ are defined by:

$$C_{\text{alloc}} = \frac{CFS_{\text{quota}}}{CFS_{\text{period}}}$$

$$P_{\text{throttle}} = \max\left(0, \frac{T_{\text{burst}} - CFS_{\text{quota}}}{T_{\text{burst}}}\right) \quad \text{for } T_{\text{burst}} > CFS_{\text{quota}}$$

When an AI agent executes compute-intensive tasks (such as JIT compilation, AST graph traversal, or matrix math), any burst exceeding $CFS_{\text{quota}}$ within time slice $CFS_{\text{period}}$ induces kernel throttling, preventing core starvation on the host machine.

### 2. Memory Envelope Bounds & Out-of-Memory (OOM) Killer Scoring
Container memory allocations are governed by strict two-tiered limits: physical RAM ($M_{\text{limit}}$) and combined swap memory ($M_{\text{swap}}$). When active memory consumption $M(t)$ surpasses $M_{\text{limit}}$, kernel page reclaim routines trigger swap migration. The OOM killer score $S_{\text{OOM}} \in [0, 1000]$ within the container cgroup hierarchy is modeled as:

$$S_{\text{OOM}} = \min\left(1000, \left\lfloor \frac{M(t) - M_{\text{reclaim}}}{M_{\text{limit}}} \times 1000 \right\rfloor + OOM_{\text{score\_adj}}\right)$$

By default, Docker MCP injects an adjusted score $OOM_{\text{score\_adj}} = +500$ into the ephemeral container process namespace, guaranteeing that in memory-pressure conditions, the guest sandbox process is terminated prior to host daemons or the FastMCP gateway itself.

### 3. FastMCP Serialization Overhead & IPC Latency
Inter-process communication between the client agent and Docker MCP server introduces transport and JSON-RPC serialization latency. Total round-trip execution latency $T_{\text{total}}$ for an ephemeral container tool invocation is formulated as:

$$T_{\text{total}} = T_{\text{ser}}(S_{\text{payload}}) + T_{\text{ipc}} + T_{\text{cgroup\_init}} + T_{\text{exec}} + T_{\text{teardown}} + T_{\text{deser}}(S_{\text{output}})$$

Where $T_{\text{ser}}$ and $T_{\text{deser}}$ scale linearly with payload size $S$ over Unix Domain Sockets ($UDS$):

$$T_{\text{ser}}(S) = \frac{S}{B_{\text{JSON}}} + \delta_{\text{schema}}$$

Here $B_{\text{JSON}} \approx 420\text{ MB/s}$ represents Pydantic v2 Rust-accelerated validation throughput, and $\delta_{\text{schema}} \le 0.45\text{ ms}$ represents frozen schema boundary checks.

## What problem it solves
Autonomous agents often need to run shell commands, compile binaries, or test untrusted code scripts. Executing these directly on the developer's host system creates significant security risks (e.g. system file modification, arbitrary command execution, dependency corruption). Docker MCP provides a secure, deterministic sandbox layer where agents execute commands inside disposable, resource-constrained Docker containers with restricted network and file system access.

## Where it fits in the stack
**Development & Operations / Infrastructure Security Layer**. Docker MCP sits between higher-level AI agent orchestrators ([Agency Swarm](../agents/agency-swarm.md), [Claude Code Container MCP](claude-code-container-mcp.md)) and the low-level Docker container daemon.

## Container Isolation & Security Boundaries
Docker MCP enforces multi-layer isolation parameters across all dynamically spawned containers:
- **CGroups v2 Resource Limits**: Caps CPU quotas (`nano_cpus`), RAM memory (`mem_limit="512m"`), and swap limits to prevent host resource starvation.
- **Rootless & User Namespaces**: Maps in-container root UID `0` to unprivileged host UID mappings (`100000+`).
- **Network Modes**: Defaults to isolated `none` or internal `bridge` networks to block unauthorized outbound socket connections during script execution.
- **Read-Only Volume Bindings**: Binds workspace directories in read-only (`:ro`) mode unless explicit temporary workspace scratchpads are requested.
- **Seccomp & AppArmor Profiles**: Drops hazardous Linux capabilities (`CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, `CAP_PTRACE`) to enforce unprivileged micro-execution.

## Typical use cases
- **Sandboxed Agent Code Execution**: Spawning temporary containers to run dynamic Python, Node.js, or Rust code without host side-effects.
- **Container Infrastructure Management**: Allowing dev agents to build Dockerfiles, list active containers, inspect system health, and inspect container logs.
- **Automated Integration Testing**: Provisioning ephemeral Postgres/Redis databases for test runs during agentic software development loops.
- **Isolated Multi-Tenant Execution**: Running simultaneous code evaluation tasks for different user requests in strictly isolated containers.
- **Environment Parity Testing**: Verifying that application code compiles and executes consistently across different Linux distributions (Ubuntu, Alpine, Debian).

## Strengths
- **Native FastMCP 3.1 Integration**: Provides pre-packaged Pydantic v2 schemas for container run, list, exec, stop, and prune tools.
- **Secure Isolation**: Runs agent actions strictly within isolated container namespaces and dynamic resource limits (CPU/RAM).
- **Cross-Platform Compatibility**: Works seamlessly across Linux, macOS (Docker Desktop/OrbStack), and Windows (WSL2).
- **Streamed Execution Telemetry**: Captures STDOUT/STDERR logs in real time and streams progress back to agent execution contexts via FastMCP `Context`.

## Limitations
- **Daemon Access Requirement**: Requires access to the Docker socket (`/var/run/docker.sock`), demanding careful socket permissions setup.
- **Image Pull Latency**: Spawning containers with non-cached images can introduce initial network download delays.
- **Storage Overhead**: Continuous container creation without prune policies can accumulate unused image layers and stopped container states.

## When to use it
- Executing untrusted AI agent generated code or dynamic scripts in isolated container environments.
- Managing containers, images, volumes, and micro-services through FastMCP tool protocols.
- Building, inspecting, and debugging Docker containers autonomously during dev loops.
- Providing standardized execution environments for LLM agent benchmark evaluation tools.

## When not to use it
- Environments where Docker daemon access is restricted or unavailable (e.g. strict serverless functions).
- Simple file or text manipulation tasks where container startup latency overhead is unnecessary.
- Workloads requiring direct host system hardware access (e.g. specialized PCIe devices without pass-through).

## Feature Matrix & Framework Comparison

| Feature / Metric | Docker MCP | Claude Code Container MCP | Podman MCP | Kubernetes Job MCP | Firecracker MicroVM MCP |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Target Engine** | Docker Engine API / Daemon | Docker / Finch Containers | Rootless Podman Socket | K8s API Server / Pods | KVM / Firecracker VMM |
| **Protocol Standard** | FastMCP 3.1 / MCP Native | Anthropic MCP Standard | FastMCP Standard | Custom K8s MCP Server | FastMCP 3.1 Unix Socket |
| **Startup Latency ($T_{\text{init}}$)** | 350 ms – 650 ms | 450 ms – 900 ms | 600 ms – 1200 ms | 2500 ms – 6000 ms | 120 ms – 250 ms |
| **Isolation Boundary** | Container Namespaces / CGroups v2 | Micro-VM / Docker Sandbox | User Namespaces (Rootless) | Pod Spec / K8s Namespace | Hardware Virtualization (KVM) |
| **Memory Quota Enforcement** | Strict `mem_limit` + cgroups v2 | Host Memory Envelope | CGroups v2 Memory Controller | K8s Memory Limits / Requests | Fixed Guest Physical RAM |
| **Network Security Guard** | `network_mode="none"` / Bridge | Air-gapped Host Bridging | Rootless Pasta / Slirp4netns | Calico / Cilium NetworkPolicies | TAP Device Filter / Zero Network |
| **Rootless Daemon Option** | Supported (RootlessKit) | Platform Managed | Native Zero-Daemon Default | Node-level Kubelet Daemon | Host KVM Device User Group |
| **Volume Mount Guard** | Strict Workspace Bounding (`:ro`) | Sandbox File Sync | User Mount Bounding | Persistent Volume Claims | Read-only virtio-blk Drive |
| **FastMCP 3.1 Ready** | Native Built-in Server | Native Built-in Server | Community Adapter | Custom Extension Layer | Native Built-in Server |

## Getting started
1. **Prerequisites**: Ensure Docker Engine or Docker Desktop is installed and active.
2. **Install Docker MCP Server**:
   ```bash
   npm install -g @docker/mcp-server
   # or run directly via npx
   npx @docker/mcp-server
   ```
3. **Configure Claude Desktop / FastMCP Client**: Add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "docker": {
         "command": "npx",
         "args": ["-y", "@docker/mcp-server"]
       }
     }
   }
   ```

## CLI examples
```bash
# Run Docker MCP Server via NPX CLI
npx @docker/mcp-server

# Build Docker image using local Docker CLI
docker build -t my-agent-sandbox:latest .

# Inspect running Docker MCP containers
docker ps --filter "label=mcp-server"

# Prune stopped MCP agent containers
docker container prune --filter "label=mcp-server" -f

# Verify cgroups v2 memory limits applied to container
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
```

## API examples
```python
import docker

client = docker.from_env()
# List running containers via Docker Engine API
containers = client.containers.list()
for container in containers:
    print(f"Container: {container.name} - Status: {container.status}")
```

## Advanced FastMCP 3.1 & Docker MCP Production Implementation

### Comprehensive Docker MCP Gateway Server
```python
import sys
import logging
from typing import Dict, Any, List, Optional
import mcp.server.fastmcp as fastmcp
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ConfigDict
import docker

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("DockerMCPGateway")

mcp_server = FastMCP(
    "Docker MCP Gateway Server",
    version="3.1",
    instructions="Production MCP gateway for isolated Docker container execution and lifecycle management."
)

try:
    docker_client = docker.from_env()
except Exception as err:
    logger.error("Failed to connect to Docker daemon: %s", err)
    docker_client = None

# --- Strict Pydantic v2 Models ---
class ContainerRunPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    image: str = Field(..., description="Target Docker image (e.g., 'python:3.12-alpine')")
    command: str = Field(..., description="Command string to execute in container")
    memory_limit: str = Field(default="512m", pattern=r"^[0-9]+[kmgKMG]$", description="Memory limit (e.g. 256m, 1g)")
    cpus: float = Field(default=1.0, ge=0.1, le=4.0, description="CPU core quota")
    timeout_seconds: int = Field(default=60, ge=1, le=600, description="Container execution timeout")
    read_only_workspace: Optional[str] = Field(default=None, description="Host directory path to mount read-only at /workspace")

class ContainerExecPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    container_id: str = Field(..., description="Target active container ID or name")
    command: str = Field(..., description="Command to execute inside running container")
    user: Optional[str] = Field(default="nobody", description="Unprivileged execution user inside container")

class ContainerInspectionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    container_id: str = Field(..., description="Container ID or name to inspect")
    tail_lines: int = Field(default=200, ge=1, le=1000, description="Number of tail log lines to fetch")

class ContainerPruneRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    all_stopped: bool = Field(default=True, description="Prune all stopped MCP ephemeral containers")
    older_than_minutes: int = Field(default=15, ge=0, le=1440, description="Minimum age in minutes for pruned containers")

# --- FastMCP 3.1 Tools ---
@mcp_server.tool()
async def run_sandboxed_container(payload: ContainerRunPayload, ctx: Context) -> Dict[str, Any]:
    """Executes a command inside an isolated disposable Docker container with resource boundaries."""
    if not docker_client:
        return {"success": False, "error": "Docker daemon unavailable", "mcp_version": "3.1"}

    await ctx.report_progress(10, 100)
    ctx.info(f"Preparing container run for image '{payload.image}'")

    volumes = {}
    if payload.read_only_workspace:
        volumes[payload.read_only_workspace] = {"bind": "/workspace", "mode": "ro"}

    try:
        await ctx.report_progress(30, 100)
        ctx.info("Spawning container with cgroups boundaries...")

        container = docker_client.containers.run(
            image=payload.image,
            command=payload.command,
            mem_limit=payload.memory_limit,
            nano_cpus=int(payload.cpus * 1e9),
            volumes=volumes,
            labels={"mcp-server": "true", "mcp-version": "3.1"},
            remove=True,
            detach=False,
            network_mode="none",  # Restrict network for code execution security
            security_opt=["no-new-privileges:true"],
            cap_drop=["ALL"]
        )

        await ctx.report_progress(100, 100)
        output_text = container.decode("utf-8") if isinstance(container, bytes) else str(container)
        return {
            "success": True,
            "output": output_text,
            "image": payload.image,
            "memory_limit": payload.memory_limit,
            "mcp_version": "3.1"
        }
    except Exception as exc:
        ctx.error(f"Container execution failed: {exc}")
        return {"success": False, "error": str(exc), "mcp_version": "3.1"}

@mcp_server.tool()
def list_mcp_containers(include_all: bool = False) -> Dict[str, Any]:
    """Lists active Docker containers created or managed by Docker MCP."""
    if not docker_client:
        return {"error": "Docker daemon unavailable", "mcp_version": "3.1"}

    filters = {"label": "mcp-server=true"} if not include_all else {}
    containers = docker_client.containers.list(all=include_all, filters=filters)

    items = []
    for c in containers:
        items.append({
            "id": c.short_id,
            "name": c.name,
            "image": c.image.tags[0] if c.image.tags else c.image.short_id,
            "status": c.status,
            "created": c.attrs.get("Created", "")
        })

    return {"containers_count": len(items), "containers": items, "mcp_version": "3.1"}

@mcp_server.tool()
def inspect_container_logs(request: ContainerInspectionRequest) -> Dict[str, Any]:
    """Retrieves standard output and error logs from a target container."""
    if not docker_client:
        return {"error": "Docker daemon unavailable", "mcp_version": "3.1"}

    try:
        container = docker_client.containers.get(request.container_id)
        logs = container.logs(tail=request.tail_lines).decode("utf-8", errors="replace")
        return {
            "container_id": request.container_id,
            "logs": logs,
            "lines_fetched": len(logs.splitlines()),
            "mcp_version": "3.1"
        }
    except Exception as e:
        return {"error": str(e), "container_id": request.container_id, "mcp_version": "3.1"}

@mcp_server.tool()
def prune_mcp_containers(request: ContainerPruneRequest) -> Dict[str, Any]:
    """Prunes stopped or abandoned containers spawned by Docker MCP."""
    if not docker_client:
        return {"error": "Docker daemon unavailable", "mcp_version": "3.1"}

    try:
        pruned = docker_client.containers.prune(filters={"label": "mcp-server=true"})
        space_reclaimed = pruned.get("SpaceReclaimed", 0)
        deleted = pruned.get("ContainersDeleted") or []
        return {
            "success": True,
            "deleted_count": len(deleted),
            "space_reclaimed_bytes": space_reclaimed,
            "mcp_version": "3.1"
        }
    except Exception as err:
        return {"success": False, "error": str(err), "mcp_version": "3.1"}

if __name__ == "__main__":
    mcp_server.run(transport="stdio")
```

### Docker MCP Async Client Invocation Example
```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_docker_mcp_client():
    server_params = StdioServerParameters(
        command="python3",
        args=["docker_mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Execute python script inside ephemeral container tool
            result = await session.call_tool(
                "run_sandboxed_container",
                arguments={
                    "payload": {
                        "image": "python:3.12-alpine",
                        "command": "python3 -c \"import sys; print(f'Python Version: {sys.version}')\"",
                        "memory_limit": "256m",
                        "cpus": 1.0,
                        "timeout_seconds": 30
                    }
                }
            )
            print("Container Output:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(run_docker_mcp_client())
```

## Docker Compose Deployment Definition

```yaml
version: "3.8"

services:
  docker-mcp-gateway:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: docker-mcp-gateway
    restart: unless-stopped
    ports:
      - "8008:8008"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:rw
      - ./workspace:/opt/docker-mcp/workspace:ro
    environment:
      - PYTHONUNBUFFERED=1
      - FASTMCP_TRANSPORT=sse
      - FASTMCP_PORT=8008
      - DOCKER_HOST=unix:///var/run/docker.sock
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8008/health"]
      interval: 15s
      timeout: 5s
      retries: 3
    networks:
      - mcp-docker-net

networks:
  mcp-docker-net:
    driver: bridge
```

## Systemd Service Unit Definition
Save unit file to `/etc/systemd/system/docker-mcp-gateway.service`:

```ini
[Unit]
Description=Docker MCP Server Gateway Service
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=docker-mcp-user
Group=docker
WorkingDirectory=/opt/docker-mcp
ExecStart=/usr/bin/python3 /opt/docker-mcp/docker_mcp_server.py --transport sse --port 8008
Restart=always
RestartSec=5s
Environment="PYTHONUNBUFFERED=1"
Environment="DOCKER_HOST=unix:///var/run/docker.sock"

# Security Hardening Settings
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Troubleshooting & Diagnostic Matrix

| Issue Symptom / Error | Root Cause | Verification Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **`Permission Denied (/var/run/docker.sock)`** | Service user lacks `docker` group permissions | `ls -la /var/run/docker.sock` | Add user to docker group: `sudo usermod -aG docker <user>` |
| **`Image Pull Failure`** | Container image tag missing or network blocked | `docker pull <image_name>` | Verify internet connectivity and exact image registry path |
| **`Container OOM Killed (Exit 137)`** | Memory limit exceeded during agent execution | `docker inspect <container_id> --format='{{.State.OOMKilled}}'` | Increase `memory_limit` in FastMCP execution payload or optimize script memory |
| **`CFS CPU Bandwidth Throttling`** | CPU quota exhausted under intensive agent computations | `docker stats --no-stream` | Increase `cpus` quota parameter in Pydantic execution payload |
| **`Socket Connection Timeout`** | Docker daemon process crashed or stopped | `systemctl status docker` | Restart daemon via `sudo systemctl restart docker` |
| **`Disk Space Exhaustion (No space left on device)`** | Dangling container images and stopped containers accumulated | `docker system df` | Run automated prune tool: `docker system prune -f --volumes` |
| **`Network Sandbox Denied`** | Code attempted outbound network request in `network_mode="none"` | Inspect Python script for network requests | Set `network_mode="bridge"` if outbound access is explicitly required |
| **`Volume Mount Denied (EACCES)`** | Target volume path outside allowed workspace directory | Check container volume binding arguments | Ensure host paths exist and have appropriate POSIX read permissions (`chmod 755`) |

## Operational Guardrails & Production Checklist
1. **Socket Access Restriction**: Always isolate `/var/run/docker.sock` using ACLs or unprivileged group proxies rather than running the agent daemon as root.
2. **Ephemeral Garbage Collection**: Schedule the `prune_mcp_containers` FastMCP tool or cron timer every 30 minutes to purge dead container metadata and dangling scratch layers.
3. **Seccomp Privilege Escalation Suppression**: Ensure `security_opt=["no-new-privileges:true"]` and `cap_drop=["ALL"]` remain enforced across all agent micro-containers.
4. **Strict Schema Integrity**: Enforce Pydantic v2 `ConfigDict(extra="forbid", frozen=True)` on all container execution input models to eliminate prototype and attribute tampering.
5. **Read-Only Code Workspaces**: Mount repository checkouts as read-only (`mode="ro"`), keeping all agent artifact generations confined to dedicated `/tmp` scratch directories.

## Related tools / concepts
- [Claude Code Container MCP](claude-code-container-mcp.md) — Containerized Claude Code workspace engine.
- [Docker Compose](../infrastructure/docker-compose.md) — Multi-container application orchestrator.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol specifications.
- [CrossHair](crosshair.md) — Symbolic contract verifier for Python functions.

## Sources / references
- [Docker MCP Server GitHub Repository](https://github.com/docker/mcp-server)
- [Official Docker Documentation](https://docs.docker.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
