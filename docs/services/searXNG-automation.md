# SearXNG Automation

SearXNG Automation provides the patterns, API integrations, and programmatic workflows for using a self-hosted [SearXNG](searXNG.md) instance as a primary live knowledge retrieval layer for AI agents and automated pipelines in early January 2027.

## What it is
SearXNG Automation encompasses programmatic interactions with SearXNG's structured JSON API endpoints. It enables local LLMs (**Gemma 3**, **Qwen 3.8**) and frontier multi-agent systems (**Claude 5.1**, **GPT-5.5 / 5.6**, **DeepSeek-V4**) to browse the live web, bypass tracking filters, and aggregate search results from over 70 search engines into clean, machine-readable JSON data streams exposed via [FastMCP 3.1](../tools/automation_orchestration/mcp.md).

## What problem it solves
It eliminates dependency on high-cost, rate-limited commercial search APIs (e.g., Tavily, Perplexity, or Bing Search API). SearXNG Automation delivers a private "Search-as-a-Service" layer on internal networks, enabling unlimited queries without per-request charges while keeping sensitive search intents from being logged or harvested for model training.

## Where it fits in the stack
**Category**: Services / Search Automation & Retrieval. It acts as the real-time web retrieval interface for private RAG pipelines, autonomous agent toolkits, and [n8n](n8n.md) automation workflows, sitting directly between agent execution loops and external web sources.

## Typical use cases
- **Multi-Agent Deep Research**: Powering autonomous research loops where agents query, filter, and summarize real-time web findings.
- **Automated Verification & Fact-Checking**: Workflows that cross-reference claims across scientific, code, and academic engines (ArXiv, GitHub, Wikipedia).
- **FastMCP 3.1 Search Server**: Exposing a standardized, tool-bound search capability to Claude 5.1, GPT-5.5, and DeepSeek-V4.
- **Continuous Intelligence & News Tracking**: Automated n8n routines monitoring technical announcements or software vulnerabilities without query leakage.
- **Dynamic Context Expansion**: Injecting live web content into local RAG pipelines to overcome static model knowledge cutoffs.

## Strengths
- **Complete Anonymity & Zero Cost**: Strips user identifiers and IP headers without per-query billing or cloud API limits.
- **Aggregated Broad Coverage**: Simultaneous execution across general, academic, file, and code search engines.
- **FastMCP 3.1 Native Binding**: Direct integration into MCP tool registries with minimal overhead (<50ms processing wrapper).
- **Fine-Grained Engine Tuning**: Granular weighting, custom timeout thresholds, and engine selection in `settings.yml`.
- **Zero Query Logging**: Prevents search query telemetry from training third-party foundation models.

## Limitations
- **Upstream IP Rate Limits**: High-frequency automated queries from a single static IP may trigger upstream CAPTCHAs or temporary blocks.
- **Scraper Breakage**: Upstream HTML changes on source engines require periodic SearXNG updates.
- **Aggregation Latency**: Overall query response time depends on the slowest active search provider.

## When to use it
- When building private, cost-effective AI research pipelines requiring real-time web search.
- When agents require aggregated results across niche engines (ArXiv, GitHub, StackOverflow) alongside mainstream providers.
- When establishing local search tools for FastMCP 3.1 compliant agent frameworks.

## When not to use it
- For mass web scraping operations better suited for dedicated browser clusters like Playwright or [Crawl4AI](../tools/process_understanding/crawl4ai.md).
- In lightweight environments unable to host the Python/Redis backend of SearXNG.

## Getting started

### SearXNG Configuration (`settings.yml`)
Ensure JSON responses and appropriate engine timeouts are enabled:

```yaml
search:
  safe_search: 0
  autocomplete: "duckduckgo"
  formats:
    - html
    - json

# Extended timeout for parallel multi-engine aggregation
engine_timeout: 5.0
```

### Basic Curl Command
```bash
curl -s "http://searxng.local:8080/search?q=FastMCP+3.1+python&format=json" | jq '.results[0]'
```

## CLI examples

