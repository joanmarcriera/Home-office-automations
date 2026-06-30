# GitHub Copilot CLI

## What it is
GitHub Copilot CLI is the terminal interface for Copilot-assisted development workflows, now primarily distributed as the `gh-copilot` extension for the GitHub CLI (`gh`). It integrates frontier reasoning from models like Claude 4.8 Opus and GPT-5.5 into shell environments. As of June 2026, it supports [MCP 3.0](../automation_orchestration/mcp.md) for tool-augmented command generation.

## What problem it solves
It bridges the gap between IDE-centric AI assistance and the terminal. It allows developers and agents to request command suggestions, explanations, and automation scripts without leaving the shell, maintaining flow in command-heavy workflows while reducing syntax errors in complex CLI tools.

## Where it fits in the stack
**Development & Ops Tool**. It extends the Copilot ecosystem from the editor into the terminal, acting as a "Shell Agent" for both interactive use and CI/CD automation.

## Typical use cases
- **Terminal-native coding assistance**: Quickly generate complex shell commands from natural language prompts.
- **Agent workflows**: Use Copilot within automated scripts for intelligent repository analysis and environment setup.
- **Interactive Scaffolding**: Generate initial project structures or boilerplate directly from the terminal.
- **CI/CD Automation**: Integrate with GitHub Actions for automated issue triage, code summaries, and release management.

## Strengths
- **Native Ecosystem Integration**: Seamlessly shares authentication and context with other GitHub tools and services.
- **Explainability**: High-quality explanations for complex, obfuscated, or potentially dangerous shell commands.
- **Extensible**: Supports custom aliases (`??`, `git?`, `gh?`) for high-speed, low-friction terminal interaction.
- **Agent-Ready**: Can be utilized by autonomous agents (like [Claude Code](./claude-code.md)) to bootstrap local environment tasks.

## Limitations
- **Account Dependency**: Requires an active GitHub Copilot subscription for all features.
- **CLI UX Constraints**: Lacks the rich, multi-file context of IDE-based Copilot (e.g., [Cursor](./cursor.md) or [VS Code](./vscode.md)).
- **Network Required**: Model-backed operations require persistent internet connectivity for inference.

## When to use it
- When you are working heavily in the terminal and need quick command syntax help for tools like `kubectl`, `docker`, or `git`.
- For teams already standardized on the GitHub/Copilot stack who want a unified AI assistant.
- When building shell-based automation that requires intelligent command generation and reasoning.

## When not to use it
- When offline or local-only coding assistants are required (see [Aider](./aider.md) or [Local LLMs](../ai_knowledge/local_llms.md)).
- When deep, multi-file repository refactoring is the primary goal (better suited for IDE extensions or dedicated agents).

## Getting started

### 1. Installation
Install via the GitHub CLI extension manager:
```bash
gh extension install github/gh-copilot
```

### 2. Authentication
Log in with your GitHub account:
```bash
gh auth login
```

### 3. Hello World
Ask for a basic command suggestion:
```bash
gh copilot suggest "list all markdown files modified in the last 2 days"
```

## CLI examples

### 1. Explaining a Complex Pipe
Understand what a dangerous-looking command does before running it:
```bash
gh copilot explain "find . -name '*.log' -delete"
```

### 2. Shell Aliases
Add ergonomics to your `.zshrc` or `.bashrc`:
```bash
eval "$(gh copilot alias -- bash)"
# Now use short syntax:
?? "how do i revert my last commit?"
```

### 3. Targeted Suggestion
Get help specific to a tool ecosystem:
```bash
gh copilot suggest "create a new release" --tool gh
```

## API examples

### 1. GitHub Actions Integration
Use Copilot CLI programmatically within a workflow for intelligent automation:
```yaml
- name: Generate Repo Digest
  env:
    GITHUB_TOKEN: ${{ secrets.COPILOT_PAT }}
  run: |
    gh copilot suggest "Summarize the changes in this repository" --no-ask-user > digest.md
```

### 2. Batch Processing with Shell
Programmatically generate and execute commands for batch operations:
```bash
# Generate a script to clean up Docker resources and execute it
gh copilot suggest "remove all unused docker volumes and images older than 1 week" --no-ask-user > cleanup.sh
bash cleanup.sh
```

## Related tools / concepts
- [GitHub Copilot](./github_copilot.md)
- [Aider](./aider.md)
- [Claude Code](./claude-code.md)
- [Continue.dev](./continue_dev.md)
- [Cursor](./cursor.md)
- [VS Code](./vscode.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / references
- [GitHub Copilot CLI GA Announcement](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)
- [GitHub Docs: Automate with Actions](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions)
- [Claude 4.8 & Copilot Integration Patterns (June 2026)](https://github.blog/2026-06-01-frontier-models-in-gh-cli)

## Contribution Metadata
- Last reviewed: 2026-06-30
- Confidence: high
