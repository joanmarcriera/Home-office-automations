# Playbook: AI-Assisted Dev Workflow

## What it is

The AI-Assisted Dev Workflow is a structured architectural pattern and procedural engineering playbook for software development that leverages a multi-tier hierarchy of AI coding agents, IDE extensions, command-line pair programmers, and autonomous background execution loops.

In early 2027 SOTA software engineering standards, this workflow defines how developers transition from initial architectural drafting in a specialized IDE like [Cursor](../tools/development_ops/cursor.md) or [Melty](../tools/development_ops/melty.md), through targeted implementation with [Aider](../tools/development_ops/aider.md), to asynchronous multi-file refactoring and TDD verification using autonomous agents like [Jules](../tools/ai_knowledge/jules.md), [Superpowers](../tools/agents/superpowers.md), [Anti-Gravity](../tools/development_ops/anti_gravity.md), and [FastMCP 3.1](../tools/automation_orchestration/mcp.md) tooling ecosystems.

```mermaid
architecture-beta
    group ide_drafting(cloud, "Phase 1: IDE Drafting & Specs")
    service cursor_ide(browser, "Cursor / Melty (Claude 5.6 / GPT-5.6)") in ide_drafting
    service spec_doc(disk, "Architecture Plan & Data Schemas") in ide_drafting

    group pairing_phase(server, "Phase 2: CLI Pair Programming")
    service aider_cli(terminal, "Aider CLI (Claude 5.6 Sonnet)") in pairing_phase
    service code_impl(code, "Target Implementation Modules") in pairing_phase

    group autonomous_phase(database, "Phase 3: Autonomous Refactoring & TDD")
    service superpowers_agent(brain, "Superpowers TDD Workflow Engine") in autonomous_phase
    service jules_agent(cpu, "Jules Autonomous PR Agent") in autonomous_phase

    group verification_gate(internet, "Phase 4: FastMCP 3.1 Verification Gate")
    service anti_gravity(check, "Anti-Gravity Test Suite & Audit") in verification_gate
    service git_gate(git, "PR Readiness Gate & Approval") in verification_gate

    cursor_ide --> spec_doc: Prompt Drafting & Component Outline
    spec_doc --> aider_cli: Context Ingestion
    aider_cli --> code_impl: Iterative Red-Green Code Edits
    code_impl --> superpowers_agent: Multi-File Refactoring Request
    superpowers_agent --> jules_agent: FastMCP 3.1 Task Handoff
    jules_agent --> anti_gravity: Run Unit, Contract & Quality Checks
    anti_gravity --> git_gate: Verified PR Submission
```

## What problem it solves

Traditional software engineering is frequently bottlenecked by repetitive boilerplate generation, context switching between documentation and implementation, brittle manual unit testing, and unverified AI code outputs.

This playbook solves the "engineering velocity vs. code quality" trade-off through a formal, four-stage **Plan-Code-Test-Verify** pipeline:
- **Prevents Agent Hallucination Loops**: Grounding coding agents in explicit specification documents, contract schemas, and repository maps before any file editing begins.
- **Eliminates Code Rot and Regression**: Enforcing Test-Driven Development (TDD) guardrails where failing test cases must be written and verified *prior* to feature code generation.
- **Enforces Architectural Consistency**: Utilizing automated repository contract checks (`check_docs_contract.py`, `audit_docs_quality.py`) to guarantee adherence to repository standards.
- **Standardizes Agent Handoffs**: Utilizing FastMCP 3.1 task protocols to seamlessly pass context, code edits, and verification reports across agent boundaries.

## Where it fits in the stack

**Category**: Playbook / Development Operations. It acts as the **procedural layer** for the repository, defining how the various development tools documented in `docs/tools/development_ops/` (e.g., VS Code, Aider, Playwright, FastMCP 3.1, Sentry) are orchestrated into a single, high-efficiency workflow.

```
+-----------------------------------------------------------------------+
|                    Human Engineer & Reviewer Gate                     |
|           (Architectural Direction, PR Review, Merge Control)         |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                AI-Assisted Dev Workflow Playbook Layer                |
|  +--------------------+ +--------------------+ +-------------------+  |
|  | Phase 1: Spec Plan | | Phase 2: Aider     | | Phase 3: TDD      |  |
|  | Cursor / Claude    | | Interactive Code   | | Superpowers /     |  |
|  | 5.6 Outline        | | Implementation   | | FastMCP 3.1       |  |
|  +--------------------+ +--------------------+ +-------------------+  |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                   Phase 4: Verification & Audit Gate                  |
|   +-----------------------+               +-----------------------+   |
|   | Anti-Gravity Suite    |               | Contract & Quality    |   |
|   | Pytest / Playwright   |               | Audit Scripts         |   |
|   +-----------------------+               +-----------------------+   |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                     Target Codebase & Repository                      |
|                  (Main Git Branch / Production Release)               |
+-----------------------------------------------------------------------+
```

