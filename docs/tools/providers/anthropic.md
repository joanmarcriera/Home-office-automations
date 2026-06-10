# Anthropic Claude

## What it is
Anthropic is an AI safety and research company that produces the Claude family of LLMs, known for strong reasoning, coding performance, and large context windows.

## What problem it solves
Offers a high-performance alternative to OpenAI with a focus on "Constitutional AI" (safety) and exceptional performance in coding, long-form document analysis, and complex reasoning tasks.

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. Often used as the primary engine for coding agents due to its high accuracy in code generation and refactoring.

## Typical use cases
- **Pair Programming**: Sonnet and Opus are the default Claude lanes for tools like [Aider](../development_ops/aider.md).
- **Complex Analysis**: Summarizing long technical documentation or legal files.
- **Strict Adherence**: Workflows requiring close following of complex formatting rules.
- **Autonomous Engineering**: Using the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) to enable Claude to interact with local and remote tools.

## Getting started
Install the SDK:
```bash
pip install anthropic
```

Basic API call (Python):
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-latest", # Or "claude-4-8-opus-20260528"
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)
```

## Strengths
- **Coding Excellence**: Widely regarded as one of the strongest daily-driver models for software engineering.
- **Safety Focus**: Built with Constitutional AI principles for better alignment and safety.
- **Large Context**: Ability to handle up to 200k+ tokens (and expanding).
- **Low Hallucination**: Generally exhibits high factual accuracy and honesty.
- **Native MCP Support**: Seamless integration with the Model Context Protocol for tool use.

## Model routing (June 2026)

### Haiku
- Use for: fast classification, extraction, rewriting, and cheap high-volume tasks
- Default? No
- Comment: use when throughput matters more than deep reasoning

### Sonnet
- Use for: default coding, planning, document reasoning, and most daily serious work
- Default? Yes
- Comment: best Claude default for mixed quality/cost work

### Opus 4.7
- Use for: complex software engineering and long-running coding tasks.
- Default? No
- Comment: Released in April 2026, improved vision and high-resolution image analysis.

### Opus 4.8
- Use for: premium escalation on hard synthesis, autonomous engineering, and browser-agent tasks.
- Default? No
- Comment: Released in May 2026. The frontier model for reliability in agentic workloads and computer use.

### Mythos
- Use for: frontier-scale simulations, extreme context tasks, and high-reliability software factory architectures
- Default? No
- Comment: The successor to Opus for the most demanding agentic workloads.

See the central routing guide: [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## Limitations
- **Cloud Dependency**: Requires external API access (proprietary, closed-source).
- **Rate Limits**: Can be stricter than OpenAI on lower usage tiers.
- **Cost**: High-end models like Opus 4.8 are significantly more expensive than smaller models.

## When to use it
- For software development tasks where Sonnet/Opus is the right default.
- When safety and alignment are critical priorities for your application.
- For analyzing very long documents or entire codebases in a single context.
- When you want a multi-tier routing strategy: Haiku for cheap work, Sonnet for defaults, Opus for escalation.

## When not to use it
- When a local/offline solution is required for privacy or cost (consider [Llama 4 Maverick](../ai_knowledge/local_llms.md)).
- If you need native image generation (DALL-E style) in the same API call.

## Licensing and cost
- **Open Source**: No (Proprietary)
- **Cost**: Paid (Usage-based pricing; free tier available via console for testing)
- **Self-hostable**: No (Cloud service)

## Related tools / concepts
- [OpenAI](../ai_knowledge/openai.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Aider](../development_ops/aider.md)
- [MCP](../automation_orchestration/mcp.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)
- [Prompt Requests](../../knowledge_base/patterns/prompt_requests.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Daily Briefing Prompt](../../reference-implementations/llm-prompts/daily-briefing.md)
- [Claude Skills](../../../skills.md)

## Sources / References
- [Official Website](https://www.anthropic.com/)
- [Anthropic News](https://www.anthropic.com/news)
- [API Documentation](https://docs.anthropic.com/)
- [Introducing Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
