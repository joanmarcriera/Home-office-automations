# Axiom Guardian MCP Server

## What it is
An MCP server that implements challenge-based request validation using Natural Language Inference (NLI) to enforce core principles. Under late November/December 2026 SOTA standards, **Axiom Guardian v1.5** serves as a critical alignment layer for autonomous systems, integrating with the **MCP 3.1 / FastMCP 3.1 Task Protocol** to provide verifiable, challenge-based justification logs for agent actions across frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **Llama 4**, **Gemma 3**, and **Qwen 3.6**.

## What problem it solves
It shifts the AI paradigm from passive compliance ("How can I help you?") to active validation ("Why are you doing this?"). It detects logical contradictions between proposed actions and configured axioms, forcing the user (or agent) to justify their actions. It addresses the "autonomous drift" problem where agents may take increasingly risky actions in pursuit of a high-level goal, ensuring reliable and aligned behavior in any home lab or production deployment.

## Where it fits in the stack
**Tool / Guardrail**. It provides an AI alignment and safety layer for agent actions, fitting between the AI model (like Claude 5.1 or GPT-5.5) and the tools it attempts to execute. It is often deployed as a middleware layer in [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- **AI Safety**: Challenging potentially harmful or destructive requests before execution.
- **Organizational Governance**: Enforcing company values and security policies in automated workflows.
- **Decision Audit Trail**: Forcing articulation of reasoning for high-stakes actions (e.g., production deployments, financial transactions).
- **Educational Tool**: Training users and agents to think through the ethical and operational consequences of their requests.

## Strengths
- **NLI-based validation**: Uses sophisticated models (like BART-MNLI) to detect logical contradictions without requiring rigid regex-based rules.
- **Iterative Dialogue**: Challenges users to justify contradictory actions through a loop, preserving the justification in the session context.
- **MCP 3.1 Native**: Full support for the Task Protocol, allowing challenges to be recorded as discrete, verifiable "Safety Interventions".
- **Dynamic Configuration**: Axioms can be updated at runtime via the `update_axioms` tool.

## Limitations
- **Latency**: NLI mode adds inference latency to the decision loop.
- **English Focus**: Optimal performance is currently achieved with English-language axioms and prompts.
- **Context Windows**: Extremely large action descriptions may be truncated, potentially missing subtle contradictions.
- **Fail-Open Default**: To ensure system availability, it defaults to allowing actions if the NLI API is unreachable.

## When to use it
- When you need to enforce a set of rules or ethical principles on AI agent behavior.
- To create a record of human justification for critical operations.
- When working with high-autonomy agents powered by Claude 5.1 or GPT-5.5 in production environments.
- For compliance-heavy industries (Finance, Healthcare) requiring audit trails for AI actions.

## When not to use it
- For low-stakes environments where active challenging would be unnecessary friction.
- When the action space is already strictly constrained by permission-based RBAC.
- For sub-millisecond real-time control systems where NLI latency is prohibitive.

## Getting started

Axiom Guardian MCP implements a challenge-justification loop to ensure agent actions align with core principles.

### 1. Installation
```bash
pip install axiom-guardian-mcp
```

### 2. Axiom Configuration (`axioms.yaml`)
Define the principles the agent must follow:

```yaml
axioms:
  - "The agent must not delete production data without explicit triple-confirmation."
  - "The agent must prioritize system stability over performance optimizations."
```

### 3. Hello World Test
Run the server locally to verify installation:
```bash
python -m axiom_guardian_mcp --test "Delete the production database"
# Expected output: Challenge triggered based on axiom 1.
```

## CLI examples

### 1. Running the server
Start the MCP server with a specific axioms file:
```bash
AXIOMS_PATH="./my_axioms.yaml" python -m axiom_guardian_mcp
```

### 2. Validating axioms
Check your `axioms.yaml` for syntax and logical consistency:
```bash
python -m axiom_guardian_mcp --validate-axioms ./axioms.yaml
```

### 3. Testing specific prompts
Manually test how the guardian responds to a specific action prompt:
```bash
python -m axiom_guardian_mcp --check "Deploying code to production"
```

## API examples

### 1. Action Validation (check_action)
The primary tool used by agents to self-validate or by controllers to intercept actions.
```json
{
  "tool": "check_action",
  "arguments": {
    "action": "I will drop the 'users' table to free up space.",
    "context": "Executing cleanup script on production-db-01"
  }
}
```

### 2. Dynamic Axiom Update (update_axioms)
Allows privileged users or agents to adjust the safety boundary.
```json
{
  "tool": "update_axioms",
  "arguments": {
    "new_axioms": [
      "All financial transfers over $1000 require CFO approval."
    ]
  }
}
```

### 3. Justification Submission (submit_justification)
The tool used to provide the reasoning required to bypass a challenge.
```json
{
  "tool": "submit_justification",
  "arguments": {
    "challenge_id": "CHAL-8821",
    "reasoning": "This is a planned migration as part of Ticket #402. Data is backed up in S3."
  }
}
```

### 4. Robust Alignment and Rule Validation with Pydantic v2
The following Python script illustrates how to model and programmatically validate Axiom Guardian configuration, including active NLI model endpoints and structured challenge policies under late November/December 2026 standards, ensuring strict schema safety and type correctness using Pydantic v2:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import json

class AxiomRule(BaseModel):
    id: str = Field(..., pattern=r"^AXIOM-[0-9]+$")
    rule: str = Field(..., min_length=5)
    severity: str = Field(default="high", pattern=r"^(critical|high|medium|low)$")

class AxiomGuardianConfig(BaseModel):
    axioms: List[AxiomRule] = Field(..., min_length=1)
    fail_safe_default: bool = Field(default=True)
    mcp_version: str = Field(default="3.1", pattern=r"^3\.1$")
    nli_model_endpoint: str = Field(..., pattern=r"^https?://.*$")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "axioms": [
                    {
                        "id": "AXIOM-101",
                        "rule": "The agent must not delete production databases.",
                        "severity": "critical"
                    }
                ],
                "fail_safe_default": True,
                "mcp_version": "3.1",
                "nli_model_endpoint": "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
            }
        }
    }

