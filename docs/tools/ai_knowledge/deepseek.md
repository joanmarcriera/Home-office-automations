# DeepSeek

## What it is
DeepSeek is an AI research company that provides powerful open-weight and API-based models, particularly strong in coding and mathematics.

## What problem it solves
Provides extremely high-performance LLMs (rivaling GPT-4/Claude 3.5) at a significantly lower cost point, making high-volume agentic loops more affordable.

## Where it fits in the stack
**LLM / Reasoning Engine**. A cost-effective alternative for coding agents and complex reasoning tasks.

## Architecture overview
Available via their own API (DeepSeek Platform) or can be self-hosted using the open-weight versions (DeepSeek-V3, DeepSeek-Coder-V2).

## Typical workflows
- **Massive Refactoring**: Using high-performance models for large-scale code changes without the high cost of OpenAI/Anthropic.
- **Math/Logic Tasks**: Leveraging DeepSeek's strong performance in logic-heavy domains.
- **Cheap Agentic Exploration**: Running agents in "discovery" modes where many API calls are expected.

## Strengths
- **Incredible Price/Performance**: Often 1/10th or less of the cost of competitors for similar performance.
- **Coding Performance**: DeepSeek-Coder series is top-tier.
- **Open Weights**: Allows for self-hosting on high-end hardware.

## Limitations
- **Region/Availability**: Can sometimes experience higher latency or downtime depending on API region.
- **Model Bias**: May have different behavioral nuances compared to Western-developed models.

## When to use it
- When cost is a major factor in scaling agentic workflows.
- For specialized coding tasks where DeepSeek-Coder excels.
- When you want to experiment with high-end reasoning without a large budget.

## When not to use it
- If your security policy restricts data flow to certain regions/providers.
- When absolute maximum reliability (SLA) is required (OpenAI/Anthropic are generally more stable).

## Security considerations
- **API Privacy**: Review their data handling and privacy policy.
- **Key Management**: Use standard secret management practices.

## Links to related pages
- [OpenAI](openai.md)
- [Anthropic](../providers/anthropic.md)
- [Local LLMs](local_llms.md)

## Sources / References

- [Reference](https://github.com/joanmarcriera/Home-office-automations)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
