# Valyu

## What it is
Valyu is an AI-native search and data retrieval API designed specifically to feed high-fidelity context, proprietary datasets, and real-time open-web research directly into LLMs and agentic workflows. By consolidating web-crawled search indexes with licensed, high-signal, and typically gated databases—such as clinical trials, PubMed, patent catalogs, arXiv, and SEC filings—Valyu acts as an intelligent aggregator that bridges frontier LLM reasoning with validated empirical data.

## What problem it solves
Traditional search engines (like Google or Bing) prioritize consumer intent, SEO-optimized web content, and low-granularity pages. AI agents performing deep clinical, financial, legal, or technical research require highly specific, cited, and peer-reviewed documentation. Valyu solves this by bypassing SEO noise, exposing "dark web" data (licensed journals and corporate documents), and returning well-structured, LLM-optimized JSON payloads complete with verified citation anchors and metadata.

## Where it fits in the stack
**AI Assistants & Knowledge / Understand (Aggregators)**. Valyu operates at the **Knowledge & Retrieval Layer**, feeding clean, citation-backed context directly into advanced RAG (Retrieval-Augmented Generation) pipelines and agentic planning steps.

## Typical use cases
- **Multi-Source Clinical Literature Review**: Programmatically scanning PubMed and clinical registries to synthesize treatment efficacy or drug side effects.
- **Financial Compliance Monitoring**: Fetching, parsing, and extracting specific quarterly data from SEC 10-K and 10-Q filings with Pydantic schema validation.
- **Academic State-of-the-Art (SOTA) Audits**: Automating the lookup of the latest publications on arXiv to compare model benchmarks (e.g., Gemini 3.5 vs. Claude 5.1).
- **Long-Horizon Deep Research**: Instantiating multi-step research loops that crawl, extract, cross-reference, and summarize technical fields under a single API call.

## Strengths
- **Unified API Access**: Query academic, clinical, financial, and patent repositories in a single unified API call.
- **Agent-First Payloads**: Output format is structured and token-optimized for LLM consumption, removing raw HTML boilerplate.
- **Built-In Citations**: Returns deterministic citation objects mapping directly to specific source sentences or table cell boundaries.
- **Deep Research Patterns**: Offers an asynchronous endpoint for deep, long-horizon research missions, generating fully structured Markdown reports natively.

## Limitations
- **API Cost**: Usage-based, premium pricing models apply due to the integration of licensed and peer-reviewed catalogs.
- **Retrieval Latency**: Deep cross-database searches have higher retrieval times compared to simple cached keyword lookups.
- **Closed-Source Aggregation**: The backend indexing pipelines, publisher licensing deals, and sorting algorithms are proprietary.

## When to use it
- When your AI agent must base its decisions, code generation, or analysis on peer-reviewed research, legal filings, or verified financial data.
- For constructing specialized knowledge agents (e.g., a "Scientific RAG Assistant") that need a high signal-to-noise ratio in their context windows.
- To feed advanced reasoning models (e.g., Claude 5.1, GPT-5.5) with highly grounded, structured context for complex reasoning tasks.

## When not to use it
- For generic, low-stakes web search queries (e.g., checking weather forecasts or restaurant operating hours) where free or standard scrapers are cheaper.
- In fully air-gapped or localized environments requiring 100% offline data indexing and search capabilities.

## Getting started

### 1. SDK Installation
Install the official Valyu client using your preferred package manager (Python 3.12+ recommended):

```bash
# Install via pip
pip install valyu

# Or install via uv (highly recommended for performance)
uv add valyu
```

### 2. Configure Your Environment
Set your API key as an environment variable to allow the client to initialize automatically:

```bash
export VALYU_API_KEY="valyu_sk_prod_xxxxxxxxxxxxxx"
```

### 3. Run a Basic Semantic Search
Execute a simple query across the standard arXiv repository to fetch relevant ML publications:

```python
from valyu import Valyu

# Initialize the client (automatically reads VALYU_API_KEY)
client = Valyu()

# Query academic literature
results = client.search(
    query="Model Context Protocol implementation in agentic workflows 2026",
    included_sources=["valyu/valyu-arxiv"]
)

for item in results:
    print(f"[{item.score:.2f}] {item.title}")
    print(f"Source URL: {item.url}\n")
```

## CLI examples

