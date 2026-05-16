# GitHub Copilot CLI

## What it is
GitHub Copilot CLI is the terminal interface for Copilot-assisted development workflows.

## What problem it solves
It brings Copilot interactions into shell-driven workflows so developers and agents can request assistance without leaving the terminal.

## Where it fits in the stack
**Development & Ops Tool**. It extends Copilot from IDE-centric use into CLI-centric environments.

## Typical use cases
- **Terminal-native coding assistance**: Quickly generate shell commands or code snippets.
- **Agent workflows**: Use Copilot within automated scripts or agent-driven shell sessions.
- **Interactive Scaffolding**: Generate initial project structures or complex boilerplate.
- **CI/CD Automation**: Use Copilot CLI in GitHub Actions for intelligent repository analysis.

## Getting started

GitHub Copilot CLI is now primarily distributed as an extension for the GitHub CLI (`gh`).

### 1. Installation
Ensure you have the [GitHub CLI](https://cli.github.com/) installed, then add the Copilot extension:

```bash
gh extension install github/gh-copilot
```

### 2. Authentication
Authenticate with your GitHub account:

```bash
gh auth login
```

### 3. Usage
Access the CLI via the `gh copilot` command:

```bash
# Get help with a shell command
gh copilot suggest "find all large files in the current directory"

# Explain a complex command
gh copilot explain "ps aux | grep node"
```

## Technical examples

### 1. Custom Shell Aliases
To improve ergonomics, add aliases to your shell configuration (`.zshrc` or `.bashrc`):

```bash
# Add to ~/.zshrc or ~/.bashrc
eval "$(gh copilot alias -- bash)"
```

This provides the following commands:
- `??`: Suggest a command.
- `git?`: Suggest a Git command.
- `gh?`: Suggest a GitHub CLI command.

Example usage:
```bash
?? "undo my last 3 git commits"
```

### 2. Programmatic Automation in GitHub Actions
Copilot CLI can be used for runner-side automation (e.g., daily repo digests or issue triage).

```yaml
# .github/workflows/copilot-digest.yml
jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Copilot CLI
        run: gh extension install github/gh-copilot
      - name: Generate Digest
        env:
          GITHUB_TOKEN: ${{ secrets.COPILOT_PAT }}
        run: |
          gh copilot suggest "Summarize the changes in this repository over the last 24 hours" --no-ask-user > daily_digest.md
```

## Strengths
- Native fit for terminal-heavy engineering workflows
- Shares Copilot ecosystem and account model
- Useful for teams standardizing on GitHub-native tooling

## Limitations
- Requires GitHub/Copilot account setup and permissions
- CLI ergonomics and capabilities differ from full IDE experiences
- Network dependency for model-backed operations

## When to use it
- When teams are already invested in Copilot and want CLI usage
- When agent workflows must remain shell-first

## When not to use it
- When offline/local-only coding assistants are required
- When editor-native context and UX are the priority

## Licensing and cost
- **Open Source**: No (product feature in GitHub ecosystem)
- **Cost**: Paid Copilot plans (subject to GitHub plan terms)
- **Self-hostable**: No

## Related tools / concepts
- [GitHub Copilot](github_copilot.md)
- [Aider](aider.md)
- [Codex](codex.md)
- [Claude Code](claude-code-setup.md)
- [Continue.dev](continue_dev.md)
- [Mentat](mentat.md)
- [Zed](zed.md)

## Sources / References
- [GitHub Copilot CLI GA announcement (2026-02-25)](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)
- [GitHub Docs: automate Copilot CLI with Actions](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
