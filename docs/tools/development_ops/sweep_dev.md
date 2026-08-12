# Sweep

## What it is
Sweep is an AI "junior developer" that automates the process of transforming GitHub issues into Pull Requests. It monitors a repository's issue tracker and, when triggered, analyzes the codebase to implement the requested fix or feature, handling the entire lifecycle from triage to code generation and PR creation.

## What problem it solves
It automates the conversion of GitHub issues into working pull requests, reducing the manual effort of triaging and implementing straightforward bug fixes and feature requests. Sweep helps teams maintain a "zero backlog" state by handling the smaller, well-defined tasks that often pile up.

## Where it fits in the stack
**Development & Ops**. Acts as an automated AI agent that integrates directly into the GitHub workflow, sitting at the intersection of issue management and version control.

## Typical use cases
- **Bug Fix Automation**: Automatically generating PRs for well-described bugs.
- **Small Feature Requests**: Implementing incremental features directly from a GitHub issue description.
- **Code Debt Reduction**: Using Sweep to handle repetitive refactoring or documentation updates via issues.
- **Initial Triaging**: Letting Sweep provide a "first pass" implementation for review.

## Strengths
- **Native GitHub Integration**: seamless workflow within the tools developers already use.
- **End-to-End Automation**: Handles cloning, branching, coding, and PR creation without human intervention.
- **"Sweep Rules"**: Allows defining project-specific coding standards that the agent must follow.
- **Interactive PRs**: Users can comment on the generated PR, and Sweep will iterate on the code.
- **Frontier Model Support**: Utilizes [Claude 5.1](../providers/anthropic.md) and [GPT-5.5](../ai_knowledge/openai.md) for complex reasoning tasks.

## Limitations
- **Scope Restriction**: Primarily optimized for tasks that can be completed in a few hundred lines of code.
- **Complexity Cap**: May struggle with architectural changes or issues requiring deep domain-specific "tribal knowledge".
- **Platform Dependency**: Currently exclusive to GitHub.

## When to use it
- When you have a backlog of well-defined GitHub issues that need straightforward fixes.
- When you want to automate "standard" tasks like adding new API endpoints or updating UI components based on clear requirements.
- For open-source projects where maintainers want to provide contributors with a base implementation to start from.

## When not to use it
- When issues require complex, multi-step architectural reasoning or cross-repository dependencies.
- When your primary issue tracker or version control system is not GitHub (e.g., GitLab, Bitbucket).

## Getting started

### Installation
Sweep is primarily used via its GitHub App.

1. **Install GitHub App**: Go to [Sweep's GitHub App page](https://github.com/apps/sweep-ai) and install it on your repository.
2. **Configure Rules**: Create a `.sweep.yaml` file in your repository root to define coding standards.
3. **Trigger**: Label an issue with `sweep` or tag `@sweepai` in an issue comment.

### Initial Configuration (`.sweep.yaml`)
```yaml
# .sweep.yaml example
branch: "main"
rules:
  - "Always use functional components for React."
  - "All new API endpoints must include a unit test in tests/api/."
  - "Follow the project's contribution metadata format: Last reviewed: YYYY-MM-DD."
exclude:
  - "node_modules/**"
  - "docs/assets/**"
description: "A junior developer agent for repo maintenance."
```

## CLI examples

### Triggering Sweep via GitHub CLI
You can use the GitHub CLI to trigger Sweep by adding the appropriate label to an issue:

```bash
# Add the 'sweep' label to trigger the agent
gh issue edit 123 --add-label "sweep"

# Comment on an issue to give Sweep specific instructions
gh issue comment 123 --body "@sweepai please refactor this to use the new API"

# List issues currently being handled by Sweep
gh issue list --label "sweep"
```

## API examples

### Integration via GitHub Actions
Trigger Sweep automatically or manually via GitHub Actions to maintain a "zero-backlog" state:

```yaml
# .github/workflows/sweep.yml
on:
  issues:
    types: [labeled]

jobs:
  sweep:
    if: github.event.label.name == 'sweep'
    runs-on: ubuntu-latest
    steps:
      - name: Sweep
        uses: sweepai/sweep-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          sweep_api_key: ${{ secrets.SWEEP_API_KEY }}
```

### Programmatic Python Rule Validator (Pydantic v2)
Validate Sweep rule structures programmatically to ensure perfect alignment with repository configuration requirements:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class SweepRuleConfig(BaseModel):
    branch: str = Field(default="main")
    rules: List[str] = Field(default_factory=list)
    exclude: List[str] = Field(default_factory=list)
    description: Optional[str] = Field(None)

# Validate config structure
yaml_data = {
    "branch": "main",
    "rules": [
        "Always use functional components.",
        "Include unit tests."
    ],
    "exclude": ["node_modules/**"],
    "description": "Auto-maintenance junior developer configuration"
}

config = SweepRuleConfig.model_validate(yaml_data)
print(f"Target Branch: {config.branch}")
print(f"Loaded {len(config.rules)} active rules")
```

## Related tools / concepts
- [Aider](aider.md) — For interactive, developer-led terminal editing.
- [Mentat](./mentat.md) — Multi-file terminal-based AI editing.
- [Plandex](./plandex.md) — For complex, multi-file plan-based refactoring.
- [Claude Code](./claude-code.md) — Anthropic's agentic coding CLI.
- [OpenSwarm](./openswarm.md) — For orchestrating multi-agent development loops.
- [Superconductor](./superconductor.md) — High-speed parallel agent sessions.
- [Jules](../ai_knowledge/jules.md) — Internal repository agent for maintenance and triage.
- [Codeium](codeium.md) — For general-purpose IDE AI assistance.
- [Claude Hooks](claude-hooks.md) — For middleware and session management.
- [Free Will MCP](free-will-mcp.md) — For AI autonomy and self-prompting.

## Sources / references
- [Official Website](https://sweep.dev/)
- [Sweep Documentation](https://docs.sweep.dev/)
- [GitHub Repository](https://github.com/sweepai/sweep)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
