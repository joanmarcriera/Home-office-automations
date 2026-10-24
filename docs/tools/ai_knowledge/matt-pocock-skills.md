# Matt Pocock Skills

## What it is
Matt Pocock Skills is a collection of production-grade agent skills, execution scaffolds, and prompt design tools designed to extend AI developer workflows with domain-specific engineering rigor. Built around flagship patterns such as the "Grill-me" plan verification skill, this framework bridges the gap between raw LLM intelligence and disciplined software engineering practices. As of early 2027, these skills operate natively with **FastMCP 3.1**, the **MCP 3.0 Task Protocol**, and frontier models including **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.

## What problem it solves
Autonomous AI agents frequently suffer from "over-confidence bias"—executing major architectural refactors or database migrations without thoroughly validating edge cases, verifying dependency constraints, or pressure-testing system assumptions. This leads to broken builds, regressions, and costly manual debugging cycles.

Matt Pocock Skills addresses this problem by embedding explicit critical-thinking scaffolds directly into the agent's reasoning loop. Skills like `grill-me` force agents to defend their execution plans against adversarial questioning, while skills like `tdd` enforce strict Red-Green-Refactor test cycles before touching production source code.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Agent Execution Skills & Scaffolds.

```
+-----------------------------------------------------------------------------------+
|                           Matt Pocock Skills Execution Architecture               |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +--------------------+         +-----------------------+                         |
|  | Developer / IDE    | ------> | Skill Trigger         |                         |
|  | Cursor, Claude Code|         | /grill-me, /tdd       |                         |
|  +--------------------+         +-----------+-----------+                         |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | FastMCP 3.1 Server    |                         |
|                                 | Task Dispatch & Schema|                         |
|                                 +-----------+-----------+                         |
|                                             |                                     |
|                        +--------------------+--------------------+                |
|                        |                                         |                |
|                        v                                         v                |
|           +-------------------------+               +-------------------------+   |
|           | Adversarial Interrogator|               | TDD Red-Green Refactor  |   |
|           | Generates probing Qs    |               | Writes failing tests    |   |
|           +------------+------------+               +------------+------------+   |
|                        |                                         |                |
|                        +--------------------+--------------------+                |
|                                             |                                     |
|                                             v                                     |
|                                 +-----------------------+                         |
|                                 | Verified Plan & Code  |                         |
|                                 | Authorized Mutator    |                         |
|                                 +-----------------------+                         |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

Operating at the reasoning and execution layer, these skills inject structured execution guidelines into agent runtimes like [Jules](jules.md) or [Claude Code](../development_ops/claude-code.md).

```
+-----------------------------------------------------------------------------------------------------------+
|                                    Grill-Me Plan Verification Sequence Flow                                |
+-----------------------------------------------------------------------------------------------------------+
|                                                                                                           |
| Developer                Agent Runtime               FastMCP 3.1 Server           Plan Mutator            |
|    |                           |                            |                          |                  |
|    |---- 1. Submit Proposal -->|                            |                          |                  |
|    |                           |---- 2. Request Grilling -->|                          |                  |
|    |                           |                            |-- 3. Evaluate Risk ---->|                  |
|    |                           |<-- 4. Return Questions ----|                          |                  |
|    |<-- 5. Interrogate User ---|                            |                          |                  |
|    |                           |                            |                          |                  |
|    |-- 6. Clarifications ----->|                            |                          |                  |
|    |                           |---- 7. Validate Answers -->|                          |                  |
|    |                           |                            |-- 8. Authorize Plan ---->|                  |
|    |                           |<-- 9. Status: Approved ----|                          |                  |
|    |                           |                            |                          |-- 10. Execute -->|
|                                                                                                           |
+-----------------------------------------------------------------------------------------------------------+
```

## Typical use cases
- **Plan Pressure-Testing (`/grill-me`)**: Requiring agents to answer 3 to 5 challenging architectural questions before executing complex code changes.
- **Strict Test-Driven Development (`/tdd`)**: Forcing agents to write failing unit tests first, verify red status, write minimal implementation, and refactor cleanly.
- **Environment & Dependency Diagnostics (`/diagnose`)**: Uncovering hidden version mismatches, missing system libraries, or environment variables causing build failures.
- **FastMCP 3.1 Agent Extensions**: Binding custom engineering tools to IDE assistants via standardized MCP server interfaces.

## Skill Suite Comparison Matrix

| Skill / Scaffold | Primary Focus | Interaction Pattern | Key Guardrails | Primary Target Models |
| :--- | :--- | :--- | :--- | :--- |
| **`/grill-me`** | Plan pressure-testing & edge case discovery | Multi-turn adversarial Q&A | Block file modifications until plan verification | Claude 5.1, GPT-5.5, Gemini 4.0 Pro |
| **`/tdd`** | Strict Red-Green-Refactor code writing | Automated test-first loop | Mandatory failing test execution before source editing | Claude 5.1, Llama 4 Maverick |
| **`/diagnose`** | Environment & dependency failure triage | System inspection & log reading | Non-mutating read-only analysis | GPT-5.5, DeepSeek-V4 |
| **Karpathy Skills** | Surgical code modification & context minimizer | Direct single-turn code refactor | Minimal diff footprint enforcement | Open-weight 70B models, Gemma 4 |
| **OpenCode Skills** | Full-repository feature generation | Autonomous task loop | Sandbox container execution | Claude Code, Cursor Agent |

## Strengths
- **Enforces Staff Engineer Rigor**: Replaces hasty token generation with deliberate plan verification and boundary testing.
- **Standardized Execution (`skills.sh`)**: Simple single-command installation across diverse terminal environments and IDE plugins.
- **Model Agnostic**: Compatible with all leading reasoning engines (Claude 5.1, GPT-5.5, Gemini 4.0 Pro, DeepSeek-V4).
- **FastMCP 3.1 & Pydantic v2 Native**: Fully integrated with standard structured schemas and agent task protocols.

## Limitations
- **Interaction Overhead**: Requires interactive user input during grilling phases, which is less suited for fully unmonitored background batch runs.
- **Token Consumption**: Detailed multi-step skill scaffolds consume additional context window tokens during initial reasoning phases.

## When to use it
- When making non-trivial modifications to core database schemas, security middleware, or public APIs.
- When practicing strict TDD discipline across TypeScript, Python, or Rust codebases.
- When seeking a standardized way to equip AI agents with reliable engineering workflows.

## When not to use it
- For quick, trivial changes (e.g. fixing a typo or modifying documentation).
- In fully automated background jobs where human feedback cannot be requested during a grill session.

## Getting started

### Installation
Install the skill suite using Node.js (v22+) and the official CLI:

```bash
# Add Matt Pocock Skills to local developer environment
npx skills@latest add mattpocock/skills
```

### Configuration
Add the setup hook to your agent's system prompt or configuration file (`CLAUDE.md` or `.cursorrules`):

```markdown
## Agent Skills Configuration
- Always run `/grill-me` before executing multi-file refactors or schema changes.
- Use `/tdd` for new feature implementations.
```

## CLI examples

```bash
# Trigger interactive plan verification session
/grill-me

