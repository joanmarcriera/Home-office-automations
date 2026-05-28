# NanoClaw

## What it is
NanoClaw is a lightweight, AI-native personal assistant framework designed as a secure, containerized alternative to [OpenClaw](openclaw.md). It runs on the Claude Agent SDK and prioritizes codebase simplicity and OS-level isolation.

## What problem it solves
It addresses the security risks and code complexity of heavy agent frameworks by providing a minimalist, container-first assistant that evolves through self-modification and composable skills.

## Where it fits in the stack
**Development & Ops / Personal Assistant**. It is a lightweight agent framework for individuals and developers.

## Typical use cases
- Secure, sandboxed AI assistance for personal local tasks
- Building custom multi-channel agents (WhatsApp, Telegram, etc.)
- Prototyping agent swarms in a low-complexity environment

## Strengths
- **Security-First**: Native container isolation; agents run in ephemeral Linux containers by default.
- **Minimalist**: Small codebase, easy to understand and fork.
- **Self-Modifying**: Can evolve its own features through code transformations via the [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) protocol.
- **High Efficiency**: Optimized layer templates can reduce token costs by up to 40% compared to unoptimized RAG patterns.

## Limitations
- **Claude-Centric**: Primary optimization is for Claude models; other models may require custom adapter work.
- **Self-Modification Risk**: Requires comfort with an assistant that writes its own logic (can be disabled via `NC_READONLY_MODE=true`).
- **Resource Minimums**: Requires at least 4GB RAM and Docker 24+ for the isolation layer to function correctly.

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
- Node.js 22+ (Baseline as of May 2026)
- [Claude Code](claude-code.md)
- Docker 24+ (or Apple Container on macOS)
- 4GB+ RAM

### Installation

```bash
# Clone the repository
git clone https://github.com/qwibitai/nanoclaw.git
cd nanoclaw

# Use Claude Code for guided setup
claude /setup
```

### Verifying Isolation
To ensure your agent is correctly sandboxed, run the following command within the NanoClaw environment:
```bash
nanoclaw exec "echo 'hello' > /root/secret.txt && ls /root"
```
Then verify that a new container cannot see that file.

## Related tools / concepts
- [OpenClaw](openclaw.md) (The heavier "Gateway" alternative)
- [Claude Code](claude-code.md) (Primary setup tool)
- [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) (Evolution protocol)
- [Symphony](../agents/symphony.md)
- [Jules](../ai_knowledge/jules.md) (Automated maintenance agent)
- [vLLM](../infrastructure/vllm.md) (Local inference backend)
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References

- [Official GitHub Repository](https://github.com/qwibitai/nanoclaw)
- [Official Website](https://nanoclaw.dev/)
- [NanoClaw vs OpenClaw: Security Comparison](https://screenshotone.com/blog/nanoclaw-versus-openclaw/)
- [NanoClaw Setup 2026 Guide](https://advenboost.com/nanoclaw-setup/)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
