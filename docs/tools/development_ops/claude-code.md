# Claude Code

## What it is
Claude Code is a command-line interface (CLI) tool and AI agent from Anthropic that can directly interact with your local development environment. It can read and write files, run terminal commands, and perform complex coding tasks. While originally a CLI-first tool, it now features a powerful **Redesigned Desktop App** for orchestrating multiple agentic workflows.

## What problem it solves
It reduces the friction of context-switching between an AI chat interface and a code editor. By operating directly in your environment, it can autonomously navigate large codebases and execute the commands necessary to implement and verify changes.

## Where it fits in the stack
**Category**: Agent / Tool

## Typical use cases
- **Codebase Refactoring**: Identifying and applying patterns across multiple files.
- **Automated Debugging**: Running tests, analyzing error logs, and applying fixes in a loop.
- **Remote Environment Control**: Managing and interacting with remote servers or containers via its Remote Control feature.
- **Overnight Routines**: Using the "Routines" feature to delegate long-running, complex tasks to Claude to complete autonomously while you are away.

## Strengths
- **Agentic Capabilities**: Can proactively run commands (e.g., `git`, `npm test`) to verify its work.
- **Remote Control**: Built-in support for managing remote dev environments.
- **Desktop Orchestration**: The redesigned desktop app features an integrated terminal, side chat, improved diff viewer, and rearrangeable panes (Preview, Plan, Diff, Tasks, Terminal).
- **Overnight Routines**: Can handle complex jobs overnight, providing a summary of changes upon your return.
- **Optimized Reasoning**: Leverages Claude 3.5 Sonnet for high-quality code generation and logic.

## Limitations
- **Proprietary**: Requires an Anthropic API key and is not open source.
- **Cost**: Token usage can be high for complex agentic tasks.

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

## Advanced Patterns & Best Practices

### 1. Orchestration Workflow (Command → Agent → Skill)
The most effective way to scale Claude Code is to use a layered orchestration pattern:
- **Slash Commands** (.claude/commands/): Simple templates for recurring tasks (e.g., `/refactor`).
- **Subagents** (.claude/agents/): Autonomous actors in isolated contexts for high-compute reasoning.
- **Skills** (.claude/skills/): Domain-specific knowledge and tools that are auto-discovered.

### 2. Context Management
- **Aggressive Compacting**: Context rot kicks in around 400k tokens. Use `/compact` manually or via hooks to drop unnecessary test logs while keeping the core reasoning.
- **Subagents for Context Isolation**: Instead of 50 file reads in your main session, use a subagent. Main session only sees the subagent's conclusion, keeping your primary window clean.
- **Rewind > Correct**: If an implementation fails, use `Esc Esc` or `/rewind` instead of prompting "fix this." It prevents failed code from polluting future reasoning.

### 3. Verification Iron Laws
- **Test-Time Compute**: Use separate context windows for implementation and review. One agent writes the code, another (fresh context) tries to find bugs in it.
- **Staff Reviewer Pattern**: Spin up a second Claude session to "grill" your plan before execution.

## Ecosystem extensions

### Curated starting points
- [awesomeclaude.ai](https://awesomeclaude.ai/) is a high-signal starting point for Claude Code workflows, skills, commands, and surrounding tools.
- [awesome-skills.com](https://awesome-skills.com/) is useful when you want reusable community skill packs rather than one-off prompt snippets.
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) works well as a broad index of commands, hooks, skills, and ecosystem repos.

### Plugin and extension layer
- Community plugin distribution is becoming a meaningful part of the Claude Code workflow, especially for browser tooling, repo helpers, and workflow packs.
- Use plugin marketplaces when you want fast installation and updates.
- Use direct GitHub repos when you want to audit the actual prompts, hooks, or skills before adoption.
- **Recommended Plugins**:
  - **connect-apps**: Bridges Claude Code with external SaaS platforms like GitHub, Slack, Notion, and Gmail for cross-app orchestration.
  - **agentlint**: Evaluates repository structure and documentation (like `CLAUDE.md`, `AGENTS.md`) to ensure it is optimized for AI agent consumption.
  - **code-review**: Automates professional-grade pull request reviews, focusing on logic, style, and security.
  - **test-writer-fixer**: A specialized agent for generating new unit tests and fixing broken ones across major frameworks (Jest, Pytest, Vitest).
  - **debugger**: An interactive diagnostic assistant that analyzes runtime logs and execution traces to identify the root cause of complex bugs.
  - **bug-fix**: Analyzes stack traces and repository context to propose and apply surgical fixes for identified issues.
  - **mcp-builder**: A development toolkit for rapidly scaffolding and testing new Model Context Protocol (MCP) servers.
  - **theme-factory**: A UI/UX utility for generating and applying consistent themes and styles across web applications.

### Context, hooks, and skills
- **Context mode / MCP** helps Claude Code pull in structured external context without stuffing everything into a single prompt.
- **Hooks** are better than prompt-only instructions when you need deterministic notifications, checks, or guardrails around the coding loop.
- **Skills** are the right layer for reusable workflows, planning patterns, and domain-specific execution scaffolds.

### Community signals
- Community skill directories are useful discovery surfaces, but quality varies widely. Prefer repos with clear READMEs, examples, and recent maintenance.
- This [Reddit field report](https://www.reddit.com/r/ClaudeAI/comments/1ok9v3d/i_tested_30_community_claude_skills_for_a_week/) is useful as a practical reminder that many community skills are best treated as starting points to adapt, not production-grade defaults.

## Sources / references
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control)
- [Claude Code: Overnight Jobs](https://thenewstack.io/claude-code-can-now-do-your-job-overnight/)
- [Automate tasks with Claude Code](https://www.geeky-gadgets.com/automate-tasks-with-claude-code/)
- [awesomeclaude.ai](https://awesomeclaude.ai/)
- [awesome-skills.com](https://awesome-skills.com/)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [Awesome Claude Plugins](https://github.com/ComposioHQ/awesome-claude-plugins)
- [Claude Hooks](https://github.com/johnlindquist/claude-hooks)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)
- [Awesome Claude Skills](https://github.com/BehiSecc/awesome-claude-skills)
- [Claude Code Best Practice (Vibe coding to agentic engineering)](https://github.com/shanraisshan/claude-code-best-practice)
- [Reddit field report](https://www.reddit.com/r/ClaudeAI/comments/1ok9v3d/i_tested_30_community_claude_skills_for_a_week/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
