# OpenSwarm

## What it is
OpenSwarm is a multi-agent orchestrator for the Claude CLI, designed specifically for managing workflows on platforms like Linear and GitHub.

## What problem it solves
It simplifies the coordination of multiple AI agents performing complex, interdependent tasks across project management and version control systems, reducing the manual overhead of managing individual agent runs.

## Where it fits in the stack
**Agent / Orchestrator**. It acts as a control layer that directs Claude-based agents to execute specific actions within a developer's workflow.

## Typical use cases
- **Automated Issue Management**: Using agents to triage, label, and respond to Linear issues.
- **Pull Request Orchestration**: Coordinating multiple agents to review code, run tests, and suggest improvements on GitHub.
- **CLI-based Agent Loops**: Running complex multi-step agentic tasks directly from the terminal.

## Strengths
- **Native Claude CLI Integration**: Leverages the power of Anthropic's official CLI tools.
- **Workflow Focused**: Specifically tuned for the tools developers use most (Linear, GitHub).
- **Open Source**: Allows for community customization and extension.

## Limitations
- **Narrow Ecosystem**: Primarily focused on Linear and GitHub; may require custom work for other integrations.
- **Dependency**: Highly dependent on the stability and features of the Claude CLI.

## When to use it
- When you need to coordinate multiple agentic tasks across Linear and GitHub using Claude.
- For developers looking for a CLI-first approach to multi-agent orchestration.

## When not to use it
- For general-purpose automation that doesn't involve the Claude CLI.
- When working with platforms not yet supported by the OpenSwarm ecosystem.

## Licensing and cost
- **Open Source**: Yes (MIT/Apache 2.0 typically for such projects)
- **Cost**: Free (software), but requires Anthropic API credits.
- **Self-hostable**: Yes

## Related tools / concepts
- [Claude Code](./claude-code.md)
- [Anthropic](../ai_knowledge/anthropic.md)
- [Multi-Agent Systems](../../knowledge_base/agent_protocols.md)

## Sources / References
- [OpenSwarm GitHub](https://github.com/Intrect-io/OpenSwarm)
