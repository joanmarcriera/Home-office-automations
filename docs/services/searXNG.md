# SearXNG

SearXNG is a free internet metasearch engine which aggregates results from more than 70 search services.

## Description
It focuses on privacy, ensuring that users are neither tracked nor profiled. It is highly customizable and can be self-hosted to provide a private search experience for your network.

## Typical use cases
- **Private Web Search**: Search multiple engines (Google, Bing, DuckDuckGo) without being tracked.
- **Agentic Tooling**: Provide local LLM agents with a reliable, structured way to browse the internet.
- **Community Search Hub**: Host a shared search service for friends and family on your local network.

## When to use it
- When you want to combine results from multiple engines while maintaining privacy.
- When you need a programmable search endpoint for automation and AI agents.
- When you want to self-host your core internet services.

## When not to use it
- If you require deeply personalized results based on your search history.
- If you cannot maintain a server for the search engine (consider using public instances).

## Getting started

### Docker
To run SearXNG using Docker:

```bash
# Create a folder and set up secrets
mkdir searxng && cd searxng
docker run --rm -it searxng/searxng -w

# Start SearXNG
docker run -d -p 8080:8080 -v ${PWD}/searxng:/etc/searxng --name searxng searxng/searxng
```

Access the UI at `http://localhost:8080`.

## API examples

### Search with JSON Output
Request structured results via `curl`:

```bash
curl "http://localhost:8080/search?q=open+source+ai&format=json"
```

*Note: Ensure `format=json` is enabled in your `settings.yml`.*

## Links
- [Official Website](https://searxng.org/)
- [GitHub Repository](https://github.com/searxng/searxng)

## Alternatives
- [Perplexity](../tools/ai_knowledge/perplexity.md)
- [DuckDuckGo](https://duckduckgo.com/)

## Backlog
- Configure as default search engine in browser for all local devices.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-08

## Sources / References
- https://searxng.org/
- https://github.com/searxng/searxng
- https://docs.searxng.org/dev/search_api.html
- https://duckduckgo.com/
