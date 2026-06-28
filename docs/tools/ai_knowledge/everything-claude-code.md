# Everything Claude Code (ECC)

## What it is
Everything Claude Code (ECC) is a comprehensive performance optimization system designed for AI agent harnesses, primarily [Claude Code](../development_ops/claude-code.md). It is not just a configuration pack but a complete ecosystem of specialized agents, skills, hooks, and rules evolved from intensive daily production use.

## What problem it solves
It bridges the gap between a raw AI CLI and a production-ready autonomous engineering environment. ECC addresses context window management, security risks, memory persistence across sessions, and language-specific coding standards through automated enforcement and optimized prompt engineering. It is specifically tuned to maximize the reasoning efficiency of frontier models like `claude-4-8-opus-20260528` and GPT-5.5 using MCP 3.0.

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
- **Optimized Performance**: Pre-configured token optimization settings (e.g., `MAX_THINKING_TOKENS`) to reduce costs while maintaining high-quality reasoning.

## Limitations
- **Configuration Overhead**: Requires manual rule installation as Claude Code plugins cannot distribute files to the filesystem.
- **Context Usage**: Large numbers of enabled MCP servers or skills can rapidly consume the LLM's context window.
- **Maintenance**: Keeping 180+ skills updated requires active community participation.

## Key Components
- **Subagents (48+)**: Specialized personas like `typescript-reviewer`, `sql-auditor`, and `build-error-resolver` for delegation.
- **Skills (182+)**: Domain-specific workflow definitions ranging from `frontend-slides` to `market-research`.
- **Hooks Runtime**: Trigger-based automations that fire on tool events (e.g., auto-formatting after an edit or secret detection before prompt submission).
- **Rules (34+)**: Standardized, language-specific guidelines (TypeScript, Python, Go, Swift, PHP) that ensure consistency across the codebase.

### AgentShield — Security Auditor
A dedicated auditor (v2.0 as of June 2026) that scans Claude Code configurations (`.claude/` directory) for vulnerabilities. It uses adversarial reasoning (Red Team/Blue Team agents) to evaluate protection layers and synthesize risk assessments.

### Skill Creator
Analyzes local Git history to automatically generate `SKILL.md` files and instinct collections, allowing the agent to "learn" from the existing codebase patterns.

## When to use it
- When building complex production applications with AI agents.
- When requiring consistent coding standards and hooks across a distributed engineering team.
- When seeking an "all-in-one" performance system for AI agent harnesses.

## When not to use it
- For trivial, single-file scripts where a standard prompt is sufficient.
- If you prefer a completely "vanilla" AI experience without automated hooks or specialized subagents.

## Getting started

### Installation (Plugin)
```bash
# Add the marketplace
/plugin marketplace add https://github.com/affaan-m/everything-claude-code

# Install the plugin
/plugin install everything-claude-code@everything-claude-code
```

### Installation (Manual)
```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code
# Deploy agents to your local configuration
cp agents/*.md ~/.claude/agents/
```

## CLI examples

### Audit Configurations with AgentShield
```bash
/plugin run ecc:agentshield --path .claude/
```

### Create a New Skill from History
```bash
/plugin run ecc:skill-creator --since "3 days ago" --name "new-feature-pattern"
```

### List Active Subagents
```bash
/plugin run ecc:list-agents
```

## API examples

### Configuring Subagent Delegation (JSON)
ECC allows defining delegation rules in a central `agents.json` file.
```json
{
  "delegation_rules": {
    "security_audit": "ecc:agentshield",
    "ui_review": "ecc:frontend-reviewer",
    "backend_refactor": "ecc:architect"
  }
}
```

### Custom Hook Trigger (JavaScript)
```javascript
// .claude/hooks/post-edit.js
module.exports = async ({ file, content }) => {
  if (file.endsWith('.ts')) {
    await run('npm run lint -- --fix ' + file);
    console.log(`ECC: Linted ${file}`);
  }
};
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) (Core harness)
- [Cursor](../development_ops/cursor.md) (Supported IDE)
- [OpenCode](../development_ops/opencode.md) (Supported harness)
- [Aider](../development_ops/aider.md) (Terminal-based alternative)
- [last30days-skill](last30days-skill.md) (Integrated social research skill)
- [AgentShield](#agentshield) (Integrated security auditor)
- [Skill Creator](#skill-creator) (Integrated pattern extractor)
- [Claude Hooks](../development_ops/claude-hooks.md) (Integrated lifecycle hooks)

## Sources / references
- [Everything Claude Code (GitHub)](https://github.com/affaan-m/everything-claude-code)
- [ECC Documentation / Guides](https://ecc.tools/)
- [Anthropic Claude Code Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- [AgentShield v2 Release](https://ecc.tools/blog/agentshield-v2)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
