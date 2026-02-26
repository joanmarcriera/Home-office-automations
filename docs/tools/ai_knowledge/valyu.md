# Valyu

## What it is
Valyu is an AI-native search API that provides agents with access to both the open web and licensed, high-signal proprietary data sources.

## What problem it solves
It allows agents to search beyond just the current web, providing structured, high-accuracy results from datasets like PubMed, SEC filings, clinical trials, patents, arXiv, and financial data through a single, natural-language-enabled API.

## Where it fits in the stack
**AI Assistants & Knowledge / Understand (Aggregators)**. It acts as a high-signal search engine that feeds real-time context and deep research data to LLMs and agents.

## Typical use cases
- **Deep Research**: Running complex queries that require cross-referencing web search with research papers (arXiv) or patents.
- **Financial Analysis**: Extracting real-time market data or historical SEC filings.
- **Medical/Scientific Agents**: Searching PubMed or clinical trials for verified medical information.

## Strengths
- **Unified API**: Access to 36+ proprietary data sources in a single query.
- **Agent-Ready**: Returns structured, LLM-ready data rather than just links.
- **Multimodal**: Supports multimodal retrieval for deep-content extraction.
- **Alternative to Tavily/Exa**: Provides a broader data scope beyond standard web search.

## Limitations
- **Paid Service**: Requires an API key and usage-based pricing.
- **Latency**: Searching proprietary databases can sometimes be slower than simple web-index searches.
- **Closed-Source**: The search engine itself is a proprietary service.

## When to use it
- When an agent needs high-accuracy, verified data from scientific, financial, or legal sources.
- For building specialized agents (e.g., a "Scientific Research Agent") that require more than just web results.

## When not to use it
- For general, low-stakes web search where free or cheaper alternatives suffice.
- If you require a fully open-source, self-hosted search index.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Usage-based pricing with free tier)
- **Self-hostable**: No

## Related tools / concepts
- [Perplexity](perplexity.md)
- [OpenRouter](openrouter.md)
- [LlamaIndex](llamaindex.md)

## Sources / References
- [Official Website](https://www.valyu.ai/)
- [Official Docs](https://docs.valyu.ai/)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: high
