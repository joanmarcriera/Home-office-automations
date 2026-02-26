# LLM Trust Boundaries Pattern

## What it is
A prompt-architecture pattern that explicitly distinguishes trusted instructions from untrusted content passed to the model (for example, web pages, emails, or retrieved documents).

## What problem it solves
Prompt-injection attacks exploit ambiguous instruction boundaries. Explicit trust-boundary framing reduces the chance that untrusted text is executed as authority.

## Where it fits in the stack
**Pattern**. This belongs in agent security, tool-calling safety, and context construction.

## Typical use cases
- Agentic web browsing workflows
- Email and document ingestion pipelines
- Multi-source RAG and tool orchestration setups

## Strengths
- Improves model clarity around authority boundaries
- Works with existing API patterns and system prompts
- Pairs well with sandboxing and tool allowlists

## Limitations
- Not a complete defense against prompt injection
- Requires consistent implementation across all ingestion paths
- May add complexity to prompt and middleware design

## When to use it
- Whenever agents process mixed-trust inputs before taking actions
- When designing high-risk automations with external content

## When not to use it
- Never skip this pattern in production agent systems with external inputs
- Only de-prioritize in closed, single-trust offline experiments

## Related tools / concepts
- [LLM Security & Privacy](../llm_security_privacy.md)
- [Claude Tool Search Pattern](claude-tool-search.md)
- [Patterns Index](index.md)

## Sources / References
- [What if LLMs Could See Trust Boundaries?](https://rockwotj.com/blog/llm-trust-boundaries/)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: high
