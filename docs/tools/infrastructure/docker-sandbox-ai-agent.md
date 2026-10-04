# Docker Sandbox for AI Agents

## What it is
**Docker Sandbox for AI Agents** is an enterprise-grade, secure containerized runtime architecture specifically tailored for isolated, deterministic execution of autonomous AI agent tool calls, dynamic code execution, and untrusted workload evaluation. By wrapping container primitives with fine-grained capability drops, isolated Linux namespaces, read-only root filesystems, ephemeral micro-VM backends, and strict resource control limits, Docker Sandbox provides LLM agents with safe environment execution without risking host system compromise or unintended enterprise network exposure.

As generative AI models increasingly write, execute, and iterate on complex software code, terminal commands, and system scripts (via MCP tools, code interpreter extensions, and autonomous multi-agent loops), traditional host-level or non-isolated process execution poses severe security risks. Docker Sandbox for AI Agents transforms Docker environments into ephemeral, zero-trust micro-executors that spin up in milliseconds, run untrusted agent actions inside jailed namespaces, capture output streams, and tear down immediately upon task completion.

```
+-----------------------------------------------------------------------------------+
|                        DOCKER SANDBOX FOR AI AGENTS ARCHITECTURE                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------------+       +-----------------------------------------+  |
|  | Autonomous Agent / FastMCP| ----> | Docker Sandbox Orchestrator Engine     |  |
|  | Tool Invocation Request   |       | (Micro-VM / Seccomp / Egress Proxy)     |  |
|  +---------------------------+       +-----------------------------------------+  |
|                                                           |                       |
|                                                           v                       |
|                                      +-----------------------------------------+  |
|                                      | Ephemeral Isolated Container Environment |  |
|                                      | - Read-Only Root Filesystem (/root)     |  |
|                                      | - Tempfs Mounts (/tmp, /workspace)      |  |
|                                      | - Dropped Linux Capabilities (ALL)      |  |
|                                      | - Strict cgroups v2 Memory & CPU Limits |  |
|                                      +-----------------------------------------+  |
|                                                           |                       |
|                                                           v                       |
|  +---------------------------+       +-----------------------------------------+  |
|  | Structured Output Capture | <---- | Execution Results, Logs & Exit Status   |  |
|  | (JSON Stream / FastMCP)   |       | (Enforced Timeout Execution Boundary)   |  |
|  +---------------------------+       +-----------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
- **Arbitrary Code Execution Risks**: Prevents LLM-generated code or malicious agent payloads from accessing host filesystems, environment variables, cloud credential stores, or system sockets.
- **Resource Exhaustion & Denial of Service**: Enforces strict CPU, memory, and disk IO limits via cgroups v2, preventing rogue infinite loops or fork bombs from overwhelming host servers.
- **Egress Network Exfiltration**: Restricts container network egress to pre-approved domains or operates in complete offline bridge mode (`--net=none`) to block unauthorized data exfiltration or command-and-control phone-home calls.
- **Environment Contamination & State Pollution**: Guarantees a pristine, reproducible starting environment for every tool call execution using copy-on-write ephemeral layers that wipe state automatically upon completion.

## Where it fits in the stack
**Infrastructure / Execution Environments / Agent Security Security**. Docker Sandbox for AI Agents operates at the foundation layer of the agent execution stack, directly underlying agent frameworks, MCP tool servers, and automated code interpreters.

```
+-----------------------------------------------------------------------------------+
|                            AGENT EXECUTION SECURITY STACK                         |
+-----------------------------------------------------------------------------------+
| Agent / Reasoning Layer : FastMCP 3.1 / Claude Code / AutoGen / LangGraph          |
+-----------------------------------------------------------------------------------+
| Tool Routing & Dispatch : MCP Tool Servers / Code Interpreter API Gateways        |
+-----------------------------------------------------------------------------------+
| Isolation Engine        : Docker Sandbox for AI Agents (Seccomp / AppArmor / gVisor)|
+-----------------------------------------------------------------------------------+
| System Infrastructure   : Linux Kernel (cgroups v2, namespaces, OverlayFS, eBPF)   |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **LLM Code Interpreter Execution**: Safely evaluating Python, Bash, Node.js, or Rust code generated by LLMs during data analysis, visualization, or algorithmic problem-solving tasks.
- **Automated Repository Editing & Testing**: Running test suites, linters, and build commands inside ephemeral container environments when AI software engineering agents (e.g., Claude Code, Plandex) modify codebases.
- **Untrusted Web Scraping & Document Parsing**: Isolating headless browser automation (Playwright/Puppeteer) and document parsing engines (Tika/pdfplumber) to prevent drive-by download exploits or memory corruption payloads.
- **Multi-Tenant AI Workload Hosting**: Operating SaaS platforms that allow external users to run dynamic agent workflows safely on shared cloud compute infrastructure.

