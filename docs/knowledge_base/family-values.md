# Family Values and Agent Communication Style

## What it is
The Family Values and Agent Communication Style is a governance framework that defines the core ethical, operational, and behavioral boundaries for Ralph, the Home Admin Agent. In early January 2027, this framework is essential for aligning frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4 with privacy-first household principles. It establishes the "Constitutional AI" foundation for the homelab, ensuring that autonomous agents act as trusted digital fiduciaries.

### Core Family Values
1. **Privacy First**: Local data (schedules, health, documents) remains local by default. Use of cloud APIs requires explicit "Value-Based Consent."
2. **Transparency**: Agents must be "legible," explaining their reasoning and tool use (FastMCP 3.1 Task Protocol) in real-time.
3. **Proactivity without Intrusion**: Agents should anticipate needs (e.g., preparing for a storm) without becoming a source of notification fatigue.
4. **Sovereignty**: All automation must be overrideable by human members; the agent is an assistant, not a ruler.

## System Architecture

The diagram below details the governance pipeline through which every human interaction, agentic planning loop, and FastMCP 3.1 tool call is evaluated against the Family Values Policy.

```
+-----------------------------------------------------------------------------------+
|                           Human Interaction & Trigger Layer                       |
|  +---------------------+   +---------------------+   +-------------------------+  |
|  | Voice Interface      |   | Mobile UI / Chat    |   | Scheduled Chronos Task  |  |
|  +----------+----------+   +----------+----------+   +------------+------------+  |
+-------------|-------------------------|---------------------------|---------------+
              | User Request / Command  | Payload                   | Event Trigger
+-------------v-------------------------v---------------------------v---------------+
|                    Family Values Governance & Policy Middleware                   |
|  +-----------------------------------------------------------------------------+  |
|  | Family Policy Engine (Pydantic v2 Context Inspector)                        |  |
|  | - Evaluates Privacy Risk Score & PII Contamination                          |  |
|  | - Checks Destination Endpoints against Whitelisted / Forbidden Domains      |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|  +-------------------------------------v---------------------------------------+  |
|  | Constitutional System Prompt Injection Layer                                 |  |
|  | - Embeds Core Family Ethics & Tone Rules into Frontier Model Memory          |  |
|  | - Enforces FastMCP 3.1 Task Protocol Legibility Constraints                    |  |
|  +-----------------------------------------------------------------------------+  |
+----------------------------------------|------------------------------------------+
                                         | Filtered & Approved Action
+----------------------------------------v------------------------------------------+
|                         Model Context Protocol (FastMCP 3.1)                      |
|  +---------------------+   +----------------------+   +------------------------+  |
|  | Local Ollama / vLLM |   | Home Assistant MCP   |   | Cloud Provider API     |  |
|  +---------------------+   +----------------------+   +------------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It prevents "agentic drift"—the tendency for autonomous systems to become overly intrusive, compromise privacy for efficiency, or adopt an inconsistent tone. By providing a clear set of behavioral rules, it ensures that AI interactions remain harmonious, predictable, and aligned with the long-term values of the household.

## Where it fits in the stack
This sits in the **Governance & Policy Layer** of the KnowledgeOps architecture. It informs the [System Prompts](system_prompts.md) and [Agentic Workflows](patterns/agentic-workflows.md), serving as the high-level logic that filters all agent actions before they are executed via the [Model Context Protocol](patterns/tool-calling-and-mcp.md).

## Governance Framework Comparison Matrix

| Governance Dimension | Family Values Framework | Standard Corporate AI Ethics | Unconstrained Frontier Agent |
| :--- | :--- | :--- | :--- |
| **Data Residency** | Strictly Local by Default | Central Cloud Storage | Cloud API Stream |
| **Tool Execution** | Human Approval for High-Impact | Automated Policy Enforcer | Unrestricted Autonomous |
| **Communication Vibe** | Warm, Legible, Concise | Formal / Corporate | Terse / Code-Centric |
| **Consent Model** | Granular Value-Based Consent | Blanket Terms of Service | Implicit Execution |
| **PII Handling** | Local Anonymization Pre-filter | Cloud Data Redaction | Pass-Through Raw |

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

### FastMCP 3.1 Governance Middleware Integration
The Python code below demonstrates a FastMCP 3.1 context middleware enforcing the Family Values policy before tool execution:

```python
import os
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("Family-Values-Governance-Gatekeeper", version="3.1.0")

class GovernanceAuditRequest(BaseModel):
    action_description: str = Field(..., description="Action proposed by the agent")
    is_external_cloud_call: bool = Field(..., description="Flag indicating outbound cloud network traffic")
    contains_private_pii: bool = Field(..., description="Flag indicating sensitive household data")

@mcp.tool()
async def validate_agent_action_governance(request: GovernanceAuditRequest) -> str:
    """Evaluates whether an agent action complies with family values privacy rules."""
    if request.is_external_cloud_call and request.contains_private_pii:
        return "BLOCKED: Cannot transmit private household PII to external cloud services under Privacy-First policy."

    return f"APPROVED: Action '{request.action_description}' conforms to family governance rules."

