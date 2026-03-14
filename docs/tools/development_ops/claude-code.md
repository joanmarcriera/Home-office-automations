# Claude Code

## What it is
Claude Code is a command-line interface (CLI) tool and AI agent from Anthropic that can directly interact with your local development environment. It can read and write files, run terminal commands, and perform complex coding tasks.

## What problem it solves
It reduces the friction of context-switching between an AI chat interface and a code editor. By operating directly in the terminal, it can autonomously navigate large codebases and execute the commands necessary to implement and verify changes.

## Where it fits in the stack
**Category**: Agent / Tool

## Typical use cases
- **Codebase Refactoring**: Identifying and applying patterns across multiple files.
- **Automated Debugging**: Running tests, analyzing error logs, and applying fixes in a loop.
- **Remote Environment Control**: Managing and interacting with remote servers or containers via its Remote Control feature.

## Strengths
- **Agentic Capabilities**: Can proactively run commands (e.g., `git`, `npm test`) to verify its work.
- **Remote Control**: Built-in support for managing remote dev environments.
- **Optimized Reasoning**: Leverages Claude 3.5 Sonnet for high-quality code generation and logic.

## Limitations
- **Proprietary**: Requires an Anthropic API key and is not open source.
- **CLI Only**: Lacks the visual multi-file diffing and GUI features found in IDEs like Cursor.

## When to use it
- Use when you need an autonomous agent to handle complex, multi-step development workflows.
- Use for tasks that require heavy terminal interaction alongside code editing.

## When not to use it
- Not necessary for simple coding questions or single-file edits.
- Not for users who prefer a fully visual GUI-based coding experience.

## Getting started

Install Claude Code via the official installation script or globally via npm, then authenticate with your Anthropic account:

```bash
# Recommended: Install via curl
curl -fsSL https://claude.ai/install.sh | bash

# Alternative: Install via npm
npm install -g @anthropic-ai/claude-code

# Authenticate
claude auth login

# Start a session in your current directory
claude
```

## CLI examples

### claude-code init
Create a `CLAUDE.md` file to give Claude persistent context about your repository:
```bash
claude init
```

### slash commands
Inside an active `claude` session, use these commands for quick actions:
```text
/help     # Show available commands and skills
/compact  # Summarize conversation history to save tokens
/config   # Interactively configure settings (model, theme, etc.)
/review   # Trigger a code review of staged changes
```

### MCP setup
Configure Model Context Protocol servers to extend Claude's capabilities:
```bash
# List configured MCP servers
claude mcp list

# Add a new MCP server
claude mcp add my-server npx -y @modelcontextprotocol/server-everything
```

## Related tools / concepts
- [Claude Code Router](./claude-code-router.md)
- [Aider](./aider.md)
- [Droid](./droid.md)
- [OpenHands](./openhands.md)
- [Claude Code Setup](./claude-code-setup.md)
- [Claude Plugins](./claude-plugins.md)
- [Claude Context Mode](./claude-context-mode.md)
- [Claude Hooks](./claude-hooks.md)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md)
- [Agent Client Protocol (ACP)](../../knowledge_base/agent_protocols.md)

## Ecosystem extensions

### Curated starting points
- [awesomeclaude.ai](https://awesomeclaude.ai/) is a high-signal starting point for Claude Code workflows, skills, commands, and surrounding tools.
- [awesome-skills.com](https://awesome-skills.com/) is useful when you want reusable community skill packs rather than one-off prompt snippets.
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) works well as a broad index of commands, hooks, skills, and ecosystem repos.

### Plugin and extension layer
- Community plugin distribution is becoming a meaningful part of the Claude Code workflow, especially for browser tooling, repo helpers, and workflow packs.
- Use plugin marketplaces when you want fast installation and updates.
- Use direct GitHub repos when you want to audit the actual prompts, hooks, or skills before adoption.

### Context, hooks, and skills
- **Context mode / MCP** helps Claude Code pull in structured external context without stuffing everything into a single prompt.
- **Hooks** are better than prompt-only instructions when you need deterministic notifications, checks, or guardrails around the coding loop.
- **Skills** are the right layer for reusable workflows, planning patterns, and domain-specific execution scaffolds.

### Community signals
- Community skill directories are useful discovery surfaces, but quality varies widely. Prefer repos with clear READMEs, examples, and recent maintenance.
- This [Reddit field report](https://www.reddit.com/r/ClaudeAI/comments/1ok9v3d/i_tested_30_community_claude_skills_for_a_week/) is useful as a practical reminder that many community skills are best treated as starting points to adapt, not production-grade defaults.

## Sources / references
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control)
- [awesomeclaude.ai](https://awesomeclaude.ai/)
- [awesome-skills.com](https://awesome-skills.com/)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [Claude Hooks](https://github.com/johnlindquist/claude-hooks)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)
- [Awesome Claude Skills](https://github.com/BehiSecc/awesome-claude-skills)
- [Reddit field report](https://www.reddit.com/r/ClaudeAI/comments/1ok9v3d/i_tested_30_community_claude_skills_for_a_week/)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium
