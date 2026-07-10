# Windsurf IDE

## What it is
**Windsurf** (v2.0+, July 2026) is the world's first agentic IDE, developed by **Codeium** (and now deeply integrated with **Cognition's Devin** technology). It is built on top of the VS Code core but features a completely reimagined AI interaction model called **Cascade**, which moves beyond simple chat interfaces into autonomous, multi-file execution and real-time environment management with native support for the **MCP 3.0 Task Protocol**.

## What problem it solves
Traditional AI assistants in IDEs are "passive observers" that can only suggest text. Windsurf solves the "context gap" and the "execution gap" by allowing its agent (Cascade) to not only see the entire codebase but also autonomously navigate files, run terminal commands, manage dependencies, and perform complex, cross-file refactors using models like [Gemma 3](../ai_knowledge/local_llms.md) and [Claude 4.8](../ai_knowledge/claude.md).

## Where it fits in the stack
**Category**: Tool / Development & Ops / Agentic IDE. It serves as the primary "Command Center" for developers who want to transition from manual coding to AI-augmented engineering, sitting at the intersection of the editor, terminal, and autonomous agent orchestration.

## Typical use cases
- **Legacy Migration**: Asking Cascade to "Convert this entire Express.js project to Go/Fiber" and letting it handle the file-by-file translation.
- **Rapid Prototyping**: Generating a full-stack feature (frontend, backend, database migrations) from a single prompt.
- **Autonomous Bug Hunting**: Letting Devin Local trace a stack trace in the terminal and apply fixes autonomously.
- **Cross-File Refactoring**: Renaming symbols or changing API signatures across hundreds of files with 100% precision.
- **Agentic CI/CD Debugging**: Using Cascade to autonomously fix failing CI pipelines by interacting with the local shell to reproduce errors.

## Strengths
- **Agentic Maturity**: Unlike Copilot or Cursor, Windsurf is designed from the ground up to let the AI *act* on the terminal and filesystem.
- **VS Code Compatibility**: Supports the entire library of VS Code extensions and themes.
- **Cognition Partnership**: Benefits from Devin's superior reasoning capabilities for long-horizon tasks.
- **Fast Indexing**: Codebase changes are indexed in real-time with near-zero latency using a proprietary semantic indexing system.
- **MCP Native**: Full support for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md), allowing Cascade to use external tools.

## Limitations
- **Cloud Dependency**: Advanced agentic features require a connection to Codeium/Cognition's cloud infrastructure.
- **Proprietary Core**: While based on VS Code, the agentic layers (Cascade/Devin) are closed-source.
- **Learning Curve**: Mastering "Agentic Engineering" requires a shift in mindset from "how to code" to "how to prompt and supervise."
- **Token Usage**: Long-running autonomous sessions can consume significant token quotas.

## When to use it
- When you are working on large, complex codebases where simple RAG is insufficient.
- If you want an IDE that can autonomously fix failing tests and run its own debugging loops.
- When you need to leverage **MCP servers** for specialized tool-calling (e.g., Jira, GitHub, Database) within your development workflow.

## When not to use it
- In **strictly air-gapped** or offline environments where cloud access is prohibited.
- For extremely simple, single-file projects where the overhead of agentic indexing is unnecessary.
- If you have a strong preference for non-VS Code based editors (e.g., Vim, Emacs, JetBrains).
- If you require a completely open-source toolchain for both the IDE and the LLM orchestration.

## Getting started
Windsurf is primarily a local desktop application. Download the latest version from the official website.

### Local Installation
1. Download the Windsurf installer for your OS (macOS, Windows, Linux).
2. Install as you would VS Code.
3. Sign in to your Codeium/Cognition account to enable **Cascade** and **Devin** features.

### Configuring MCP Tools
Extend Windsurf's capabilities by adding MCP servers to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-search"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

## CLI examples
Windsurf provides a CLI tool to bridge the gap between your shell and the IDE.

```bash
# Launch Windsurf in the current directory
windsurf .

# Start a specific file at a specific line number
windsurf -g src/api/main.go:120

# Open a diff view between two files
windsurf --diff old_version.js new_version.js

# List active MCP servers detected by the IDE
windsurf --mcp-status
```

## API examples
Windsurf's **Cascade** engine is typically interacted with via natural language, but it can be controlled via the `Cascade API` (internal) or extended via MCP.

### Example MCP Tool Definition
You can create custom tools that Windsurf can call:
```typescript
// my-custom-tool.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "project-stats",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

// Windsurf will now be able to call 'get_project_health' via Cascade
server.tool("get_project_health", {}, async () => {
  return { content: [{ type: "text", text: "Healthy: 0 failing tests." }] };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Related tools / concepts
- [Cursor](cursor.md) — The primary competitor in the AI-IDE space with 'Composer' mode.
- [Aider](aider.md) — Terminal-based agentic coding tool for rapid command-line editing.
- [Claude Code](claude-code.md) — Anthropic's terminal-native agent for high-fidelity code manipulation.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The standard for extending Windsurf's tools.
- [Continue](continue_dev.md) — Open-source alternative for building custom AI IDE experiences.
- [OpenClaw](openclaw.md) — Gateway for agentic workflows and tool-calling security.
- [NanoClaw](nanoclaw.md) — Secure, containerized personal assistant framework.
- [Gemma 3](../ai_knowledge/local_llms.md) — Supported local model for agentic coding.
- [Claude 4.8](../ai_knowledge/claude.md) — Frontier model powering Cascade reasoning.

## Sources / References
- [Windsurf Official Documentation](https://docs.windsurf.com/)
- [Codeium Release Notes (July 2026)](https://codeium.com/blog/windsurf-v2-devin-integration)
- [Windsurf MCP Guide](https://docs.windsurf.com/windsurf/cascade/mcp)
- [Cognition AI: Devin in Windsurf](https://www.cognition.ai/blog/windsurf-integration)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
