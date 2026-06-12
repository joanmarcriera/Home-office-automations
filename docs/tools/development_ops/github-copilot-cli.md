# GitHub Copilot CLI

## What it is
GitHub Copilot CLI is the terminal interface for Copilot-assisted development workflows, now primarily distributed as the `gh-copilot` extension for the GitHub CLI (`gh`). It integrates frontier reasoning from models like Claude 4.8 Opus and GPT-5.5 into shell environments.

## What problem it solves
It bridges the gap between IDE-centric AI assistance and the terminal. It allows developers and agents to request command suggestions, explanations, and automation scripts without leaving the shell, maintaining flow in command-heavy workflows.

## Where it fits in the stack
**Development & Ops Tool**. It extends the Copilot ecosystem from the editor into the terminal, acting as a "Shell Agent" for both interactive use and CI/CD automation.

## Typical use cases
- **Terminal-native coding assistance**: Quickly generate complex shell commands from natural language.
- **Agent workflows**: Use Copilot within automated scripts for intelligent repository analysis.
- **Interactive Scaffolding**: Generate initial project structures or boilerplate directly from the prompt.
- **CI/CD Automation**: Integrate with GitHub Actions for automated issue triage or code summaries.

## Strengths
- **Native Ecosystem Integration**: Seamlessly shares authentication and context with other GitHub tools.
- **Explainability**: High-quality explanations for complex, obfuscated, or dangerous shell commands.
- **Extensible**: Supports custom aliases (`??`, `git?`, `gh?`) for high-speed interaction.
- **Agent-Ready**: Can be used by autonomous agents (like Claude Code) to bootstrap local environment tasks.

## Limitations
- **Account Dependency**: Requires an active GitHub Copilot subscription.
- **CLI UX Constraints**: Lacks the rich, multi-file context of IDE-based Copilot (e.g., Cursor or VS Code).
- **Network Required**: Model-backed operations require persistent internet connectivity.

## When to use it
- When you are working heavily in the terminal and need quick command syntax help.
- For teams already standardized on the GitHub/Copilot stack.
- When building shell-based automation that requires intelligent command generation.

## When not to use it
- When offline or local-only coding assistants are required (see [Aider](./aider.md) or [Ollama](../../knowledge_base/energy-anomaly-detection-baseline.md)).
- When deep, multi-file repository refactoring is the primary goal (better suited for IDE extensions).

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
Use Copilot CLI programmatically within a workflow:
```yaml
- name: Generate Repo Digest
  env:
    GITHUB_TOKEN: ${{ secrets.COPILOT_PAT }}
  run: |
    gh copilot suggest "Summarize the changes in this repository" --no-ask-user > digest.md
```

### 2. JSON Output (Mock)
> [!NOTE]
> Copilot CLI is primarily interactive. Programmatic JSON output is currently managed via standard shell redirection and `--no-ask-user` flags.

```bash
gh copilot suggest "list pods" --tool kubectl --no-ask-user
```

## Related tools / concepts
- [GitHub Copilot](github_copilot.md)
- [Aider](aider.md)
- [Codex](codex.md)
- [Claude Code](claude-code-setup.md)
- [Continue.dev](continue_dev.md)
- [Mentat](mentat.md)
- [Zed](zed.md)

## Sources / references
- [GitHub Copilot CLI GA Announcement](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)
- [GitHub Docs: Automate with Actions](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions)
- [Claude 4.8 & Copilot Integration Patterns (June 2026)](https://github.blog/2026-06-01-frontier-models-in-gh-cli)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-12