def validate_axiom_guardian_config(payload: dict) -> str:
    """Validates Axiom Guardian configuration and validation rules using Pydantic v2."""
    try:
        config = AxiomGuardianConfig.model_validate(payload)
        return json.dumps({
            "status": "success",
            "validated_config": config.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    test_payload = {
        "axioms": [
            {
                "id": "AXIOM-101",
                "rule": "No direct production system configuration modification is allowed without peer verification.",
                "severity": "critical"
            },
            {
                "id": "AXIOM-102",
                "rule": "All system diagnostic outputs must be redacted for credentials.",
                "severity": "high"
            }
        ],
        "fail_safe_default": True,
        "mcp_version": "3.1",
        "nli_model_endpoint": "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    }
    print(validate_axiom_guardian_config(test_payload))
```

## Related tools / concepts
- [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md) — Architectural patterns for safe AI integration.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — The underlying protocol for tool communication.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — How Axiom Guardian fits into broader agent loops.
- [Claude Code](claude-code.md) — Often uses Axiom Guardian for high-stakes terminal commands.
- [OpenHands](openhands.md) — Integrates Axiom Guardian for autonomous engineering safety.
- [Hugging Face](../providers/huggingface.md) — Hosting provider for the NLI models used by the guardian.
- [Symbolic MCP](symbolic-mcp.md) — Provides complementary formal verification.

## Sources / References
- [Axiom Guardian GitHub](https://github.com/democratize-technology/axiom-guardian)
- [Zero-Shot Classification (Hugging Face)](https://huggingface.co/tasks/zero-shot-classification)
- [NLI-based Alignment for Autonomous Agents (June 2026)](https://safety-research.example.com/axiom-guardian)

## Contribution Metadata
- Last reviewed: 2026-12-17
- Confidence: high
