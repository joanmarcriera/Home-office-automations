# Software Factories Pattern

An architectural pattern for high-autonomy, non-interactive software engineering where agents spec, code, and verify work through rigorous validation harnesses as of early January 2027.

## What it is
The Software Factory is a "dark factory" approach to development where autonomous agents (Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, [Gemma 3](../../tools/ai_knowledge/local_llms.md), [Llama 4](../../tools/ai_knowledge/local_llms.md)) operate within closed-loop environments. It shifts the human role from writing code to defining the "seeds" (specifications) and "validation harnesses" (test scenarios), treating code generation as a high-volume, low-marginal-cost industrial process using **AI-native software assembly** with the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1**.

## Closed-Loop Factory Architecture

```
+-----------------------------------------------------------------------------------+
|                        Autonomous Software Factory Pipeline                       |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------------+        +-----------------------------------------+  |
|  | Human / System Seed File  +------->+ FastMCP 3.1 Factory Task Controller      |  |
|  +---------------------------+        +--------------------+--------------------+  |
|                                                            |                      |
|                                                            v                      |
|  +---------------------------+        +-----------------------------------------+  |
|  | Multi-Trajectory Agent    +<------>+ Docker Isolated Validation Sandbox      |  |
|  | (Claude 5.6 / Llama 4)    |        | (AST, Linters, Integration Test Suite)  |  |
|  +---------------------------+        +--------------------+--------------------+  |
|                                                            |                      |
|                                                            v                      |
|  +---------------------------+        +-----------------------------------------+  |
|  | Automated PR / Merge Hub  +<-------+ Satisfaction Evaluator (Pydantic v2)    |  |
|  +---------------------------+        +-----------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It eliminates the human review bottleneck in traditional PR workflows and mitigates "inhuman mistakes" through exhaustive automated validation. It addresses the economic challenge of building and maintaining complex digital twins, legacy system migrations, and specialized tooling that was previously too expensive for manual development.

## Where it fits in the stack
The Software Factory resides in the **Orchestration and Quality Layer** of the [Home-Office Architecture](../../architecture/README.md). It serves as the primary engine for [Jules](../../tools/ai_knowledge/jules.md) and other coding agents, utilizing **MCP 3.1** (with **FastMCP 3.1** for low-latency tool hosting) for tool-use and [Docker](../../tools/infrastructure/docker.md) for isolated validation environments.

## Software Factory Orchestration Engine Comparison

| Factory Framework / Engine | Execution Autonomy | Isolation Sandbox | Primary Validation Mechanism | Preferred LLM Engines |
| :--- | :--- | :--- | :--- | :--- |
| **Jules Factory Engine** | High (Multi-Day Loops) | Docker Container / Rootless | Satisfaction-Based Test Suites | Claude 5.6, GPT-5.6, DeepSeek-V4 |
| **StrongDM Factory Pattern** | Fully Autonomous | Firecracker MicroVMs | Deterministic Unit & Integration Scans | Gemini 4.0 Pro, Llama 4 |
| **OpenClaw Factory Mesh** | Hybrid Autonomous | Podman / Linux Namespaces | FastMCP 3.1 Task Contracts | Local Qwen 3.6 Coder / vLLM |
| **Traditional CI/CD Agent** | Semi-Autonomous | Standard Runner / VM | Unit Tests & Lint Checks | Claude 3.5 Sonnet / GPT-4o |

## Typical use cases
- **Autonomous Maintenance**: Agents that monitor, debug, and patch production codebases without human intervention.
- **Gene Transfusion**: Automatically porting legacy business logic from monolithic architectures to modern microservices or agent-native platforms.
- **Digital Twin Development**: Generating high-fidelity mocks of external SaaS services (Okta, Jira, Slack) for safe, high-volume stress testing.
- **Documentation as Code**: Maintaining perfectly synced technical documentation by having agents update docs whenever a code change is validated.
- **Automated Validation Ingestion**: Programmatically parsing and validating incoming factory seeds using strong schema guarantees.
- **Continuous Technical Debt Elimination**: Systematic overnight deprecation and refactoring of legacy APIs across thousands of microservices.

## Strengths
- **Compounding Correctness**: Long-horizon workflows can self-correct when guided by strong, deterministic validation loops.
- **Infinite Scalability**: Production throughput is limited only by token availability and compute, not by human developer availability.
- **High-Fidelity Mocks**: Enables testing against complex scenarios that are impossible to simulate manually.
- **Self-Documenting Evolution**: Every change comes with an agentic trace and automated validation report.

## Limitations
- **Token Intensive**: High-autonomy loops require significant spending on frontier models for reasoning and synthesis.
- **Seed Dependency**: The quality of the output is strictly bounded by the precision of the initial human-provided specification or "seed."
- **Infrastructure Overhead**: Requires sophisticated, containerized validation environments to prevent side effects from autonomous code execution.
- **Probabilistic Success**: Outcomes are based on multiple trajectories, requiring "Satisfaction-Based Validation" rather than simple boolean pass/fail.

## When to use it
- When building systems where the cost of human review exceeds the cost of exhaustive token-based validation.
- For "Maintenance-Heavy" projects where the goal is zero manual hand-coding for routine updates.
- When you need to create "Dark Factory" environments for rapid prototyping and iteration.
- In high-concurrency environments where manual PR reviews would stall development.

## When not to use it
- For small, low-complexity scripts where a human can verify the code in seconds.
- In low-budget environments where the token cost for recursive validation is prohibitive (unless using local LLMs like Qwen 3.6 Coder).
- For safety-critical systems where the validation harness itself cannot be 100% verified by humans.

## Systemd Service Configuration
Managing an automated software factory dispatcher daemon on Linux build servers using systemd:

```ini
[Unit]
Description=Software Factory Autonomous Task Runner & Harness Daemon
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=factory
Group=factory
WorkingDirectory=/var/lib/software-factory
Environment="FACTORY_SANDBOX=docker"
Environment="MAX_CONCURRENT_TRAJECTORIES=4"
Environment="MCP_PORT=8095"
ExecStart=/usr/local/bin/python3 -m software_factory.daemon --config /etc/software-factory/config.json
Restart=always
RestartSec=5s
LimitNOFILE=65536
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
ProtectSystem=full
ProtectHome=read-only
ReadWritePaths=/var/lib/software-factory/runs /var/lib/software-factory/logs

