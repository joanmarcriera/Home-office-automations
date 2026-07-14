# Perplexity

## What it is
Perplexity is an AI-powered conversational search engine and LLM provider that specializes in real-time information retrieval and cited answers. As of July 2026, it utilizes a sophisticated orchestration layer to route queries between frontier models like [Gemma 3](../ai_knowledge/local_llms.md), [Claude 4.8](../ai_knowledge/claude.md), and its own fine-tuned "Sonar" models. It operates as a proprietary cloud service with usage-based API pricing, bridging the gap between static LLM knowledge and the live web.

## What problem it solves
It addresses the "hallucination" and "knowledge cutoff" problems of traditional LLMs by grounding every response in current web data. Perplexity can search the internet in real-time to provide up-to-date information with verifiable citations, allowing for rapid verification of facts, technical specifications, and market trends.

## Where it fits in the stack
**Category**: Provider / AI Search. It acts as a specialized inference retrieval layer for tasks that require live data, such as news analysis, market research, or technical troubleshooting for new releases. It is often integrated into agentic workflows via its OpenAI-compatible API to provide real-time grounding for autonomous agents using [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) or [FastMCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md).

## Typical use cases
- **Technical Research**: Discovering the latest stable versions of libraries, APIs, and frameworks with cited documentation.
- **Market Intelligence**: Tracking real-time financial data, product launches, and industry trends.
- **Fact-Checking**: Verifying claims by reviewing primary sources cited in the response.
- **Research Agents**: Automating the collection of cited information for reports and technical audits.
- **Autonomous Browsing**: Leveraging the "Computer" orchestration layer for multi-step web research.

### Model Routing (July 2026)
| Model | Primary Use Case | Default? |
| :--- | :--- | :--- |
| **Sonar Small / Medium** | Fast, high-volume search tasks and simple extraction | No |
| **Sonar Reasoning** | Standard research tasks requiring a balance of speed and depth | Yes |
| **Sonar Reasoning Pro** | Complex, multi-step research, deep analysis, and high-stakes reasoning | No (Premium) |
| **Agent API** | Supports third-party models like [Claude 4.8](../ai_knowledge/claude.md) for tool-calling | No |

## Strengths
- **Verifiable Citations**: Every claim is linked to a source, drastically reducing hallucinations.
- **Live Web Access**: Exceptional at fetching and summarizing real-time data with no knowledge cutoff.
- **Model Choice**: Pro users can toggle between different frontier models for varied reasoning styles.
- **OpenAI Compatibility**: Its API is compatible with the OpenAI SDK, making it a drop-in replacement for search tasks.
- **Tool Integration**: Native support for financial data connectors and [n8n](../../services/n8n.md) workflows.

## Limitations
- **External Dependency**: As a cloud-based service, it requires internet access and third-party data processing.
- **Privacy Concerns**: Not suitable for processing highly sensitive data that cannot leave the local network.
- **API Cost**: High-volume usage via API can be more expensive than self-hosted RAG solutions.
- **Latency**: Search-augmented reasoning takes longer than simple LLM inference.

## When to use it
- When you need the most up-to-date information available on the web.
- When source verification and citations are critical for your work.
- For conductng rapid research on topics outside your immediate expertise.
- For [n8n](../../services/n8n.md) workflows using the native Perplexity node.

## When not to use it
- When working with **private, air-gapped, or highly confidential data** (use [Local LLMs](../ai_knowledge/local_llms.md)).
- When you require absolute deterministic outputs.
- When offline access is a requirement.

## Getting started

### Account Setup
Sign up at [perplexity.ai](https://www.perplexity.ai/) to access the conversational interface. API keys can be generated in the [API Settings](https://www.perplexity.ai/settings/api).

### API Setup
Perplexity provides an OpenAI-compatible API, easily manageable via [LiteLLM](../../services/litellm.md).

```bash
pip install openai
export PPLX_API_KEY="your-api-key"
```

### Minimal API Example (Python)
```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_PPLX_API_KEY", base_url="https://api.perplexity.ai")

response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[{"role": "user", "content": "What is the status of FastMCP 3.0 adoption in July 2026?"}]
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
      {"role": "user", "content": "Latest stable version of Kubernetes as of July 2026."}
    ]
  }'
```

### 2. Integration with LiteLLM CLI
```bash
litellm --model perplexity/sonar-reasoning-pro --messages '{"role": "user", "content": "Compare Gemma 3 vs Llama 4 for home-office automation."}'
```

### 3. Checking Model Availability
Verify the current active models in the Sonar catalog:
```bash
# Using the sonar-cli tool (community)
sonar-cli models list
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
        {"role": "system", "content": "Be precise and cited."},
        {"role": "user", "content": "Research the current status of EKS Auto Mode in July 2026."}
    ]
)

content = response.choices[0].message.content
print(f"Citations and Analysis: {content}")
```

### Structured Output (JSON Mode)
```python
response = client.chat.completions.create(
    model="sonar-reasoning",
    messages=[
        {"role": "system", "content": "Return a JSON object with 'summary' and 'sources'."},
        {"role": "user", "content": "Research the latest developments in MCP 3.0."}
    ],
    response_format={ "type": "json_object" }
)
```

### Integration with Agentic Frameworks
Perplexity can be used as a `tool` within agentic frameworks following [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) standards.

```python
# Simplified pseudocode for agentic tool use
def web_search(query: str):
    return client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": query}]
    ).choices[0].message.content
```

## Related tools / concepts
- [Google Search](../ai_knowledge/google-search.md) — Traditional search alternative.
- [Genspark](../ai_knowledge/genspark.md) — AI-driven research and custom page generation.
- [Tavily](tavily.md) — Search-optimized API for LLM agents.
- [OpenRouter](../ai_knowledge/openrouter.md) — Access Perplexity models via a unified gateway.
- [Gemma 3](../ai_knowledge/local_llms.md) — Canonical local LLM guide.
- [n8n](../../services/n8n.md) — Workflow automation with native Perplexity support.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Protocol for connecting search tools to agents.
- [LiteLLM](../../services/litellm.md) — Proxy for managing Perplexity API access.

## Sources / References
- [Perplexity Official Website](https://www.perplexity.ai/)
- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Perplexity Model Catalog](https://docs.perplexity.ai/docs/model-cards)
- [FastMCP 3.0 Specification](https://modelcontextprotocol.io/fastmcp)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
