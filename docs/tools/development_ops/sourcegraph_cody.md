# Sourcegraph Cody

## What it is
Cody is an AI coding assistant developed by Sourcegraph that leverages a comprehensive "Code Graph" to provide context-aware answers and completions. Unlike tools that only see the currently open file, Cody understands your entire codebase, including documentation, symbols, and dependencies.

## What problem it solves
It solves the problem of "disconnected context" in AI coding. By grounding its responses in the full codebase index, Cody provides more accurate and relevant suggestions than file-level tools. It helps developers understand large, complex repositories, find relevant code segments, and write code that follows project-specific patterns.

## Where it fits in the stack
**Development & Ops**. It functions as a codebase-aware AI assistant that can be integrated into IDEs (VS Code, JetBrains) or used via Sourcegraph's web interface for enterprise-scale code navigation.

## Typical use cases
- **Codebase Q&A**: Asking questions like "How is authentication handled in this project?"
- **Context-Aware Completions**: Generating code that uses existing project utilities and follows established styles.
- **Unit Test Generation**: Creating tests that use project-specific mocks and data structures.
- **Legacy Code Understanding**: Navigating and explaining poorly documented parts of a large monolith.

## Strengths
- **Deep Context**: Uses Sourcegraph's powerful indexing to retrieve context from across the entire repository.
- **Multi-Repo Awareness**: Can pull context from multiple related repositories in enterprise environments.
- **Flexibility**: Supports various LLMs (Claude, GPT-4, etc.) as the underlying reasoning engine.
- **Documentation Grounding**: Can be configured to index project documentation (Markdown, Notion) alongside code.

## Limitations
- **Indexing Overhead**: Requires a Sourcegraph instance (local or cloud) to maintain the code graph for full functionality.
- **Proprietary**: While it has a free tier, the most powerful codebase-aware features are gated behind paid or enterprise plans.

## When to use it
- When working in large, complex codebases where file-level context is insufficient.
- When you need an AI that "knows" your project's internal libraries and architectural patterns.
- If you already use Sourcegraph for code search.

## When not to use it
- For small projects or single-file scripts where simpler tools like Codeium or Copilot are faster to set up.
- If you cannot allow external indexing of your codebase (though self-hosted Sourcegraph mitigates this).

## Getting started

### VS Code Setup
1. Install the "Cody AI" extension from the Marketplace.
2. Sign in to Sourcegraph (Cloud or your private instance).
3. Open a workspace; Cody will begin indexing files in the background to build local context.

### Indexing External Documentation
In the Cody chat sidebar, you can use the `@` symbol to reference specific files, or use the "Context" settings to add external documentation URLs for Cody to index and use as grounding.

## Technical Examples

### Cody CLI (Context Fetching)
The Cody CLI allows you to fetch context-aware answers from the terminal:
```bash
# Ask a question grounded in the current repository
cody chat -m "How do I add a new API route in this project?"

# Generate a commit message based on staged changes
cody commit
```

### Configuration (cody.json)
You can customize Cody's behavior for your project using a `.vscode/cody.json` file:
```json
{
  "cody.chat.pre-instruction": "Always use the functional programming patterns found in src/utils/ when suggesting code.",
  "cody.codebase": "github.com/sourcegraph/cody"
}
```

## Related tools / concepts
- [Sourcegraph](https://sourcegraph.com) (parent platform)
- [GitHub Copilot](github_copilot.md)
- [Codeium](./codeium.md)
- [Cursor](./cursor.md)
- [Zed](./zed.md)
- [Claude Code — Project Setup Guide](claude-code-setup.md)
- [OpenCode (Oh My OpenCode Ecosystem)](opencode.md)
- [Aider](../development_ops/aider.md)

## Sources / references
- [Official Website](https://about.sourcegraph.com/cody)
- [Cody Documentation](https://sourcegraph.com/docs/cody)
- [Cody GitHub](https://github.com/sourcegraph/cody)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
