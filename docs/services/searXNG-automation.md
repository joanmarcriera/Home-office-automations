# SearXNG Automation

SearXNG Automation provides the patterns, API integrations, and programmatic workflows for using a self-hosted [SearXNG](searXNG.md) instance as a primary live knowledge retrieval layer for AI agents and automated pipelines in early January 2027.

## What it is
SearXNG Automation encompasses programmatic interactions with SearXNG's structured JSON API endpoints. It enables local LLMs (**Gemma 3**, **Qwen 3.8**) and frontier multi-agent systems (**Claude 5.1**, **GPT-5.5 / 5.6**, **DeepSeek-V4**) to browse the live web, bypass tracking filters, and aggregate search results from over 70 search engines into clean, machine-readable JSON data streams exposed via [FastMCP 3.1](../tools/automation_orchestration/mcp.md).

Through automated metasearch wrappers, AI agents perform real-time internet research, query code repositories, parse academic papers, and verify web citations with zero per-request API costs.

```
+-----------------------------------------------------------------------------------+
|                            SearXNG Automation Flow                                |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-------------------+       +-----------------------+      +------------------+  |
|  | Multi-Agent RAG   |       | FastMCP 3.1 Client    |      | n8n Workflow     |  |
|  | Execution Loop    |       | (Claude/GPT/DeepSeek) |      | (Automation Node)|  |
|  +---------+---------+       +-----------+-----------+      +--------+---------+  |
|            |                             |                           |            |
|            +------------------+          |          +----------------+            |
|                               |          v          |                             |
|                               v                     v                             |
|                  +-------------------------------------+                          |
|                  | SearXNG Automation Server (FastMCP)  |                          |
|                  | - Query Construction & Formatting   |                          |
|                  | - Category Filtering (IT/Science)   |                          |
|                  | - Pydantic v2 Schema Validator      |                          |
|                  +-------------------+-----------------+                          |
|                                      |                                            |
|          +---------------------------+---------------------------+                |
|          |                           |                           |                |
|          v                           v                           v                |
|  +-------------------+     +-------------------+     +-------------------+        |
|  | Local SearXNG     |     | Crawl4AI Deep     |     | Paperless-ngx     |        |
|  | JSON Endpoint     |     | Content Scraper   |     | Search Archiver   |        |
|  +-------------------+     +-------------------+     +-------------------+        |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It eliminates dependency on high-cost, rate-limited commercial search APIs (e.g., Tavily, Perplexity, or Bing Search API). SearXNG Automation delivers a private "Search-as-a-Service" layer on internal networks, enabling unlimited queries without per-request charges while keeping sensitive search intents from being logged or harvested for model training.

Furthermore, commercial web search APIs restrict category filtering or charge extra for deep academic and code searches. SearXNG Automation provides fine-grained control over upstream search categories (e.g., querying GitHub, ArXiv, and StackOverflow simultaneously), returning unified JSON structures ready for LLM context injection.

## Where it fits in the stack
**Category**: Services / Search Automation & Retrieval. It acts as the real-time web retrieval interface for private RAG pipelines, autonomous agent toolkits, and [n8n](n8n.md) automation workflows, sitting directly between agent execution loops and external web sources.

```
+-----------------------------------------------------------------------------------+
|                             Stack Integration Context                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|   [ Agent Layer ] -----------> ( Claude 5.1 / GPT-5.6 / DeepSeek-V4 Subagents )     |
|                                              |                                    |
|                                              v                                    |
|   [ Tool Binding Layer ] ----> ( FastMCP 3.1 SearXNG Automation Server )          |
|                                              |                                    |
|                                              v                                    |
|   [ Metasearch Engine ] -----> ( SearXNG Docker Container : JSON Endpoint )       |
|                                              |                                    |
|                                              v                                    |
|   [ Content Processing ] ----> ( Crawl4AI / Docling Web Extractor )              |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Feature Comparison Matrix

| Capability / Dimension | SearXNG Automation (FastMCP 3.1) | Commercial Tavily / Perplexity API | Raw Playwright Browser Scraping |
| :--- | :--- | :--- | :--- |
| **API Cost Structure** | $0 / Free (Self-hosted) | $0.005–$0.02 per query | Free code, high server memory usage |
| **Data Privacy** | 100% On-Premise; zero query logging | Vendor logs search telemetry | High anti-bot footprint |
| **Category Selection** | Granular (General, IT, Science, News, Files)| Fixed general web search | Domain-specific scripting required |
| **Response Latency** | 200ms–600ms (Parallel engine fetch) | 100ms–300ms | 2s–6s (Full rendering) |
| **FastMCP 3.1 Integration**| Native Python async FastMCP tool | Standard REST / SDK | Custom wrapper required |
| **Schema Validation** | Strict Pydantic v2 output schemas | Proprietary SDK objects | Custom DOM parser scripts |

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

