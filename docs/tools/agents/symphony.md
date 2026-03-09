# Symphony

Symphony is an autonomous implementation framework by OpenAI that turns project work into isolated, autonomous implementation runs, allowing teams to manage work instead of supervising individual coding agents.

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
- [OpenCode](opencode.md)

## Sources / References

- [Official GitHub Repository](https://github.com/openai/symphony)
- [Symphony Specification (SPEC.md)](https://github.com/openai/symphony/blob/main/SPEC.md)

## Contribution Metadata
- Last reviewed: 2026-03-09
- Confidence: high
