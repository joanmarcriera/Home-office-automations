# Google Search

## What it is
Google Search is the world's most widely used web search engine. As of 2026, it has transitioned into an "Agentic Search" platform, utilizing the **Gemini 3.5 Flash** model and the **Antigravity** platform to provide "AI Mode," which synthesizes answers, generates custom UIs, and executes agentic workflows directly within the search interface.

## What problem it solves
It provides near-instant access to billions of web pages while reducing the cognitive load of sifting through links. It solves the "search to action" gap by allowing users to execute tasks (like booking travel or summarizing technical manuals) without leaving the search results.

## Where it fits in the stack
**AI & Knowledge**. It is a primary "grounding" source for AI agents. In the [Home-Office Architecture](../../architecture/README.md), it serves as the **Discovery and Grounding** layer, providing real-time web context to local agents like [Ralph](../../reference-implementations/llm-prompts/family-context.md).

## Typical use cases
- **Grounding for Agents**: Providing real-time technical documentation to local LLMs.
- **AI Mode Synthesis**: Getting a single, cited answer for complex "how-to" homelab queries.
- **Antigravity Agent Integration**: Using search-based agents to perform multi-step research tasks.
- **Dynamic UI Generation**: Generating mini-dashboards or visual tools for data-heavy queries (e.g., "compare power usage of 5 vector databases").

## Strengths
- **Massive Index**: Still the gold standard for finding niche or long-tail technical content.
- **Gemini 3.5 Flash Integration**: Extremely fast (sub-second) AI summaries and "AI Mode" responses.
- **Agentic Infrastructure**: Native support for **Antigravity** agents that can perform tasks across the Google ecosystem.
- **Custom Search API**: High reliability and structured data for RAG pipelines.

## Limitations
- **Generative Ads**: Ads are now integrated directly into AI Overviews and AI Mode responses.
- **Privacy Trade-offs**: Deep integration with "Personal Intelligence" (Gmail/Photos) requires broad data access.
- **AI Hallucinations**: Despite grounding, synthesized answers can still misinterpret complex technical nuances.
- **Search-to-Action Friction**: Many agentic features require a Google/Gemini subscription for full capability.

## When to use it
- When you need the most comprehensive and up-to-date web index.
- For "AI Mode" queries that require synthesizing information from multiple authoritative sources.
- When grounding local agents using the Custom Search API or the new **Gemini Grounding** features.

## When not to use it
- For queries involving highly sensitive or private household data (consider [SearXNG](../../services/searXNG.md)).
- When you want a purely local, non-tracking search experience.
- For deep, iterative research where [Perplexity](perplexity.md)'s persistent thread model might be superior.

## Getting started

### Python (Google Custom Search API)
The recommended way for homelab agents to access Google Search data securely.

```python
import requests

def google_search(query, api_key, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cx
    }
    response = requests.get(url, params=params)
    return response.json()

# Example usage
# results = google_search("n8n wyoming protocol integration", "YOUR_KEY", "YOUR_CX")
```

### Gemini Grounding (v1.5+ / v3.5)
Modern agents can now use the Gemini API with "Google Search Grounding" enabled to get verified citations natively.

```python
# Pseudo-code for Gemini API Grounding
model = genai.GenerativeModel('gemini-3.5-flash')
response = model.generate_content(
    "How do I set up a local vector DB in 2026?",
    tools=[{'google_search_retrieval': {}}]
)
print(response.text)
print(response.candidates[0].grounding_metadata)
```

## CLI examples

```bash
# Using the new Antigravity CLI for agentic search tasks
antigravity search "Summarize the latest Home Assistant release notes" --agent research

# Legacy Custom Search check
curl "https://www.googleapis.com/customsearch/v1?key=KEY&cx=CX&q=test"
```

## Related tools / concepts
- [Perplexity](perplexity.md)
- [SearXNG](../../services/searXNG.md)
- [Antigravity Ecosystem](https://antigravity.google) — Google's 2026 agent platform.
- [Gemini](gemini.md) — the model family powering Google's AI features.
- [Architecture](../../architecture/README.md)
- [Grounding with Google Search](https://blog.google/technology/ai/google-search-grounding-ai-overviews/)

## Sources / references
- [Official Website](https://www.google.com)
- [Google I/O 2026: The Agentic Gemini Era](https://blog.google/innovation-and-ai/sundar-pichai-io-2026/)
- [Google Custom Search API Documentation](https://developers.google.com/custom-search/v1/overview)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
