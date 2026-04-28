# oh-my-opencode

## What it is
oh-my-opencode (also known as `omo` or `oh-my-openagent`) is a collaborative AI coding platform and ecosystem designed to bring open-source models and agentic workflows to the modern development environment. It provides a suite of tools for hosting, training, and deploying AI models specifically optimized for code generation and analysis.

## What problem it solves
It reduces the reliance on proprietary, closed-source coding assistants by providing a high-performance, open alternative that developers can trust and customize. It specifically addresses the "harness problem" by implementing specialized edit tools and multi-agent orchestration.

## Where it fits in the stack
**Development & Ops**. It provides the infrastructure and tools for AI-assisted software engineering, specifically as a plugin/extension for the OpenCode ecosystem.

## Typical use cases
- Replacing proprietary coding assistants with open-source alternatives.
- Orchestrating multiple models (Claude, Kimi, GPT, Gemini) for complex development tasks.
- Running agentic coding workflows with high autonomy ("ultrawork").

## Strengths
- Commitment to open-source models and transparency.
- **Hashline Edit Tool**: High success rate for surgical code edits by using content hashes to anchor changes.
- **Discipline Agents**: Orchestrates specialized agents (Sisyphus, Hephaestus, Prometheus) for different tasks.

## Limitations
- Heavily optimized for the OpenCode/AmpCode ecosystem.
- May require significant token budget for full multi-agent orchestration.

## When to use it
- When you want the power of AI coding assistants but require an open-source or self-hosted stack.
- For complex projects where multi-model orchestration provides better results than a single model.

## When not to use it
- If you prefer the seamless, zero-config experience of [GitHub Copilot](../development_ops/github_copilot.md) or [Cursor](../development_ops/cursor.md).
- If you do not want to manage custom agent configurations.

## Licensing and cost
- **Open Source**: Yes (SUL-1.0)
- **Cost**: Free (Core plugin), requires AI provider API keys.
- **Self-hostable**: Yes

## Getting started

### Installation via Agent
Paste this into your AI agent (Claude Code, etc.):
```text
Install and configure oh-my-opencode by following the instructions here:
https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/guide/installation.md
```

### Manual Installation
```bash
# Fetch the installation guide
curl -s https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/dev/docs/guide/installation.md
```

## CLI examples
```bash
# Execute the main ultrawork loop
omo ultrawork "Refactor the authentication logic to use JWT"

# Initialize deep project context (AGENTS.md)
omo /init-deep

# Run diagnostics
omo doctor
```

## Related tools / concepts
- [Aider](../development_ops/aider.md)
- [Continue.dev](../development_ops/continue_dev.md)
- [Claude Code](../development_ops/claude-code.md)
- [Hash-Anchored Edits](../../knowledge_base/patterns/filesystem-context.md)

## Sources / References
- [Official Website](https://ohmyopenagent.com/)
- [GitHub Repository](https://github.com/code-yeongyu/oh-my-openagent)
- [The Harness Problem](https://blog.can.ac/2026/02/12/the-harness-problem/)

## Contribution Metadata
- Last reviewed: 2026-04-28
- Confidence: high
