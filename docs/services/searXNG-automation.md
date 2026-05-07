# SearXNG Automation

Patterns and tools for using SearXNG as a programmatic search provider.

## What it is
SearXNG Automation involves interacting with a self-hosted [SearXNG](searXNG.md) instance via its JSON API to provide web search capabilities to AI agents, scripts, and other services.

## What problem it solves
It provides a private, rate-limit-friendly way for local scripts and AI models to access web information. Unlike commercial search APIs (like Google or Bing), SearXNG is free to use once self-hosted and aggregates results from dozens of sources.

## Where it fits in the stack
**Category**: Services / Search Automation. It acts as the "Web Retrieval" layer for AI agents and automated research pipelines.

## Typical use cases
- Giving a local LLM (via Ollama or LangChain) the ability to search the live web.
- Automated brand monitoring or news aggregation scripts.
- Building a private "Daily Briefing" that searches for specific topics every morning.
- Programmatically checking for broken links or updated information on specific sites.

## Strengths
- **No API Keys**: Once hosted, you have full control and no per-query costs.
- **Aggregated Data**: Access results from Google, Bing, Wikipedia, and 70+ others in one request.
- **Privacy**: Your automated queries are proxied and stripped of tracking data.
- **JSON Output**: Results are returned in a clean, machine-readable format.

## Limitations
- **Upstream Blocking**: High-frequency automation can lead to your SearXNG IP being blocked by major search engines (use proxies if needed).
- **Format Stability**: Changes in upstream engine HTML can occasionally break scrapers, requiring SearXNG updates.

## When to use it
- When building AI agents that need to browse the web without expensive API fees.
- When you want to maintain full privacy for your automated search queries.
- For niche research tasks that require data from multiple search engines simultaneously.

## When not to use it
- For extremely high-volume (thousands per minute) search tasks without a sophisticated proxy setup.
- If you need real-time, millisecond-latency search results (SearXNG latency is tied to the slowest upstream engine).

## Getting started

### Prerequisites
- A running [SearXNG](searXNG.md) instance.
- JSON output enabled in `settings.yml`:
  ```yaml
  search:
    formats:
      - html
      - json
  ```

### Hello World (curl)
Test the API from your command line:
```bash
curl "http://localhost:8080/search?q=open+source+llm&format=json"
```

### Hello World (Python)
```python
import requests

def search_searxng(query):
    url = "http://localhost:8080/search"
    params = {"q": query, "format": "json"}
    response = requests.get(url, params=params)
    return response.json()

results = search_searxng("Model Context Protocol")
print(f"Top Result: {results['results'][0]['title']}")
```

## CLI examples

Automation often involves filtering results via command line tools like `jq`.

```bash
# Get only the URLs of the top 5 results
curl -s "http://localhost:8080/search?q=homelab&format=json" | jq -r '.results[:5][].url'

# Search specifically for images and save the first URL to a file
curl -s "http://localhost:8080/search?q=sunset&categories=images&format=json" | jq -r '.results[0].img_src' > image_url.txt

# Search Wikipedia via SearXNG
curl -s "http://localhost:8080/search?q=Python&engines=wikipedia&format=json" | jq -r '.results[0].content'
```

## API examples

### LangChain Integration
SearXNG is a first-class tool in the LangChain ecosystem.

```python
from langchain_community.utilities import SearxSearchWrapper

# Configure the wrapper
search = SearxSearchWrapper(searx_host="http://localhost:8080")

# Run a query
output = search.run("What are the latest features of n8n?")
print(output)
```

### n8n Integration (HTTP Request)
In n8n, use the **HTTP Request** node to fetch search results:
- **Method**: GET
- **URL**: `http://searxng:8080/search`
- **Query Parameters**:
  - `q`: `{{ $json["query"] }}`
  - `format`: `json`
- This allows your workflows to "research" topics before making decisions or sending notifications.

## Related tools / concepts
- [SearXNG](searXNG.md) (The core service)
- [n8n](n8n.md) (To orchestrate search-based workflows)
- [Ollama](../services/ollama.md) (To process search results with local AI)
- [LangChain](../tools/ai_knowledge/langchain.md) (For building search-enabled agents)
- [Tavily](../tools/providers/tavily.md) (Commercial alternative)

## Sources / References
- [SearXNG API Documentation](https://docs.searxng.org/dev/search_api.html)
- [LangChain SearXNG Documentation](https://python.langchain.com/docs/integrations/tools/searx_search/)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-12
