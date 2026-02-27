# Cursor

## What it is
An AI-powered code editor built on top of VS Code. It features a native AI chat, codebase indexing for context-aware answers, and "Composer" mode for multi-file edits.

## What problem it solves
Provides a deeply integrated AI coding experience where the editor itself understands the full codebase context, enabling more accurate completions and multi-file refactors.

## Where it fits in the stack
**Development & Ops**. Functions as a primary code editor with native AI capabilities.

## Typical use cases
- Context-aware code completion using codebase indexing
- Multi-file edits via Composer mode
- AI chat grounded in the current project

## Strengths
- Built on VS Code, so existing extensions and settings transfer easily
- Codebase indexing provides deep context for AI responses
- Composer mode supports complex, multi-file changes

## Limitations
- Proprietary; requires a subscription for full features
- Dependent on external AI providers for model inference

## When to use it
- When you want an AI-native editor with deep codebase understanding
- When performing frequent multi-file refactors or large-scale edits

## When not to use it
- When you prefer a fully open-source editor
- When you want to use only local LLMs without cloud dependencies

## Getting started

Download Cursor from the official website and sign in. On first run, it will index your codebase for AI context.

1. **Install**: Download for your OS (Windows/Mac/Linux).
2. **Index**: Let Cursor index your repository (check the status in the bottom right corner).
3. **Configure**: Add your custom instructions in `.cursorrules` to guide the AI.

## Usage examples

### .cursorrules setup
Create a `.cursorrules` file in your root directory to enforce coding standards:
```markdown
# Coding Standards
- Use TypeScript for all new files.
- Prefer functional components over classes.
- Use Tailwind CSS for styling.
- Ensure all functions have JSDoc comments.
```

### AI Keyboard Shortcuts
| Action | Shortcut (Mac) | Shortcut (Windows/Linux) |
| :--- | :--- | :--- |
| **Edit code in place** | `Cmd + K` | `Ctrl + K` |
| **Chat with codebase** | `Cmd + L` | `Ctrl + L` |
| **Open Composer** | `Cmd + I` | `Ctrl + I` |

## Related tools / concepts
- [VS Code](vscode.md) + [Continue](continue_dev.md)
- [Zed](zed.md)

## Sources / references
- [Reference](https://cursor.com/)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: medium
