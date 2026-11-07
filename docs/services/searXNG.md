# SearXNG

SearXNG is a free internet metasearch engine which aggregates results from more than 70 search services, providing a privacy-preserving and agent-friendly search infrastructure in early January 2027.

## What it is
SearXNG is an open-source, privacy-preserving internet metasearch engine that aggregates search results from over 70 search engines and services. Operating as an anonymizing proxy, SearXNG strips tracking cookies, user tokens, and IP addresses from outgoing queries, providing clean, structured results to end users, local LLM agents (**Gemma 3**, **Gemma 4**, **Qwen 3.8**), and frontier multi-agent systems (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Pro**, **DeepSeek-V4**).

In the early 2027 AI architecture ecosystem, SearXNG acts as an essential gateway between deterministic internal agent loops and the noisy external web. By unifying multiple upstream providers—ranging from general search (Google, Bing, DuckDuckGo, Brave) to technical hubs (GitHub, StackOverflow, ArXiv, Wikipedia)—it normalizes unstructured web data into structured JSON objects. This empowers local RAG pipelines and autonomous agent toolkits to perform dynamic research without leaking private operational telemetry or incurring high API fees from commercial search providers.

```
+-----------------------------------------------------------------------------------+
|                            SearXNG Metasearch Architecture                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-------------------+       +-----------------------+      +------------------+  |
|  | Multi-Agent System|       | FastMCP 3.1 Server    |      | Local RAG Engine |  |
|  | (Claude/GPT/Gemma)|       | (Tool Binding Server) |      | (Qwen/Docling)   |  |
|  +---------+---------+       +-----------+-----------+      +--------+---------+  |
|            |                             |                           |            |
|            +------------------+          |          +----------------+            |
|                               |          v          |                             |
|                               v                     v                             |
|                    +-----------------------------------+                          |
|                    |  SearXNG Anonymizing Proxy Engine |                          |
|                    |  - Cookie/IP Stripping            |                          |
|                    |  - Engine Priority Weighting      |                          |
|                    |  - JSON Output Normalizer         |                          |
|                    +------------------+----------------+                          |
|                                       |                                           |
|            +--------------------------+--------------------------+                |
|            |                          |                          |                |
|            v                          v                          v                |
|  +-------------------+      +-------------------+      +-------------------+      |
|  | General Search    |      | Developer Hubs    |      | Academic / ArXiv  |      |
|  | (Google/Bing/DDG) |      | (GitHub/SO/Docs)  |      | (ArXiv/Wikipedia) |      |
|  +-------------------+      +-------------------+      +-------------------+      |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It eliminates search profiling, behavioral tracking, and search bubble bias enforced by commercial engines. For autonomous AI agent workflows, SearXNG solves rate-limiting, engine-specific IP blocking, and formatting fragmentation by unifying diverse upstream search provider responses into standardized JSON payloads accessible via [FastMCP 3.1](../tools/automation_orchestration/mcp.md) servers and direct HTTP APIs:

1. **User Profiling & Data Harvesting**: Commercial search providers log user identities, query patterns, and browsing history to target advertising. SearXNG completely anonymizes queries before dispatching them to external engines.
2. **Search API Paywalls & Rate Constraints**: Proprietary agent search APIs impose steep costs ($0.005–$0.02 per search call). SearXNG enables continuous, cost-free search across hundreds of daily agent research loops.
3. **Engine-Specific Formatting Discrepancies**: Different search APIs provide varying response schemas, markdown formats, and metadata tags. SearXNG unifies diverse results into clean, normalized JSON structures.
4. **IP Blocking on Cloud VPS Ranges**: Major search providers aggressively challenge or block IP ranges from AWS, DigitalOcean, and Hetzner. SearXNG supports built-in proxy rotation and multiple engine fallbacks.

## Mathematical Formulations: Multi-Engine Rank Merging & Latency Optimization

### 1. Reciprocal Rank Fusion (RRF) Metasearch Aggregation
SearXNG aggregates and re-scores search result hits from $E$ upstream engines using Reciprocal Rank Fusion (RRF) with engine reliability weighting $w_e$:

$$RRF\_Score(d \in D) = \sum_{e \in E} w_e \cdot \frac{1}{k + r_e(d)}$$

Where:
- $r_e(d)$ is the ordinal ranking of document $d$ within engine $e$ ($1 \le r_e(d) \le 50$).
- $k$ is a rank smoothing constant (standardized to $k = 60$).
- $w_e \in (0, 5.0]$ is the configured engine priority weight (e.g. $w_{github} = 3.0$, $w_{internal} = 5.0$).

This guarantees that a result appearing in the top 3 of multiple search engines dominates items ranked #1 on only a single engine, filtering out clickbait outliers.

### 2. Parallel Engine Response Latency Damping
Given that each upstream scraper engine $e_i$ exhibits stochastic network latency $L_i \sim \mathcal{N}(\mu_i, \sigma_i^2)$, waiting for all $E$ engines results in severe straggler delay:

$$L_{total} = \max_{i=1 \dots E} (L_i)$$

SearXNG implements a dual-stage timeout deadline $\tau_{soft}$ and $\tau_{hard}$:

$$\text{ActiveSet}(t) = \{ e_i \mid L_i \le \tau_{soft} \}$$

If $|\text{ActiveSet}(\tau_{soft})| \ge N_{min}$ (where $N_{min} = 3$), SearXNG immediately normalizes and returns results, cancelling slower pending scraper workers and capping P99 search latency to $\le 650\text{ ms}$.

## Where it fits in the stack
**Category**: Services / Search & Discovery. SearXNG acts as the primary web search and live-retrieval engine for private RAG pipelines and autonomous agent toolkits. It typically resides behind reverse proxies (Nginx, Traefik, or Caddy) with authentication secured by [Authentik](authentik.md) or Authelia, interfacing directly with orchestration engines like [n8n](n8n.md) or custom MCP servers.

```
+-----------------------------------------------------------------------------------+
|                             Stack Integration Context                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|   [ Reverse Proxy Layer ] ---> ( Traefik / Nginx with Authentik TLS )             |
|                                         |                                         |
|                                         v                                         |
|   [ Ingestion & Retrieval ] -> ( SearXNG Engine : 8080 JSON Endpoint )             |
|                                         |                                         |
|                                         v                                         |
|   [ FastMCP 3.1 Layer ] -----> ( FastMCP Search Tool Server )                     |
|                                         |                                         |
|                                         v                                         |
|   [ Agent Execution Loop ] -> ( Claude 5.6 / DeepSeek-V4 / Gemma 4 RAG )          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Feature Comparison Matrix

