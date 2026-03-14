# Tavily

## What it is
Tavily is a search and web-extraction provider built for AI agents and LLM applications.

## What problem it solves
It gives agents a cleaner way to search the web and retrieve grounded results than relying on generic search scraping or brittle custom connectors.

## Where it fits in the stack
**Provider / Search API**. It is commonly used as the web-research layer inside agent or workflow systems.

## Typical use cases
- Web research for agents
- Retrieval-augmented generation with current web results
- Competitive and trend monitoring pipelines

## Strengths
- Designed for AI-agent use cases
- Simple integration path for search-backed workflows
- Good fit for research and monitoring agents

## Limitations
- Adds another paid API dependency to your stack
- Search quality and coverage still need evaluation against your domain

## When to use it
- When agents need current web results as part of their loop
- When you want a purpose-built search layer rather than generic scraping

## When not to use it
- When your corpus is entirely internal and web search is unnecessary
- When you need a self-hosted search engine such as [SearXNG](../../services/searXNG.md)

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium / Paid API
- **Self-hostable**: No

## Related tools / concepts
- [DeerFlow](../agents/deerflow.md)
- [SearXNG](../../services/searXNG.md)
- [Firecrawl](../process_understanding/firecrawl.md)

## Sources / References
- [Official Website](https://www.tavily.com/)
- [Documentation](https://docs.tavily.com/)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: high
