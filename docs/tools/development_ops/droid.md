# Factory AI Droid CLI

## What it is
An AI-powered coding agent that works directly within your project to perform tasks like code reviews, security scans, and feature implementation. Droid leverages LLMs (typically Claude) to interact with your codebase and supports specialized "droids" (sub-agents) for specific domains like infrastructure, security, or frontend development.

## What problem it solves
Automates repetitive development tasks such as code review, security scanning, and feature implementation by delegating them to specialized AI sub-agents.

## Where it fits in the stack
**Development & Ops**. Acts as a CLI-based AI coding agent with domain-specific sub-agents.

## Typical use cases
- Automated code reviews and security scans
- Feature implementation via AI agents
- Domain-specific tasks using specialized droids (infrastructure, security, frontend)

## Strengths
- Specialized sub-agents for different development domains
- CLI-first design integrates well with existing workflows
- Supports GitHub Actions integration

## Limitations
- Depends on external LLM providers (typically Claude)
- Limited documentation on custom droid orchestration

## When to use it
- When you want AI-driven automation for code reviews, security scans, or feature work
- When you need domain-specific AI agents within a CI/CD pipeline

## When not to use it
- When a general-purpose AI coding assistant (e.g., GitHub Copilot) is sufficient
- When you need full control over the AI model used

## Related tools / concepts
- [Claude Code](https://github.com/anthropic/claude-code)
- [Aider](aider.md)

## Sources / references
- [Factory AI Website](https://www.factory.ai/)
- [GitHub - Droid Action](https://github.com/Factory-AI/droid-action)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
