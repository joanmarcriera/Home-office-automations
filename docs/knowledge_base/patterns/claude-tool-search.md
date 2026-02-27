# Claude Tool Search Pattern

## What it is
A tool-selection pattern where Claude discovers and chooses tools based on task intent, tool metadata, and iterative execution feedback.

## What problem it solves
Naive tool-calling can fail when many tools overlap or when tool descriptions are incomplete. Tool search improves reliability by making selection explicit and model-guided.

## Where it fits in the stack
**Pattern**. This sits in the agent planning and tool-routing layer.

## Typical use cases
- Large tool catalogs where direct single-shot tool choice is brittle
- Agent loops that need better first-tool accuracy
- Dynamic environments where tool availability changes over time

## Strengths
- Better tool recall in broad catalogs
- More transparent routing behavior when instrumented
- Compatible with iterative agent loops

## Limitations
- Can add token and latency overhead
- Still sensitive to poor tool descriptions/schemas
- Needs guardrails to prevent tool overuse

## When to use it
- When an agent can call many tools and quality depends on choosing the right one
- When task-to-tool mapping is ambiguous

## When not to use it
- When only one deterministic tool exists for a task
- When ultra-low-latency responses are the main constraint

## Related tools / concepts
- [Anthropic Claude](../../tools/providers/anthropic.md)
- [Agent Protocols](../agent_protocols.md)
- [Patterns Index](index.md)

## Sources / References
- [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
