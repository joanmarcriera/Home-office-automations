# Tavily

## What it is
Tavily is a search and web-extraction provider built specifically for AI agents and LLM applications. As of late August 2026, it operates as a core component of the **Nebius Group** AI cloud ecosystem. It provides a specialized API that returns structured, cleaned, and LLM-ready content from the live web, optimized for RAG (Retrieval-Augmented Generation) and agentic research.

## What problem it solves
It gives agents a reliable way to search the web and retrieve grounded results without the "glue code" burden of generic search scraping or parsing raw HTML. Tavily handles JavaScript rendering, proxy rotation, and content deduplication automatically, delivering context-rich, citation-ready results with minimal latency.

## Where it fits in the stack
Tavily sits in the **Providers / Search** layer. It acts as the primary "Agentic Search" interface, allowing autonomous models to access real-time information and external knowledge to augment their static training data.

## Typical use cases
- **Agentic Research**: Powering multi-step loops (like [DeerFlow](../agents/deerflow.md)) that search, evaluate, and synthesize complex findings.
- **Real-time RAG**: Providing fresh web context for grounding LLM outputs in production applications.
- **Fact-Checking & Verification**: Automatically verifying claims by searching high-authority sources in real-time.
- **Competitor Monitoring**: Automated tracking of market trends, news, and product launches with structured extraction.

## Strengths
- **LLM-Optimized Results**: Returns results in structured JSON with summaries, citations, and highlights that models can immediately process.
- **RAG-First Features**: Specialized endpoints like `get_search_context` return a single combined string of relevant context to minimize token usage.
- **Nebius Cloud Scale**: Deep integration with Nebius infrastructure ensures high availability and enterprise-grade performance.
- **Built-in Research Logic**: The `/research` endpoint can generate comprehensive research reports across multiple sources in a single call.
- **Native MCP 3.1 Support**: Provides an official Model Context Protocol (MCP 3.1) server for seamless integration with Claude Desktop, GPT-5.5 tools, and other agentic workbenches.

## Limitations
- **API Latency**: Advanced search depth (which uses multiple scrapers) can introduce 1-3 seconds of latency.
- **Cost for Scale**: High-volume automated research loops can become expensive compared to self-hosted alternatives like [SearXNG](../../services/searXNG.md).
- **Nebius Ecosystem Tie-in**: Roadmap is increasingly aligned with the broader Nebius AI platform.

## When to use it
- When your agents need high-quality, real-time web information with zero scraping management.
- For production RAG systems where grounding and citation accuracy are critical.
- When you need a "set and forget" search layer with native integration into frameworks like LangChain or Vercel AI SDK.

## When not to use it
- For basic web searches where a free, generic search API is sufficient.
- When you need to host your own search infrastructure due to privacy or cost (use [SearXNG](../../services/searXNG.md)).
- When document retrieval is limited to a closed, internal knowledge base.

## Getting started

### Installation
```bash
pip install tavily-python
# Or for Node.js
npm install @tavily/core
```

### Quick Search
```python
from tavily import TavilyClient

tavily = TavilyClient(api_key="tvly-YOUR_API_KEY")
# Late August 2026 update supporting Claude 5.1 and GPT-5.5 optimization parameters
response = tavily.search(
    query="Current status of the Model Context Protocol MCP 3.1",
    search_depth="advanced",
    include_answer=True,
    max_results=5
)

for result in response['results']:
    print(f"[{result['score']}] {result['title']}: {result['url']}")
```

## CLI examples
Tavily provides a CLI for quick research and configuration.

```bash
# Research a topic and output a report
tavily research "Impact of GPT-5.5 on enterprise automation" --format markdown

# Search and get context-only output
tavily search "Nebius Tavily integration 2026" --context-only

# Verify API key and usage
tavily usage
```

## API examples

### Agentic Research Endpoint (v3.1)
```python
# Programmatic search utilizing advanced filtering for frontier models (Claude 5.1, GPT-5.5)
research_report = tavily.research(
    query="Comprehensive audit of late 2026 vector database performance",
    search_depth="advanced",
    max_results=20,
    topic="general"
)

# Output includes synthesized report and all source citations
print(research_report['report'])
```

### MCP 3.1 Configuration (`claude_desktop_config.json`)
The Model Context Protocol (MCP 3.1) setup enables seamless tool schema binding:
```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server@latest"],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR_API_KEY"
      }
    }
  }
}
```

## Related tools / concepts
- [Exa AI](../providers/exa_ai.md) - Embedding-based search for agentic retrieval.
- [Perplexity API](../providers/perplexity.md) - Conversational search and grounding.
- [SearXNG](../../services/searXNG.md) - Self-hosted search aggregator.
- [Firecrawl](../process_understanding/firecrawl.md) - Web crawling optimized for LLM use.
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) - Unified framework with native Tavily support.
- [Agentic Search](../../knowledge_base/patterns/search-patterns.md) - The architectural pattern Tavily powers.
- [DeerFlow](../agents/deerflow.md) - Agentic research framework using Tavily.
- [Nebius Group](https://nebius.com) - The parent company and AI cloud provider.

## Sources / References
- [Official Website](https://tavily.com/)
- [Tavily Documentation](https://docs.tavily.com/)
- [Nebius Acquisition Announcement](https://nebius.com/news/tavily-acquisition)
- [Tavily v3.1 Release Notes (August 2026)](https://docs.tavily.com/release-notes/v3)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-08-05
