# Superpowers

## What it is
Superpowers is a comprehensive software development workflow and agentic skills framework designed for next-generation coding agents like [Claude Code](../development_ops/claude-code.md), [Cursor](../development_ops/cursor.md), and [Aider](../development_ops/aider.md). It builds on top of composable "skills" to enforce a rigorous engineering process, optimized for frontier models like [Claude 5.6](../providers/anthropic.md) and [GPT-5.6](../ai_knowledge/openai.md) while utilizing **Gemini 4.0 Pro visual reasoning** and **FastMCP 3.1** for complex UI tasks, sandbox execution, and agentic tool orchestration.

Superpowers enforces structured planning, test-driven development (TDD), YAGNI principles, DRY architecture, and automated verification gates across multi-file refactoring tasks, converting chaotic agent interactions into reproducible, enterprise-grade software engineering pipelines.

```mermaid
architecture-beta
    group agent_layer(cloud, "Coding Agent Layer")
    service claude_code(cpu, "Claude Code CLI / Cursor") in agent_layer
    service superpowers_engine(server, "Superpowers Workflow Engine") in agent_layer

    group skill_system(database, "Superpowers Skill Framework")
    service plan_skill(disk, "Plan & Spec Skill") in skill_system
    service tdd_skill(code, "TDD Enforcer Skill") in skill_system
    service verify_skill(check, "Verification & Audit Skill") in skill_system

    group runtime_env(internet, "Sandbox & Execution Layer")
    service mcp_bridge(network, "FastMCP 3.1 Tool Bridge") in runtime_env
    service vision_eval(camera, "Gemini 4.0 Pro Visual Verifier") in runtime_env
    service git_sandbox(disk, "Isolated Git Worktree Sandbox") in runtime_env

    claude_code --> superpowers_engine: User Prompt & Directives
    superpowers_engine --> plan_skill: Task Decomposition & Spec Draft
    plan_skill --> tdd_skill: Red-Green-Refactor Plan
    tdd_skill --> mcp_bridge: FastMCP Tool Calls
    mcp_bridge --> git_sandbox: File Edits & Unit Test Execution
    git_sandbox --> verify_skill: Test Results & Coverage
    verify_skill --> vision_eval: Screenshot / UI Rendering Check
    vision_eval --> superpowers_engine: Approval Gate & PR Entry
```

---

## Mathematical Formulation: TDD State Transitions & Test Entropy

Under Superpowers, software modifications follow a strictly ordered finite state machine (FSM) governed by **Test-Driven Development (TDD)** and entropy reduction.

Let a codebase state at step $t$ be represented by $\mathcal{S}_t = \langle \mathcal{C}_t, \mathcal{T}_t, \mathcal{E}_t \rangle$, where $\mathcal{C}_t$ is implementation source code, $\mathcal{T}_t$ is the test suite, and $\mathcal{E}_t$ represents the execution evaluation vector.

For a target test suite $\mathcal{T} = \{\tau_1, \tau_2, \dots, \tau_N\}$, the pass indicator function is $I(\tau_i \mid \mathcal{C}) \in \{0, 1\}$. The **Test Failure Entropy** $H(\mathcal{T} \mid \mathcal{C})$ is formulated as:

$$
H(\mathcal{T} \mid \mathcal{C}) = - \left( p_{\text{pass}} \log_2 p_{\text{pass}} + p_{\text{fail}} \log_2 p_{\text{fail}} \right)
$$

Where:

$$
p_{\text{pass}} = \frac{1}{N} \sum_{i=1}^N I(\tau_i \mid \mathcal{C}), \quad p_{\text{fail}} = 1 - p_{\text{pass}}
$$

The Superpowers transition operator $\Psi$ enforces a 3-phase invariant:

$$
\mathcal{S}_{\text{start}} \xrightarrow{\Psi_{\text{red}}} \mathcal{S}_{\text{red}} \xrightarrow{\Psi_{\text{green}}} \mathcal{S}_{\text{green}} \xrightarrow{\Psi_{\text{refactor}}} \mathcal{S}_{\text{refactor}}
$$

1. **Red Phase Requirement**: The new test $\tau_{\text{new}}$ must fail cleanly against prior code $\mathcal{C}_0$:
   $$
   I(\tau_{\text{new}} \mid \mathcal{C}_0) = 0 \quad \text{and} \quad \text{exit\_code}(\tau_{\text{new}}) \ne 0
   $$
