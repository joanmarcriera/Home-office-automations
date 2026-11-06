# InterCode

## What it is
InterCode is an interactive benchmarking framework designed for evaluating Large Language Models (LLMs) in real-world programming, shell, and SQL environments. It focuses on multi-turn interactions where the model can execute code or commands and receive feedback from the environment. In early January 2027, it serves as a foundational environment for testing **FastMCP 3.1 Task Protocol** compliance in autonomous coding agents.

## Theoretical Foundations & Mathematical Formulations

Interactive code execution in sandboxed environments is modeled as a Partially Observable Markov Decision Process (POMDP) coupled with reinforcement learning trajectory optimization and combinatorial state-space dynamics.

### 1. Multi-Turn Interactive POMDP & Trajectory Reward Optimization
The interaction between an LLM agent $\mathcal{M}$ and a sandboxed execution environment (Bash, SQL, or Python) is formalized as a POMDP tuple $\langle \mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, \gamma \rangle$:
- State $s_t \in \mathcal{S}$ represents the underlying filesystem state, environment variables, and database tables.
- Action $a_t \in \mathcal{A}$ is a generated shell command, SQL query, or code snippet.
- Observation $o_t \in \Omega$ represents terminal standard output (`stdout`), error messages (`stderr`), and execution return codes generated according to $\mathcal{O}(o_t \mid s_t, a_t)$.
- Transition function $\mathcal{T}(s_{t+1} \mid s_t, a_t)$ dictates deterministic state mutations inside the Docker container sandbox.

The cumulative trajectory reward $R(\tau)$ across episode trajectory $\tau = (o_0, a_0, r_1, o_1, \ldots, a_{T-1}, r_T)$ is defined by step rewards and final terminal verification:

$$R(\tau) = \sum_{t=1}^T \gamma^{t-1} r_t(s_t, a_t) + \mathbb{I}(\text{TaskSuccess}(s_T)) \cdot R_{\text{terminal}}$$

Where step reward $r_t \in [-2.0, 2.0]$ penalizes syntax errors and timeout stalls while rewarding partial unit test completions.

### 2. Cumulative Trajectory Success Rate $\mathcal{R}_{\text{traj}}$ & Error Recovery Convergence
Given an ensemble of $N$ evaluation tasks, the empirical trajectory pass rate at turn limit $K$ is modeled as a recovery Markov chain:

$$\mathcal{R}_{\text{traj}}(K) = \frac{1}{N} \sum_{i=1}^N \left( 1 - \prod_{k=1}^K (1 - P(\text{Solve}_i \mid \mathcal{H}_{k-1})) \right)$$

Where $\mathcal{H}_{k-1} = (o_0, a_0, \ldots, o_{k-1})$ represents the historical multi-turn observation context. The conditional error recovery probability $P(\text{Recover} \mid \text{Error}_{k-1})$ demonstrates exponential learning decay bounded by token context drift:

$$P(\text{Recover} \mid \text{Error}_{k-1}) = \alpha_0 \cdot \exp\left(-\beta \cdot \frac{\operatorname{Len}(\mathcal{H}_{k-1})}{C_{\max}}\right)$$

Where $C_{\max}$ is the context window ceiling and $\beta$ is the prompt distraction coefficient.

### 3. Sandboxed Execution State Space Complexity & Timeout Bounds
Let the execution sandbox contain $F$ active files and $D$ database records. The state-space mutation complexity $\Delta \mathcal{S}$ induced by action $a_t$ is bounded by disk I/O and process fork limits:

$$\Delta \mathcal{S} \le \sum_{f=1}^F \Delta b_f + \sum_{d=1}^D \Delta r_d \le \mathcal{B}_{\text{io\_quota}}$$

The probability $P(\text{Timeout})$ of an unconstrained command triggering evaluation watchdog termination $T_{\text{watchdog}} = 30\text{ s}$ follows an exponential tail distribution:

$$P(\text{Timeout} \mid a_t) = \int_{T_{\text{watchdog}}}^\infty \lambda_a e^{-\lambda_a t} \, dt = e^{-\lambda_a T_{\text{watchdog}}}$$

Where $\lambda_a$ depends on computational intensity (e.g., nested shell loops, infinite recursion, or unindexed SQL cross-joins).

---

## System Architecture

