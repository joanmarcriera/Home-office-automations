# Valyu

## What it is
Valyu is an AI-native search API that provides agents with access to both the open web and licensed, high-signal proprietary data sources.

## What problem it solves
It allows agents to search beyond just the current web, providing structured, high-accuracy results from datasets like PubMed, SEC filings, clinical trials, patents, arXiv, and financial data through a single, natural-language-enabled API.

## Where it fits in the stack
**AI Assistants & Knowledge / Understand (Aggregators)**. It acts as a high-signal search engine that feeds real-time context and deep research data to LLMs and agents.

## Typical use cases
- **Deep Research**: Running complex queries that require cross-referencing web search with research papers (arXiv) or patents.
- **Financial Analysis**: Extracting real-time market data or historical SEC filings.
- **Medical/Scientific Agents**: Searching PubMed or clinical trials for verified medical information.
- **RAG Enrichment**: Feeding high-fidelity, citation-backed data into retrieval-augmented generation pipelines.

## Technical Capabilities
- **Search API**: Core semantic search across 36+ proprietary sources and the open web.
- **Answer API**: Returns AI-synthesized answers grounded in search results with inline citations.
- **Deep Research API**: Performs multi-step, autonomous research plans and returns structured reports.
- **Content API**: High-quality Markdown extraction and structured data parsing from URLs.

## Strengths
- **Unified API**: Access to licensed repositories (PubMed, SEC, Wiley) in a single request.
- **Agent-Ready**: Returns structured, LLM-ready data rather than just a list of links.
- **High Recall**: Accesses "dark data" not indexable by standard search bots.
- **Citations**: Native support for source attribution in the Answer and Deep Research endpoints.

## Limitations
- **Paid Service**: Requires an API key and usage-based pricing.
- **Latency**: Searching proprietary databases can sometimes be slower than simple web-index searches.
- **Closed-Source**: The search engine itself is a proprietary service.

## When to use it
- When an agent needs high-accuracy, verified data from scientific, financial, or legal sources.
- For building specialized agents (e.g., a "Scientific Research Agent") that require more than just web results.

## When not to use it
- For general, low-stakes web search where free or cheaper alternatives suffice.
- If you require a fully open-source, self-hosted search index.

## Implementation: Cross-Source Answer API
The following example demonstrates using the `Answer` API to synthesize findings across scientific literature and regulatory filings.

```python
from valyu import Valyu

# Initialize the client
client = Valyu(api_key="your-api-key")

# Perform a grounded answer query across specific proprietary sources
response = client.answer(
    query="Analyze the impact of GLP-1 agonists on healthcare provider stock volatility in 2024",
    included_sources=["valyu/valyu-pubmed", "valyu/valyu-sec-filings"],
    summary_instructions="Provide a structured analysis with citations from both medical and financial sources.",
    response_length="large"
)

print(f"Answer: {response.answer}")
for citation in response.citations:
    print(f"[{citation.id}] {citation.title} ({citation.url})")
```

## Implementation: Deep Research Pattern
For long-horizon tasks, use the Deep Research API to generate comprehensive reports.

```python
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

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Usage-based pricing with free tier)
- **Self-hostable**: No

## Related tools / concepts
- [Perplexity](perplexity.md)
- [OpenRouter](openrouter.md)
- [LlamaIndex](llamaindex.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [Firecrawl](../process_understanding/firecrawl.md)
- [DeepSeek R1](../providers/deepseek.md)
- [Search-as-a-Service Patterns](../../knowledge_base/patterns/claude-tool-search.md)

## Sources / References
- [Official Website](https://www.valyu.ai/)
- [Official Docs](https://docs.valyu.ai/)
- [Valyu API Reference](https://docs.valyu.ai/api-reference)
- [Deep Research Guide (2026)](https://dev.to/valyuai/deep-research-api-for-ai-agents-the-complete-guide-2026-5bkl)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
