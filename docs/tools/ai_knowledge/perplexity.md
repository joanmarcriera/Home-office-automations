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

## Related tools / concepts
- [Google Search](https://www.google.com)
- [Genspark](https://www.genspark.ai/)

## Getting started

Perplexity provides an OpenAI-compatible API. You can use the standard OpenAI Python client to interact with it. To use the Perplexity API, you need a valid API key from the [Perplexity API Settings](https://www.perplexity.ai/settings/api).

```bash
pip install openai
```

## API examples

### Calling Perplexity API with Python

```python
from openai import OpenAI

YOUR_API_KEY = "pplx-xxxxxxxx"

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# Chat completion without streaming
response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[
        {
            "role": "system",
            "content": "Be precise and concise.",
        },
        {
            "role": "user",
            "content": "What are the latest developments in MCP (Model Context Protocol)?",
        },
    ],
)
print(response.choices[0].message.content)
```

### Calling Perplexity API with curl

```bash
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer {YOUR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-reasoning-pro",
    "messages": [
      {"role": "system", "content": "Be precise and concise."},
      {"role": "user", "content": "How many stars are in the Milky Way?"}
    ]
  }'
```

## Sources / references
- [Official Website](https://www.perplexity.ai/)

## Contribution Metadata

- Last reviewed: 2026-03-01
- Confidence: medium
