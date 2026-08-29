# Perplexity

## What it is
Perplexity is an AI-powered conversational search engine and LLM provider that specializes in real-time information retrieval and cited answers. As of January 2027, it utilizes a sophisticated orchestration layer to route queries between frontier models like [Gemma 4](../ai_knowledge/local_llms.md), [Claude 5.6](../ai_knowledge/claude.md), GPT-5.6, Gemini 4.0 Ultra, and its own fine-tuned "Sonar" models. It operates as a proprietary cloud service with usage-based API pricing, bridging the gap between static LLM knowledge and the live web.

## What problem it solves
It addresses the "hallucination" and "knowledge cutoff" problems of traditional LLMs by grounding every response in current web data. Perplexity can search the internet in real-time to provide up-to-date information with verifiable citations, allowing for rapid verification of facts, technical specifications, and market trends.

## Where it fits in the stack
**Category**: Provider / AI Search. It acts as a specialized inference retrieval layer for tasks that require live data, such as news analysis, market research, or technical troubleshooting for new releases. It is often integrated into agentic workflows via its OpenAI-compatible API to provide real-time grounding for autonomous agents using [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) or **FastMCP 3.1** standards.

## Typical use cases
- **Technical Research**: Discovering the latest stable versions of libraries, APIs, and frameworks with cited documentation.
- **Market Intelligence**: Tracking real-time financial data, product launches, and industry trends.
- **Fact-Checking**: Verifying claims by reviewing primary sources cited in the response.
- **Research Agents**: Automating the collection of cited information for reports and technical audits.
- **Autonomous Browsing**: Leveraging the "Computer" orchestration layer for multi-step web research.

### Model Routing (January 2027)
| Model | Primary Use Case | Default? |
| :--- | :--- | :--- |
| **Sonar Small / Medium** | Fast, high-volume search tasks and simple extraction | No |
| **Sonar Reasoning** | Standard research tasks requiring a balance of speed and depth | Yes |
| **Sonar Reasoning Pro** | Complex, multi-step research, deep analysis, and high-stakes reasoning | No (Premium) |
| **Agent API** | Supports third-party models like [Claude 5.6](../ai_knowledge/claude.md) for tool-calling | No |

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
- For conducting rapid research on topics outside your immediate expertise.
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
pip install openai pydantic
export PPLX_API_KEY="your-api-key"
```

### Minimal API Example (Python)
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("PPLX_API_KEY", "mock-key"),
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[{"role": "user", "content": "What is the status of FastMCP 3.1 adoption in January 2027?"}]
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
      {"role": "user", "content": "Latest stable version of Kubernetes as of January 2027."}
    ]
  }'
```

### 2. Integration with LiteLLM CLI
```bash
litellm --model perplexity/sonar-reasoning-pro --messages '{"role": "user", "content": "Compare Gemma 4 vs Llama 4 Maverick for home-office automation."}'
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
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("PPLX_API_KEY", "mock-key"),
    base_url="https://api.perplexity.ai"
)

# Using 'sonar-reasoning-pro' for complex research tasks
response = client.chat.completions.create(
    model="sonar-reasoning-pro",
    messages=[
        {"role": "system", "content": "Be precise and cited."},
        {"role": "user", "content": "Research the current status of EKS Auto Mode in January 2027."}
    ]
)

content = response.choices[0].message.content
print(f"Citations and Analysis: {content}")
```

### Structured Output and Schema Validation (Pydantic v2)
This example demonstrates how to retrieve and strictly validate search results from Perplexity's API using **Pydantic v2**.

```python
import os
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

# Initialize OpenAI client to connect to Perplexity's API
client = OpenAI(
    api_key=os.environ.get("PPLX_API_KEY", "mock-key"),
    base_url="https://api.perplexity.ai"
)

# Define Pydantic v2 structured response schema for search outcomes
class SearchCitation(BaseModel):
    source_url: str = Field(description="URL of the cited source")
    relevance_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score of relevance")

class SearchResponse(BaseModel):
    summary: str = Field(description="Synthesized summary of the search results")
    citations: list[SearchCitation] = Field(default_factory=list, description="List of source citations")

try:
    response = client.chat.completions.create(
        model="sonar-reasoning-pro",
        messages=[
            {"role": "system", "content": "You are a precise search parser. Output JSON matching the requested schema strictly."},
            {"role": "user", "content": "Query: What is the current status of FastMCP 3.1 adoption in January 2027?"}
        ],
        response_format={
            "type": "json_object",
            "schema": SearchResponse.model_json_schema()
        }
    )

    # Parse and validate using Pydantic v2 model_validate_json
    raw_content = response.choices[0].message.content
    search_data = SearchResponse.model_validate_json(raw_content)
    print(f"Summary: {search_data.summary}")
    print(f"Citations: {len(search_data.citations)} sources verified.")

except ValidationError as e:
    print(f"Pydantic validation error: {e}")
except Exception as e:
    print(f"Request failed: {e}")
```

### Integration with Agentic Frameworks
Perplexity can be used as a `tool` within agentic frameworks following [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) / FastMCP 3.1 standards.

```python
# Simplified pseudocode for agentic tool use
def web_search(query: str):
    return client.chat.completions.create(
        model="sonar-reasoning-pro",
        messages=[{"role": "user", "content": query}]
    ).choices[0].message.content
```

## Related tools / concepts
- [Google Search](../ai_knowledge/google-search.md) — Traditional search alternative.
- [Genspark](../ai_knowledge/genspark.md) — AI-driven research and custom page generation.
- [Tavily](tavily.md) — Search-optimized API for LLM agents.
- [OpenRouter](../ai_knowledge/openrouter.md) — Access Perplexity models via a unified gateway.
- [Gemma 4](../ai_knowledge/local_llms.md) — Canonical local LLM guide.
- [n8n](../../services/n8n.md) — Workflow automation with native Perplexity support.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Protocol for connecting search tools to agents.
- [LiteLLM](../../services/litellm.md) — Proxy for managing Perplexity API access.

## Sources / References
- [Perplexity Official Website](https://www.perplexity.ai/)
- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Perplexity Model Catalog](https://docs.perplexity.ai/docs/model-cards)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
