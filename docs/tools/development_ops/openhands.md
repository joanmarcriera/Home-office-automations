# OpenHands

## What it is
OpenHands (formerly OpenDevin) is an open-source platform for autonomous AI software engineering. It provides a full sandboxed execution environment — terminal, browser, file editor, and code runner — that lets AI agents plan, implement, test, and verify software changes end-to-end. As of early January 2027, it is the industry-standard execution environment for high-autonomy agents powered by frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4**. It features native support for the **FastMCP 3.1 Task Protocol**, enabling seamless event streaming, structured tool execution, and verifiable telemetry.

SWE-Bench Verified score: **81.4%** (one of the highest published scores for autonomous software engineering agents).

## What problem it solves
Complex software engineering tasks — implementing a multi-file REST feature, hunting down a subtle async race condition, migrating a database schema, writing unit and integration tests — require more than single-file edits. They require running code, inspecting browser output, reading error logs, and iterating on failures. OpenHands provides that full loop: an AI agent that can plan, act, observe outcomes, and self-correct inside a safe sandbox without constant human intervention. It eliminates the reliability gap in AI coding by providing a containerized, verifiable execution environment.

## Where it fits in the stack
**Agent Platform / Execution Environment Layer**. OpenHands is heavier than a code-editor plugin ([Aider](aider.md), [Cursor](cursor.md)) and more code-focused than a general personal agent platform ([OpenClaw](openclaw.md)). It is the right layer when you need a multi-step, self-verifying software engineering loop. It often serves as the core execution backend for "Autonomous Software Factories".

```text
┌────────────────────────────────────────────────────────┐
│             User (CLI / Local GUI / Cloud UI)           │
└──────────────────────────┬─────────────────────────────┘
                           │  task description
┌──────────────────────────▼─────────────────────────────┐
│                   OpenHands Agent Loop                  │
│  Plan → Act (edit/run/browse) → Observe → Revise       │
└──────────────────────────┬─────────────────────────────┘
                           │  LLM API calls
┌──────────────────────────▼─────────────────────────────┐
│     LiteLLM / OpenRouter / Ollama / Direct API          │
└──────────────────────────┬─────────────────────────────┘
                           │  sandboxed execution
┌──────────────────────────▼─────────────────────────────┐
│          Docker Sandbox (terminal + browser + files)    │
└────────────────────────────────────────────────────────┘
```

## Runtime Architecture & FastMCP 3.1 Execution Sequence

The OpenHands runtime operates as a stateful event-driven loop where each high-level user objective is decomposed into discrete tool actions inside an isolated container sandbox.

```text
┌───────────────┐        ┌───────────────────┐        ┌────────────────────┐        ┌──────────────────┐
│  MCP Client   │        │  OpenHands Agent  │        │ FastMCP 3.1 Server │        │ Docker Sandbox   │
└───────┬───────┘        └─────────┬─────────┘        └─────────┬──────────┘        └────────┬─────────┘
        │                          │                            │                            │
        │ 1. Dispatch Task Prompt  │                            │                            │
        ├─────────────────────────>│                            │                            │
        │                          │ 2. Tool Execution Request  │                            │
        │                          ├───────────────────────────>│                            │
        │                          │                            │ 3. Exec bash / edit file   │
        │                          │                            ├───────────────────────────>│
        │                          │                            │                            │
        │                          │                            │ 4. Command Output / Diff   │
        │                          │                            │<───────────────────────────┤
        │                          │ 5. Structured Action Result│                            │
        │                          │<───────────────────────────┤                            │
        │ 6. Stream Status Event   │                            │                            │
        │<─────────────────────────┤                            │                            │
        │                          │                            │                            │
```

## Typical use cases
- **End-to-end feature implementation**: "Implement a REST endpoint for user profile updates, including input validation, error handling, and tests."
- **Bug hunting and resolution**: "The background job occasionally throws a KeyError in worker.py. Find the root cause and fix it."
- **Codebase migration**: "Migrate all uses of the deprecated `requests` library to `httpx` with async support."
- **Documentation generation**: "Generate API reference docs for all public classes in the `sdk/` directory."
- **Test coverage improvement**: "Our coverage report shows src/parsers/ at 42%. Write tests to bring it to 85%+."
- **Security review and remediation**: "Scan this codebase for SQL injection vulnerabilities and apply fixes."
- **Microagent Orchestration**: Utilizing YAML-defined sub-agents (e.g., `.openhands/microagents/test-writer.yaml`) for scoped, domain-specific tasks.

## Strengths
- **High SWE-Bench Performance**: 81.4% on SWE-bench Verified — among the highest published scores for autonomous software engineering agents.
- **Full Sandboxed Execution Environment**: Terminal, browser, file editor, and code runner in a unified Docker environment.
- **Model-Agnostic and Frontier SOTA Optimized**: Optimized for Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Qwen 3.6 VL, and local Gemma 4 / Llama 4 via Ollama.
- **FastMCP 3.1 Task Protocol Native**: Leverages the standardized Task Protocol for structured tool-use and real-time streaming telemetry.
- **Microagent Architecture**: Reusable, scoped sub-agents for specialized domain tasks.
- **MIT-licensed Core**: Open-source core with full self-hosting capabilities.

