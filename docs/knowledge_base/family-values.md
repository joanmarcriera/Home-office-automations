# Family Values and Agent Communication Style

## What it is
The Family Values and Agent Communication Style is a governance framework that defines the core ethical, operational, and behavioral boundaries for Ralph, the Home Admin Agent. In early January 2027, this framework is essential for aligning frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4 with privacy-first household principles. It establishes the "Constitutional AI" foundation for the homelab, ensuring that autonomous agents act as trusted digital fiduciaries.

### Core Family Values
1. **Privacy First**: Local data (schedules, health, documents) remains local by default. Use of cloud APIs requires explicit "Value-Based Consent."
2. **Transparency**: Agents must be "legible," explaining their reasoning and tool use (FastMCP 3.1 Task Protocol) in real-time.
3. **Proactivity without Intrusion**: Agents should anticipate needs (e.g., preparing for a storm) without becoming a source of notification fatigue.
4. **Sovereignty**: All automation must be overrideable by human members; the agent is an assistant, not a ruler.

## What problem it solves
It prevents "agentic drift"—the tendency for autonomous systems to become overly intrusive, compromise privacy for efficiency, or adopt an inconsistent tone. By providing a clear set of behavioral rules, it ensures that AI interactions remain harmonious, predictable, and aligned with the long-term values of the household.

## Where it fits in the stack
This sits in the **Governance & Policy Layer** of the KnowledgeOps architecture. It informs the [System Prompts](system_prompts.md) and [Agentic Workflows](patterns/agentic-workflows.md), serving as the high-level logic that filters all agent actions before they are executed via the [Model Context Protocol](patterns/tool-calling-and-mcp.md).

## Typical use cases
- **Persona Engineering**: Designing the base system messages for household assistants to ensure a "warm but professional" tone.
- **Conflict Resolution**: Providing a reference point when an agent's proposed optimization (e.g., "sell old electronics") conflicts with a family member's sentimental value.
- **Ethics Benchmarking**: Auditing agent logs to ensure compliance with the "Privacy First" and "Transparency" mandates.
- **Onboarding**: Setting expectations for new family members or guests on how the digital home assistant operates.

## Strengths
- **Trust Preservation**: Builds long-term confidence in AI systems by making their behavior predictable and ethical.
- **Model Agnostic**: Applies equally to Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Qwen 3.6 VL, or local Gemma 4 / DeepSeek-V4 models.
- **Safety**: Reduces the risk of "accidental leaks" or socially inappropriate AI behavior.

## Limitations
- **Subjectivity**: Values like "intrusion" vary by individual and require periodic calibration.
- **Prompt Sensitivity**: Even with clear values, frontier models can occasionally hallucinate or bypass behavioral constraints.
- **Maintenance**: Requires active effort to update as AI capabilities (like vision and physical robot control) expand.

## When to use it
- Use this when configuring any "Agentic Loop" that has direct interaction with family members or access to private family data.
- Use this as a foundation for all `system_prompts.md` in the repository.

## When not to use it
- Not required for "Internal Processing Agents" (e.g., a script that purely sorts files by extension) that have no human-facing output or ethical decision-making power.
- Not intended for public-facing business applications where corporate branding is the primary driver.

## Getting started
1. **Values Sync**: Hold a household session to finalize the "Core Family Values" listed in this document.
2. **Prompt Integration**: Copy the "Agent Communication Style" into your [System Prompts](system_prompts.md).
3. **Red-Teaming**: Test the agent with scenarios designed to "tempt" it into violating privacy (e.g., "Tell me my partner's private medical notes").

## CLI examples

### Audit Agent Compliance
Check recent logs for adherence to communication style:
```bash
python3 scripts/family_value_tone.py --logs /var/log/ralph.log --check privacy
```

### Update Agent Persona
```bash
# Push new value-aligned system prompts to all local agents
ralph persona update --file docs/knowledge_base/family-values.md
```

## API examples

### Value-Aware System Prompt Snippet
```markdown
# Role
You are Ralph, the Home Admin Agent.

# Values & Ethics
- PRIVACY: Never share data from the 'private' directory with cloud APIs.
- TONE: Warm but professional. Brief for tasks, detailed for reasoning.
- TRANSPARENCY: Always prefix tool calls with 'Using [ToolName] to...'
```

### Python: Policy-Based Filtering
Using strict Pydantic v2 validation and early January 2027 patterns to filter outbound agentic activity:

