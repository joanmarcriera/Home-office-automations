# Tavily

## What it is
Tavily is a search and web-extraction provider built for AI agents and LLM applications. It provides a specialized API that returns cleaned, LLM-ready content from the web.

## What problem it solves
It gives agents a cleaner way to search the web and retrieve grounded results than relying on generic search scraping or brittle custom connectors. It handles JavaScript rendering, proxy rotation, and content extraction automatically.

## Where it fits in the stack
**Provider / Search API**. It is commonly used as the web-research layer inside agent or workflow systems like LangChain or CrewAI.

## Typical use cases
- Web research for agents
- Retrieval-augmented generation (RAG) with current web results
- Competitive and trend monitoring pipelines
- Automated fact-checking for LLM outputs

## Strengths
- **Agent-Optimized**: Returns content in formats that are easy for LLMs to parse and use.
- **Speed**: Optimized for low-latency search results.
- **Built-in Extraction**: Extracts main content from pages, removing ads and navigation.
- **Easy Integration**: Official SDKs for Python and JavaScript.

## Limitations
- **Cost**: Adds another paid API dependency to your stack.
- **Search Quality**: While high, it may still vary depending on the niche or domain.
- **Proprietary**: Unlike self-hosted solutions, you are dependent on their service uptime and pricing.

## When to use it
- When agents need current web results as part of their loop.
- When you want a purpose-built search layer rather than managing generic scraping.
- For production-grade agents requiring high reliability and performance.

## When not to use it
- When your corpus is entirely internal and web search is unnecessary.
- When you need a self-hosted search engine such as [SearXNG](../../services/searXNG.md).
- For very high-volume search tasks where cost becomes prohibitive.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium / Paid API (Free tier typically includes 1,000 searches/month)
- **Self-hostable**: No

## Getting started

Install the Tavily Python SDK:

```bash
pip install tavily-python
```

Initialize and run a basic search:

```python
from tavily import TavilyClient

# Initialize the client with your API key
tavily = TavilyClient(api_key="tvly-YOUR_API_KEY")

# Perform a search
response = tavily.search(query="What happened in the AI world today?")

# Print the results
for result in response['results']:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['content']}\n")
```

## API examples

### Context-based Search
Used for RAG applications to get a single string of context.

```python
context = tavily.get_search_context(query="Latest news on Claude 3.5", search_depth="advanced")
print(context)
```

### Q&A Search
Returns a direct answer to a question based on web results.

```python
answer = tavily.qna_search(query="Who won the Nobel Prize in Physics 2024?")
print(answer)
```

## Related tools / concepts
- [DeerFlow](../agents/deerflow.md)
- [SearXNG](../../services/searXNG.md)
- [Firecrawl](../process_understanding/firecrawl.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [Perplexity API](../ai_knowledge/perplexity.md)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [CrewAI Framework](../frameworks/crewai.md)

## Sources / References
- [Official Website](https://www.tavily.com/)
- [Documentation](https://docs.tavily.com/)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