if __name__ == "__main__":
    mcp.run()
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
        normalized = [dest.strip().lower() for dest in value if dest.strip()]
        if not normalized:
            raise ValueError("Forbidden destinations list cannot be empty.")
        return normalized

    @model_validator(mode="after")
    def verify_policy_boundaries(self) -> "FamilyValuePolicy":
        if self.privacy_strictness == PrivacyLevel.LOCAL_ONLY and self.max_allowable_risk > 0.10:
            self.max_allowable_risk = 0.10
        return self

def check_action_compliance(action: AgentAction, policy: FamilyValuePolicy) -> tuple[bool, str]:
    """Evaluates whether a proposed agent action conforms to the family values privacy model."""
    if action.target_destination.lower().strip() in policy.forbidden_destinations:
        return False, f"Action blocked: Destination '{action.target_destination}' is explicitly forbidden."

    if action.privacy_impact_score > policy.max_allowable_risk:
        return False, f"Action blocked: Risk score {action.privacy_impact_score} exceeds maximum allowed ({policy.max_allowable_risk})."

    if policy.privacy_strictness == PrivacyLevel.LOCAL_ONLY and action.contains_personally_identifiable_info:
        if action.target_destination.lower().strip() != "localhost" and not action.target_destination.startswith("192.168."):
            return False, f"Action blocked: Cannot send PII to non-local destination '{action.target_destination}' under LOCAL_ONLY."

    return True, "Action approved: Complies with all family privacy policies."

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

## Containerized Deployment & Docker Compose Setup

Deploying the Family Values Governance Middleware in containerized environments ensures that outbound tool invocations and AI reasoning steps pass through an isolated policy proxy before contacting external infrastructure or models. The `docker-compose.yml` snippet below illustrates running the governance sidecar:

```yaml
version: "3.8"

services:
  family-values-governance:
    image: ghcr.io/openclaw/family-values-governance:v2.1.0
    container_name: family-values-governance
    restart: unless-stopped
    environment:
      - PRIVACY_LEVEL=LOCAL_ONLY
      - MAX_ALLOWABLE_RISK=0.10
      - LOG_LEVEL=INFO
      - ENCRYPT_AUDIT_LOGS=true
      - PORT=8080
    ports:
      - "8080:8080"
    volumes:
      - /opt/homelab/governance/policies:/etc/governance/policies:ro
      - /opt/homelab/governance/logs:/var/log/governance:rw
    security_opt:
      - no-new-privileges:true
    read_only: false
    networks:
      - ai-agent-network

networks:
  ai-agent-network:
    external: true
```

## Systemd Service Unit Specification

For host-level Linux deployments, the systemd unit (`family-values-governance.service`) keeps the gatekeeper daemon alive, enforcing real-time privacy verification on all local agent sockets:

```ini
[Unit]
Description=Family Values Governance & Privacy Gatekeeper Daemon
After=network.target home-assistant.service
Documentation=https://github.com/OpenClaw/OpenClaw/docs/architecture/ethics.md

[Service]
Type=simple
User=ralph-governance
Group=ralph-governance
WorkingDirectory=/opt/homelab/family-values-governance
ExecStart=/usr/bin/python3 -m governance.middleware --port 8080 --policy /etc/governance/policies/family.yaml
Restart=always
RestartSec=3s
Environment=PRIVACY_LEVEL=LOCAL_ONLY
Environment=MAX_ALLOWABLE_RISK=0.10
LimitNOFILE=65536
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/governance

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| `BLOCKED: Non-local PII transfer` | Agent attempted to transmit personal data to an unauthorized cloud API. | Check agent prompt and target endpoint. If cloud transfer is required, acquire Value-Based Consent or update `forbidden_destinations`. |
| `Risk Score Exceeded (Score > 0.10)` | Action privacy impact rating exceeds maximum policy threshold. | Inspect `privacy_impact_score` in Pydantic payload. Anonymize sensitive fields before invoking tool. |
| `Governance Gatekeeper Socket Timeout` | Governance daemon offline or CPU bound. | Verify service status (`systemctl status family-values-governance`). Ensure port 8080 is accessible on the `ai-agent-network`. |
| `Audit Log Write Error: Permission Denied` | Container or systemd service lacks write access to log volume. | Fix directory permissions (`chmod -R 775 /var/log/governance`) or check systemd `ReadWritePaths`. |

## Operational Best Practices & Red-Teaming Guidelines

1. **Automated Red-Teaming Probes**: Run periodic synthetic test scenarios against local LLM agents to ensure system prompts resist adversarial jailbreaks attempting to extract sensitive household data.
2. **Audit Log Retention & Encryption**: Store all agent action evaluation logs in encrypted SQLite or PostgreSQL databases with strict access control, ensuring transparency without compromising privacy.
3. **Emergency Override Switch**: Maintain a hardware or zero-trust software button (e.g., via Home Assistant) that instantly revokes API tokens for all autonomous agents if anomalous behavior is observed.

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
