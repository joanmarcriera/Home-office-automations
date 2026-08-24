# Prompt Requests: Post-PR Development Workflows

This document outlines the transition from traditional Git-based "Pull Requests" to agent-centric "Prompt Requests" and reputation-based auto-convergence workflows in early 2027 software engineering environments.

## What it is

The evolution from traditional human Pull Requests (PRs) toward agentic "Prompt Requests" represents a core shift in software delivery pipelines. As autonomous AI agents (Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, Gemma 3, Qwen 3.8) generate, refactor, and verify codebases, traditional line-by-line human code reviews create operational friction. A **Prompt Request** is a machine-readable specification of intent that an autonomous agent uses to execute, test, and validate changes directly against current repository main branches.

Prompt Requests leverage **Agentic Prompt Engineering** and **FastMCP 3.1** protocol interfaces, employing "File-as-Bus" state management and durable sandboxed workspaces (e.g., E2B, Modal, Docker) for autonomous task completion.

## What problem it solves

- **Human Code Review Bottlenecks**: Eliminates developer review backlog when merging high-volume, automated agent code.
- **Git Branch Drift & Merge Conflicts**: Replaces stale feature branches with intent-based prompt specifications that re-evaluate against `main` in real time.
- **Specification vs. Implementation Divergence**: Establishes the high-level intent prompt as the authoritative source of truth rather than transient diffs.
- **Multi-Agent Scale**: Supports federated multi-agent contributions without overloading maintainer workflows.

## Where it fits in the stack

It resides at the **Software Development & CI/CD Layer**. It replaces or enhances traditional feature branching (`git checkout -b -> commit -> PR -> review -> merge`) with an **Agentic Intent Pipeline** (`prompt spec -> FastMCP task runner -> isolated sandbox execution -> automated verification -> reputation auto-merge`).

## Typical use cases

- **Automated Defect Remediation**: Ingesting stack traces or telemetry errors and dispatching autonomous repair prompts.
- **API & Schema Migrations**: Upgrading API contracts across microservices by updating repository prompt specifications.
- **Bulk Codebase Refactoring**: Applying codebase-wide pattern updates (e.g., migrating to FastMCP 3.1 and Pydantic v2 schemas).
- **Reputation-Based Auto-Merging**: Merging code changes automatically when submitters (human or agent) satisfy pass criteria and high reputation scores.

## Strengths

- **Strict Architectural Alignment**: Enforces repository prompt instructions (`AGENTS.md`) across generated code.
- **Reduced Manual Review Friction**: Automates mechanical code review for standard bug fixes and boilerplate updates.
- **Durable Intent Provenance**: Maintains clear historical context on why code modifications were made.
- **Sandbox Security Boundary**: Isolates execution environments to mitigate untrusted code execution risks.

## Limitations

- **Specification Fidelity**: Demands unambiguous prompt definitions to avoid hallucinated implementation logic.
- **Sandboxing Overhead**: Requires secure, isolated runtime environments (E2B, Modal) for agent code compilation and execution.
- **Reputation Scoring Complexity**: Demands calibrated evaluation metrics before delegating zero-human auto-merge permissions.

## When to use it

- For structured refactoring, dependency upgrades, and repetitive pattern applications.
- In environments backed by comprehensive test suites (>=90% coverage) and automated validation scripts.
- In multi-agent software engineering pipelines.

## When not to use it

- For security-critical cryptographic or auth kernel modifications requiring human safety audits.
- For open-ended subjective UI/UX design changes.
- In codebases lacking automated test suites.

## Getting started

### 1. Define Prompt Request Schemas
Establish a `.prompt-requests/` directory containing JSON or YAML intent templates.

### 2. Configure Agent Sandbox Runner
Ensure an agent runner (e.g., Claude Code, OpenClaw) is connected to a secure runtime environment with FastMCP 3.1 support.

### 3. Integrate CI Auto-Verification
Add CI workflows that validate incoming `.prompt-request.yaml` payloads using Pydantic v2 validation scripts.

## CLI examples

### Submitting & Executing Prompt Requests
```bash
# Submit a prompt request for automated refactoring
fastmcp prompt-request submit --spec ./prompts/PR-2027-0107.yaml --sandbox docker

# Verify agent execution status
fastmcp task status --task-id PR-2027-0107
```

## API examples

### Programmatic Prompt Request Validation (Python & Pydantic v2)
This script validates Prompt Request YAML payloads against FastMCP 3.1 execution safety rules using Pydantic v2:

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class PromptRequestPayload(BaseModel):
    """Pydantic v2 model for validating Prompt Request specifications."""
    request_id: str = Field(..., alias="id", description="Unique Prompt Request identifier.")
    intent: str = Field(..., description="High-level specification of code change intent.")
    context_files: List[str] = Field(..., alias="context", description="List of context files.")
    constraints: List[str] = Field(default_factory=list, description="Architectural or security constraints.")
    verification_commands: List[str] = Field(..., alias="verification", description="Testing/verification commands.")

    @field_validator("verification_commands")
    @classmethod
    def validate_command_safety(cls, commands: List[str]) -> List[str]:
        """Enforce strict command isolation to prevent shell injection."""
        forbidden_tokens = [";", "&&", "||", "|", "`", "$("]
        for cmd in commands:
            if any(token in cmd for token in forbidden_tokens):
                raise ValueError(f"Unsafe command detected: '{cmd}'. Commands must be separate array items.")
        return commands

# Example Verification Usage
if __name__ == "__main__":
    payload = {
        "id": "PR-2027-0107",
        "intent": "Upgrade API handlers to FastMCP 3.1 specification with Pydantic v2 schemas.",
        "context": [
            "docs/knowledge_base/patterns/data-copilot-mcp-tooling.md"
        ],
        "constraints": [
            "Maintain 100% test pass rate.",
            "Enforce strict type annotations."
        ],
        "verification": [
            "pytest tests/test_mcp_tooling.py"
        ]
    }

    try:
        validated_pr = PromptRequestPayload.model_validate(payload)
        print(f"Validated Prompt Request ID: {validated_pr.request_id}")
        print(f"Intent: {validated_pr.intent}")
    except ValidationError as err:
        print(f"Validation Error: {err.json(indent=2)}")
```

### Prompt Request YAML Spec Example
```yaml
# .prompt-requests/PR-2027-0107.yaml
prompt_request:
  id: "PR-2027-0107"
  intent: "Upgrade API endpoints to FastMCP 3.1 and Pydantic v2 validation."
  context:
    - path: "src/api/routes.py"
    - pattern: "docs/knowledge_base/patterns/data-copilot-mcp-tooling.md"
  constraints:
    - "No external unapproved dependencies."
    - "Pass all pre-commit validation checks."
  verification:
    - command: "pytest tests/test_routes.py"
```

## Related tools / concepts
- [Agentic Workflows](agentic-workflows.md) — Multi-agent engineering patterns.
- [Software Factories](software-factories.md) — Automated software construction loops.
- [FastMCP 3.1 Tooling](data-copilot-mcp-tooling.md) — Protocol tool standard.
- [Model Routing Guide](../model_routing_guide.md) — Provider routing framework.

## Sources / References
- [RIP Pull Requests (2005-2026) Analysis](https://www.latent.space/p/ainews-rip-pull-requests-2005-2026)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