## Production Deployment & Orchestration

### Systemd Service & Timer Configuration

Automating periodic health audits and upstream engine failover ensures production agent pipelines are not stalled by unresponsive external search providers.

> **Status: design sketch.** The units below start a `scripts.rotate_engines` module that does not ship in this repository; there is no engine-rotation script under `scripts/`. Treat the service and timer as a template for your own rotator.

#### Service Unit: `/etc/systemd/system/searxng-rotator.service`
```ini
[Unit]
Description=SearXNG Upstream Engine Health Evaluator and Proxy Rotator
After=network.target docker.service
Documentation=https://docs.searxng.org/

[Service]
Type=oneshot
User=searxng
Group=searxng
WorkingDirectory=/opt/searxng-automation
Environment="SEARXNG_URL=http://127.0.0.1:8080"
Environment="HEALTH_THRESHOLD_RELIABILITY=75"
ExecStart=/opt/searxng-automation/bin/python3 -m scripts.rotate_engines
StandardOutput=journal
StandardError=journal
SyslogIdentifier=searxng-rotator
```

#### Timer Unit: `/etc/systemd/system/searxng-rotator.timer`
```ini
[Unit]
Description=Run SearXNG Upstream Engine Health Evaluator every 15 minutes
Requires=searxng-rotator.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Persistent=true

[Install]
WantedBy=timers.target
```

### Multi-Container Docker Compose Stack (`docker-compose.searxng.yml`)

The following Compose specification deploys SearXNG alongside a Redis cache, Caddy TLS reverse proxy, and a FastMCP 3.1 gateway:

```yaml
version: "3.8"

services:
  searxng-redis:
    image: redis:7.2-alpine
    container_name: searxng_redis
    command: redis-server --save "" --appendonly no --maxmemory 256mb --maxmemory-policy allkeys-lru
    restart: unless-stopped
    networks:
      - searxng-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  searxng:
    image: searxng/searxng:latest
    container_name: searxng_instance
    restart: unless-stopped
    depends_on:
      searxng-redis:
        condition: service_healthy
    volumes:
      - ./searxng:/etc/searxng:ro
    environment:
      - SEARXNG_BASE_URL=https://search.internal.net/
      - SEARXNG_REDIS_URL=redis://searxng-redis:6379/0
      - UWSGI_WORKERS=4
      - UWSGI_THREADS=4
    networks:
      - searxng-net

  fastmcp-searxng-gateway:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    container_name: fastmcp_searxng_gateway
    restart: unless-stopped
    depends_on:
      - searxng
    environment:
      - SEARXNG_INTERNAL_URL=http://searxng:8080
      - MCP_PORT=8010
    ports:
      - "8010:8010"
    networks:
      - searxng-net

  caddy:
    image: caddy:2.8-alpine
    container_name: searxng_caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    depends_on:
      - searxng
    networks:
      - searxng-net

volumes:
  caddy_data:

networks:
  searxng-net:
    driver: bridge
```

## API examples

### FastMCP 3.1 Search Tool (Python)
Exposing SearXNG to autonomous AI agents via FastMCP 3.1 with strict Pydantic v2 schemas:

```python
import httpx
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP

mcp = FastMCP("SearXNG-Automation-Server", version="3.1.0")

SEARXNG_URL = "http://localhost:8080/search"

class SearchItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., description="Title of the returned webpage")
    url: str = Field(..., description="Direct hyperlink to the source")
    content: str = Field(..., description="Extracted content snippet or summary")
    engine: str = Field(..., description="Upstream search engine identifier")
    score: Optional[float] = Field(None, description="SearXNG score metric")

class SearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(..., description="Processed query string")
    category: str = Field(..., description="SearXNG category searched")
    count: int = Field(..., description="Total items returned")
    results: List[SearchItem] = Field(default_factory=list)

@mcp.tool()
async def search_web(query: str, category: str = "general", count: int = 5) -> Dict[str, Any]:
    """Performs an aggregated web search using self-hosted SearXNG with strict schema validation.

    Args:
        query: Search query string.
        category: Search category ('general', 'it', 'science', 'news', 'files').
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

            raw_results = data.get("results", [])[:count]
            validated_items: List[SearchItem] = []
            for item in raw_results:
                validated_items.append(
                    SearchItem(
                        title=item.get("title", "Untitled"),
                        url=item.get("url", ""),
                        content=item.get("content", ""),
                        engine=item.get("engine", "unknown"),
                        score=item.get("score")
                    )
                )

            response = SearchResponse(
                query=query,
                category=category,
                count=len(validated_items),
                results=validated_items
            )
            return response.model_dump()
        except Exception as e:
            return {"error": f"Search execution failed: {str(e)}", "query": query, "results": []}

if __name__ == "__main__":
    mcp.run()
```

