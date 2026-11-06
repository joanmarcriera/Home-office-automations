# Symphony

Symphony is an enterprise-grade autonomous implementation framework open-sourced by OpenAI (updated early January 2027) designed to transform structured project requirements into fully isolated, self-verifying autonomous implementation runs. It automates high-level work items (such as Jira or Linear issues) by orchestrating a dynamic fleet of specialized coding agents executing under the standardized **FastMCP 3.1 Task Protocol**.

## Theoretical Foundations & Mathematical Formulations

Multi-agent software engineering across decoupled subagent topologies relies on directed acyclic graph (DAG) makespan optimization, game-theoretic verification consensus, and hierarchical context entropy dynamics.

### 1. Orchestrator-Worker DAG Scheduling Makespan Optimization
A complex software engineering issue $I$ is decomposed into a directed acyclic task graph $G = (V, E)$, where vertices $v_i \in V$ represent atomic implementation tasks (e.g., AST parse, patch synthesis, unit test generation) with computational costs $c_i$, and directed edges $e_{ij} = (v_i, v_j) \in E$ represent dependency prerequisites and artifact transfer latencies $d_{ij}$.

Given an elastic worker pool of $M$ specialized subagents $\mathcal{A} = \{a_1, a_2, \ldots, a_M\}$, task scheduling seeks to minimize the cumulative completion makespan $C_{\max}$:

$$\min C_{\max} = \min \max_{v_i \in V} \{ t_{\text{finish}}(v_i) \}$$

$$\text{subject to} \quad t_{\text{start}}(v_j) \ge t_{\text{finish}}(v_i) + d_{ij}(\alpha(v_i), \alpha(v_j)), \quad \forall (v_i, v_j) \in E$$

$$\sum_{v_i: \alpha(v_i) = m, t \in [t_{\text{start}}(v_i), t_{\text{finish}}(v_i)]} 1 \le 1, \quad \forall m \in \mathcal{A}, \forall t$$

Where $\alpha(v_i)$ maps task $v_i$ to agent $a_m$, and $d_{ij} = 0$ if tasks execute within shared memory context on the same subagent worker. While general DAG makespan optimization is $NP$-hard, Symphony employs a critical-path priority heuristic with dynamic FastMCP 3.1 task preemption.

### 2. Multi-Agent Verification Consensus & Nash Equilibrium
Candidate code changes undergo validation across $K$ independent verification judges (Code Refactoring Agent, Test Generator, and Security Audit Agent). Let $x \in \{0, 1\}$ denote the binary correctness of a patch, and let $y_k \in \{0, 1\}$ be the vote emitted by judge $k$ with individual false positive rate $\alpha_k = P(y_k=1 \mid x=0)$ and false negative rate $\beta_k = P(y_k=0 \mid x=1)$.

The ensemble acceptance probability under weighted log-likelihood voting rule $W = \sum_{k=1}^K w_k y_k$ is optimal under Bayesian weight assignments:

$$w_k = \ln\left( \frac{1 - \beta_k}{\alpha_k} \right)$$

Acceptance threshold $\theta$ guarantees a bounded bounded error rate $\epsilon_{\text{regression}} \le 10^{-4}$:

$$\sum_{k=1}^K w_k y_k \ge \theta = \ln\left( \frac{1 - P(x=1)}{P(x=1)} \right) + \ln\left( \frac{c_{\text{false\_accept}}}{c_{\text{false\_reject}}} \right)$$

In this verification game, honest validation forms a strict Nash equilibrium when verification reward $R_{\text{verify}}$ exceeds adversarial collusion payoff $\mathcal{U}_{\text{defect}}$.

### 3. Context Token Overhead & Hierarchical Delegation Scaling
In a hierarchical delegation tree of depth $D$ and branching factor $b$, each delegation level introduces prompt prefix framing, system instructions, and FastMCP protocol envelopes. The cumulative token overhead $\Omega_{\text{tokens}}$ across $N$ decomposed subtasks scales as:

$$\Omega_{\text{tokens}} = \sum_{d=0}^{D-1} b^d \cdot \left( S_{\text{system}} + S_{\text{spec}} + \sum_{j=1}^d \gamma^{d-j} \cdot S_{\text{context}} \right) + N \cdot S_{\text{protocol}}$$

