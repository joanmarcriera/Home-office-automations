# SearXNG

SearXNG is a free internet metasearch engine which aggregates results from more than 70 search services, providing a privacy-preserving and agent-friendly search infrastructure in early January 2027.

## What it is
SearXNG is a free, privacy-preserving internet metasearch engine that aggregates search results from over 70 search engines and services. Operating as an anonymizing proxy, SearXNG strips tracking cookies, user tokens, and IP addresses from outgoing queries, providing clean, structured results to end users, local LLM agents (**Gemma 3**, **Qwen 3.8**), and frontier multi-agent systems (**Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro**).

## What problem it solves
It eliminates search profiling, behavioral tracking, and search bubble bias enforced by commercial engines. For autonomous AI agent workflows, SearXNG solves rate-limiting, engine-specific IP blocking, and formatting fragmentation by unifying diverse upstream search provider responses into standardized JSON payloads accessible via [FastMCP 3.1](../tools/automation_orchestration/mcp.md) servers and direct HTTP APIs.

## Where it fits in the stack
**Category**: Services / Search & Discovery. SearXNG acts as the primary web search and live-retrieval engine for private RAG pipelines and autonomous agent toolkits. It typically resides behind reverse proxies (Nginx, Traefik, or Caddy) with authentication secured by [Authentik](authentik.md) or [Authelia](authelia.md), interfacing directly with orchestration engines like [n8n](n8n.md) or custom MCP servers.

## Typical use cases
- **Privacy-First Search Infrastructure**: Secure search backend for enterprise networks and self-hosted environments without tracking or analytics leakage.
- **Agentic Web Retrieval**: Providing structured search capabilities to FastMCP 3.1 tools for [Claude 5.1](../tools/providers/anthropic.md), [GPT-5.5](../tools/ai_knowledge/openai.md), and [DeepSeek-V4](../tools/providers/deepseek.md).
- **Domain-Specific Aggregation**: Filtering and weighting results across specialized sources (e.g., GitHub, StackOverflow, ArXiv, Wikipedia) for developer research loops.
- **RAG Context Expansion**: Fetching real-time web citations and context snippets to augment prompt context windows for local models like Gemma 3 and Llama 4.
- **Unified Internal & External Search**: Integrating local documentation JSON endpoints alongside public search providers.

## Strengths
- **Anonymization & Zero Tracking**: Strips all user identifiers and IP headers before querying upstream search providers.
- **Aggregated Broad Coverage**: Fetches and rank-merges results across 70+ general, academic, code, and news search engines.
- **Native JSON Output**: Built-in `format=json` response support designed for seamless programmatic ingestion.
- **Customizable Weighting**: Granular settings to adjust engine priorities, response timeouts, and category definitions.
- **Open Source Security**: AGPL-3.0 licensed codebase with active community security auditing.

## Limitations
- **Upstream Scraping Blockades**: Search engines frequently update CAPTCHA systems or block cloud provider IP ranges, requiring active SearXNG maintenance.
- **Aggregated Latency**: Querying multiple engines in parallel inherently introduces slight latency compared to single-source search APIs.
- **No Native Personalization**: High-volume localized query results (e.g., "nearby cafes") require explicit spatial coordinates in the search query.

## When to use it
- When providing privacy-focused web search capabilities for self-hosted AI agent frameworks.
- When building tool-use pipelines where agents require structured search without relying on paid proprietary search APIs.
- When combining internal documentation search endpoints with external web retrieval in a single query interface.

## When not to use it
- When requiring consumer-focused personalized search histories or real-time location tracking.
- When operating in environments unable to manage proxy IPs or maintain scraper engine definitions.

## Getting started

### Installation (Docker Compose)
```yaml
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng
    environment:
      - SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml
      - SEARXNG_SECRET=a_very_secure_random_secret_key_2027
    restart: always
```

### Custom Engine Configuration (`settings.yml`)
Configure domain-specific weights and integrate custom JSON endpoints:

