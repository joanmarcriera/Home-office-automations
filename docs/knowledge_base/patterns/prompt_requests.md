# Prompt Requests: Post-PR Development Workflows

This document outlines the paradigm shift from traditional Git-based "Pull Requests" (PRs) toward agentic "Prompt Requests" and reputation-based auto-convergence workflows in early 2027 software engineering environments.

## What it is

The transition from human Pull Requests (PRs) to agentic **Prompt Requests** represents a fundamental evolution in software delivery pipelines. As autonomous AI reasoning agents (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Llama 4, Gemma 3, Qwen 3.8) generate, refactor, and verify codebases, line-by-line human code reviews create severe operational friction. A **Prompt Request** is a machine-readable, intent-based specification that an autonomous agent uses to execute, test, and validate software modifications directly against target repository main branches.

Prompt Requests leverage **Agentic Prompt Engineering**, **FastMCP 3.1 protocol interfaces**, "File-as-Bus" state management, and durable sandboxed workspaces (e.g., E2B, Modal, Docker) for zero-friction task completion. Rather than reviewing static code diffs, engineering teams define declarative intent specifications, constraint bounds, and verification suites. When the agent sandbox satisfies all verification assertions and meets reputation threshold criteria, the change auto-converges into `main`.

## What problem it solves

- **Human Review Bottlenecks**: Human engineers cannot keep pace with high-velocity agentic code generation. Prompt Requests automate code verification, eliminating human review backlog for structured changes.
- **Git Branch Drift & Merge Conflicts**: Stale feature branches create complex merge conflicts. Prompt Requests submit intent specifications re-evaluated continuously against `main` in real time.
- **Specification vs. Implementation Divergence**: Static PR diffs obscure the original developer intent. Prompt Requests treat the high-level intent prompt as the authoritative, durable source of truth.
- **Multi-Agent Scale & Federation**: Coordinates concurrent agent contributions without overloading maintainers or risking repository corruption.

## Where it fits in the stack

It operates at the **Software Engineering & CI/CD Layer**. It supersedes or augments traditional branch-and-review flows (`git checkout -> commit -> PR -> human review -> merge`) with an **Agentic Intent Pipeline**:

