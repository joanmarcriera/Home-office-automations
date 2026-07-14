# Perplexity Agent API

## What it is
The Perplexity Agent API is a suite of programmatic interfaces released in early 2026 that provide developers with access to Perplexity's agentic workflows and orchestration capabilities. It features specialized models like **Sonar Pro**, **Sonar Reasoning Pro**, and **Sonar Deep Research**, which integrate real-time web search and multi-step reasoning. By July 2026, it has become a standard backend for agents requiring SOTA search-groundedness, often compared to the reasoning density of **Gemma 3** in local environments.

## What problem it solves
It simplifies the creation of research-capable AI agents by offloading the complex tasks of web searching, data extraction, and information synthesis to Perplexity's specialized engine. It eliminates the need for developers to build and maintain their own RAG (Retrieval-Augmented Generation) pipelines for public web data, providing a turn-key solution for grounded AI.

## Where it fits in the stack
**Agentic Search / Orchestration API**. It serves as a high-level tool for agents to perform real-world research and retrieval, often used as a backend for [n8n](../../services/n8n.md) workflows or custom [LangGraph](../frameworks/langgraph.md) agents. It is increasingly utilized via the **MCP 3.0 Task Protocol** for standardized automated benchmarking and research execution.

## Typical use cases
- **Automated Research**: Creating agents that perform deep-dives into specific topics using **Sonar Deep Research**.
- **Real-time Information Retrieval**: Providing apps with up-to-date facts, financial data, or news via the **Finance Search** tool.
- **Workflow Orchestration**: Using Perplexity's reasoning to handle multi-step tasks involving external data with models like **Claude 4.8 Opus** or **GPT-5.5** available via the Agentic Research API.
- **Automated Benchmarking**: Leveraging the MCP 3.0 Task Protocol to run standardized evaluations against real-time web data.

## Strengths
- **SOTA Search Integration**: Direct access to Perplexity's world-class search and retrieval engine with inline citations.
- **Model Marketplace**: Access to OpenAI, Anthropic, Google, and xAI models at direct provider rates plus a flat search fee.
- **Low Capability Damage**: High-fidelity responses with verifiable sources via the `citations` metadata field.
- **Ease of Use**: OpenAI-compatible API allows for drop-in replacement using the OpenAI SDK.
- **Task Protocol Support**: Native integration with MCP 3.0 for structured task execution.

## Limitations
- **Paid Service**: Requires a Perplexity API subscription (usage-based pricing).
- **Rate Limits**: Subject to API usage limits which can be restrictive for high-volume automated agents.
- **Cloud Dependent**: Not suitable for 100% offline or air-gapped environments (unlike [Llama 4](../providers/llama.md) or [Gemma 3](../ai_knowledge/local_llms.md)).

## When to use it
- When your agent needs the absolute latest information from the web (e.g., news, market trends, public filings).
- When you want to leverage Perplexity's citation and source-linking capabilities for groundedness.
- For high-accuracy research tasks where ground truth and verification matter.
- When implementing automated research pipelines using the MCP 3.0 Task Protocol.

## When not to use it
- For strictly private, proprietary data that should not be sent to a cloud search engine.
- For simple logic tasks that don't require external web search (use a local LLM like [Gemma 3](../ai_knowledge/local_llms.md) instead).
- When operating in a low-latency requirement environment where the overhead of web search is prohibitive.

## Getting started

### API Key Management
Perplexity uses a one-time reveal model for API keys. Generate your key in the Perplexity Developer Portal and store it securely in your environment variables.

### Installation
Since the API is OpenAI-compatible, you can use the official OpenAI Python library.

```bash
pip install openai
```

## CLI examples

### Testing the Connection (cURL)
A basic request to the Sonar Pro model to verify connectivity.

```bash
curl -X POST https://api.perplexity.ai/chat/completions \
     -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "sonar-pro",
       "messages": [{"role": "user", "content": "Latest status of the Artemis program?"}]
     }'
```

### Deep Research Request
Triggering a multi-step research workflow.

```bash
curl -X POST https://api.perplexity.ai/chat/completions \
     -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "sonar-deep-research",
       "messages": [{"role": "user", "content": "Detailed technical comparison of Blackwell vs Axion GPUs"}]
     }'
```

## API examples

### Python (OpenAI SDK Integration)
The most common way to integrate Perplexity into an agentic workflow.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "system", "content": "You are a technical researcher. Be precise and cite sources."},
        {"role": "user", "content": "What are the current rate limits for the OpenAI API as of July 2026?"}
    ]
)

print(f"Content: {response.choices[0].message.content}")
print(f"Citations: {response.citations}")
```

### Using the Finance Search Tool
Programmatic access to structured financial data.

```python
import requests

url = "https://api.perplexity.ai/chat/completions"
payload = {
    "model": "sonar-pro",
    "messages": [{"role": "user", "content": "What is the current P/E ratio and next earnings date for NVDA?"}],
    "tools": [{"type": "finance_search"}]
}
headers = {"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}"}

response = requests.post(url, json=payload, headers=headers)
print(response.json()['choices'][0]['message']['tool_calls'])
```

## Related tools / concepts
- [Perplexity](../providers/perplexity.md)
- [Tavily](../providers/tavily.md)
- [SearXNG](../../services/searXNG.md)
- [Firecrawl](../process_understanding/firecrawl.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [Exa AI](../providers/exa_ai.md)
- [Google Search](../ai_knowledge/google-search.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Claude 4.8 Opus](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Perplexity API Pricing 2026: Models, Costs & Optimization Tips](https://www.cloudzero.com/blog/perplexity-api-pricing/)
- [Perplexity API Guide: Search-Grounded AI From Setup to Production (2026)](https://techjacksolutions.com/ai-tools/perplexity/perplexity-api-guide/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
