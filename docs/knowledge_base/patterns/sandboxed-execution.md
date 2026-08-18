# Sandboxed Code Execution

## What it is

- **Strict Process Isolation**: Running code inside ephemeral container runtimes, WebAssembly sandboxes, or gVisor/Firecracker microVMs to prevent unauthorized host filesystem or memory access.
- **Resource Constraints (cgroups v2)**: Enforcing hard limits on CPU usage, RAM allocation, execution timeout limits, disk I/O, and file descriptor allocation.
- **Network Air-Gapping & Policy Filtering**: Disabling network access by default or enforcing eBPF/iptables outbound destination filtering to prevent exfiltration or unauthorized API access.
- **Syscall Restrictions (seccomp & AppArmor)**: Restricting available kernel system calls (blocking `ptrace`, raw socket creation, kernel module loading) to neutralize container breakout vectors.
- **Ephemeral Cleanup & Snapshot Restores**: Booting clean sandbox environments in milliseconds and immediately destroying sandbox instances after execution completion.


## What problem it solves
- Eliminates arbitrary code execution (ACE), privilege escalation, and host filesystem compromise risks when running untrusted, LLM-generated code.
- Prevents resource exhaustion and network exfiltration during autonomous agent coding and data analysis tasks.

## Where it fits in the stack
- Sits in the **Security & Execution Boundary** layer of autonomous coding agents and evaluation engines.
- Wraps agentic tool calls (Bash, Python, Node.js) inside isolated cgroup/seccomp containers or microVMs.

## Typical use cases

- **Autonomous Coding Agents**: Safely running unit tests, linting scripts, and code generation outputs produced by coding assistants (Claude Engineer, OpenCode, Aider).
- **Data Copilot Data Analysis**: Executing pandas/polars/matplotlib code generated on user spreadsheets without risking corporate network exposure.
- **Web Scraping & DOM Rendering**: Running browser automation tools (Puppeteer, Playwright) to scrape untrusted external web pages safely.
- **Benchmark Evaluation Platforms**: Running untrusted code generation test suites (HumanEval, MultiPL-E, SWE-bench) across multi-tenant evaluation infrastructure.


## Strengths

- **Enterprise Security Compliance**: Mitigates prompt injection, malicious code generation, and arbitrary code execution (ACE) risks in production AI deployments.
- **Multi-Tenant Isolation**: Prevents side-channel data leaks and cross-agent memory pollution in shared multi-agent servers.
- **Deterministic Reproducibility**: Clean, reproducible base images ensure consistent script evaluation regardless of host system configuration.


## Limitations

- **Latency Overhead**: MicroVM creation and container startup introduce execution latency compared to native host execution (mitigated by pre-warmed sandbox pools).
- **Tooling Constraints**: Air-gapped sandboxes prevent script installation of missing PyPI/npm packages at runtime without pre-built environment images or proxy mirrors.


## When to use it

- When building agentic platforms that execute LLM-generated code, shell scripts, or raw queries.
- When running multi-tenant coding platforms processing user-submitted or agent-generated scripts.
- When enterprise security standards prohibit direct execution of AI code output on host developer machines or production servers.


## When not to use it
- When executing fully trusted, pre-compiled static system maintenance scripts on dedicated isolated hardware.
- When minimal execution latency (<1ms) is strictly required and process isolation overhead is prohibitive.

## Getting started

```
+-------------------------------------------------------------------+
|                        Host / Agent Engine                        |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   | FastMCP 3.1 Agent / LLM Code Generation Output            |   |
|   +-----------------------------------------------------------+   |
|                                ||                                 |
|         Validate Code Payload via Pydantic v2 Schema              |
|                                ||                                 |
|                                \/                                 |
|   +-----------------------------------------------------------+   |
|   | Sandboxed Execution Orchestrator (gVisor / Docker / Wasm) |   |
|   +-----------------------------------------------------------+   |
+-------------------------------------------------------------------+
                                 ||
                 Isolated Container / MicroVM Boundary
                                 ||
                                 \/
+-------------------------------------------------------------------+
| Ephemeral Sandbox Instance                                        |
|                                                                   |
|  - cgroups v2 Limits (RAM: 512MB, CPU: 1.0)                        |
|  - Network: Disconnected (Air-gapped)                              |
|  - Syscall Filter: Seccomp Profile (No ptrace / raw sockets)      |
|  - Read-Only Root Filesystem + Ephemeral /tmp                      |
|                                                                   |
|  +-------------------------------------------------------------+  |
|  | Isolated Code Execution Runtime (Python / Node / Bash)       |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```


