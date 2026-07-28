# Firecrawl

## What it is
Firecrawl is an API-first web scraping and crawling engine that converts entire websites into clean, structured, and LLM-ready formats (Markdown or JSON). In late 2026, it serves as a core ingestion gateway for frontier systems including **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0**, handling modern web delivery methods such as shadow DOM elements, dynamic JavaScript execution, and anti-bot mitigation.

## What problem it solves
It eliminates the heavy infrastructure tax of self-managed scraping pipelines. Instead of maintaining complex Playwright/Puppeteer browser pools, proxy rotation pools, and custom HTML/boilerplate cleansing heuristics, developers can invoke simple API endpoints to retrieve high-fidelity Markdown optimized directly for RAG (Retrieval-Augmented Generation) and agentic workflows.

## Where it fits in the stack
**Ingest / Process & Understanding**. It acts as the data-acquisition gateway, allowing agents (such as Claude 5.1 and GPT-5.5) to interact with the real-time web by providing clean, structured text representations, natively integrated via **Model Context Protocol (MCP 3.1)**.

## Typical use cases
- **Real-Time Agent Search**: Allowing an MCP-compatible agent to instantly crawl and extract the latest documentation, technical blogs, or market developments.
- **RAG Pipeline Ingestion**: Orchestrating scheduled batch crawls across target domains to continuously update a vector database.
- **Structured Schema Extraction**: Converting messy product pages, job listings, or financial reports into validated, structured JSON formats using Pydantic schemas.
- **Site Mapping and Discovery**: Performing shallow mapping of sub-URLs across a domain without triggering a slow, comprehensive crawl.

## Strengths
- **Clean Markdown Native**: Output is optimized specifically to minimize token consumption in large LLM context windows.
- **MCP 3.1 Compliance**: Native Model Context Protocol servers enable zero-config tool registration in modern agent platforms.
- **Anti-Bot Defense**: Built-in, high-efficiency proxy rotation and JS rendering capable of bypassing advanced Cloudflare and Akamai protective wrappers.
- **Scalable Asynchronous Crawling**: Endpoints support high-concurrency background crawls with webhook-based status callbacks.

## Limitations
- **Processing Latency**: Deep multi-page crawls can introduce latency bounds inappropriate for real-time agent responses.
- **Operational Costs**: Managed cloud tiers can become cost-prohibitive for continuous high-frequency, multi-gigabyte ingestion.
- **Self-Hosting Dependencies**: Running the open-source version locally requires a production-grade Docker, Redis, and PostgreSQL infrastructure.

## When to use it
- When your AI agents require live web interaction but are constrained by strict token limit policies.
- When you need to retrieve complex web content as highly-accurate, clean Markdown while preserving table structures and link formatting.
- When utilizing MCP-compatible tools like [Claude Code](../development_ops/claude-code.md) or [Zed](../development_ops/zed.md).

## When not to use it
- For retrieving static data from websites that offer clean, public REST APIs (e.g., GitHub, Slack).
- For lightweight, single-page, local scraping operations where simple libraries like `BeautifulSoup` or native `curl` can fetch the target content immediately.

## Getting started

### Installation
Install the official Python SDK using `pip`:

```bash
pip install firecrawl-py
```

### Basic Scrape (Python)
Authenticate and scrape a website to clean Markdown using the standard async-ready SDK:

```python
from firecrawl import FirecrawlApp

# Initialize the application with your API credentials
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a target URL to clean Markdown
scrape_result = app.scrape_url("https://example.com", params={"formats": ["markdown"]})
print(scrape_result.get("markdown", ""))
```

## CLI examples
The `firecrawl` CLI (available via NPM) enables rapid terminal-based scraping and testing.

```bash
# Install the command line tool globally
npm install -g firecrawl-cli

# Scrape a website and output the raw Markdown to standard output
firecrawl scrape https://docs.firecrawl.dev

# Map a website to discover all discoverable sub-URLs
firecrawl map https://firecrawl.dev

# Query the web and return top 3 search results in clean Markdown format
firecrawl search "Firecrawl vs Crawl4AI" --limit 3 --format markdown
```

## API examples

### Structured Data Extraction with Pydantic v2
Using Firecrawl's JSON extraction capabilities powered by LLMs (such as GPT-5.5 or Claude 5.1) to parse messy pricing structures into validated Pydantic models:

```python
from typing import List
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field

# Define target schema using modern Pydantic v2
class PricingTier(BaseModel):
    tier_name: str = Field(description="The name of the pricing plan")
    price_usd: float = Field(description="Monthly cost in USD")
    features: List[str] = Field(description="List of features included in this tier")

class PricingSchema(BaseModel):
    product_name: str
    tiers: List[PricingTier]

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Perform the structured extraction
extraction_data = app.scrape_url(
    "https://firecrawl.dev/pricing",
    params={
        "formats": ["json"],
        "jsonOptions": {
            "schema": PricingSchema.model_json_schema()
        }
    }
)

# Output the parsed JSON results
print(extraction_data.get("json"))
```

## Related tools / concepts
- [Crawl4AI](crawl4ai.md) - High-performance local-first open-source web scraper.
- [Docling](docling.md) - Sophisticated document and PDF layout parser.
- [Docling MCP](docling-mcp.md) - Document processing service leveraging Model Context Protocol.
- [Model Context Protocol](../automation_orchestration/mcp.md) - Standard protocol for agent-to-tool integration.
- [Claude Code](../development_ops/claude-code.md) - Command-line agent native tool.
- [RAGFlow](ragflow.md) - High-efficiency visual RAG pipeline builder.
- [Browser Use](../automation_orchestration/browser-use.md) - Vision-aware agentic web browser driver.

## Sources / references
- [Firecrawl Documentation Portal](https://docs.firecrawl.dev/)
- [Firecrawl Open-Source GitHub Repository](https://github.com/mendableai/firecrawl)
- [Official MCP Server for Firecrawl](https://github.com/firecrawl/mcp-server-firecrawl)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
