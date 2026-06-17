# SearXNG

SearXNG is a free internet metasearch engine which aggregates results from more than 70 search services, providing a privacy-preserving and agent-friendly search infrastructure in June 2026.

## What it is
SearXNG is a free internet metasearch engine which aggregates results from more than 70 search services (engines). It provides a private, decentralized search experience by acting as a proxy between you and major search engines like Google, Bing, and DuckDuckGo.

## What problem it solves
It strips tracking cookies and personal data from your requests, preventing search engines from profiling you. It also solves the "fragmentation" problem by combining results from multiple niche and general engines into a single, structured interface, which is particularly valuable for LLMs and autonomous agents like Claude 4.8 Opus.

## Where it fits in the stack
**Category**: Services / Search & Discovery. It serves as a privacy-preserving front-end for web search and acts as a **primary data retrieval tool** for local AI agents. It often sits behind a reverse proxy like Nginx or Traefik and is secured via [Authentik](authentik.md).

## Typical use cases
- **Private Web Searching**: No tracking or profiling during daily browsing.
- **Agentic Information Retrieval**: Providing a search API for local AI agents to browse the live web.
- **Source Aggregation**: Combining results from Wikipedia, GitHub, and Google for a unified technical overview.
- **RAG Context Filling**: Using SearXNG to fetch real-time data for Retrieval-Augmented Generation loops.
- **Local Knowledge Base Integration**: Configuring SearXNG to search your local documentation via custom JSON engines.

## Strengths
- **Privacy-First**: No tracking, no profiling, no cookies.
- **Aggregated Results**: Combines results from 70+ engines.
- **Customizable**: Extensive settings for engines, categories, and UI.
- **Self-Hostable**: Easy to deploy via Docker.
- **Open API**: Provides search results in JSON format, ideal for MCP (Model Context Protocol) integration.
- **Cost**: Free and Open Source (AGPL-3.0).

## Limitations
- **Upstream Reliability**: If an upstream engine (like Google) blocks SearXNG's IP, results from that engine may be missing.
- **Maintenance**: Requires occasional updates to keep engine scrapers functioning.
- **Performance**: Aggregating from 70+ sources can be slower than a single-source search.

## When to use it
- When you value privacy and want to avoid being tracked by major search engines.
- When you want to combine results from multiple niche engines (e.g., academic, code, news).
- When building local AI tools that need to search the web without reliance on proprietary search APIs.

## When not to use it
- If you rely heavily on personalized search results (e.g., "restaurants near me" based on Google History).
- If you don't want to manage your own search infrastructure or deal with potential IP blocks.

## Getting started

### Installation (Docker Compose)
```yaml
services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng
    environment:
      - SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml
    restart: always
```

### Custom Engine Configuration
SearXNG allows granular control over engine priority and local integration via `settings.yml`.

```yaml
# /etc/searxng/settings.yml
engines:
  - name: google
    weight: 1.0
  - name: wikipedia
    weight: 2.0  # Give Wikipedia higher priority
  - name: github
    weight: 3.0  # Bias heavily towards code for dev workflows

  - name: local-knowledge-base
    engine: json_engine
    search_url: http://your-docs-site:8000/search?q={query}
    results_query: results
    title_query: title
    url_query: url
    content_query: snippet
    categories: general
    weight: 5.0  # Force local knowledge to the top
```

## CLI examples

SearXNG is primarily a web service, but you can interact with it via `curl` to test the API or retrieve results.

```bash
# curl (JSON Search)
curl "http://localhost:8080/search?q=open+source+llm&format=json"

# curl (Specific Category)
curl "http://localhost:8080/search?q=sunset&categories=images&format=json"

# curl (Specific Engine)
curl "http://localhost:8080/search?q=SearXNG&engines=wikipedia&format=json"
```

## API examples

### Python (Simple Search)
```python
import requests

url = "http://localhost:8080/search"
params = {
    "q": "Model Context Protocol",
    "format": "json"
}

response = requests.get(url, params=params)
results = response.json()

for result in results.get('results', []):
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}\n")
```

### Advanced: RAG Pipeline Pattern (Python)
This example demonstrates using SearXNG in a retrieval-augmented generation (RAG) loop with custom weighting for specific engines.

```python
import requests

def rag_search(query, search_domain="tech"):
    url = "http://localhost:8080/search"
    if search_domain == "tech":
        params = {
            "q": query,
            "engines": "github,stackoverflow,wikipedia,reddit",
            "categories": "it",
            "format": "json",
            "time_range": "month"
        }
    else:
        params = {"q": query, "format": "json"}

    response = requests.get(url, params=params)
    results = response.json().get('results', [])

    context_snippets = [
        f"Source: {r['url']}\nSnippet: {r.get('content', '')}"
        for r in results[:5]
    ]
    return "\n\n".join(context_snippets)
```

## Related tools / concepts
- [Perplexity](../tools/ai_knowledge/perplexity.md) — AI-powered search engine.
- [n8n](n8n.md) — For automating search workflows.
- [Ollama](ollama.md) — To use search results with local LLMs.
- [Paperless-ngx](paperless-ngx.md) — For archiving and managing documents.
- [IT-Tools](it-tools.md) — Comprehensive developer utility suite.
- [Linkwarden](linkwarden.md) — To save and organize search results.
- [Crawl4AI](../tools/process_understanding/crawl4ai.md) — For high-performance scraping of search results.
- [Authentik](authentik.md) — For securing the SearXNG web interface.

## Sources / References
- [Official Website](https://searxng.org/)
- [GitHub Repository](https://github.com/searxng/searxng)
- [Documentation](https://docs.searxng.org/)
- [LangChain SearXNG Integration](https://python.langchain.com/docs/integrations/tools/searxng_search)

## Backlog
- [x] Perform technical freshness audit (June 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-16
