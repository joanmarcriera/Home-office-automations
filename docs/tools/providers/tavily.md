# Tavily

## What it is
Tavily is a search and web-extraction provider built specifically for AI agents and LLM applications. As of February 2026, it is a part of **Nebius Group** following a $275M+ acquisition. It provides a specialized API that returns structured, cleaned, and LLM-ready content from the live web.

## What problem it solves
It gives agents a reliable way to search the web and retrieve grounded results without the "glue code" burden of generic search scraping. It handles JavaScript rendering, proxy rotation, and content extraction automatically, delivering citation-ready results with minimal latency.

## Where it fits in the stack
**Provider / Search API**. It sits at the **Retrieval Layer**, acting as the primary gateway for agents to access real-time information outside their training data.

## Typical use cases
- **Agentic Research**: Powering multi-step research loops that search from multiple angles and synthesize findings.
- **Real-time RAG**: Providing fresh web context for retrieval-augmented generation in production applications.
- **Competitive Intelligence**: Automated monitoring of news, trends, and competitor activity with high-fidelity extraction.
- **Automated Fact-Checking**: Grounding LLM outputs in verified web sources to reduce hallucinations.

## Strengths
- **RAG-Native Structured Retrieval**: Returns results in JSON with summaries, citations, and highlights optimized for LLM consumption.
- **Nebius Cloud Integration**: Now part of a larger AI cloud ecosystem (Nebius), ensuring enterprise-grade scale and performance.
- **Managed Research Endpoint**: The `/research` endpoint allows generating entire research reports in a single API call.
- **Official Vercel AI SDK Support**: Native integration with the Vercel AI SDK for building streaming agentic web apps.
- **Citation Ready**: Results include high-confidence provenance and source metadata by default.

## Limitations
- **Acquisition Uncertainty**: Following the 2026 acquisition by Nebius, the pricing and product roadmap for the free/indie tier may evolve.
- **Search Latency**: While advanced search depth is thorough, it can introduce latency (often ~1s) that needs to be managed in real-time loops.

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
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md)
- [DeerFlow](../agents/deerflow.md)
- [SearXNG](../../services/searXNG.md)
- [Firecrawl](../process_understanding/firecrawl.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [Perplexity API](../ai_knowledge/perplexity.md)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Exa AI](../providers/exa_ai.md)

## Sources / References
- [Official Website](https://www.tavily.com/)
- [Documentation](https://docs.tavily.com/)
- [Nebius to acquire Tavily (Calcalist)](https://www.calcalistech.com/ctechnews/article/r168bhodbe)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