### Async Python Client with Pydantic v2 Schema Validation
Fetching and validating SearXNG responses asynchronously:

```python
import asyncio
import httpx
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError, ConfigDict

class SearchResultModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., description="Title of the search result")
    url: HttpUrl = Field(..., description="Validated destination URL")
    content: Optional[str] = Field("", description="Text snippet of the search result")
    engine: str = Field(..., description="Upstream search engine provider")
    score: Optional[float] = Field(0.0, description="SearXNG internal relevance score")

class SearXNGAPIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
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

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Steps | Resolution Procedure |
|:---|:---|:---|:---|
| **JSON Response Disabled Error (403/HTML returned)** | `formats: [json]` missing or commented out in `settings.yml`. | Inspect raw HTTP headers and body: `curl -v "http://localhost:8080/search?q=test&format=json"`. | Add `- json` under the `search.formats` array in `settings.yml` and restart container. |
| **Upstream 429 Rate Limit (Too Many Requests)** | Source engines (e.g., Google/Bing) detect frequent queries originating from single server IP. | Query `http://localhost:8080/stats` to identify engines returning 0% reliability or HTTP 429. | Route SearXNG outbound traffic through rotating residential SOCKS5 proxies or enable engine rotation in `settings.yml`. |
| **Engine Timeout During Multi-Engine Aggregation** | Remote upstream engine taking longer than default timeout (3.0s). | Check SearXNG container logs for `searx.engines: ERROR: <engine> timeout`. | Increase `engine_timeout: 6.0` in `settings.yml` and set client `httpx` timeout to 10.0s. |
| **Redis Cache Socket Connection Refused** | SearXNG cannot reach internal Redis instance for caching rate limits and session states. | Check Redis container status: `docker ps --filter name=searxng_redis` and `nc -zv 127.0.0.1 6379`. | Verify `SEARXNG_REDIS_URL` matches Docker service name (`redis://searxng-redis:6379/0`) and network configuration. |
| **FastMCP Extra Parameter Forbidden Error** | Tool client passing unstructured metadata forbidden by strict Pydantic v2 `extra="forbid"`. | Inspect MCP server stdout/stderr logs for Pydantic `ValidationError`. | Align client tool parameters strictly to `query`, `category`, and `count` arguments. |

## Operational Best Practices

### Egress IP Management & Proxy Pools
High-frequency agent queries can trigger upstream search engine blockades if routed from a single cloud server IP.
1. **Rotating Egress Proxies**: Configure SearXNG to route outbound requests through rotating residential proxies or wireguard VPN tunnels.
2. **Category Isolation**: Assign developer research tasks specifically to the `it` category to avoid sending code queries to general search engines.
3. **Engine Reliability Audits**: Periodically query `http://searxng.local:8080/stats` to detect and temporarily disable failing upstream search providers.

## Related tools / concepts
- [SearXNG](searXNG.md) — The underlying self-hosted search engine container.
- [FastMCP](../tools/automation_orchestration/mcp.md) — Protocol for exposing SearXNG tools to AI agents.
- [Crawl4AI](../tools/process_understanding/crawl4ai.md) — For deep-crawling URLs extracted from SearXNG search results.
- [n8n](n8n.md) — Workflow engine for multi-step search pipelines.
- [Authentik](authentik.md) — Securing SearXNG endpoints in production.
- [Paperless-ngx](paperless-ngx.md) — For archiving extracted web search summaries.
- [Gitea](gitea.md) — For managing custom SearXNG plugin and automation repositories.
- [Ollama](ollama.md) — For local LLM processing of search results.

## Sources / references
- [SearXNG Developer Documentation](https://docs.searxng.org/dev/search_api.html)
- [FastMCP Python Specification](https://github.com/jlowin/fastmcp)
- [Model Context Protocol 3.1 Spec](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