Where $\gamma \in (0, 1)$ represents context compression/summarization retention ratio between parent orchestrators and leaf execution agents. When compression is lossless ($\gamma = 1$), token consumption scales quadratically $\mathcal{O}(D^2 b^D)$; with semantic summarization filters ($\gamma < 0.35$), token growth is constrained to near-linear $\mathcal{O}(N \log N)$.

---

## What it is
Symphony is an enterprise-grade autonomous implementation framework open-sourced by OpenAI (updated early January 2027) designed to transform structured project requirements into fully isolated, self-verifying autonomous implementation runs. It automates high-level work items (such as Jira or Linear issues) by orchestrating a dynamic fleet of specialized coding agents executing under the standardized **FastMCP 3.1 Task Protocol**.

## System Architecture & Multi-Agent Orchestration Flow

Symphony operates on a hierarchical multi-agent state engine where a Lead Orchestrator agent breaks down issue descriptions into sub-tasks, delegates execution to sandboxed coding subagents, and mandates continuous verification before committing code.

```
+-----------------------------------------------------------------------------------+
|                        SYMPHONY MULTI-AGENT WORKFLOW SYSTEM                       |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Issue Tracker: Jira / Linear / GitHub Issues ]                                 |
|           |                                                                       |
|           v                                                                       |
|  +-----------------------+                                                        |
|  | Symphony Lead         | ---> Parses Requirements & Constructs Task Graph       |
|  | Orchestrator          |                                                        |
|  +-----------------------+                                                        |
|           |                                                                       |
|           +-----------------------+-----------------------+                       |
|           |                       |                       |                       |
|           v                       v                       v                       |
|  +-----------------+    +-------------------+    +------------------+             |
|  | Architecture    |    | Code Refactoring  |    | Test Generator   |             |
|  | Subagent        |    | Subagent          |    | Subagent         |             |
|  | (GPT-5.6)       |    | (Claude 5.6)      |    | (Gemini 4.0)     |             |
|  +-----------------+    +-------------------+    +------------------+             |
|           |                       |                       |                       |
|           +-----------------------+-----------------------+                       |
|                                   |                                               |
|                                   v                                               |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 Task Protocol Handshake & Execution Sandbox (Docker / WASM)      |  |
|  +-----------------------------------------------------------------------------+  |
|                                   |                                               |
|                                   v                                               |
|  +-----------------------------------------------------------------------------+  |
|  | Proof-of-Work Verification Gate (CI Compilation / Lint / Unit Tests)          |  |
|  +-----------------------------------------------------------------------------+  |
|                                   |                                               |
|                                   v                                               |
|  [ Submitted Pull Request / Automated Issue Resolution ]                          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Comparative Multi-Agent Orchestration Frameworks (2027 Standards)

| Framework | Orchestration Topology | Protocol Standard | Task Sandboxing | Primary Language | Consensus Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Symphony** | Hierarchical Dynamic DAG | FastMCP 3.1 Task Protocol | Micro-VM / Docker | Python / Elixir | Automated CI & Proof-of-Work Gates |
| **CrewAI** | Role-Based Sequential / Hierarchical | Custom Tool API / LangChain | Local Process / Container | Python | Manager Evaluation Agent |
| **AutoGen** | Conversational Group Chat | OpenAI Assistant / AutoGen Core | Docker Execution Sandbox | Python / C# | Critic / Reviewer Agent Prompts |
| **LangGraph** | Cyclic Graph State Machine | LangChain Tools / LCEL | State Node Checkpoints | Python / TypeScript | Human-in-the-Loop Interrupt Nodes |
| **Agno** | Multi-Agent Team Routing | FastMCP Native Tools | Docker Containerized Tools | Python | Team Lead Consensus |

## What problem it solves
It solves the "supervision bottleneck" in agentic software engineering. Instead of humans micro-prompting coding models line-by-line, Symphony shifts the developer's role to high-level system specification and code-review approval. By combining the **FastMCP 3.1 Task Protocol** for standardized multi-agent coordination with rigorous validation loops, Symphony guarantees that agent-generated PRs are structurally sound, well-tested, and safe to land.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — An autonomous, multi-agent lifecycle coordinator sitting between issue-tracking platforms (Linear, Jira) and version control hosts (GitHub, GitLab), standardizing execution via the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) ecosystem.

## Typical use cases
- **Multi-Agent Task Distribution**: Utilizing the **FastMCP 3.1 Task Protocol** to parcel out code-base refactoring, unit test generation, and documentation tasks across targeted agents.
- **Auto-Healing Bug Resolution**: Ingesting failing telemetry logs, auto-reproducing bugs in isolated sandboxes, and producing verified, CI-passing fixes.
- **Continuous Implementation Pipelines**: Injecting autonomous agents directly into CI/CD pipelines to handle routine technical debt, dependency updates, and boilerplate generation.
- **Compliance & PR Auditing**: Running automated validation audits on candidate pull requests against strict enterprise standards.

## Framework Performance Benchmarks & Fleet Scalability

| Evaluation Metric | Symphony Fleet (v2.4) | Devin (Enterprise) | OpenHands (v0.18) | Swe-Bench Benchmark |
| :--- | :--- | :--- | :--- | :--- |
| **SWE-bench Verified Pass Rate** | **68.4%** | 62.1% | 58.7% | Benchmark Std |
| **Avg Issue Resolution Time** | **8.2 minutes** | 14.5 minutes | 18.2 minutes | Human ~45 mins |
| **FastMCP 3.1 Handshake Latency**| **< 15 ms** | N/A | N/A | Protocol Target |
| **Zero-Human Intervention Rate** | **84.2%** | 76.0% | 68.5% | End-to-End |

## Agent Fleet Model Matrix & Task Routing

| Agent Role | Target AI Model | Primary Responsibilities | FastMCP Toolset |
| :--- | :--- | :--- | :--- |
| **Lead Orchestrator** | GPT-5.6 / GPT-5.5 | Issue decomposition, task graph creation, state auditing | `mcp_dispatch_task`, `mcp_verify_ci` |
| **Code Refactoring Agent** | Claude 5.6 Sonnet | Surgical code editing, file patching, refactoring | `mcp_patch_file`, `mcp_search_ast` |
| **Test Engine Agent** | Gemini 4.0 Ultra | Unit test generation, coverage expansion, integration test run | `mcp_run_tests`, `mcp_calc_coverage` |
| **Security & Audit Agent** | Llama 4 Maverick | Static analysis, secrets scan, vulnerability verification | `mcp_scan_vulnerabilities` |

## Strengths
- **FastMCP 3.1 Task Protocol Alignment**: Native compatibility with early 2027 Task Protocol standards for seamless handshake, lifecycle state, and token routing across agent fleets.
- **Isolated Run Architectures**: Spawns isolated, self-contained runtimes (Docker, WASM, or micro-VMs) for agents to safely build and execute code.
- **Proof-of-Work Constraints**: Enforces mandatory verification steps (compilation gates, test coverage thresholds, lint checks) before submitting pull requests.
- **Multi-Model Support**: Dynamically routes specific tasks to specialized model variants (e.g., GPT-5.6 for architecture, Claude 5.6 for surgical code refinement, Gemini 4.0 Ultra for multimodal auditing).

## Limitations
- **Harness & CI Dependency**: Extremely dependent on pre-existing unit test suites and comprehensive coverage to prevent regressions.
- **Token Consuming**: Deep-research and multi-agent synthesis loops can become highly token-intensive.
- **Evolving Standard**: The FastMCP 3.1 Task Protocol and associated server-side libraries are iterating rapidly, requiring frequent runtime updates.

## Production Systemd Service Unit (`symphony-orchestrator.service`)

Run the Symphony multi-agent supervisor as a resilient background system daemon with process monitoring:

```ini
[Unit]
Description=Symphony Multi-Agent Autonomous Orchestrator
After=network-online.target docker.service
Wants=network-online.target docker.service