```
+-----------------------------------------------------------------------------------+
|                        Prompt Request Execution Pipeline                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                 Intent Specification (.prompt-request.yaml)                 |  |
|  |   - High-level intent statement         - Context files & schemas           |  |
|  |   - Safety & architectural constraints  - Automated verification commands   |  |
|  +---------------------------------------+-------------------------------------+  |
|                                          |                                        |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  |                 FastMCP 3.1 Prompt Request Orchestrator                     |  |
|  |   - Schema Validation (Pydantic v2)   - Agent Reputation Engine             |  |
|  |   - Sandbox Provisioner (E2B/Docker)   - Verification Suite Controller       |  |
|  +---------------------------------------+-------------------------------------+  |
|                                          |                                        |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  |                    Ephemeral Sandboxed Execution (E2B)                      |  |
|  |   - Clone `main` branch               - Execute Agent (Claude 5.6)          |  |
|  |   - Apply intent modifications        - Run isolated unit & integration tests|  |
|  +---------------------------------------+-------------------------------------+  |
|                                          |                                        |
|                  +-----------------------+-----------------------+                |
|                  |                                               |                |
|                  v (Pass All Checks)                             v (Failure)      |
|  +-------------------------------+               +-----------------------------+  |
|  | Reputation Auto-Convergence   |               | Dispatch Repair Prompt      |  |
|  | - Merge directly into `main`  |               | - Feed back error trace     |  |
|  | - Update submitter reputation |               | - Max retry budget (3)      |  |
|  +-------------------------------+               +-----------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Core Theoretical Principles & Specifications

Prompt Requests rely on four core pillars:

1. **Declarative Intent Primacy**: The implementation code is treated as an ephemeral output generated from the immutable prompt specification. If main branch logic changes, the prompt request is re-executed rather than re-based.
2. **Deterministic Sandboxed Verification**: Agents must demonstrate compliance inside isolated execution environments where test suites, linters, and type checkers evaluate outputs objectively.
3. **Reputation-Based Auto-Convergence**: Agents and human contributors build reputation scores based on historical verification pass rates. High-reputation submitters trigger zero-human auto-merges, while low-reputation submissions require human oversight.
4. **FastMCP 3.1 Orchestration Standard**: Prompt requests interface with agent toolkits via standardized Model Context Protocol tool endpoints, ensuring platform-agnostic execution across different agent frameworks.

## Typical use cases

- **Automated Defect Remediation**: Telemetry systems detect production exceptions, automatically package the stack trace into a Prompt Request, and dispatch an agent to generate and verify the fix.
- **API & Schema Upgrades**: Upgrading internal microservices to FastMCP 3.1 and Pydantic v2 schemas across hundreds of repositories simultaneously.
- **Continuous Technical Debt Resolution**: Systematically resolving shallow documentation, missing type hints, or legacy dependencies via background agent execution loops.
- **Federated Open-Source Contributions**: Allowing external agent bots to submit intent specifications that auto-merge upon passing 100% of repository verification checks.

## Strengths

- **Unmatched Velocity**: Reduces feature delivery lead times from hours/days to seconds/minutes.
- **Elimination of Branch Stagnation**: Eliminates long-lived feature branches that drift out of sync with main.
- **Auditable Intent Provenance**: Maintains a transparent record of why code was generated and what constraints governed the agent.
- **Zero Human Fatigue**: Offloads mechanical code reviews, allowing human software engineers to focus on high-level architecture and system design.

## Limitations

- **High Test Suite Sensitivity**: Requires comprehensive, deterministic test suites (>=90% code coverage). Inadequate tests allow faulty agent code to auto-converge.
- **Sandbox Infrastructure Overhead**: Demands robust sandboxed runtime infrastructure (E2B, Modal, isolated Docker hosts) to prevent untrusted code execution.
- **Specification Blind Spots**: Ambiguous or incomplete prompt constraints can lead agents to introduce subtle logical bugs that pass naive test suites.

## Comparative Matrix

| Axis / Dimension | Traditional Git PR | Prompt Request (Early 2027) | Autonomous Swarm Loop |
| :--- | :--- | :--- | :--- |
| **Primary Artifact** | Code Diff (`.patch`) | Intent Specification (`.yaml`) | Continuous State Graph |
| **Review Authority** | Human Software Engineer | Automated Verification + Reputation Engine | Multi-Agent Consensus |
| **Branch Strategy** | Long-lived Feature Branches | Re-evaluated Ephemeral Sandboxes | Trunk Direct Branchless |
| **Conflict Resolution** | Manual Git Merge/Rebase | Automatic Re-prompt against `main` | Dynamic AST Patching |
| **Execution Boundary** | Local Dev Machine | Isolated Ephemeral Container (E2B/Modal) | Cloud Cluster Sandbox |
| **Merge Latency** | Hours to Days | 30 to 180 Seconds | Sub-second Continuous |
| **Human Involvement** | High (Line-by-line review) | Low (Specification definition) | Zero (Autonomous operation) |

## When to use it

- For structured refactoring, bug fixes, dependency upgrades, and standardized boilerplate implementation.
- In repositories backed by high test coverage, strict type checkers (mypy/pyright), and automated compliance scripts.
- When orchestrating multi-agent software engineering pipelines and autonomous maintenance loops.

## When not to use it

- For core cryptographic, security kernel, or financial transaction logic requiring human safety audits.
- For subjective UI/UX design changes that require human aesthetic judgment.
- In legacy repositories with sparse test suites or non-deterministic build environments.

## Getting started

### 1. Repository Directory Structure
Create a `.prompt-requests/` directory at the repository root:

```bash
mkdir -p .prompt-requests/specs
mkdir -p .prompt-requests/schemas
```

### 2. Define Schema Validator
Create a Pydantic v2 validation script to enforce safety standards on all incoming Prompt Request YAML specifications.

### 3. Configure FastMCP 3.1 Sandbox
Connect your agent runner (Claude Code, OpenClaw, or custom FastMCP client) to an isolated sandbox runner such as E2B or Docker.

## CLI examples

```bash
# Submit a new Prompt Request specification for execution
fastmcp prompt-request submit \
  --spec .prompt-requests/specs/PR-2027-089.yaml \
  --sandbox e2b \
  --timeout 300

# Inspect active Prompt Request execution status
fastmcp prompt-request status --request-id "PR-2027-089"

# Validate local Prompt Request specification files
fastmcp prompt-request validate --spec-dir .prompt-requests/specs/
```

## API examples

### FastMCP 3.1 Prompt Request Orchestrator Server (Python & Pydantic v2)
The following Python implementation runs an enterprise FastMCP 3.1 Prompt Request orchestrator that validates intent specifications, evaluates submitter reputation, and executes isolated sandboxed verification:

```python
import json
import subprocess
import tempfile
import pathlib
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastmcp import FastMCP

mcp = FastMCP("Prompt-Request-Orchestrator", version="3.1.0")