2. **Green Phase Requirement**: Implementation edits $\Delta \mathcal{C}$ must satisfy all tests simultaneously without regression:
   $$
   \forall \tau \in \mathcal{T} \cup \{\tau_{\text{new}}\}, \quad I(\tau \mid \mathcal{C}_0 + \Delta \mathcal{C}) = 1
   $$
3. **Refactor Phase Invariant**: Structural optimization preserving behavioral invariance ($H \to 0$):
   $$
   \Delta H = |H(\mathcal{T} \mid \mathcal{C}_{\text{refactored}}) - H(\mathcal{T} \mid \mathcal{C}_{\text{green}})| = 0
   $$

For visual verification tasks using Gemini 4.0 Pro, rendering fidelity between reference design $I_{\text{ref}}$ and actual screenshot $I_{\text{actual}}$ is evaluated via the **Structural Similarity Index Measure (SSIM)**:

$$
\text{SSIM}(x, y) = \frac{(2\mu_x \mu_y + c_1)(2\sigma_{xy} + c_2)}{(\mu_x^2 + \mu_y^2 + c_1)(\sigma_x^2 + \sigma_y^2 + c_2)}
$$

Superpowers mandates $\text{SSIM}(I_{\text{ref}}, I_{\text{actual}}) \ge 0.95$ before passing UI verification gates.

---

## What problem it solves
It addresses the lack of discipline and engineering rigor in standard AI coding interactions by providing a structured, skills-based workflow for design, planning, and implementation. Standard coding agent sessions frequently suffer from:
- **Hallucinated File Paths and Dependencies**: Editing non-existent modules or introducing incompatible library versions.
- **Circular Refactoring Loops**: Repeatedly fixing unit tests by breaking other existing modules without root-cause diagnosis.
- **Spec Drift and Premature Implementation**: Writing code before validating requirements or designing explicit component interfaces.

Superpowers prevents these failure modes by enforcing a strict **Plan-First, Test-Driven Execution Loop**, achieving top-tier performance on benchmarks like [SWE-bench](../benchmarking/swe-bench.md).

---

## Where it fits in the stack
**Agents / Workflow Framework**. It sits on top of coding agents to provide process-level guardrails and skills. It is often used in conjunction with the [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md) for direct filesystem and terminal control within containerized sandboxes.

```
+-----------------------------------------------------------------------+
|                      User & Team Interaction Layer                    |
|             (CLI Commands, Pull Requests, Issue Trackers)             |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                 Superpowers Agent Orchestration Layer                 |
|  +--------------------+ +--------------------+ +-------------------+  |
|  | Plan & Spec Skill  | | TDD Guardrail Loop | | FastMCP 3.1 Task  |  |
|  | YAML Skill Rules   | | Red-Green-Refactor | | State Sync        |  |
|  +--------------------+ +--------------------+ +-------------------+  |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                      Execution & Sandbox Bridge                       |
|   +-----------------------+               +-----------------------+   |
|   | FastMCP 3.1 Server    |               | Gemini 4.0 Pro Vision |   |
|   | Desktop Commander     |               | Visual UI Verifier    |   |
|   +-----------------------+               +-----------------------+   |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                    Target Repository & Test Suite                     |
|           (Pytest, Jest, Playwright, Git Working Tree)                |
+-----------------------------------------------------------------------+
```

---

## Engineering Agent Framework Comparison Matrix

| Dimension / Capability | Superpowers | MetaGPT | Devika | OpenHands | SWE-agent |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Paradigm** | Skills-first TDD FSM | Multi-agent SOP | Fullstack Agent | Docker Sandbox Agent | CLI Agent Tuning |
| **TDD Red-Green Gate** | Strictly enforced in FSM | Post-hoc review | Optional | Optional | Benchmark harness |
| **Visual Verification** | Gemini 4.0 Pro + SSIM | None | Browser screenshots | Playwright eval | None |
| **FastMCP 3.1 Support** | Native Task Protocol | None | Custom REST | Internal Tool API | Custom CLI commands |
| **Context Window Control** | Dynamic Skill Scoping | Message routing | Workspace indexing | Micro-agent loops | File windowing |
| **State Serialization** | Pydantic v2 JSON Spec | Markdown SOPs | SQLite database | Event stream | Shell history |

---

## Production Multi-Container Orchestration (`docker-compose.yml`)

