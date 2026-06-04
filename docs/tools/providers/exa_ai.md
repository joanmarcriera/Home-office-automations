# Exa AI

## What it is
Exa AI is a search engine specifically designed for AI agents and LLMs. Unlike traditional keyword-based search engines, Exa uses embeddings-based search to find high-quality, relevant web content that is structured for machine consumption.

## What problem it solves
Traditional search engines (like Google or Bing) are optimized for human browsing, often returning SEO-heavy pages that are difficult for LLMs to parse. Exa provides clean, structured, and parsed web data, reducing the noise and token overhead when agents perform web research.

## Where it fits in the stack
**Category**: [Providers](index.md) / [Search & Ingest](../process_understanding/index.md). It acts as the primary web-intelligence layer for research-capable agents.

## Typical use cases
- **Agentic Search**: Giving LLMs the ability to find ground-truth information on the live web.
- **Automated Research**: Compiling B2B leads, competitor analysis, or technical documentation reports.
- **Real-time Data Ingestion**: Feeding fresh web content into RAG pipelines for up-to-date context.

## Technical Capabilities
- **Neural Search**: Uses a transformer-based model to understand the semantic intent of a query.
- **Structured Extraction**: The `/contents` endpoint returns clean HTML or parsed Markdown.
- **Websets**: Filtered views of the web (e.g., "all healthcare company websites").
- **Agentic Research**: Dedicated endpoints for automated, multi-step research tasks.

## Strengths
- **Clean Markdown**: Directly returns LLM-ready markdown, bypassing the need for complex custom scrapers.
- **High Relevance**: Specifically finds high-signal content (blogs, docs, academic papers) instead of ads.
- **Official SDKs**: Robust support for Python, TypeScript, and official MCP integration.

## Limitations
- **Subscription Required**: Requires an API key and has usage-based pricing.
- **Web-Only**: Does not search private internal data (unless integrated into a custom pipeline).
- **Rate Limits**: Subject to plan-based concurrency and request limits.

## When to use it
- When your AI agent needs to perform "deep research" rather than just a quick keyword lookup.
- When you want to avoid the maintenance of a custom scraping stack (JS rendering, proxy management).
- For high-accuracy tasks where the quality of the source matters more than the volume of results.

## When not to use it
- For simple, internal repository searches (use [ripgrep](../development_ops/ripgrep.md) instead).
- If your project is 100% offline or requires strict on-premise data boundaries.

## Getting started

### Installation
```bash
pip install exa_py
```

### Basic Search
```python
from exa_py import Exa

exa = Exa("YOUR_API_KEY")

# Search for the latest AI agent frameworks
results = exa.search(
  "What are the top 5 open-source agent frameworks in June 2026?",
  num_results=5,
  use_autoprompt=True
)

for result in results.results:
  print(f"Title: {result.title}\nURL: {result.url}\n")
```

## API: Content Extraction
One of Exa's core strengths is the ability to get clean content directly from search results.

```python
# Search and get clean markdown content in one call
search_and_contents = exa.search_and_contents(
    "How to set up a LangGraph agent",
    num_results=1,
    text=True # Returns clean parsed text
)

print(search_and_contents.results[0].text[:500])
```

## CLI examples
Exa can be used via its official CLI or via standard `curl` commands.

```bash
# Search using the Exa CLI
exa search "LLM observability patterns" --limit 3

# Fetch contents for a specific URL
exa contents https://docs.exa.ai/introduction
```

## Related tools / concepts
- [Tavily](tavily.md): A direct competitor also focused on AI search.
- [Firecrawl](../process_understanding/firecrawl.md): For crawling and scraping specific domains.
- [Crawl4AI](../process_understanding/crawl4ai.md): An open-source alternative for scraping.
- [Perplexity](perplexity.md): A consumer-facing research engine with an API.
- [Google Search](../ai_knowledge/google-search.md): Traditional search with broad coverage.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md): The architectural pattern Exa often powers.
- [LangChain](../ai_knowledge/langchain.md): Often uses Exa as a research tool.

## Sources / References
- [Exa AI Official Website](https://exa.ai/)
- [Exa Documentation](https://docs.exa.ai/)
- [Exa Python SDK (GitHub)](https://github.com/exa-labs/exa-py)

## Contribution Metadata
- Last reviewed: 2026-06-04
- Confidence: high
