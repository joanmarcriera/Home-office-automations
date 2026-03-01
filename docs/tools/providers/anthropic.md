# Anthropic Claude

## What it is
Anthropic is an AI safety and research company that produces the Claude family of LLMs, known for their strong reasoning and large context windows.

## What problem it solves
Offers a high-performance alternative to OpenAI with a focus on "Constitutional AI" (safety) and exceptional performance in coding and long-form document analysis.

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. Often used as the primary engine for coding agents due to its high accuracy in code generation and refactoring.

## Typical use cases
- **Pair Programming**: Claude 3.5 Sonnet is currently a top choice for tools like Aider.
- **Complex Analysis**: Summarizing long technical documentation or legal files.
- **Strict Adherence**: Workflows requiring close following of complex formatting rules.

## Getting started
Install the SDK:
```bash
pip install anthropic
```

Basic API call:
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)
```

## Strengths
- **Coding Excellence**: Claude 3.5 Sonnet is widely regarded as one of the best models for software engineering.
- **Safety Focus**: Built with Constitutional AI principles.
- **Large Context**: Ability to handle up to 200k+ tokens.
- **Low Hallucination**: Generally exhibits high factual accuracy.
- **Pricing Tiers**: Offers a competitive range from the low-cost **Haiku** (high speed) to the flagship **Sonnet** (balanced) and **Opus** (most capable/expensive).

## Limitations
- **Cloud Dependency**: Similar to OpenAI, requires external API access.
- **Rate Limits**: Can be stricter than OpenAI on lower tiers.
- **Cost**: High-end models (Opus) can be expensive.

## When to use it
- For software development tasks (Sonnet 3.5).
- When safety and alignment are critical priorities.
- For analyzing very long documents or codebases.

## When not to use it
- When a local/offline solution is required.
- If already deeply integrated into another provider's ecosystem with significant credits.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Usage-based pricing; free tier available via console for testing)
- **Self-hostable**: No (Cloud service)

## Related tools / concepts
- [OpenAI](../ai_knowledge/openai.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Aider](../development_ops/aider.md)

## Sources / References
- [Official Website](https://www.anthropic.com/)
- [Anthropic News](https://www.anthropic.com/news)
- [API Documentation](https://docs.anthropic.com/)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
