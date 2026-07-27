# Valyu

## What it is
Valyu is an AI-native search API that provides agents with access to both the open web and licensed, high-signal proprietary data sources. As of late August/September 2026, it is a key integration endpoint for frontier models conducting complex semantic searches and grounded retrieval.

## What problem it solves
It allows agents to search beyond just the current public web, providing structured, high-accuracy results from premium, difficult-to-scrape datasets like PubMed, SEC filings, clinical trials, patents, arXiv, and financial data through a single, natural-language-enabled API.

## Where it fits in the stack
**AI Assistants & Knowledge / Understand (Aggregators)**. It acts as a high-signal search engine and data integration layer that feeds real-time context and deep research data to LLMs and agents.

## Typical use cases
- **Deep Research**: Running complex queries that require cross-referencing web search with research papers (arXiv) or patents.
- **Financial Analysis**: Extracting real-time market data or historical SEC filings.
- **Medical/Scientific Agents**: Searching PubMed or clinical trials for verified medical information.
- **RAG Enrichment**: Feeding high-fidelity, citation-backed data into retrieval-augmented generation pipelines using Model Context Protocol (MCP 3.1).

## Strengths
- **Unified API**: Access to licensed repositories (PubMed, SEC, Wiley) in a single request.
- **Agent-Ready**: Returns structured, LLM-ready data rather than just a list of links.
- **High Recall**: Accesses "dark data" not indexable by standard search bots.
- **Citations**: Native support for source attribution in the Answer and Deep Research endpoints.

## Limitations
- **Paid Service**: Requires an API key and usage-based pricing.
- **Latency**: Searching proprietary databases can sometimes be slower than simple web-index searches.
- **Closed-Source**: The search engine itself is a proprietary service.
- **Reasoning Overhead**: While it provides the data, the final synthesis still depends on the reasoning capabilities of the consuming frontier models (e.g., Claude 5.1, GPT-5.5, or Llama 4).

## When to use it
- When an agent needs high-accuracy, verified data from scientific, financial, or legal sources.
- For building specialized agents (e.g., a "Scientific Research Agent") that require more than just web results.
- To provide frontier models like Claude 5.1, GPT-5.5, or Gemini 3.5 series with grounded, verifiable context for deep reasoning tasks using high-signal research patterns.

## When not to use it
- For general, low-stakes web search where free or cheaper alternatives suffice.
- If you require a fully open-source, self-hosted search index.

## Getting started

### Installation
Install the Valyu Python SDK via `pip` or `uv`:

```bash
pip install valyu
# or
uv add valyu
```

### Basic Usage
Initialize the client and perform a simple semantic search across all sources.

```python
from valyu import Valyu
import os

# Initialize with API key from environment
client = Valyu(api_key=os.getenv("VALYU_API_KEY"))

# Basic search query
results = client.search(query="Latest developments in room-temperature superconductors")

for result in results:
    print(f"[{result.score:.2f}] {result.title}")
    print(f"URL: {result.url}\n")
```

## CLI examples
> [!NOTE]
> Official CLI examples for Valyu are primarily managed through SDK integrations or direct API calls. A standalone CLI for end-users is not currently promoted in the official 2026 documentation.

### 1. Execute Search Query via curl
Submit a raw semantic query to the Valyu endpoint for arXiv research.

```bash
curl -X POST https://api.valyu.ai/v1/search \
  -H "Authorization: Bearer $VALYU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest breakthroughs in fusion energy 2026", "source": "valyu/valyu-arxiv"}'
```

### 2. Check Service Status
Verify API key validity and service status from the command line.

```bash
curl -I https://api.valyu.ai/v1/status \
  -H "Authorization: Bearer $VALYU_API_KEY"
```

## API examples

### Cross-Source Answer API (Pydantic v2)
The following example demonstrates using the `Answer` API to synthesize findings across scientific literature and regulatory filings, leveraging Pydantic v2 validation.

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from valyu import Valyu

class AnswerCitation(BaseModel):
    id: str
    title: str
    url: Optional[str] = None

class GroundedAnswerResponse(BaseModel):
    answer: str
    citations: List[AnswerCitation]

# Initialize the client
client = Valyu(api_key="your-api-key")

# Perform a grounded answer query across specific proprietary sources
raw_response = client.answer(
    query="Analyze the impact of GLP-1 agonists on healthcare provider stock volatility in 2026",
    included_sources=["valyu/valyu-pubmed", "valyu/valyu-sec-filings"],
    summary_instructions="Provide a structured analysis with citations from both medical and financial sources.",
    response_length="large"
)

# Parse and validate with Pydantic v2
validated_response = GroundedAnswerResponse(
    answer=raw_response.get("answer", ""),
    citations=[
        AnswerCitation(id=c.get("id"), title=c.get("title"), url=c.get("url"))
        for c in raw_response.get("citations", [])
    ]
)

print(f"Answer: {validated_response.answer}")
for citation in validated_response.citations:
    print(f"[{citation.id}] {citation.title} ({citation.url})")
```

### Deep Research Pattern
For long-horizon tasks, use the Deep Research API to generate comprehensive reports.

```python
from valyu import Valyu

# Initialize the client
client = Valyu(api_key="your-api-key")

# Deep Research for a specific market landscape
report = client.deep_research(
    query="Future of solid-state battery manufacturing: key players, patent landscape, and supply chain risks",
    output_format="markdown",
    max_steps=10
)

# Save the generated research report
with open("solid_state_research.md", "w") as f:
    f.write(report.content)
```

## Related tools / concepts
- [Perplexity](../providers/perplexity.md)
- [OpenRouter](openrouter.md)
- [LlamaIndex](llamaindex.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [Firecrawl](../process_understanding/firecrawl.md)
- [Exa AI](../providers/exa_ai.md)
- [Tavily](../providers/tavily.md)
- [DeepSeek R1](../providers/deepseek.md)
- [Search-as-a-Service Patterns](../../knowledge_base/patterns/claude-tool-search.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://www.valyu.ai/)
- [Official Docs](https://docs.valyu.ai/)
- [Valyu API Reference](https://docs.valyu.ai/api-reference)
- [Deep Research Guide (2026)](https://dev.to/valyuai/deep-research-api-for-ai-agents-the-complete-guide-2026-5bkl)

## Contribution Metadata
- Last reviewed: 2026-09-03
- Confidence: high
