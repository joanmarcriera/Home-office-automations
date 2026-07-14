# Crawl4AI

## What it is
Crawl4AI is an open-source, high-performance web crawler designed specifically for LLM applications. It provides a robust, asynchronous interface for converting complex web pages into clean, structured Markdown or JSON. In June 2026, it is a primary tool for feeding `claude-4-8-opus-20260528` and GPT-5.5 with real-time web data.

## What problem it solves
It solves the "LLM context clutter" problem. Modern web pages are filled with ads, tracking scripts, and complex layouts that waste tokens. Crawl4AI uses advanced filtering and layout-aware parsing to ensure that only relevant content is extracted, making it ideal for RAG pipelines and agentic search.

## Where it fits in the stack
**Ingest / Process & Understanding**. It provides a self-hosted, local-first alternative to managed services like [Firecrawl](firecrawl.md), supporting MCP 3.0 for seamless agentic integration.

## Typical use cases
- **Local RAG Ingestion**: Crawling entire documentation sets for local vector indexing.
- **Agentic Search**: Providing a "search and read" tool for autonomous agents using Claude 4.8 or GPT-5.5.
- **Batch Dataset Collection**: Gathering large amounts of high-quality Markdown for fine-tuning or training.
- **Dynamic Content Extraction**: Handling JavaScript-heavy SPAs (Single Page Applications) that standard scrapers cannot read.

## Strengths
- **Async Efficiency**: Built on `asyncio` with a smart browser pool (Playwright) for high-concurrency crawling.
- **Markdown V2**: Native engine that preserves tables, citations, and nested structures with minimal token footprint.
- **Zero-Cost**: Completely open-source and self-hostable with no API keys or subscription fees.
- **Extensible Extraction**: Built-in support for CSS-based and LLM-based extraction strategies.

## Limitations
- **Resource Intensive**: Requires significant RAM and CPU to run multiple headless browser instances.
- **Maintenance**: Users are responsible for proxy rotation and managing Playwright dependencies.
- **Learning Curve**: The asynchronous API and configuration options are more complex than simple REST-based scrapers.

## When to use it
- When you need a high-speed, self-hosted crawler for private or large-scale data ingestion.
- When budget is a primary concern and you have the infrastructure to host a Playwright-based stack.
- For local agentic workflows where data privacy is paramount.

## When not to use it
- For lightweight, static site scraping (use BeautifulSoup).
- When you prefer a "pay-as-you-go" managed service with guaranteed anti-bot bypass (use [Firecrawl](firecrawl.md)).

## Getting started

### Installation
```bash
pip install crawl4ai
crawl4ai-setup  # Installs Playwright browsers
```

### Basic Async Usage
```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://crawl4ai.com")
        print(result.markdown[:500])

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples
The `crwl` command provides a quick way to interact with the crawler.

```bash
# Scrape a single URL to a markdown file
crwl https://crawl4ai.com -o result.md

# Deep crawl a documentation site with BFS strategy
crwl https://docs.crawl4ai.com --deep-crawl bfs --max-depth 2

# Extract data using a natural language query
crwl https://news.ycombinator.com -q "Extract the top 5 story titles and their points"
```

## API examples

### Concurrent Multi-URL Crawl
Efficiently crawling multiple documentation pages for a RAG update.

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl_docs():
    urls = [
        "https://docs.crawl4ai.com/basic-usage",
        "https://docs.crawl4ai.com/advanced-extraction",
        "https://docs.crawl4ai.com/configuration"
    ]

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(urls)
        for res in results:
            print(f"URL: {res.url} | Status: {res.success}")

if __name__ == "__main__":
    asyncio.run(crawl_docs())
```

## Related tools / concepts
- [Firecrawl](firecrawl.md)
- [Docling](docling.md)
- [Playwright](https://playwright.dev/)
- [RAGFlow](ragflow.md)
- [Valyu](../ai_knowledge/valyu.md)
- [LangChain](../ai_knowledge/langchain.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / references
- [Crawl4AI Official Documentation](https://docs.crawl4ai.com/)
- [GitHub Repository](https://github.com/unclecode/crawl4ai)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