[Install]
WantedBy=multi-user.target
```

## Production Docker Compose Multi-Container Stack
Complete isolated execution topology for autonomous software generation, testing harnesses, and scoring engines:

```yaml
version: "3.8"

services:
  factory-orchestrator:
    image: software-factory/controller:2027.1
    container_name: factory-controller
    restart: unless-stopped
    ports:
      - "8095:8095"
    environment:
      - RUNNER_POOL_URL=http://factory-sandbox:9000
      - EVALUATOR_URL=http://satisfaction-eval:5000
      - MAX_RETRIES=5
      - SATISFACTION_THRESHOLD=0.92
    volumes:
      - ./seeds:/seeds:ro
      - factory_runs:/workspace/runs
    networks:
      - factory-mesh

  factory-sandbox:
    image: software-factory/runner-sandbox:latest
    container_name: factory-sandbox
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=1g
    volumes:
      - factory_runs:/workspace/runs
    networks:
      - factory-mesh

  satisfaction-eval:
    image: software-factory/evaluator:latest
    container_name: factory-evaluator
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - AST_STRICTNESS=high
      - LINT_SCORE_MIN=9.0
    networks:
      - factory-mesh

networks:
  factory-mesh:
    driver: bridge

volumes:
  factory_runs:
```

## Getting started

### Local Factory Orchestration (Ollama + vLLM)
Implement a software factory using local, high-performance coding models like [Gemma 3](../../tools/ai_knowledge/local_llms.md) or [Llama 4](../../tools/ai_knowledge/local_llms.md) to minimize costs.

```yaml
services:
  factory_agent:
    image: jules-factory-node:latest
    environment:
      - MODEL=gemma3-27b-it
      - BACKEND=vllm
    volumes:
      - ./seeds:/seeds
      - ./harnesses:/harnesses
      - ./output:/output
    restart: unless-stopped
```

### The "Gene Transfusion" Seed
Example of a factory seed for porting a legacy function:
*"Source: legacy_auth.py. Target: Go (auth_svc). Harness: integration_suite_v1. Run until 100% satisfaction in auth_scenario.md."*

## CLI examples

```bash
# Start an autonomous factory run from a seed file
jules-cli factory --seed ./seeds/migration_v2.md --harness ./tests/auth_suite