# Initialize Test-Driven Development loop for target module
/tdd src/auth/session.ts

# Run diagnostic check on environment and dependencies
/diagnose

# List all active skills
/skills list
```

## API examples

### FastMCP 3.1 Server for Grill-Me Task Interrogation
The Python code below demonstrates a complete **FastMCP 3.1** server that executes the `/grill-me` skill workflow, validating technical plans using **Pydantic v2** models.

```python
import asyncio
import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server for Pocock Skills
mcp = FastMCP(
    name="Matt Pocock Skills Engine",
    version="3.1.0"
)

class PlanGrillRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    proposal_title: str = Field(..., alias="title", min_length=5, description="Title of the technical proposal")
    plan_description: str = Field(..., alias="description", min_length=20, description="Detailed architectural plan")
    target_files: List[str] = Field(default_factory=list, alias="targetFiles", description="Files affected by proposed changes")
    question_depth: int = Field(default=3, alias="questionDepth", ge=1, le=5, description="Depth level of probing questions")

    @field_validator("target_files")
    @classmethod
    def validate_files(cls, files: List[str]) -> List[str]:
        if not files:
            raise ValueError("At least one target file must be specified for plan grilling")
        return files

class GrillQuestion(BaseModel):
    question_id: int
    topic: str
    question_text: str
    risk_level: str = Field(default="medium")

class GrillSessionResult(BaseModel):
    session_id: str
    status: str
    questions: List[GrillQuestion]
    authorized: bool = False
    verification_score: float = Field(default=0.0, ge=0.0, le=100.0)

class GrillResponseEvaluation(BaseModel):
    session_id: str
    answers: Dict[int, str]
    evaluator_comments: Optional[str] = None

@mcp.tool(name="grill_me_plan", description="Interrogates a proposed technical plan using the /grill-me scaffold")
async def grill_me_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Validate payload using Pydantic v2
    request = PlanGrillRequest.model_validate(payload)

    session_id = f"grill-{uuid.uuid4().hex[:8]}"

    # Generate structured interrogation questions based on input scope
    questions = [
        GrillQuestion(
            question_id=1,
            topic="Data Integrity & Rollback",
            question_text=f"How will target files {request.target_files} handle transactional rollback on unexpected exception during schema mutation?",
            risk_level="high"
        ),
        GrillQuestion(
            question_id=2,
            topic="Performance Boundary",
            question_text="What is the expected latency overhead when context size or payload volume grows past threshold?",
            risk_level="medium"
        ),
        GrillQuestion(
            question_id=3,
            topic="Regression Risk",
            question_text="Which automated test suites will be run to ensure zero backward-compatibility regressions occur?",
            risk_level="high"
        )
    ]

    result = GrillSessionResult(
        session_id=session_id,
        status="awaiting_user_clarification",
        questions=questions[:request.question_depth],
        authorized=False,
        verification_score=0.0
    )

    return {
        "status": "success",
        "result": result.model_dump()
    }

