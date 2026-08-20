# Claude Hooks

## What it is
Claude Hooks are event-driven middleware interceptors and configuration standards used to wrap **Claude Code** agentic sessions with deterministic lifecycle guardrails. As of early 2027, Claude Hooks natively integrate with **MCP 3.1 / FastMCP 3.1** specification primitives, allowing engineering teams to intercept tool executions before (`PreToolUse`) or after (`PostToolUse`) execution during autonomous coding loops with **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**.

## What problem it solves
Autonomous AI coding agents can occasionally make unintended filesystem modifications, introduce secret leaks in Git commits, or bypass corporate compliance rules. Claude Hooks solve this by providing a deterministic, non-LLM enforcement layer. By intercepting tool calls in real time, hooks can run static analysis, check secret scanners, enforce branch protection policies, or execute automatic formatting before changes are permanently applied to the codebase.

## Where it fits in the stack
**Development & Ops / Workflow Guardrails**. Claude Hooks sit directly between the agent reasoning loop and system execution primitives, acting as safety middleware and event triggers inside [Claude Code](claude-code.md) environments.

## Typical use cases
- **Pre-Commit Secret Scanning**: Intercepting `git_commit` tool calls to verify no API credentials, private keys, or certificates are staged.
- **Automated Formatting & Linting**: Triggering `ruff`, `prettier`, or `eslint` automatically in `PostToolUse` steps when `write_file` modifies source files.
- **Protected File Guardrails**: Preventing the agent from modifying critical system manifests, lockfiles, or standard documentation headers without explicit permission.
- **Observability & Telemetry**: Emitting webhook events or logging execution metrics to observability dashboards when tools execute.

## Strengths
- **Deterministic Enforcement**: Guardrail rules are executed by local shell binaries or Python scripts, guaranteeing 100% compliance regardless of model prompting.
- **Native FastMCP 3.1 Compatibility**: Seamlessly intercepts standard MCP tool invocation payloads.
- **Clear Lifecycle Transparency**: Standard JSON configuration (`.claude/hooks.json`) is version-controlled alongside application code.
- **Extensible Integration**: Supports any executable script or CLI tool binary as an action handler.

## Limitations
- **Latency Overhead**: Complex or network-dependent hook scripts add execution delay to each step in the agent's interaction loop.
- **Environment Dependency**: Hooks depend on local system dependencies (e.g., `python3`, `node`, `ruff`) being present in the shell `$PATH`.
- **Configuration Scope**: Complex nested hook configurations can require ongoing maintenance as repository tooling evolves.

## When to use it
- In multi-developer team environments requiring strict adherence to security protocols, secret scanning, and formatting standards.
- When delegating autonomous, high-impact tasks (such as refactoring database schemas or infrastructure configuration) to terminal agents.
- When integrating [Claude Code](claude-code.md) with internal auditing or CI/CD pipelines.

## When not to use it
- During rapid, lightweight local prototyping where strict pre-commit checks hinder developer velocity.
- For isolated sandbox environments where code execution is fully untrusted and ephemeral.

## Getting started

### Configuration Directory Setup
Initialize the configuration directory inside your repository root:

```bash
mkdir -p .claude
touch .claude/hooks.json
```

### Basic `.claude/hooks.json` Configuration
Define pre-tool and post-tool lifecycle hooks:

```json
{
  "version": "1.0",
  "hooks": [
    {
      "name": "Secret Scanner",
      "type": "PreToolUse",
      "tool": "git_commit",
      "action": "python3 scripts/scan_secrets.py",
      "on_failure": "abort"
    },
    {
      "name": "Code Formatter",
      "type": "PostToolUse",
      "tool": "write_file",
      "action": "ruff format {{filepath}}",
      "on_failure": "warn"
    }
  ]
}
```

## CLI examples

### Testing Pre-Commit Secret Scanner Hook Manually
Verify that the hook script functions correctly outside the agent loop:

```bash
python3 scripts/scan_secrets.py --staged --verbose
```

### Environment Verification for Required Hook Dependencies
Ensure all executables referenced in `.claude/hooks.json` are in system path:

```bash
which ruff eslint python3
```

### Inspecting Active Hook Logs
Tail execution logs emitted during Claude Code agent sessions:

```bash
tail -f .claude/hooks.log
```

## API examples

### Custom Python Middleware Hook with Pydantic v2 Payload Validation
Implement a robust, type-safe hook handler in Python to enforce protected path policies:

```python
import sys
from typing import Literal, Dict, Any
from pydantic import BaseModel, Field, ValidationError

class HookPayload(BaseModel):
    hook_name: str = Field(..., description="Label of executing hook")
    type: Literal["PreToolUse", "PostToolUse"]
    tool_name: str = Field(..., description="Target tool identifier")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Captured tool arguments")

def evaluate_tool_invocation(raw_payload: Dict[str, Any]) -> bool:
    try:
        payload = HookPayload.model_validate(raw_payload)

        # Guardrail rule: Protect standards and core configuration files from unauthorized deletion
        if payload.tool_name == "delete_file":
            target_path = str(payload.arguments.get("filepath", ""))
            if "standards" in target_path or "config" in target_path:
                print(f"SECURITY BLOCK [{payload.hook_name}]: Deletion of protected path '{target_path}' is prohibited.", file=sys.stderr)
                return False
        return True
    except ValidationError as err:
        print(f"Hook payload validation error: {err}", file=sys.stderr)
        return False

if __name__ == "__main__":
    sample_payload = {
        "hook_name": "Protected Path Guard",
        "type": "PreToolUse",
        "tool_name": "delete_file",
        "arguments": {"filepath": "docs/standards.md"}
    }

    allowed = evaluate_tool_invocation(sample_payload)
    print(f"Tool invocation permitted: {allowed}")
```

## Related tools / concepts
- [Claude Code](claude-code.md) — Primary terminal CLI running Claude Hooks.
- [Claude Plugins](claude-plugins.md) — Extension ecosystem providing modular tools and skills.
- [Aider](aider.md) — Terminal pair programmer supporting linting and auto-test triggers.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standardized tool execution framework.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Operational patterns for autonomous coding agents.

## Sources / references
- [Anthropic Claude Code Tool Use Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Claude Hooks Community Pattern Library](https://github.com/johnlindquist/claude-hooks)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
