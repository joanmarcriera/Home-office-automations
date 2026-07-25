# Family Values and Agent Communication Style

## What it is
The Family Values and Agent Communication Style is a governance framework that defines the core ethical, operational, and behavioral boundaries for Ralph, the Home Admin Agent. In late August 2026, this framework is essential for aligning frontier models like Claude 5.1, GPT-5.5, and Llama 4 Maverick with privacy-first household principles. It establishes the "Constitutional AI" foundation for the homelab, ensuring that autonomous agents act as trusted digital fiduciaries.

### Core Family Values
1. **Privacy First**: Local data (schedules, health, documents) remains local by default. Use of cloud APIs requires explicit "Value-Based Consent."
2. **Transparency**: Agents must be "legible," explaining their reasoning and tool use (MCP 3.1 Task Protocol) in real-time.
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
- **Model Agnostic**: Applies equally to Claude 5.1, GPT-5.5, or local Llama 4 Maverick models.
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
Using Pydantic v2 and late August 2026 patterns:
```python
from pydantic import BaseModel, Field

class FamilyValuePolicy(BaseModel):
    max_allowable_risk: float = Field(default=0.1, description="Threshold for data export risk")
    privacy_strictness: str = "high"

def is_action_compliant(action, values: FamilyValuePolicy) -> bool:
    if action.privacy_impact > values.max_allowable_risk:
        return False
    return True
```

## Related tools / concepts
- [Home Admin Agent Architecture](home-admin-agent-architecture.md) — The technical implementation of these values.
- [System Prompts](system_prompts.md) — Where values are codified into instructions.
- [Agentic Workflows](patterns/agentic-workflows.md) — Executable patterns following these rules.
- [Claude Code](../tools/development_ops/claude-code.md) — Inspiration for the "transparent reasoning" style.
- [MCP](patterns/tool-calling-and-mcp.md) — The protocol enabling legible tool use.
- [Model Routing Guide](model_routing_guide.md) — Selecting models based on the complexity of the ethical task.
- [Privacy First Design](https://en.wikipedia.org/wiki/Privacy_by_design) — Foundational concept for the homelab.

## Sources / References
- [Anthropic: Constitutional AI](https://www.anthropic.com/news/constitutional-ai-harmlessness-from-ai-feedback)
- [Microsoft: Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/)
- [OpenClaw Ethics Charter (Internal Draft)](https://github.com/OpenClaw/OpenClaw/docs/architecture/ethics.md)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