@mcp.tool(name="evaluate_grill_answers", description="Evaluates developer answers to grill questions and computes authorization score")
async def evaluate_grill_answers(payload: Dict[str, Any]) -> Dict[str, Any]:
    evaluation = GrillResponseEvaluation.model_validate(payload)

    # Assess completeness of answers provided
    answered_count = len(evaluation.answers)
    score = min(100.0, (answered_count / 3.0) * 100.0)
    authorized = score >= 80.0

    return {
        "session_id": evaluation.session_id,
        "score": score,
        "authorized": authorized,
        "status": "approved" if authorized else "rejected_insufficient_clarification"
    }

if __name__ == "__main__":
    mcp.run()
```

### Systemd Service Unit Configuration

To run the FastMCP 3.1 Pocock Skills engine as a persistent local background daemon (`/etc/systemd/system/pocock-skills.service`):

```ini
[Unit]
Description=FastMCP 3.1 Matt Pocock Skills Agent Engine
After=network.target daemon.service
Wants=network-online.target

[Service]
Type=simple
User=pocock-agent
Group=pocock-agent
WorkingDirectory=/opt/pocock-skills
ExecStart=/usr/bin/python3 -m mcp.server.fastmcp run server.py --port 8092
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=LOG_LEVEL=INFO
Environment=MCP_SERVER_PORT=8092

# System Security & Sandboxing Guardrails
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/pocock-skills/logs /tmp
PrivateTmp=true
NoNewPrivileges=true
CapabilityBoundingSet=

[Install]
WantedBy=multi-user.target
```

## Troubleshooting & Failure Modes

| Failure Mode / Error | Cause | Resolution Strategy |
| :--- | :--- | :--- |
| **Grill Loop Deadlock** | Agent refuses to proceed waiting for human answers in an unattended environment. | Use `--non-interactive` flag or configure automated synthetic answers for CI pipelines. |
| **Over-Engineering Bias** | `/grill-me` generates excessive architectural questions for minor feature changes. | Set `question_depth=1` for minor refactors; enforce strict scope boundaries. |
| **FastMCP Schema Mismatch** | Agent runtime tool payload missing required `targetFiles` alias field. | Use Pydantic v2 `populate_by_name=True` or enforce alias validation in tool wrappers. |
| **Context Window Overflow** | Long `/tdd` test runs accumulate excessive test log output in agent context. | Pipe test output through log filter scripts (`/tdd --quiet`) to preserve context. |
| **Permission Denied Mutator** | Agent attempts file modifications prior to plan verification approval. | Configure IDE system prompts to strictly require `grill_session_result.authorized == True`. |
| **Port Conflict on FastMCP Start** | Port 8092 is occupied by another local agent sidecar process. | Verify active ports via `lsof -i :8092` or change `MCP_SERVER_PORT` in unit configuration. |

## Production Deployment Guardrails

1. **Gatekeeping File Access**: Enforce system prompt rules prohibiting code generation tools from touching files until `/grill-me` returns `authorized: True`.
2. **Context Window Preserving**: Truncate test runner output in `/tdd` loops to only display relevant stack traces and failure assertions.
3. **Automated Interrogation Fallback**: In automated batch mode, feed `/grill-me` questions to an independent reviewer agent (e.g., Gemini 4.0 Ultra) to verify answers autonomously.
4. **Audit Trajectory Logging**: Store all grill questions and developer clarifications in version-controlled markdown reports (`docs/reports/grill-sessions/`).
5. **Tool Scope Enforcement**: Ensure skills only access white-listed directories and cannot run arbitrary shell commands outside test targets.

## Related tools / concepts
- [Andrej Karpathy Skills](karpathy-skills.md) — Surgical code modification patterns.
- [Claude Code](../development_ops/claude-code.md) — Primary IDE runtime for agent skills.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) — Extension ecosystem for agent capabilities.
- [Jules](jules.md) — Specialized coding agent.
- [FastMCP 3.1 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Agent protocol specification.

## Sources / references
- [Matt Pocock Skills GitHub Repository](https://github.com/mattpocock/skills)
- [Total TypeScript - Professional AI Engineering Workflows](https://www.totaltypescript.com/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
