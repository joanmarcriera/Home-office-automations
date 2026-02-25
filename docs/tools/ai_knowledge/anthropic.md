# Anthropic Claude

## What it is
Anthropic is an AI safety and research company that produces the Claude family of LLMs, known for their strong reasoning and large context windows.

## What problem it solves
Offers a high-performance alternative to OpenAI with a focus on "Constitutional AI" (safety) and exceptional performance in coding and long-form document analysis.

## Where it fits in the stack
**LLM / Reasoning Engine**. Often used as the primary engine for coding agents due to its high accuracy in code generation and refactoring.

## Architecture overview
Cloud-hosted API service (via Anthropic Console or Amazon Bedrock/Google Vertex AI).

## Typical workflows
- **Pair Programming**: Claude 3.5 Sonnet is currently a top choice for tools like Aider.
- **Complex Analysis**: Summarizing long technical documentation or legal files.
- **Strict Adherence**: Workflows requiring close following of complex formatting rules.

## Strengths
- **Coding Excellence**: Claude 3.5 Sonnet is widely regarded as one of the best models for software engineering.
- **Safety Focus**: Built with Constitutional AI principles.
- **Large Context**: Ability to handle up to 200k+ tokens.
- **Low Hallucination**: Generally exhibits high factual accuracy.

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

## Security considerations
- **Key Safety**: Protect Anthropic API keys.
- **Shared Responsibility**: Ensure data sent to the API complies with your organization's privacy standards.

## Links to related pages
- [OpenAI](openai.md)
- [OpenRouter](openrouter.md)
- [Aider](../development_ops/aider.md)
