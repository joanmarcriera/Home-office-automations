# Everything Claude Code (ECC)

## What it is
Everything Claude Code (ECC) is a comprehensive performance optimization system designed for AI agent harnesses, primarily [Claude Code](../development_ops/claude-code.md). It is not just a configuration pack but a complete ecosystem of specialized agents, skills, hooks, and rules evolved from intensive daily production use.

## What problem it solves
It bridges the gap between a raw AI CLI and a production-ready autonomous engineering environment. ECC addresses context window management, security risks, memory persistence across sessions, and language-specific coding standards through automated enforcement and optimized prompt engineering.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Developer Tooling

## Typical use cases
- **Autonomous Engineering**: Leveraging specialized subagents (Architect, Planner, TDD Guide) for complex feature implementation.
- **Security Auditing**: Using the integrated [AgentShield](#agentshield) to scan configurations for secrets and injection risks.
- **Continuous Learning**: Automatically extracting patterns from development sessions into reusable "instincts" and skills.
- **Multi-Agent Orchestration**: Managing complex workflows across multiple services using PM2 and collaborative planning commands.

## Strengths
- **Comprehensive Ecosystem**: Offers 48+ agents and 182+ skills covering 10+ programming languages.
- **Cross-Platform & Harness**: Supports Claude Code, Cursor, OpenCode, Codex, and Antigravity with unified rules.
- **Security-First**: Includes AgentShield for adversarial reasoning and secret detection.
- **Optimized Performance**: Pre-configured token optimization settings (e.g., `MAX_THINKING_TOKENS`) to reduce costs.

## Limitations
- **Configuration Overhead**: Requires manual rule installation as Claude Code plugins cannot distribute files to the filesystem.
- **Context Usage**: Large numbers of enabled MCP servers or skills can rapidly consume the LLM's context window.

## When to use it
- When building complex production applications with AI agents.
- When requiring consistent coding standards and hooks across a distributed engineering team.
- When seeking an "all-in-one" performance system for AI agent harnesses.

## When not to use it
- For trivial, single-file scripts where a standard prompt is sufficient.
- If you prefer a completely "vanilla" AI experience without automated hooks or specialized subagents.

## Key Components
- **Subagents (48+)**: Specialized personas like `typescript-reviewer`, `sql-auditor`, and `build-error-resolver` for delegation.
- **Skills (182+)**: Domain-specific workflow definitions ranging from `frontend-slides` to `market-research`.
- **Hooks Runtime**: Trigger-based automations that fire on tool events (e.g., auto-formatting after an edit or secret detection before prompt submission).
- **Rules (34+)**: Standardized, language-specific guidelines (TypeScript, Python, Go, Swift, PHP) that ensure consistency across the codebase.

## Ecosystem Tools

### AgentShield — Security Auditor
A dedicated auditor that scans Claude Code configurations (`.claude/` directory) for vulnerabilities. It uses adversarial reasoning (Red Team/Blue Team agents) to evaluate protection layers and synthesize risk assessments.

### Skill Creator
Analyzes local Git history to automatically generate `SKILL.md` files and instinct collections, allowing the agent to "learn" from the existing codebase patterns.

## Getting started

### Option 1: Install as a Claude Code Plugin (Recommended)
```bash
# Add the marketplace
/plugin marketplace add https://github.com/affaan-m/everything-claude-code

# Install the plugin
/plugin install everything-claude-code@everything-claude-code
```

### Option 2: Manual Installation
```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# Copy agents to your configuration
cp agents/*.md ~/.claude/agents/
```

## Technical details
- **Cross-Platform Support**: Rewritten in Node.js for compatibility across Windows, macOS, and Linux.
- **Adapter Pattern**: Uses a DRY (Don't Repeat Yourself) adapter to share hook scripts between Claude Code and [Cursor](../development_ops/cursor.md).
- **Token Optimization**: Includes recommended settings to reduce costs (e.g., setting `MAX_THINKING_TOKENS`) without sacrificing reasoning quality.
- **Memory Persistence**: Implements SQLite-backed state stores to track session history and skill evolution.

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) (Core harness)
- [Cursor](../development_ops/cursor.md) (Supported IDE)
- [OpenCode](../development_ops/opencode.md) (Supported harness)
- [Aider](../development_ops/aider.md) (Terminal-based alternative)
- [last30days-skill](last30days-skill.md) (Integrated social research skill)

## Sources / references
- [Everything Claude Code (GitHub)](https://github.com/affaan-m/everything-claude-code)
- [ECC Documentation / Guides](https://ecc.tools/)
- [Anthropic Claude Code Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)

## Contribution Metadata
- Last reviewed: 2026-05-17
- Confidence: high