The following Compose specification deploys a containerized Superpowers workflow execution cluster with headless Playwright browser automation, Redis state management, and a FastMCP 3.1 task gateway:

```yaml
version: "3.8"

services:
  superpowers-daemon:
    image: python:3.11-slim
    container_name: superpowers-daemon
    restart: unless-stopped
    working_dir: /workspace
    environment:
      - SUPERPOWERS_ENV=production
      - FASTMCP_PORT=8001
      - REDIS_URL=redis://superpowers-redis:6379/0
      - PLAYWRIGHT_WS_ENDPOINT=ws://headless-chromium:3000
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    ports:
      - "8001:8001"
    volumes:
      - .:/workspace:rw
      - superpowers_state:/root/.superpowers
    command: >
      bash -c "pip install fastmcp>=3.1.0 pydantic>=2.0 redis pytest playwright httpx && python3 -m scripts.superpowers_server"
    depends_on:
      - superpowers-redis
      - headless-chromium

  headless-chromium:
    image: browserless/chrome:latest
    container_name: superpowers-chrome
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - CONCURRENT=5
      - KEEP_ALIVE=true

  superpowers-redis:
    image: redis:7.2-alpine
    container_name: superpowers-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - superpowers_redis_data:/data

volumes:
  superpowers_state:
  superpowers_redis_data:
```

---

## Production Systemd Service Unit (`superpowers.service`)

To host the Superpowers execution bridge as a managed Linux daemon:

```ini
[Unit]
Description=Superpowers TDD Workflow Engine & FastMCP Gateway
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=developer
Group=developer
WorkingDirectory=/opt/superpowers-runner
ExecStart=/usr/local/bin/python3 -m scripts.superpowers_server --port 8001 --strict-tdd
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=SUPERPOWERS_STRICT_TDD=1

# Security and Sandboxing
ProtectSystem=strict
ProtectHome=read-only
PrivateTmp=true
NoNewPrivileges=true
ReadWritePaths=/opt/superpowers-runner/artifacts /opt/superpowers-runner/logs /tmp

# Resource Limits
LimitNOFILE=65536
MemoryAccounting=true
MemoryHigh=8G
MemoryMax=12G

[Install]
WantedBy=multi-user.target
```

Reload and initialize:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now superpowers.service
sudo systemctl status superpowers.service
```

---

## Typical use cases
- **Enforcing Test-Driven Development (TDD)**: Ensuring unit tests are written and verified as failing *before* any implementation code is generated.
- **Breaking Down Complex Architectural Tasks**: Decomposing multi-module refactoring goals into distinct, verifiable sub-tasks with isolated git commits.
- **Managing Long-Running Autonomous Coding Sessions**: Sustaining multi-hour agent execution pipelines across hundreds of files without spec drift.
- **Visual Regression Testing**: Combining Gemini 4.0 Pro visual reasoning with Playwright screenshots to verify UI component rendering.
- **Standardizing Team Agent Behaviors**: Distributing version-controlled `.superpowers` skill definitions across enterprise software engineering teams.

---

## Strengths
- **FastMCP 3.1 Task Protocol**: Native implementation of the standardized task protocol for multi-agent handoffs, state serialization, and verifiable progress across Llama 4, Gemma 4, and Qwen 3.6 VL.
- **Visual Reasoning Integration**: Native hooks into **Gemini 4.0 Pro** for automated UI/UX visual verification, screenshot diff analysis, and accessibility checking.
- **Process Rigor**: Strict guardrails enforcing industry standards (TDD, YAGNI, DRY, SOLID).
- **Agent Autonomy**: High reliability achieved through explicit verification steps, isolated sandbox execution, and self-correction loops.
- **Frontier Model Optimization**: Fine-tuned for the long-context and complex reasoning capabilities of [Claude 5.6](../providers/anthropic.md) and [GPT-5.6](../ai_knowledge/openai.md).

---

## Limitations
- **Process Overhead**: Introduces higher latency and token usage for trivial "one-liner" code modifications.
- **Environment Requirements**: Requires a agent execution environment supporting the Superpowers skills protocol or MCP connections.
- **Token Budget Footprint**: Deep planning and verification cycles consume significant prompt tokens (mitigated by token-saving patterns in [Everything Claude Code](../ai_knowledge/everything-claude-code.md)).
- **Skill Authoring Learning Curve**: Authoring custom skill YAMLs and verification hooks requires understanding Superpowers event triggers.

---

## When to use it
- To enforce high-quality engineering standards (TDD, YAGNI, DRY) in agent-driven development.
- When you want agents to work autonomously for extended periods (hours) without deviating from an architectural plan.
- For complex projects that require a systematic approach to design, planning, and implementation, as described in the [AI-Assisted Dev Workflow](../../playbooks/dev-workflow-ai-assisted.md).
- When multi-agent systems require verifiable task status handoffs using FastMCP 3.1.

---

## When not to use it
- For trivial code changes, quick questions, or interactive exploratory scripting.
- If you prefer an ad-hoc, conversational approach to coding without structured planning or test requirements.
- In restricted environments where coding agents lack terminal, filesystem, or container execution permissions.

---

## Getting started

### Installation (Claude Code Plugin)
Superpowers is installed as a plugin or set of skill packages using the FastMCP 3.1 marketplace:

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### Enabling Gemini 4.0 Pro Visual Verification
To enable visual UI/UX verification using Gemini 4.0 Pro reasoning:

```bash
superpowers config set vision_provider gemini-4.0-pro
superpowers config set vision_api_key $GEMINI_API_KEY
```

### Creating Custom Skill Packages
Create a custom TDD coverage skill definition in `.superpowers/skills/coverage_check.yaml`:

```yaml
name: "coverage_check"
description: "Runs Pytest coverage and verifies that new code achieves at least 85% coverage."
version: "3.1.0"
execution:
  command: "pytest --cov=src --cov-report=json"
  evaluator: "python .superpowers/evaluators/check_coverage.py"