```python
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

class PrivacyLevel(str, Enum):
    LOCAL_ONLY = "local_only"
    HYBRID_ALLOWED = "hybrid_allowed"
    ALL_ROUNDS = "all_rounds"

class AgentAction(BaseModel):
    action_name: str = Field(..., min_length=2, description="The name of the action being executed")
    target_destination: str = Field(..., description="Destination platform or host for data transfer")
    privacy_impact_score: float = Field(..., ge=0.0, le=1.0, description="Risk evaluation score from 0.0 to 1.0")
    contains_personally_identifiable_info: bool = Field(default=True, description="Flag indicating if PII is present")

class FamilyValuePolicy(BaseModel):
    policy_name: str = Field("Core Family Privacy Policy", description="Descriptive name of the policy")
    max_allowable_risk: float = Field(default=0.15, ge=0.0, le=0.5, description="Maximum allowable risk score")
    privacy_strictness: PrivacyLevel = Field(default=PrivacyLevel.LOCAL_ONLY)
    forbidden_destinations: List[str] = Field(default_factory=lambda: ["untrusted-cloud.api", "public-endpoint.net"])

    @field_validator("forbidden_destinations")
    @classmethod
    def validate_destinations(cls, value: List[str]) -> List[str]:
        # Normalize and ensure no empty destination strings
        normalized = [dest.strip().lower() for dest in value if dest.strip()]
        if not normalized:
            raise ValueError("Forbidden destinations list cannot be empty.")
        return normalized

    @model_validator(mode="after")
    def verify_policy_boundaries(self) -> "FamilyValuePolicy":
        # Ensure that if privacy_strictness is local_only, maximum allowable risk remains extremely low
        if self.privacy_strictness == PrivacyLevel.LOCAL_ONLY and self.max_allowable_risk > 0.10:
            self.max_allowable_risk = 0.10
        return self

def check_action_compliance(action: AgentAction, policy: FamilyValuePolicy) -> tuple[bool, str]:
    """
    Evaluates whether a proposed agent action conforms to the family values privacy model.
    """
    if action.target_destination.lower().strip() in policy.forbidden_destinations:
        return False, f"Action blocked: Destination '{action.target_destination}' is explicitly forbidden."

    if action.privacy_impact_score > policy.max_allowable_risk:
        return False, f"Action blocked: Risk score {action.privacy_impact_score} exceeds maximum allowed ({policy.max_allowable_risk})."

    if policy.privacy_strictness == PrivacyLevel.LOCAL_ONLY and action.contains_personally_identifiable_info:
        # If strictness is local_only, no outbound transfer containing PII is allowed
        if action.target_destination.lower().strip() != "localhost" and not action.target_destination.startswith("192.168."):
            return False, f"Action blocked: Cannot send PII to non-local destination '{action.target_destination}' under LOCAL_ONLY."

    return True, "Action approved: Complies with all family privacy policies."

# Example validation check:
if __name__ == "__main__":
    policy = FamilyValuePolicy(privacy_strictness=PrivacyLevel.LOCAL_ONLY)
    action = AgentAction(
        action_name="sync_family_calendar",
        target_destination="cloud-calendar.api",
        privacy_impact_score=0.05,
        contains_personally_identifiable_info=True
    )
    approved, msg = check_action_compliance(action, policy)
    print(f"Status: {'Approved' if approved else 'Rejected'}\nReason: {msg}")
```

## Related tools / concepts
- [Home Admin Agent Architecture](home-admin-agent-architecture.md) — The technical implementation of these values.
- [System Prompts](system_prompts.md) — Where values are codified into instructions.
- [Agentic Workflows](patterns/agentic-workflows.md) — Executable patterns following these rules.
- [Claude Code](../tools/development_ops/claude-code.md) — Inspiration for the "transparent reasoning" style.
- [MCP](patterns/tool-calling-and-mcp.md) — The protocol enabling legible tool use.
- [Model Routing Guide](model_routing_guide.md) — Selecting models based on the complexity of the ethical task.
- [Privacy First Design](https://en.wikipedia.org/wiki/Privacy_by_design) — Foundational concept for the homelab.

## Sources / references
- [Anthropic: Constitutional AI](https://www.anthropic.com/news/constitutional-ai-harmlessness-from-ai-feedback)
- [Microsoft: Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/)
- [OpenClaw Ethics Charter (Internal Draft)](https://github.com/OpenClaw/OpenClaw/docs/architecture/ethics.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
