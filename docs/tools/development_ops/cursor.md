# Cursor

## What it is
Cursor is an AI-native code editor built on top of Visual Studio Code. It is designed to integrate large language models deeply into the development process.

## What problem it solves
It solves the "context gap" in traditional code editors by providing a built-in AI that understands the entire codebase, making it much faster to refactor, write tests, and explore complex projects.

## Where it fits in the pipeline
**Reason / Act (Development)**

## Typical use cases (in this homelab / family automation context)
- **Repo-Wide Refactoring**: Asking the AI to update all home automation scripts to use a new API or pattern.
- **Natural Language Coding**: Describing a new feature for a homelab dashboard and having the AI generate the boilerplate and logic.
- **Bug Discovery**: Asking the AI to analyze a failing script and suggest a fix based on project context.

## Integration points
- **VS Code Extensions**: Compatible with almost all existing VS Code extensions.
- **GitHub**: Integrated for code synchronization and PR management.
- **Custom LLM Backends**: Allows users to use their own API keys for OpenAI or Anthropic.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium
- **Free tier**: Yes (Limited AI requests per month).
- **Self-hostable**: No

## Strengths
- Unmatched "project-wide" context awareness.
- Beautifully integrated AI chat and inline editing.
- Built on VS Code, so the transition for existing users is seamless.

## Limitations
- Proprietary software.
- High-level features require a subscription.

## Alternatives / Related tools
- **VS Code** (with AI extensions)
- **Zed**
- **Aider**

## Links
- [Official Website](https://cursor.sh/)
