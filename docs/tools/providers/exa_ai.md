# Exa AI

## What it is
Exa AI is a search engine specifically designed for AI agents and LLMs. Unlike traditional keyword-based search engines, Exa uses embeddings-based search to find high-quality, relevant web content that is structured for machine consumption. As of June 2026, it serves as a foundational component for agentic search workflows.

## What problem it solves
Traditional search engines (like Google or Bing) are optimized for human browsing, often returning SEO-heavy pages that are difficult for LLMs to parse. Exa provides clean, structured, and parsed web data, reducing the noise and token overhead when agents perform web research. It enables agents to navigate the "live" web with semantic intent rather than just keyword matches.

## Where it fits in the stack
**Category**: [Providers](index.md) / [Search & Ingest](../process_understanding/index.md). It acts as the primary web-intelligence layer for research-capable agents and RAG pipelines requiring real-time web grounding.

## Typical use cases
- **Agentic Search**: Giving LLMs the ability to find ground-truth information on the live web via MCP 3.0.
- **Automated Research**: Compiling B2B leads, competitor analysis, or technical documentation reports.
- **Real-time Data Ingestion**: Feeding fresh web content into RAG pipelines for up-to-date context.
- **Fact Verification**: Automating the process of grounding agent claims with cited web sources.

## Strengths
- **Clean Markdown**: Directly returns LLM-ready markdown, bypassing the need for complex custom scrapers.
- **High Relevance**: Specifically finds high-signal content (blogs, docs, academic papers) instead of ads.
- **Official SDKs**: Robust support for Python, TypeScript, and native MCP 3.0 integration.
- **Neural Search**: Uses a transformer-based model to understand the semantic intent of a query.

## Limitations
- **Subscription Required**: Requires an API key and has usage-based pricing.
- **Web-Only**: Does not search private internal data (unless integrated into a custom pipeline).
- **Rate Limits**: Subject to plan-based concurrency and request limits.
- **SEO Gaps**: Occasionally misses extremely new or niche content that hasn't been indexed by its neural model yet.

## When to use it
- When your AI agent needs to perform "deep research" rather than just a quick keyword lookup.
- When you want to avoid the maintenance of a custom scraping stack (JS rendering, proxy management).
- For high-accuracy tasks where the quality of the source matters more than the volume of results.
- When implementing Agentic RAG patterns that require high-fidelity web grounding.

## When not to use it
- For simple, internal repository searches (use [ripgrep](../development_ops/ripgrep.md) instead).
- If your project is 100% offline or requires strict on-premise data boundaries.
- For extremely high-volume, low-value scraping tasks where cost is the primary constraint.

## Getting started

### Installation
```bash
pip install exa_py
```

### Basic Setup
Get your API key from the [Exa Dashboard](https://dashboard.exa.ai/) and set it as an environment variable:
```bash
export EXA_API_KEY="your_api_key_here"
```

## CLI examples
Exa can be used via its official CLI or via standard `curl` commands.

```bash
# Search using the Exa CLI
exa search "LLM observability patterns June 2026" --limit 3

# Fetch contents for a specific URL as markdown
exa contents https://docs.exa.ai/introduction --text
```

## API examples

### Basic Search (Python)
```python
from exa_py import Exa
import os

exa = Exa(os.environ["EXA_API_KEY"])

# Search for the latest AI agent frameworks
results = exa.search(
  "What are the top 5 open-source agent frameworks in June 2026?",
  num_results=5,
  use_autoprompt=True
)

for result in results.results:
  print(f"Title: {result.title}\nURL: {result.url}\n")
```

### Content Extraction
One of Exa's core strengths is the ability to get clean content directly from search results.

```python
# Search and get clean markdown content in one call
search_and_contents = exa.search_and_contents(
    "How to set up a LangGraph agent with MCP 3.0",
    num_results=1,
    text=True # Returns clean parsed text
)

print(search_and_contents.results[0].text[:500])
```

## Related tools / concepts
- [Tavily](tavily.md): A direct competitor also focused on AI search.
- [Firecrawl](../process_understanding/firecrawl.md): For crawling and scraping specific domains.
- [Crawl4AI](../process_understanding/crawl4ai.md): An open-source alternative for scraping.
- [Perplexity](perplexity.md): A consumer-facing research engine with an API.
- [Google Search](../ai_knowledge/google-search.md): Traditional search with broad coverage, now supporting Agentic Search.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md): The architectural pattern Exa often powers.
- [LangChain](../ai_knowledge/langchain.md): Frequently uses Exa as a research tool.
- [MultiOn](../agents/multion.md): Used for web interaction, often following an Exa search.
- [Jina Reader](../process_understanding/jina-reader.md): For converting URLs to markdown.

## Sources / references
- [Exa AI Official Website](https://exa.ai/)
- [Exa Documentation](https://docs.exa.ai/)
- [Exa Python SDK (GitHub)](https://github.com/exa-labs/exa-py)
- [Agentic Search Patterns (June 2026)](https://exa.ai/blog/agentic-search)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
