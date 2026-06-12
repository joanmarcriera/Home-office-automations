# Firecrawl

## What it is
Firecrawl is an API-first web scraping and crawling service that converts entire websites into clean, structured, and LLM-ready data (Markdown or JSON). It handles the complexities of modern web browsing, including JS rendering and anti-bot measures.

## What problem it solves
It eliminates the "scraping tax" for AI developers. Instead of managing Playwright/Puppeteer clusters, proxy rotations, and complex HTML cleaning, developers can use a single API call to get high-fidelity Markdown from any URL, optimized for RAG and agentic tools.

## Where it fits in the stack
**Ingest / Process & Understanding**. It serves as the primary gateway for AI agents (like Claude 4.8 and GPT-5.5) to "see" the live web through clean, structured data.

## Typical use cases
- **Agent Web Access**: Giving an MCP-enabled agent the ability to read documentation or news in real-time.
- **RAG Pipeline Ingestion**: Batch-crawling industry websites to keep a vector database updated.
- **Structured Extraction**: Using Pydantic schemas to turn messy product pages into clean JSON.
- **Site Mapping**: Rapidly discovering the entire sitemap of a domain without a full crawl.

## Strengths
- **Clean Markdown Native**: Output is specifically formatted for LLM context windows, reducing token waste.
- **MCP Native**: Provides an official Model Context Protocol server for instant integration with Claude.
- **High Reliability**: Sophisticated bypasses for Cloudflare and other advanced anti-bot systems.
- **Scalable Extraction**: v1/v2 endpoints support high-concurrency batch processing.

## Limitations
- **Latency**: Deep crawls of large sites (1,000+ pages) can take significant time.
- **Cost**: While open-source, the managed cloud version can scale in price for high-volume enterprise use.
- **Complexity of Self-Hosting**: Requires a robust Docker/Redis/Postgres stack for self-hosted production.

## When to use it
- When your AI agent needs reliable, real-time access to web content.
- When you need to extract specific JSON schemas from hundreds of different web layouts.
- When using tools that support MCP, like [Claude Code](../development_ops/claude-code.md) or [Zed](../development_ops/zed.md).

## When not to use it
- For trivial, single-page scrapes where `curl` or `BeautifulSoup` would suffice.
- When the data is available through a structured REST API (e.g., GitHub API).

## Getting started

### Installation
```bash
pip install firecrawl-py
```

### Basic Scrape (Python)
```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a URL to clean Markdown
doc = app.scrape_url("https://example.com", params={"formats": ["markdown"]})
print(doc["markdown"])
```

## CLI examples
The `firecrawl` CLI (via NPM) allows for rapid testing.

```bash
# Scrape a single page to the terminal
firecrawl scrape https://docs.firecrawl.dev

# Map a website to see all its sub-URLs
firecrawl map https://firecrawl.dev

# Search the web and return top 3 results in markdown
firecrawl search "Firecrawl vs Crawl4AI" --limit 3 --format markdown
```

## API examples

### Structured Extraction with Pydantic
Using Firecrawl's extract feature to get predictable JSON for GPT-5.5 or Claude 4.8.

```python
from firecrawl import FirecrawlApp
from pydantic import BaseModel

class ProductInfo(BaseModel):
    name: str
    price: float
    features: list[str]

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Extract structured data from a pricing page
data = app.scrape_url("https://firecrawl.dev/pricing", {
    "formats": ["json"],
    "jsonOptions": {
        "schema": ProductInfo.model_json_schema()
    }
})

print(data["json"])
```

## Related tools / concepts
- [Crawl4AI](crawl4ai.md)
- [Docling](docling.md)
- [Valyu](../ai_knowledge/valyu.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)
- [Claude Code](../development_ops/claude-code.md)
- [RAGFlow](ragflow.md)
- [Browser Use](../automation_orchestration/browser-use.md)

## Sources / references
- [Firecrawl Documentation](https://docs.firecrawl.dev/)
- [Firecrawl GitHub Repository](https://github.com/mendableai/firecrawl)
- [MCP Server for Firecrawl](https://github.com/firecrawl/mcp-server-firecrawl)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
