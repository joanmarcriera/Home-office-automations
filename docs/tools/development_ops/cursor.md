# Cursor

## What it is
Cursor is an AI-native fork of VS Code that integrates large language models directly into the editor's core. As of late December 2026, **Cursor 3.5** introduces **Composer 3.5**, **Design Mode v3**, and native **FastMCP 3.1** support, making it the standard for high-velocity AI engineering.

## What problem it solves
It eliminates the "context-switching" penalty of moving between an editor and an LLM chat interface. Cursor deeply indexes your entire codebase (locally and securely), allowing the AI to provide relevant code suggestions, perform complex refactors, and answer architectural questions with full awareness of your project's structure.

## Where it fits in the stack
**Development & Ops / AI-Native IDE**. It is the primary environment for most AI-assisted development, serving as the "cockpit" for both human developers and their agentic counterparts.

## Typical use cases
- **Multi-File Refactoring**: Using `Ctrl+K` or `Composer` to refactor logic across dozens of files simultaneously.
- **Codebase Indexing**: Asking high-level questions like "Where is the authentication logic handled?" and getting precise answers.
- **Automated Bug Fixing**: Providing an error message and letting Cursor suggest and apply the fix.
- **UI Prototyping**: Using **Design Mode** to generate and refine React/Vue components from natural language descriptions or wireframes.

## Strengths
- **Native Indexing**: Extremely fast and accurate codebase awareness via local embeddings.
- **Composer 3.5**: A powerful "multi-agent" workspace that can plan and execute complex features autonomously.
- **VS Code Compatibility**: Supports all existing VS Code extensions and keybindings.
- **Privacy First**: Offers "Local Mode" where code never leaves your machine (requires a local model like **Llama 4 Maverick**).

## Limitations
- **Subscription Required**: Advanced features like Composer 3.5 require a paid subscription.
- **Closed Source Core**: While based on VS Code, the AI integration layer is proprietary.
- **Memory Usage**: Deep indexing of very large projects (multi-million lines) can be resource-intensive.

## When to use it
- When working on large, complex codebases where context is difficult to maintain manually.
- For "flow-state" coding where you want to minimize the gap between thought and implementation.
- When you need a balance between full IDE power and AI-first simplicity.

## When not to use it
- If your organization forbids the use of proprietary AI-integrated IDEs.
- For extremely lightweight editing (consider **Vim** or **Zed** instead).
- If you prefer a pure terminal experience (consider **Aider** or **Claude Code**).

## Getting started

### Installation
Download the latest version from the [Cursor website](https://cursor.com/) and follow the installation wizard.

### Initial Configuration
Upon first launch, Cursor will offer to index your current project. This is highly recommended for full feature support:

1. Open a folder.
2. Click the `Index` button in the bottom-right status bar.
3. Select your preferred model (e.g., **Claude 5.1** or **GPT-5.5**).

## CLI examples

### Running Cursor from the Terminal
Launch Cursor in the current directory:

```bash
cursor .
```

### Using the Cursor CLI Agent (Late 2026)
Execute AI-assisted tasks directly from your shell using the new `cursor-agent` binary:

```bash
cursor-agent "Update all API endpoints to use the v3 schema"
```

### Managing MCP Servers
Cursor 3.5 allows you to manage **FastMCP 3.1** servers via the CLI:

```bash
cursor-mcp add-server "npx @modelcontextprotocol/server-postgres"
```

## API examples

### Cursor SDK (TypeScript)
Developers can now extend Cursor using its internal SDK for custom agentic behaviors.

```typescript
import { cursor } from 'cursor-sdk';

export async function onFileSave(file: string) {
  if (file.endsWith('.ts')) {
    await cursor.chat.ask(`Please lint this file: ${file}`);
  }
}
```

### Exposing Custom Tools
Expose local scripts as tools that Cursor can use in Composer sessions:

```json
// .cursor/tools.json
{
  "tools": [
    {
      "name": "run-tests",
      "command": "npm test",
      "description": "Run the project test suite"
    }
  ]
}
```

### Programmatic Setup with Pydantic v2
Validate local workspace config and agent limits securely before initiating composer pipelines:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class CursorConfig(BaseModel):
    model: str = Field(default="claude-5.1")
    enable_mcp: bool = Field(default=True, alias="enableMCP")
    indexing_excludes: List[str] = Field(default_factory=list, alias="indexingExcludes")
    mcp_servers: List[str] = Field(default_factory=list, alias="mcpServers")

    class Config:
        populate_by_name = True

# Parse and validate setup configuration
config_data = {
    "model": "claude-5.1",
    "enableMCP": True,
    "indexingExcludes": ["**/node_modules/**", "**/dist/**"],
    "mcpServers": ["npx @modelcontextprotocol/server-postgres"]
}

session = CursorConfig.model_validate(config_data)
print(f"Validated model: {session.model}")
print(f"MCP Servers: {session.mcp_servers}")
```

## Related tools / concepts
- [VS Code](../development_ops/vscode.md) — The foundation for Cursor.
- [Windsurf](../development_ops/windsurf.md) — A direct competitor with "Flow" based orchestration.
- [Zed](../development_ops/zed.md) — High-performance Rust-based editor.
- [Aider](aider.md) — Terminal-native pair programmer.
- [Claude Code](claude-code.md) — Anthropic's official CLI agent.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Native protocol for tool extensions (FastMCP 3.1).
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Often used as a local model provider for Cursor.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Underlying patterns.
- [Claude Hooks](claude-hooks.md) — For adding guardrails to Cursor's autonomous features.

## Sources / references
- [Cursor Official Website](https://cursor.com/)
- [Cursor Forum / Community](https://forum.cursor.com/)
- [Documentation: Composer](https://docs.cursor.com/composer)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
