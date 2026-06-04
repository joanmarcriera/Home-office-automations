# Perplexity AI

## What it is
Perplexity is an AI-powered conversational search engine. It provides real-time information and citations from across the web to answer complex questions.

## What problem it solves
Combines the depth of AI-generated answers with the currency of web search, providing cited, up-to-date responses that go beyond what a static LLM knowledge cutoff can offer.

## Where it fits in the stack
AI & Knowledge — used as a research and information retrieval tool when up-to-date, cited web information is needed.

## Typical use cases
- Researching technical topics with source citations
- Getting up-to-date answers that require current web information
- Comparing tools, libraries, or approaches with cited references

## Strengths
- Provides citations and sources for its answers
- Access to real-time web information beyond LLM training data
- Conversational interface allows follow-up questions to refine results

## Limitations
- Cloud-based service; queries and data are sent to external servers
- Free tier has usage limits; Pro subscription required for heavy use
- Cannot process private or local data

## When to use it
- When you need current, cited information from the web
- When researching topics where accuracy and source verification matter

## When not to use it
- When working with private or sensitive data that should not leave the local network
- When offline access is required

## Getting started

### Installation

Perplexity provides an OpenAI-compatible API. You can use the standard OpenAI Python client to interact with it.

```bash
pip install openai
```

### Minimal Python Example

To use the Perplexity API, you need a valid API key from the [Perplexity API Settings](https://www.perplexity.ai/settings/api).

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_PPLX_API_KEY", base_url="https://api.perplexity.ai")

response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[{"role": "user", "content": "What are the current top 3 Python frameworks for web development in 2026?"}],
)
print(response.choices[0].message.content)
```

## CLI examples

### 1. Basic Search Query (curl)
```bash
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PPLX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-reasoning-pro",
    "messages": [
      {"role": "user", "content": "What is the latest stable version of Kubernetes?"}
    ]
  }'
```

### 2. Precise and Concise Output
```bash
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PPLX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-reasoning-pro",
    "messages": [
      {"role": "system", "content": "Be precise and concise."},
      {"role": "user", "content": "Current price of Bitcoin in USD."}
    ]
  }'
```

### 3. List Supported Models
```bash
# Perplexity uses a specific set of Sonar models. Refer to docs for the latest list.
curl https://api.perplexity.ai/models \
  -H "Authorization: Bearer $PPLX_API_KEY"
```

## API examples

### Python (OpenAI SDK)

```python
from openai import OpenAI

YOUR_API_KEY = "pplx-xxxxxxxx"

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# Chat completion with reasoning and citations
response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[
        {
            "role": "system",
            "content": "You are a professional researcher.",
        },
        {
            "role": "user",
            "content": "Analyze the impact of Model Context Protocol (MCP) on the AI agent ecosystem.",
        },
    ],
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [Google Search](google-search.md)
- [Genspark](genspark.md)
- [ChatGPT](chatgpt.md)
- [Claude](claude.md)
- [Gemini](gemini.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / references
- [Official Website](https://www.perplexity.ai/)
- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Official MCP Website](https://modelcontextprotocol.io/)

## Contribution Metadata

- Last reviewed: 2026-05-28
- Confidence: high
