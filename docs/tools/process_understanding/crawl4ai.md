# Crawl4AI

## What it is
Crawl4AI is an open-source, LLM-friendly web crawler and scraper designed for high-speed, structured extraction of web content into clean Markdown.

## What problem it solves
It simplifies the process of turning complex, noisy web pages into clean data formats ready for RAG (Retrieval-Augmented Generation) or LLM training.

## Where it fits in the stack
**Ingest / Process & Understanding**. It provides the crawler layer that feeds data into LLMs or vector databases.

## Typical use cases
- **RAG Data Pipelines**: Crawling documentation or news sites for vector indexing.
- **LLM Training**: Mass-collecting clean web-to-Markdown data.
- **Web Monitoring**: Tracking changes on multiple sites in real-time.
- **Structured Extraction**: Converting unstructured product or news pages into validated JSON.

## Technical Capabilities
- **AsyncWebCrawler**: High-concurrency crawling using `asyncio` and a shared browser pool.
- **Markdown V2**: Advanced HTML-to-Markdown engine that preserves tables, code blocks, and citations.
- **Deep Crawling**: Multi-strategy traversal (BFS, DFS, Best-First) with automatic filtering.
- **Structured Extraction**: Integrated CSS-based (`JsonCssExtractionStrategy`) and LLM-based extraction.
- **Adaptive Crawling**: Dynamic stopping logic based on content relevance and system resources.

## Strengths
- **Fast and Efficient**: Async-based crawling with a smart browser pool.
- **Clean Output**: Native Markdown generation with headings, tables, and code blocks preserved.
- **Zero-Key Option**: Can be run entirely for free and self-hosted with no API tokens required.
- **Huge Popularity**: One of the most-starred crawlers on GitHub (51k+ stars).

## Limitations
- **Maintenance**: Requires a browser environment (Playwright) which can be complex to manage at scale.
- **Resource Intensive**: Like all headless browser crawlers, it requires significant RAM and CPU.
- **Proxy Management**: Large-scale crawling requires external proxy or anti-bot solutions.

## When to use it
- When you need to crawl multiple pages and output clean Markdown for LLMs.
- For local, self-hosted RAG pipelines that need to ingest documentation.

## When not to use it
- For simple, static scraping that can be handled by standard HTML parsers like BeautifulSoup.
- When an official API is available for the same data source.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free (Self-hosted)
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
# Install the package
pip install -U crawl4ai

# Post-installation browser setup
crawl4ai-setup
```

### Basic usage
```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://crawl4ai.com",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples
```bash
# Basic crawl with markdown output
crwl https://crawl4ai.com -o markdown

# Deep crawl with BFS strategy, max 10 pages
crwl https://docs.crawl4ai.com --deep-crawl bfs --max-pages 10

# LLM-based extraction with a specific query
crwl https://www.example.com/products -q "Extract all product prices"
```

## API: Structured Extraction
Crawl4AI v0.8.x supports predictable JSON extraction via CSS-based schemas.

```python
import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    schema = {
        "name": "Hacker News Items",
        "baseSelector": ".athing",
        "fields": [
            {"name": "title", "selector": ".titleline > a", "type": "text"},
            {"name": "rank", "selector": ".rank", "type": "text"}
        ]
    }

    config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(schema)
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://news.ycombinator.com",
            config=config
        )
        data = json.loads(result.extracted_content)
        print(data[:3])

if __name__ == "__main__":
    asyncio.run(main())
```

## API: Deep Crawling
Deep crawling allows for automated discovery and traversal of sub-pages.

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

async def main():
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            include_external_links=False
        )
    )

    async with AsyncWebCrawler() as crawler:
        # result will contain the main page and metadata about the crawl session
        result = await crawler.arun("https://docs.crawl4ai.com", config=config)
```

## API: Multi-URL Concurrent Crawling
The `arun_many` method enables high-speed crawling of multiple targets with resource monitoring.

```python
async def main():
    urls = ["https://example.com/p1", "https://example.com/p2"]

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(urls)
        for res in results:
            print(f"URL: {res.url} | Markdown Length: {len(res.markdown)}")
```

## Related tools / concepts
- [Firecrawl](firecrawl.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [RAGFlow](../benchmarking/ragflow.md)
- [Skyvern](../automation_orchestration/skyvern.md)
- [Docling](docling.md)
- [Valyu](../ai_knowledge/valyu.md)
- [LangChain](../ai_knowledge/langchain.md)

## Sources / References
- [GitHub](https://github.com/unclecode/crawl4ai)
- [Official Website](https://crawl4ai.com/)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
