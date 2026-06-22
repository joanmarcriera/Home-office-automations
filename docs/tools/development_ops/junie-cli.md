# Junie CLI

## What it is
Junie CLI is an AI coding assistant designed to live in the terminal and assist with repository-wide tasks. Developed as part of the JetBrains AI Lab initiative, it provides tools for navigating code, understanding dependencies, and making changes across multiple files. As of June 2026, it is optimized for high-speed, terminal-native workflows, serving as a "second brain" for developers who prefer CLI-first environments over heavy IDEs.

## What problem it solves
Bridges the gap between high-level AI reasoning and the raw terminal interface. It solves the context-switching problem where developers must leave their terminal to use web-based or IDE-based AI assistants. Junie is specifically engineered for codebase exploration, rapid navigation, and performing repository-wide audits without high latency.

## Where it fits in the stack
**Development & Ops**. Functions as a lightweight, terminal-native AI agent for codebase exploration and maintenance. It sits alongside tools like `rg` (ripgrep) and `fd`, providing an intelligent reasoning layer on top of standard CLI utilities.

## Typical use cases
- **Repository-wide Audits**: "Find all instances of deprecated API calls and suggest a migration path."
- **Codebase Exploration**: "Explain how the authentication flow is implemented across the project."
- **Terminal-Native Editing**: Making quick, context-aware fixes across multiple files directly from the tmux or shell environment.
- **Onboarding**: Helping new contributors understand the project structure and key entry points via natural language queries.

## Strengths
- **Terminal Native**: No need for a heavy IDE; works seamlessly over SSH or in minimal environments.
- **Workflow Integration**: Can be piped to and from other terminal tools (`grep`, `cat`, etc.).
- **Context Awareness**: Efficiently handles repository-wide context using local indexing and LLM-driven search.
- **Lightweight**: Optimized for speed and low resource consumption compared to full-featured AI IDEs.

## Limitations
- **No GUI**: Lacks the visual file diffing and project tree navigation of Cursor or VS Code.
- **Learning Curve**: Requires familiarity with terminal commands to maximize its utility.
- **Plugin Ecosystem**: Fewer third-party extensions compared to mature IDE-based assistants.
- **Visual Feedback**: Limited ability to provide real-time visual previews of UI changes.

## When to use it
- When you prefer a terminal-first development workflow (Vim, Neovim, Tmux users).
- When performing repository-wide tasks that span multiple files over an SSH connection.
- For quick codebase exploration and dependency analysis without opening a heavy IDE.

## When not to use it
- When you prefer a graphical IDE experience with real-time linting and visual debugging.
- When performing complex frontend work that requires immediate visual feedback.
- If you require deep integration with a specific proprietary IDE's internal state.

## Getting started
### Installation
Junie CLI is typically distributed via common package managers or directly from JetBrains' AI Lab repositories.

```bash
# Install via npm
npm install -g @jetbrains/junie-cli

# Or via Homebrew (macOS)
brew install jetbrains/tap/junie
```

### Initial Setup
Run the initialization command within your repository to build the local index:
```bash
junie init
```

## CLI examples
### Codebase Inquiry
```bash
# Ask about a specific implementation detail
junie ask "How are webhooks handled in this project?"
```

### Repository Search
```bash
# Find files related to a specific feature
junie find "authentication middleware"
```

### Automated Audit
```bash
# Run a specific audit across the repository
junie audit --rules "security-v1" --output audit_results.md
```

## API examples
### Custom Skill Implementation (JavaScript)
Junie allows developers to define custom "Skills" that extend its capabilities.

```javascript
// my-skill.js
export const skill = {
  name: "doc-verifier",
  description: "Verifies that all markdown files have contribution metadata",
  async run(context) {
    const files = await context.files.glob("**/*.md");
    // ... verification logic ...
    return results;
  }
};
```

### Integration in Scripts
```bash
# Using Junie to generate a summary for a PR
junie summary --branch main..feature-x > pr_description.txt
```

## Related tools / concepts
- [Aider](aider.md) — For terminal-based pair programming and editing.
- [ripgrep (rg)](ripgrep.md) — High-speed search utility used in conjunction with Junie.
- [Claude Code](claude-code.md) — Interactive terminal coding agent from Anthropic.
- [Codeium](codeium.md) — Multi-IDE AI completion and chat.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Automated development patterns.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Orchestration of AI tasks.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standard for tool-use integration.
- [Zed](zed.md) — High-performance, collaborative AI editor.

## Sources / references
- [Junie CLI Home Page](https://junie.jetbrains.com/)
- [JetBrains AI Lab Research](https://blog.jetbrains.com/ai/)
- [GitHub - Junie CLI Discussions](https://github.com/jetbrains/junie)
- [Junie v1.8 Release Notes](https://github.com/jetbrains/junie/releases)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