```yaml
# /etc/searxng/settings.yml
search:
  safe_search: 0
  autocomplete: "duckduckgo"
  formats:
    - html
    - json

engines:
  - name: google
    weight: 1.0
  - name: wikipedia
    weight: 2.0  # Prioritize encyclopedia references
  - name: github
    weight: 3.0  # Heavily bias developer code searches

  - name: internal-docs
    engine: json_engine
    search_url: http://docs-server:8000/api/v1/search?q={query}
    results_query: results
    title_query: title
    url_query: url
    content_query: snippet
    categories: general
    weight: 5.0  # Highest priority for internal docs
```

## CLI examples

```bash
# General web search in JSON format
curl -s "http://localhost:8080/search?q=FastMCP+3.1+python&format=json" | jq '.results[0]'

# Category-filtered search (IT / Development)
curl -s "http://localhost:8080/search?q=DeepSeek-V4+architecture&categories=it&format=json"

# Direct query to specific search engine
curl -s "http://localhost:8080/search?q=SearXNG&engines=wikipedia&format=json"
```

## API examples

### Python FastMCP 3.1 Integration
Exposing SearXNG as a standard tool for autonomous AI agents using FastMCP 3.1:

```python
import requests
from fastmcp import FastMCP

mcp = FastMCP("SearXNG-Search-Server", version="3.1.0")

@mcp.tool()
def search_web(query: str, category: str = "general", max_results: int = 5) -> str:
    """Performs a privacy-preserving metasearch query using SearXNG.

    Args:
        query: The search query string.
        category: Search category ('general', 'it', 'science', 'news').
        max_results: Maximum number of search results to return.
    """
    url = "http://localhost:8080/search"
    params = {
        "q": query,
        "categories": category,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])[:max_results]
        formatted = []
        for item in results:
            title = item.get("title", "No Title")
            link = item.get("url", "")
            content = item.get("content", "")
            engine = item.get("engine", "unknown")
            formatted.append(f"[{title}]({link}) (via {engine})\n{content}")

        return "\n\n".join(formatted) if formatted else "No results found."
    except Exception as e:
        return f"SearXNG query error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

### Response Validation using Pydantic v2
Validating aggregated SearXNG search responses using Pydantic v2 schemas:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class SearchResultItem(BaseModel):
    title: str = Field(..., description="The title of the search result")
    url: HttpUrl = Field(..., description="The source URL of the search result")
    content: Optional[str] = Field(None, description="Text snippet or summary")
    engine: str = Field(..., description="Upstream engine providing the result")
    score: Optional[float] = Field(None, description="Aggregated relevance score")

class SearXNGQueryResponse(BaseModel):
    query: str = Field(..., description="The original search query executed")
    results: List[SearchResultItem] = Field(default_factory=list, description="Validated search results")
    unresponsive_engines: List[str] = Field(default_factory=list, description="Timed out or failed engines")

def parse_searxng_response(raw_json: str) -> Optional[SearXNGQueryResponse]:
    try:
        data = json.loads(raw_json)
        return SearXNGQueryResponse.model_validate(data)
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"Validation failure: {e}")
        return None
```

## Related tools / concepts
- [Authentik](authentik.md) — Identity provider securing SearXNG endpoints.
- [n8n](n8n.md) — Workflow automation tool integrating SearXNG API nodes.
- [Crawl4AI](../tools/process_understanding/crawl4ai.md) — High-performance scraping tool for deep-crawling SearXNG search result URLs.
- [Perplexity](../tools/providers/perplexity.md) — Commercial AI search alternative.
- [FastMCP](../tools/automation_orchestration/mcp.md) — Model Context Protocol framework for agent tool binding.

## Sources / references
- [SearXNG Official Website](https://searxng.org/)
- [SearXNG GitHub Repository](https://github.com/searxng/searxng)
- [SearXNG Documentation](https://docs.searxng.org/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