| Feature / Dimension | SearXNG | Commercial Search APIs (Tavily/Perplexity) | Brave Search API | Raw HTML Scraping (Playwright) |
| :--- | :--- | :--- | :--- | :--- |
| **Privacy & Anonymity** | Complete IP & Header stripping; zero telemetry | Telemetry logged for service optimization | Query telemetry logged | High exposure; exposes scraper IP to anti-bot |
| **Pricing Model** | 100% Free & Open Source (Self-hosted) | Per-query API charges ($0.005–$0.02 / query) | $0.003–$0.005 per query | Free code, high compute/proxy infrastructure cost |
| **Data Format** | Native standardized JSON payload | Proprietary agent-optimized JSON | Clean structured JSON | Unstructured HTML requires DOM parsing |
| **Multi-Engine Aggregation**| Aggregates 70+ engines in parallel | Single backend aggregator | Single independent index | Single targeted domain per scraper session |
| **Agent Protocol Support** | Native FastMCP 3.1 & REST integration | Standard REST / SDK wrappers | REST API | Requires custom tool wrapper scripts |
| **Latency Profile** | Low-to-medium (200ms–650ms parallel fetch) | Very low (100ms–300ms cached API) | Low (150ms–350ms) | High (1s–5s browser render time) |
| **Internal Doc Integration**| Turnkey JSON engine wrapper | Not supported | Not supported | Custom scraper required |

## Typical use cases
- **Privacy-First Search Infrastructure**: Secure search backend for enterprise networks and self-hosted environments without tracking or analytics leakage.
- **Agentic Web Retrieval**: Providing structured search capabilities to FastMCP 3.1 tools for [Claude 5.6](../tools/providers/anthropic.md), [GPT-5.6](../tools/ai_knowledge/openai.md), and [DeepSeek-V4](../tools/providers/deepseek.md).
- **Domain-Specific Aggregation**: Filtering and weighting results across specialized sources (e.g., GitHub, StackOverflow, ArXiv, Wikipedia) for developer research loops.
- **RAG Context Expansion**: Fetching real-time web citations and context snippets to augment prompt context windows for local models like Gemma 4 and Llama 4.
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

# Extract top 5 result URLs and titles for agent processing
curl -s "http://localhost:8080/search?q=Gemma+4+benchmarks&format=json" | \
  jq -r '.results[:5][] | "[\(.engine)] \(.title) -> \(.url)"'
```

## API examples

### Python FastMCP 3.1 Integration
Exposing SearXNG as a standard tool for autonomous AI agents using FastMCP 3.1 with strict schema enforcement:

```python
import httpx
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from fastmcp import FastMCP

mcp = FastMCP("SearXNG-Search-Server", version="3.1.0")

class SearchParameters(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., min_length=2, max_length=500, description="The search query string")
    category: str = Field(default="general", pattern=r"^(general|it|science|news|files)$")
    max_results: int = Field(default=5, ge=1, le=20)

