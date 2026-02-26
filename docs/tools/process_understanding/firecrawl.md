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

## Related tools / concepts
- [Crawl4AI](crawl4ai.md)
- [Browser Use](../automation_orchestration/browser-use.md)

## Sources / References
- [GitHub](https://github.com/firecrawl/firecrawl)
- [Official Website](https://firecrawl.dev/)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: high
