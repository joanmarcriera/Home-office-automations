# Firecrawl

## What it is
Firecrawl is an API-first web scraping and crawling service that converts entire websites into clean, structured, and LLM-ready data (Markdown or JSON).

## What problem it solves
It abstracts away the complexities of modern web scraping, including JS rendering, anti-bot detection, and proxy management, providing a single endpoint for high-quality web data.

## Where it fits in the stack
**Ingest / Process & Understanding**. It provides a hosted or self-hosted API for web-to-LLM data pipelines.

## Typical use cases
- **AI Agent Context**: Enabling agents to "read" a website URL by sending a request to the Firecrawl API.
- **Structured Extraction**: Extracting data from many sites into a uniform JSON schema.
- **RAG Workflows**: Feeding clean Markdown from many URLs into vector databases.

## Technical Capabilities
- **Scrape**: High-fidelity conversion of single URLs to Markdown, HTML, or structured JSON.
- **Crawl**: Recursive traversal of entire domains with controlled depth and concurrency.
- **Map**: Instant discovery of site structure and all sub-URLs without full page rendering.
- **Extract**: AI-powered structured data extraction using Pydantic schemas (67% token reduction vs. full scrape).
- **Search**: Real-time web search that returns full page content for top results.

## Strengths
- **Managed Reliability**: Handled anti-bot, IP rotation, and dynamic JS rendering.
- **MCP Support**: Official Firecrawl MCP server for easy integration with Claude.
- **Self-Hostable**: While it has a popular cloud version, it's also fully open-source (Docker-based).
- **Popularity**: Highly starred (85k+) and widely used in AI developer communities.

## Limitations
- **API Latency**: Crawling large sites can take time, though it supports batch scraping.
- **Cost**: Managed version can become expensive for high volumes.
- **Maintenance**: Self-hosting requires a complex Docker Compose setup with PostgreSQL and Redis.

## When to use it
- When you need a reliable, high-uptime API for scraping many different websites.
- For integrating web search and scraping directly into AI agents via MCP.

## When not to use it
- For small-scale, simple scraping where a library like `BeautifulSoup` or `Crawl4AI` suffices.
- When an official, structured data API (like a company's REST API) is available.

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0)
- **Cost**: Free (Self-hosted) / Paid (Cloud Tier)
- **Self-hostable**: Yes

## Getting started

### Installation

**Python SDK:**
```bash
pip install firecrawl-py
```

**CLI (via NPM):**
```bash
npm install -g firecrawl-cli
```

### Basic usage
```python
from firecrawl import Firecrawl

app = Firecrawl(api_key="YOUR_API_KEY")

# Scrape a single URL
doc = app.scrape("https://firecrawl.dev", formats=["markdown"])
print(doc.markdown)
```

## CLI examples
The CLI requires the `firecrawl-cli` NPM package.

```bash
# Scrape a URL to markdown
firecrawl scrape https://firecrawl.dev

# Search the web and return 5 results
firecrawl search "firecrawl" --limit 5

# Crawl an entire website
firecrawl crawl https://docs.firecrawl.dev --limit 10
```

## API: Structured Extraction
Firecrawl v1 excels at extracting structured data using Pydantic schemas, significantly reducing LLM token usage.

```python
from firecrawl import Firecrawl
from pydantic import BaseModel
from typing import List

app = Firecrawl(api_key="fc-YOUR_API_KEY")

class PricingPlan(BaseModel):
    name: str
    price: float
    features: List[str]

# Extract structured data from a pricing page
# This uses the /extract endpoint which is optimized for JSON output
data = app.scrape("https://firecrawl.dev/pricing", {
    "formats": ["json"],
    "jsonOptions": {
        "schema": PricingPlan.model_json_schema()
    }
})

print(data["json"])
```

## API: Advanced Mapping and Searching
The `map` endpoint is used for discovery, while `search` provides real-time content.

```python
# Discover all product URLs on a site instantly
map_result = app.map("https://firecrawl.dev", search="product")
print(f"Discovered URLs: {map_result['links']}")

# Search the web and get full content for the top 3 results
search_result = app.search("Best open-source RAG frameworks", {
    "limit": 3,
    "scrapeOptions": {"formats": ["markdown"]}
})

for result in search_result["data"]:
    print(f"Source: {result['url']}\nContent: {result['markdown'][:200]}...")
```

## API: Actions and Interaction
Firecrawl allows for complex browser interactions before content extraction.

```python
# Interact with a page (click, wait, scroll) before scraping
result = app.scrape("https://example.com/login", {
    "formats": ["markdown"],
    "actions": [
        {"type": "click", "selector": "#login-btn"},
        {"type": "wait", "milliseconds": 2000},
        {"type": "scroll", "direction": "down"}
    ]
})
```

## Related tools / concepts
- [Crawl4AI](crawl4ai.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [Skyvern](../automation_orchestration/skyvern.md)
- [Docling](docling.md)
- [RAGFlow](ragflow.md)
- [Valyu](../ai_knowledge/valyu.md)
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md)

## Sources / References
- [GitHub](https://github.com/firecrawl/firecrawl)
- [Official Website](https://firecrawl.dev/)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
