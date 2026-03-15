# Anthropic Claude

## What it is
Anthropic is an AI safety and research company that produces the Claude family of LLMs, known for strong reasoning, coding performance, and large context windows.

## What problem it solves
Offers a high-performance alternative to OpenAI with a focus on "Constitutional AI" (safety) and exceptional performance in coding, long-form document analysis, and complex reasoning tasks.

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. Often used as the primary engine for coding agents due to its high accuracy in code generation and refactoring.

## Typical use cases
- **Pair Programming**: Sonnet is typically the default Claude lane for tools like [Aider](../development_ops/aider.md).
- **Complex Analysis**: Summarizing long technical documentation or legal files.
- **Strict Adherence**: Workflows requiring close following of complex formatting rules.

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
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)
```

## Strengths
- **Coding Excellence**: Sonnet is widely regarded as one of the strongest daily-driver models for software engineering.
- **Safety Focus**: Built with Constitutional AI principles for better alignment and safety.
- **Large Context**: Ability to handle up to 200k+ tokens (and expanding).
- **Low Hallucination**: Generally exhibits high factual accuracy and honesty.
- **Pricing Tiers**: Offers a competitive range from the low-cost **Haiku** (high speed, low cost) to the flagship **Sonnet** (balanced performance/cost) and **Opus** (most capable/expensive).

## Model routing

### Haiku
- Use for: fast classification, extraction, rewriting, and cheap high-volume tasks
- Default? No
- Comment: use when throughput matters more than deep reasoning

### Sonnet
- Use for: default coding, planning, document reasoning, and most daily serious work
- Default? Yes
- Comment: best Claude default for mixed quality/cost work

### Opus
- Use for: premium escalation on hard synthesis, difficult reasoning, or high-stakes final passes
- Default? No
- Comment: use only after Sonnet fails or when the answer quality matters enough to justify the premium

See the central routing guide: [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## Limitations
- **Cloud Dependency**: Requires external API access (proprietary, closed-source).
- **Rate Limits**: Can be stricter than OpenAI on lower usage tiers.
- **Cost**: High-end models like Opus are significantly more expensive than smaller models.

## When to use it
- For software development tasks where Sonnet is the right default
- When safety and alignment are critical priorities for your application.
- For analyzing very long documents or entire codebases in a single context.
- When you want a three-tier routing strategy: Haiku for cheap work, Sonnet for defaults, Opus for escalation

## When not to use it
- When a local/offline solution is required for privacy or cost.
- If you need native image generation (DALL-E style) in the same API call.

## Licensing and cost
- **Open Source**: No (Proprietary)
- **Cost**: Paid (Usage-based pricing; free tier available via console for testing)
- **Self-hostable**: No (Cloud service)

## Related tools / concepts
- [OpenAI](../ai_knowledge/openai.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Aider](../development_ops/aider.md)
- [Mistral AI](mistral.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## Sources / References
- [Official Website](https://www.anthropic.com/)
- [Anthropic News](https://www.anthropic.com/news)
- [API Documentation](https://docs.anthropic.com/)
- [Models Overview](https://docs.anthropic.com/en/docs/about-claude/models/overview)

## Contribution Metadata
- Last reviewed: 2026-03-15
- Confidence: high