## CLI examples



## API examples

The following Python example demonstrates an execution orchestrator for sandboxed Python script execution using Docker/Podman SDK with strict resource bounds, air-gapped network restrictions, and **Pydantic v2** validation of execution inputs and outputs.

```python
import docker
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Pydantic v2 Input/Output Schemas
# ---------------------------------------------------------------------------
class SandboxExecutionRequest(BaseModel):
    code_script: str = Field(..., description="Python script to execute in sandbox")
    timeout_seconds: int = Field(default=5, ge=1, le=30, description="Max allowed execution duration")
    memory_limit_mb: int = Field(default=256, ge=64, le=1024, description="RAM cap in Megabytes")

class SandboxExecutionResult(BaseModel):
    stdout: str = Field(default="", description="Captured standard output")
    stderr: str = Field(default="", description="Captured standard error")
    exit_code: int = Field(..., description="Process exit code (0 for success)")
    is_timeout: bool = Field(default=False, description="Whether process timed out")

# ---------------------------------------------------------------------------
# Sandboxed Runner Implementation
# ---------------------------------------------------------------------------
class PythonSandboxRunner:
    def __init__(self, base_image: str = "python:3.12-slim"):
        self.client = docker.from_env()
        self.base_image = base_image

    def execute_script(self, request_data: Dict[str, Any]) -> SandboxExecutionResult:
        req = SandboxExecutionRequest.model_validate(request_data)

        try:
            container = self.client.containers.run(
                image=self.base_image,
                command=["python", "-c", req.code_script],
                detach=True,
                network_mode="none",  # Air-gapped sandbox
                mem_limit=f"{req.memory_limit_mb}m",
                nano_cpus=1000000000,  # 1 CPU core limit
                cap_drop=["ALL"],      # Drop all Linux capabilities
                read_only=True,        # Read-only root filesystem
                tmpfs={'/tmp': 'size=64M,exec'},
            )

            try:
                result = container.wait(timeout=req.timeout_seconds)
                exit_code = result.get("StatusCode", -1)
                stdout = container.logs(stdout=True, stderr=False).decode("utf-8", errors="replace")
                stderr = container.logs(stdout=False, stderr=True).decode("utf-8", errors="replace")

                return SandboxExecutionResult(
                    stdout=stdout,
                    stderr=stderr,
                    exit_code=exit_code,
                    is_timeout=False
                )
            except Exception as e:
                container.kill()
                return SandboxExecutionResult(
                    stdout="",
                    stderr=f"Execution timed out after {req.timeout_seconds}s: {e}",
                    exit_code=124,
                    is_timeout=True
                )
            finally:
                container.remove(force=True)

        except Exception as err:
            return SandboxExecutionResult(
                stdout="",
                stderr=f"Failed to initialize sandbox container: {err}",
                exit_code=-1,
                is_timeout=False
            )

if __name__ == "__main__":
    runner = PythonSandboxRunner()
    sample_request = {
        "code_script": "import math\nprint(f'Calculated pi: {math.pi}')",
        "timeout_seconds": 3,
        "memory_limit_mb": 128
    }

    print("Executing sandboxed python script...")
    # Requires running Docker daemon; mock output when Docker is inactive
    try:
        res = runner.execute_script(sample_request)
        print(f"Exit code: {res.exit_code}")
        print(f"Stdout: {res.stdout.strip()}")
    except Exception as e:
        print(f"Docker sandbox skipped: {e}")
```


## Related tools / concepts

- **[Docker](../tools/infrastructure/docker.md)**: Container engine providing cgroups, namespace isolation, and ephemeral base images.
- **[Inspect AI](../tools/benchmarking/inspect-ai.md)**: Framework for orchestrating model evaluations using sandboxed execution.
- **[Agency-Agents](../tools/agents/agency-agents.md)**: Agent personas utilizing sandboxed tools for secure multi-step tasks.


## Sources / references

- **[NIST Special Publication 800-190: Application Container Security Guide](https://csrc.nist.gov/publications/detail/sp/800-190/final)**
- **[Docker Container Isolation & Security Best Practices](https://docs.docker.com/engine/security/)**
- **[gVisor Container Sandbox Documentation](https://gvisor.dev/docs/)**
- **[Firecracker MicroVM Architecture](https://firecracker-microvm.github.io/)**



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
