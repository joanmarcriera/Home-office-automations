# Prompt Requests: Post-PR Development Workflows

This document outlines the transition from traditional Git-based "Pull Requests" to agent-centric "Prompt Requests" and reputation-based systems for post-human development as of late October / November 2026.

## What it is

The "RIP Pull Requests (2005-2026)" analysis highlights a fundamental shift in software engineering. As AI agents (Claude 5.1, GPT-5.5, Gemini 4.0, [Gemma 3](../../tools/ai_knowledge/local_llms.md), [Llama 4](../../tools/ai_knowledge/local_llms.md)) handle an increasing percentage of code generation and modification, traditional human-centric collaboration tools like Pull Requests (PRs) and Code Reviews are being superseded by workflows optimized for speed, safety, and agentic autonomy through **Agentic Prompt Engineering** under **MCP 3.1** standards.

A **Prompt Request** is a structured specification of intent that an agent uses to generate, validate, and merge code independently. This pattern often involves **Agent-to-Agent Collaboration**, where stateless orchestrators operate in stateful, durable workspaces (e.g., OpenAI Agents SDK, Cloudflare Project Think), using files as the primary communication medium ("File-as-Bus").

## What problem it solves

- **The Human Bottleneck**: Traditional PRs require human review, which is slow compared to the speed at which agents can generate code.
- **Merge Conflicts**: Agent-generated code often drifts from the main branch; Prompt Requests focus on the *intent* (the prompt), allowing the agent to regenerate against the latest main branch.
- **Spec-Code Divergence**: Ensures the source of truth is the high-level specification or prompt, not just the resulting lines of code.
- **Scale**: Enables "Federated KnowledgeOps" where thousands of specialized agents can contribute to a codebase simultaneously without overloading human maintainers.

## Where it fits in the stack

**Workflow Pattern**. Operates at the **Development / CI layer**. It replaces or augments the standard GitHub Flow (branch -> commit -> PR -> merge) with an **Agentic Flow** (spec/prompt -> agent execution -> validation -> reputation-based auto-merge). It utilizes the **Model Context Protocol (MCP 3.1)** (leveraging **FastMCP 3.1** for low-latency tool hosting and **MCP 3.1 Task Protocol** for standardized execution) for tool discovery and execution.

## Typical use cases

- **Automated Bug Fixing**: Providing a stack trace and asking an agent to "fix this and update the test suite."
- **Feature Expansion**: Adding a new API endpoint based on an existing schema and pattern.
- **Large-scale Refactoring**: Migrating a codebase from one library version to another by updating the global "coding standards" prompt.
- **Reputation-Based Auto-Merging**: Utilizing systems where code contributions are evaluated based on the submitter's historical reliability and automated safety checks, rather than manual line-by-line review.
- **Structured Specification Validation**: Ensuring that prompt request files committed to repository control strictly follow secure schema boundaries.

## Strengths

- **High Architectural Alignment**: Agents follow the provided prompt strictly, ensuring consistency across a large codebase.
- **Reduced Human Labor**: Removes the need for line-by-line review for boilerplate or standard tasks.
- **Durable Intent**: The "Prompt Request" serves as documentation for *why* a change was made, often more clearly than a commit message.
- **Security-First Intent**: It is harder to slip malicious code into a prompt modification than into an innocent-looking 1,000-line PR.
- **Lethal Trifecta Mitigation**: Incorporates guardrails to prevent the combination of code execution, network access, and credential leakage.

## Limitations

- **Spec Fidelity**: Requires extremely clear and high-quality prompts/specifications to avoid "hallucinated" features.
- **Sandboxing Requirements**: Demands robust, isolated execution environments (like E2B or Modal) for all agentic code execution.
- **Reputation Complexity**: Building a reliable system to "trust" agent output without human eyes is technically challenging.
- **Context Windows**: Extremely large codebase changes still face context window limitations, requiring RAG or partitioned processing.

## When to use it

- For **boilerplate-heavy tasks** or repetitive pattern application.
- When working in **sandboxed environments** where automated tests provide 100% coverage confidence.
- In **high-velocity teams** where humans focus on architecture and agents focus on implementation.
- For **standardized migrations** (e.g., upgrading a library across 50 microservices).

## When not to use it

- **Critical Security Kernels**: Any code where a single logic error could lead to a major breach still requires human "Deep Review".
- **Ambiguous UI/UX Polish**: Tasks requiring subjective human aesthetic judgment.
- **Low Test Coverage**: If you cannot prove the code is correct via automation, do not use autonomous Prompt Requests.

## Getting started

To implement Prompt Requests in your workflow, you need an agentic runner capable of interpreting specifications and executing tools.

1.  **Install an Agentic CLI**: Use a tool like `claude-code` or `openclaw` which supports MCP 3.1.
2.  **Define a Template**: Create a `.prompt-request` directory in your repo to store structured JSON/YAML templates.
3.  **Setup Sandboxing**: Configure an environment like Docker or E2B to run the agent's proposed changes safely.
4.  **Integrate CI**: Add a step in your GitHub Actions or GitLab CI to trigger agent runs when a new `.pr.yaml` file is committed to a `prompts/` branch.

## CLI examples

Submitting a prompt request using a hypothetical `jules` CLI tool (representing the agentic reviewer pattern):