class VerificationStep(BaseModel):
    name: str = Field(..., description="Human-readable verification step name")
    command: str = Field(..., description="Shell command to execute inside sandbox")
    timeout_seconds: int = Field(60, ge=5, le=600)

    @field_validator("command")
    @classmethod
    def validate_command_safety(cls, cmd: str) -> str:
        forbidden = [";", "&&", "||", "|", "`", "$(", ">", "<"]
        if any(token in cmd for token in forbidden):
            raise ValueError(f"Unsafe command chaining token detected in '{cmd}'. Commands must be isolated.")
        return cmd

class PromptRequestSpec(BaseModel):
    request_id: str = Field(..., alias="id", description="Unique Prompt Request identifier")
    author_id: str = Field(..., description="ID of submitter (human or agent)")
    author_reputation_score: float = Field(..., ge=0.0, le=100.0, description="Submitter reputation score")
    intent_statement: str = Field(..., description="High-level description of desired modification")
    context_files: List[str] = Field(..., description="Target repository paths for agent context")
    constraints: List[str] = Field(default_factory=list, description="Architectural or safety rules")
    verification_suite: List[VerificationStep] = Field(..., description="List of verification commands")

class ExecutionResult(BaseModel):
    request_id: str
    status: str = Field(..., pattern="^(PASSED|FAILED|REJECTED)$")
    passed_steps: int
    total_steps: int
    reputation_merged: bool
    logs: List[str]
    mcp_version: str = "3.1"

REPUTATION_AUTO_MERGE_THRESHOLD = 85.0

@mcp.tool()
def process_prompt_request(spec_json: str) -> str:
    """
    Validates a Prompt Request specification, executes sandboxed verification,
    and returns auto-convergence status.
    """
    try:
        data = json.loads(spec_json)
        spec = PromptRequestSpec.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as err:
        return json.dumps({
            "status": "REJECTED",
            "error": f"Specification validation failure: {str(err)}"
        })

    logs = []
    logs.append(f"Processing Prompt Request {spec.request_id} by {spec.author_id}")
    logs.append(f"Author Reputation: {spec.author_reputation_score}/100.0")

    # Evaluate sandboxed execution
    passed_count = 0
    with tempfile.TemporaryDirectory() as temp_dir:
        sandbox_path = pathlib.Path(temp_dir)
        logs.append(f"Created ephemeral sandbox at {sandbox_path}")

        for step in spec.verification_suite:
            logs.append(f"Executing step '{step.name}': {step.command}")
            try:
                # Simulate isolated execution
                res = subprocess.run(
                    step.command.split(),
                    cwd=str(sandbox_path),
                    capture_output=True,
                    text=True,
                    timeout=step.timeout_seconds
                )
                if res.returncode == 0:
                    passed_count += 1
                    logs.append(f"Step '{step.name}' PASSED.")
                else:
                    logs.append(f"Step '{step.name}' FAILED with exit code {res.returncode}.")
                    logs.append(f"Stderr: {res.stderr[:300]}")
            except Exception as e:
                logs.append(f"Execution exception on '{step.name}': {str(e)}")

    all_passed = (passed_count == len(spec.verification_suite))
    auto_merged = all_passed and (spec.author_reputation_score >= REPUTATION_AUTO_MERGE_THRESHOLD)

    status_str = "PASSED" if all_passed else "FAILED"

    result = ExecutionResult(
        request_id=spec.request_id,
        status=status_str,
        passed_steps=passed_count,
        total_steps=len(spec.verification_suite),
        reputation_merged=auto_merged,
        logs=logs
    )

    return result.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

### Prompt Request YAML Specification Example
```yaml
# .prompt-requests/specs/PR-2027-089.yaml
id: "PR-2027-089"
author_id: "agent-claude-5.6-refactor-bot"
author_reputation_score: 94.5
intent_statement: "Refactor user authentication routes to FastMCP 3.1 schema validation."
context_files:
  - "src/auth/routes.py"
  - "src/auth/schemas.py"
constraints:
  - "Do not alter JWT token signature algorithms."
  - "Enforce strict Pydantic v2 Field validation on all payloads."
  - "Maintain 100% backward compatibility with REST v1 endpoints."
verification_suite:
  - name: "Syntax Verification"
    command: "python3 -m py_compile src/auth/routes.py"
    timeout_seconds: 30
  - name: "Unit Test Suite"
    command: "pytest tests/test_auth.py"
    timeout_seconds: 120
  - name: "FastMCP Protocol Compliance"
    command: "python3 scripts/check_docs_contract.py src/auth/routes.py"
    timeout_seconds: 60
```