# Monitor the agentic trace and validation progress
jules-cli monitor --session factory_run_01

# Inspect the 'Digital Twin' status in the local factory environment
docker exec -it factory_mock_okta status

# Validate trajectory satisfaction score manually
factory-eval --trajectory-id tx_9821 --report /workspace/runs/tx_9821/report.json
```

## API examples

### FastMCP 3.1 Software Factory Task Dispatcher
This FastMCP 3.1 tool server manages software factory job creation and validation runs over the standardized Task Protocol:

```python
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional

mcp = FastMCP("Software Factory Control Plane", version="3.1.0")

class FactoryTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    seed_id: str = Field(..., description="Unique seed specification identifier")
    target_language: str = Field(..., description="Target programming language (python, go, rust)")
    max_iter: int = Field(10, ge=1, le=50, description="Maximum self-healing loop iterations")
    target_satisfaction_threshold: float = Field(default=0.90, ge=0.50, le=1.0)
    sandbox_image: str = Field(default="software-factory/runner-sandbox:latest")

    @field_validator("target_language")
    @classmethod
    def validate_lang(cls, v: str) -> str:
        supported = {"python", "go", "rust", "typescript", "c"}
        if v.lower() not in supported:
            raise ValueError(f"Language {v} not supported. Must be one of {supported}")
        return v.lower()

class FactoryTaskStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    job_id: str
    status: str
    current_satisfaction: float
    iterations_completed: int
    active_sandbox_id: Optional[str] = None

@mcp.tool(name="dispatch_factory_job", description="Dispatches an autonomous software generation task into the isolated container harness")
async def dispatch_factory_job(req: FactoryTaskRequest, ctx: Context) -> FactoryTaskStatus:
    """Dispatches an autonomous software generation task into the isolated container harness."""
    ctx.info(f"Initiating software factory run for seed '{req.seed_id}' in language '{req.target_language}'")

    return FactoryTaskStatus(
        job_id="fact_9021",
        status="RUNNING_VALIDATION_LOOP",
        current_satisfaction=0.82,
        iterations_completed=2,
        active_sandbox_id="box_sandbox_9021"
    )

if __name__ == "__main__":
    mcp.run()
```

### Satisfaction-Based Scoring API (Python & Pydantic v2)
The following Python script illustrates how satisfaction-based evaluations are structured, verified, and parsed using modern Pydantic v2.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict

class TrajectoryMetric(BaseModel):
    """Evaluation metrics for an agent's code generation run in the factory."""
    model_config = ConfigDict(extra="forbid")

    test_coverage: float = Field(..., ge=0.0, le=100.0, description="Percentage of test coverage")
    pylint_score: float = Field(..., ge=0.0, le=10.0, description="Pylint static code quality score")
    vulnerabilities_found: int = Field(default=0, ge=0, description="Number of security issues identified")
    cyclomatic_complexity_delta: int = Field(default=0, description="Delta against baseline complexity")

class SatisfactionEvaluation(BaseModel):
    """Pydantic v2 model to assess and score a completed code generation trajectory."""
    model_config = ConfigDict(extra="forbid")

    trajectory_id: str = Field(..., description="Unique transaction/trajectory identifier")
    metrics: TrajectoryMetric = Field(..., description="The objective metrics achieved by the generation run")
    satisfaction_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Final satisfaction score between 0.0 and 1.0")

    @field_validator("satisfaction_score")
    @classmethod
    def calculate_satisfaction(cls, score: float, info) -> float:
        """Enforces matching score boundaries based on trajectory code metrics."""
        metrics: Optional[TrajectoryMetric] = info.data.get("metrics")
        if metrics:
            calculated = (metrics.test_coverage / 100.0) * (metrics.pylint_score / 10.0)
            if metrics.vulnerabilities_found > 0:
                calculated *= 0.1 # penalize heavily for security concerns
            if metrics.cyclomatic_complexity_delta > 10:
                calculated *= 0.8 # penalize for unnecessary branching

            calculated = max(0.0, min(1.0, calculated))
            return round(calculated, 4)
        return score

# Example Execution & Verification
if __name__ == "__main__":
    payload = {
        "trajectory_id": "tx_9821",
        "metrics": {
            "test_coverage": 98.5,
            "pylint_score": 9.2,
            "vulnerabilities_found": 0,
            "cyclomatic_complexity_delta": 2
        }
    }

    try:
        eval_result = SatisfactionEvaluation.model_validate(payload)
        print(f"Validation Successful for Trajectory: {eval_result.trajectory_id}")
        print(f"Computed Satisfaction Score: {eval_result.satisfaction_score}")
        if eval_result.satisfaction_score >= 0.90:
            print("Action: Approved for Production Merge.")
        else:
            print("Action: Rejected. Requesting Code Regeneration.")
    except ValidationError as e:
        print(f"Validation Error: {e.json(indent=2)}")
```

