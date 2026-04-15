# GitHub Copilot CLI

## What it is
GitHub Copilot CLI is the terminal interface for Copilot-assisted development workflows.

## What problem it solves
It brings Copilot interactions into shell-driven workflows so developers and agents can request assistance without leaving the terminal.

## Where it fits in the stack
**Development & Ops Tool**. It extends Copilot from IDE-centric use into CLI-centric environments.

## Typical use cases
- Terminal-native coding assistance
- Agent workflows that call Copilot from scripts or shells
- Fast code/task prompting while staying in command-line flow
- Scheduled repository summaries or scaffolding tasks in GitHub Actions

## Automation in GitHub Actions

GitHub now documents Copilot CLI as a runner-side automation tool, not just an interactive terminal assistant. The practical pattern is:

1. Trigger a workflow on `workflow_dispatch`, a schedule, or repository events.
2. Check out the repository with enough history for the prompt to inspect.
3. Install the CLI on the runner with `npm install -g @github/copilot`.
4. Authenticate with `COPILOT_GITHUB_TOKEN`, backed by a fine-grained PAT that has the `Copilot Requests` permission.
5. Run `copilot -p ... --no-ask-user` in programmatic mode and decide whether the output should be logged, written to a file, or turned into a follow-on workflow step.

That makes Copilot CLI viable for recurring changelog generation, daily repo digests, lightweight issue triage, and other text-heavy CI tasks where a full IDE session would be unnecessary.

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

## Sources / References
- [GitHub Copilot CLI GA announcement (2026-02-25)](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)
- [GitHub Docs: automate Copilot CLI with Actions](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions)

## Contribution Metadata

- Last reviewed: 2026-03-29
- Confidence: medium
