# Software Factories Pattern

An architectural pattern for high-autonomy, non-interactive software engineering where agents spec, code, and verify work through rigorous validation harnesses as of early January 2027.

## What it is
The Software Factory is a "dark factory" approach to development where autonomous agents (Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, [Gemma 3](../../tools/ai_knowledge/local_llms.md), [Llama 4](../../tools/ai_knowledge/local_llms.md)) operate within closed-loop environments. It shifts the human role from writing code to defining the "seeds" (specifications) and "validation harnesses" (test scenarios), treating code generation as a high-volume, low-marginal-cost industrial process using **AI-native software assembly** with the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1**.

## What problem it solves
It eliminates the human review bottleneck in traditional PR workflows and mitigates "inhuman mistakes" through exhaustive automated validation. It addresses the economic challenge of building and maintaining complex digital twins, legacy system migrations, and specialized tooling that was previously too expensive for manual development.

## Where it fits in the stack
The Software Factory resides in the **Orchestration and Quality Layer** of the [Home-Office Architecture](../../architecture/README.md). It serves as the primary engine for [Jules](../../tools/ai_knowledge/jules.md) and other coding agents, utilizing **MCP 3.1** (with **FastMCP 3.1** for low-latency tool hosting) for tool-use and [Docker](../../tools/infrastructure/docker.md) for isolated validation environments.

## Typical use cases
- **Autonomous Maintenance**: Agents that monitor, debug, and patch production codebases without human intervention.
- **Gene Transfusion**: Automatically porting legacy business logic from monolithic architectures to modern microservices or agent-native platforms.
- **Digital Twin Development**: Generating high-fidelity mocks of external SaaS services (Okta, Jira, Slack) for safe, high-volume stress testing.
- **Documentation as Code**: Maintaining perfectly synced technical documentation by having agents update docs whenever a code change is validated.
- **Automated Validation Ingestion**: Programmatically parsing and validating incoming factory seeds using strong schema guarantees.

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
```

## API examples

### Factory Validation Request (MCP 3.1 Task Protocol)
Example of an agent requesting a validation run within the software factory using the **MCP 3.1 Task Protocol**.

```json
{
  "mcp_version": "3.1",
  "method": "tasks/run",
  "params": {
    "task_id": "factory_run_validation",
    "input": {
      "code_path": "/src/auth_handler.go",
      "test_harness": "security_scan_v4",
      "max_iterations": 5,
      "stop_on_satisfaction": true
    }
  }
}
```

### Satisfaction-Based Scoring API (Python & Pydantic v2)
The following Python script illustrates how satisfaction-based evaluations are structured, verified, and parsed using modern Pydantic v2.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class TrajectoryMetric(BaseModel):
    """Evaluation metrics for an agent's code generation run in the factory."""
    test_coverage: float = Field(..., ge=0.0, le=100.0, description="Percentage of test coverage")
    pylint_score: float = Field(..., ge=0.0, le=10.0, description="Pylint static code quality score")
    vulnerabilities_found: int = Field(default=0, ge=0, description="Number of security issues identified")

class SatisfactionEvaluation(BaseModel):
    """Pydantic v2 model to assess and score a completed code generation trajectory."""
    trajectory_id: str = Field(..., description="Unique transaction/trajectory identifier")
    metrics: TrajectoryMetric = Field(..., description="The objective metrics achieved by the generation run")
    satisfaction_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Final satisfaction score between 0.0 and 1.0")

    @field_validator("satisfaction_score")
    @classmethod
    def calculate_satisfaction(cls, score: float, info) -> float:
        """Enforces matching score boundaries based on trajectory code metrics."""
        metrics: Optional[TrajectoryMetric] = info.data.get("metrics")
        if metrics:
            # Logic: If high test coverage, high pylint score, and 0 vulnerabilities -> high satisfaction score
            calculated = (metrics.test_coverage / 100.0) * (metrics.pylint_score / 10.0)
            if metrics.vulnerabilities_found > 0:
                calculated *= 0.1 # penalize heavily for security concerns

            # Bound check
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
            "vulnerabilities_found": 0
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
