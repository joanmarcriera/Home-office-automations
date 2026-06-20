# Perplexity AI

## What it is
Perplexity is a leading AI-powered conversational search engine that provides real-time information with verifiable citations. As of June 2026, it utilizes a sophisticated orchestration layer to route queries between frontier models like Gemini 3.5, Claude 4.8, and their own fine-tuned "Sonar" models. It is designed to bridge the gap between static LLM knowledge and the live web.

## What problem it solves
Perplexity addresses the "hallucination" and "knowledge cutoff" problems of traditional LLMs by grounding every response in current web data. It provides users with direct links to sources, allowing for rapid verification of facts, technical specifications, and current events. It serves as a more efficient alternative to traditional keyword-based search by synthesizing multiple sources into a single, cohesive answer.

## Where it fits in the stack
**Category**: AI & Knowledge / Agentic Search
Perplexity serves as the primary "Knowledge Retrieval" layer for researchers and developers. It is often integrated into agentic workflows via its OpenAI-compatible API to provide real-time grounding for autonomous agents.

## Typical use cases
- **Technical Research**: Discovering the latest stable versions of libraries, APIs, and frameworks with cited documentation.
- **Market Intelligence**: Tracking real-time financial data, product launches, and industry trends.
- **Fact-Checking**: Verifying claims by reviewing the primary sources cited in the response.
- **Comparative Analysis**: Generating cited comparisons between tools, services, or architectural patterns.

## Strengths
- **Verifiable Citations**: Every claim is linked to a source, drastically reducing hallucinations.
- **Real-Time Web Access**: No knowledge cutoff; access to news and data published minutes ago.
- **Model Choice**: Pro users can toggle between different frontier models for varied reasoning styles.
- **Multi-modal Search**: Supports searching and analyzing uploaded files (PDFs, CSVs) alongside web data.
- **Integration**: Offers a robust, OpenAI-compatible API for programmatic access.

## Limitations
- **External Dependency**: As a cloud-based service, it requires internet access and involves sending data to third-party servers.
- **Privacy Concerns**: Not suitable for processing highly sensitive or proprietary data that cannot leave the local network.
- **API Cost**: High-volume usage via API can be more expensive than self-hosted RAG solutions.
- **Source Quality**: The accuracy of the answer is ultimately dependent on the quality and reliability of the web sources retrieved.

## When to use it
- When you need the most up-to-date information available on the web.
- When source verification and citations are critical for your work.
- When conducting rapid research on topics outside your immediate expertise.

## When not to use it
- When working with **private, air-gapped, or highly confidential data**.
- When you require absolute deterministic outputs (search results can vary over time).
- When offline access is a requirement.

## Getting started

### Account Setup
Sign up at [perplexity.ai](https://www.perplexity.ai/) to access the conversational interface. API keys can be generated in the [API Settings](https://www.perplexity.ai/settings/api).

### API Installation
Perplexity provides an OpenAI-compatible API.

```bash
pip install openai
```

### Minimal API Example (Python)
```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_PPLX_API_KEY", base_url="https://api.perplexity.ai")

response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[{"role": "user", "content": "What is the status of MCP 3.0 adoption in June 2026?"}]
)
print(response.choices[0].message.content)
```

## CLI examples

### 1. Basic Search (curl)
```bash
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PPLX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-reasoning-pro",
    "messages": [
      {"role": "user", "content": "Latest stable version of Kubernetes as of today."}
    ]
  }'
```

### 2. Precise Research Query
```bash
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PPLX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-reasoning-pro",
    "messages": [
      {"role": "system", "content": "Focus on peer-reviewed academic sources."},
      {"role": "user", "content": "Impact of quantum computing on RSA encryption."}
    ]
  }'
```

## API examples

### Python (OpenAI SDK with citations)
```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY", base_url="https://api.perplexity.ai")

# Using 'sonar-reasoning-pro' for complex research tasks
response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[
        {"role": "system", "content": "You are a senior technical architect."},
        {"role": "user", "content": "Compare Tailscale vs Headscale for a 100-node agentic mesh network."}
    ]
)

content = response.choices[0].message.content
print(f"Citations and Analysis: {content}")
```

### Integration with Agentic Frameworks
Perplexity can be used as a `tool` or `skill` within agentic frameworks to provide external knowledge.

```python
# Simplified pseudocode for agentic tool use
def web_search(query: str):
    return client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": query}]
    ).choices[0].message.content
```

## Related tools / concepts
- [Google Search](google-search.md) — Traditional search with agentic overlays.
- [Genspark](genspark.md) — AI-driven research and custom page generation.
- [ChatGPT](chatgpt.md) — Competitor with integrated "SearchGPT" features.
- [Claude](claude.md) — High-reasoning model often used to process Perplexity outputs.
- [Gemini](gemini.md) — Google's multi-modal model with deep search integration.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Protocol for connecting search tools to agents.
- [SearXNG Automation](../../services/searXNG-automation.md) — Privacy-first, self-hosted meta-search alternative.
- [LiteLLM](../../services/litellm.md) — Proxy for managing Perplexity API access.

## Sources / references
- [Perplexity Official Website](https://www.perplexity.ai/)
- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Official Model Context Protocol (MCP) Website](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