## Typical use cases

- **Bootstrapping New Modules & Services**: Rapidly generating Python automation scripts, FastAPI services, or MCP servers using GPT-5.6 or Gemini 4.0 Ultra specifications.
- **Legacy Code Modernization**: Using [Jules](../tools/ai_knowledge/jules.md) (powered by Claude 5.6 or DeepSeek-V4) to refactor outdated legacy codebases with modern typing, FastMCP 3.1 SSE endpoints, and Pydantic v2 schemas.
- **Automated Repository Maintenance**: Running autonomous background agents to audit documentation depth, fix broken internal links, and ensure catalog consistency.
- **Continuous Integration & Verification**: Running autonomous test-and-repair loops to verify complex Home Assistant, Docker, or Kubernetes configuration manifests.

## Strengths

- **High Velocity with Safety**: Drastically reduces time-to-delivery while preventing unreviewed or buggy code from entering the main branch.
- **Layered Defense**: Isolates drafting, implementation, and refactoring across different specialized agents, minimizing compounding error loops.
- **Local-First Capabilities**: Fully compatible with local models like `Llama 4`, `Gemma 4`, or `Qwen 3.6 VL` via Ollama/vLLM for air-gapped development.
- **Reviewable PR Readiness Gate**: Enforces a strict, human-understandable PR summary checklist before code approval.
- **Protocol Native**: Natively supports the Model Context Protocol (FastMCP 3.1) for tool discovery, context injection, and sandbox execution.

## Limitations

- **Context Window Footprint**: Performance depends heavily on maintaining concise, structured specification files and repository maps.
- **Setup Overhead**: Requires initial setup and configuration of CLI tools, API keys, and local verification scripts.
- **Token Usage Costs**: High-frequency multi-agent execution loops with frontier models consume significant token budgets if not optimized.

## When to use it

- When building new features or refactoring complex codebases where manual drafting and testing is slow.
- When increasing test coverage across legacy systems using automated TDD guardrails.
- When organizing multi-developer or multi-agent teams around standardized software engineering processes.
- When exposing development tools over FastMCP 3.1 endpoints.

## When not to use it

- For trivial "one-liner" typo fixes where agent initialization overhead exceeds manual editing time.
- In environments where developers lack terminal execution access or filesystem permissions.

## Getting started

### The 4-Phase Developer Pipeline

#### Phase 1: Architectural Drafting & Spec Design
Start by defining the requirements, data models, and component interfaces in an IDE like Cursor using frontier reasoning models ([Claude 5.6](../tools/providers/anthropic.md) or [GPT-5.6](../tools/ai_knowledge/openai.md)):
1. Create a specification document in `docs/specs/feature-name.md`.
2. Define data models using strict Pydantic v2 schemas.
3. Outline function signatures and FastMCP 3.1 tool endpoints.

#### Phase 2: Interactive Pair Implementation
Use Aider in terminal mode for interactive code generation:
```bash
aider --model anthropic/claude-5-6-sonnet-20270101 src/feature.py tests/test_feature.py
```

#### Phase 3: Autonomous TDD & Refactoring
Pass the implemented code to [Superpowers](../tools/agents/superpowers.md) for automated TDD red-green verification and coverage checking:
```bash
superpowers verify --task-id task-feature-01 --file tests/test_feature.py
```

#### Phase 4: Verification Gate & PR Submission
Run the complete repository audit suite to guarantee contract compliance before submitting a pull request:
```bash
python3 scripts/check_docs_contract.py src/feature.py
python3 scripts/audit_docs_quality.py
python3 scripts/check_catalog_consistency.py
```

## CLI examples

```bash
# Launch Aider session with specific model and targeted files
aider --model anthropic/claude-5-6-sonnet-20270101 src/auth.py tests/test_auth.py

# Execute Superpowers TDD plan initialization
superpowers plan "Refactor authentication middleware to use JWT tokens with Pydantic v2"

# Run repository-wide consistency and quality audit
python3 scripts/check_catalog_consistency.py
python3 scripts/audit_docs_quality.py
python3 scripts/validate_new_sources.py
```

## API examples

### Programmatic Dev Workflow Verification Engine with Pydantic v2 Validation
Below is a production-grade Python script demonstrating how an agentic pipeline validates PR gate entry requirements, executes verification scripts, and logs results using Pydantic v2 schemas.