@mcp.tool()
async def search_web(params: SearchParameters) -> str:
    """Performs a privacy-preserving metasearch query using SearXNG."""
    url = "http://localhost:8080/search"
    query_params = {
        "q": params.query,
        "categories": params.category,
        "format": "json"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=query_params)
            response.raise_for_status()
            data = response.json()

        results = data.get("results", [])[:params.max_results]
        formatted = []
        for item in results:
            title = item.get("title", "No Title")
            res_url = item.get("url", "")
            content = item.get("content", "")
            engine = item.get("engine", "unknown")
            formatted.append(f"[{title}]({res_url}) (via {engine})\n{content}")

        return "\n\n".join(formatted) if formatted else "No results found."
    except Exception as e:
        return f"SearXNG query error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

### Response Validation using Pydantic v2
Validating aggregated SearXNG search responses using strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
import json
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, ValidationError

class SearchResultItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    title: str = Field(..., description="The title of the search result")
    url: HttpUrl = Field(..., description="The source URL of the search result")
    content: Optional[str] = Field(None, description="Text snippet or summary")
    engine: str = Field(..., description="Upstream engine providing the result")
    score: Optional[float] = Field(None, description="Aggregated relevance score")

class SearXNGQueryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

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

if __name__ == "__main__":
    mock_payload = {
        "query": "FastMCP 3.1 specification",
        "results": [
            {
                "title": "Model Context Protocol Spec 3.1",
                "url": "https://modelcontextprotocol.io/spec",
                "content": "Official specification for MCP 3.1 tooling and tasks.",
                "engine": "github",
                "score": 0.95
            }
        ],
        "unresponsive_engines": []
    }
    validated = parse_searxng_response(json.dumps(mock_payload))
    if validated:
        print(f"Validated query '{validated.query}' with {len(validated.results)} results.")
```

## Production Systemd Daemon Unit (`searxng-engine.service`)

For bare-metal or container-runtime hosts running SearXNG under systemd:

```ini
[Unit]
Description=SearXNG Metasearch Engine Daemon
After=network.target network-online.target docker.service
Requires=docker.service
Wants=network-online.target

[Service]
Type=simple
User=searxng
Group=docker
WorkingDirectory=/opt/searxng-stack
ExecStart=/usr/bin/docker compose up
ExecStop=/usr/bin/docker compose down
Restart=always
RestartSec=10s
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Docker Compose Multi-Container Production Cluster

Deploy SearXNG with Redis caching and automated Valkey session storage for high-throughput agent retrieval:

```yaml
version: "3.8"

services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng_metasearch
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng:ro
    environment:
      - SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml
      - SEARXNG_SECRET=a_very_secure_random_secret_key_2027
      - SEARXNG_REDIS_URL=redis://searxng-redis:6379/0
    depends_on:
      - searxng-redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/healthz"]
      interval: 15s
      timeout: 5s
      retries: 3

  searxng-redis:
    image: redis:7.2-alpine
    container_name: searxng_redis
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - searxng_redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  searxng_redis_data:
```

## Diagnostic & Operational Troubleshooting Matrix

| Issue / Symptom | Root Cause | Remediation Strategy |
| :--- | :--- | :--- |
| **HTTP 429 Too Many Requests from Upstream Engines** | Cloud provider IP range blocked by Google, Bing, or Yahoo. | Configure outbound proxy rotation in `settings.yml` (`outgoing.proxies`) or route via residential VPN. |
| **JSONDecodeError / Empty Response on `/search`** | `format: json` is missing from `search.formats` in `settings.yml`. | Add `- json` under `search.formats` and restart the SearXNG service container. |
| **High Search Latency (> 3.5s)** | Straggler engines (e.g. academic or slow code repositories) delaying response aggregation. | Lower `request_timeout` to `2.5` seconds or disable slow engines in `engines` configuration. |
| **All Results Empty for Specific Engine** | Upstream HTML structure changed, breaking the SearXNG scraping parser. | Pull latest Docker image `searxng/searxng:latest` containing updated engine parsers. |
| **CAPTCHA Triggered Repeatedly on Google Engine** | Aggressive concurrent requests from parallel agent loops. | Decrease engine weight (`weight: 0.5`) or substitute Google with DuckDuckGo and Brave engines. |
| **SearXNG Secret Key Warning at Boot** | Missing or default `SEARXNG_SECRET` environment variable. | Generate secure 32-byte secret with `openssl rand -hex 32` and set `SEARXNG_SECRET`. |
| **Pydantic Validation Error on Empty Snippet** | Upstream engine returned `null` content field violating strict model requirements. | Set `content: Optional[str] = Field(None)` to handle null snippets cleanly. |
| **Redis Cache Connection Timeout** | Redis container unreachable or internal Docker bridge DNS lookup failed. | Verify `SEARXNG_REDIS_URL` matches network service name and port (`redis://searxng-redis:6379/0`). |

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