## Production Hardening & Operational Safety

### Container Hardening & Rootless Execution
Autonomous code execution must strictly occur inside disposable, non-root micro-containers to isolate network resources and host file systems:

```dockerfile
FROM alpine:3.20
RUN adduser -D -u 10001 factoryrunner
USER factoryrunner
WORKDIR /home/factoryrunner
# Read-only root filesystem with temporal tmpfs scratch disk
```

### Maximum Iteration & Token Hard-Caps
To prevent endless recursive self-healing loops when an agent encounters unresolvable logical contradictions, set hard ceilings on both iteration count and token budget:

```python
MAX_FACTORY_ITERATIONS = 5
MAX_FACTORY_TOKENS = 150_000

def enforce_factory_limits(current_iter: int, total_tokens: int):
    if current_iter >= MAX_FACTORY_ITERATIONS:
        raise RuntimeError("Factory execution terminated: Maximum iteration threshold exceeded.")
    if total_tokens >= MAX_FACTORY_TOKENS:
        raise RuntimeError("Factory execution terminated: Token spending cap reached.")
```

## Troubleshooting & Common Issues

| Issue / Failure | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| **Infinite Loop on Flaky Tests** | Non-deterministic test harness failing intermittently. | Ensure test suite relies on deterministic mocks or freeze time/RNG seeds in validation harness. |
| **AST Parse Errors in Seed Ingestion** | Syntax errors present in generated gene-transfusion targets. | Run an initial tree-sitter or AST static syntax check before executing full integration suites. |
| **Docker Out-Of-Memory (OOM)** | Parallel validation runners overwhelming host RAM. | Enforce strictly bounded cgroup memory limits (`--memory=2g`) per factory runner node. |
| **Low Satisfaction Convergence** | Under-specified seed prompt or missing target environment context. | Enrich the seed prompt with dynamic RAG context from production architectural schemas. |
| **Sandbox Network Escape Attempt** | Agent binary attempted external outbound connection during validation | Verify Docker network is bound to `internal: true` or disconnected `--net=none`. |
| **Token Budget Overrun** | Recursive self-healing loop caught in oscillating lint fixes | Trigger early exit after 3 repeated identical AST error hashes. |

## Related tools / concepts
- [Prompt Requests](prompt_requests.md) — Post-PR development workflows.
- [Jules](../../tools/ai_knowledge/jules.md) — The primary autonomous coding agent.
- [MCP 3.1](../../tools/automation_orchestration/mcp.md) — The protocol for agent-tool interaction.
- [Agentic Flows](../../architecture/flows.md) — The underlying workflow patterns.
- [LLM Security and Privacy](../llm_security_privacy.md) — Sandbox security.
- [Qwen 3.6 Coder](../../tools/ai_knowledge/qwen.md) — Local coding models.
- [Docker](../../tools/infrastructure/docker.md) — Isolation for factory harnesses.
- [n8n](../../services/n8n.md) — Factory orchestration workflows.
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md) — Automated data engineering.

## Sources / references
- [Simon Willison on Software Factories](https://simonwillison.net/2026/Feb/7/software-factory/)
- [StrongDM Software Factory Principles](https://factory.strongdm.ai/principles)
- [Notion: Token Town & The Software Factory Future](https://www.latent.space/p/notion)
- [Deloitte Tech Trends 2026: The Agentic Reality Check](https://www.deloitte.com/us/en/insights/topics/technology-management/tech-trends.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
