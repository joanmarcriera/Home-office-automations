# Mycelium

## What it is
Mycelium is a Clojure-based framework and architectural pattern designed for building complex, large-scale AI applications using state machines and formal contracts.

## What problem it solves
It addresses "context rot" and cognitive saturation in LLM agents by decomposing complex software into isolated, stable subassemblies. By separating routing logic (orchestration) from implementation details (cells), it ensures that both humans and agents work within manageable, bounded contexts.

## Where it fits in the stack
**Framework / Pattern**. It provides the structural blueprint for how agents and code interact within a larger system.

## Typical use cases
- **Complex Agentic Systems**: Building software where LLMs manage multiple interdependent tasks.
- **Large-Scale Functional Applications**: Leveraging Clojure's strengths for robust, observable AI workflows.
- **Self-Correcting Loops**: Using formal contracts (Malli) to validate agent output and provide immediate feedback.

## Strengths
- **Observability**: Every state transition is traced, providing a "flight recorder" for agentic workflows.
- **Strict Contracts**: Uses Malli schemas to enforce inputs and outputs, preventing hallucinated data structures.
- **Recursive Design**: Systems built with Mycelium can themselves be treated as individual cells in larger graphs.
- **Agent Synergy**: Designed to thrive on the "ceremony" and structural planning that humans find tedious but LLMs find clarifying.

## Limitations
- **Language Barrier**: Requires knowledge of Clojure and functional programming paradigms.
- **Initial Overhead**: Requires more upfront architectural planning compared to ad-hoc "if-statement" based logic.

## When to use it
- For mission-critical AI applications where reliability and observability are paramount.
- When building systems that are too complex for a single LLM context window to manage effectively.

## When not to use it
- For simple, linear scripts or small prototypes where the architectural overhead isn't justified.
- If your development team is not comfortable with Clojure or functional patterns.

## Licensing and cost
- **Open Source**: Yes
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Maestro](https://github.com/yogthos/maestro) (underlying workflow engine)
- [Malli](https://github.com/metosin/malli) (data-driven schemas)
- [Orchestration](../automation_orchestration/index.md)

## Sources / References
- [Managing Complexity with Mycelium](https://yogthos.net/posts/2026-02-25-ai-at-scale.html)
- [Mycelium GitHub](https://github.com/yogthos/mycelium)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
