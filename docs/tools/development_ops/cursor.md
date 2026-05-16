# Cursor

## What it is
An AI-powered code editor built on top of VS Code. It features a native AI chat, codebase indexing for context-aware answers, and "Composer" mode for multi-file edits. It is designed to be an "AI-native" fork of VS Code rather than just an extension.

## What problem it solves
Provides a deeply integrated AI coding experience where the editor itself understands the full codebase context, enabling more accurate completions and multi-file refactors. It solves the "context fragmentation" problem where developers have to copy-paste code between their editor and a chat window.

## Where it fits in the stack
**Development & Ops**. Functions as a primary code editor with native AI capabilities, serving as the interface between the developer and the AI-augmented development lifecycle.

## Typical use cases
- **Context-Aware Completion**: Predictive typing that understands your current file and project structure.
- **Multi-File Edits**: Using "Composer" mode to apply a change across multiple files (e.g., "Add a new field to the user model and update all related API routes").
- **Codebase Q&A**: Asking questions like "Where is the authentication logic handled?" and getting specific file references.

## Strengths
- **VS Code Compatibility**: Existing extensions, themes, and keybindings work out of the box.
- **Deep Context**: Locally-stored embeddings for your entire codebase ensure the AI has relevant context.
- **Composer Mode**: High-reliability multi-file generation that can be reviewed and applied in one click.

## Limitations
- **Proprietary**: The core AI orchestration layer is closed source.
- **Subscription Model**: Full features (like indexing large repos or using advanced models) require a paid plan.
- **Cloud Dependency**: While it indexes locally, most model inference still happens on Cursor's servers.

## When to use it
- When you want an AI-native editor with deep codebase understanding and low-friction multi-file editing.
- When you are already comfortable with the VS Code ecosystem.
- For complex refactoring tasks that span many files and directories.

## When not to use it
- When you prefer a fully open-source editor (consider [Zed](zed.md) or VS Code with [Continue](continue_dev.md)).
- When you want to use strictly local LLMs for privacy or air-gapped environments (unless using specific local-mode configurations).

## Getting started

Download Cursor from the official website and sign in. On first run, it will index your codebase for AI context.

1. **Install**: Download for your OS (Windows/Mac/Linux).
2. **Index**: Let Cursor index your repository (check the status in the bottom right corner).
3. **Configure**: Add your custom instructions in `.cursorrules` to guide the AI's behavior.

## Usage examples

### .cursorrules file
Create a `.cursorrules` file in your root directory to enforce coding standards. This file is automatically read by Cursor to ground its suggestions:

```markdown
# Coding Standards for Project X
- Use TypeScript with strict mode enabled.
- Prefer functional components and Tailwind CSS.
- Ensure all business logic is in the `/services` directory.
- Use `consola` for logging instead of `console.log`.
```

### Keyboard Shortcuts for AI Features
| Action | Shortcut (Mac) | Shortcut (Windows/Linux) |
| :--- | :--- | :--- |
| **Edit code in place** | `Cmd + K` | `Ctrl + K` |
| **Chat with codebase** | `Cmd + L` | `Ctrl + L` |
| **Open Composer** | `Cmd + I` | `Ctrl + I` |
| **Apply Suggested Fix** | `Cmd + Enter` | `Ctrl + Enter` |

## Practical Notes
- Cursor is strongest when rules, project memory, and model selection are treated as part of the editor setup rather than optional extras.
- It overlaps with [Claude Code](claude-code.md) on autonomous edits, but Cursor remains more editor-centric while Claude Code remains more terminal-centric.
- It pairs well with reusable workflow systems such as [Superpowers](../agents/superpowers.md) when you want stronger process control than the editor provides by default.

## Related tools / concepts
- [VS Code](vscode.md)
- [Continue](continue_dev.md)
- [Zed](zed.md)
- [Aider](aider.md)
- [Claude Code](claude-code.md)
- [Plandex](plandex.md)
- [Windsurf](windsurf.md)

## Sources / References
- [Cursor Official Website](https://cursor.com/)
- [Cursor Documentation](https://docs.cursor.com/)
- [Cursor GitHub Community](https://github.com/getcursor/cursor)

## Contribution Metadata

- Last reviewed: 2026-05-15
- Confidence: high
