# OpenClaw Security and Operations Pattern

## What it is
An operating pattern for running OpenClaw and other high-autonomy agents with explicit trust boundaries, patch discipline, skill review, and approval gates for high-impact actions. As of January 2027, it is the primary framework for managing agents powered by frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **Llama 4**, **Gemma 3**, and **Qwen 3.8** utilizing **FastMCP 3.1** security bindings.

## What problem it solves
OpenClaw combines messaging channels, browser automation, shell-capable skills, and third-party integrations. This power creates a massive attack surface where "prompt injection" or "malicious skill execution" can lead to credential theft or destructive filesystem actions. This pattern provides a "defense-in-depth" strategy for agentic operations.

## Where it fits in the stack
**Governance / Operations Layer**. It wraps the OpenClaw runtime with the safety, routing, and review controls needed for production or always-on home-office use.

## Typical use cases
- **Always-on Personal Assistant**: Hardening an agent that has access to your real accounts (Email, Calendar, Slack).
- **Autonomous Research Agents**: Safely browsing the web where content may contain adversarial prompts.
- **Enterprise Agent Orchestration**: Managing a fleet of agents with varying levels of privilege.
- **CI/CD Automation**: Gating shell-access agents that perform infrastructure updates.

## Strengths
- **Least Privilege**: Ensures agents only have the access they need for a specific task.
- **Human-in-the-Loop**: Standardizes the use of approval gates for irreversible actions.
- **Traceability**: Provides a clear audit log of which skills were executed and why.
- **Model Efficiency**: Pairs well with **ClawRouter** to use cheaper models for low-risk triage.

## Limitations
- **Operator Friction**: Over-strict security can slow down legitimate agent tasks.
- **Configuration Complexity**: Requires ongoing maintenance of trust tags and skill policies.
- **Supply Chain Risk**: Still vulnerable to compromises in the underlying model providers or skill registries.

## When to use it
- When OpenClaw or any high-autonomy agent is connected to real-world accounts.
- When agents have "write" access to the filesystem or shell.
- When you are processing untrusted external data (web content, emails, PDFs).

## When not to use it
- For fully deterministic, read-only scripts that have no external side effects.
- During early-stage prototyping in a completely isolated sandbox environment.

## Getting started

### Initial Hardening Checklist
Before deploying OpenClaw in an "always-on" mode, complete these steps:
1. **Patch Verification**: Run `openclaw --version` to ensure you are on the latest security release (minimum `2027.1.0`).
2. **Network Isolation**: Ensure the OpenClaw gateway is not publicly accessible without a VPN or authenticated proxy.
3. **Skill Audit**: Remove all unused default skills, especially those with shell access or file deletion capabilities.
4. **Approval Setup**: Configure a messaging provider (Slack/Telegram) to receive `requires_approval` notifications.

## Technical Implementation: Claude Hooks & Trust Tagging

Modern security operations utilize **Claude Hooks** (Middleware) to intercept tool calls before execution. Under the **Model Context Protocol (FastMCP 3.1)** standard, Claude Hooks include specialized `PreToolUse` and `PostToolUse` logic, enabling granular control over the full tool-calling lifecycle for frontier engines.

### 1. PreToolUse Hook (Approval Gate)
Configure a middleware layer that pauses execution for high-risk tools.

```json
// claude_hooks_config.json
{
  "mcp_version": "3.1",
  "hooks": {
    "PreToolUse": [
      {
        "tool": "shell_execute",
        "action": "pause_and_request_approval",
        "criteria": {
          "contains_keywords": ["sudo", "rm -rf", "chmod", "curl", "wget"],
          "user_id": "openclaw-worker-01"
        }
      }
    ]
  }
}
```

### 2. Prompt-Level Trust Tagging
Always wrap untrusted external data in XML tags to prevent the model from confusing it with system instructions. This is highly effective with high-reasoning models like **Claude 5.1** and **GPT-5.5**.

```markdown
System: You are an OpenClaw security-hardened assistant.
Instruction: Extract the meeting date from the email below.
Trust Boundary:
<untrusted_content>
{{email_body}}
</untrusted_content>
```

### 3. Programmatic Trust Validation & Security Hook Evaluation (Python API)
A Python wrapper using strict **Pydantic v2** validation to evaluate security hooks and validate prompt payloads before submission to frontier models:

```python
import re
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any

class SecurityHookEvaluation(BaseModel):
    """Pydantic v2 model for auditing and evaluating OpenClaw tool call permissions."""
    tool_name: str = Field(..., description="Target tool name requested by agent")
    tool_args: Dict[str, Any] = Field(default_factory=dict, description="Arguments passed to tool call")
    user_id: str = Field(..., description="Identifier of worker or user triggering tool")
    high_risk_keywords: List[str] = Field(
        default=["sudo", "rm -rf", "chmod", "curl", "wget", "DROP TABLE"],
        description="Forbidden/gated terms"
    )

    def is_approval_required(self) -> bool:
        """Determines if execution requires human approval gate."""
        arg_str = str(self.tool_args).lower()
        return any(kw.lower() in arg_str for kw in self.high_risk_keywords)

class SecurityPayload(BaseModel):
    """Pydantic v2 model for sanitizing and wrapping untrusted inputs."""
    untrusted_data: str = Field(..., description="Raw untrusted input text")
    system_prompt: str = Field(default="You are an OpenClaw security-hardened assistant.", description="System instruction")

    @field_validator("untrusted_data")
    @classmethod
    def sanitize_xml(cls, v: str) -> str:
        """Removes existing XML trust markers to prevent escaping."""
        return re.sub(r'</?untrusted_content>', '', v, flags=re.IGNORECASE)

def validate_and_execute_payload(payload: SecurityPayload, hook_eval: SecurityHookEvaluation) -> str:
    """Evaluates security gates and formats boundary prompt for Claude 5.1 / GPT-5.5."""
    if hook_eval.is_approval_required():
        return f"APPROVAL_REQUIRED: Action [{hook_eval.tool_name}] requested by [{hook_eval.user_id}] requires human confirmation."

    boundary_prompt = (
        f"{payload.system_prompt}\n"
        f"<untrusted_content>\n{payload.untrusted_data}\n</untrusted_content>"
    )
    return f"Payload authorized and framed for execution:\n{boundary_prompt}"
```

## CLI examples

### 1. Install Security-Hardened Skill
Install a skill specifically from a trusted, pinned repository.

```bash
openclaw skill install https://github.com/OpenClaw/trusted-skills/archive/refs/tags/v2.1.0.zip
```

### 2. Audit Active Permissions
List all skills and their associated capability tiers.

```bash
openclaw skills list --show-permissions --format table
```

### 3. Rotate Gateway Credentials
Rotate the local gateway's access token to prevent session hijacking.

```bash
openclaw config rotate-token --force --expiry 24h
```

## API examples

### Programmatic Approval (n8n Integration)
Use a webhook to confirm or deny an agent's requested action under MCP 3.1.

```javascript
// Example webhook payload sent to n8n for approval under MCP 3.1 payload schemas
{
  "mcp_version": "3.1",
  "agent_id": "research-bot-alpha-v5",
  "tool_call": "browser_open_url",
  "arguments": {
    "url": "https://suspicious-site.com/payload.sh"
  },
  "risk_score": 0.95,
  "approval_url": "https://n8n.internal/workflow/approval?id=123"
}
```

## Related tools / concepts
- [OpenClaw](../../tools/development_ops/openclaw.md)
- [Promptfoo](../../tools/benchmarking/promptfoo.md)
- [LLM Trust Boundaries](llm-trust-boundaries.md)
- [LiteLLM](../../services/litellm.md)
- [n8n](../../services/n8n.md)
- [OpenClaw Use-Case Catalog](openclaw-use-case-catalog.md)
- [ClawRouter](../../tools/infrastructure/clawrouter.md)
- [Aider](../../tools/development_ops/aider.md)
- [Claude Hooks](../../tools/development_ops/claude-hooks.md)

## Sources / References
- [OpenClaw system prompt concepts](https://docs.openclaw.ai/concepts/system-prompt)
- [TechRadar: "ClawJacked" vulnerability report](https://www.techradar.com/pro/security/a-human-chosen-password-doesnt-stand-a-chance-openclaw-has-yet-another-major-security-flaw-heres-what-we-know-about-clawjacked)
- [Anthropic: Tool Use Security Best Practices](https://docs.anthropic.com/claude/docs/tool-use-security)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
