# GPT Researcher

## What it is
GPT Researcher (v4.2+, late November 2026) is an autonomous agent designed for comprehensive online research on any given topic. It plans the research, browses the web, and synthesizes a final report with deep citations. It uses a "master-agent" and "research-agent" pattern to break down complex queries into manageable sub-tasks, now supporting multi-modal search and the **MCP 3.1 Task Protocol**.

## What problem it solves
It automates the time-consuming process of manual research, gathering information from multiple sources and producing high-quality, grounded summaries. It specifically addresses LLM hallucinations by grounding every claim in a retrieved web source (via Tavily/SearXNG) and providing a verifiable bibliography.

## Where it fits in the stack
**Category**: Agent / Research Automation. It serves as a specialized "Knowledge Acquisition" layer in an agentic stack, feeding structured data and reports into other agents or long-term memory stores like [Letta](letta.md).

## Typical use cases
- **Market Research**: Analyzing industry trends, competitor offerings, and financial reports.
- **Technical Deep Dives**: Researching new software frameworks, hardware specifications, or architectural patterns.
- **Academic/Legal Preparation**: Gathering sources, summaries, and case law for specific inquiries.
- **Daily Intelligence**: Generating automated briefings on evolving news topics or specific market sectors.
- **Agentic Knowledge Base Population**: Automatically generating documentation for new tools identified during a crawl.

## Strengths
- **High Recall**: Scrapes dozens of sources per task, far exceeding standard "search" tools or single-shot RAG.
- **Citation-First**: Every report includes a comprehensive bibliography with direct links to sources.
- **Customizable**: Allows defining specific "research tasks", tones, and report formats (PDF, Markdown, JSON).
- **Agentic Tooling**: Native support for **MCP 3.1**, allowing it to be used as a tool by other agents like [Claude 5.1](../providers/anthropic.md) or [Gemma 3](../ai_knowledge/local_llms.md).

## Limitations
- **Cost**: Scraping and synthesizing many sources can consume significant LLM tokens and API credits (Tavily).
- **Speed**: A thorough research task can take several minutes to complete as it operates asynchronously across many sources.
- **Quality Dependency**: Final report quality is heavily dependent on the quality of the underlying LLM used for synthesis and the search engine results.

## When to use it
- **Exhaustive Research**: When you need to gather information from dozens of sources simultaneously and summarize them into a single coherent report.
- **Fact-Checking**: To verify information against current web data and receive a cited bibliography for verification.
- **Automated Long-Form Synthesis**: When you need to create comprehensive, structured reports on complex topics without manual browsing.

## When not to use it
- **Real-Time Fact Retrieval**: For single-shot questions (e.g., "What is the capital of France?"), standard search tools or basic RAG are faster and cheaper.
- **Creative Writing**: It is optimized for factual synthesis and technical reporting, not creative or conversational tasks.
- **Strict Budget Constraints**: High token usage and search API costs make it expensive for high-volume, low-value tasks.

## Getting started

### Installation
```bash
pip install gpt-researcher
```

### Environment Setup
```bash
export OPENAI_API_KEY='your-key'
export TAVILY_API_KEY='your-key'
```

### Basic Usage
Run a research task via the Python API to generate a markdown report.

## CLI examples
```bash
# Run a quick research report on a topic
python -m gpt_researcher.cli "Future of solid-state batteries in 2027" --report_type research_report

# Generate a detailed, in-depth report with a specific tone
python -m gpt_researcher.cli "Impact of MCP 3.1 on agentic ecosystems" --report_type detailed_report --tone analytical

# Conduct research filtered by specific domains
python -m gpt_researcher.cli "Latest SpaceX launches" --report_type research_report --query_domains spacex.com,nasa.gov
```

## API examples

### Example: Running a Simple Research Session
```python
from gpt_researcher import GPTResearcher
import asyncio

async def run_research():
    researcher = GPTResearcher(
        query="Evolution of agentic frameworks in November 2026",
        report_type="research_report",
        tone="technical"
    )
    await researcher.conduct_research()
    report = await researcher.write_report()
    return report
```

### Example: Programmatic Web Scraping and Citation Validation
In order to guarantee that all scraped data feeds are valid and carry legitimate, parseable URLs and metadata, GPT Researcher workflows utilize **Pydantic v2** validation before compiling report bibliographies.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator

# Define Pydantic v2 schemas for validating scraped sources
class ScrapedCitation(BaseModel):
    title: str = Field(..., min_length=2, description="Title of the source webpage")
    url: HttpUrl = Field(..., description="Fully qualified HTTP/HTTPS url of the source")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Confidence rating of source relevance")
    summary: str = Field(..., description="Extracted relevant summary text")

class ResearchReport(BaseModel):
    topic: str = Field(..., description="Query topic")
    sources: List[ScrapedCitation]
    synthesized_markdown: str = Field(..., min_length=10, description="The main compiled report content")

    @field_validator('sources')
    @classmethod
    def enforce_minimum_citations(cls, citations_list: List[ScrapedCitation]) -> List[ScrapedCitation]:
        # Enforce that a high-quality report must ground its findings in at least 2 citations
        if len(citations_list) < 2:
            raise ValueError("High-quality research reports must include at least two distinct citations.")
        return citations_list

def parse_and_validate_report(raw_data: dict) -> Optional[ResearchReport]:
    try:
        validated_report = ResearchReport.model_validate(raw_data)
        print(f"Report validated successfully for topic: '{validated_report.topic}'")
        print(f"Citations Verified: {len(validated_report.sources)}")
        for i, src in enumerate(validated_report.sources):
            print(f"  [{i+1}] {src.title} -> {src.url}")
        return validated_report
    except Exception as e:
        print(f"Research report validation failed: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initializing GPT Researcher citation validator (Pydantic v2)...")

    # Valid payload containing two distinct citations
    valid_payload = {
        "topic": "FastMCP 3.1 optimization benchmarks",
        "sources": [
            {
                "title": "Model Context Protocol 3.1 Specifications",
                "url": "https://modelcontextprotocol.io/spec/3.1",
                "relevance_score": 0.98,
                "summary": "Introduces high-throughput session protocols and multi-threading parameters."
            },
            {
                "title": "FastMCP benchmarking on local Gemma 3 models",
                "url": "https://huggingface.co/blog/gemma-3-mcp",
                "relevance_score": 0.89,
                "summary": "Demonstrates sub-10ms tool call latency when run locally."
            }
        ],
        "synthesized_markdown": "## Executive Summary\\n\\nFastMCP 3.1 represents a massive leap in low-latency orchestration..."
    }

    parse_and_validate_report(valid_payload)
```

## Related tools / concepts
- [Tavily](../providers/tavily.md)
- [Perplexity Agent API](perplexity-agent-api.md)
- [Crawl4AI](../process_understanding/crawl4ai.md)
- [SearXNG Automation](../../services/searXNG-automation.md)
- [Letta](letta.md)
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Claude 5.1](../ai_knowledge/claude.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Search Patterns](../../knowledge_base/patterns/search-patterns.md)

## Sources / references
- [GPT Researcher GitHub Repository](https://github.com/assafelovic/gpt-researcher)
- [GPT Researcher Official Documentation](https://docs.gptr.dev/)

## Contribution Metadata
- Last reviewed: 2026-11-27
- Confidence: high