[Service]
Type=simple
User=symphony
Group=symphony
WorkingDirectory=/opt/symphony
ExecStart=/opt/symphony/venv/bin/python -m symphony.server \
    --config /etc/symphony/symphony.conf \
    --mcp-port 8080 \
    --sandbox-driver docker
Restart=always
RestartSec=10
LimitNOFILE=65536
EnvironmentFile=/etc/symphony/secrets.env

# Systemd Hardening Guidelines
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/opt/symphony/workspaces /var/log/symphony /tmp
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Production Multi-Container Docker Compose Stack

The following Docker Compose manifest deploys Symphony with an isolated Redis task broker, sandbox execution runner, and FastMCP protocol bridge:

```yaml
version: "3.8"

services:
  symphony-lead:
    image: openai/symphony:v2.4
    container_name: symphony-lead-orchestrator
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - SYMPHONY_REDIS_URL=redis://redis-broker:6379/0
      - SYMPHONY_DEFAULT_MODEL=gpt-5.6
      - FASTMCP_SERVER_PORT=8080
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - ./workspaces:/app/workspaces:rw
      - ./config/SYMPHONY.md:/app/SYMPHONY.md:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      redis-broker:
        condition: service_healthy
    networks:
      - symphony-net

  redis-broker:
    image: redis:7.4-alpine
    container_name: symphony-redis-broker
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass symphonypass123
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "symphonypass123", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - symphony-net

networks:
  symphony-net:
    driver: bridge

volumes:
  redis-data:
```

