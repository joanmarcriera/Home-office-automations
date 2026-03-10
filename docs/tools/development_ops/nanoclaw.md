# NanoClaw

NanoClaw is a lightweight, AI-native personal assistant framework designed as a secure, containerized alternative to [OpenClaw](openclaw.md). It runs on the Claude Agent SDK and prioritizes codebase simplicity and OS-level isolation.

## When to use it

- When you want a personal AI assistant that can be fully understood and customized (low code complexity).
- When you require strong security via Linux container isolation (Apple Container or Docker).
- If you prefer a "skills over features" model where the assistant evolves through code transformations rather than configuration.

## When not to use it

- If you require a managed service or a complex, multi-user enterprise framework.
- If you are not comfortable with an assistant that modifies its own source code to add features.

## Key Features

- **Container Isolation**: Agents run in sandboxed Linux containers, seeing only explicitly mounted directories.
- **Skills-Based Architecture**: Uses [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) to add capabilities (e.g., `/add-whatsapp`, `/add-telegram`) by dynamically rewriting the NanoClaw codebase.
- **Multi-Channel**: Supports WhatsApp, Telegram, Discord, Slack, Gmail, and more.
- **Agent Swarms**: First personal assistant to support collaborative teams of agents.
- **Small Footprint**: Designed to be small enough for a single developer to understand the entire codebase.

## Getting started

### Requirements

- macOS or Linux
- Node.js 20+
- [Claude Code](claude-code.md)
- Docker (or Apple Container on macOS)

### Installation

```bash
git clone https://github.com/qwibitai/nanoclaw.git
cd nanoclaw
claude
```
Then run `/setup` inside the Claude CLI.

## Related tools / concepts
- [OpenClaw](openclaw.md)
- [Claude Code](claude-code.md)
- [Anthropic Agent Skills](../agents/anthropic-agent-skills.md)

## Sources / References

- [Official GitHub Repository](https://github.com/qwibitai/nanoclaw)
- [Official Website](https://nanoclaw.dev/)

## Contribution Metadata
- Last reviewed: 2026-03-09
- Confidence: high
