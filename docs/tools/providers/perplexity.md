# Perplexity

## What it is
Perplexity is an AI-powered search engine and LLM provider that specializes in real-time information retrieval and cited answers. While primarily known as a search tool, it also provides an API (Sonar) that allows developers to integrate its search-augmented reasoning into their own applications.

## What problem it solves
It bridges the gap between static LLM knowledge and the live web. Traditional LLMs have knowledge cutoffs, but Perplexity can search the internet in real-time to provide up-to-date information with verifiable citations.

## Where it fits in the stack
**Category**: Provider / AI Search. It acts as a specialized inference provider for tasks that require live data, such as news analysis, market research, or technical troubleshooting for new releases.

## Typical use cases
- **Research Agents**: Automating the collection of cited information for reports.
- **Support Bots**: Providing accurate, up-to-date answers about products or services.
- **Technical Research**: Finding the latest documentation or API changes that occurred after an LLM's cutoff date.
- **Financial Analysis**: Using the `finance_search` tool to pull structured market data and transcripts.
- **Autonomous Browsing**: Leveraging the "Computer" orchestration layer for multi-step web research.

## Strengths
- **Live Web Access**: Exceptional at fetching and summarizing real-time data.
- **Citations**: Automatically provides links to the sources used to generate answers.
- **OpenAI Compatibility**: Its API is compatible with the OpenAI SDK, making it easy to swap in.
- **Reasoning Models**: Offers **Sonar Reasoning Pro** which combines deep chain-of-thought with live search.
- **Tool Integration**: Native support for financial data connectors (FactSet, Morningstar, etc.).

## Model Routing (June 2026)

### Sonar Small / Medium
- Use for: fast, high-volume search tasks and simple extraction.
- Default? No.

### Sonar Reasoning
- Use for: standard research tasks requiring a balance of speed and depth.
- Default? Yes.

### Sonar Reasoning Pro
- Use for: complex, multi-step research, deep analysis, and high-stakes reasoning tasks.
- Default? No (Premium).

### Agent API
- Supports third-party models like [Claude Opus 4.7](anthropic.md) and [GPT-5.5](../ai_knowledge/openai.md) for tool-calling and structured outputs.

## Limitations
- **Rate Limits**: API rate limits can be restrictive for high-volume applications.
- **Cost**: Perplexity Pro subscription includes some API credits, but heavy usage requires separate billing.
- **Latency**: Search-augmented reasoning takes longer than a simple LLM inference call.

## When to use it
- When the accuracy of real-time information is more important than raw inference speed.
- When you need to verify the sources of an AI-generated answer.
- For "Daily Briefing" or "Market Analysis" workflows.
- For [n8n](../../services/n8n.md) workflows using the native Perplexity node.

## When not to use it
- For general creative writing or purely local processing tasks.
- When latency is a critical factor (e.g., real-time chat UI).

## Getting started

### API Setup
1. Get an API key from the [Perplexity Settings](https://www.perplexity.ai/settings/api).
2. Install the OpenAI SDK: `pip install openai`.

### Python Example
```python
from openai import OpenAI

PPLX_API_KEY = "your-api-key"

client = OpenAI(api_key=PPLX_API_KEY, base_url="https://api.perplexity.ai")

# Chat completion with search-augmented reasoning
response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[
        {"role": "system", "content": "Be precise and cited."},
        {"role": "user", "content": "What are the latest developments in the Model Context Protocol as of June 2026?"}
    ]
)

print(response.choices[0].message.content)
```

## Licensing and cost
- **Open Source**: No (Proprietary)
- **Cost**: Paid API (Usage-based; Perplexity Pro subscription benefits available)
- **Self-hostable**: No (Cloud service)

## Related tools / concepts
- [Tavily](tavily.md) (Search-optimized API)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Google Search](../ai_knowledge/google-search.md)
- [n8n](../../services/n8n.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Daily Briefing Prompt](../../reference-implementations/llm-prompts/daily-briefing.md)
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)

## Sources / References
- [Official Website](https://www.perplexity.ai/)
- [API Documentation](https://docs.perplexity.ai/)
- [Model Catalog](https://docs.perplexity.ai/docs/model-cards)
- [Sonar Reasoning Pro Reference](https://docs.perplexity.ai/docs/sonar/models/sonar-reasoning-pro)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