## Strengths
- **Native Ecosystem Support**: Leverages standard OCI image formats, Dockerfiles, and existing container registries without requiring customized virtual machine infrastructure.
- **Sub-Second Spin-up Latency**: Ephemeral sandbox containers instantiate in under 200 milliseconds when utilizing pre-warmed base images and optimized storage drivers.
- **Deep Kernel-Level Security**: Combines Seccomp syscall filtering, AppArmor profiles, non-root user execution, and capability dropping (`cap-drop=ALL`) for defense-in-depth isolation.
- **Seamless FastMCP Integration**: Easy integration into FastMCP 3.1 tool interfaces, returning stdout, stderr, and exit codes cleanly as structured JSON schemas.

## Limitations
- **Container Escape Vulnerabilities**: Pure container isolation shares the host Linux kernel; zero-day kernel vulnerabilities could theoretically allow privilege escalation without micro-VM hypervisors (such as Kata Containers or Firecracker).
- **Cold-Start Latency for Heavy Workloads**: Large Docker images containing multi-gigabyte data science libraries (PyTorch, TensorFlow, CUDA drivers) require image caching strategies to avoid startup delays.
- **State Persistence Complexity**: Ephemeral execution models require explicit volume binding or artifact export routines if the agent needs to preserve generated files or test results across multiple turns.

## When to use it
- When allowing AI agents to generate and execute shell commands or code snippets dynamically in production environments.
- When building multi-tenant agent platforms that execute user-submitted code or third-party MCP tool plugins.
- To prevent agent hallucination errors or runaway scripts from damaging host servers or exfiltrating sensitive environment keys.
- When needing reproducible, isolated environments with custom dependency runtimes (Python packages, CLI tools, system libraries).

## When not to use it
- For static API tool calls (e.g., fetching weather forecasts, querying internal REST APIs) where no dynamic code execution takes place.
- In extreme low-resource microcontrollers or embedded devices where container daemon overhead is prohibitive.
- When micro-VM level hypervisor isolation (e.g., AWS Firecracker or Kata Containers) is strictly required by regulatory compliance standards for multi-tenant kernel separation.

## Getting started

### Prerequisites
- Docker Engine 24.0+ or Docker Desktop with cgroups v2 enabled.
- Python 3.10+ with `docker` SDK, `pydantic` v2, and `fastmcp` installed.

### Verification of Docker Security Capabilities
```bash
# Verify Docker security capabilities and default runtime profile
docker info --format '{{json .SecurityOptions}}' | jq .

# Test dropped capability execution with read-only root filesystem
docker run --rm \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  alpine:latest whoami
```

### Quickstart Execution with Python Docker SDK
```python
import docker

client = docker.from_env()

container = client.containers.run(
    image="python:3.11-slim",
    command=["python", "-c", "print('Hello from isolated AI Sandbox!')"],
    network_mode="none",
    mem_limit="128m",
    nano_cpus=1000000000, # 1 CPU
    cap_drop=["ALL"],
    read_only=True,
    security_opt=["no-new-privileges:true"],
    remove=True,
    stdout=True,
    stderr=True
)

print("Sandbox Execution Output:", container.decode("utf-8"))
```

## CLI examples

### Running Untrusted Bash Command in Hardened Docker Sandbox
```bash
# Execute untrusted bash payload in fully isolated container
docker run --rm \
  --name agent-sandbox-exec \
  --network none \
  --memory 256m \
  --cpus 1.0 \
  --pids-limit 64 \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --tmpfs /workspace:rw,nosuid,size=128m \
  --workdir /workspace \
  python:3.11-slim \
  bash -c "python3 -c 'import sys; print(\"Evaluating payload safely inside sandbox\")'"
```

### Inspecting Resource Constraints and Seccomp Profile
```bash
# Check container resource utilization and status
docker stats agent-sandbox-exec --no-stream

# Run container with custom strict seccomp profile
docker run --rm \
  --security-opt seccomp=default_seccomp_profile.json \
  --network none \
  alpine:latest uname -a
```

## API examples

### FastMCP 3.1 Integration Server
This example demonstrates a FastMCP 3.1 server that safely executes arbitrary Python code inside an ephemeral, hardened Docker sandbox environment:

```python
from fastmcp import FastMCP
import docker
from pydantic import BaseModel, Field
import time

mcp = FastMCP("Docker-Agent-Sandbox")
docker_client = docker.from_env()

class SandboxCodeRequest(BaseModel):
    code_snippet: str = Field(..., description="Python code block to execute in the isolated sandbox")
    timeout_seconds: int = Field(default=10, ge=1, le=60, description="Maximum execution timeout")
    memory_limit_mb: int = Field(default=256, ge=64, le=1024, description="RAM limit in Megabytes")

class SandboxCodeResponse(BaseModel):
    stdout: str = Field(..., description="Captured standard output")
    stderr: str = Field(..., description="Captured standard error")
    exit_code: int = Field(..., description="Process exit code (0 for success)")
    execution_time_ms: float = Field(..., description="Duration of container execution in milliseconds")

@mcp.tool()
def execute_python_sandbox(request: SandboxCodeRequest) -> SandboxCodeResponse:
    """Executes untrusted Python code inside an isolated, security-hardened Docker container sandbox."""
    start_time = time.time()

    # Format inline command
    command = ["python", "-c", request.code_snippet]

    try:
        container = docker_client.containers.run(
            image="python:3.11-slim",
            command=command,
            network_mode="none",  # Complete network isolation
            mem_limit=f"{request.memory_limit_mb}m",
            nano_cpus=1000000000, # 1 CPU limit
            pids_limit=32,        # Block fork bombs
            cap_drop=["ALL"],
            read_only=True,
            security_opt=["no-new-privileges:true"],
            tmpfs={"/tmp": "rw,noexec,nosuid,size=32m", "/workspace": "rw,nosuid,size=64m"},
            working_dir="/workspace",
            detach=False,
            stdout=True,
            stderr=True,
            remove=True
        )
        stdout_str = container.decode("utf-8")
        stderr_str = ""
        exit_code = 0
    except docker.errors.ContainerError as err:
        stdout_str = ""
        stderr_str = err.stderr.decode("utf-8") if err.stderr else str(err)
        exit_code = err.exit_status
    except Exception as ex:
        stdout_str = ""
        stderr_str = f"Sandbox Exception: {str(ex)}"
        exit_code = -1

    elapsed_ms = round((time.time() - start_time) * 1000, 2)
    return SandboxCodeResponse(
        stdout=stdout_str,
        stderr=stderr_str,
        exit_code=exit_code,
        execution_time_ms=elapsed_ms
    )

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Security Configuration & Schema Validation
```python
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class SandboxSecurityConfig(BaseModel):
    image: str = Field(..., description="Docker base image tag")
    cap_drop: List[str] = Field(default_factory=lambda: ["ALL"], description="Linux capabilities to drop")
    network_mode: str = Field(default="none", description="Network driver configuration")
    read_only_root: bool = Field(default=True, description="Mount root filesystem as read-only")
    max_memory_mb: int = Field(default=256, ge=64, le=4096)
    cpu_count: float = Field(default=1.0, ge=0.1, le=8.0)

    @field_validator("network_mode")
    @classmethod
    def validate_network(cls, v: str) -> str:
        allowed = ["none", "bridge", "host"]
        if v not in allowed:
            raise ValueError(f"Network mode '{v}' must be one of {allowed}")
        if v == "host":
            raise ValueError("Host network mode is prohibited in secure sandbox environments")
        return v

# Schema validation demonstration
try:
    config = SandboxSecurityConfig(
        image="python:3.11-slim",
        network_mode="none",
        read_only_root=True,
        max_memory_mb=512,
        cpu_count=2.0
    )
    print("Validated Sandbox Configuration:", config.model_dump_json(indent=2))
except ValidationError as err:
    print("Security Schema Validation Error:", err.json())
```

## Related tools / concepts
- [Docker](../infrastructure/docker.md) — Fundamental containerization platform for enterprise applications.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standard framework for building high-performance MCP servers.
- [Open-Interpreter](../automation_orchestration/open-interpreter.md) — Natural language interface for executing local computer code.
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md) — Containerized MCP environment designed for Claude agentic execution.
- gVisor — Application kernel providing sandbox isolation for containers.

## Sources / references
- [Docker Security for AI Workloads](https://www.infoq.com/news/2026/10/docker-sandbox-ai-agent/)
- [Docker Engine Security Hardening Guide](https://docs.docker.com/engine/security/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
