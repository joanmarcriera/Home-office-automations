# SearXNG Automation

SearXNG Automation provides the patterns and programmatic interfaces for using a self-hosted [SearXNG](searXNG.md) instance as a primary knowledge retrieval layer for AI agents and automated workflows. In the late October / November 2026 landscape, it serves as a privacy-preserving, high-performance alternative to commercial search APIs for "Deep Research" agents powered by **Gemma 3**, **Llama 4**, and **Claude 5.1**.

## What it is
SearXNG Automation is the practice of interacting with SearXNG's JSON API to perform aggregated web searches. It enables local LLMs and agents to browse the live web, bypass corporate tracking, and consolidate results from over 70 engines into a single, structured data stream. By late October / November 2026, it is standard to expose SearXNG via the **Model Context Protocol (MCP 3.1)** using **FastMCP 3.1** for low-latency tool execution.

## What problem it solves
It eliminates dependency on expensive, gated commercial search APIs (like Tavily or Google Search API). SearXNG Automation provides a "Search-as-a-Service" layer within a private network, offering unlimited queries without per-request costs, while protecting search intent and history from being used for upstream model training.

## Where it fits in the stack
**Category**: Services / Search Automation. It serves as the **Real-Time Retrieval Layer** for RAG systems and the external knowledge interface for autonomous agents. It sits between the agent orchestration layer and the public internet.

## Typical use cases
- **Gemma 3 Deep Research**: Powering local search agents that use multimodal reasoning to synthesize information from web results.
- **Automated Fact-Checking**: Workflows that verify claims by querying specialized authoritative engines (Arxiv, Wikipedia) via SearXNG.
- **Privacy-First Intelligence**: Monitoring industry trends without leaking research interests to commercial search providers.
- **Agentic Resource Discovery**: Allowing an agent to find and download relevant datasets or documentation for a specific task.
- **MCP 3.1 Search Integration**: Providing a standardized search tool that can be called by any MCP-compliant agent.

## Strengths
- **Privacy-Native**: Proxies all requests and strips PII, ensuring "Search Anonymity" for the homelab.
- **Engine Aggregation**: Simultaneous access to general, scientific, social media, and file-based engines.
- **Cost Independence**: No API keys or credit-based billing required.
- **Local Control**: Fine-grained control over which engines are used and how results are ranked via `settings.yml`.
- **FastMCP Optimization**: Sub-100ms overhead for tool invocation in late 2026.

## Limitations
- **Rate Limiting**: High-volume automation requires a proxy pool to avoid IP bans from major search engines like Google or Bing.
- **Maintenance**: Upstream engine changes frequently require SearXNG core updates to maintain scraper compatibility.
- **Latency**: Aggregate search speed is bound by the slowest active engine; timeouts must be managed.

## When to use it
- When building private, agentic research systems that require live web access.
- When you need to aggregate results from niche or specialized search engines alongside mainstream ones.
- When you want to minimize the operational costs of running a large-scale research agent.

## When not to use it
- For ultra-high volume "scraping" tasks that are better handled by dedicated headless browser clusters.
- In environments where hosting a complex Python/Redis stack is not feasible due to resource constraints.
- For simple site-specific searches where a direct API (like GitHub API) is more reliable.

## Getting started

### Configuration for Automation
Enable the JSON output format in `settings.yml` to allow machine-readable interaction.

```yaml
search:
  formats:
    - html
    - json
  # Late 2026: Recommended to set a longer timeout for aggregate engines
  engine_timeout: 4.5
```

### Basic API Interaction (curl)
```bash
curl "http://searxng.local:8080/search?q=Gemma+3+capabilities&format=json"
```

## CLI examples

### Filter Results with jq
Extract the top 5 titles and source engines:
```bash
curl -s "http://searxng.local:8080/search?q=homelab+trends+2026&format=json" | \
jq -r '.results[:5][] | "[\(.engine)] \(.title)"'
```

### Health Check and Metrics
Monitor the latency and status of upstream engines.
```bash
curl -s "http://searxng.local:8080/stats" | jq '.engines | map(select(.reliability < 50))'
```

### Multi-Engine Category Search
Search for files related to a query:
```bash
curl -s "http://searxng.local:8080/search?q=architecture+diagram&categories=files&format=json"
```

## API examples

### FastMCP 3.1 Search Tool (TypeScript)
The modern way to expose SearXNG to late October / November 2026 agents.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("searxng-search");

mcp.addTool({
  name: "web_search",
  description: "Search the web for real-time information",
  parameters: {
    query: { type: "string", description: "The search query" },
    category: { type: "string", description: "Optional: general, science, files, etc." }
  },
  execute: async ({ query, category = "general" }) => {
    const url = `http://searxng:8080/search?q=${encodeURIComponent(query)}&categories=${category}&format=json`;
    const res = await fetch(url);
    const data = await res.json();
    return data.results.slice(0, 5).map(r => ({ title: r.title, url: r.url, snippet: r.content }));
  }
});

mcp.serve();
```

### Python Search Client with Pydantic v2 Validation (Advanced)
Below is an asynchronous Python snippet retrieving and validating search query results directly from SearXNG's JSON API endpoint using **Pydantic v2**:

```python
import asyncio
import httpx
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class SearchResultModel(BaseModel):
    title: str = Field(..., description="The title of the search result page")
    url: HttpUrl = Field(..., description="The validated destination URL")
    content: Optional[str] = Field("", description="A short text snippet of the matched content")
    engine: str = Field(..., description="The source engine that fetched this result")
    score: Optional[float] = Field(0.0, description="SearXNG score for result relevance")

class SearXNGAPIResponse(BaseModel):
    query: str
    results: List[SearchResultModel]
    unresponsive_engines: List[str] = Field(default=[], alias="unresponsive_engines")

async def agentic_search(query: str, base_url: str = "http://localhost:8080", pageno: int = 1) -> SearXNGAPIResponse:
    headers = {"User-Agent": "AgenticResearch/2.5 (Late 2026)"}
    params = {
        "q": query,
        "format": "json",
        "pageno": pageno,
        "safesearch": 0
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/search",
            params=params,
            headers=headers
        )
        response.raise_for_status()
        raw_data = response.json()

        # Validates and parses response structure using Pydantic v2
        return SearXNGAPIResponse.model_validate(raw_data)

async def main():
    try:
        data = await agentic_search("Model Context Protocol 3.1 specifications")
        print(f"Results for '{data.query}':")
        for idx, res in enumerate(data.results[:5]):
            print(f"[{idx+1}] {res.title} (Engine: {res.engine})")
            print(f"    URL: {res.url}")
            print(f"    Snippet: {res.content[:100]}...\n")
    except Exception as e:
        print(f"Validation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [SearXNG](searXNG.md) — The core self-hosted search engine.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Primary multimodal model for reasoning over search results.
- [FastMCP 3.1](../tools/automation_orchestration/mcp.md) — Standard protocol for tool exposure.
- [n8n](n8n.md) — For building complex, multi-step search and notification pipelines.
- [LiteLLM](litellm.md) — Unified inference for search-enabled agents.
- [Tavily](../tools/providers/tavily.md) — The commercial benchmark for AI search comparison.
- [Crawl4AI](../tools/process_understanding/crawl4ai.md) — For deep scraping of URLs found via SearXNG.
- [Open-WebUI](open-webui.md) — Front-end that supports native SearXNG integration.

## Sources / references
- [SearXNG API Documentation](https://docs.searxng.org/dev/search_api.html)
- [FastMCP Tooling Guide (2026)](https://github.com/jlowin/fastmcp)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