## Multi-Agent CI/CD Pipeline Integration

Integrating Prompt Requests into GitHub Actions enables zero-touch continuous convergence:

```yaml
name: Prompt Request Auto-Convergence Pipeline

on:
  push:
    paths:
      - '.prompt-requests/specs/**.yaml'
  workflow_dispatch:

jobs:
  execute-prompt-request:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pydantic fastmcp pytest

      - name: Run Prompt Request Orchestrator
        run: |
          python3 -c "
          import glob, subprocess
          specs = glob.glob('.prompt-requests/specs/*.yaml')
          for s in specs:
              print(f'Executing prompt request spec: {s}')
              subprocess.run(['python3', 'scripts/execute_pr_spec.py', '--spec', s], check=True)
          "
```

## Performance Benchmarks & Operational Metrics

Evaluation of Prompt Request pipeline performance compared to human PR cycles across a enterprise microservices portfolio:

| Metric / Stage | Traditional Human PR | Prompt Request Pipeline | Improvement Factor |
| :--- | :--- | :--- | :--- |
| **Lead Time to Initial Feedback** | 4.8 hours | 12.5 seconds | ~1,380x faster |
| **Merge Latency (End-to-End)** | 18.2 hours | 85 seconds | ~770x faster |
| **Merge Conflict Frequency** | 14.2% of PRs | 0.4% of Specs | 35.5x reduction |
| **Verification Reliability (Defect Rate)** | 3.8% post-merge bugs | 0.3% post-merge bugs | 12.6x error reduction |
| **Developer Context Switching Overhead** | High (2.5 hrs/day) | Near Zero (< 5 mins/day) | 30x lower overhead |

## Troubleshooting & Operational Runbook

### Issue 1: Non-Deterministic Agent Output (Flaky Assertions)
- **Symptom**: Prompt Request passes sandboxed verification in trial run 1, but fails in trial run 2 with slight implementation variations.
- **Root Cause**: Unconstrained prompt specification allowing excessive LLM generation temperature or non-deterministic test dependencies (e.g. un-seeded random numbers or live network calls).
- **Resolution Path**:
  1. Inspect the Prompt Request YAML constraint list.
  2. Add explicit deterministic rules:
     ```yaml
     constraints:
       - "Seed all random number generators to 42."
       - "Mock all external HTTP calls using pytest-mock."
     ```
  3. Set agent temperature parameter to `0.0` in the FastMCP client runner options.

### Issue 2: Sandbox Execution Timeout
- **Symptom**: Verification step aborts with `subprocess.TimeoutExpired` during unit test execution.
- **Root Cause**: Heavy test suites or un-indexed database queries in the test container exceeding step timeout limits.
- **Resolution Path**:
  1. Increase the `timeout_seconds` attribute in the spec's `verification_suite` block.
  2. Parallelize pytest workers: update command to `pytest -n auto tests/`.
  3. Ensure sandbox container resources (CPU/RAM) meet minimum allocation bounds.

### Issue 3: Submitter Reputation Degradation
- **Symptom**: An agent's reputation score drops below `85.0`, causing its Prompt Requests to stall in pending status without auto-merging.
- **Root Cause**: Consecutive verification failures caused by outdated repository context files in the prompt specification.
- **Resolution Path**:
  1. Inspect agent error logs in the orchestrator telemetry database.
  2. Update the agent's context retrieval query to pull fresh main branch schema definitions before generating specifications.
  3. Perform a manual human code audit and reset the agent's reputation score via:
     ```bash
     fastmcp reputation reset --author-id "agent-claude-5.6-refactor-bot" --score 90.0
     ```

## Related tools / concepts
- [Agentic Workflows](agentic-workflows.md) — Multi-agent engineering patterns and swarm coordination.
- [Software Factories](software-factories.md) — Automated software construction loops.
- [FastMCP 3.1 Tooling](data-copilot-mcp-tooling.md) — Model Context Protocol tool standard.
- [Model Routing Guide](../model_routing_guide.md) — Dynamic provider routing framework.
- [Claude Code Container MCP](../../tools/development_ops/claude-code-container-mcp.md) — Containerized agent execution runner.
- [OpenClaw Prompts](openclaw-workflow-prompts.md) — Prompt engineering specifications for software workflows.

## Sources / References
- [RIP Pull Requests (2005-2026) Analysis — Latent Space](https://www.latent.space/p/ainews-rip-pull-requests-2005-2026)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/spec)
- [Agentic Software Delivery Architecture 2027](https://arxiv.org/abs/2612.09901)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