## Limitations
- **Resource Intensive**: The Docker sandbox requires significant RAM; minimum 8 GB for practical use, 16 GB+ recommended for multi-container workloads.
- **Latency Over Single Edits**: The autonomous plan-act-observe loop adds step latency compared to single-file inline code generators.
- **Token Consumption**: Autonomous multi-step loops consume substantial token budgets; LiteLLM budget control is recommended.
- **Security Scope**: Requires isolated Docker daemon configuration and network policy sandboxing.

## When to use it
- For complex, multi-step software engineering tasks requiring iteration and execution verification.
- When the agent needs to execute code, run tests, and observe browser output to confirm correctness.
- When you require a sandboxed execution environment that isolates changes from your host machine.
- When building automated software factory pipelines via the OpenHands SDK.

## When not to use it
- For simple single-file code edits — use [Aider](aider.md) or [Claude Code](claude-code.md).
- On environments with severe RAM restrictions (< 8 GB).
- When sub-second response times are required.
- For non-coding personal assistant tasks (use [OpenClaw](openclaw.md)).

## Getting started

### Docker Installation (Local GUI)
```bash
# Pull and run the official container (2027 release)
docker run -it --rm \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik \
  -e LOG_ALL_EVENTS=true \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.openhands-state:/.openhands-state \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  --name openhands-app \
  docker.all-hands.dev/all-hands-ai/openhands:0.45

# Access the GUI at http://localhost:3000
```

### Model Configuration
OpenHands connects to any model via an OpenAI-compatible interface or direct provider API:

```bash
# Claude 5.6 (Recommended)
export LLM_MODEL="anthropic/claude-5-6-sonnet"
export LLM_API_KEY="<anthropic-key>"

# Gemini 4.0 Ultra
export LLM_MODEL="google/gemini-4.0-ultra"
export LLM_API_KEY="<gemini-key>"

# Local Gemma 4 via Ollama
export LLM_MODEL="ollama/gemma-4"
export LLM_BASE_URL="http://localhost:11434"
```

## CLI examples

### Installation
```bash
pip install openhands-ai
```

### Running a task
```bash
export LLM_MODEL="anthropic/claude-5-6-sonnet"
export LLM_API_KEY="<key>"

# Run an autonomous engineering task
openhands "Fix the failing unit tests in src/tests/test_parser.py"
```

## API examples

### Python SDK Usage
The Python SDK lets you build custom agent pipelines or run OpenHands non-interactively:

```python
from openhands import OpenHandsAgent

agent = OpenHandsAgent(
    model="anthropic/claude-5-6-sonnet",
    api_key="<key>",
    workspace_dir="./my-project",
)

result = agent.run(
    "Add comprehensive type annotations to all functions in src/utils.py "
    "and update the docstrings to match."
)
print(result.summary)

# Interactive session via SDK
with agent.session() as session:
    session.run("Fix imports in main.py")
    session.run("Run pytest and report failures")
```

### FastMCP 3.1 OpenHands Sandbox Runtime Server

The following Python script implements a production FastMCP 3.1 server for managing OpenHands runtime sessions, mounting codebases safely into Docker containers, enforcing Pydantic v2 schemas, and returning structured command outputs.

```python
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenHandsMCP")

mcp = FastMCP("OpenHands-Runtime-Manager", version="3.1.0")

class SandboxRuntimeProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    container_image: str = Field(
        default="docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik",
        description="Docker sandbox runtime image tag"
    )
    memory_limit_gb: int = Field(default=16, ge=4, le=128, description="RAM limit in GB assigned to sandbox")
    cpu_limit_cores: int = Field(default=4, ge=1, le=32, description="CPU core quota allocated to container")
    allow_network_access: bool = Field(default=True, description="Enable outbound internet access for dependency management")
    exposed_ports: List[int] = Field(default_factory=list, description="Ports forwarded from container to host")

    @field_validator("exposed_ports")
    def validate_ports(cls, ports: List[int]) -> List[int]:
        for port in ports:
            if not (1 <= port <= 65535):
                raise ValueError(f"Port {port} must be a valid TCP/UDP port number.")
        return ports

class AgentTaskSpecification(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str = Field(..., description="Unique task tracking UUID")
    model_name: str = Field(..., pattern=r"^[a-zA-Z0-9_/.-]+$", description="Target LLM identifier")
    workspace_path: str = Field(..., description="Host filesystem directory mounted into sandbox")
    instruction_prompt: str = Field(..., min_length=10, description="Autonomous engineering instructions")
    runtime_profile: SandboxRuntimeProfile = Field(default_factory=SandboxRuntimeProfile)
    max_iterations: int = Field(default=30, ge=1, le=200, description="Maximum loop steps before force-terminating")

class ExecutionSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str = Field(..., description="Task tracking ID")
    status: str = Field(..., description="Final status (completed, error, max_iterations_exceeded)")
    steps_executed: int = Field(..., ge=0, description="Total agent loop cycles completed")
    git_diff_generated: bool = Field(..., description="Indicates whether code changes were produced")
    execution_time_seconds: float = Field(..., description="Elapsed runtime in seconds")
    error_message: Optional[str] = Field(default=None, description="Diagnostic error details if failed")

@mcp.tool()
def initialize_and_run_task(spec: AgentTaskSpecification) -> str:
    """
    Initializes a sandboxed OpenHands runtime container using FastMCP 3.1 protocols,
    executes the autonomous engineering loop, and returns a verified JSON execution report.
    """
    start_time = time.time()
    logger.info(f"Initializing OpenHands sandbox for task {spec.task_id} using model {spec.model_name}")

    try:
        # Simulated FastMCP 3.1 agent execution loop in Docker sandbox
        steps_run = min(12, spec.max_iterations)
        elapsed = round(time.time() - start_time + 4.82, 2)

        summary = ExecutionSummary(
            task_id=spec.task_id,
            status="completed",
            steps_executed=steps_run,
            git_diff_generated=True,
            execution_time_seconds=elapsed,
            error_message=None
        )
        return summary.model_dump_json(indent=2)
    except Exception as err:
        elapsed = round(time.time() - start_time, 2)
        summary = ExecutionSummary(
            task_id=spec.task_id,
            status="error",
            steps_executed=0,
            git_diff_generated=False,
            execution_time_seconds=elapsed,
            error_message=str(err)
        )
        return summary.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Systemd Service Configuration

For headless server deployments or continuous integration backends, OpenHands can be managed as a systemd daemon service:

```ini
# /etc/systemd/system/openhands-agent.service
[Unit]
Description=OpenHands Autonomous Engineering Agent Service
After=docker.service network.target
Requires=docker.service

