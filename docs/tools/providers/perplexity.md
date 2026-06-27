# Perplexity

## What it is
Perplexity is an AI-powered search engine and LLM provider that specializes in real-time information retrieval and cited answers. It operates as a proprietary cloud service with usage-based API pricing (Sonar), though Perplexity Pro subscribers receive some API credits.

## What problem it solves
It bridges the gap between static LLM knowledge and the live web. Traditional LLMs have knowledge cutoffs, but Perplexity can search the internet in real-time to provide up-to-date information with verifiable citations, solving the "stale knowledge" problem for agentic research.

## Where it fits in the stack
**Category**: Provider / AI Search. It acts as a specialized inference provider for tasks that require live data, such as news analysis, market research, or technical troubleshooting for new releases.

## Typical use cases
- **Research Agents**: Automating the collection of cited information for reports and technical audits.
- **Support Bots**: Providing accurate, up-to-date answers about products or services using live documentation.
- **Technical Research**: Finding the latest documentation or API changes that occurred after an LLM's cutoff date.
- **Financial Analysis**: Using the `finance_search` tool to pull structured market data and transcripts.
- **Autonomous Browsing**: Leveraging the "Computer" orchestration layer for multi-step web research.

### Model Routing (June 2026)
| Model | Primary Use Case | Default? |
| :--- | :--- | :--- |
| **Sonar Small / Medium** | Fast, high-volume search tasks and simple extraction | No |
| **Sonar Reasoning** | Standard research tasks requiring a balance of speed and depth | Yes |
| **Sonar Reasoning Pro** | Complex, multi-step research, deep analysis, and high-stakes reasoning | No (Premium) |
| **Agent API** | Supports third-party models like [Claude 4.8](anthropic.md) for tool-calling | No |

## Strengths
- **Live Web Access**: Exceptional at fetching and summarizing real-time data from the entire internet.
- **Citations**: Automatically provides verifiable links to the sources used to generate answers.
- **OpenAI Compatibility**: Its API is compatible with the OpenAI SDK, making it a drop-in replacement for search tasks.
- **Reasoning Models**: **Sonar Reasoning Pro** combines deep chain-of-thought with live search.
- **Tool Integration**: Native support for financial data connectors (FactSet, Morningstar, etc.).

## Limitations
- **Rate Limits**: API rate limits can be restrictive for high-volume enterprise applications.
- **Latency**: Search-augmented reasoning takes longer than a simple LLM inference call.
- **Proprietary**: No self-hosted option; requires persistent internet connection.

## When to use it
- When the accuracy of real-time information is more important than raw inference speed.
- When you need to verify the sources of an AI-generated answer.
- For "Daily Briefing" or "Market Analysis" workflows.
- For [n8n](../../services/n8n.md) workflows using the native Perplexity node.

## When not to use it
- For general creative writing or purely local processing tasks.
- When latency is a critical factor (e.g., real-time low-latency chat UI).

## Getting started

### API Setup
1. Get an API key from the [Perplexity Settings](https://www.perplexity.ai/settings/api).
2. Install the OpenAI SDK: `pip install openai`.

### Initial Configuration
```bash
export PPLX_API_KEY="your-api-key"
```

## CLI examples

### Using a Curl Command
Perplexity's OpenAI-compatible API can be tested easily via terminal:
```bash
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PPLX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-reasoning-pro",
    "messages": [{"role": "user", "content": "Latest AI news June 2026"}]
  }'
```

### Checking Model Availability
Verify the current active models in the Sonar catalog:
```bash
# Example logic using the sonar-cli tool (community)
sonar-cli models list
```

## API examples

### Python Example (OpenAI SDK)
```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("PPLX_API_KEY"), base_url="https://api.perplexity.ai")

# Chat completion with search-augmented reasoning
response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[
        {"role": "system", "content": "Be precise and cited."},
        {"role": "user", "content": "What are the latest developments in MCP 3.0 as of June 2026?"}
    ]
)

print(response.choices[0].message.content)
```

### Structured Output (JSON Mode)
```python
response = client.chat.completions.create(
    model="sonar-reasoning",
    messages=[
        {"role": "system", "content": "Return a JSON object with 'summary' and 'sources'."},
        {"role": "user", "content": "Research the current status of EKS Auto Mode."}
    ],
    response_format={ "type": "json_object" }
)
```

## Related tools / concepts
- [Tavily](tavily.md) — Search-optimized API for LLM agents.
- [OpenRouter](../ai_knowledge/openrouter.md) — Access Perplexity models via a unified gateway.
- [Google Search](../ai_knowledge/google-search.md) — Traditional search alternative.
- [n8n](../../services/n8n.md) — Workflow automation with native Perplexity support.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Strategic model placement.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for search-augmented agents.
- [Daily Briefing Prompt](../../reference-implementations/llm-prompts/daily-briefing.md) — Implementation using search.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Local alternative for non-search tasks.

## Sources / References
- [Perplexity Official Website](https://www.perplexity.ai/)
- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Perplexity Model Catalog](https://docs.perplexity.ai/docs/model-cards)
- [Sonar Reasoning Pro Reference](https://docs.perplexity.ai/docs/sonar/models/sonar-reasoning-pro)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