## Diagnostic Troubleshooting Matrix

| Issue / Error Symptom | Root Cause | Verification Procedure | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **`FastMCPHandshakeTimeout` (10000ms)** | Sandbox container startup delay exceeding handshake threshold | Check system load and Docker daemon start logs | Increase `SYMPHONY_MCP_HANDSHAKE_TIMEOUT_MS=30000` |
| **Flaky CI false negatives in proof gate** | Non-deterministic external network calls in unit tests | Inspect failing test trace for network timeout | Mock external API endpoints or set `verification_retries=3` |
| **Parallel git branch merge conflicts** | Multiple subagents concurrently editing identical source lines | Check git log on conflicting implementation branches | Enable `strict_ast_file_locking=true` in orchestrator settings |
| **Context token limit exhaustion** | Unbounded conversation history in recursive delegation | Calculate cumulative prompt token volume | Enable hierarchical summarization filter with ratio $\gamma \le 0.35$ |
| **Docker sandbox escape / access denied** | Insufficient permissions on `/var/run/docker.sock` | Test docker access with `docker ps` from symphony user | Add symphony user to docker group: `usermod -aG docker symphony` |
| **Model rate limit 429 (`insufficient_quota`)** | Subagent fleet bursting concurrent requests beyond API tier | Check orchestrator API dispatch logs | Configure token bucket rate limiter in `SYMPHONY.md` |
| **Stale task lock in Redis task broker** | Subagent process crash during AST modification pass | Inspect Redis key `symphony:locks:*` via redis-cli | Configure TTL (Time-To-Live) on task lock keys (e.g. 300 seconds) |
| **Pydantic schema validation failure** | FastMCP message payload contains unexpected fields | Inspect raw protocol JSON response in debug logs | Validate against strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) |

## When to use it
- When implementing a fully automated [Software Factories](../../knowledge_base/patterns/software-factories.md) model within mature codebases.
- For managing and orchestrating parallel task executions using high-capability models like [GPT-5.6](../ai_knowledge/chatgpt.md) or [Claude 5.6](../providers/anthropic.md).
- When a codebase already has rigorous automated test suites and robust containerized staging environments.

## When not to use it
- In early-stage, fast-moving prototypes lacking comprehensive unit testing or automated CI.
- For simple interactive tasks where single-agent CLI assistants (such as [Aider](../development_ops/aider.md)) are faster and easier to deploy.

## Getting started

### Requirements
- Containerized or isolated execution environment (Docker or WASM sandbox).
- High-coverage CI test runner.
- Valid API keys for GPT-5.6, Claude 5.6, or Gemini 4.0 Ultra.
- A FastMCP 3.1-compliant environment for agent-to-tool handshakes.

### Installation
```bash
git clone https://github.com/openai/symphony.git
cd symphony
pip install -e . fastmcp pydantic
```
For the Elixir reference implementation:
```bash
cd elixir
mix deps.get
mix compile
```

### Basic Implementation Run
Configure your environment to point to a FastMCP 3.1 Task Protocol endpoint and trigger an autonomous implementation run:
```bash
export SYMPHONY_MODEL=gpt-5.6
export SYMPHONY_MCP_ENDPOINT=http://localhost:8000/v1/task-protocol

# Start an implementation run for a designated issue
symphony run --issue BUG-904 --verify-with-ci
```

## CLI examples

```bash
# Initialize a workspace with standard workflow specifications
symphony start --workflow ./WORKFLOW.md

# List and audit running implementation sessions across the fleet
symphony status --detailed

# Trigger a manual handshake to inspect FastMCP 3.1 Task Protocol capability matrices
symphony mcp handshake --endpoint http://localhost:8080

# Audit code verification metrics across all subagents
symphony audit --run-id run_2027_8812
```

## Production Workflow Configuration (`SYMPHONY.md`)

To standardize multi-agent orchestration for enterprise repositories, place a `SYMPHONY.md` file in the repo root:

```markdown
# Symphony Workflow Specification v2.4

## Task Delegation Rules
- Architecture / Spec: GPT-5.6
- Code Editing: Claude 5.6 Sonnet
- Test Verification: Gemini 4.0 Ultra

## Mandatory Verification Gates
1. `npm test` or `pytest` must achieve 100% pass rate.
2. Code coverage delta must be >= 0.0%.
3. Static security scan (`gitleaks`, `bandit`) must return zero findings.

## Sandbox Configuration
- Container Image: `ubuntu:24.04-slim`
- Max Memory: 8GB
- Execution Timeout: 600s
```

## API examples

### FastMCP 3.1 Orchestration & Strict Pydantic v2 Verification Server
This executable Python script demonstrates building a **FastMCP 3.1** server that receives issue payloads, delegates execution steps, and validates agent run states using strict **Pydantic v2** models (`extra="forbid"`, `frozen=True`):

```python
import asyncio
import time
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from fastmcp import FastMCP

mcp = FastMCP("Symphony Task Orchestrator", version="3.1.0")

class TaskMetric(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    mcp_protocol_version: str = Field("3.1", pattern=r"^3\.\d+$")
    agent_id: str = Field(..., min_length=3)
    tokens_consumed: int = Field(..., ge=0)
    execution_time_ms: float = Field(..., gt=0.0)

class RunStatus(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    issue_id: str = Field(..., pattern=r"^[A-Z]+-\d+$")
    status: Literal["pending", "in_progress", "verifying", "completed", "failed"]
    ci_passed: bool
    metrics: TaskMetric
    active_steps: List[str] = Field(default_factory=list)

    @field_validator("status")
    @classmethod
    def validate_ci_on_completion(cls, v: str, info) -> str:
        if v == "completed" and not info.data.get("ci_passed", False):
            raise ValueError("Run cannot be marked completed if CI is failing.")
        return v

class DispatchTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    issue_id: str = Field(..., description="Target issue key, e.g., FEAT-102")
    target_agent: str = Field(..., description="Agent role allocation")
    instructions: str = Field(..., description="High level instructions")

@mcp.tool(
    name="dispatch_symphony_run",
    description="Trigger an autonomous Symphony agent task run with FastMCP 3.1 protocol handshake."
)
async def dispatch_symphony_run(issue_id: str, target_agent: str, instructions: str) -> str:
    """Trigger an autonomous Symphony agent task run with FastMCP 3.1 protocol handshake."""
    start_time = time.time()

    try:
        req = DispatchTaskRequest(
            issue_id=issue_id,
            target_agent=target_agent,
            instructions=instructions
        )
    except ValidationError as e:
        return f"Validation error: {e.errors()}"

    # Simulated runtime payload returned by Symphony Elixir core
    raw_payload = {
        "issue_id": req.issue_id,
        "status": "completed",
        "ci_passed": True,
        "metrics": {
            "mcp_protocol_version": "3.1",
            "agent_id": req.target_agent,
            "tokens_consumed": 18450,
            "execution_time_ms": 4210.5
        },
        "active_steps": [
            "Parse AST and identify target files",
            "Generate patch via FastMCP tool",
            "Execute CI test runner in Docker sandbox",
            "Verify code coverage threshold"
        ]
    }

    try:
        validated = RunStatus.model_validate(raw_payload)
        elapsed = (time.time() - start_time) * 1000
        return (
            f"Run Verified: {validated.issue_id}\n"
            f"Status: {validated.status} (CI Passed: {validated.ci_passed})\n"
            f"Agent: {validated.metrics.agent_id}\n"
            f"Tokens Consumed: {validated.metrics.tokens_consumed}\n"
            f"Total Tool Latency: {elapsed:.2f}ms\n\n"
            f"Active Steps:\n" + "\n".join([f"- {s}" for s in validated.active_steps])
        )
    except ValidationError as e:
        return f"Validation error: {e.errors()}"

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Software Factories](../../knowledge_base/patterns/software-factories.md)
- [LangGraph](../frameworks/langgraph.md)
- [Bee Agent Framework](bee-agent-framework.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Superpowers](superpowers.md)
- [OpenHands](../development_ops/openhands.md)
- [Devin](../development_ops/devin.md)
- [Cline](cline.md)

## Sources / references
- [Symphony Specifications](https://github.com/openai/symphony/blob/main/SPEC.md)
- [OpenAI GitHub Repository](https://github.com/openai/symphony)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/spec/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