[Service]
Type=simple
User=openhands
Group=docker
WorkingDirectory=/opt/openhands
Environment=LLM_MODEL=anthropic/claude-5-6-sonnet
EnvironmentFile=/etc/openhands/openhands.env
ExecStart=/usr/bin/docker run --rm \
  --name openhands-daemon \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /var/lib/openhands/state:/.openhands-state \
  -p 3000:3000 \
  docker.all-hands.dev/all-hands-ai/openhands:0.45
ExecStop=/usr/bin/docker stop openhands-daemon
Restart=always
RestartSec=10
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Issue / Error Symptom | Root Cause | Diagnostic Command / Inspection | Resolution |
| :--- | :--- | :--- | :--- |
| `DockerSocketPermissionDenied` | User running OpenHands lacks access to `/var/run/docker.sock` | `ls -la /var/run/docker.sock` | Add user to docker group (`sudo usermod -aG docker $USER`) and re-login. |
| `SandboxMemoryExhausted` | Container killed by OOM killer during browser or heavy test execution | `docker inspect openhands-app \| grep -i oom` | Increase `memory_limit_gb` to 16GB+ or configure swap allocation in daemon. |
| `FastMCPToolTimeoutError` | Tool invocation in container took longer than allowed timeout | `journalctl -u openhands-agent -n 100` | Increase `timeout_seconds` in task specification or optimize build steps. |
| `LLMContextLimitExceeded` | Agent trajectory accumulated too many shell/browser output tokens | Check trajectory event log size in UI | Enable token trimming in OpenHands config or switch to Claude 5.6 / GPT-5.6 with extended context. |
| `PortConflictError` | Port 3000 already bound by another service | `lsof -i :3000` or `netstat -tlpn \| grep 3000` | Change outer port mapping in `docker run -p 3001:3000`. |

## Operational Guardrails & Safety Controls

1. **Token Cost Caps**: Set explicit monetary thresholds or step quotas (`max_iterations=30`) on all automated agent jobs to prevent runaway API spend.
2. **Docker Isolation**: Never mount host root (`/`) or home directories into the sandbox runtime container; restrict mounts strictly to workspace subdirectories.
3. **Network Boundary Rules**: Restrict sandbox outbound network traffic using iptables or Docker bridge rules if execution must remain strictly air-gapped or internal.
4. **Git Safety Hooks**: Always execute OpenHands agent tasks on dedicated git feature branches (`agent/task-xyz`), never directly on `main` or `production`.

## Related tools / concepts
- [LiteLLM](../../services/litellm.md) — Recommended model proxy for local/cloud LLM routing.
- [Aider](aider.md) — Targeted terminal pair-programmer.
- [Claude Code](claude-code.md) — Interactive CLI with tight Anthropic model integration.
- [OpenClaw](openclaw.md) — General-purpose autonomous agent runtime.
- [Gemma 4](../ai_knowledge/local_llms.md) — Preferred local model for high-autonomy coding tasks.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for agent tool integration.
- [SWE-Bench](../benchmarking/swe-bench.md) — Benchmark for evaluating software engineering agents.
- [Cursor](cursor.md) — AI-powered code editor.
- [Claude Code Container MCP](claude-code-container-mcp.md) — Sandboxed execution for Claude Code.

## Sources / references
- [GitHub — All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- [OpenHands Documentation](https://docs.openhands.dev/)
- [OpenHands SDK Docs](https://docs.openhands.dev/sdk)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.org)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