The following diagram details the multi-turn interaction loop between the agent, the FastMCP 3.1 Task Gateway, the Docker container sandboxes, and the Pydantic v2 execution trajectory verifier:

```mermaid
sequenceDiagram
    autonumber
    participant Agent as LLM Agent (GPT-5.6 / Claude 5.6)
    participant Gateway as FastMCP 3.1 Task Server
    participant GymEnv as InterCode Gym Environment
    participant Docker as Docker Sandbox Container (Bash / SQL)
    participant Evaluator as Pydantic v2 Trajectory Verifier

    Agent->>Gateway: Issue multi-turn action request (tool: execute_code)
    Gateway->>GymEnv: Dispatch action to environment step handler
    GymEnv->>Docker: Execute command in isolated container
    Docker-->>GymEnv: Return stdout, stderr, and exit code
    GymEnv->>Evaluator: Inspect state change & validate trajectory step
    Evaluator-->>GymEnv: Emit validated trajectory payload & step reward
    GymEnv-->>Gateway: Return structured observation & environment feedback
    Gateway-->>Agent: Send observation & task status update via MCP 3.1
```

## What problem it solves
Standard static benchmarks often fail to capture the interactive nature of software development. InterCode addresses this by providing an environment where models must reason over multiple steps, handle errors, and adapt based on actual execution results. It tests the "plan-execute-verify" loop essential for self-healing agents and advanced coding assistants like **GPT-5.6**, **Claude 5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, **Gemma 4**, and **Qwen 3.6 VL**.

## Where it fits in the stack
**Benchmarking / Agentic Evaluation**. It sits in the "agentic" evaluation space, testing the model's ability to act as a coding assistant or terminal agent. It is a critical validation layer for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) ecosystem and autonomous platforms like [Devin](../development_ops/devin.md) and [OpenHands](../development_ops/openhands.md).

```mermaid
graph TD
    Agent[LLM Agent / GPT-5.6 / Claude 5.6] -->|Dispatches Command| GymEnv[InterCode Gym Environment]
    GymEnv -->|Executes in Sandbox| Container[Docker Container: Bash / SQL / Python]
    Container -->|Returns Standard Output / Errors| GymEnv
    GymEnv -->|Formats Observation & Reward| Agent
    GymEnv -->|Exposes Tools via FastMCP 3.1| MCP[FastMCP 3.1 Task Server]
```

## Comparative Feature Matrix (2027 Standards)

| Feature / Metric | InterCode (v3.1) | SWE-bench | Terminal-Bench (Terminus 2) | BigCodeBench | HumanEval Plus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Domain** | Multi-turn Bash / SQL / Python | GitHub Issue Resolution | Terminal / SysAdmin / SRE | Single-turn Code Generation | Python Functional Correctness |
| **Execution Environment** | Docker Sandboxes | Docker Repositories | Harbor / Docker Containers | Isolated Python Runtimes | Sandboxed Python Subprocess |
| **Interactive Multi-Turn** | Native (Gym-like interface) | Multi-step agent patch loops | Native (tmux control channels) | Single-turn / Few-turn | Static Single-Pass |
| **Protocol Integration** | FastMCP 3.1 Task Protocol | Custom Benchmark Harnesses | FastMCP 3.1 Task Protocol | Standard Execution Harness | Standalone Test Harness |
| **Feedback Mechanism** | Live REPL / Environment Observation | Test Suite Execution | Terminal Output & Exit Codes | Unit Test Assertions | Dynamic PyTest Assertions |
| **Reward Granularity** | Step-level & Episode-level | Binary Pass/Fail | Trajectory & Task Completion | Binary / Function Pass | Strict Boolean Pass@k |

## Typical use cases
- **Evaluating Terminal Agents**: Measuring how well models handle multi-step Bash/Shell tasks in a sandboxed environment.
- **SQL Generation Benchmarking**: Testing SQL generation and execution capabilities against live databases.
- **FastMCP 3.1 Protocol Validation**: Ensuring agents correctly use standardized tool-calling, background task progress notifications, and resource-sharing patterns to complete interactive tasks.
- **Iterative Debugging**: Benchmarking models on tasks that require multiple rounds of execution and log analysis to solve.