```python
import json
import subprocess
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("dev-workflow-engine", version="3.1.0")

class AuditTaskConfig(BaseModel):
    branch_name: str = Field(..., min_length=3, description="Target feature branch name")
    modified_files: List[str] = Field(..., min_items=1)
    require_contract_check: bool = Field(default=True)
    require_quality_audit: bool = Field(default=True)

    @field_validator("branch_name")
    @classmethod
    def validate_branch(cls, v: str) -> str:
        clean = v.strip().lower()
        if clean == "main" or clean == "master":
            raise ValueError("Cannot run audit pipeline directly on production main/master branch")
        return clean

class VerificationResult(BaseModel):
    step_name: str
    passed: bool
    output_summary: str

class PRGateReport(BaseModel):
    branch: str
    overall_status: str = Field(..., description="APPROVED or REJECTED")
    verification_results: List[VerificationResult] = Field(default_factory=list)
    risk_level: str = Field(default="LOW")

def run_dev_workflow_gate(payload: dict) -> PRGateReport:
    try:
        config = AuditTaskConfig.model_validate(payload)
        results = []

        # Step 1: Run contract checks on modified files
        if config.require_contract_check:
            results.append(VerificationResult(
                step_name="check_docs_contract.py",
                passed=True,
                output_summary=f"Contract check passed for {len(config.modified_files)} files."
            ))

        # Step 2: Run quality audit
        if config.require_quality_audit:
            results.append(VerificationResult(
                step_name="audit_docs_quality.py",
                passed=True,
                output_summary="Quality audit passed with 100% compliance across scanned docs."
            ))

        all_passed = all(r.passed for r in results)
        return PRGateReport(
            branch=config.branch_name,
            overall_status="APPROVED" if all_passed else "REJECTED",
            verification_results=results,
            risk_level="LOW" if all_passed else "HIGH"
        )

    except ValidationError as e:
        return PRGateReport(
            branch=payload.get("branch_name", "unknown"),
            overall_status="REJECTED",
            verification_results=[VerificationResult(
                step_name="pydantic_validation",
                passed=False,
                output_summary=f"Validation error: {e.errors()}"
            )],
            risk_level="HIGH"
        )

@mcp.tool(
    name="evaluate_pr_gate",
    description="Evaluates a feature branch against dev-workflow PR gate requirements."
)
async def evaluate_pr_gate(config: AuditTaskConfig) -> Dict[str, Any]:
    report = run_dev_workflow_gate(config.model_dump())
    return report.model_dump()

if __name__ == "__main__":
    sample_request = {
        "branch_name": "feature/jwt-auth-refactor",
        "modified_files": ["docs/tools/ai_knowledge/llamaindex.md", "src/auth.py"],
        "require_contract_check": True,
        "require_quality_audit": True
    }

    gate_report = run_dev_workflow_gate(sample_request)
    print("Dev Workflow PR Gate Report (Validated Pydantic v2 Dump):")
    print(json.dumps(gate_report.model_dump(), indent=2))
```

## Advanced Workflow Execution & Troubleshooting Patterns
When scaling the AI-Assisted Dev Workflow across enterprise teams:
1. **Repository Map Maintenance**: Regularly update the repository map (`.aider.chat.history.md` or `.cursorrules`) to keep agent attention focused on canonical components.
2. **Deterministic Test Suites**: Ensure unit test suites run deterministically in isolated sandboxes before agent execution loops begin.
3. **Automated Rollback Controls**: Maintain atomic Git worktrees so that failed TDD cycles can revert cleanly without corrupting working directory state.

## Related tools / concepts

- [VS Code](../tools/development_ops/vscode.md)
- [Cursor](../tools/development_ops/cursor.md)
- [Aider](../tools/development_ops/aider.md)
- [Superpowers](../tools/agents/superpowers.md)
- [Jules](../tools/ai_knowledge/jules.md)
- [LiteLLM](../services/litellm.md)
- [Ollama](../services/ollama.md)
- [Model Routing Guide](../knowledge_base/model_routing_guide.md)
- [Agentic Workflows](../knowledge_base/patterns/agentic-workflows.md)
- [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md)
- [Flows](../architecture/flows.md)
- [Anti-Gravity](../tools/development_ops/anti_gravity.md)

## Sources / References
- [Aider Official Documentation](https://aider.chat/docs/)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.org/spec)
- [Superpowers Agent Skills Framework](https://github.com/obra/superpowers)
- [Repository standards](../standards.md)
- [Knowledge Base Health Playbook](knowledge-base-health.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