guardrails:
  fail_on_coverage_drop: true
  min_coverage_pct: 85
```

---

## CLI examples

```bash
# List all active Superpowers skills and MCP tool integrations
superpowers list --active

# Initialize a new engineering plan for a complex feature task
superpowers plan "Refactor authentication logic to use JWT with Pydantic v2 validation"

# Execute verification steps for a specific sub-task ID
superpowers verify --task-id task-2027-auth-01 --file tests/test_auth.py

# Run visual verification loop against a rendered Playwright screenshot
superpowers vision-check --image artifacts/login_screen.png --spec specs/login.md
```

---

## API examples

### Python Task Execution Engine with Strict Pydantic v2 Validation
You can interact with Superpowers programmatically to define task specifications, validate execution payloads, and execute verification hooks using FastMCP 3.1 tooling context and Pydantic v2 validation (`ConfigDict(extra="forbid", frozen=True)`).

```python
import json
import sys
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError

class TaskSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str = Field(..., description="Unique alphanumeric identifier for the task")
    title: str = Field(..., min_length=5, description="Short descriptive title of the task")
    affected_files: List[str] = Field(default_factory=list, description="Target files for modification")
    require_tdd: bool = Field(default=True, description="Enforce TDD test-first cycle")
    min_test_coverage: float = Field(default=85.0, ge=0.0, le=100.0)

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v: str) -> str:
        clean = v.strip().lower()
        if not clean.startswith("task-"):
            raise ValueError("task_id must begin with 'task-' prefix")
        return clean

class ExecutionStepResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    step_index: int = Field(..., ge=0)
    command: str = Field(..., min_length=1)
    exit_code: int = Field(...)
    stdout: str = Field(default="")
    stderr: str = Field(default="")
    passed: bool = Field(...)

class SuperpowersTaskReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    spec: TaskSpec
    steps_executed: List[ExecutionStepResult] = Field(default_factory=list)
    overall_status: str = Field(..., description="PASSED, FAILED, or IN_PROGRESS")
    summary: str = Field(...)

def run_superpowers_task_pipeline(raw_spec_payload: dict) -> SuperpowersTaskReport:
    try:
        spec = TaskSpec.model_validate(raw_spec_payload)

        # Simulate executing TDD step 1: Test writing (Red phase)
        step_1 = ExecutionStepResult(
            step_index=0,
            command="pytest tests/test_jwt_auth.py",
            exit_code=1,
            stdout="1 failed, 0 passed in 0.12s (Tests created before implementation)",
            stderr="",
            passed=True
        )

        # Simulate executing TDD step 2: Implementation & passing (Green phase)
        step_2 = ExecutionStepResult(
            step_index=1,
            command="pytest tests/test_jwt_auth.py --cov=src/auth",
            exit_code=0,
            stdout="3 passed in 0.45s. Coverage: 91.2%",
            stderr="",
            passed=True
        )

        return SuperpowersTaskReport(
            spec=spec,
            steps_executed=[step_1, step_2],
            overall_status="PASSED",
            summary="Task completed under TDD guardrails with 91.2% coverage achieved."
        )

    except ValidationError as e:
        print(f"Task specification validation failed: {e.errors()}")
        raise

