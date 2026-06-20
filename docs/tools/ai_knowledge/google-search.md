# Google Search

## What it is
Google Search is the world's most widely used web search engine. As of June 2026, it has fully matured into an "Agentic Search" platform, powered by the **Gemini 3.5 Ultra** and **Flash** models. It utilizes the **Antigravity** orchestration layer to provide "AI Mode," which synthesizes real-time web data, generates dynamic UIs, and executes complex multi-step workflows directly within the search interface or via API.

## What problem it solves
It reduces the cognitive load of information retrieval by transitioning from "link providing" to "answer synthesis." It solves the "search-to-action" gap, allowing users and autonomous agents to execute tasks (like booking services, comparing complex datasets, or summarizing technical documentation) without leaving the search context.

## Where it fits in the stack
**AI & Knowledge / Discovery**. In the [Home-Office Architecture](../../architecture/README.md), it serves as the primary **External Grounding Layer**. It provides real-time web context to local agents and is often integrated via the [Model Context Protocol (MCP 3.0)](../../knowledge_base/patterns/tool-calling-and-mcp.md) for secure, tool-augmented research.

## Typical use cases
- **Agentic Grounding**: Providing real-time technical context to local LLMs like Claude 4.8 or GPT-5.5.
- **V-RAG (Vision RAG)**: Using Google's multi-modal capabilities to search and retrieve information from visual documents and charts.
- **Automated Research**: Utilizing Antigravity agents to perform longitudinal studies or market analysis.
- **Dynamic Dashboarding**: Generating real-time visual summaries of fluctuating data (e.g., "track energy prices across 5 providers").

## Strengths
- **Global Index**: The most comprehensive index for long-tail technical and niche content.
- **Gemini 3.5 Integration**: Native, sub-second grounding with high reasoning capabilities.
- **Multi-modal Native**: Superior handling of images, video, and complex document layouts.
- **API Reliability**: Standard-setting uptime and structured data output for enterprise RAG.

## Limitations
- **Privacy Boundary**: Requires careful data handling when integrating with personal household context.
- **Generative Noise**: AI-generated overviews may occasionally include sponsored content or generative artifacts.
- **Subscription Gates**: Advanced agentic features often require a Gemini Advanced or Enterprise tier.

## When to use it
- When you need the absolute latest information from the live web.
- For complex, multi-faceted queries that benefit from AI-led synthesis.
- When grounding agents in the [Home-Office stack](../../architecture/README.md) using official APIs.

## When not to use it
- For queries involving highly sensitive personal data (use [SearXNG](../../services/searXNG.md)).
- When a purely local, private search is required.
- For deep, thread-persistent research where [Perplexity](perplexity.md) might offer better continuity.

## Getting started

### Personal Use
1. Navigate to [google.com](https://www.google.com).
2. Enable "AI Mode" in your search settings to access Gemini 3.5-powered synthesis.
3. Use the Antigravity sidebar to trigger agentic workflows.

### Agentic Integration (Local Setup)
To integrate Google Search into your local agentic stack:
1. Obtain a **Google Cloud API Key** and a **Search Engine ID (CX)** from the [Google Cloud Console](https://console.cloud.google.com/).
2. Install the necessary Python libraries:
   ```bash
   pip install google-api-python-client
   ```
3. Configure your local [LiteLLM](../../services/litellm.md) proxy to include Google Search as a grounding tool.

## CLI examples

### Using the Antigravity CLI
```bash
# Perform an agentic search with a specific research persona
antigravity search "Compare the power efficiency of Llama 4 vs GPT-5.5 for local hosting" --agent deep-research

# Generate a visual report from search data
antigravity report "Solar panel ROI in Seattle 2026" --format markdown > report.md
```

### Legacy Custom Search (curl)
```bash
curl "https://www.googleapis.com/customsearch/v1?key=${GOOGLE_API_KEY}&cx=${GOOGLE_CX}&q=Model+Context+Protocol+v3.0"
```

## API examples

### Python (Google Search Grounding via Gemini API)
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-3.5-ultra')
# Enable Google Search as a tool for real-time grounding
response = model.generate_content(
    "What is the current status of the Matter 1.5 protocol?",
    tools=[{'google_search_retrieval': {}}]
)

print(response.text)
# Inspect grounding metadata for citations
print(response.candidates[0].grounding_metadata.search_entry_point)
```

## Related tools / concepts
- [Perplexity](perplexity.md) — Persistent research-focused search.
- [SearXNG](../../services/searXNG.md) — Privacy-first, self-hosted search aggregator.
- [Gemini](gemini.md) — The underlying model family.
- [Antigravity Ecosystem](https://antigravity.google) — Google's 2026 agent platform.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Protocol for agent-tool communication.
- [Grounding Patterns](../../knowledge_base/patterns/rag.md) — How search is used in RAG pipelines.
- [Home-Office Architecture](../../architecture/README.md) — Central architecture documentation.

## Sources / references
- [Google Search Official](https://www.google.com)
- [Google I/O 2026 Keynote: The Agentic Web](https://blog.google/innovation-and-ai/google-io-2026-recap/)
- [Gemini API Documentation: Search Grounding](https://ai.google.dev/gemini-api/docs/grounding)
- [Antigravity Developer Portal](https://developers.google.com/antigravity)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
