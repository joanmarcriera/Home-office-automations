# SearXNG

## What it is
SearXNG is a free internet metasearch engine which aggregates results from more than 70 search services (engines).

## What problem it solves
It provides a private, decentralized search experience by acting as a proxy between you and major search engines like Google, Bing, and DuckDuckGo. It strips tracking cookies and personal data from your requests, preventing search engines from profiling you.

## Where it fits in the stack
**Category**: Services / Search & Discovery. It serves as a privacy-preserving front-end for web search within a homelab or private network.

## Typical use cases
- Private web searching without tracking or profiling.
- Aggregating results from multiple engines into a single interface.
- Providing a search API for local AI agents (e.g., using SearXNG as a tool for an LLM).
- Self-hosting search for a home or small office network.

## Strengths
- **Privacy-First**: No tracking, no profiling, no cookies.
- **Aggregated Results**: Combines results from 70+ engines.
- **Customizable**: Extensive settings for engines, categories, and UI.
- **Self-Hostable**: Easy to deploy via Docker.
- **Open API**: Provides search results in JSON format for programmatic use.

## Limitations
- **Upstream Reliability**: If an upstream engine (like Google) blocks SearXNG's IP, results from that engine may be missing.
- **Maintenance**: Requires occasional updates to keep engine scrapers functioning.

## When to use it
- When you value privacy and want to avoid being tracked by major search engines.
- When you want to combine results from multiple niche engines.
- When building local AI tools that need to search the web.

## When not to use it
- If you rely heavily on personalized search results or localized features that require tracking.
- If you don't want to manage your own search infrastructure.

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

### Hello World (Web)
1. Start the SearXNG container.
2. Navigate to `http://localhost:8080`.
3. Type a query in the search bar and press Enter to see aggregated results.

## CLI examples

SearXNG is primarily a web service, but you can interact with it via `curl` to test the API or retrieve results.

### curl (JSON Search)
```bash
curl "http://localhost:8080/search?q=open+source+llm&format=json"
```

### curl (Specific Category)
```bash
curl "http://localhost:8080/search?q=sunset&categories=images&format=json"
```

### curl (Specific Engine)
```bash
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

### Python (Using with LangChain)
SearXNG can be used as a search tool for AI agents.
```python
from langchain_community.utilities import SearxSearchWrapper

search = SearxSearchWrapper(searx_host="http://localhost:8080")
results = search.run("What is vLLM?")
print(results)
```

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Perplexity](../tools/ai_knowledge/perplexity.md) (AI-powered search)
- [DuckDuckGo](https://duckduckgo.com/) (Privacy-focused search)
- [n8n](../services/n8n.md) (For search automation)
- [Ollama](../services/ollama.md) (To use SearXNG results with local LLMs)
- [JSON-LD](https://json-ld.org/) (Metadata standard used in results)

## Sources / References
- [Official Website](https://searxng.org/)
- [GitHub Repository](https://github.com/searxng/searxng)
- [Documentation](https://docs.searxng.org/)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
