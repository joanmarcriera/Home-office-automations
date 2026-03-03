# Axiom Guardian MCP Server

## What it is
An MCP server that implements challenge-based request validation using Natural Language Inference (NLI) to enforce core principles.

## What problem it solves
It shifts the AI paradigm from passive compliance ("How can I help you?") to active validation ("Why are you doing this?"). It detects logical contradictions between proposed actions and configured axioms, forcing the user (or agent) to justify their actions.

## Where it fits in the stack
**Tool / Guardrail**. It provides an AI alignment and safety layer for agent actions.

## Typical use cases
- AI Safety: Challenging potentially harmful or destructive requests before execution.
- Organizational Governance: Enforcing company values in automated workflows.
- Decision Audit Trail: Forcing articulation of reasoning for high-stakes actions.
- Educational tool for training users to think through consequences.

## Strengths
- **NLI-based validation**: Uses sophisticated models (like BART-MNLI) to detect logical contradictions.
- **Iterative Dialogue**: Challenges users to justify contradictory actions through a loop.
- **Fail-Open Design**: Defaults to allowing actions if the API fails, ensuring system usability.
- **Dynamic Configuration**: Axioms can be updated at runtime.

## Limitations
- NLI mode requires an internet connection and a HuggingFace API token.
- English language only (model limitation).
- Keyword fallback mode is basic and can produce false positives.

## When to use it
- When you need to enforce a set of rules or ethical principles on AI agent behavior.
- To create a record of human justification for critical operations.

## When not to use it
- For low-stakes environments where active challenging would be an unnecessary friction.
- When an internet connection to HuggingFace is not available (unless using basic keyword mode).

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free (software); HuggingFace API costs may apply for high usage.
- **Self-hostable**: Yes

## Related tools / concepts
- [AI Alignment](../../knowledge_base/patterns/llm-trust-boundaries.md)
- [Natural Language Inference](https://huggingface.co/tasks/natural-language-inference)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)

## Sources / References
- [Axiom Guardian GitHub](https://github.com/democratize-technology/axiom-guardian)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
