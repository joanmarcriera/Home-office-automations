# Sweep

## What it is
Sweep is an open-source AI junior developer that transforms GitHub issues into Pull Requests. It functions as an autonomous coding agent that can search your codebase, plan changes, and implement code, acting like an extra pair of hands on your engineering team.

## What problem it solves
It automates the repetitive parts of software development, such as fixing small bugs, refactoring code, or writing documentation. By handling the initial draft of a fix or feature, Sweep reduces the time developers spend on low-level tasks and context switching.

## Where it fits in the stack
**Development & Ops / AI Developer**. It typically integrates as a GitHub App or via a CLI, providing a hands-free bridge between issue tracking and code implementation.

## Typical use cases
- **Bug Fixing**: Assigning a GitHub issue to Sweep to have it automatically identify and fix the bug.
- **Documentation Updates**: Describing a change in an issue and letting Sweep update the relevant markdown files.
- **Refactoring**: Asking Sweep to clean up a specific module or move logic to a new file.
- **Unit Test Generation**: Requesting Sweep to add test coverage for a specific component.

## Getting started

### Installation
Sweep can be used as a GitHub App or run locally via the CLI.

#### GitHub App
The easiest way is to install the Sweep GitHub App from the [GitHub Marketplace](https://github.com/marketplace/sweep-ai).

#### CLI (Local Run)
Install the Sweep CLI via pip:

```bash
pip install sweep
sweep init
```
During initialization, you will be prompted to provide your OpenAI, Anthropic, and GitHub API keys.

### Basic Usage
To run Sweep on a specific issue using the CLI:

```bash
sweep run https://github.com/ORG_NAME/REPO_NAME/issues/ISSUE_NUMBER
```

## Strengths
- **Fully Autonomous**: Moves from issue to PR without requiring constant human steering.
- **GitHub Native**: Deep integration with GitHub's issue and PR workflow.
- **Multi-file Editing**: Capable of coordinating changes across several files in a single pass.
- **Integrated Code Search**: Uses advanced search and reranking (e.g., Voyage AI) to find relevant code context.

## Limitations
- **Complexity Limits**: May struggle with very large architectural changes or deeply nuanced logic.
- **Human Review Required**: Like all AI tools, the generated PRs should be reviewed for quality and correctness.
- **Cost**: Local CLI usage consumes significant tokens from your own API keys.

## When to use it
- For routine maintenance tasks, small feature additions, and bug fixes.
- When you want to automate the transition from "issue" to "code" in your GitHub workflow.
- To provide a "first draft" of an implementation for a developer to review and refine.

## When not to use it
- For complex, high-stakes features that require deep architectural understanding.
- In repositories where automated code changes are restricted.
- When you prefer a real-time, interactive pairing experience (where [Aider](aider.md) or [Cursor](cursor.md) might be better).

## Related tools / concepts
- [Aider](aider.md): A terminal-based AI pair programmer.
- [Devin](devin.md): A high-autonomy AI software engineer.
- [OpenHands](openhands.md): An open-source platform for autonomous agents.
- [Plandex](plandex.md): An AI coding engine for complex tasks.
- [GitHub App Integration](../../knowledge_base/patterns/github-apps.md): Architectural patterns for AI-GitHub connections.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): The paradigm of autonomous code generation.
- [Claude Code](claude-code.md): Anthropic's terminal-based assistant.

## Sources / References
- [Official Website](https://sweep.dev/)
- [Sweep GitHub Repository](https://github.com/sweepai/sweep)
- [Sweep CLI Documentation](https://github.com/sweepai/sweep/discussions/3435)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