```bash
# Create a new prompt request from a natural language description
jules prompt "Add PII masking to UserProfile logging in src/users/profile.py" \
  --context "docs/playbooks/data-copilot-sql-validation.md" \
  --test "pytest tests/test_profile_masking.py"

# Execute a pending prompt request from a YAML file
jules execute ./prompts/PR-2026-0528.yaml --sandbox docker

# Check the reputation of an agent before auto-merging its output
jules reputation check agent-alpha-7
```

## API examples

### Submitting a Prompt Request via MCP 3.1
Using the **MCP 3.1 Task Protocol** to programmatically trigger a Prompt Request via an orchestrator:

```python
import mcp.client

async def submit_prompt_request():
    async with mcp.client.connect("https://mcp-server.internal") as client:
        # Register the prompt request using the tasks/run method
        response = await client.call_tool(
            "tasks/run",
            arguments={
                "task_id": "PR-2026-0620",
                "input": {
                    "intent": "Refactor legacy axios calls to fetch API in TriliumNext",
                    "constraints": ["No external dependencies", "Maintain TS types"],
                    "verification_suites": ["npm test", "npm run lint"]
                }
            }
        )
        print(f"Prompt Request submitted: {response['status']}")

# Trigger the refactoring agent
await submit_prompt_request()
```

### Prompt Request YAML Validation Schema (Python & Pydantic v2)
The following Python implementation provides strict validation of the Prompt Request YAML structure, verifying execution constraints and sandboxing properties using modern Pydantic v2.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class PromptRequestPayload(BaseModel):
    """Pydantic v2 model to validate incoming Prompt Requests for agentic development."""
    request_id: str = Field(..., alias="id", description="Unique prompt request identifier")
    intent: str = Field(..., description="High-level specification of the code change intent")
    context_files: List[str] = Field(..., alias="context", description="List of file paths representing code context")
    constraints: List[str] = Field(default_factory=list, description="Mandatory architectural or security constraints")
    verification_commands: List[str] = Field(..., alias="verification", description="List of testing/verification commands to run")

    @field_validator("verification_commands")
    @classmethod
    def validate_safety_of_commands(cls, commands: List[str]) -> List[str]:
        """Ensures testing and verification commands do not contain malicious shell operators."""
        blacklisted_operators = [";", "&&", "||", "|", "`", "$("]
        for cmd in commands:
            if any(op in cmd for op in blacklisted_operators):
                raise ValueError(
                    f"Command '{cmd}' contains illegal shell operators or chaining symbols. "
                    f"Commands must be run sequentially in clean arrays."
                )
        return commands

# Example Execution & Verification
if __name__ == "__main__":
    payload = {
        "id": "PR-2026-0528",
        "intent": "Add PII masking to the UserProfile logging module.",
        "context": [
            "src/users/profile.py",
            "docs/playbooks/data-copilot-sql-validation.md"
        ],
        "constraints": [
            "No external dependencies.",
            "Maintain 100% test coverage."
        ],
        "verification": [
            "pytest tests/test_profile_masking.py" # Safe, simple execution
        ]
    }

    try:
        validated_pr = PromptRequestPayload.model_validate(payload)
        print(f"Prompt Request '{validated_pr.request_id}' verified successfully!")
        print(f"Verified Intent: {validated_pr.intent}")
    except ValidationError as e:
        print(f"Validation Error: {e.json(indent=2)}")
```

### YAML Schema Structure
A "Prompt Request" often takes the form of a structured JSON or YAML file that defines the intent, allowing different agents to attempt the implementation.

```yaml
# prompts/PR-2026-0528.yaml
prompt_request:
  id: "PR-2026-0528"
  intent: "Add PII masking to the UserProfile logging module."
  context:
    - path: "src/users/profile.py"
    - pattern: "docs/playbooks/data-copilot-sql-validation.md"
  constraints:
    - "No external dependencies."
    - "Maintain 100% test coverage."
    - "Pass Claude Code security scan."
  verification:
    - command: "pytest tests/test_profile_masking.py"
    - tool: "scripts/sql_validator.py"
```

## Related tools / concepts

- [Agentic Workflows](agentic-workflows.md) — The broader framework for agent-led development.
- [Software Factories](software-factories.md) — The architectural pattern for non-interactive code convergence.
- [Claude Code](../../tools/development_ops/claude-code.md) — Terminal-based agent that implements Prompt Request patterns.
- [OpenClaw](../../tools/development_ops/openclaw.md) — Runtime for executing agentic prompts and MCP tools.
- [Devin](../../tools/development_ops/devin.md) — Autonomous agent capable of handling end-to-end development tasks.
- [Aider](../../tools/development_ops/aider.md) — CLI tool for pair-programming with LLMs.
- [Plandex](../../tools/development_ops/plandex.md) — AI coding engine for complex, multi-file tasks.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — Coordination protocol for agentic contributions.

## Sources / References
- [[AINews] RIP Pull Requests (2005-2026) (Latent Space)](https://www.latent.space/p/ainews-rip-pull-requests-2005-2026)
- [The Rise of the Prompt Request (Mitchell Hashimoto)](https://mitchellh.com/writing/prompt-requests)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2026-11-20
- Confidence: high