if __name__ == "__main__":
    payload = {
        "task_id": "task-2027-jwt-01",
        "title": "Refactor authentication middleware to use JWT tokens",
        "affected_files": ["src/auth/jwt.py", "tests/test_jwt_auth.py"],
        "require_tdd": True,
        "min_test_coverage": 85.0
    }

    report = run_superpowers_task_pipeline(payload)
    print("Superpowers Execution Report (JSON):")
    print(report.model_dump_json(indent=2))
```

### FastMCP 3.1 Task Execution Tool Server
Exposing Superpowers skills as a FastMCP 3.1 server endpoint:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

mcp = FastMCP("superpowers-orchestrator", version="3.1.0")

class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    feature_description: str = Field(..., min_length=10)
    target_repo: str = Field(..., min_length=1)

class PlanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    plan_id: str
    subtasks: list[str]
    tdd_mode: bool

@mcp.tool(
    name="generate_engineering_plan",
    description="Generates a structured TDD engineering plan using Superpowers skill guardrails."
)
async def generate_engineering_plan(params: PlanRequest) -> PlanResponse:
    subtasks = [
        f"Write failing unit tests for {params.feature_description}",
        f"Implement minimum viable code for {params.feature_description}",
        "Run coverage verification and visual regression audit"
    ]
    return PlanResponse(
        plan_id=f"plan-{abs(hash(params.feature_description)) % 10000}",
        subtasks=subtasks,
        tdd_mode=True
    )

if __name__ == "__main__":
    mcp.run(transport="sse", port=8001)
```

---

## Systematic Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **`PrematureImplementationError`** | Agent wrote application code before establishing failing unit tests | `superpowers verify --tdd-status` | Revert code diff and write failing test suite first (Red Phase). |
| **`CoverageThresholdDrop`** | New code coverage fell below declared 85% project threshold | `pytest --cov=src --cov-report=term-missing` | Add targeted unit tests for un-covered conditional branches. |
| **`SSIMVisualRegressionFail`** | UI rendered screenshot SSIM dropped below 0.95 threshold | `superpowers vision-check --diff` | Compare rendered artifact against Figma/spec baseline and fix CSS styling. |
| **`FastMCPSocketDisconnect`** | Sub-task runner exceeded default 120s execution timeout | Check daemon log: `journalctl -u superpowers -n 50` | Split long refactoring task into multiple granular sub-tasks. |
| **`CircularRefactorLoop`** | Agent toggling fixes between two mutually conflicting tests | `superpowers audit-history --recent 5` | Step back to spec planning phase and clarify component contract boundaries. |
| **`BrowserlessConnectionRefused`** | Headless Chrome container not reachable on port 3000 | `curl -s http://headless-chromium:3000/json/version` | Verify Docker container network and restart `headless-chromium` service. |
| **`PydanticFrozenInstanceError`** | Hook attempting to directly mutate fields on `TaskSpec` | Review Python traceback logs | Use `task.model_copy(update={...})` for immutable record transformations. |
| **`TokenBudgetExhaustion`** | Deep planning session consuming excessive context tokens | `claude /usage` | Prune unneeded test output buffers using `--compact-logs` flag. |

---

## Related tools / concepts
- [Agency-Agents](agency-agents.md) — Multi-agent persona frameworks.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's agentic CLI terminal.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Interoperability protocol (FastMCP 3.1).
- [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md) — System filesystem and process control bridge.
- [Aider](../development_ops/aider.md) — Command-line AI pair programmer.
- [Plandex](../development_ops/plandex.md) — Enterprise task decomposition engine.
- [Mentat](../development_ops/mentat.md) — Context-aware AI coding agent.
- [SWE-bench](../benchmarking/swe-bench.md) — Software engineering agent benchmark.

---

## Sources / references
- [Official GitHub Repository](https://github.com/obra/superpowers)
- [Superpowers for Claude Code (Blog Post)](https://blog.fsck.com/2025/10/09/superpowers/)
- [Anthropic Agent Skills Specification](https://agentskills.io/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.0)
- [Awesome Skills Directory](https://awesome-skills.com/)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