The Valyu API can be integrated directly with standard command-line tools for automated scripting and scheduled cron jobs.

### 1. Perform Direct REST API Query (curl)
Submit a POST request to search licensed financial catalogs.

```bash
curl -X POST https://api.valyu.ai/v1/search \
  -H "Authorization: Bearer $VALYU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Quantum computing hardware advancements patent landscape 2026",
    "sources": ["valyu/valyu-patents"],
    "max_results": 5
  }' | jq '.results[].title'
```

### 2. Extract Document Content via CLI
Retrieve the raw, LLM-ready text content from a specific Valyu citation ID.

```bash
# Retrieve structured markdown content from a specific academic index ID
curl -s https://api.valyu.ai/v1/documents/arxiv_doc_2604_1203 \
  -H "Authorization: Bearer $VALYU_API_KEY" | jq '.content.markdown' | head -n 30
```

### 3. Check Account Usage and Rate Limits
Verify remaining API credits and active limits on your developer dashboard.

```bash
curl -s https://api.valyu.ai/v1/usage \
  -H "Authorization: Bearer $VALYU_API_KEY" | jq .
```

## API examples

Below are production-ready API patterns demonstrating how to execute advanced research and programmatic validation using Valyu's deep features.

### 1. Programmatic Answer Synthesis (Cross-Source SEC and PubMed)
This pattern runs an analytical query over legal financial files and biomedical databases simultaneously, enforcing strict structured outputs via Pydantic v2.

```python
import os
from pydantic import BaseModel, Field
from typing import List, Optional
from valyu import Valyu

# 1. Define the desired structured output schema
class ComplianceSummary(BaseModel):
    corporation_name: str = Field(..., description="The exact legal name of the entity.")
    hazard_class: str = Field(..., description="The FDA or environmental classification of the compound.")
    regulatory_citations: List[str] = Field(..., description="List of SEC filing IDs or legal clauses cited.")
    medical_findings: str = Field(..., description="Synthesis of PubMed findings regarding compound safety.")
    confidence_score: float = Field(..., description="Self-assessed confidence in research alignment (0.0 - 1.0).")

# 2. Initialize Valyu client
client = Valyu(api_key=os.getenv("VALYU_API_KEY"))

# 3. Request structured synthesis
try:
    response = client.answer_structured(
        query="Synthesize SEC risk factors and PubMed clinical trials for Compound GLP-99 safety profiles in 2026",
        included_sources=["valyu/valyu-sec-filings", "valyu/valyu-pubmed"],
        response_model=ComplianceSummary,
        summary_instructions="Extract corporate filing declarations and cross-reference clinical trial conclusions."
    )

    # 4. Access the validated object directly
    summary: ComplianceSummary = response.data
    print(f"Company: {summary.corporation_name}")
    print(f"Hazard Class: {summary.hazard_class}")
    print(f"Medical Findings: {summary.medical_findings}")
    print(f"Citations: {summary.regulatory_citations}")
except Exception as e:
    print(f"Failed to execute structured research: {str(e)}")
```

### 2. Initiating a Long-Horizon Deep Research Task
For complex topics, trigger the deep research engine to perform an autonomous research loop.

```python
from valyu import Valyu

client = Valyu()

# Launch an asynchronous deep research task
task = client.deep_research.create(
    query="Lithium sulfur battery solid-state electrolyte degradation pathways and anode shielding 2026 SOTA",
    max_steps=12,
    priority="high"
)

print(f"Deep Research Task successfully created! Task ID: {task.id}")
print(f"Polling status...")

# Poll for completion
while task.status not in ["completed", "failed"]:
    task = client.deep_research.get(task.id)
    print(f"Current Status: {task.status} (Steps executed: {task.steps_completed}/12)")
    import time
    time.sleep(15)

if task.status == "completed":
    print("Research complete! Writing report...")
    with open("degradation_report.md", "w", encoding="utf-8") as f:
        f.write(task.report_markdown)
else:
    print(f"Research failed: {task.error_message}")
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
- [Valyu API Reference Guide](https://docs.valyu.ai/api-reference)
- [Deep Research API for AI Agents: The Complete September 2026 Guide](https://dev.to/valyuai/deep-research-api-for-ai-agents-the-complete-guide-2026-5bkl)

## Contribution Metadata
- Last reviewed: 2026-09-04
- Confidence: high
