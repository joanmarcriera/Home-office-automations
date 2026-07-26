# OpenClaw Security and Operations Pattern

## What it is
An operating pattern for running OpenClaw and other high-autonomy agents with explicit trust boundaries, patch discipline, skill review, and approval gates for high-impact actions. It is the primary framework for managing agents powered by frontier models like **Claude 5.1**, **GPT-5.5**, **Llama 4**, **Gemma 3**, **Qwen 3.6**, and the **Gemini 3.5 series**.

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
1. **Patch Verification**: Run `openclaw --version` to ensure you are on the latest security release (minimum `2026.8.31`).
2. **Network Isolation**: Ensure the OpenClaw gateway is not publicly accessible without a VPN or authenticated proxy.
3. **Skill Audit**: Remove all unused default skills, especially those with shell access or file deletion capabilities.
4. **Approval Setup**: Configure a messaging provider (Slack/Telegram) to receive `requires_approval` notifications.

## Technical Implementation: Claude Hooks & Trust Tagging

Modern security operations utilize **Claude Hooks** (Middleware) to intercept tool calls before execution. By September 2026, Claude Hooks include specialized `PreToolUse` and `PostToolUse` logic under the **Model Context Protocol (MCP 3.1)** standard, enabling granular control over the full tool-calling lifecycle for frontier engines.

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

### 3. Programmatic Trust Validation Loop (Python API)
A Python wrapper to validate that prompt payloads do not escape their trust boundaries prior to submission to frontier models.

```python
import re
from openai import OpenAI

client = OpenAI()

def validate_and_execute_payload(untrusted_data: str, system_prompt: str) -> str:
    # 1. Neutralize raw XML markers to prevent escaping trust tags
    sanitized_data = re.sub(r'</?untrusted_content>', '', untrusted_data)

    # 2. Formulate explicit trust boundary
    boundary_prompt = f"{system_prompt}\n<untrusted_content>\n{sanitized_data}\n</untrusted_content>"

    # 3. Call Claude 5.1 / GPT-5.5 model
    response = client.chat.completions.create(
        model="gpt-5.5-preview",
        messages=[{"role": "user", "content": boundary_prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content
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
- [LLM Trust Boundaries](llm-trust-boundaries.md)
- [ClawRouter](../../tools/infrastructure/clawrouter.md)
- [Aider](../../tools/development_ops/aider.md)
- [Claude Hooks](../../tools/development_ops/claude-hooks.md)

## Sources / References
- [OpenClaw system prompt concepts](https://docs.openclaw.ai/concepts/system-prompt)
- [TechRadar: "ClawJacked" vulnerability report](https://www.techradar.com/pro/security/a-human-chosen-password-doesnt-stand-a-chance-openclaw-has-yet-another-major-security-flaw-heres-what-we-know-about-clawjacked)
- [Anthropic: Tool Use Security Best Practices](https://docs.anthropic.com/claude/docs/tool-use-security)

## Contribution Metadata
- Last reviewed: 2026-09-02
- Confidence: high