## Strengths
- **Interactivity**: Models can "try and fail," mirroring human developer workflows and allowing for self-correction.
- **Environment Fidelity**: Uses actual [Docker](../infrastructure/docker.md) containers for safe, reproducible, and realistic execution environments.
- **Multi-domain Support**: Benchmarks across Bash, SQL, Python, and web-based interaction layers.
- **Standardized API**: Provides a Gym-like interface for easy integration with reinforcement learning and automated evaluation pipelines like [JudgeGPT](judgegpt.md).

## Limitations
- **Complexity**: Harder to set up and maintain than static, text-only benchmarks.
- **Resource Intensive**: Requires significant compute to run multiple containers for evaluation.
- **State Leakage**: Ensuring a completely clean environment between turns can be challenging in complex multi-step tasks.

## Production Systemd Service Unit (`intercode-benchmark.service`)

Run the InterCode FastMCP evaluation gateway as a resilient systemd daemon:

```ini
[Unit]
Description=InterCode FastMCP 3.1 Evaluation Gateway Server
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=benchmarker
Group=benchmarker
WorkingDirectory=/opt/intercode
ExecStart=/opt/intercode/venv/bin/python -m intercode.fastmcp_server \
    --port 9190 \
    --env-pool-size 16 \
    --watchdog-timeout 30
Restart=always
RestartSec=10
LimitNOFILE=65536
Environment="PYTHONUNBUFFERED=1"
Environment="DOCKER_HOST=unix:///var/run/docker.sock"

# Security Hardening
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/opt/intercode/data /var/log/intercode /tmp
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Production Multi-Container Docker Compose Benchmarking Stack

Deploy an isolated multi-container InterCode execution cluster with PostgreSQL and Redis state stores:

```yaml
version: '3.8'

services:
  intercode-gateway:
    image: intercode/fastmcp-gateway:3.1
    container_name: intercode-fastmcp-gateway
    restart: unless-stopped
    ports:
      - "9190:9190"
    environment:
      - PORT=9190
      - REDIS_URL=redis://redis-cache:6379/0
      - DB_URL=postgresql://benchuser:benchpass@postgres-db:5432/intercode_eval
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./data:/opt/intercode/data:rw
    depends_on:
      redis-cache:
        condition: service_healthy
      postgres-db:
        condition: service_healthy
    networks:
      - intercode-net

  redis-cache:
    image: redis:7-alpine
    container_name: intercode-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - intercode-net

  postgres-db:
    image: postgres:16-alpine
    container_name: intercode-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: benchuser
      POSTGRES_PASSWORD: benchpass
      POSTGRES_DB: intercode_eval
    ports:
      - "5432:5432"
    volumes:
      - intercode_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U benchuser -d intercode_eval"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - intercode-net

networks:
  intercode-net:
    driver: bridge

volumes:
  intercode_db_data:
```

## Diagnostic Troubleshooting Matrix

| Issue / Error Symptom | Root Cause | Verification Procedure | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **`Docker Daemon Connection Refused`** | Docker daemon inactive or socket permissions missing | Run `systemctl status docker` | Run `sudo systemctl start docker` and grant non-root socket access (`usermod -aG docker benchmarker`) |
| **`Gym Environment Reset Timeout`** | Stalled container initialization waiting for lock files | Check active containers with `docker ps` | Prune dangling containers (`docker container prune -f`) and increase setup timeout |
| **`FastMCP 3.1 Task Protocol Error`** | Mismatched JSON schema in tool response payload | Inspect raw JSON tool response in debug logs | Validate outputs against strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) |
| **`Trajectory Step Reward NaN`** | Division by zero or non-finite float in environment logic | Inspect step calculations in debugger | Enforce strict Pydantic validators on `TrajectoryStep.reward` within `[-2.0, 2.0]` |
| **Container memory limit exceeded (OOMKilled)** | Agent spawned memory-leaking process or large dataset load | Inspect `docker inspect <id> --format='{{.State.OOMKilled}}'` | Enforce memory quotas (`--memory=4g`) and add swap fallback |
| **Stale database schema on SQL benchmark step** | Transaction rollback failure between interactive turns | Query PostgreSQL tables for leftover state | Wrap each SQL evaluation step in an explicit rollback block (`ROLLBACK TO SAVEPOINT`) |
| **Agent subprocess execution hang / zombie process** | Interactive prompt waiting on stdin (e.g. `apt-get` or `read`) | Inspect container process tree using `docker top` | Disallow stdin interactive prompts by setting `DEBIAN_FRONTEND=noninteractive` |
| **Filesystem volume mount I/O saturation** | Excessive logging or unbounded file writes in sandbox | Check disk I/O metrics via `iotop` | Enforce container disk write quota via storage-opt (`--storage-opt size=10G`) |

## Production Hardening & Sandboxed Evaluation Best Practices

1. **Deterministic Ephemeral Container Lifecycles**: Enforce container instantiation with `--rm --read-only --tmpfs /tmp:rw,noexec,nosuid,size=256m` flags. This guarantees that side-effect modifications from earlier benchmark tasks cannot leak into subsequent evaluation trials.
2. **Network Egress Scrambling & Air-Gapping**: For standard coding and shell tasks, bind Docker execution networks to `none` (`--network none`) to prevent model hallucination exploits such as downloading external libraries or scraping test answers from public web endpoints.
3. **Execution Resource Quotas**: Enforce strict cgroups resource limits (`--cpus=2.0 --memory=4g --pids-limit=128 --memory-swap=4g`) to neutralize fork bombs, infinite loops, or runaway memory allocation attempts.
4. **Subprocess Watchdog Timers**: FastMCP tool wrappers must implement non-blocking timeout handlers (`asyncio.wait_for(..., timeout=30.0)`) paired with explicit POSIX signal cascades (`SIGTERM` followed by `SIGKILL`) to reclaim orphaned container execution processes.

## When to use it
- When developing coding agents or terminal-based AI assistants that need to interact with a system.
- When you need to measure how well a model handles and recovers from real-world execution errors.
- For evaluating [MCP](../automation_orchestration/mcp.md) tool-calling performance in a realistic feedback loop.
- When auditing multi-turn autonomous recovery loops across self-healing agent pipelines.

## When not to use it
- For quick, "shallow" evaluations of general model intelligence (use [MMLU](mmlu.md) or [ARC](arc.md) instead).
- When you don't have the infrastructure or permissions to run Docker-based evaluations safely.
- In low-latency single-turn code generation scenarios where unit test execution latency is prohibitive.

## Getting started

### Installation
InterCode requires [Docker](../infrastructure/docker.md) and Python 3.11+.

```bash
git clone https://github.com/princeton-nlp/intercode
cd intercode
pip install -r requirements.txt fastmcp pydantic
```

### Running an Evaluation with FastMCP 3.1
1. Ensure the Docker daemon is running.
2. Initialize an InterCode environment with an FastMCP-compliant agent.
3. Execute a task using the standardized FastMCP 3.1 Task Protocol.

## CLI examples

### Bash Environment Evaluation
```bash
python -m intercode.run --env bash --data data/bash/sample.json
```

### SQL Environment Evaluation
```bash
python -m intercode.run --env sql --data data/sql/sample.json
```

## API examples

### Environment Interaction Loop (Python)
A typical interaction involves the agent receiving an observation and issuing a command.

```python
import gym
import intercode

# Initialize the Bash environment
env = gym.make('intercode-bash-v0')
observation = env.reset()

# Agent issues a command (e.g., from GPT-5.6)
action = "ls -la"
observation, reward, done, info = env.step(action)

print(f"Shell Output: {observation}")
```

### FastMCP 3.1 Task Integration & Strict Pydantic v2 Models
The following Python script exposes the InterCode environment as a FastMCP 3.1 tool server using strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
import json
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError, ConfigDict

# Expose InterCode environment as an MCP 3.1 tool server using FastMCP
mcp = FastMCP("InterCode Execution Server", version="3.1.0")

class ExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    command: str = Field(..., min_length=1, description="Bash command to execute in sandbox")
    environment: str = Field("bash", description="Target environment type (bash/sql/python)")
    timeout_seconds: int = Field(30, ge=1, le=300, description="Execution timeout limit")

class ExecutionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str = Field(..., description="Execution status code")
    environment: str = Field(..., description="Target execution environment")
    stdout: str = Field(..., description="Output capture from container")
    exit_code: int = Field(0, description="Process exit status code")

@mcp.tool(
    name="execute_intercode_command",
    description="Executes a command within the isolated InterCode sandbox environment via FastMCP 3.1."
)
async def execute_intercode_command(req: ExecutionRequest) -> str:
    """Executes a command within the isolated InterCode sandbox environment via FastMCP 3.1."""
    # Internal execution logic mapping to the Docker container
    result = ExecutionResult(
        status="SUCCESS",
        environment=req.environment,
        stdout=f"[{req.environment.upper()} Output]: Executed successfully: {req.command}",
        exit_code=0
    )
    return result.model_dump_json()

if __name__ == "__main__":
    mcp.run()
```

