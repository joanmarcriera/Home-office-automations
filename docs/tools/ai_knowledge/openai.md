# OpenAI

## What it is
OpenAI is a leading AI research and deployment company that provides high-performance Large Language Models (LLMs), including the GPT-5 family and coding-specialized model lines.

## What problem it solves
Provides state-of-the-art reasoning, coding, and instruction-following capabilities via a reliable API, enabling complex automation and agentic workflows.

## Where it fits in the stack
**LLM / Reasoning Engine**. It serves as the "brain" that processes information, plans actions, and generates code or commands for agents to execute.

## Architecture overview
Cloud-hosted API service. Agents send prompts (context + instructions) to OpenAI's endpoints and receive structured or natural language responses.

## Typical workflows
- **Code Generation**: Used by agents like Aider or OpenHands to write and refactor code.
- **Infrastructure Planning**: Reasoning about system state and proposing shell commands.
- **Data Extraction**: Converting unstructured documents (scans, emails) into structured JSON.

## Strengths
- **State-of-the-art performance**: Strong reasoning, coding, and tool-use capabilities across the GPT-5 family.
- **Large context windows**: Support for processing large codebases or multiple documents.
- **Tool use (Function Calling)**: Robust support for structured output and calling external tools.
- **Reliability**: Highly available API with predictable latency.

## Limitations
- **Privacy**: Data is processed on OpenAI servers (though API data is generally not used for training by default on enterprise/tier accounts).
- **Cost**: Can become expensive with high-volume agentic loops.
- **Dependency**: Requires active internet connection and relies on a third-party provider.

## When to use it
- When maximum reasoning power is required for complex tasks.
- For production-grade automations where reliability is paramount.
- When needing to process very large contexts that local models can't handle yet.

## Effort-level routing

### GPT-5.4 `low`
- Use for: straightforward serious work where you still want GPT-5.4 quality
- Default? No
- Comment: good first pass when latency and cost matter

### GPT-5.4 `medium`
- Use for: the default OpenAI lane for planning, debugging, analysis, and non-trivial implementation help
- Default? Yes
- Comment: best general OpenAI default

### GPT-5.4 `high`
- Use for: hard reasoning, difficult debugging, deeper architecture analysis
- Default? No
- Comment: use when `medium` is not holding up

### GPT-5.4 `xhigh`
- Use for: explicit last-step escalation on very hard or very important reasoning tasks
- Default? No
- Comment: avoid using this as background default because it adds cost and latency quickly

### GPT-5.3 Codex
- Use for: code-specialized generation and editing
- Default? Only for code-centric lanes
- Comment: use this when the task is mostly code, not broad general reasoning

See the central routing guide: [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## When not to use it
- For processing highly sensitive/private data that must remain on-premises.
- When working offline or in air-gapped environments.
- For high-frequency, simple tasks where a cheaper or local model would suffice.

## Security considerations
- **API Key Management**: Never hardcode keys; use environment variables or secret managers.
- **Data Privacy**: Review OpenAI's data usage policy; ensure sensitive PII is redacted if necessary.
- **Prompt Injection**: Be aware that models can be manipulated via input; implement output validation.

## Related tools / concepts
- [Anthropic](../providers/anthropic.md)
- [Mistral AI](../providers/mistral.md)
- [OpenRouter](openrouter.md)
- [Aider](../development_ops/aider.md)
- [OpenHands](../development_ops/openhands.md)
- [SSH Execution Patterns](../../architecture/ssh_execution_patterns.md)
- [OpenAI Codex](../development_ops/codex.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## Sources / References

- [OpenAI](https://openai.com/)
- [Models Overview](https://platform.openai.com/docs/models)
- [Reasoning Guide](https://platform.openai.com/docs/guides/reasoning)
- [Codex](https://openai.com/codex/)

## Contribution Metadata

- Last reviewed: 2026-03-15
- Confidence: medium