### Processing Search Results with JQ
Extract top 5 result titles, URLs, and source engines:
```bash
curl -s "http://searxng.local:8080/search?q=DeepSeek-V4+architecture&format=json" | \
jq -r '.results[:5][] | "[\(.engine)] \(.title) -> \(.url)"'
```

### Engine Health & Latency Audit
Query engine stats to identify slow or failing search providers:
```bash
curl -s "http://searxng.local:8080/stats" | jq '.engines[] | select(.reliability < 80) | {engine: .name, reliability: .reliability}'
```

### Category-Specific File Search
```bash
curl -s "http://searxng.local:8080/search?q=FastMCP+specification&categories=files&format=json"
```

## API examples

### FastMCP 3.1 Search Tool (Python)
Exposing SearXNG to autonomous AI agents via FastMCP 3.1:

```python
import httpx
from fastmcp import FastMCP

mcp = FastMCP("SearXNG-Automation-Server", version="3.1.0")

SEARXNG_URL = "http://localhost:8080/search"

@mcp.tool()
async def search_web(query: str, category: str = "general", count: int = 5) -> str:
    """Performs an aggregated web search using self-hosted SearXNG.

    Args:
        query: Search query string.
        category: Search category ('general', 'it', 'science', 'news').
        count: Number of results to return (max 10).
    """
    params = {
        "q": query,
        "categories": category,
        "format": "json"
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(SEARXNG_URL, params=params, timeout=8.0)
            res.raise_for_status()
            data = res.json()

            results = data.get("results", [])[:count]
            if not results:
                return "No search results returned."

            snippets = []
            for item in results:
                title = item.get("title", "")
                url = item.get("url", "")
                content = item.get("content", "")
                engine = item.get("engine", "")
                snippets.append(f"Title: {title}\nURL: {url}\nEngine: {engine}\nSnippet: {content}\n")

            return "\n---\n".join(snippets)
        except Exception as e:
            return f"Search execution error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

### Async Python Client with Pydantic v2 Schema Validation
Fetching and validating SearXNG responses asynchronously:

```python
import asyncio
import httpx
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class SearchResultModel(BaseModel):
    title: str = Field(..., description="Title of the search result")
    url: HttpUrl = Field(..., description="Validated destination URL")
    content: Optional[str] = Field("", description="Text snippet of the search result")
    engine: str = Field(..., description="Upstream search engine provider")
    score: Optional[float] = Field(0.0, description="SearXNG internal relevance score")

class SearXNGAPIResponse(BaseModel):
    query: str = Field(..., description="Original search query")
    results: List[SearchResultModel] = Field(default_factory=list)
    unresponsive_engines: List[str] = Field(default_factory=list)

async def search_searxng(query: str, base_url: str = "http://localhost:8080") -> Optional[SearXNGAPIResponse]:
    params = {
        "q": query,
        "format": "json"
    }
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f"{base_url}/search", params=params, timeout=10.0)
            res.raise_for_status()
            return SearXNGAPIResponse.model_validate(res.json())
        except (httpx.HTTPError, ValidationError) as e:
            print(f"SearXNG query failed: {e}")
            return None

async def main():
    data = await search_searxng("Claude 5.1 FastMCP integration")
    if data:
        print(f"Results for '{data.query}': {len(data.results)} items found.")
        for item in data.results[:3]:
            print(f"- {item.title} ({item.url})")

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [SearXNG](searXNG.md) — The underlying self-hosted search engine container.
- [FastMCP](../tools/automation_orchestration/mcp.md) — Protocol for exposing SearXNG tools to AI agents.
- [Crawl4AI](../tools/process_understanding/crawl4ai.md) — For deep-crawling URLs extracted from SearXNG search results.
- [n8n](n8n.md) — Workflow engine for multi-step search pipelines.
- [Authentik](authentik.md) — Securing SearXNG endpoints in production.

## Sources / references
- [SearXNG Developer Documentation](https://docs.searxng.org/dev/search_api.html)
- [FastMCP Python Specification](https://github.com/jlowin/fastmcp)
- [Model Context Protocol 3.1 Spec](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
