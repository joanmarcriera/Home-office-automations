# Google Gemini CLI

## What it is
Google Gemini CLI is an open-source AI agent that brings the power of the Gemini model family directly into the terminal and GitHub workflows. It acts as both a standalone CLI tool for local development and a set of GitHub Actions for repository automation.

## What problem it solves
It streamlines the developer workflow by providing immediate access to AI assistance for coding, refactoring, and documentation without leaving the terminal. In CI/CD, it automates repetitive tasks like issue triaging and pull request reviews.

## Where it fits in the stack
**Tool / Agent / Developer Experience (DX)**.

## Typical use cases
- **Terminal Assistant**: Direct terminal interactions for code generation and command explanation.
- **Pull Request Reviewer**: Automating code reviews via GitHub Actions by commenting on diffs.
- **Issue Triager**: Analyzing new issues, labeling them, and suggesting fixes.
- **Batch Code Modification**: Using agentic capabilities to refactor code across multiple files.

## Strengths
- **Native Integration**: Developed by Google, ensuring first-class support for Gemini models.
- **GitHub Actions Native**: Specifically designed to work within GitHub's ecosystem.
- **Project Context**: Uses a `GEMINI.md` file (similar to `AGENTS.md`) to follow repository-specific rules.
- **Tool Calling**: Can interact with other CLI tools (like `gh` CLI) to perform complex actions.

## Limitations
- **Internet Dependency**: Requires a connection to Google AI Studio or Vertex AI.
- **Token Usage**: Large codebases can consume significant quotas/costs depending on the model used (though AI Studio has generous free tiers).
- **Environment**: Optimized for Unix-like environments and specific Node.js versions.

## When to use it
- To automate repository maintenance tasks on GitHub.
- For a lightweight, terminal-based alternative to heavy AI IDEs like Cursor.

## When not to use it
- In strictly offline environments.
- If you prefer a full GUI-based AI coding experience.

## Getting started

### Installation
```bash
npm install -g @google/gemini-cli
```

### Basic Usage
```bash
gemini "Refactor this python script to use async/await"
```

### GitHub Action Setup
Initialize the configuration in your repository:
```bash
gemini setup-github
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free (using Google AI Studio quotas) or Paid (via Vertex AI).
- **Self-hostable**: Yes (the CLI itself).

## Related tools / concepts
- [Google Gemini](google-gemini.md) (Underlying Model)
- [Aider](../agents/aider.md) (Terminal-based agent)
- [Claude Code](../development_ops/claude-code.md) (Anthropic's equivalent)

## Sources / References
- [Gemini CLI Documentation](https://geminicli.com/)
- [Official GitHub](https://github.com/google-gemini/gemini-cli)
- [GitHub Marketplace Action](https://github.com/marketplace/actions/run-gemini-cli)

## Contribution Metadata
- Last reviewed: 2026-04-28
- Confidence: high
