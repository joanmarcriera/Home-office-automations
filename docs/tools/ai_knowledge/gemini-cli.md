# Google Gemini CLI

## What it is
**Google Gemini CLI** is a high-performance terminal interface and agentic toolkit that brings the Gemini model family directly into developer workflows and CI/CD pipelines. It acts as both a standalone CLI assistant for local development and a suite of GitHub Actions for automated repository management.

## What problem it solves
It eliminates the "context switching" penalty by allowing developers to access state-of-the-art AI for code generation, explanation, and refactoring without leaving the terminal. In CI/CD, it automates high-volume maintenance tasks like issue triaging, PR reviews, and changelog generation.

## Where it fits in the stack
**Category**: Tool / Agent / Developer Experience (DX). It serves as a bridge between the local terminal environment and Google's Vertex AI / AI Studio infrastructure.

## Key Features (May 2026)
- **Subagent Protocol**: Support for spawning specialized sub-agents to handle complex, multi-step tasks (e.g., "Refactor this API and update all dependent tests").
- **Native GitHub Action**: Deep integration for automated pull request summaries and "smart" issue labeling.
- **Session Export/Import**: Ability to save complex agentic sessions and resume them across different machines or team members.
- **Node.js 24 Baseline**: Optimized for the latest Node.js LTS, providing improved performance and security for local executions.
- **Vertex AI & AI Studio Support**: Seamlessly switch between enterprise-grade Vertex AI and the developer-friendly Google AI Studio.
- **Long Context Native**: Designed to leverage the 1M+ token context windows of Gemini 1.5/2.0+ models for full-project analysis.

## Typical use cases
- **Terminal Engineering Assistant**: Asking "Explain why this Docker build is failing" by piping logs directly into the CLI.
- **Automated PR Reviewer**: Using the `gemini-review` action to identify logic flaws and style violations in new code submissions.
- **Interactive Refactoring**: Using the agentic mode to "Upgrade all React components in this folder to use the new useFormStatus hook."
- **Knowledge Synthesis**: Summarizing long documentation threads or technical specs into actionable TODO lists.

## Strengths
- **Google Ecosystem Integration**: First-class support for new Gemini features (e.g., ground-truth search, code execution).
- **Speed**: Extremely low latency when using the 'Gemini Flash' model family.
- **Context Handling**: Better at analyzing large repositories compared to agents with smaller context windows.
- **Extensible**: Supports custom `.geminirc` configurations and repository-specific `GEMINI.md` rules.

## Limitations
- **Internet Requirement**: Requires an active connection to Google's AI APIs (Vertex or AI Studio).
- **Rate Limits**: Free-tier AI Studio usage is generous but subject to RPM (Requests Per Minute) limits.
- **Privacy Trade-offs**: Unless using Enterprise Vertex AI, data usage policies should be reviewed for sensitive codebases.

## When to use it
- To automate high-volume repository maintenance on GitHub.
- For a lightweight, CLI-native alternative to heavy AI IDEs.
- When working with very large files or projects that exceed the context limits of other agents.

## When not to use it
- In offline or air-gapped development environments.
- If your organization has a hard prohibition on using Google Cloud / Vertex AI services.
- For tasks requiring specialized non-LLM tools not yet supported by the Gemini tool-calling ecosystem.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free (via Google AI Studio quotas) or Pay-as-you-go (via Vertex AI).
- **Self-hostable**: Yes (the CLI client).

## Getting started (CLI)

### Installation
Ensure you have Node.js 24+ installed.
```bash
npm install -g @google/gemini-cli
```

### Basic Usage
```bash
# Set your API Key
export GEMINI_API_KEY="your_key_here"

# Ask a coding question
gemini "How do I implement a rate-limiter in Go using middleware?"

# Refactor a file
gemini --file app.py "Refactor this to use the repository pattern"
```

### Agentic Mode (Subagents)
```bash
# Spawn a subagent to handle a complex task
gemini "Find all deprecated API calls in /src and create a migration plan" --agentic
```

## GitHub Action Example
Add this to your `.github/workflows/ai-review.yml`:

```yaml
name: Gemini PR Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Gemini Review
        uses: google-github-actions/run-gemini-cli@v1
        with:
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          prompt: "Review this PR for security vulnerabilities and performance bottlenecks."
        env:
          FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
```

## Related tools / concepts
- [Google Gemini](google-gemini.md) — The underlying model family.
- [Aider](../development_ops/aider.md) — Alternative terminal-based agent.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's CLI-native agent.
- [Vertex AI](../providers/google-vertex-ai.md) — Enterprise-grade hosting for Gemini.

## Sources / References
- [Official GitHub Repository](https://github.com/google-gemini/gemini-cli)
- [Google AI Studio Console](https://aistudio.google.com/)
- [Gemini CLI v0.43 Release Notes](https://releasebot.io/updates/google/gemini-cli)
- [GitHub Blog: Node.js 20 Deprecation](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)

## Contribution Metadata
- Last reviewed: 2026-05-29
- Confidence: high
