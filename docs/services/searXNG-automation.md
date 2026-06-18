# SearXNG Automation

SearXNG Automation provides the patterns and programmatic interfaces for using a self-hosted [SearXNG](searXNG.md) instance as a primary knowledge retrieval layer for AI agents and automated workflows. In the June 2026 landscape, it serves as a privacy-preserving, high-performance alternative to commercial search APIs for "Deep Research" agents.

## What it is
SearXNG Automation is the practice of interacting with SearXNG's JSON API to perform aggregated web searches. It enables local LLMs and agents to browse the live web, bypass corporate tracking, and consolidate results from over 70 engines (including Google, Bing, DuckDuckGo, and Wikipedia) into a single, structured data stream. By 2026, it is frequently exposed via the **Model Context Protocol (MCP 3.0)** to provide frontier models like Claude 4.8 Opus and GPT-5.5 with real-time world knowledge.

## What problem it solves
It solves the dependency on expensive, data-hungry commercial search APIs (like Tavily or Google Search API). SearXNG Automation provides a "Search-as-a-Service" layer within a private homelab or enterprise network, offering unlimited queries without per-request costs, while protecting the user's IP and search history from upstream tracking.

## Where it fits in the stack
**Category**: Services / Search Automation
It serves as the **Retrieval Layer** for RAG (Retrieval-Augmented Generation) systems and the "eyes" for autonomous agents that need to fact-check or research topics beyond their training data.

## Typical use cases
- **AI Deep Research**: Powering local "Perplexity-style" search agents that synthesize information from multiple web sources.
- **Automated Fact-Checking**: Scripts that verify claims by querying authoritative sources (Wikipedia, Arxiv) via SearXNG.
- **Privacy-First News Aggregation**: Creating daily custom digests without being profiled by news trackers.
- **Price and Availability Monitoring**: Programmatically checking for product updates across diverse e-commerce engines.
- **Agentic Information Retrieval**: Allowing a Claude 4.8 agent to decide when it needs to "look up" information to complete a task.

## Strengths
- **Privacy-Centric**: Aggregates and proxies requests, stripping all identifying information from upstream engines.
- **Cost-Effective**: Zero marginal cost per query once the instance is hosted.
- **Highly Aggregated**: Access to specialized engines (Scientific, Files, Images, Social Media) in a single request.
- **JSON-Native**: Returns clean, machine-readable results that are easy for LLMs to parse.
- **Extensible**: Easy to add custom search engines or filter existing ones via `settings.yml`.

## Limitations
- **Upstream Resilience**: High-volume automation can lead to IP blocks if not managed via a rotating proxy pool.
- **Latency**: The search speed is limited by the slowest upstream engine; timeouts must be carefully tuned.
- **Scraper Fragility**: Changes to upstream search engine HTML can occasionally break individual engines until the next SearXNG update.

## When to use it
- When building private AI agents that require web access.
- When you need to search multiple specialized engines (e.g., GitHub, StackOverflow, and Reddit) simultaneously.
- When you want to avoid the cost and tracking associated with commercial search APIs.

## When not to use it
- For ultra-low latency requirements (sub-200ms) where a single-engine direct API might be faster.
- For extremely high-volume enterprise traffic without a sophisticated proxy and infrastructure setup.

## Getting started

### Enable JSON Output
Ensure the JSON format is enabled in your `settings.yml`:

```yaml
search:
  formats:
    - html
    - json
```

### Basic API Call (curl)
```bash
curl "http://localhost:8080/search?q=Model+Context+Protocol&format=json"
```

## CLI examples

### Filter Results with jq
Get the top 3 URLs and titles for a query:
```bash
curl -s "http://localhost:8080/search?q=homelab+automation&format=json" | \
jq -r '.results[:3][] | "\(.title): \(.url)"'
```

### Search Specific Categories
Limit the search to the "science" category:
```bash
curl -s "http://localhost:8080/search?q=quantum+computing&categories=science&format=json"
```

### Scripted Engine Selection
Search only Wikipedia and DuckDuckGo:
```bash
curl -s "http://localhost:8080/search?q=Python&engines=wikipedia,duckduckgo&format=json"
```

## API examples

### Python (Simple Search Client)
```python
import requests

def search(query, engines=["google", "bing"]):
    url = "http://localhost:8080/search"
    params = {
        "q": query,
        "format": "json",
        "engines": ",".join(engines)
    }
    response = requests.get(url, params=params)
    return response.json().get('results', [])

results = search("Best privacy-first LLMs")
for r in results[:2]:
    print(f"{r['title']} - {r['url']}")
```

### LangChain Integration
```python
from langchain_community.utilities import SearxSearchWrapper

search = SearxSearchWrapper(searx_host="http://localhost:8080")
result = search.run("What is the latest version of Matrix Synapse?")
print(result)
```

## Related tools / concepts
- [SearXNG](searXNG.md) — The core self-hosted search engine.
- [n8n](n8n.md) — For orchestrating search-based automation workflows.
- [LiteLLM](../services/litellm.md) — Unified inference proxy for search-enabled agents.
- [Ollama](../services/ollama.md) — Local LLM runner that can ingest SearXNG results.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Used to expose SearXNG as a tool for agents.
- [Playwright](../tools/development_ops/playwright.md) — Used for deep-scraping URLs discovered by SearXNG.
- [Tavily](../tools/providers/tavily.md) — Commercial alternative for AI-optimized search.
- [Perplexity Agent API](../tools/agents/perplexity-agent-api.md) — Managed search-as-an-agent service.

## Sources / references
- [SearXNG Official API Docs](https://docs.searxng.org/dev/search_api.html)
- [SearXNG Settings Guide](https://docs.searxng.org/admin/settings/settings.html)
- [Agentic Search Patterns (2026)](https://ai.riera.co.uk/knowledge_base/patterns/agentic-search)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
