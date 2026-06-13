# Everything Claude Code (ECC)

## What it is
Everything Claude Code (ECC) is a comprehensive performance optimization system designed for AI agent harnesses, primarily [Claude Code](../development_ops/claude-code.md). It is not just a configuration pack but a complete ecosystem of specialized agents, skills, hooks, and rules evolved from intensive daily production use. It is optimized for the latest frontier models including `claude-4-8-opus-20260528` and GPT-5.5.

## What problem it solves
It bridges the gap between a raw AI CLI and a production-ready autonomous engineering environment. ECC addresses context window management, security risks, memory persistence across sessions, and language-specific coding standards through automated enforcement and optimized prompt engineering. It helps users manage the high token usage and cost associated with advanced reasoning models in June 2026.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Developer Tooling. It acts as the orchestration and enhancement layer for terminal-based AI agents.

## Typical use cases
- **Autonomous Engineering**: Leveraging specialized subagents (Architect, Planner, TDD Guide) for complex feature implementation.
- **Security Auditing**: Using the integrated AgentShield to scan configurations for secrets and injection risks.
- **Continuous Learning**: Automatically extracting patterns from development sessions into reusable "instincts" and skills.
- **Multi-Agent Orchestration**: Managing complex workflows across multiple services using collaborative planning commands.

## Strengths
- **Comprehensive Ecosystem**: Offers 48+ agents and 182+ skills covering 10+ programming languages.
- **Cross-Platform & Harness**: Supports Claude Code, Cursor, OpenCode, Codex, and Antigravity with unified rules.
- **Security-First**: Includes AgentShield for adversarial reasoning and secret detection.
- **Optimized Performance**: Pre-configured token optimization settings (e.g., `MAX_THINKING_TOKENS`) to reduce costs while maintaining reasoning quality.
- **Rapid Evolution**: Updated daily based on real-world production performance of Claude 4.8.

## Limitations
- **Configuration Overhead**: Requires manual rule installation as Claude Code plugins cannot easily distribute files to the filesystem.
- **Context Usage**: Large numbers of enabled MCP servers or skills can rapidly consume the LLM's context window.
- **Learning Curve**: The vast number of agents and skills requires time to master and integrate into a standard workflow.

## When to use it
- When building complex production applications with AI agents.
- When requiring consistent coding standards and hooks across a distributed engineering team.
- When seeking an "all-in-one" performance system for AI agent harnesses to maximize the value of expensive frontier models.

## When not to use it
- For trivial, single-file scripts where a standard prompt is sufficient.
- If you prefer a completely "vanilla" AI experience without automated hooks or specialized subagents.
- In environments where strict security policies prohibit the use of third-party agent enhancement packs.

## Getting started
Installation is typically done via the Claude Code marketplace or by cloning the repository for manual setup.

```bash
# Add the marketplace
/plugin marketplace add https://github.com/affaan-m/everything-claude-code

# Install the plugin
/plugin install everything-claude-code@everything-claude-code
```

## CLI examples
### 1. Initialize Project
Setup ECC rules and hooks in the current repository.
```bash
claude --prompt "Project context: $(cat AGENTS.md)" --run "init ecc"
```

### 2. Audit Configuration
Use AgentShield to audit your Claude Code setup.
```bash
/plugin run everything-claude-code:audit
```

### 3. Generate Skill
Extract patterns from your current session to create a new reusable skill.
```bash
/plugin run everything-claude-code:extract-skill --name "my-new-workflow"
```

## API examples
ECC provides a set of hooks that can be configured in your `.claude/config.json`.

```json
{
  "hooks": {
    "pre_tool_use": "node ~/.claude/plugins/ecc/hooks/pre-tool-audit.js",
    "post_edit": "node ~/.claude/plugins/ecc/hooks/lint-and-format.js"
  },
  "settings": {
    "MAX_THINKING_TOKENS": 16000
  }
}
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — The core terminal-based AI assistant from Anthropic.
- [Cursor](../development_ops/cursor.md) — AI-native code editor with similar agentic capabilities.
- [Aider](../development_ops/aider.md) — Popular terminal-based AI coding assistant.
- [last30days-skill](last30days-skill.md) — Specialized social research skill integrated into ECC.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Conceptual foundation for ECC's multi-agent approach.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Underlying standard for tool and skill integration.
- [OpenCode](../development_ops/opencode.md) — Open-source alternative to Claude Code supported by ECC.

## Sources / references
- [Everything Claude Code (GitHub)](https://github.com/affaan-m/everything-claude-code)
- [ECC Documentation / Guides](https://ecc.tools/)
- [Anthropic Claude Code Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