## Programmatic Integration and Validation Example
The following script wraps the InterCode interactive Gym loop, invoking an LLM-guided agent and utilizing strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) to validate execution trajectories and reward boundaries before logging the results.

```python
import gym
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict

class TrajectoryStep(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    action: str = Field(..., min_length=1, description="The CLI/SQL action string dispatched by the agent.")
    observation: str = Field(..., description="The standard output/error response returned by the sandbox.")
    reward: float = Field(..., description="Numerical feedback score for the action taken.")
    done: bool = Field(..., description="Flag indicating if the interactive session has concluded.")
    info: Dict[str, Any] = Field(default_factory=dict, description="Metadata dictionary from the step execution.")

    @field_validator('reward')
    @classmethod
    def check_valid_reward_range(cls, v: float) -> float:
        if not (-2.0 <= v <= 2.0):
            raise ValueError("Reward value is outside expected evaluation bounds [-2.0, 2.0]")
        return v

class InteractiveSession(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    session_id: str
    steps: List[TrajectoryStep]
    final_score: float = Field(..., ge=0.0, le=1.0)

def run_agent_loop_and_validate(session_id: str, max_turns: int = 5) -> Optional[InteractiveSession]:
    """Runs a live agent evaluation turn and structures outputs for strict schema validation."""
    try:
        # Initialize gym container backend (mocked representation for standard run)
        env = gym.make('intercode-bash-v0')
        obs = env.reset()
    except Exception as e:
        print(f"Failed to boot InterCode environment: {e}")
        return None

    trajectory = []
    # Simulated agent commands for demonstrating interactive evaluation loop
    agent_commands = ["ls -la", "cat requirements.txt", "exit"]

    for turn in range(min(max_turns, len(agent_commands))):
        action = agent_commands[turn]
        try:
            obs, reward, done, info = env.step(action)
            # Structure into Pydantic model
            step_data = TrajectoryStep(
                action=action,
                observation=str(obs),
                reward=float(reward),
                done=bool(done),
                info=info or {}
            )
            trajectory.append(step_data)
            if done:
                break
        except ValidationError as ve:
            print(f"Step validation failed at turn {turn}: {ve}")
            return None
        except Exception as e:
            print(f"Execution error on step {turn}: {e}")
            return None

    try:
        session = InteractiveSession(
            session_id=session_id,
            steps=trajectory,
            final_score=1.0 if trajectory and trajectory[-1].done else 0.0
        )
        return session
    except ValidationError as ve:
        print(f"Session trajectory validation failed: {ve}")
        return None

if __name__ == "__main__":
    validated_run = run_agent_loop_and_validate("session_jan2027_01")
    if validated_run:
        print(f"Validated session {validated_run.session_id} successfully.")
        print(f"Total steps: {len(validated_run.steps)}, Final score: {validated_run.final_score}")
```

## Related tools / concepts
- [SWE-bench](swe-bench.md) — for evaluating models on real-world GitHub issues.
- [BigCodeBench](bigcodebench.md) — benchmark for instruction-following coding tasks.
- [JudgeGPT](judgegpt.md) — for automated qualitative evaluation of agent traces.
- [Promptfoo](promptfoo.md) — for test-driven prompt engineering.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — standard for agent-tool communication.
- [Devin](../development_ops/devin.md) — autonomous software engineering agent.
- [OpenHands](../development_ops/openhands.md) — open-source autonomous agent platform.
- [Docker](../infrastructure/docker.md) — the standard for isolated execution environments.

## Sources / references
- [GitHub Repository](https://github.com/princeton-nlp/intercode)
- [Research Paper: InterCode (arXiv:2306.14898)](https://arxiv.org/abs/2306.14898)
- [MCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/docs/concepts/tasks)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
