# Symphony

## What it is
Symphony is an autonomous implementation framework by OpenAI that turns project work into isolated, autonomous implementation runs, allowing teams to manage work instead of supervising individual coding agents.

## What problem it solves
It solves the "supervision bottleneck" in agentic software engineering by shifting the human role from direct supervision to high-level work item management, relying on "harness engineering" for verification.

## Where it fits in the stack
**Agents / Orchestration Framework**. It manages the lifecycle of implementation runs within a software factory model.

## Typical use cases
- Automating the transition from issue tracker (e.g., Linear) to pull request
- Managing fleets of agents working in parallel on isolated features or bug fixes
- Enforcing standardized proof-of-work (CI, walkthroughs) for AI-generated code

## Strengths
- Highly scalable autonomous implementation model
- Language-agnostic specification (`SPEC.md`)
- Focuses on verifiable proof-of-work rather than chat-based interaction

## Limitations
- Strong dependency on robust "harness engineering" (comprehensive tests and CI)
- Reference implementation is experimental (Elixir-based)

## When to use it

- When you want to move from micro-managing coding agents to managing high-level work items.
- In codebases that have adopted [harness engineering](https://openai.com/index/harness-engineering/).
- When you need isolated environments for agentic implementation tasks.

## When not to use it

- In small projects where manual agent supervision is not a bottleneck.
- In environments where "harness engineering" (comprehensive testing and CI) is not yet established.

## Key Features

- **Autonomous Implementation Runs**: Spawns agents to handle tasks from a work board (e.g., Linear).
- **Proof of Work**: Agents provide CI status, PR review feedback, complexity analysis, and walkthrough videos.
- **Safe Landing**: Agents can land PRs safely once accepted.
- **Spec-Driven**: Can be implemented in any language following the [Symphony Spec](https://github.com/openai/symphony/blob/main/SPEC.md).

## Getting started

### Requirements

- A codebase with established CI and testing harnesses.
- An environment capable of running the Symphony reference implementation (Elixir-based).

### Installation

Symphony offers two primary paths:

1.  **Reference Implementation**: Use the experimental Elixir-based implementation provided in the [official repository](https://github.com/openai/symphony/tree/main/elixir).
2.  **Custom Implementation**: Use the [Symphony Specification](https://github.com/openai/symphony/blob/main/SPEC.md) to build your own implementation in your preferred programming language.

## Related tools / concepts

- [Harness Engineering (OpenAI Blog)](https://openai.com/index/harness-engineering/)
- [OpenCode](../development_ops/opencode.md)
- [LangGraph](langgraph.md)
- [Bee Agent Framework](bee-agent-framework.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [NanoClaw](../development_ops/nanoclaw.md)
## Sources / References

- [Official GitHub Repository](https://github.com/openai/symphony)
- [Symphony Specification (SPEC.md)](https://github.com/openai/symphony/blob/main/SPEC.md)

## Contribution Metadata
- Last reviewed: 2026-03-09
- Confidence: high
