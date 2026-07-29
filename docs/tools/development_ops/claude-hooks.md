# Claude Hooks

## What it is
Claude Hooks are middleware patterns and JSON-based configuration standards used to wrap **Claude Code** sessions with deterministic guardrails. As of late 2026, they natively support **MCP 3.1** and allow for complex `PreToolUse` and `PostToolUse` logic to be injected into the agentic loop.

## What problem it solves
Autonomous agents like **Claude 5.1** and **GPT-5.5** can occasionally overlook repository-specific rules or security constraints. Claude Hooks solve this by providing an "interceptor" layer that can block or modify tool calls based on hard-coded conditions (e.g., preventing a commit if secrets are detected or automatically formatting code).

## Where it fits in the stack
**Development & Ops / Workflow Guardrails**. It acts as a configuration and orchestration layer sitting directly between the agent and the operating system, often integrated via specialized **MCP** servers or custom shell wrappers.

## Typical use cases
- **Security Interception**: Scanning for credentials or PII before the `git_commit` or `write_file` tools are allowed to execute.
- **Automated Formatting**: Running `prettier`, `ruff`, or `eslint` automatically after a `write_file` operation to ensure style compliance.
- **Workflow Notifications**: Sending a Slack, Teams, or **Chronos MCP** alert when a long-running refactor session completes.
- **Environment Verification**: Ensuring a clean Git state, active VPN connection, or passing test suite before allowing the agent to proceed.

## Strengths
- **Deterministic**: Logic is executed by the shell or a local runtime, not the LLM, ensuring 100% compliance with defined rules.
- **Complexity Management**: Simplifies cascading execution requirements in complex developer tools.
- **Transparency**: Uses standard JSON schemas (`hooks.json`) that are easy to audit, version control, and share across teams.
- **Extensible**: Supports any local binary or script as a hook action.

## Limitations
- **Configuration Overhead**: Requires maintaining `.claude/hooks.json` or equivalent setup files which can drift from project needs.
- **Latency**: Multiple complex hooks (especially network-dependent ones) can add measurable delay to the agent's "thinking" loop.
- **Local Tool Reliance**: Hooks depend on the presence of local binaries (e.g., `grep`, `npm`, `python`) which must be present in the execution environment.

## When to use it
- In shared team environments where standardized coding practices and security gates must be enforced.
- When delegating sensitive tasks (e.g., infrastructure-as-code or production database migrations) to an autonomous agent.
- To automate the feedback loop between the agent and local CI/CD scripts.

## When not to use it
- For rapid, exploratory prototyping where strict rules might hinder velocity.
- In small, single-file scripts where natural language instructions in the system prompt are sufficient.
- If the environment lacks the necessary tooling to execute the hook actions reliably.

## Getting started

### Configuration Directory
Claude Hooks typically look for configuration in the `.claude/` directory of your repository root.

```bash
mkdir -p .claude
touch .claude/hooks.json
```

### Implementing a Wrapper
Since hooks are often implemented as middleware, you can wrap your agent execution in a script:

```bash
# Example: run-claude-with-hooks.sh
# Runs a pre-hook script before starting the Claude Code session
python3 scripts/pre_hook_audit.py && claude && bash scripts/post_hook_cleanup.sh
```

### v0.5 Hooks Schema
The late 2026 schema supports conditional execution based on tool arguments and schema definitions conforming to **MCP 3.1**:

```json
{
  "version": "0.5",
  "hooks": [
    {
      "name": "Audit Commits",
      "tool": "git_commit",
      "type": "PreToolUse",
      "action": "scripts/audit_msg.py"
    }
  ]
}
```

## CLI examples

### Manual Hook Execution
Test your pre-commit hook manually before the agent runs to ensure it behaves correctly:

```bash
python3 scripts/scan_secrets.py --staged --verbose
```

### Validating Hook Environment
Ensure all tools required by your hooks are available in the current `$PATH`:

```bash
which eslint prettier python3 ruff
```

### Monitoring Hook Logs
View the output of middleware execution during an active agent session for debugging:

```bash
tail -f .claude/hooks.log
```

## API examples

### Hook Definition (JSON)
Define hooks using the standard middleware pattern for **Claude Code** and **MCP 3.1**.

```json
{
  "hooks": [
    {
      "name": "Pre-Commit Secret Scan",
      "type": "PreToolUse",
      "tool": "git_commit",
      "action": "scripts/scan_secrets.sh",
      "on_failure": "abort"
    },
    {
      "name": "Post-Write Lint",
      "type": "PostToolUse",
      "tool": "write_file",
      "action": "npx eslint {{filepath}} --fix",
      "on_failure": "warn"
    }
  ]
}
```

### Custom Python Hook (Middleware Logic) with Pydantic v2
Run robust validation of hook payload data programmatically:

```python
from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, Union
import sys

class HookPayload(BaseModel):
    hook_name: str = Field(..., description="The label of the hook execution")
    type: Literal["PreToolUse", "PostToolUse"]
    tool_name: str = Field(..., description="Name of intercepted tool")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Captured tool parameters")

def evaluate_tool_execution(payload_data: Dict[str, Any]) -> bool:
    try:
        payload = HookPayload.model_validate(payload_data)
        if payload.tool_name == "delete_file" and "protected" in payload.arguments.get("path", ""):
            print(f"Error [{payload.hook_name}]: Aborted tool run. Cannot delete protected path.", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"Validation failure: {e}", file=sys.stderr)
        return False

# Example payload
test_payload = {
    "hook_name": "Audit Deletions",
    "type": "PreToolUse",
    "tool_name": "delete_file",
    "arguments": {"path": "docs/protected/standards.md"}
}

is_allowed = evaluate_tool_execution(test_payload)
print(f"Execution Allowed? {is_allowed}")
```

## Related tools / concepts
- [Claude Code](claude-code.md) — The primary agentic CLI.
- [Model Context Protocol](../automation_orchestration/mcp.md) — For extending agent capabilities.
- [Aider](aider.md) — Alternative CLI coding assistant with similar hook support.
- [Plandex](plandex.md) — Plan-first engineering engine.
- [GitHub Actions](../../architecture/infrastructure.md) — For server-side CI hooks.
- [Playwright](playwright.md) — Often used in post-execution verification hooks.
- [Claude Plugins](claude-plugins.md) — Native extensions for Claude.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for autonomous agents.
- [Free Will MCP](free-will-mcp.md) — Autonomous loop management.

## Sources / references
- [Claude Hooks Pattern Library](https://github.com/johnlindquist/claude-hooks)
- [Anthropic: Tool Use Middleware Patterns](https://docs.anthropic.com/claude/docs/tool-use-middleware)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
