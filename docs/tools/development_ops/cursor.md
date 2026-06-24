# Cursor

## What it is
Cursor is an AI-native fork of VS Code, redesigned to facilitate seamless human-AI collaboration. It features deep codebase indexing, a native "Composer" for multi-file edits, and a built-in agentic ecosystem that can run tests, debug errors, and review PRs.

## What problem it solves
It solves the "context gap" in traditional IDEs by maintaining a persistent, high-fidelity index of the entire codebase. This allows models like [Claude 4.8 Opus](../ai_knowledge/claude.md) and [GPT-5.5](../ai_knowledge/openai.md) to perform complex, multi-file refactors with minimal hallucination, eliminating the need to manually supply file context to the AI.

## Where it fits in the stack
**Development & Ops / [Development Environment](index.md)**. It serves as the primary interface for AI-augmented engineering, acting as a successor to traditional VS Code setups.

## Typical use cases
- **Multi-File Refactoring**: Using "Composer" mode to apply architectural changes across many files simultaneously.
- **Visual UI Design**: Utilizing "Design Mode" in the Cursor browser to describe or draw UI changes by voice or click.
- **Pre-Push Security Audits**: Running `/review-security` to find vulnerabilities before opening a PR.
- **Autonomous Bug Hunting**: Tasking the "Bugbot" agent with identifying and fixing intermittent test failures.
- **Onboarding & Q&A**: Asking complex questions about a new codebase ("How is the database migration handled?") and receiving context-aware answers.

## Strengths
- **VS Code Native**: Full compatibility with all VS Code extensions, themes, and settings.
- **Composer 3.0**: High-speed, multi-agent editing engine that can orchestrate complex changes across hundreds of files.
- **Codebase Awareness**: Sophisticated RAG system that uses local embeddings for lightning-fast retrieval of relevant code.
- **Native MCP Support**: Direct integration with [Model Context Protocol](../automation_orchestration/mcp.md) servers for extended tool capabilities.
- **Design Mode**: Revolutionary UI-editing experience using voice input and element selection in a live browser.

## Limitations
- **Subscription Lock-in**: Advanced features and frontier model access require a monthly subscription.
- **Closed Source Core**: The orchestration and indexing layers are proprietary.
- **Telemetry**: Requires a cloud connection for many AI features, which may be a concern for highly sensitive environments.

## When to use it
- When you want the most polished, integrated AI coding experience available.
- For complex projects where maintaining manual context in a chat window is overwhelming.
- If you rely on the VS Code ecosystem but want "agentic" powers (terminal execution, multi-file editing).

## When not to use it
- In strictly offline or air-gapped environments.
- If you prefer a minimal, terminal-only workflow (use [Aider](aider.md) or [Claude Code](claude-code.md)).
- If your organization has a "no-AI-fork" policy and requires using official VS Code only.

## Getting started

### Installation
Download the Cursor binary for your operating system:

```bash
# MacOS/Linux/Windows
# Visit https://cursor.com/download
```

### Initial Configuration
Upon first run, Cursor will index your project. You can guide this process with a `.cursorrules` file in the root of your repository:

```markdown
# .cursorrules
- Prefer functional components over classes.
- Use Tailwind for styling.
- All database queries must go through the repository pattern in `/src/db`.
```

## CLI examples

### Running Cursor from the Terminal
Launch Cursor in the current directory:

```bash
cursor .
```

### Using the Cursor CLI Agent (June 2026)
Cursor now includes a CLI agent for headless operations:

```bash
cursor agent /review-bugbot --branch feature/auth
```

### Managing MCP Servers
Configure [MCP Servers](../automation_orchestration/mcp.md) via the Cursor settings or CLI:

```bash
cursor mcp add postgres npx @modelcontextprotocol/server-postgres
```

## API examples

### Cursor SDK (TypeScript)
Cursor provides an SDK for building custom agents and tools that run natively within the editor:

```typescript
import { CursorAgent } from "@cursor/sdk";

const myAgent = new CursorAgent({
  name: "DocUpdater",
  tools: [
    {
      name: "update_readme",
      handler: async (context) => {
        // Custom logic to update documentation
      }
    }
  ]
});

myAgent.run();
```

### Exposing Custom Tools
You can expose local functions to the Cursor agent as tools via the `cursor-config.json`:

```json
{
  "tools": [
    {
      "name": "run_internal_audit",
      "command": "sh scripts/audit.sh",
      "description": "Runs the project's internal security audit script."
    }
  ]
}
```

## Related tools / concepts
- [VS Code](vscode.md) — The foundation of Cursor.
- [Claude Code](claude-code.md) — The primary terminal-based alternative.
- [Aider](aider.md) — Terminal-native pair programmer.
- [Windsurf](windsurf.md) — Alternative AI-native IDE with "Flows".
- [Model Context Protocol](../automation_orchestration/mcp.md) — Supported for tool extensions.
- [Zed](zed.md) — High-performance Rust-based editor.
- [Continue](continue_dev.md) — VS Code extension for those who don't want a fork.
- [Bugbot](../agents/autoreason.md) — The native debugging agent in Cursor.

## Sources / references
- [Cursor Official Site](https://cursor.com/)
- [Cursor Changelog](https://cursor.com/changelog)
- [Cursor SDK Documentation](https://cursor.com/docs/sdk)
- [What's New in Cursor - June 2026](https://releasebot.io/updates/cursor)

## Contribution Metadata
- Last reviewed: 2026-06-11
- Confidence: high
