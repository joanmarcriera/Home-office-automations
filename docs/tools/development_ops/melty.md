# Melty

## What it is
Melty is an open-source AI code editor designed to be a "human-in-the-loop" collaborator that understands the intent behind your changes. As of June 2026, it has matured into a premier agentic editor, utilizing an "Intent-State" loop to synchronize developer actions with AI assistance. It focuses on the "Collaborative Editing" pattern, where the AI acts as a pair programmer rather than just a code generator.

## What problem it solves
Bridges the gap between AI code generation and developer intent. It solves the "black box" generation problem where AI makes changes that the developer doesn't fully understand or that don't align with the long-term architectural goals of the project. Melty ensures that every AI suggestion is grounded in the developer's current "Intent," making the AI a more reliable and predictable partner.

## Where it fits in the stack
**Development & Ops**. Serves as an AI-native code editor with intent-aware editing. It is a direct open-source competitor to proprietary editors like Cursor and Zed, providing a transparent and extensible platform for agentic development.

## Typical use cases
- **Intent-driven editing**: When the purpose of the change (e.g., "Refactor this class for better testability") is more important than the specific lines of code.
- **Collaborative coding**: Working with an AI that respects and learns from your specific coding style and project-specific patterns.
- **Open-source AI Stack**: For developers who prefer an entirely open-source toolchain for their primary development environment.
- **Human-in-the-Loop Pair Programming**: Real-time collaboration where the AI proposes whole-block changes based on predicted developer intent.

## Strengths
- **Open Source**: Transparent, extensible, and community-driven.
- **Intent-Awareness**: Focuses on higher-level reasoning and "Why" behind changes rather than simple line autocompletion.
- **Developer Control**: Keeps the human developer firmly in the driver's seat through iterative feedback loops and explicit confirmation.
- **Privacy Centric**: Optimized for local or self-hosted indexing, ensuring project-wide context doesn't necessarily require sending entire files to proprietary servers.

## Limitations
- **Maturity**: Younger project compared to established editors like VS Code; the extension ecosystem is still growing.
- **Performance**: High-level intent tracking and real-time indexing can be resource-intensive on older hardware.
- **Ecosystem**: Lacks some of the deep, pre-integrated features found in proprietary tools like GitHub Copilot or Devin.
- **Learning Curve**: Users may need to adjust their workflow to effectively communicate "Intent" to the editor.

## When to use it
- When you want an open-source AI editor focused on understanding developer intent and long-term architectural goals.
- When you prefer a "Pair Programming" feel rather than "Autopilot" style assistance.
- For projects where data privacy, open-source compliance, and transparency are critical requirements.

## When not to use it
- When you rely on a vast library of legacy extensions only available for VS Code.
- When performing rapid, low-level edits where advanced intent tracking might introduce unwanted overhead.
- If you prefer a terminal-only workflow (use [Aider](aider.md) or [Junie CLI](junie-cli.md)).

## Getting started
### Installation
Melty is available as a standalone application or can be built from source for maximum customization.

1. **Download**: Fetch the latest release from the official Melty site or GitHub.
2. **Setup**: Follow the onboarding wizard to configure your preferred LLM provider (e.g., OpenAI, Anthropic, or local Ollama).
3. **Indexing**: Open your project folder and allow Melty to build its "Intent Index."

### Basic Workflow
As you begin typing or refactoring, look for the Melty "Intent Bar" to confirm its understanding of your task. You can explicitly override or refine the intent at any time.

## CLI examples
Melty primarily operates as a GUI editor, but it includes CLI utilities for management and integration.

### Application Launch
```bash
# Open a specific project folder in Melty
melty .
```

### Indexing Management
```bash
# Force a re-index of the current repository
melty index --force
```

### Config Management
```bash
# View the current AI provider configuration
melty config list
```

## API examples
Melty's core logic is accessible via an internal API for extension developers.

### Defining a Custom Intent Handler (TypeScript)
```typescript
import { IntentHandler } from '@melty/sdk';

export const myRefactorHandler: IntentHandler = {
  id: 'custom-refactor',
  onIntentDetected: async (intent, context) => {
    if (intent.type === 'refactor') {
      // Custom logic to guide the AI's refactoring strategy
      return context.proposeChanges('Consider using the Factory pattern here...');
    }
  }
};
```

### External Tool Integration
```bash
# Using Melty's headless mode to generate a diff based on a specific intent
melty generate --intent "Implement logger in all controllers" --apply
```

## Related tools / concepts
- [Cursor](cursor.md) — Proprietary AI-native IDE.
- [Zed](zed.md) — High-performance, collaborative AI editor.
- [Codeium](codeium.md) — Multi-IDE AI completion and chat.
- [Aider](aider.md) — Terminal-based pair programming.
- [Junie CLI](junie-cli.md) — Terminal-native AI assistant for codebase exploration.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Automated development architectures.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — High-level orchestration of AI tasks.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standard for integrating AI tools.

## Sources / references
- [Melty Labs Official Site](https://melty.sh/)
- [GitHub Repository](https://github.com/meltylabs/melty)
- [Melty Documentation Wiki](https://github.com/meltylabs/melty/wiki)
- [Melty v1.2 Release Notes](https://github.com/meltylabs/melty/releases)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
