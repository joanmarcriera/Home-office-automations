# Claude Hooks

## What it is
Claude Hooks are middleware patterns and JSON-based configuration standards used to wrap [Claude Code](claude-code.md) sessions with deterministic guardrails. By defining `PreToolUse` and `PostToolUse` logic, teams can enforce security policies, run automated linting, and trigger external notifications without altering the agent's core reasoning.

## What problem it solves
Autonomous agents like [Claude 4.8 Opus](claude.md) can occasionally overlook repo-specific rules or security constraints. Claude Hooks solve this by providing an "interceptor" layer that can block or modify tool calls based on hard-coded conditions (e.g., preventing a commit if secrets are detected).

## Where it fits in the stack
**Development & Ops / [Workflow Guardrails](index.md)**. It acts as a configuration and orchestration layer sitting directly between the agent and the operating system.

## Typical use cases
- **Security Interception**: Scanning for credentials before the `git_commit` tool is allowed to execute.
- **Automated Formatting**: Running `prettier` or `eslint` automatically after a `write_file` operation.
- **Workflow Notifications**: Sending a Slack or Teams alert when a long-running refactor session completes.
- **Environment Verification**: Ensuring a clean Git state or active VPN connection before allowing the agent to start work.

## Strengths
- **Deterministic**: Logic is executed by the shell/runtime, not the LLM, ensuring 100% compliance.
- **Transparency**: Uses standard JSON schemas that are easy to audit and version control.
- **Low Friction**: Integrates directly with existing CLI agents via standard wrapper patterns.

## Limitations
- **Configuration Overhead**: Requires maintaining `.claude/hooks.json` or equivalent setup files.
- **Latency**: Multiple complex hooks can add measurable delay to the agent's "thinking" loop.
- **Local Tool Reliance**: Hooks depend on the presence of local binaries (e.g., `grep`, `npm`, `python`).

## When to use it
- In shared team environments where standardized coding practices must be enforced.
- When delegating sensitive tasks (e.g., infrastructure-as-code) to an autonomous agent.
- To automate the feedback loop between the agent and local CI/CD scripts.

## When not to use it
- For rapid, exploratory prototyping where strict rules might hinder velocity.
- In small, single-file scripts where natural language instructions in the prompt are sufficient.

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
python3 scripts/pre_hook.py && claude && bash scripts/post_hook.sh
```

## CLI examples

### Manual Hook Execution
Test your pre-commit hook before the agent runs:

```bash
python3 scripts/scan_secrets.py --staged
```

### Validating Hook Environment
Ensure all tools required by your hooks are available in the current `$PATH`:

```bash
which eslint prettier python3
```

### Monitoring Hook Logs
View the output of middleware execution during an active agent session:

```bash
tail -f .claude/hooks.log
```

## API examples

### Hook Definition (JSON)
Define hooks using the standard middleware pattern for [Claude Code](claude-code.md).

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

## Related tools / concepts
- [Claude Code](claude-code.md) — The primary agentic CLI.
- [Model Context Protocol](../automation_orchestration/mcp.md) — For extending agent capabilities.
- [Aider](aider.md) — Alternative CLI coding assistant.
- [Plandex](plandex.md) — Plan-first engineering engine.
- [GitHub Actions](../../architecture/infrastructure.md) — For server-side CI hooks.
- [Playwright](playwright.md) — Often used in post-execution verification.
- [Claude Plugins](claude-plugins.md) — Native extensions for Claude.

## Sources / references
- [Claude Hooks Pattern Library](https://github.com/johnlindquist/claude-hooks)
- [Anthropic: Tool Use Middleware Patterns](https://docs.anthropic.com/claude/docs/tool-use-middleware)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

## Contribution Metadata
- Last reviewed: 2026-06-11
- Confidence: high
